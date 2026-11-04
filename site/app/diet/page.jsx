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
  if (c.includes('snack') || c.includes('bite') || c.includes('food') || c.includes('bowl') || c.includes('meal')) return '🥪';
  return '☕';
}

export default function DietGuidePage() {
  const [activeDietFilter, setActiveDietFilter] = useState('all');
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [imgErrors, setImgErrors] = useState({});

  const items = menuItemsData;

  // Extract unique categories dynamically from menu items
  const categories = useMemo(() => {
    const cats = [];
    items.forEach((item) => {
      if (item.category && !cats.includes(item.category)) {
        cats.push(item.category);
      }
    });
    return cats;
  }, [items]);

  // Counts for each dietary preference
  const counts = useMemo(() => {
    const vegan = items.filter((i) => (i.diet || '').toLowerCase() === 'vegan').length;
    const vegetarian = items.filter((i) => {
      const d = (i.diet || '').toLowerCase();
      return d === 'veg' || d === 'vegan';
    }).length;
    const eggFree = items.filter((i) => !i.containsEgg).length;
    const containsEgg = items.filter((i) => Boolean(i.containsEgg)).length;
    const nonVeg = items.filter((i) => (i.diet || '').toLowerCase().includes('non-veg')).length;
    return {
      all: items.length,
      vegan,
      vegetarian,
      eggFree,
      containsEgg,
      nonVeg,
    };
  }, [items]);

  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      const dietLower = (item.diet || '').toLowerCase();

      // Category filter
      if (activeCategory !== 'all' && item.category !== activeCategory) {
        return false;
      }

      // Dietary filter
      if (activeDietFilter === 'vegan') {
        if (dietLower !== 'vegan') return false;
      } else if (activeDietFilter === 'vegetarian') {
        if (dietLower !== 'veg' && dietLower !== 'vegan') return false;
      } else if (activeDietFilter === 'egg-free') {
        if (item.containsEgg) return false;
      } else if (activeDietFilter === 'contains-egg') {
        if (!item.containsEgg) return false;
      } else if (activeDietFilter === 'non-veg') {
        if (!dietLower.includes('non-veg')) return false;
      }

      // Search match
      if (searchQuery) {
        const q = searchQuery.toLowerCase().trim();
        const matchesName = (item.name || '').toLowerCase().includes(q);
        const matchesDesc = (item.description || '').toLowerCase().includes(q);
        const matchesCat = (item.category || '').toLowerCase().includes(q);
        const matchesDiet = dietLower.includes(q);
        const matchesEgg = (item.containsEgg ? 'contains egg' : 'egg-free').includes(q);

        if (!matchesName && !matchesDesc && !matchesCat && !matchesDiet && !matchesEgg) {
          return false;
        }
      }

      return true;
    });
  }, [items, activeCategory, activeDietFilter, searchQuery]);

  const handleAddToCart = (item) => {
    Cart.addToCart(item, 1);
  };

  const handleImageError = (id) => {
    setImgErrors((prev) => ({ ...prev, [id]: true }));
  };

  const resetFilters = () => {
    setActiveDietFilter('all');
    setActiveCategory('all');
    setSearchQuery('');
  };

  return (
    <div className="w-full bg-background py-space-xl">
      <div className="max-w-[1280px] mx-auto px-gutter-desktop">
        {/* Page Header */}
        <div className="flex flex-col max-w-3xl mb-space-lg">
          <div className="inline-flex items-center gap-space-xs self-start px-space-md py-space-xs rounded-full bg-secondary-container text-on-secondary-container font-label-md text-xs shadow-xs mb-3">
            <span>🌱 Mindful Dining</span>
          </div>
          <h1 className="font-display-hero text-display-hero-mobile md:text-display-hero text-on-surface tracking-tight">
            Diet &amp; Allergen Guide
          </h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant mt-2 leading-relaxed">
            Find items tailored to your lifestyle, from 100% plant-based drinks to egg-free bakery treats.
          </p>
        </div>

        {/* Friendly Kitchen Note */}
        <div className="mb-space-lg p-space-md bg-surface-container-low rounded-xl border border-outline-variant/30 flex items-start gap-space-sm">
          <span className="material-symbols-outlined text-primary text-xl mt-0.5">info</span>
          <p className="font-body-md text-sm text-on-surface-variant">
            Please let our baristas know if you have severe food allergies before ordering.
          </p>
        </div>

        {/* Dietary Overview Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md mb-space-xl">
          {/* Vegan Card */}
          <button
            type="button"
            onClick={() => setActiveDietFilter(activeDietFilter === 'vegan' ? 'all' : 'vegan')}
            className={`text-left p-space-md rounded-xl transition-all duration-200 border cursor-pointer ${
              activeDietFilter === 'vegan'
                ? 'bg-surface-container-lowest border-primary shadow-md ring-2 ring-primary/20'
                : 'bg-surface-container-lowest border-outline-variant/30 hover:border-primary/50 shadow-xs hover:shadow-sm'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">🌱</span>
              <span className="font-label-sm text-xs bg-tertiary-fixed text-on-tertiary-fixed font-semibold px-2 py-0.5 rounded-full">
                {counts.vegan} items
              </span>
            </div>
            <h2 className="font-headline-sm text-base text-on-surface font-semibold">100% Vegan</h2>
            <p className="font-body-sm text-xs text-on-surface-variant mt-1 leading-snug">
              Plant-based drinks and meals crafted without animal products or dairy.
            </p>
          </button>

          {/* Vegetarian Card */}
          <button
            type="button"
            onClick={() => setActiveDietFilter(activeDietFilter === 'vegetarian' ? 'all' : 'vegetarian')}
            className={`text-left p-space-md rounded-xl transition-all duration-200 border cursor-pointer ${
              activeDietFilter === 'vegetarian'
                ? 'bg-surface-container-lowest border-primary shadow-md ring-2 ring-primary/20'
                : 'bg-surface-container-lowest border-outline-variant/30 hover:border-primary/50 shadow-xs hover:shadow-sm'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">🥬</span>
              <span className="font-label-sm text-xs bg-tertiary-fixed/60 text-on-tertiary-fixed-variant font-semibold px-2 py-0.5 rounded-full">
                {counts.vegetarian} items
              </span>
            </div>
            <h2 className="font-headline-sm text-base text-on-surface font-semibold">Vegetarian</h2>
            <p className="font-body-sm text-xs text-on-surface-variant mt-1 leading-snug">
              Wholesome choices prepared with dairy, fresh greens, and farm ingredients.
            </p>
          </button>

          {/* Egg-Free Card */}
          <button
            type="button"
            onClick={() => setActiveDietFilter(activeDietFilter === 'egg-free' ? 'all' : 'egg-free')}
            className={`text-left p-space-md rounded-xl transition-all duration-200 border cursor-pointer ${
              activeDietFilter === 'egg-free'
                ? 'bg-surface-container-lowest border-primary shadow-md ring-2 ring-primary/20'
                : 'bg-surface-container-lowest border-outline-variant/30 hover:border-primary/50 shadow-xs hover:shadow-sm'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">✨</span>
              <span className="font-label-sm text-xs bg-surface-container-high text-on-surface-variant border border-outline-variant/40 font-semibold px-2 py-0.5 rounded-full">
                {counts.eggFree} items
              </span>
            </div>
            <h2 className="font-headline-sm text-base text-on-surface font-semibold">100% Egg-Free</h2>
            <p className="font-body-sm text-xs text-on-surface-variant mt-1 leading-snug">
              Delicious sips, snacks, and treats crafted without any eggs.
            </p>
          </button>

          {/* Contains Egg Card */}
          <button
            type="button"
            onClick={() => setActiveDietFilter(activeDietFilter === 'contains-egg' ? 'all' : 'contains-egg')}
            className={`text-left p-space-md rounded-xl transition-all duration-200 border cursor-pointer ${
              activeDietFilter === 'contains-egg'
                ? 'bg-surface-container-lowest border-primary shadow-md ring-2 ring-primary/20'
                : 'bg-surface-container-lowest border-outline-variant/30 hover:border-primary/50 shadow-xs hover:shadow-sm'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">🥚</span>
              <span className="font-label-sm text-xs bg-secondary-fixed text-on-secondary-fixed font-semibold px-2 py-0.5 rounded-full">
                {counts.containsEgg} treats
              </span>
            </div>
            <h2 className="font-headline-sm text-base text-on-surface font-semibold">Contains Egg</h2>
            <p className="font-body-sm text-xs text-on-surface-variant mt-1 leading-snug">
              Rich bakery items, pancakes, and desserts baked with whole eggs.
            </p>
          </button>
        </div>

        {/* Filter and Search Controls */}
        <div className="flex flex-col gap-space-sm mb-space-xl">
          {/* Search Box */}
          <div className="relative w-full max-w-md">
            <span className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-outline">
              <span className="material-symbols-outlined text-lg">search</span>
            </span>
            <input
              id="diet-search"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-surface-container-lowest border border-outline-variant/50 rounded-full pl-11 pr-4 py-2.5 font-body-md text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary shadow-sm"
              placeholder="Search dishes by name or description..."
            />
          </div>

          {/* Category Pills */}
          <div className="flex items-center gap-space-xs overflow-x-auto pb-space-xs no-scrollbar">
            <button
              type="button"
              onClick={() => setActiveCategory('all')}
              className={`whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md transition-all duration-150 cursor-pointer ${
                activeCategory === 'all'
                  ? 'bg-secondary-container text-on-secondary-container font-semibold shadow-sm'
                  : 'bg-surface-container-high text-on-surface-variant hover:text-on-surface'
              }`}
            >
              All Categories ({items.length})
            </button>
            {categories.map((cat) => {
              const count = items.filter((i) => i.category === cat).length;
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setActiveCategory(cat)}
                  className={`whitespace-nowrap px-space-lg py-space-xs rounded-full font-label-md text-label-md transition-all duration-150 cursor-pointer ${
                    activeCategory === cat
                      ? 'bg-secondary-container text-on-secondary-container font-semibold shadow-sm'
                      : 'bg-surface-container-high text-on-surface-variant hover:text-on-surface'
                  }`}
                >
                  {cat} ({count})
                </button>
              );
            })}
          </div>

          {/* Dietary Filter Buttons */}
          <div className="flex flex-wrap items-center gap-space-xs font-label-sm text-xs text-on-surface-variant">
            <span className="opacity-70">Diet Filter:</span>
            <button
              type="button"
              onClick={() => setActiveDietFilter('all')}
              className={`px-space-sm py-1 rounded-full transition-all cursor-pointer ${
                activeDietFilter === 'all'
                  ? 'bg-primary text-on-primary font-semibold shadow-xs'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              All ({counts.all})
            </button>
            <button
              type="button"
              onClick={() => setActiveDietFilter('vegan')}
              className={`px-space-sm py-1 rounded-full transition-all cursor-pointer ${
                activeDietFilter === 'vegan'
                  ? 'bg-primary text-on-primary font-semibold shadow-xs'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Vegan ({counts.vegan})
            </button>
            <button
              type="button"
              onClick={() => setActiveDietFilter('vegetarian')}
              className={`px-space-sm py-1 rounded-full transition-all cursor-pointer ${
                activeDietFilter === 'vegetarian'
                  ? 'bg-primary text-on-primary font-semibold shadow-xs'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Vegetarian ({counts.vegetarian})
            </button>
            <button
              type="button"
              onClick={() => setActiveDietFilter('egg-free')}
              className={`px-space-sm py-1 rounded-full transition-all cursor-pointer ${
                activeDietFilter === 'egg-free'
                  ? 'bg-primary text-on-primary font-semibold shadow-xs'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              100% Egg-Free ({counts.eggFree})
            </button>
            <button
              type="button"
              onClick={() => setActiveDietFilter('contains-egg')}
              className={`px-space-sm py-1 rounded-full transition-all cursor-pointer ${
                activeDietFilter === 'contains-egg'
                  ? 'bg-primary text-on-primary font-semibold shadow-xs'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Contains Egg ({counts.containsEgg})
            </button>
            <button
              type="button"
              onClick={() => setActiveDietFilter('non-veg')}
              className={`px-space-sm py-1 rounded-full transition-all cursor-pointer ${
                activeDietFilter === 'non-veg'
                  ? 'bg-primary text-on-primary font-semibold shadow-xs'
                  : 'bg-surface-container-low hover:bg-surface-container'
              }`}
            >
              Customizable / Non-Veg ({counts.nonVeg})
            </button>

            <span className="ml-auto text-xs text-secondary opacity-75">
              Showing {filteredItems.length} of {items.length} items
            </span>
          </div>
        </div>

        {/* Items Grid */}
        <div id="diet-items-grid" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-space-lg">
          {filteredItems.length === 0 ? (
            <div className="col-span-full text-center py-12 px-4 bg-surface-container-lowest rounded-xl border border-outline-variant/30">
              <div className="text-4xl mb-2">🥗</div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface mb-1">
                No items match your selected filters
              </h3>
              <p className="font-body-md text-body-md text-on-surface-variant mb-4">
                Try adjusting your search terms or clearing current diet filters.
              </p>
              <button
                type="button"
                onClick={resetFilters}
                className="inline-flex items-center justify-center px-space-lg py-space-xs rounded-full bg-primary text-on-primary font-label-md text-sm shadow-sm hover:bg-primary-container transition-colors cursor-pointer"
              >
                Reset All Filters
              </button>
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
                    {dietLower === 'veg or non-veg' ? 'Veg or Non-Veg' : 'Non-Veg'}
                  </span>
                );
              } else {
                dietBadge = (
                  <span className="badge badge-veg bg-tertiary-fixed/60 text-on-tertiary-fixed-variant font-label-md text-[11px] px-2.5 py-0.5 rounded-full font-semibold shadow-xs">
                    Vegetarian
                  </span>
                );
              }

              const eggBadge = item.containsEgg ? (
                <span className="badge badge-egg bg-secondary-fixed text-on-secondary-fixed font-label-md text-[11px] px-2 py-0.5 rounded-full font-semibold shadow-xs">
                  Contains Egg
                </span>
              ) : (
                <span className="badge badge-eggfree bg-surface-bright/90 text-on-surface-variant border border-outline-variant/40 font-label-md text-[11px] px-2 py-0.5 rounded-full font-semibold shadow-xs">
                  Egg-Free
                </span>
              );

              const hasPhoto =
                (item.hasPhoto !== undefined ? Boolean(item.hasPhoto) : KNOWN_PHOTO_IDS.has(item.id)) &&
                !imgErrors[item.id];
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
                        <span className="font-label-sm text-[11px] text-secondary tracking-normal">
                          {item.category}
                        </span>
                      </div>
                    )}

                    {/* Badges */}
                    <div className="absolute top-2.5 left-2.5 flex flex-wrap items-center gap-1 max-w-[80%]">
                      {dietBadge}
                      {eggBadge}
                    </div>

                    {/* Price Badge */}
                    <div className="absolute bottom-2 right-2 bg-surface-bright/95 backdrop-blur-md px-2.5 py-0.5 rounded-md font-headline-sm text-headline-sm text-primary font-bold shadow-sm item-price">
                      ${Number(item.price || 0).toFixed(2)}
                    </div>
                  </div>

                  {/* Info Area */}
                  <div className="p-space-md flex flex-col flex-1 justify-between gap-space-sm">
                    <div>
                      <div className="flex items-baseline justify-between gap-space-xs">
                        <h3 className="font-headline-sm text-headline-sm text-on-surface group-hover:text-primary transition-colors item-name">
                          {item.name}
                        </h3>
                        <span className="font-label-sm text-label-sm text-secondary shrink-0">
                          {item.category}
                        </span>
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
                        <span>+ Add to Cart</span>
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
