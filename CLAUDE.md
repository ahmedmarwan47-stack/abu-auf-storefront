# CLAUDE.md — operating rules for this repo

Read this before touching anything. It is the standing brief; `HANDOFF.md` has
the rationale and history, `DESIGN-NOTES.md` has every open question and
deviation.

## What this project is

A **static Abu Auf storefront**, rebuilt from a Koueider/OrderBase static export
against the Abu Auf Figma (`tQiydoANmIdYWq0IfmTsMz`) and, increasingly, against
the live site at **abuauf.com**. 31 pages, Arabic-first, right-to-left. No
framework, no server — plain HTML + Tailwind Play CDN + vanilla JS.

Abu Auf is the client; we have rights to their assets.

**Status:** rebrand complete, mobile pass complete, cart **and favourites** are
real state with event APIs, listing filters and nav routes genuinely work, and
the chrome is measured against the live site. Remaining work is in
`DESIGN-NOTES.md` under "Open questions" and "Blocked on client data".

## Hard rules

1. **Never hand-edit `static-export/*.html`.** They are generated. Edit
   `build/` and run `python3 build/build.py`. The next build silently
   overwrites anything you type into the HTML.
2. **Changes must reflect site-wide.** An explicit client requirement. Shared
   markup goes in `build/components.py`; chrome (header/footer/overlays/cart) in
   `static-export/scripts.js`; tokens in `static-export/tw-config.js`. Never
   copy-paste between pages.
3. **Arabic-first, RTL.** Every page is `<html lang="ar" dir="rtl">`. Use
   logical properties (`ms/me`, `ps/pe`, `start/end`, `inset-inline`) — never
   `left`/`right`. New user-facing copy is Arabic. Latin runs get `class="latin"`.
4. **Measure, don't eyeball.** Design values come from Figma *variables*
   (`get_variable_defs`) or from measuring the live site in the browser. Several
   "it still looks bigger" rounds in this project were resolved only by opening
   abuauf.com and reading computed styles off it. Do that.
5. **Verify in the browser** — see "How to verify" below. Do not trust that a
   config change took effect.
6. **Real data over invented data.** If it can be fetched from Abu Auf's
   endpoints, fetch it. Anything you write yourself is placeholder and goes in
   `DESIGN-NOTES.md`. This has teeth: branch phone numbers, product compare-at
   prices and English prose were all left *missing* rather than invented.
7. **Don't silently "fix" the client's design system.** Flag deviations in
   `DESIGN-NOTES.md`. Sanctioned exceptions: colour contrast, and matching the
   live site where it differs from the Figma.
8. **Report failures honestly.** If something doesn't work, say so with the
   output.

## Three editing layers

**Runtime — no rebuild, refresh is enough:**

| File | Owns |
|---|---|
| `static-export/tw-config.js` | design tokens |
| `static-export/styles.css` | base styles, tabs, accordions, drawers, sheets, carousel |
| `static-export/scripts.js` | header, footer, mega-menu, cart store, i18n, all overlays |

**Build-time — `python3 build/build.py`:**

- `build/components.py` — single source of truth for shared markup
- `build/catalog.py` — data access, price/name formatting
- `build/pages/<name>.py` — one per page; `_`-prefixed are shared layouts
  (`_listing`, `_auth`, `_account`, `_legal`, `_geo`, `_posts`)

The build fails loudly on any unresolved asset reference. Keep it that way.

### Three systems inside `scripts.js` worth knowing before you edit it

**Cart store** — `window.abuaufCart`, persisted to `localStorage` under
`abuauf:cart`. `add/setQty/remove/clear/items/count/subtotal/find`. Every
mutation dispatches `cart:change` on `document` with
`{reason, product, items, count, subtotal}`. The renderer is a **keyed
reconcile, not an innerHTML swap** — rows keep their DOM nodes so animations and
focus survive. Don't "simplify" it back to innerHTML; that breaks the
micro-interaction work it exists for.

**Favourites store** — `window.abuaufFavs`, `localStorage` key `abuauf:favs`,
built to the same contract as the cart: `add/remove/toggle/has/items/count/
clear`, every mutation dispatching `favs:change` with
`{reason, product, items, count}`. Saved state is expressed by **`aria-pressed`
on the button and nothing else** — `styles.css` swaps the heart glyph off that
selector, so the accessible state and the painted state cannot drift. It
deliberately does not use the `hidden` attribute (see the `[hidden]` trap
below). `my-account-favorites.html` ships the whole catalogue hidden and
reveals what is saved, the same way the listing chips filter cards already in
the DOM — so card markup stays in `components.py` alone.

**Any seeded product must be keyed by its `catalog.json` id**, not its barcode.
Both stores dedupe on id against the `data-id` on product cards; a barcode key
silently creates a second line for a product already in the cart.

**i18n** — `t()` for chrome strings and `translateDocument()` for build-time
copy, both keyed off an `EN` dictionary of exact Arabic strings. Switching
language re-renders the injected chrome and walks text nodes, stashing originals
in a `WeakMap` so switching back is lossless. Exact-match only: a string with no
entry is deliberately left in Arabic rather than half-translated.

## Environment gotchas

These have each cost real time. Read them.

- **Python is 3.9.** f-strings reject backslashes inside the expression part.
- **Serve on a fresh port every time you check a CSS/JS change.**
  `python3 -m http.server` sends no cache headers and browsers hold assets hard.
  Two separate "this is still wrong" reports in this project were a stale port.
  Also confirm what the server is rooted at (`lsof -a -p <pid> -d cwd -Fn`).
