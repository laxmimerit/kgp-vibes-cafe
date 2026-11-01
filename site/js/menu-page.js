/**
 * menu-page.js
 * Handles menu rendering, category filtering, dietary filtering, search,
 * and direct addition to cart from the menu page.
 */

document.addEventListener('DOMContentLoaded', async () => {
  const menuContainer = document.getElementById('menu-items-grid');
  const searchInput = document.getElementById('menu-search');
  const categoryButtons = document.querySelectorAll('.category-btn');
  const dietPills = document.querySelectorAll('.diet-pill');
  const itemsCountLabel = document.getElementById('menu-items-count');

  if (!menuContainer) return;

  // Load items from loader
  const items = await MenuLoader.loadMenu();

  let activeCategory = 'all';
  let activeDiet = 'all';
  let searchQuery = '';

  function render() {
    const filtered = items.filter(item => {
      // Category match
      if (activeCategory !== 'all' && item.category.toLowerCase() !== activeCategory.toLowerCase()) {
        return false;
      }

      // Diet match
      if (activeDiet === 'vegetarian') {
        if (item.diet.toLowerCase() !== 'veg' && item.diet.toLowerCase() !== 'vegan') {
          return false;
        }
      } else if (activeDiet === 'vegan') {
        if (item.diet.toLowerCase() !== 'vegan') {
          return false;
        }
      } else if (activeDiet === 'egg-free') {
        if (item.containsEgg) {
          return false;
        }
      }

      // Search match
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const matchesName = item.name.toLowerCase().includes(query);
        const matchesDesc = item.description.toLowerCase().includes(query);
        const matchesCat = item.category.toLowerCase().includes(query);
        if (!matchesName && !matchesDesc && !matchesCat) {
          return false;
        }
      }

      return true;
    });

    if (itemsCountLabel) {
      itemsCountLabel.textContent = `Showing ${filtered.length} of ${items.length} items`;
    }

    if (filtered.length === 0) {
      menuContainer.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
          <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="margin-bottom: 0.5rem;">No menu items matched your filter</h3>
          <p>Try clearing your search or selecting a different dietary filter.</p>
        </div>
      `;
      return;
    }

    menuContainer.innerHTML = '';
    filtered.forEach(item => {
      const card = document.createElement('div');
      card.className = 'menu-card';

      // Build dietary badges
      let badgesHtml = '';
      if (item.diet.toLowerCase() === 'vegan') {
        badgesHtml += `<span class="badge badge-vegan">Vegan</span>`;
      } else if (item.diet.toLowerCase().includes('veg') && !item.diet.toLowerCase().includes('non-veg')) {
        badgesHtml += `<span class="badge badge-veg">Veg</span>`;
      } else if (item.diet.toLowerCase().includes('non-veg')) {
        badgesHtml += `<span class="badge badge-nonveg">Non-Veg</span>`;
      }

      if (item.containsEgg) {
        badgesHtml += `<span class="badge badge-egg">Contains Egg</span>`;
      }

      // Pairing snippet
      const pairingHtml = item.pairsWith 
        ? `<div class="item-pair"><span>💡 Pairs with: <strong>${item.pairsWith}</strong></span></div>` 
        : '';

      card.innerHTML = `
        <div class="card-header-row">
          <h3 class="item-name">${item.name}</h3>
          <span class="item-price">${Cart.formatPrice(item.price)}</span>
        </div>
        <div class="item-tags">${badgesHtml}</div>
        <p class="item-desc">${item.description}</p>
        ${pairingHtml}
        <div class="card-footer">
          <button type="button" class="btn btn-primary btn-sm btn-block add-to-cart-btn" data-id="${item.id}">
            + Add to Order
          </button>
        </div>
      `;

      menuContainer.appendChild(card);
    });
  }

  // Handle Add to Cart click
  menuContainer.addEventListener('click', (e) => {
    const btn = e.target.closest('.add-to-cart-btn');
    if (!btn) return;

    const itemId = btn.dataset.id;
    const item = items.find(i => i.id === itemId);
    if (item) {
      Cart.addToCart(item, 1);
      btn.textContent = '✓ Added!';
      btn.style.backgroundColor = 'var(--success)';
      setTimeout(() => {
        btn.textContent = '+ Add to Order';
        btn.style.backgroundColor = '';
      }, 1200);
    }
  });

  // Filter: Category
  categoryButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.dataset.category;
      render();
    });
  });

  // Filter: Diet
  dietPills.forEach(pill => {
    pill.addEventListener('click', () => {
      dietPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeDiet = pill.dataset.diet;
      render();
    });
  });

  // Filter: Search Input
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim();
      render();
    });
  }

  // Initial render
  render();
});
