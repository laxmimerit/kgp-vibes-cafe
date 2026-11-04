'use client';

import { useState, useMemo } from 'react';
import menuItemsData from '../../data/menu.json';
import Cart from '../../lib/cart';

// Known item IDs with photography available in /images/menu/
const KNOWN_PHOTO_IDS = new Set([
  'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C10',
  'D04', 'M01', 'M07', 'S04', 'S05'
]);

function getCategoryIcon(cat) {
  const c = (cat || '').toLowerCase();
  if (c.includes('coffee')) return '☕';
  if (c.includes('chai')) return '🫖';
  if (c.includes('cold') || c.includes('brew') || c.includes('cooler')) return '🥤';
  if (c.includes('bakery') || c.includes('dessert') || c.includes('pastry')) return '🥐';
  if (c.includes('snack') || c.includes('bite') || c.includes('food') || c.includes('bowl')) return '🥪';
  return '☕';
}

export default function MenuPage() {
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeDiet, setActiveDiet] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [imgErrors, setImgErrors] = useState({});

  const items = menuItemsData;

  // Extract unique categories dynamically from menu items (sourced from menu.csv)
  const categories = useMemo(() => {
    const cats = [];
    items.forEach((item) => {
      if (item.category && !cats.includes(item.category)) {
        cats.push(item.category);
      }
    });
    return cats;
  }, [items]);

  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      // Category match
      if (activeCategory !== 'all') {
        if (item.category !== activeCategory) {
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
  }, [items, activeCategory, activeDiet, searchQuery]);

  const handleAddToCart = (item) => {
    Cart.addToCart(item, 1);
  };

  const handleImageError = (id) => {
    setImgErrors((prev) => ({ ...prev, [id]: true }));
  };

  return (
    <div className="w-full bg-background py-space-xl">
      <div className="max-w-[1280px] mx-auto px-gutter-desktop">
        {/* Menu Header */}
        <div className="flex flex-col max-w-2xl mb-space-lg">
          <span className="font-label-sm text-primary uppercase tracking-wider font-semibold">Freshly Prepared</span>
          <h1 className="font-display-hero text-display-hero-mobile md:text-display-hero text-on-surface tracking-tight mt-1">
            Our Menu
          </h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant mt-2 leading-relaxed">
            Explore our handcrafted chai, single-origin coffee, wholesome food, and bakery treats.
          </p>
        </div>

        {/* Search and Filter Bar */}
        <div className="flex flex-col gap-space-sm mb-space-xl">
          <div className="relative w-full max-w-md">
            <span className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-outline">
              <span className="material-symbols-outlined text-lg">search</span>
            </span>
            <input
              id="menu-search"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-surface-container-lowest border border-outline-variant/50 rounded-full pl-11 pr-4 py-2.5 font-body-md text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary shadow-sm"
              placeholder="Search menu by name, ingredient, or tag..."
            />
          </div>

          {/* Category Selector Buttons */}
          <div className="flex items-center gap-space-xs overflow-x-auto pb-space-xs no-scrollbar" id="category-pills">
            <button
              type="button"
              data-category="all"
              onClick={() => setActiveCategory('all')}
              className={`category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md transition-all duration-150 cursor-pointer ${
                activeCategory === 'all'
                  ? 'bg-secondary-container text-on-secondary-container font-semibold shadow-sm active'
                  : 'bg-surface-container-high text-on-surface-variant hover:text-on-surface'
              }`}
            >
              All Items ({items.length})
            </button>
            {categories.map((cat) => {
              const count = items.filter((i) => i.category === cat).length;
              return (
                <button
                  key={cat}
                  type="button"
                  data-category={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`category-btn filter-pill-btn whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md transition-all duration-150 cursor-pointer ${
                    activeCategory === cat
                      ? 'bg-secondary-container text-on-secondary-container font-semibold shadow-sm active'
                      : 'bg-surface-container-high text-on-surface-variant hover:text-on-surface'
                  }`}
                >
                  {cat} ({count})
                </button>
              );
            })}
          </div>

          {/* Dietary Filters */}
          <div className="flex flex-wrap items-center gap-space-xs font-label-sm text-xs text-on-surface-variant">
            <span className="opacity-70">Dietary Filter:</span>
            <button
              type="button"
              data-diet="all"
              onClick={() => setActiveDiet('all')}
              className={`diet-pill px-space-sm py-0.5 rounded-full transition-all cursor-pointer ${
                activeDiet === 'all'
                  ? 'bg-primary/10 text-primary font-semibold'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              All Diets
            </button>
            <button
              type="button"
              data-diet="vegetarian"
              onClick={() => setActiveDiet('vegetarian')}
              className={`diet-pill px-space-sm py-0.5 rounded-full transition-all cursor-pointer ${
                activeDiet === 'vegetarian'
                  ? 'bg-primary/10 text-primary font-semibold'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Veg
            </button>
            <button
              type="button"
              data-diet="vegan"
              onClick={() => setActiveDiet('vegan')}
              className={`diet-pill px-space-sm py-0.5 rounded-full transition-all cursor-pointer ${
                activeDiet === 'vegan'
                  ? 'bg-primary/10 text-primary font-semibold'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Vegan
            </button>
            <button
              type="button"
              data-diet="egg-free"
              onClick={() => setActiveDiet('egg-free')}
              className={`diet-pill px-space-sm py-0.5 rounded-full transition-all cursor-pointer ${
                activeDiet === 'egg-free'
                  ? 'bg-primary/10 text-primary font-semibold'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Egg-Free
            </button>
            <span id="menu-items-count" className="ml-auto text-xs text-secondary opacity-75">
              Showing {filteredItems.length} of {items.length} items
            </span>
          </div>
        </div>

        {/* Menu Items Grid */}
        <div id="menu-items-grid" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-space-lg">
          {filteredItems.length === 0 ? (
            <div className="col-span-full text-center py-12 px-4 bg-surface-container-lowest rounded-xl border border-outline-variant/30">
              <div className="text-4xl mb-2">☕</div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface mb-1">No items matched your search</h3>
              <p className="font-body-md text-body-md text-on-surface-variant">
                Try adjusting your query or resetting dietary filters.
              </p>
            </div>
          ) : (
            filteredItems.map((item) => {
              const dietLower = (item.diet || '').toLowerCase();
              let dietBadge = null;
              if (dietLower === 'vegan') {
                dietBadge = (
                  <span className="badge badge-vegan bg-tertiary-fixed text-on-tertiary-fixed font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">
                    Vegan
                  </span>
                );
              } else if (dietLower.includes('non-veg')) {
                dietBadge = (
                  <span className="badge badge-nonveg bg-secondary-container text-on-secondary-container font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">
                    Non-Veg
                  </span>
                );
              } else {
                dietBadge = (
                  <span className="badge badge-veg bg-tertiary-fixed/60 text-on-tertiary-fixed-variant font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">
                    Vegetarian
                  </span>
                );
              }

              const hasPhoto = (item.hasPhoto !== undefined ? Boolean(item.hasPhoto) : KNOWN_PHOTO_IDS.has(item.id)) && !imgErrors[item.id];
              const categoryIcon = getCategoryIcon(item.category);

              return (
                <div
                  key={item.id}
                  data-category={item.category}
                  className="menu-card menu-item-card group flex flex-col bg-surface-container-lowest rounded-xl shadow-[0_4px_20px_-4px_rgba(43,24,16,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(43,24,16,0.12)] transition-all duration-300 overflow-hidden border border-outline-variant/30"
                >
                  {/* Photo area */}
                  <div className="relative h-44 w-full bg-surface-container-low border-b border-outline-variant/20 overflow-hidden select-none">
                    {hasPhoto ? (
                      <img
                        src={`/images/menu/${item.id}.jpg`}
                        alt={item.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        loading="lazy"
                        onError={() => handleImageError(item.id)}
                      />
                    ) : (
                      <div className="w-full h-full flex flex-col items-center justify-center text-center p-space-sm menu-card-placeholder">
                        <div className="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-2xl mb-1 shadow-xs group-hover:scale-105 transition-transform">
                          {categoryIcon}
                        </div>
                        <span className="font-label-sm text-[11px] text-secondary tracking-normal">{item.category}</span>
                      </div>
                    )}

                    {/* Badges */}
                    <div className="absolute top-2.5 left-2.5 flex items-center gap-1">
                      {dietBadge}
                      {item.containsEgg && (
                        <span className="badge badge-egg bg-secondary-fixed text-on-secondary-fixed font-label-md text-[11px] px-2 py-0.5 rounded-full font-semibold shadow-xs">
                          Egg
                        </span>
                      )}
                    </div>

                    {/* Price Badge */}
                    <div className="absolute bottom-2 right-2 bg-surface-bright/95 backdrop-blur-md px-2.5 py-0.5 rounded-md font-headline-sm text-headline-sm text-primary font-bold shadow-sm item-price">
                      {Cart.formatPrice(item.price)}
                    </div>
                  </div>

                  {/* Info Area */}
                  <div className="p-space-md flex flex-col flex-1 justify-between gap-space-sm">
                    <div>
                      <div className="flex items-baseline justify-between gap-space-xs">
                        <h3 className="font-headline-sm text-headline-sm text-on-surface group-hover:text-primary transition-colors item-name">
                          {item.name}
                        </h3>
                        <span className="font-label-sm text-label-sm text-secondary">{item.category}</span>
                      </div>
                      <p className="font-body-sm text-body-sm text-on-surface-variant mt-2 line-clamp-2 item-desc">
                        {item.description}
                      </p>
                      {item.pairsWith && (
                        <div className="mt-2 font-body-sm text-xs text-secondary opacity-80">
                          Pairs with: <strong>{item.pairsWith}</strong>
                        </div>
                      )}
                    </div>
                    <div className="card-footer pt-space-xs mt-auto">
                      <button
                        type="button"
                        data-id={item.id}
                        onClick={() => handleAddToCart(item)}
                        className="btn btn-primary btn-sm btn-block add-to-cart-btn w-full bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md py-space-xs px-space-md rounded-full shadow-sm transition-all duration-200 flex items-center justify-center gap-space-xs cursor-pointer"
                      >
                        <span className="material-symbols-outlined text-sm">add_shopping_cart</span>
                        <span>+ Add to Order</span>
                      </button>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
