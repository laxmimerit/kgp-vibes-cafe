"""
Script to synchronize baseline/menu.csv to site/data/menu.csv, site/public/data/menu.csv,
and site/data/menu.json.
Ensures single source of truth for the menu across the cafe Next.js application.
"""
import csv
import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_MENU_CSV = os.path.join(BASE_DIR, "baseline", "menu.csv")
DEST_MENU_CSV = os.path.join(BASE_DIR, "site", "data", "menu.csv")
DEST_PUBLIC_MENU_CSV = os.path.join(BASE_DIR, "site", "public", "data", "menu.csv")
DEST_MENU_JSON = os.path.join(BASE_DIR, "site", "data", "menu.json")

def sync_menu():
    if not os.path.exists(SRC_MENU_CSV):
        raise FileNotFoundError(f"Source menu CSV not found at {SRC_MENU_CSV}")

    os.makedirs(os.path.dirname(DEST_MENU_CSV), exist_ok=True)
    os.makedirs(os.path.dirname(DEST_PUBLIC_MENU_CSV), exist_ok=True)

    # 1. Copy CSV file directly to both locations
    shutil.copyfile(SRC_MENU_CSV, DEST_MENU_CSV)
    shutil.copyfile(SRC_MENU_CSV, DEST_PUBLIC_MENU_CSV)
    print(f"Copied {SRC_MENU_CSV} -> {DEST_MENU_CSV} & {DEST_PUBLIC_MENU_CSV}")

    # 2. Parse CSV to structured JSON
    items = []
    with open(SRC_MENU_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row["item_id"].strip()
            img_path = os.path.join(BASE_DIR, "site", "public", "images", "menu", f"{item_id}.jpg")
            has_photo = os.path.exists(img_path)
            items.append({
                "id": item_id,
                "name": row["name"].strip(),
                "category": row["category"].strip(),
                "description": row["description"].strip(),
                "price": float(row["price_usd"].strip()),
                "diet": row["diet"].strip(),
                "containsEgg": row["contains_egg"].strip().lower() == "yes",
                "pairsWith": row["pairs_with"].strip(),
                "foodCost": float(row["food_cost_usd"].strip()),
                "hasPhoto": has_photo
            })

    # Write JSON for Next.js imports
    with open(DEST_MENU_JSON, mode="w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    print(f"Generated {DEST_MENU_JSON} with {len(items)} items.")

if __name__ == "__main__":
    sync_menu()
