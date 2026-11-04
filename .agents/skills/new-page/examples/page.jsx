'use client';

import { useState } from 'react';

const faqs = [
  {
    q: 'When are you open?',
    a: 'Every day, 8:00 AM to 10:00 PM, at both our Koramangala and Indiranagar locations.',
  },
  {
    q: 'Where are the cafes located?',
    a: (
      <span>
        <strong>Koramangala:</strong> No. 27, 6th Cross, Koramangala 5th Block, Bengaluru 560095<br />
        <strong>Indiranagar:</strong> 100 Feet Road, Indiranagar, Bengaluru 560038 (Opening Soon)
      </span>
    ),
  },
  {
    q: 'Do you have vegetarian and vegan options?',
    a: 'Yes! Almost every item on our menu is vegetarian. Vegan favorites include the Vibes Espresso Shot, KGP Cold Brew, Nitro Cold Brew, Cloud Fries, Algorithm Wrap, Server Side Salad, Backend Bowl, Chill Zone Mojito, and Bandwidth Lemonade. Any milk-based coffee can also be prepared with oat milk upon request.',
  },
  {
    q: 'Which menu items contain egg?',
    a: 'Only eight baked items contain egg: Byte Brownie, Python Pancakes, AI Waffle, Loop Croissant, Git Commit Cookies, Zero-Bug Brownie Sundae, Compile Cheesecake, and Runtime Tiramisu. Every other item is 100% egg-free.',
  },
  {
    q: 'Can I work on my laptop from the cafe?',
    a: 'Absolutely. Free high-speed Wi-Fi is available for all guests, and most tables have easy access to power sockets. During peak rush hours, we kindly ask laptop guests to share tables so everyone has a seat.',
  },
  {
    q: 'How does the order-ahead feature work?',
    a: 'Our website lets you pick your items, choose a pickup window, and receive an instant order number. When you arrive at the cafe, simply walk up to the pickup counter, quote your order number, pay via UPI, card, or cash, and collect your freshly prepared order without standing in the register line.',
  },
  {
    q: 'What payment methods do you take?',
    a: 'We accept UPI (Google Pay, PhonePe, Paytm, etc.), credit/debit cards, and cash at our counter. All prices on our menu include all applicable taxes.',
  },
  {
    q: 'Do you take group bookings?',
    a: 'Yes, we welcome group reservations for 6 or more people, study meetups, and office catering. Reach out via email or ask our counter staff.',
  },
];

export default function AboutPage() {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleFaq = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="w-full bg-background pb-16">
      {/* Hero Header */}
      <section className="bg-surface-container-low py-12 md:py-16 border-b border-outline-variant/30 text-center">
        <div className="max-w-[1280px] mx-auto px-gutter-desktop">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-md text-xs mb-4">
            <span>🌱 Our Origins</span>
          </div>
          <h1 className="font-display-hero text-3xl md:text-5xl text-on-surface font-semibold mb-4">
            The Story Behind the Vibes
          </h1>
          <p className="font-body-lg text-on-surface-variant max-w-2xl mx-auto leading-relaxed">
            How a passion for technology, college nostalgia, and real chai came together to create your neighborhood workspace cafe.
          </p>
        </div>
      </section>

      {/* Founder & Story Section */}
      <section className="py-12 max-w-[1000px] mx-auto px-gutter-desktop">
        <div className="bg-surface-container-lowest rounded-2xl p-8 md:p-12 shadow-sm border border-outline-variant/30 mb-12">
          <h2 className="font-headline-lg text-2xl md:text-3xl text-secondary mb-4 font-semibold">
            From IIT Kharagpur to the Coffee Bar
          </h2>
          <blockquote className="font-headline-md italic text-primary text-lg md:text-xl border-l-4 border-primary pl-4 mb-6 leading-relaxed">
            “The most transformative ideas do not originate in fluorescent conference rooms. They happen around a steaming cup of chai with good friends and an open laptop.”
          </blockquote>
          <p className="font-body-md text-on-surface-variant mb-4 leading-relaxed">
            KGP Vibes Cafe was founded by Laxmi Kant, an alumnus of IIT Kharagpur who spent over a decade writing software, architecting systems, and mentoring developers. Throughout his tech career, he observed that teams solved their hardest debugging challenges and forged their best startup concepts while huddled over hot chai and casual bites.
          </p>
          <p className="font-body-md text-on-surface-variant leading-relaxed">
            He set out to build the exact haven he always wished existed: a cafe combining authentic Indian tea, artisan coffee, and honest prices with rock-solid Wi-Fi, plenty of power sockets, and a supportive atmosphere where students and engineers feel welcome to stay, code, and chat.
          </p>
        </div>

        {/* Values Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm border border-outline-variant/30">
            <div className="text-3xl mb-3">🍵</div>
            <h3 className="font-headline-sm text-lg text-on-surface font-semibold mb-2">Good Chai at Fair Prices</h3>
            <p className="font-body-sm text-sm text-on-surface-variant leading-relaxed">
              Every menu item is priced fairly between $2.00 and $6.50, crafted with fresh, clean ingredients.
            </p>
          </div>
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm border border-outline-variant/30">
            <div className="text-3xl mb-3">🔌</div>
            <h3 className="font-headline-sm text-lg text-on-surface font-semibold mb-2">Built for Deep Work</h3>
            <p className="font-body-sm text-sm text-on-surface-variant leading-relaxed">
              Work undisturbed. We provide high-speed internet and power outlets at virtually every seat.
            </p>
          </div>
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm border border-outline-variant/30">
            <div className="text-3xl mb-3">🤝</div>
            <h3 className="font-headline-sm text-lg text-on-surface font-semibold mb-2">Community First</h3>
            <p className="font-body-sm text-sm text-on-surface-variant leading-relaxed">
              We know our regulars by name, support local student projects, and keep the vibe warm and welcoming.
            </p>
          </div>
        </div>

        {/* FAQs */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-md text-xs mb-3">
            <span>❓ Frequently Asked Questions</span>
          </div>
          <h2 className="font-headline-lg text-2xl md:text-3xl text-on-surface font-semibold mb-2">
            Everything You Might Want to Know
          </h2>
          <p className="font-body-md text-on-surface-variant max-w-xl mx-auto">
            Quick answers about our hours, menu options, work tables, and pickup ordering.
          </p>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div
                key={idx}
                className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 overflow-hidden shadow-xs"
              >
                <button
                  type="button"
                  onClick={() => toggleFaq(idx)}
                  className="w-full px-6 py-4 flex items-center justify-between text-left font-headline-sm text-base text-on-surface hover:text-primary transition-colors cursor-pointer"
                >
                  <span className="font-medium">{faq.q}</span>
                  <span className={`transform transition-transform text-primary font-bold ${isOpen ? 'rotate-180' : ''}`}>
                    ▾
                  </span>
                </button>
                {isOpen && (
                  <div className="px-6 pb-4 pt-1 font-body-sm text-sm text-on-surface-variant border-t border-outline-variant/15 leading-relaxed">
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
