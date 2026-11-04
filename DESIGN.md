# Design System: KGP Vibes Cafe

**Design System Theme:** Warm Terminal Roast  
**Design Movement:** Tactile Warmth & Developer Utility

---

## 1. Brand & Tone of Voice

Inspired by the collegiate coffeehouse tradition and developer subculture, KGP Vibes Cafe balances nostalgic campus study corners with the calm focus of a late-night hackathon. The atmosphere is an inviting sanctuary with reliable power outlets, high-speed Wi-Fi, and artisanal brews.

* **Target Customers:** Students, developers, tech workers, and creators seeking a calm, welcoming workspace with fast Wi-Fi to code, create, and collaborate.
* **Tone of Voice:** Friendly, tech-witty, calm, nostalgic, and unpretentious.
* **Brand Descriptors:** Welcoming, Tech-Witty, Nostalgic, Collaborative, and Energizing.
* **Visual Direction:** 
  * Paper-like tinted canvases, linen-soft cream backgrounds, and grounded espresso borders create an analog, tactile presence.
  * Syntax-styled micro-elements, inline badge pills shaped like terminal tags (`git pull origin coffee`, `<chai status="brewing" />`), and subtle monospaced metadata ground the product firmly in tech culture without feeling sterile or intimidating.
  * Interactions are deliberate, snappy, and calm—favoring warm micro-interactions over frantic, flashy animations.

---

## 2. Color Palette

The color palette balances warm organic cafe tones with sharp code-editor semantics.

### Core Brand Colors

| Token | Name | Hex Code | Usage |
| :--- | :--- | :--- | :--- |
| `primary` | Warm Chai Amber | `#C25E1A` | Key calls-to-action, primary ordering triggers, active table reservations, accents |
| `primary-container` | Roasted Amber | `#BA5814` | High-emphasis interactive elements, button hover transitions |
| `on-primary` | White | `#FFFFFF` | Text and icons on primary backgrounds |
| `secondary` | Deep Espresso Roast | `#2B1810` | Primary headlines, structural borders, navigation accents, high-emphasis controls |
| `secondary-container` | Toasted Biscuit | `#FCD8CA` | Secondary container surfaces, pill backgrounds |
| `on-secondary` | White | `#FFFFFF` | Text on secondary dark containers |
| `tertiary` | Matcha Green | `#2E7D5B` | Live operational status tokens (`seats: available`, `wifi: 350mbps`), health tags, organic markers |
| `tertiary-container` | Sage Container | `#348260` | Tertiary button/badge container |
| `on-tertiary` | White | `#FFFFFF` | Text and icons on tertiary backgrounds |

### Surface & Neutral Colors

| Token | Name | Hex Code | Usage |
| :--- | :--- | :--- | :--- |
| `surface` / `background` | Steamed Oat Cream | `#FAF7F2` / `#FCF9F4` | Primary canvas backdrop, soft paper texture base |
| `surface-dim` | Muted Parchment | `#DCDAD5` | Dimmed surface state, subtle dividers |
| `surface-bright` | Bright Oat | `#FAF7F2` | Highlighted surface base |
| `surface-container-lowest` | Pure White | `#FFFFFF` | Card backgrounds, elevated form inputs |
| `surface-container-low` | Light Linen | `#F6F3EE` | Resting card containers, nested panels |
| `surface-container` | Warm Oatmeal | `#F0EDE9` | Standard grouped containers |
| `surface-container-high` | Deep Parchment | `#EBE8E3` | Elevated card surfaces, hovered panels |
| `surface-container-highest` | Biscuit Surface | `#E5E2DD` | Highest elevation neutral container |
| `on-surface` | Deep Charcoal Roast | `#1C1C19` | High-contrast body text and titles |
| `on-surface-variant` | Espresso Muted | `#564339` | Secondary descriptions, captions, subtitled metadata |
| `inverse-surface` | Terminal Midnight | `#31302D` | Dark popups, inverted banners, command palette backdrop |
| `inverse-on-surface` | Cream White | `#F3F0EB` | Text on inverted surfaces |

### System Accents & Status Indicators

