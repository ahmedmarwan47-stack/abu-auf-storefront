# Abu Auf — Static Frontend

A fully **static** Arabic-first storefront for **Abu Auf**, built on the
OrderBase static export and rebuilt against the Abu Auf Figma. Plain HTML +
Tailwind CSS (Play CDN) + vanilla JavaScript. No React, no build server, no
runtime — every page is a standalone `.html` file you can drop on any static
host (S3, Netlify, GitHub Pages, Cloudflare Pages, nginx…).

The site renders **right-to-left in Arabic** (`<html lang="ar" dir="rtl">`).

---

## Quick start

Because the pages load Tailwind and Google Fonts from a CDN, serve them over
HTTP (recommended) or open directly:

```bash
# from this folder
python3 -m http.server 8899
# then open http://localhost:8899/
```

Opening `index.html` via `file://` also works — pages carry no runtime data
fetching — but the Tailwind CDN and Google Fonts need an internet connection.

---

## Editing: two layers

**Layer 1 — runtime. Change these and every page updates on refresh, no build.**

| File | Owns |
|------|------|
| `tw-config.js` | All design tokens — colour, type scale, radii, shadows |
| `scripts.js`   | Header, footer, cart drawer, search, mobile menu, all behaviour |
| `styles.css`   | Base styles, tabs, accordions, drawers, carousel |

**Layer 2 — build-time components.** Page *content* is generated from shared
components so a card or section changes everywhere at once:

```bash
python3 build/build.py            # rebuild all 29 pages
python3 build/build.py home shop  # rebuild specific pages
```

- `build/components.py` — single source of truth for cross-page markup
  (product card, category tile, blog/recipe/review cards, buttons, forms,
  breadcrumb, carousel shell, page shell).
- `build/catalog.py` — shared data access and price/name formatting.
- `build/pages/<name>.py` — one module per page. Files prefixed `_` are shared
  layouts (`_listing`, `_auth`, `_account`, `_legal`), not pages.

The build fails loudly if a page references an asset that isn't in the export.

---

## Data

| File | Contents |
|------|----------|
| `data/catalog.json`  | 99 products, 12 categories — real names (Arabic + English), prices, images |
| `data/branches.json` | 316 real branches across 25 governorates |

Both were scraped from Abu Auf's public endpoints; see `build/scrape_assets.py`,
`build/fetch_arabic_names.py` and `build/fill_missing_names.py`.

---

## Project structure

```
static-export/
├── index.html                 # Home
├── <28 more>.html             # One file per route
│
├── tw-config.js               # Abu Auf design tokens
├── styles.css                 # Global CSS + component styles
├── scripts.js                 # Shared chrome + all interactions
│
├── data/                      # catalog.json, branches.json
├── images/abuauf/             # brand, icons, social, payments,
│                              #   categories, products, site imagery
└── css/                       # third-party CSS (toastify)
```

Every page provides two mount points — `#site-header` and `#site-footer` —
which `scripts.js` fills in, so the chrome stays DRY.

---

## Known gaps

See `../DESIGN-NOTES.md` for colour-contrast issues carried over faithfully
from the Figma, placeholder copy that needs client sign-off, and Figma export
quirks worth knowing about.
