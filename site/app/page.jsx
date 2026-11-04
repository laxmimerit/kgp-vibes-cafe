'use client';

import Link from 'next/link';
import Cart from '../lib/cart';

export default function HomePage() {
  const handleAddToCart = (item) => {
    Cart.addToCart(item, 1);
  };

  return (
    <div className="w-full bg-background">
      {/* Hero Section with Masala Chai & Chocolate Brownie Photo */}
      <section className="relative w-full overflow-hidden border-b border-outline-variant/20 min-h-[520px] lg:min-h-[580px] flex items-center">
        {/* Background Hero Image */}
        <img
          src="/images/hero.jpg"
          alt="Handcrafted Masala Chai and Chocolate Brownie on cafe table"
          className="absolute inset-0 w-full h-full object-cover object-right md:object-center select-none"
        />

        {/* Gradient Overlays for Readability */}
        <div className="absolute inset-0 bg-gradient-to-t sm:bg-gradient-to-r from-surface-bright/95 via-surface-bright/90 md:via-surface-bright/80 to-surface-bright/40 md:to-transparent"></div>

        {/* Hero Content */}
        <div className="relative w-full max-w-[1280px] mx-auto px-gutter-desktop py-space-xl lg:py-space-2xl z-10">
          <div className="max-w-xl lg:max-w-2xl flex flex-col gap-space-md bg-surface-bright/60 sm:bg-transparent backdrop-blur-xs sm:backdrop-blur-none p-space-sm sm:p-0 rounded-2xl">
            <div className="inline-flex items-center gap-space-xs self-start px-space-md py-space-xs rounded-full bg-secondary-container/95 text-on-secondary-container font-label-md text-xs shadow-sm backdrop-blur-sm">
              <span>☕ Freshly Brewed Daily</span>
              <span className="opacity-60">·</span>
              <span>Koramangala &amp; Indiranagar</span>
            </div>

            <h1 className="font-display-hero text-display-hero-mobile md:text-display-hero text-on-surface leading-tight tracking-tight">
              Where code meets chai: now open in Indiranagar
            </h1>

            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-xl leading-relaxed">
              An approachable neighborhood sanctuary for builders, students, and thinkers. Enjoy handcrafted Kulhad Chai, artisanal coffee, and comforting bites.
            </p>

            <div className="flex flex-wrap items-center gap-space-sm pt-space-xs">
              <Link
                href="/cart"
                className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-xl py-space-sm rounded-full shadow-md transition-all duration-200"
              >
                Order Ahead
              </Link>
              <Link
                href="/menu"
                className="bg-surface-container-high/90 hover:bg-surface-container-highest text-on-surface font-label-md text-label-md px-space-lg py-space-sm rounded-full transition-all duration-200 border border-outline-variant/40 backdrop-blur-sm"
              >
                Browse Menu
              </Link>
            </div>

            <div className="grid grid-cols-3 gap-space-sm pt-space-md max-w-lg border-t border-outline-variant/30">
              <div>
                <span className="font-headline-sm text-primary font-bold block">39 Items</span>
                <span className="font-body-sm text-xs text-on-surface-variant">Chai, Coffee &amp; Food</span>
              </div>
              <div>
                <span className="font-headline-sm text-primary font-bold block">15-Min</span>
                <span className="font-body-sm text-xs text-on-surface-variant">Quick Pickup Slots</span>
              </div>
              <div>
                <span className="font-headline-sm text-primary font-bold block">2 Outlets</span>
                <span className="font-body-sm text-xs text-on-surface-variant">Open Daily 8 AM - 10 PM</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 1: The Spirit of KGP Vibes */}
      <section className="py-space-xl bg-surface">
        <div className="max-w-[1280px] mx-auto px-gutter-desktop">
          <div className="text-center max-w-2xl mx-auto mb-space-xl">
            <span className="font-label-sm text-primary uppercase tracking-wider font-semibold">Our Philosophy</span>
            <h2 className="font-headline-lg text-headline-lg text-on-surface mt-1">The Spirit of KGP Vibes</h2>
            <p className="font-body-md text-on-surface-variant mt-2">
              Born from late-night college discussions and a craving for honest, comforting chai, KGP Vibes is an unpretentious home away from home.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-space-lg">
            <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30 flex flex-col gap-space-xs">
              <div className="w-12 h-12 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-2xl mb-2">
                🫖
              </div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Authentic Kulhad Chai</h3>
              <p className="font-body-sm text-on-surface-variant">
                Simmered with whole cardamom, crushed fresh ginger, and rich Assam tea leaves in natural earthen clay.
              </p>
            </div>

            <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30 flex flex-col gap-space-xs">
              <div className="w-12 h-12 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-2xl mb-2">
                🌱
              </div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Mindful &amp; Wholesome Food</h3>
              <p className="font-body-sm text-on-surface-variant">
                From hearty breakfast bowls and signature burgers to vegan bites and fresh sourdough snacks.
              </p>
            </div>

            <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30 flex flex-col gap-space-xs">
              <div className="w-12 h-12 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-2xl mb-2">
                🤝
              </div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Welcoming Community</h3>
              <p className="font-body-sm text-on-surface-variant">
                A peaceful place where you can study, read a novel, meet collaborators, or just take a breather.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2: Cafe Favorites */}
      <section className="py-space-xl bg-surface-container-low border-y border-outline-variant/20">
        <div className="max-w-[1280px] mx-auto px-gutter-desktop">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-space-md mb-space-lg">
            <div>
              <span className="font-label-sm text-primary uppercase tracking-wider font-semibold">Campus Specials</span>
              <h2 className="font-headline-lg text-headline-lg text-on-surface mt-1">Cafe Favorites</h2>
              <p className="font-body-md text-on-surface-variant mt-1">Our most beloved drinks and bites, ready for order-ahead pickup.</p>
            </div>
            <Link href="/menu" className="font-label-md text-primary hover:underline flex items-center gap-1 font-semibold">
              View full menu (39 items) &rarr;
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-lg">
            {/* Favorite 1: Talkie Chai */}
            <div className="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
              <div className="p-space-lg">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Talkie Chai</h3>
                  <span className="font-headline-sm font-bold text-primary">$2.00</span>
                </div>
                <span className="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
                <p className="font-body-sm text-on-surface-variant">Signature masala chai brewed in an authentic clay kulhad with crushed ginger and aromatic green cardamom.</p>
              </div>
              <div className="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
                <button
                  type="button"
                  className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all cursor-pointer"
                  onClick={() => handleAddToCart({ id: 'C09', name: 'Talkie Chai', price: 2.0, category: 'Coffee' })}
                >
                  + Add to Order
                </button>
              </div>
            </div>

            {/* Favorite 2: Byte Brownie */}
            <div className="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
              <div className="p-space-lg">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Byte Brownie</h3>
                  <span className="font-headline-sm font-bold text-primary">$2.50</span>
                </div>
                <span className="inline-block bg-secondary-fixed text-on-secondary-fixed text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Egg</span>
                <p className="font-body-sm text-on-surface-variant">Rich fudgy dark chocolate brownie baked fresh every morning with a crisp crackly crust.</p>
              </div>
              <div className="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
                <button
                  type="button"
                  className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all cursor-pointer"
                  onClick={() => handleAddToCart({ id: 'S04', name: 'Byte Brownie', price: 2.5, category: 'Snacks & Meals' })}
                >
                  + Add to Order
                </button>
              </div>
            </div>

            {/* Favorite 3: Filter Coffee */}
            <div className="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
              <div className="p-space-lg">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Filter Coffee</h3>
                  <span className="font-headline-sm font-bold text-primary">$2.50</span>
                </div>
                <span className="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
                <p className="font-body-sm text-on-surface-variant">Traditional South Indian brass filter coffee made with chicory blend and frothed steamed milk.</p>
              </div>
              <div className="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
                <button
                  type="button"
                  className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all cursor-pointer"
                  onClick={() => handleAddToCart({ id: 'C06', name: 'Filter Coffee', price: 2.5, category: 'Coffee' })}
                >
                  + Add to Order
                </button>
              </div>
            </div>

            {/* Favorite 4: KGP Maggi Bowl */}
            <div className="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
              <div className="p-space-lg">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">KGP Maggi Bowl</h3>
                  <span className="font-headline-sm font-bold text-primary">$3.00</span>
                </div>
                <span className="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
                <p className="font-body-sm text-on-surface-variant">Double masala street-style noodles tossed with crisp onions, bell peppers, sweet corn, and a squeeze of fresh lime.</p>
              </div>
              <div className="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
                <button
                  type="button"
                  className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all cursor-pointer"
                  onClick={() => handleAddToCart({ id: 'M01', name: 'KGP Maggi Bowl', price: 3.0, category: 'Meals' })}
                >
                  + Add to Order
                </button>
              </div>
            </div>

            {/* Favorite 5: Startup Burger */}
            <div className="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
              <div className="p-space-lg">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Startup Burger</h3>
                  <span className="font-headline-sm font-bold text-primary">$4.00</span>
                </div>
                <span className="inline-block bg-secondary-container text-on-secondary-container text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Non-Veg</span>
                <p className="font-body-sm text-on-surface-variant">Grilled herb patty with melted cheddar, crisp lettuce, spicy chipotle mayo on a toasted brioche bun.</p>
              </div>
              <div className="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
                <button
                  type="button"
                  className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all cursor-pointer"
                  onClick={() => handleAddToCart({ id: 'M07', name: 'Startup Burger', price: 4.0, category: 'Meals' })}
                >
                  + Add to Order
                </button>
              </div>
            </div>

            {/* Favorite 6: Stack Overflow Nachos */}
            <div className="bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 flex flex-col justify-between">
              <div className="p-space-lg">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Stack Overflow Nachos</h3>
                  <span className="font-headline-sm font-bold text-primary">$3.50</span>
                </div>
                <span className="inline-block bg-tertiary-fixed/60 text-on-tertiary-fixed-variant text-xs px-2 py-0.5 rounded-full font-label-md mb-2">Vegetarian</span>
                <p className="font-body-sm text-on-surface-variant">Crisp tortilla chips piled high with warm queso cheese sauce, fresh salsa, jalapeños, and sour cream.</p>
              </div>
              <div className="p-space-md bg-surface-container-low border-t border-outline-variant/20 flex justify-end">
                <button
                  type="button"
                  className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-1.5 rounded-full transition-all cursor-pointer"
                  onClick={() => handleAddToCart({ id: 'S08', name: 'Stack Overflow Nachos', price: 3.5, category: 'Snacks & Meals' })}
                >
                  + Add to Order
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Our Outlets */}
      <section className="py-space-xl bg-surface">
        <div className="max-w-[1280px] mx-auto px-gutter-desktop">
          <div className="text-center max-w-2xl mx-auto mb-space-xl">
            <span className="font-label-sm text-primary uppercase tracking-wider font-semibold">Locations</span>
            <h2 className="font-headline-lg text-headline-lg text-on-surface mt-1">Our Outlets</h2>
            <p className="font-body-md text-on-surface-variant mt-2">Find a comfortable table near you or order ahead for quick pickup.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-space-lg max-w-4xl mx-auto">
            <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-headline-sm text-headline-sm text-on-surface">Koramangala</h3>
                <span className="bg-tertiary-fixed text-on-tertiary-fixed text-xs px-2.5 py-0.5 rounded-full font-semibold">Open Daily</span>
              </div>
              <p className="font-body-sm text-on-surface-variant mb-3">No. 27, 6th Cross, 5th Block · Daily 8:00 AM – 10:00 PM</p>
              <p className="font-body-sm text-sm text-on-surface-variant mb-4">Our flagship cafe featuring outdoor patio seating, comfortable spaces, and warm campus energy.</p>
              <Link href="/cart" className="inline-block bg-primary hover:bg-primary-container text-on-primary font-label-md text-xs px-space-md py-2 rounded-full transition-all">
                Order Ahead for Koramangala
              </Link>
            </div>

            <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm border border-outline-variant/30">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-headline-sm text-headline-sm text-on-surface">Indiranagar</h3>
                <span className="bg-secondary-container text-on-secondary-container text-xs px-2.5 py-0.5 rounded-full font-semibold">Opening Soon</span>
              </div>
              <p className="font-body-sm text-on-surface-variant mb-3">100 Feet Road · Daily 8:00 AM – 10:00 PM</p>
              <p className="font-body-sm text-sm text-on-surface-variant mb-4">Our newest location bringing comfortable study corners and artisanal chai closer to office commuters.</p>
              <Link href="/menu" className="inline-block bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-label-md text-xs px-space-md py-2 rounded-full transition-all border border-outline-variant/40">
                Explore Launch Specials
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