| Token | Name | Hex Code | Usage |
| :--- | :--- | :--- | :--- |
| `code-sky` | Code Sky | `#0284C7` | Technical micro-badges, IP addresses, terminal parameters, live ping |
| `border-muted` | Warm Biscuit Border | `#E8DFC8` / `#EADFC9` | Structural dividers, 1px card borders |
| `body-text` | Espresso Charcoal | `#1F1916` | Low-strain reading text (WCAG AAA compliant) |
| `terminal-inset` | Dark Espresso Inset | `#24150E` | Terminal blocks, code containers, live telemetry panels |
| `status-brewing-bg` | Brewing Yellow Light | `#FEF3C7` | Active brewing / order preparation tag background |
| `status-brewing-text` | Brewing Amber Dark | `#92400E` | Active brewing / order preparation tag text |
| `status-wifi-bg` | Wi-Fi Blue Light | `#E0F2FE` | Wi-Fi and speed telemetry badge background |
| `status-wifi-text` | Wi-Fi Blue Dark | `#0369A1` | Wi-Fi and speed telemetry badge text |
| `status-seats-bg` | Seats Green Light | `#DCFCE7` | Open seating badge background |
| `status-seats-text` | Seats Green Dark | `#15803D` | Open seating badge text |
| `error` | Red Alert | `#BA1A1A` | Error messages, failed checkout notices, validation alerts |
| `error-container` | Red Alert Tint | `#FFDAD6` | Error banner background |

---

## 3. Typography

The typographic stack contrasts literary academia with code-editor precision.

### Font Families

* **Headings:** **Literata** (Serif)  
  *Delivers an authentic editorial feel reminiscent of well-thumbed campus library books, literary journals, and cozy menu signboards.*
* **Body / Text:** **Plus Jakarta Sans** (Geometric Sans-Serif)  
  *Contemporary, clear, and fatigue-free for menus, narratives, and customer instructions.*
* **Labels & Code:** **JetBrains Mono** (Monospace) & **Plus Jakarta Sans** (UI Sans)  
  *Infuses witty terminal aesthetics into prices, telemetry, code pills, and metadata.*

### Type Scale & Hierarchy

| Role | Font Family | Size | Weight | Line Height | Letter Spacing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display Hero (Desktop)** | Literata | `56px` | `600` (SemiBold) | `64px` | `-0.02em` |
| **Display Hero (Mobile)** | Literata | `36px` | `600` (SemiBold) | `42px` | `-0.01em` |
| **Headline Large (Desktop)** | Literata | `36px` | `600` (SemiBold) | `44px` | `-0.015em` |
| **Headline Large (Mobile)** | Literata | `28px` | `600` (SemiBold) | `34px` | `-0.01em` |
| **Headline Medium** | Literata | `26px` | `500` (Medium) | `34px` | `-0.01em` |
| **Headline Small** | Literata | `20px` | `500` (Medium) | `28px` | `0` |
| **Body Large** | Plus Jakarta Sans | `18px` | `400` (Regular) | `28px` | `0` |
| **Body Medium** | Plus Jakarta Sans | `15px` | `400` (Regular) | `24px` | `0` |
| **Body Small** | Plus Jakarta Sans | `13px` | `400` (Regular) | `20px` | `0` |
| **Label Medium** | Plus Jakarta Sans | `14px` | `600` (SemiBold) | `20px` | `0` |
| **Label Small** | JetBrains Mono | `11px` | `400` (Regular) | `14px` | `+0.04em` |
| **Code Pill** | JetBrains Mono | `12px` | `500` (Medium) | `16px` | `+0.02em` |

---

## 4. Spacing System

Spacing is built on a consistent 4px baseline scale to ensure visual rhythm and comfortable scanning.

### Spacing Tokens

| Token | Rem | Pixels | Example Application |
| :--- | :--- | :--- | :--- |
| `space-xs` | `0.25rem` | `4px` | Micro-gaps between badge dot and text, hairline borders |
| `space-sm` | `0.5rem` | `8px` | Button vertical padding, chip gaps, compact list spacing |
| `space-md` | `1rem` | `16px` | Standard card internal padding, form input spacing |
| `space-lg` | `1.5rem` | `24px` | Section sub-dividers, button horizontal padding, card gaps |
| `space-xl` | `2.5rem` | `40px` | Major section margins, grid row gaps, hero header margins |

### Responsive Layout & Grid

* **Desktop (`>= 1024px`)**:
  * 12-column fluid grid
  * Max container width: `1280px` centered
  * Gutters: `2rem` (`32px`)
  * Margins: `3.5rem` (`56px`)
