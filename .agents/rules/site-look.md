---
trigger: glob
globs: site/**
---

# Site Visual & Styling Rules

These rules apply to all files and components within the `site/` folder.

## 1. Visual Design, Colors, Fonts & Spacing

All visual design specifications—including color palette, typography, spacing, corner radius, elevation, and component styling—are defined in `DESIGN.md`.

- Refer directly to `DESIGN.md` for all color tokens, typography scales, spacing tokens, and component aesthetics.
- Do not redefine or override colors, fonts, or spacing tokens locally.

## 2. Customer Tone & Copy

While the visual style follows `DESIGN.md`, all customer-facing text, copy, and messaging must strictly adhere to `AGENTS.md`:
- Use plain, friendly, and welcoming language for customers.
- Do not use terminal-style syntax, CLI commands (e.g., `$ order --now`), or unnecessary technical jargon in customer-facing copy.

## 3. Scope Boundaries

Keep the site's scope as it is today:
- Do not implement dynamic telemetry or developer tools described in `DESIGN.md` (e.g., Command Palette modal, live Wi-Fi telemetry pinging, desk pool seating counters, or table reservations).
- Keep the site focused on menu browsing, item details, cart management, and the demo checkout flow.
