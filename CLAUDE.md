# CLAUDE.md — operating rules for this repo

Read this before touching anything. It is the standing brief; `HANDOFF.md` has
the full rationale and decision history.

## What this project is

A **static Abu Auf storefront**, rebuilt from a Koueider/OrderBase static export
against the Abu Auf Figma (`tQiydoANmIdYWq0IfmTsMz`). 29 pages, Arabic-first,
right-to-left. No framework, no server — plain HTML + Tailwind Play CDN +
vanilla JS. Abu Auf is the client; we have rights to their assets.

Status: the rebrand is **complete**. Zero Koueider references remain. Next phase
is Ahmed's own enhancements, plus a mobile pass against the Figma `Mobile` page.

## Hard rules

1. **Never hand-edit `static-export/*.html`.** They are generated. Edit
   `build/` and run `python3 build/build.py`. The next build silently
   overwrites anything you type into the HTML.
2. **Changes must reflect site-wide.** This was an explicit client requirement.
   Put shared markup in `build/components.py`, never copy-paste between pages.
   Chrome (header/footer/overlays) belongs in `static-export/scripts.js`;
   tokens in `static-export/tw-config.js`.
3. **Arabic-first, RTL.** Every page is `<html lang="ar" dir="rtl">`. Use
   logical properties (`ms/me`, `ps/pe`, `start/end`) — never `left`/`right`.
   New user-facing copy is Arabic. Latin runs (prices, SKUs) get `class="latin"`.
4. **Design tokens come from Figma *variables*, not from eyeballing screenshots.**
   Use `get_variable_defs` on a node.
5. **Verify in the browser, with computed styles.** Do not trust that a config
   change took effect. This repo has already burned a cycle on exactly that.
6. **Real data over invented data.** If it can be fetched from Abu Auf's public
   endpoints, fetch it. If you invent copy, label it as placeholder in
   `DESIGN-NOTES.md`.
7. **Don't silently "fix" the client's design system.** Flag deviations in
   `DESIGN-NOTES.md`. The one sanctioned exception is colour contrast, which
   Ahmed explicitly asked to fix — the build now intentionally diverges from the
   Figma there.
8. **Report failures honestly.** If something doesn't work, say so with the
   output. Don't paper over it.

## Two editing layers

**Runtime — no rebuild, refresh is enough:**
- `static-export/tw-config.js` — all design tokens
- `static-export/scripts.js` — header, footer, cart drawer, search, mobile menu, behaviour
- `static-export/styles.css` — base styles, tabs, accordions, drawers, carousel

**Build-time — `python3 build/build.py` to apply:**
- `build/components.py` — single source of truth for cross-page markup
- `build/catalog.py` — data access, price/name formatting
- `build/pages/<name>.py` — one per page; `_`-prefixed files are shared layouts
  (`_listing`, `_auth`, `_account`, `_legal`, `_geo`, `_posts`)

The build fails loudly on any asset reference that doesn't resolve. Keep it that way.

## Environment gotchas

- **Python is 3.9.** f-strings reject backslashes inside the expression part.
- **Tailwind Play CDN:** a nested colour key containing a hyphen (e.g.
  `primary["on-dark"]`) produces **no usable class** — `text-primary-on-dark` is
  ambiguous between colour and shade and silently falls back to the inherited
  colour. Accessibility tokens are deliberately flat: `onDarkGreen`, `onBlack`,
  `onBeigeMuted`.
- **Figma asset exports can be pre-transformed.** The logo exported upside-down
  and stretched (its wrapper carried a net vertical flip plus
  `preserveAspectRatio="none"`). Check exported SVGs render correctly.
- **`neutral.secondary` is for light surfaces only.** It inverts badly on black
  (3.29:1); use `onBlack` there.
- Serving over `python3 -m http.server` caches aggressively — bump the port to
  force a clean load when verifying CSS/JS changes.

## Accessibility baseline

The site passes **WCAG 2.1 AA** (4.5:1 body, 3:1 large). Verified live against
computed styles: 0 failures on index/checkout/my-account/shop-category. Don't
regress it. Re-run the audit in `HANDOFF.md` after any colour change.

## Data

- `static-export/data/catalog.json` — 99 products (`nameAr` + English), 12 categories
- `static-export/data/branches.json` — 316 branches, 25 governorates

Scrapers: `build/scrape_assets.py`, `build/fetch_arabic_names.py`,
`build/fill_missing_names.py`.

Abu Auf's public routes are `/ar/category/<slug>` and `/ar/products/<slug>` —
**not** `/product-category/...`, which 404s. Product names are English in the
WooCommerce Store API under every locale hint; the Arabic ones are
server-rendered into the storefront's Next.js flight payload.

## Before launch

See `DESIGN-NOTES.md`. Blocking: the three legal pages are placeholder text
written in-house and **must** be replaced with the client's legal copy.
