# New Page Quality Checklist

Use this checklist before and after creating any new page for the cafe website:

- [ ] **Header and footer come from the layout**: Do not include `<Header>` or `<Footer>` components in the page. `site/app/layout.jsx` wraps all pages with `Header`, `Footer`, and `MobileNav` automatically.
- [ ] **Colours and fonts from DESIGN.md**: Use the Warm Terminal Roast color tokens (`primary`, `secondary`, `surface`, `surface-container-*`, `on-surface`) and typography tokens (`font-display-hero`, `font-headline-*`, `font-body-*`, `font-label-*`) defined in `DESIGN.md`.
- [ ] **Prices in dollars with two decimals**: Every price displayed on the page must be formatted in USD with two decimal places (e.g., `$2.50`, `$3.50`, `$4.00`).
- [ ] **A link in the top menu**: Add a navigation link pointing to the new page in `site/components/Header.jsx` (and update `site/components/MobileNav.jsx` if mobile navigation should include it).
- [ ] **Every image the page uses exists**: Verify that all image paths referenced by the page actually exist under `site/public/` (e.g., `site/public/images/`) so no broken images are served.
- [ ] **The order test passes**: Run `python scripts/test_order_flow.py` and confirm that all order flow checks pass without regressions.
