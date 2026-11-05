'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';

const FAQ_CATEGORIES = [
  { id: 'all', label: 'All Questions', icon: '✨' },
  { id: 'pickup', label: 'Pickup & Ordering', icon: '🛍️' },
  { id: 'locations', label: 'Outlets & Hours', icon: '📍' },
  { id: 'workspace', label: 'Wi-Fi & Workspace', icon: '💻' },
  { id: 'menu', label: 'Menu & Dietary', icon: '☕' },
  { id: 'payments', label: 'Payment & Demo', icon: '💳' },
];

const FAQS = [
  {
    id: 'pickup-counter',
    category: 'pickup',
    tag: 'Pickup Counter',
    question: 'How does in-store pickup work?',
    answer:
      'Walk up to the pickup counter, quote your order number, and collect your freshly prepared food and drinks without waiting in the register line.',
  },
  {
    id: 'order-ahead-pickup',
    category: 'pickup',
    tag: 'Ordering Ahead',
    question: 'Can I order ahead for pickup?',
    answer:
      'Yes, visit our menu page to choose your favorites and order ahead for quick pickup.',
  },
  {
    id: 'order-ahead-flow',
    category: 'pickup',
    tag: 'Ordering Ahead',
    question: 'How do I order ahead on the website?',
    answer:
      'Select your favorite items online, choose a convenient pickup window, and receive an instant order number to quote at the counter.',
  },
  {
    id: 'order-ahead-time',
    category: 'pickup',
    tag: 'Pickup Time',
    question: 'How long does an order ahead take?',
    answer: 'Most orders are ready in about 15 minutes.',
  },
  {
    id: 'customization',
    category: 'pickup',
    tag: 'Customization',
    question: 'Can I customize sweetness or milk preferences?',
    answer:
      'Yes, simply let our counter barista know your milk choice or sweetness preference when you collect your order.',
  },
  {
    id: 'opening-hours',
    category: 'locations',
    tag: 'Hours',
    question: 'What are your opening hours?',
    answer:
      'We are open every day from 8:00 AM to 10:00 PM at both our Koramangala and Indiranagar locations.',
  },
  {
    id: 'outlets-locations',
    category: 'locations',
    tag: 'Outlets',
    question: 'Where are your two cafe outlets located?',
    answer:
      'We welcome you in Koramangala at No. 27, 6th Cross, Koramangala 5th Block, Bengaluru 560095, and in Indiranagar at 100 Feet Road, Indiranagar, Bengaluru 560038.',
  },
  {
    id: 'payment-methods',
    category: 'payments',
    tag: 'Payment Methods',
    question: 'What payment methods do you accept?',
    answer:
      'We accept UPI, debit or credit cards, and cash at our counter when you pick up your order. Website checkout is a demo order-ahead system with no online payment needed.',
  },
  {
    id: 'demo-checkout',
    category: 'payments',
    tag: 'Demo Checkout',
    question: 'Do I need to enter credit card details on the website?',
    answer:
      'No, our online ordering system is strictly a demo preview that never asks for, collects, or stores credit cards or real payment details.',
  },
  {
    id: 'wifi-and-laptops',
    category: 'workspace',
    tag: 'Wi-Fi & Power',
    question: 'Can I work on my laptop and use the Wi-Fi?',
    answer:
      'Yes, we provide free high-speed Wi-Fi and power outlets at most seats, and we kindly ask laptop guests to share tables during busy rush hours.',
  },
  {
    id: 'group-bookings',
    category: 'workspace',
    tag: 'Group Bookings',
    question: 'Do you take group bookings or study meetups?',
    answer:
      'Yes, we warmly welcome group reservations for 6 or more people, study meetups, and office catering when you reach out in advance.',
  },
  {
    id: 'dietary-options',
    category: 'menu',
    tag: 'Dietary Options',
    question: 'Do you offer vegetarian, vegan, and egg-free options?',
    answer:
      'Almost every item on our menu is vegetarian, oat milk is available on request, and all items except eight baked treats are completely egg-free.',
  },
  {
    id: 'bring-own-cup',
    category: 'menu',
    tag: 'Reusable Cups',
    question: 'Can I bring my own cup?',
    answer: 'Yes, any of our hot drinks can go in your own clean cup.',
  },
  {
    id: 'pricing-range',
    category: 'menu',
    tag: 'Menu Pricing',
    question: 'What are your menu prices?',
    answer:
      'Every handcrafted tea, cold brew, and fresh bite is priced honestly between $2.00 and $6.50.',
  },
];

