#!/usr/bin/env python3
"""
import_menu.py
Reads cafe menu items from a source PDF and updates baseline/menu.csv.
- Matches items by name (case-insensitive)
- Only changes names, prices, and categories for existing items
- Keeps existing descriptions intact (does not overwrite existing descriptions with PDF wording)
- Retains existing item_id and columns not present in the PDF (diet, contains_egg, pairs_with, food_cost_usd)
- Adds new items present in the PDF that are not in the CSV
- Removes items from the CSV that are no longer present in the PDF
- Never adds duplicate items
- Formats prices in USD with two decimal places (e.g., 2.50, 3.75)
- Idempotent: reports zero changes when run repeatedly without changes in the PDF
"""

import argparse
import csv
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

try:
    import pypdf
except ImportError:
    print("Error: pypdf is required to read menu PDFs. Run 'pip install pypdf'.", file=sys.stderr)
    sys.exit(1)

# Canonical mapping for menu sections to standard CSV categories
SECTION_TO_CATEGORY = {
    "COFFEE": "Coffee",
    "SNACKS & MEALS": "Snacks & Meals",
    "MEALS": "Meals",
    "DESSERTS & DRINKS": "Desserts & Drinks",
}

# Standard column headers expected in baseline/menu.csv
CSV_HEADERS = [
    "item_id",
    "name",
    "category",
    "description",
    "price_usd",
    "diet",
    "contains_egg",
    "pairs_with",
    "food_cost_usd",
]