- **`getComputedStyle` from the top-level document can be stale right after a
  viewport resize.** A no-media `!important` rule appeared to have no effect,
  which is impossible. **Screenshots and same-origin iframe measurements were
  both accurate.** If computed styles contradict a screenshot, distrust the
  computed style.
- **Tailwind Play CDN, nested colour keys:** a key containing a hyphen (e.g.
  `primary["on-dark"]`) produces **no usable class**. Accessibility tokens are
  deliberately flat: `onDarkGreen`, `onBlack`, `onBeigeMuted`.
- **Tailwind Play CDN, `xl:` variants:** on some elements the CDN simply did not
  apply an `xl:` variant — an identical probe element created at runtime
  resolved correctly while the real elements did not. Where this bites, author
  the rule in `styles.css` under a media query with a selector that wins on
  specificity (`a.chip-filter` beats `.bg-white`).
- **The `hidden` attribute is overridden by any author `display` rule.** An
  element with both `hidden` and `.flex` stays visible. `styles.css` carries
  `[hidden] { display: none !important; }` — anything toggling `hidden` on a
  flex/grid element depends on it.
- **Two Tailwind utilities in the same group tie on specificity, so emit order
  wins.** Adding `fixed` to an element whose base classes include `relative`
  does nothing — Tailwind emits `.relative` after `.fixed`. The sticky nav was
  broken this way for the whole project. Same remedy as the `xl:` trap: author
  the rule in `styles.css` on a selector that outranks a single class, e.g.
  `[data-navbar][data-stuck="true"]` (0,2,0).
- **Never let a missing asset fail silently.** `icon-leaf.svg` was referenced
  with `onerror="this.style.display='none'"` and did not exist — 8 broken
  images per page that nothing surfaced. The build only validates asset
  references in generated HTML, **not** the ones inside `scripts.js`.
- **Figma asset exports can be pre-transformed.** The logo exported upside-down
  and stretched (net vertical flip + `preserveAspectRatio="none"`). Several
  icons carry `preserveAspectRatio="none"` too. Check exported SVGs render.
- **`neutral.secondary` is for light surfaces only.** It inverts badly on black
  (3.29:1); use `onBlack` there.
- **`min-w-0` on flex/grid children.** The single most common bug class in this
  codebase. A `flex-1` child has `min-width: auto`, so it cannot shrink below its
  content and pushes its parent wider. Symptom: clipped content that page-level
  scroll never reveals, because a top-level `overflow-x-hidden` eats it.
  Related: `lg:grid-cols-[Npx_1fr]` **with no base rule** collapses below `lg`
  to one max-content column. Four separate pages had this.

## Layout constants

- **Content container is `mx-auto px-4 max-w-[1536px]`** — measured off the live
  site. Coloured bars stay full-bleed behind it. **The padding belongs on the
  same element as the cap**, not on a wrapper outside it: the header bands
  carried `px-4 xl:px-20` on the outer element, which subtracted 80px *before*
  `max-w-[1536px]` applied, so the cap never bound and the header ran 64px
  narrower than the page on all 31 pages.
- **Masthead logo is 120×31**; the real mark's aspect is **3.91** (524×134).
  Anything at aspect 3.0 is the old stretched box.
- **Header bands:** utility 33px, masthead 79px, nav 48px (total 161 live / 160
  ours). Footer 764 live / 767 ours.
- **Header z-order:** utility `z-50` > masthead `z-40` > nav `z-30`. Anything
  opening a dropdown must live in a bar above what it needs to overlap.
- **Tap targets are 44px minimum** (WCAG 2.5.5). Audited and passing; don't
  regress it.

## How to verify

```bash
python3 build/build.py                    # must report 31 pages, no missing assets
node --check static-export/scripts.js
grep -ril 'koueider\|kouider' static-export/   # must return nothing
git status --porcelain                    # rebuild must produce no diff
(cd static-export && python3 -m http.server <FRESH_PORT>)
```

Then in the browser run the **sweep** in `HANDOFF.md` §5 — it loads all 31 pages
in a same-origin iframe at 320/360/375/390/414 and reports horizontal overflow
plus WCAG contrast. Current baseline: **31/31 clean at every width, ~5000 text
nodes checked, 0 contrast failures.**

**Seed the cart before you quote that number.** An earlier "31/31 clean" was
measured against an emptied cart, so no cart line ever rendered and a 13px
overflow at 320 went unnoticed. `localStorage.removeItem("abuauf:cart")` before
sweeping re-seeds it.

The sweep distinguishes real overflow from intentional `line-clamp`/ellipsis
truncation. If you quote a number, know which you're quoting.

## Accessibility baseline

Passes **WCAG 2.1 AA** (4.5:1 body, 3:1 large) across all 31 pages, verified
against computed styles. Tap targets ≥44px. Don't regress either; re-run the
sweep after any colour or spacing change.

## Data

- `static-export/data/catalog.json` — 99 products (`nameAr` + English `name`,
  `categorySlug`, price/sale), 12 categories
- `static-export/data/branches.json` — 316 branches, 25 governorates.
  **Every `phone` field is empty** and there are no coordinates.

Scrapers: `build/scrape_assets.py`, `build/fetch_arabic_names.py`,
`build/fill_missing_names.py`.

Abu Auf's public routes are `/ar/category/<slug>` and `/ar/products/<slug>` —
**not** `/product-category/...`, which 404s. Product names are English in the
WooCommerce Store API under every locale hint; the Arabic ones are
server-rendered into the storefront's Next.js flight payload.

## Before launch

See `DESIGN-NOTES.md`. **Blocking:** the three legal pages are in-house
placeholder and must be replaced with the client's legal copy. Also outstanding:
branch phone numbers, real sale prices, and sign-off on every in-house English
and Arabic string.