export default function FaqPage() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [openIds, setOpenIds] = useState(() => new Set(['pickup-counter', 'order-ahead-pickup', 'opening-hours']));

  const toggleAccordion = (id) => {
    setOpenIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const expandAll = () => {
    setOpenIds(new Set(FAQS.map((f) => f.id)));
  };

  const collapseAll = () => {
    setOpenIds(new Set());
  };

  const filteredFaqs = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return FAQS.filter((faq) => {
      const matchesCategory =
        selectedCategory === 'all' || faq.category === selectedCategory;
      const matchesQuery =
        !q ||
        faq.question.toLowerCase().includes(q) ||
        faq.answer.toLowerCase().includes(q) ||
        faq.tag.toLowerCase().includes(q);
      return matchesCategory && matchesQuery;
    });
  }, [selectedCategory, searchQuery]);

  return (
    <div className="w-full bg-background pb-20">
      {/* Hero Header Section */}
      <section className="bg-surface-container-low py-12 md:py-16 border-b border-outline-variant/30 text-center">
        <div className="max-w-[1280px] mx-auto px-gutter-desktop">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-md text-xs mb-4 shadow-xs">
            <span>Frequently Asked Questions</span>
          </div>

          <h1 className="font-display-hero text-3xl md:text-5xl text-on-surface font-semibold mb-4 tracking-tight">
            Help &amp; Answers
          </h1>

          <p className="font-body-lg text-on-surface-variant max-w-2xl mx-auto leading-relaxed">
            Everything you need to know about our freshly brewed chai, easy pickup counter, opening hours, and workspace amenities.
          </p>

          {/* Quick Stats / Info Badges */}
          <div className="mt-8 flex flex-wrap justify-center items-center gap-3">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-lowest border border-outline-variant/40 text-on-surface font-body-sm text-xs shadow-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>Open Daily: 8:00 AM – 10:00 PM</span>
            </div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-lowest border border-outline-variant/40 text-on-surface font-body-sm text-xs shadow-xs">
              <span>📍 Koramangala &amp; Indiranagar</span>
            </div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-lowest border border-outline-variant/40 text-on-surface font-body-sm text-xs shadow-xs">
              <span>⚡ Free Fast Wi-Fi &amp; Outlets</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main FAQ Content Section */}
      <section className="max-w-[960px] mx-auto px-gutter-desktop pt-10">
        {/* Search & Filter Controls */}
        <div className="bg-surface-container-lowest rounded-2xl p-6 shadow-sm border border-outline-variant/30 mb-8">
          <div className="relative mb-5">
            <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-on-surface-variant text-base">
              🔍
            </span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search questions by keyword (e.g. pickup, wifi, vegan, payment)..."
              className="w-full pl-10 pr-10 py-3 rounded-xl bg-surface-container-low border border-outline-variant/40 text-on-surface placeholder-on-surface-variant/60 font-body-md text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              aria-label="Search frequently asked questions"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-on-surface-variant hover:text-on-surface text-sm cursor-pointer"
                aria-label="Clear search query"
              >
                ✕
              </button>
            )}
          </div>

          {/* Category Filter Chips */}
          <div className="flex flex-wrap items-center gap-2">
            {FAQ_CATEGORIES.map((cat) => {
              const isActive = selectedCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-3.5 py-1.5 rounded-full font-label-md text-xs sm:text-sm flex items-center gap-1.5 transition-all cursor-pointer ${
                    isActive
                      ? 'bg-primary text-on-primary shadow-xs font-semibold'
                      : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-container hover:text-on-surface border border-outline-variant/30'
                  }`}
                  aria-pressed={isActive}
                >
                  <span>{cat.icon}</span>
                  <span>{cat.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Toolbar: Results Count & Expand/Collapse */}
        <div className="flex items-center justify-between gap-4 mb-4 px-1">
          <p className="font-body-sm text-xs sm:text-sm text-on-surface-variant">
            Showing <span className="font-semibold text-on-surface">{filteredFaqs.length}</span>{' '}
            {filteredFaqs.length === 1 ? 'question' : 'questions'}
            {searchQuery && <span> for &ldquo;{searchQuery}&rdquo;</span>}
          </p>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={expandAll}
              className="font-label-sm text-xs text-primary hover:underline cursor-pointer"
            >
              Expand all
            </button>
            <span className="text-outline-variant text-xs">·</span>
            <button
              type="button"
              onClick={collapseAll}
              className="font-label-sm text-xs text-secondary hover:underline cursor-pointer"
            >
              Collapse all
            </button>
          </div>
        </div>

        {/* Accordion List */}
        {filteredFaqs.length === 0 ? (
          <div className="bg-surface-container-lowest rounded-2xl p-10 text-center border border-outline-variant/30">
            <div className="text-4xl mb-3">🔍</div>
            <h3 className="font-headline-sm text-lg text-on-surface font-semibold mb-2">
              No matching questions found
            </h3>
            <p className="font-body-md text-sm text-on-surface-variant max-w-md mx-auto mb-5">
              We couldn&apos;t find any answers matching your query, so please try a different keyword or choose a category above.
            </p>
            <button
              type="button"
              onClick={() => {
                setSearchQuery('');
                setSelectedCategory('all');
              }}
              className="bg-primary text-on-primary px-4 py-2 rounded-full font-label-md text-xs shadow-xs hover:bg-primary-container transition-colors cursor-pointer"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="space-y-3.5">
            {filteredFaqs.map((faq) => {
              const isOpen = openIds.has(faq.id);
              return (
                <div
                  key={faq.id}
                  className={`bg-surface-container-lowest rounded-2xl border transition-all duration-200 overflow-hidden ${
                    isOpen
                      ? 'border-primary/40 shadow-sm ring-1 ring-primary/10'
                      : 'border-outline-variant/30 hover:border-outline-variant/60 shadow-xs'
                  }`}
                >
                  <button
                    type="button"
                    onClick={() => toggleAccordion(faq.id)}
                    aria-expanded={isOpen}
                    className="w-full px-6 py-4 sm:py-5 flex items-start justify-between gap-4 text-left cursor-pointer group"
                  >
                    <div className="flex flex-col gap-1.5 pr-2">
                      <span className="font-label-sm font-mono text-[11px] uppercase tracking-wider text-primary font-semibold">
                        {faq.tag}
                      </span>
                      <span className="font-headline-sm text-base sm:text-lg text-on-surface group-hover:text-primary transition-colors font-medium">
                        {faq.question}
                      </span>
                    </div>
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 transition-transform duration-200 ${
                        isOpen
                          ? 'bg-primary text-on-primary rotate-180'
                          : 'bg-surface-container-low text-on-surface-variant group-hover:bg-surface-container'
                      }`}
                      aria-hidden="true"
                    >
                      <span className="text-xs font-bold leading-none">▾</span>
                    </div>
                  </button>

                  {isOpen && (
                    <div className="px-6 pb-5 pt-1 border-t border-outline-variant/15 font-body-md text-sm text-on-surface-variant leading-relaxed">
                      <p>
                        {faq.answer.includes('menu page') ? (
                          <>
                            {faq.answer.split('menu page')[0]}
                            <Link href="/menu" className="text-primary underline hover:opacity-80 font-medium">
                              menu page
                            </Link>
                            {faq.answer.split('menu page')[1]}
                          </>
                        ) : (
                          faq.answer
                        )}
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Demo Checkout Notice Banner */}
        <div className="mt-12 bg-secondary-container/50 border border-outline-variant/40 rounded-2xl p-6 flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-xl shrink-0 font-bold">
            🛡️
          </div>
          <div className="flex-1">
            <h4 className="font-headline-sm text-base text-on-surface font-semibold mb-1">
              Demo Order-Ahead Experience
            </h4>
            <p className="font-body-sm text-xs sm:text-sm text-on-surface-variant leading-relaxed">
              Our online ordering is strictly a demo system, so you simply pay when you collect your order at the counter.
            </p>
          </div>
          <Link
            href="/cart"
            className="shrink-0 bg-primary hover:bg-primary-container text-on-primary px-4 py-2 rounded-full font-label-md text-xs shadow-xs transition-colors"
          >
            Try Demo Checkout
          </Link>
        </div>

        {/* Two Outlets Quick Location Cards */}
        <div className="mt-12">
          <div className="text-center mb-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-md text-xs mb-2">
              <span>📍 Visit Our Cafes</span>
            </div>
            <h2 className="font-headline-lg text-2xl md:text-3xl text-on-surface font-semibold">
              Our Two Bengaluru Locations
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Koramangala Outlet */}
            <div className="bg-surface-container-lowest rounded-2xl p-6 sm:p-7 border border-outline-variant/30 shadow-xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-label-sm font-mono text-[11px] text-primary uppercase font-bold tracking-wider">
                    Outlet 01
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-medium">
                    Open Daily
                  </span>
                </div>
                <h3 className="font-headline-sm text-xl text-on-surface font-semibold mb-2">
                  Koramangala
                </h3>
                <p className="font-body-md text-sm text-on-surface-variant mb-4 leading-relaxed">
                  No. 27, 6th Cross, Koramangala 5th Block, Bengaluru 560095
                </p>
                <div className="space-y-1.5 text-xs text-on-surface-variant font-body-sm mb-6 border-t border-outline-variant/20 pt-3">
                  <div className="flex items-center gap-2">
                    <span>⏰</span>
                    <span>8:00 AM to 10:00 PM Every Day</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>⚡</span>
                    <span>High-Speed Wi-Fi &amp; Laptop Tables</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>🛍️</span>
                    <span>Quick Order-Ahead Pickup Counter</span>
                  </div>
                </div>
              </div>
              <Link
                href="/menu"
                className="w-full text-center py-2.5 rounded-xl bg-surface-container-low hover:bg-surface-container text-primary font-label-md text-xs border border-outline-variant/30 transition-colors"
              >
                Browse Menu for Koramangala
              </Link>
            </div>

            {/* Indiranagar Outlet */}
            <div className="bg-surface-container-lowest rounded-2xl p-6 sm:p-7 border border-outline-variant/30 shadow-xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-label-sm font-mono text-[11px] text-primary uppercase font-bold tracking-wider">
                    Outlet 02
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-medium">
                    Open Daily
                  </span>
                </div>
                <h3 className="font-headline-sm text-xl text-on-surface font-semibold mb-2">
                  Indiranagar
                </h3>
                <p className="font-body-md text-sm text-on-surface-variant mb-4 leading-relaxed">
                  100 Feet Road, Indiranagar, Bengaluru 560038
                </p>
                <div className="space-y-1.5 text-xs text-on-surface-variant font-body-sm mb-6 border-t border-outline-variant/20 pt-3">
                  <div className="flex items-center gap-2">
                    <span>⏰</span>
                    <span>8:00 AM to 10:00 PM Every Day</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>⚡</span>
                    <span>High-Speed Wi-Fi &amp; Laptop Tables</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>🛍️</span>
                    <span>Quick Order-Ahead Pickup Counter</span>
                  </div>
                </div>
              </div>
              <Link
                href="/menu"
                className="w-full text-center py-2.5 rounded-xl bg-surface-container-low hover:bg-surface-container text-primary font-label-md text-xs border border-outline-variant/30 transition-colors"
              >
                Browse Menu for Indiranagar
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom CTA Banner */}
        <div className="mt-14 bg-surface-container-low rounded-2xl p-8 text-center border border-outline-variant/30">
          <h3 className="font-headline-md text-2xl text-on-surface font-semibold mb-2">
            Still Have Questions?
          </h3>
          <p className="font-body-md text-sm sm:text-base text-on-surface-variant max-w-xl mx-auto mb-6 leading-relaxed">
            Come say hello at our pickup counter or order your favorite chai and bites ahead of time to skip the line.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/menu"
              className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-sm px-6 py-2.5 rounded-full shadow-xs transition-colors"
            >
              Browse Full Menu
            </Link>
            <Link
              href="/cart"
              className="bg-surface-container-lowest hover:bg-surface-container-high text-on-surface font-label-md text-sm px-6 py-2.5 rounded-full border border-outline-variant/40 transition-colors"
            >
              Start Pickup Order
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
