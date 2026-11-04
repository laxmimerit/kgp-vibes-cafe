---
name: menu-import
description: it imports a whole new weekly menu from source/KGP_Vibes_Cafe_Menu.pdf; use it only when a new weekly menu PDF arrives, never for a single item.
---

# Menu Import

Follow these steps to perform the weekly cafe menu update and keep all menu data and assets synchronized.

## Steps

1. **Import the new menu from source PDF into baseline data**
   - Run the dedicated menu import script to read `source/KGP_Vibes_Cafe_Menu.pdf` and update `baseline/menu.csv`:
     ```bash
     python .agents/skills/menu-import/scripts/import_menu.py
     ```
   - This matches items by name, preserves existing item IDs, descriptions, and non-PDF attributes (`diet`, `contains_egg`, `pairs_with`, `food_cost_usd`), updates names, categories, and USD prices with two decimal places, handles adding or removing items, and never adds duplicates.

2. **Sync the website menu**
   - Run the synchronization script to propagate updates from `baseline/menu.csv` to `site/data/menu.csv`, `site/public/data/menu.csv`, and `site/data/menu.json`:
     ```bash
     python scripts/sync_menu.py
     ```

3. **Rebuild the website**
   - Build the Next.js site to ensure all static pages and bundles reflect the updated menu data:
     ```bash
     cd site && npm run build && cd ..
     ```

4. **Regenerate the menu card**
   - Regenerate the print-ready table menu cards (`print/menu_a4.pdf` and `print/menu_letter.pdf`):
     ```bash
     python scripts/generate_menu_card.py
     ```

5. **Run the order test**
   - Run the end-to-end order flow test to verify that ordering works as expected with the updated menu:
     ```bash
     python scripts/test_order_flow.py
     ```