def extract_items_from_pdf(pdf_path: str) -> List[Dict[str, str]]:
    """Extract menu items (name, category, price_usd, description) from PDF."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = pypdf.PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            full_text += txt + "\n"

    lines = [l.strip() for l in full_text.splitlines() if l.strip()]

    items: List[Dict[str, str]] = []
    current_category: Optional[str] = None
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for section header
        upper_line = line.upper()
        if upper_line in SECTION_TO_CATEGORY:
            current_category = SECTION_TO_CATEGORY[upper_line]
            i += 1
            continue

        # Check for item header line: Name ... $Price
        # Pattern handles varying numbers of dots and optional spaces
        item_match = re.match(r"^(.+?)\s*\.{2,}\s*\$?(\d+(?:\.\d{1,2})?)$", line)
        if item_match and current_category:
            item_name = item_match.group(1).strip()
            raw_price = float(item_match.group(2).strip())
            price_usd = f"{raw_price:.2f}"

            # Next line may be description if not a section header, item line, or footer
            description = ""
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_upper = next_line.upper()
                is_next_section = next_upper in SECTION_TO_CATEGORY
                is_next_item = bool(re.match(r"^(.+?)\s*\.{2,}\s*\$?(\d+(?:\.\d{1,2})?)$", next_line))
                is_footer = next_upper.startswith("KGP VIBES") or next_upper.startswith("EST 2025") or next_upper == "MENU"

                if not is_next_section and not is_next_item and not is_footer:
                    description = next_line.strip()
                    i += 1

            items.append({
                "name": item_name,
                "category": current_category,
                "price_usd": price_usd,
                "description": description,
            })

        i += 1

    return items


def generate_next_item_id(existing_ids: set, category: str) -> str:
    """Generate a clean item_id for a new item based on its category prefix."""
    prefix_map = {
        "Coffee": "C",
        "Snacks & Meals": "S",
        "Meals": "M",
        "Desserts & Drinks": "D",
    }
    prefix = prefix_map.get(category, "X")
    for n in range(1, 100):
        candidate = f"{prefix}{n:02d}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
    return f"{prefix}{len(existing_ids) + 1:03d}"


def update_menu_csv(pdf_items: List[Dict[str, str]], csv_path: str) -> Tuple[int, int, int, List[str]]:
    """
    Update baseline/menu.csv with items extracted from the PDF.
    Only updates names, prices, and categories for existing items.
    Preserves existing descriptions.
    Adds new items and removes deleted items.
    Returns: (updated_count, added_count, removed_count, change_logs)
    """
    existing_rows: List[Dict[str, str]] = []
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_rows = list(reader)

    # Index existing rows by normalized name
    existing_by_name: Dict[str, Dict[str, str]] = {}
    existing_ids = set()
    for row in existing_rows:
        norm_name = row["name"].strip().lower()
        existing_by_name[norm_name] = row
        if "item_id" in row and row["item_id"].strip():
            existing_ids.add(row["item_id"].strip())

    changes_logged: List[str] = []
    updated_count = 0
    added_count = 0
    removed_count = 0

    # Build unique set of PDF items and track seen names to prevent duplicates
    pdf_by_name: Dict[str, Dict[str, str]] = {}
    for item in pdf_items:
        norm_name = item["name"].strip().lower()
        if norm_name not in pdf_by_name:
            pdf_by_name[norm_name] = item

    # 1. Update existing items and handle removals
    new_rows: List[Dict[str, str]] = []
    for row in existing_rows:
        norm_name = row["name"].strip().lower()
        if norm_name not in pdf_by_name:
            # Item is no longer in the PDF -> remove it
            removed_count += 1
            changes_logged.append(f"Removed item '{row['name']}' (ID: {row.get('item_id', '')})")
            continue

        item = pdf_by_name[norm_name]
        item_changes = []

        # Update category if changed
        if item["category"] and row.get("category") != item["category"]:
            old_cat = row.get("category", "")
            row["category"] = item["category"]
            item_changes.append(f"category: '{old_cat}' -> '{item['category']}'")

        # Update price_usd if changed
        old_price = row.get("price_usd", "").strip()
        if old_price != item["price_usd"]:
            row["price_usd"] = item["price_usd"]
            item_changes.append(f"price: ${old_price} -> ${item['price_usd']}")

        # Update name if casing changed
        if row.get("name") != item["name"]:
            old_name = row.get("name", "")
            row["name"] = item["name"]
            item_changes.append(f"name: '{old_name}' -> '{item['name']}'")

        # Note: description is deliberately NOT modified for existing items.
        # Existing description is preserved.

        if item_changes:
            updated_count += 1
            changes_logged.append(f"Updated '{item['name']}': {', '.join(item_changes)}")

        new_rows.append(row)

    # 2. Add any new items present in PDF but not in CSV
    for norm_name, item in pdf_by_name.items():
        if norm_name not in existing_by_name:
            new_id = generate_next_item_id(existing_ids, item["category"])
            new_row = {
                "item_id": new_id,
                "name": item["name"],
                "category": item["category"],
                "description": item["description"],
                "price_usd": item["price_usd"],
                "diet": "veg",
                "contains_egg": "no",
                "pairs_with": "",
                "food_cost_usd": f"{(float(item['price_usd']) * 0.3):.2f}",
            }
            new_rows.append(new_row)
            added_count += 1
            changes_logged.append(f"Added new item '{item['name']}' (ID: {new_id}, ${item['price_usd']})")

    # Only rewrite CSV if there were actual updates, additions, or removals
    if updated_count > 0 or added_count > 0 or removed_count > 0:
        os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
        with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for row in new_rows:
                row_dict = {col: row.get(col, "") for col in CSV_HEADERS}
                writer.writerow(row_dict)

    return updated_count, added_count, removed_count, changes_logged


def main():
    parser = argparse.ArgumentParser(description="Import cafe menu from PDF into baseline/menu.csv")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    default_pdf = os.path.join(base_dir, "source", "KGP_Vibes_Cafe_Menu.pdf")
    default_csv = os.path.join(base_dir, "baseline", "menu.csv")

    parser.add_argument("--pdf", default=default_pdf, help="Path to source menu PDF")
    parser.add_argument("--csv", default=default_csv, help="Path to destination menu CSV")

    args = parser.parse_args()

    print(f"Reading menu from PDF: {args.pdf}")
    items = extract_items_from_pdf(args.pdf)
    print(f"Extracted {len(items)} items across categories.")

    updated_count, added_count, removed_count, changes = update_menu_csv(items, args.csv)

    if updated_count == 0 and added_count == 0 and removed_count == 0:
        print(f"✓ No changes detected. {args.csv} is already up to date (0 items modified).")
    else:
        print(f"✓ Menu update complete: {updated_count} items updated, {added_count} items added, {removed_count} items removed.")
        for change in changes:
            print(f"  - {change}")


if __name__ == "__main__":
    main()
