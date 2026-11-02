/**
 * menu-page.js
 * Handles menu rendering, category filtering, dietary filtering, search,
 * and direct addition to cart from the menu page.
 * Styled with the Warm Terminal Roast design system matching Stitch.
 * Uses plain cream placeholders for food photos and plain customer badges.
 */

document.addEventListener('DOMContentLoaded', async () => {
  const menuContainer = document.getElementById('menu-items-grid');
  const searchInput = document.getElementById('menu-search');
  const categoryButtons = document.querySelectorAll('.category-btn');
  const dietPills = document.querySelectorAll('.diet-pill');
  const itemsCountLabel = document.getElementById('menu-items-count');

  if (!menuContainer) return;

  function getCategoryIcon(cat) {
    const c = (cat || '').toLowerCase();
    if (c.includes('coffee')) return '☕';
    if (c.includes('chai')) return '🫖';
    if (c.includes('cold') || c.includes('brew') || c.includes('cooler')) return '🥤';
    if (c.includes('bakery') || c.includes('dessert') || c.includes('pastry')) return '🥐';
    if (c.includes('snack') || c.includes('bite') || c.includes('food') || c.includes('bowl')) return '🥪';
    return '☕';
  }

  // Load items from loader
  const items = await MenuLoader.loadMenu();

  let activeCategory = 'all';
  let activeDiet = 'all';
  let searchQuery = '';

  function render() {
    const filtered = items.filter(item => {
      // Category match
      if (activeCategory !== 'all') {
        const catNorm = activeCategory.toLowerCase();
        const itemCat = item.category.toLowerCase();
        if (catNorm === 'snacks' && !itemCat.includes('snack') && !itemCat.includes('bites')) {
          if (itemCat !== 'snacks') return false;
        } else if (catNorm === 'bakery' && !itemCat.includes('bakery') && !itemCat.includes('dessert')) {
          if (itemCat !== 'bakery') return false;
        } else if (catNorm === 'cold brew' && !itemCat.includes('cold') && !itemCat.includes('cooler')) {
          if (itemCat !== 'cold brew') return false;
        } else if (!itemCat.includes(catNorm)) {
          return false;
        }
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
        <div class="col-span-full text-center py-12 px-4 bg-surface-container-lowest rounded-xl border border-outline-variant/30">
          <div class="text-4xl mb-2">☕</div>
          <h3 class="font-headline-sm text-headline-sm text-on-surface mb-1">No items matched your search</h3>
          <p class="font-body-md text-body-md text-on-surface-variant">Try adjusting your query or resetting dietary filters.</p>
        </div>
      `;
      return;
    }

    menuContainer.innerHTML = '';
    filtered.forEach(item => {
      const card = document.createElement('div');
      card.className = 'menu-card menu-item-card group flex flex-col bg-surface-container-lowest rounded-xl shadow-[0_4px_20px_-4px_rgba(43,24,16,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(43,24,16,0.12)] transition-all duration-300 overflow-hidden border border-outline-variant/30';
      card.dataset.category = item.category;

      const dietLower = (item.diet || '').toLowerCase();
      let dietBadge = '';
      if (dietLower === 'vegan') {
        dietBadge = `<span class="badge badge-vegan bg-tertiary-fixed text-on-tertiary-fixed font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">Vegan</span>`;
      } else if (dietLower.includes('non-veg')) {
        dietBadge = `<span class="badge badge-nonveg bg-secondary-container text-on-secondary-container font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">Non-Veg</span>`;
      } else {
        dietBadge = `<span class="badge badge-veg bg-tertiary-fixed/60 text-on-tertiary-fixed-variant font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">Vegetarian</span>`;
      }

      let eggBadge = '';
      if (item.containsEgg) {
        eggBadge = `<span class="badge badge-egg bg-secondary-fixed text-on-secondary-fixed font-label-md text-[11px] px-2 py-0.5 rounded-full font-semibold shadow-xs">Egg</span>`;
      }

      const categoryIcon = getCategoryIcon(item.category);

      card.innerHTML = `
        <!-- Food Photo on Menu Card -->
        <div class="relative h-44 w-full bg-surface-container-low border-b border-outline-variant/20 overflow-hidden select-none">
          <img src="images/menu/${item.id}.jpg" alt="${item.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.classList.remove('hidden');">
          <div class="hidden w-full h-full flex flex-col items-center justify-center text-center p-space-sm">
            <div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-2xl mb-1 shadow-xs group-hover:scale-105 transition-transform">
              ${categoryIcon}
            </div>
            <span class="font-label-sm text-[11px] text-secondary tracking-normal">${item.category}</span>
          </div>
          
          <!-- Plain Badges (No code tags) -->
          <div class="absolute top-2.5 left-2.5 flex items-center gap-1">
            ${dietBadge}
            ${eggBadge}
          </div>
          
          <!-- Price Badge -->
          <div class="absolute bottom-2 right-2 bg-surface-bright/95 backdrop-blur-md px-2.5 py-0.5 rounded-md font-headline-sm text-headline-sm text-primary font-bold shadow-sm item-price">
            ${Cart.formatPrice(item.price)}
          </div>
        </div>

        <div class="p-space-md flex flex-col flex-1 justify-between gap-space-sm">
          <div>
            <div class="flex items-baseline justify-between gap-space-xs">
              <h3 class="font-headline-sm text-headline-sm text-on-surface group-hover:text-primary transition-colors item-name">
                ${item.name}
              </h3>
              <span class="font-label-sm text-label-sm text-secondary">${item.category}</span>
            </div>
            <p class="font-body-sm text-body-sm text-on-surface-variant mt-2 line-clamp-2 item-desc">${item.description}</p>
            ${item.pairsWith ? `<div class="mt-2 font-body-sm text-xs text-secondary opacity-80">Pairs with: <strong>${item.pairsWith}</strong></div>` : ''}
          </div>
          <div class="card-footer pt-space-xs mt-auto">
            <button type="button" class="btn btn-primary btn-sm btn-block add-to-cart-btn w-full bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md py-space-xs px-space-md rounded-full shadow-sm transition-all duration-200 flex items-center justify-center gap-space-xs" data-id="${item.id}">
              <span class="material-symbols-outlined text-sm">add_shopping_cart</span>
              <span>+ Add to Order</span>
            </button>
          </div>
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
    const item = items.find(it => it.id === itemId);
    if (item) {
      Cart.addToCart(item, 1);
    }
  });

  // Search input handler
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim();
      render();
    });
  }

  // Category filter buttons
  categoryButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryButtons.forEach(b => {
        b.classList.remove('bg-secondary-container', 'text-on-secondary-container', 'font-semibold', 'shadow-sm', 'active');
        b.classList.add('bg-surface-container-high', 'text-on-surface-variant');
      });
      btn.classList.remove('bg-surface-container-high', 'text-on-surface-variant');
      btn.classList.add('bg-secondary-container', 'text-on-secondary-container', 'font-semibold', 'shadow-sm', 'active');
      activeCategory = btn.dataset.category || 'all';
      render();
    });
  });

  // Dietary filter pills
  dietPills.forEach(pill => {
    pill.addEventListener('click', () => {
      dietPills.forEach(p => {
        p.classList.remove('bg-primary/10', 'text-primary', 'font-semibold', 'active');
        p.classList.add('bg-surface-container-low', 'text-on-surface-variant');
      });
      pill.classList.remove('bg-surface-container-low', 'text-on-surface-variant');
      pill.classList.add('bg-primary/10', 'text-primary', 'font-semibold', 'active');
      activeDiet = pill.dataset.diet || 'all';
      render();
    });
  });

  // Initial render
  render();
});
