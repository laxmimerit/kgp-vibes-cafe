/**
 * menu-loader.js
 * Loads and provides access to KGP Vibes Cafe menu items.
 * Supports static pre-bundled data (window.MENU_DATA) and dynamic CSV fetching.
 */

const MenuLoader = {
  items: [],

  async loadMenu() {
    // If pre-bundled by scripts/sync_menu.py, use that immediately
    if (window.MENU_DATA && Array.isArray(window.MENU_DATA) && window.MENU_DATA.length > 0) {
      this.items = window.MENU_DATA;
      return this.items;
    }

    // Otherwise attempt fetching data/menu.csv
    try {
      const response = await fetch('data/menu.csv');
      if (response.ok) {
        const text = await response.text();
        this.items = this.parseCSV(text);
        return this.items;
      }
    } catch (e) {
      console.warn("Could not fetch data/menu.csv directly, checking fallback", e);
    }

    return this.items;
  },

  parseCSV(text) {
    const lines = text.trim().split('\n');
    if (lines.length <= 1) return [];

    const items = [];
    // Skip header line
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      // Handle quotes with commas inside
      const row = [];
      let inQuotes = false;
      let field = '';

      for (let c = 0; c < line.length; c++) {
        const char = line[c];
        if (char === '"') {
          inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
          row.push(field.trim());
          field = '';
        } else {
          field += char;
        }
      }
      row.push(field.trim());

      if (row.length >= 9) {
        items.push({
          id: row[0],
          name: row[1],
          category: row[2],
          description: row[3],
          price: parseFloat(row[4]),
          diet: row[5],
          containsEgg: row[6].toLowerCase() === 'yes',
          pairsWith: row[7],
          foodCost: parseFloat(row[8])
        });
      }
    }

    return items;
  },

  getItemById(id) {
    return this.items.find(item => item.id === id);
  },

  formatPrice(price) {
    return '$' + Number(price).toFixed(2);
  }
};
