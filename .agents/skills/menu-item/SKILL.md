---
name: menu-item
description: it adds, changes or removes one item on the cafe menu (menu data, price format, photo or placeholder, build, order test); use it whenever the user asks to add, change or remove a single menu item.
---

# Menu Item

Follow these steps to add a single new item to the cafe menu while keeping menu data, prices, assets, and tests in sync.

> [!NOTE]
> Do not display calendar dates or years anywhere. Format all prices in USD with two decimal places.

---

## Steps

### 1. Determine the Next Free ID for the Category
- Inspect the existing items in `baseline/menu.csv` and identify the item's category.
- Standard category prefixes:
  - **Coffee**: `C` (e.g., `C01`, `C02`, ... `C12` -> next is `C13`)
  - **Snacks & Meals**: `S` (e.g., `S01`, `S02`, ... `S09` -> next is `S10`)
  - **Meals**: `M` (e.g., `M01`, `M02`, ... `M09` -> next is `M10`)
  - **Desserts & Drinks**: `D` (e.g., `D01`, `D02`, ... `D09` -> next is `D10`)
- Find the highest numerical ID currently used in that category and increment it using two-digit zero-padding (e.g., `C13`, `S10`).

### 2. Write the Price in USD with Two Decimals
- Ensure the price is formatted in USD with two decimal places (e.g., `2.50`, `3.75`, `4.00`), matching the Cafe House Rules and the standard in `baseline/menu.csv`.

### 3. Add the Item to `baseline/menu.csv` and `site/data/menu.json`
- **In `baseline/menu.csv`**:
  Append a new row adhering to the CSV schema:
  ```csv
  item_id,name,category,description,price_usd,diet,contains_egg,pairs_with,food_cost_usd
  ```
  Example:
  ```csv
  C13,Hazelnut Cold Brew,Coffee,"Cold brew infused with roasted hazelnut syrup.",4.50,vegan,no,Binary Bagel,1.15
  ```
- **In `site/data/menu.json`**:
  Add the matching JSON object with the appropriate keys (`id`, `name`, `category`, `description`, `price`, `diet`, `containsEgg`, `pairsWith`, `foodCost`):
  ```json
  {
    "id": "C13",
    "name": "Hazelnut Cold Brew",
    "category": "Coffee",
    "description": "Cold brew infused with roasted hazelnut syrup.",
    "price": 4.5,
    "diet": "vegan",
    "containsEgg": false,
    "pairsWith": "Binary Bagel",
    "foodCost": 1.15
  }
  ```
- **Sync**:
  Alternatively or additionally, run `python scripts/sync_menu.py` to synchronize `baseline/menu.csv` across `site/data/menu.csv`, `site/public/data/menu.csv`, and `site/data/menu.json`.

### 4. Check Photo and Card Placeholder Handling
- Check if an image exists at `site/public/images/menu/<id>.jpg`.
- If the item has no photo in `site/public/images/menu`, verify that a clean placeholder is shown on its card instead of a broken image (the menu card component handles missing images via fallback error state, rendering a clean placeholder badge with the category icon and name).

### 5. Build the Site
- Build the Next.js site to ensure all static pages and bundles compile properly:
  ```bash
  cd site && npm run build && cd ..
  ```

### 6. Run the Order Test
- Run the end-to-end order flow test to verify that the ordering workflow succeeds with the updated menu:
  ```bash
  python scripts/test_order_flow.py
  ```
