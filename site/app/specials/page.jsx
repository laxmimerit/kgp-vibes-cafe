'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import menuItemsData from '../../data/menu.json';
import Cart from '../../lib/cart';

const WEEKLY_SPECIALS = [
  {
    day: 'Monday',
    itemId: 'C01',
    theme: 'Fresh Start Monday',
    badge: 'Kickstart',
  },
  {
    day: 'Tuesday',
    itemId: 'S04',
    theme: 'Comfort Tuesday',
    badge: 'Warm Hug',
  },
  {
    day: 'Wednesday',
    itemId: 'C02',
    theme: 'Midweek Focus',
    badge: 'Sweet Fuel',
  },
  {
    day: 'Thursday',
    itemId: 'M01',
    theme: 'Power Lunch Thursday',
    badge: 'Hearty Bite',
  },
  {
    day: 'Friday',
    itemId: 'C06',
    theme: 'Sprint Energizer Friday',
    badge: 'Weekend Warmup',
  },
  {
    day: 'Saturday',
    itemId: 'S05',
    theme: 'Weekend Brunch Saturday',
    badge: 'Treat Yourself',
  },
  {
    day: 'Sunday',
    itemId: 'D04',
    theme: 'Sweet Chill Sunday',
    badge: 'Sweet Finish',
  },
];

export default function SpecialsPage() {
  const [currentDay, setCurrentDay] = useState(null);

  useEffect(() => {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const now = new Date();
    setCurrentDay(days[now.getDay()]);
  }, []);

  const handleAddToCart = (item) => {
    Cart.addToCart(item, 1);
  };

  const specials = WEEKLY_SPECIALS.map((s) => {
    const item = menuItemsData.find((m) => m.id === s.itemId) || {
      id: s.itemId,
      name: 'Special Item',
      price: 0,
      description: '',
      category: '',
      diet: 'veg',
    };
    return {
      ...s,
      item,
    };
  });

  return (
    <div className="w-full bg-background py-space-xl">
      <div className="max-w-[1280px] mx-auto px-gutter-desktop">
        {/* Header Section */}
        <div className="flex flex-col max-w-2xl mb-space-xl">
          <div className="inline-flex items-center gap-space-xs self-start px-space-md py-space-xs rounded-full bg-secondary-container text-on-secondary-container font-label-md text-xs shadow-xs mb-3">
            <span>✨ Weekly Lineup</span>
          </div>
          <h1 className="font-display-hero text-display-hero-mobile md:text-display-hero text-on-surface tracking-tight">
            Daily Specials
          </h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant mt-2 leading-relaxed">
            Enjoy a featured cafe favorite every day from Monday to Sunday.
          </p>
        </div>

        {/* Specials Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-space-lg">
          {specials.map(({ day, badge, item }) => {
            const isToday = currentDay === day;
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

            return (
              <div
                key={day}
                className={`menu-card menu-item-card group flex flex-col bg-surface-container-lowest rounded-xl shadow-[0_4px_20px_-4px_rgba(43,24,16,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(43,24,16,0.12)] transition-all duration-300 overflow-hidden border ${
                  isToday ? 'border-primary ring-2 ring-primary/20' : 'border-outline-variant/30'
                }`}
              >
                {/* Day Header Bar */}
                <div className="px-space-md py-2.5 bg-surface-container-low border-b border-outline-variant/20 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-headline-sm text-base text-on-surface font-semibold">{day}</span>
                    {isToday && (
                      <span className="bg-primary text-on-primary font-label-md text-[11px] px-2 py-0.5 rounded-full font-semibold shadow-xs">
                        Today
                      </span>
                    )}
                  </div>
                  <span className="font-label-sm text-[11px] text-secondary">{badge}</span>
                </div>

                {/* Photo Area */}
                <div className="relative h-48 w-full bg-surface-container-low border-b border-outline-variant/20 overflow-hidden select-none">
                  <img
                    src={`/images/menu/${item.id}.jpg`}
                    alt={item.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    loading="lazy"
                  />

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
                      <span className="font-label-sm text-label-sm text-secondary shrink-0">{item.category}</span>
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
          })}
        </div>

        {/* Bottom Callout banner */}
        <div className="mt-space-xl p-space-lg rounded-2xl bg-surface-container-low border border-outline-variant/30 flex flex-col sm:flex-row items-center justify-between gap-space-md">
          <div>
            <h3 className="font-headline-sm text-lg text-on-surface font-semibold">Want to see our full selection?</h3>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1">
              Explore our full catalog of handcrafted chai, specialty coffees, and wholesome snacks.
            </p>
          </div>
          <Link
            href="/menu"
            className="shrink-0 bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-lg py-space-xs rounded-full shadow-sm transition-all duration-200"
          >
            View Full Menu
          </Link>
        </div>
      </div>
    </div>
  );
}
