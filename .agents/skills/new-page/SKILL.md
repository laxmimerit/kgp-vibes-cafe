---
name: new-page
description: >-
  Adds a new page to the cafe website adhering to the house style, layout standards,
  and design system. Use this skill whenever creating a new route or page for the cafe website.
---

# New Page Creation

Follow these steps to create a new page for the KGP Vibes Cafe website that matches the house style, design system, and project rules.

Before starting, consult the reference page and checklist provided with this skill:
- Reference implementation: [`examples/page.jsx`](examples/page.jsx) (copied from `site/app/about/page.jsx`)
- Quality checklist: [`resources/checklist.md`](resources/checklist.md)

---

## Steps

1. **Review the Reference Page & Design System**
   - Inspect [`examples/page.jsx`](examples/page.jsx) to understand how pages are structured, styled, and laid out. Notice section dividers, hero headers, badge pills, cards, and Tailwind CSS utility usage.
   - Reference `DESIGN.md` for official brand colors (e.g., `primary`, `secondary`, `surface`, `surface-container-low`), typography styles (`font-display-hero`, `font-headline-*`, `font-body-*`, `font-label-*`), and the Warm Terminal Roast theme.

2. **Create the Route Page Component**
   - Create a new directory under `site/app/<route-name>/` and add `page.jsx`.
   - **Header and Footer**: Do not import or render `<Header>` or `<Footer>` inside the page component. The root layout in `site/app/layout.jsx` automatically wraps all pages with the header, footer, and mobile nav.
   - **Tone and Voice**: Keep messaging friendly, approachable, and plain.
   - **No Dates or Years**: Do not display years or calendar dates anywhere on the page.
   - **Price Formatting**: If any prices are shown, format them in USD with two decimal places (e.g., `$2.50`, `$3.50`).

3. **Verify Assets and Images**
   - Confirm that every image the page references actually exists under `site/public/` (e.g., `site/public/images/`).
   - If new images are required, place them in `site/public/images/` before referencing them in code.

4. **Add Navigation Links**
   - Add a navigation link to the top menu in `site/components/Header.jsx` under the desktop `<nav>` section.
   - If the new page should also appear in mobile bottom navigation, update `site/components/MobileNav.jsx`.

5. **Validate with the Checklist**
   - Review each item in [`resources/checklist.md`](resources/checklist.md):
     - Header and footer come from the layout.
     - Colours and fonts from `DESIGN.md`.
     - Prices in dollars with two decimals.
     - A link in the top menu.
     - Every image the page uses exists.
     - The order test passes.

6. **Build and Test Verification**
   - Build the Next.js site to verify compilation and static generation:
     ```bash
     cd site && npm run build && cd ..
     ```
   - Run the order flow test suite to ensure the ordering flow remains intact and no regressions occurred:
     ```bash
     python scripts/test_order_flow.py
     ```