* **Tablet (`768px - 1023px`)**:
  * 8-column responsive grid
  * Gutters: `1.5rem` (`24px`)
  * Margins: `2rem` (`32px`)
* **Mobile (`< 768px`)**:
  * 4-column fluid stack
  * Gutters: `1.25rem` (`20px`)
  * Margins: `1rem` (`16px`)
  * Horizontal scrolling carousels with edge-fades for category filters

---

## 5. Corner Radius (Roundedness)

Approachable, ergonomic curves that mimic keyboard keys, smooth ceramic mugs, and modern application frames.

| Token | Value | Applied To |
| :--- | :--- | :--- |
| `rounded-sm` | `0.25rem` (`4px`) | Small tags, inline code snippets, subtle badges |
| `rounded-DEFAULT` | `0.5rem` (`8px`) | Standard text inputs, regular menu cards, modal dialogs, select dropdowns |
| `rounded-md` | `0.75rem` (`12px`) | Medium interactive cards, toast alerts, drawer containers |
| `rounded-lg` | `1rem` (`16px`) | Hero panels, featured station cards, workspace station tiles |
| `rounded-xl` | `1.5rem` (`24px`) | Checkout order review containers, floating sheets |
| `rounded-full` | `9999px` (Pill) | Primary & secondary CTA buttons, filter chips, terminal tags, status pills |

---

## 6. Elevation & Depth

Elevation uses **tonal paper layering** and **warm-tinted ambient shadows** rather than harsh, artificial dark shadows:

* **Layer 0 (Canvas):** `#FAF7F2` with optional subtle dot-matrix grid overlay (`24px` grid).
* **Layer 1 (Cards & Containers):** `#FFFFFF` or `#F6F3EE` bounded by a 1px solid border in `#E8DFC8`.
* **Layer 2 (Interactive Floating Cards & Trays):** Soft warm amber-tinted shadow: `0 8px 24px -4px rgba(43, 24, 16, 0.08)`.
* **Layer 3 (Modals & Command Palettes):** Deep ambient shadow: `0 20px 40px -8px rgba(43, 24, 16, 0.16)` paired with backdrop blur (`backdrop-filter: blur(8px); background: rgba(250, 247, 242, 0.85)`).
* **Terminal Insets:** Dark espresso `#24150E` with crisp monospaced contrast for telemetry, code blocks, and logs.

---

## 7. Component Styling Guidelines

### Buttons
* **Primary CTA:** Background `#C25E1A`, text `#FFFFFF` bold, full pill shape (`9999px`), padding `0.5rem 1.5rem` (`space-sm space-lg`). Hover darkens to `#A84F14` with a gentle `1px` translateY lift.
* **Developer Secondary:** Background `#2B1810`, text `#FFFFFF`, monospaced prefix (e.g. `$ order --now`).
* **Ghost / Tertiary:** Background `#FAF7F2`, 1px border `#EADFC9`, text `#1F1916`.

### Code Chips & Status Badges
* Monospaced (`JetBrains Mono`), pill-shaped (`9999px`), compact padding (`0.25rem 0.75rem`).
* **Status Brewing:** Background `#FEF3C7`, text `#92400E`, with pulsing dot indicator.
* **Wi-Fi Telemetry:** Background `#E0F2FE`, text `#0369A1` (e.g. `wifi: 480_mbps`).
* **Seat Availability:** Background `#DCFCE7`, text `#15803D` (e.g. `desk_pool: 6_open`).

### Menu Cards & Lists
* White or light oat surface bounded by `1px solid #E8DFC8`.
* Title in `Literata` serif; price and tasting notes in `JetBrains Mono` (e.g. `$3.50`, `notes: [hazelnut, dark_chocolate]`).
* Compact pill buttons for action slots.

### Form Inputs
* Rounded `0.5rem` (`8px`), background `#FFFFFF`, border `1.5px solid #D8CEB9`.
* Monospaced placeholder styling (`e.g., dev@campus.edu`). Focus ring highlights in Warm Chai Amber (`#C25E1A`) with soft `3px` ambient glow (`rgba(194, 94, 26, 0.2)`).

### Command Palette (`Cmd+K` / `Ctrl+K`)
* Spotlight modal styled with dark espresso backdrop `#24150E`, featuring a faux-terminal prompt (`> search menu, seats, wifi...`) with glowing matcha-green cursor blinks.
