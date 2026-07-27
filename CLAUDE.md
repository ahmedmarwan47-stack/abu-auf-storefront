# CLAUDE.md — operating rules for this repo

Read this before touching anything. It is the standing brief; `HANDOFF.md` has
the rationale and history, `DESIGN-NOTES.md` has every open question and
deviation.

## What this project is

A **static Abu Auf storefront**, rebuilt from a Koueider/OrderBase static export
against the Abu Auf Figma (`tQiydoANmIdYWq0IfmTsMz`) and, increasingly, against
the live site at **abuauf.com**. 31 core pages plus a generated
`product-<id>.html` for every catalogue product (130 HTML files), Arabic-first,
right-to-left. No framework, no server — plain HTML + a build-time Tailwind
stylesheet + vanilla JS.

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
   `static-export/scripts.js`; tokens in `tailwind.config.js`. Never
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
8. **Never paint a "selected" state the way a "hover" state is painted.**
   This has been reported four times across two components. If pointing at a
   thing also selects it, an identical treatment makes the survivor look stuck
   under a pointer that left. Selected gets weight, a marker bar, ink colour;
   hover gets a transient wash. See `.nav-underline` and `.mega-cat`.
8. **Report failures honestly.** If something doesn't work, say so with the
   output.

## Three editing layers

**Runtime — no rebuild, refresh is enough:**

| File | Owns |
|---|---|
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

**Card stepper** — once a product is in the cart, its card swaps the add button
for a `−/n/+` control (`[data-card-stepper]`, `[data-card-step]`,
`[data-card-qty]`). It is not separate state: `syncCardSteppers()` runs on every
`cart:change` and reads the store by the card's `data-id`, so every card for the
same product stays in step, the drawer and the cards agree, and a reload
restores it. Stepping below 1 removes the line and the add button returns. Each
`+` fires the flight again — that repetition is the point, don't quietly drop
it. The control and the add button carry the **same `basis-[104px]`** so they
wrap identically and the card never changes height on the swap; read the `basis`
vs `min-width` note in `DESIGN-NOTES.md` §8 before touching those numbers.

**Motion** — `flyTo(source, target, ghostHTML?, opts?)` arcs a fixed-position
clone to a destination and resolves on landing; `pulse(el)` is the landing beat.
The flight is **two stages**: a *pick-up*, where the ghost stays put and
condenses into a small rounded shadowed white tile (`opts.card`, optionally with
a `+n` chip via `opts.tag`), then the throw. The tile **keeps** its gathered
scale for the whole flight — `is-picked` stays on; removing it mid-flight makes
the ghost swell in mid-air. Keep the stages separate — a single keyframe list that
both grows and travels has to compromise its easing and the throw starts before
the eye has found the object. The pick-up is a CSS transition on an inner
`.fly-ghost__plate`, kicked off with `void ghost.offsetWidth` and **not** `rAF`,
which does not fire in a background tab. `opts.quick` is the tighter version
used for stepper repeats. The destination is clamped into the viewport, so a
click that lands before `[data-sticky-actions]` has stuck does not throw the
item off the top of the screen.
`badgeHold` freezes the *displayed* cart count while a ghost is in flight so
the number lands with the item — the store mutates immediately, only the paint
waits, so the two can never desync. Everything checks `reduceMotion()` first.
The shared interaction system (easing token, shadow tokens, `.btn-elevate`,
`.product-card__*`, `.tile-lift`, `.link-sweep`, `[data-reveal]`) is at the
foot of `styles.css` — **extend those rather than inventing per-component
hovers.**

`[data-reveal]` is applied to **every `<section>` on every page**, injected
centrally by `_with_reveal()` in `components.py` — not hand-placed per page, so
the entrance stays one decision. Sections that already carry the attribute are
skipped.

Its hidden state is gated behind `.js-reveal`, which JS adds to `<html>` at
runtime. Never move that into the markup: if JS fails, the page must degrade to
*unanimated*, not *invisible*. For the same reason `initReveal` carries a
**2.5s failsafe** that reveals anything still pending — `IntersectionObserver`
does **not** fire in a hidden or backgrounded document, and now that the reveal
covers the whole site, an observer that never reports would leave most of every
page faded out. Worst case is no animation, never no content. Don't remove it,
and don't replace it with rAF or a scroll listener — both are throttled in
exactly the case it exists to cover.

**When running the sweep, force-reveal first** (the snippet in `HANDOFF.md` §5
does this) or below-fold content is measured at opacity 0 and the run is
meaningless.

**Search** — the **only** runtime reader of `catalog.json`. `loadCatalog()`
fetches it once, lazily, on first modal open and caches the promise; a failed
fetch resolves to `null` and paints a message rather than hanging. `fold()`
normalises Arabic before matching (`ة`→`ه`, `ى`→`ي`, `أإآ`→`ا`, tashkeel
stripped) — without it `قهوه` returns nothing while `قهوة` returns six. All
terms must match (AND, not OR), prefix matches outrank buried ones, and
`popularityRank` breaks ties. Because it fetches, **search is the one feature
that does not work from `file://`** — everything else still does.

**i18n** — `t()` for chrome strings and `translateDocument()` for build-time
copy, both keyed off an `EN` dictionary of exact Arabic strings. Switching
language re-renders the injected chrome and walks text nodes, stashing originals
in a `WeakMap` so switching back is lossless. Exact-match only: a string with no
entry is deliberately left in Arabic rather than half-translated.

## Environment gotchas

These have each cost real time. Read them.

- **Python is 3.9.** f-strings reject backslashes inside the expression part.
- **Serve with `python3 build/serve.py`. One port, 8000, always.**
  Do **not** use `python3 -m http.server`: it sends no cache headers at all, so
  browsers hold `scripts.js` and `styles.css` hard and a refresh keeps showing
  the old file. Two "this is still wrong" reports in this project were exactly
  that. The old workaround was to bump the port on every check, which fixed the
  staleness but made the URL move constantly — Ahmed asked for it to stop, and
  it should: it was treating the symptom. `serve.py` sends
  `Cache-Control: no-store` on every response, so a **plain refresh on a fixed
  URL** always shows the current build. Verified: editing `styles.css` and
  reloading `http://localhost:8000` with no cache-buster picks the change up.
  It is rooted at `static-export/` no matter where it is invoked from, running
  it twice is a no-op, and it refuses to move to another port on its own.
- **`getComputedStyle` from the top-level document can be stale right after a
  viewport resize.** A no-media `!important` rule appeared to have no effect,
  which is impossible. **Screenshots and same-origin iframe measurements were
  both accurate.** If computed styles contradict a screenshot, distrust the
  computed style.
- **Tailwind only emits classes it can SEE as literal strings.** This replaced
  the Play CDN's quirks as the thing to watch. `tailwind.config.js` scans the
  generated HTML, `scripts.js` **and** `build/**/*.py`; drop any of the three
  and whole regions lose their styling (the chrome lives entirely in
  `scripts.js` template literals). **Never build a class by concatenation**
  (`"bg-" + name`) — it compiles to nothing, silently.
- **A class that isn't a real Tailwind utility compiles to nothing, silently.**
  `inset-inline-0` and `inset-inline-start-0` were used on the mega-menu for
  months; neither exists. The panel sat at its static position, 300px narrower
  than intended, and looked close enough in RTL to pass. The logical
  utilities are **`start-*` / `end-*`** (they emit `inset-inline-start/end`).
  If you are unsure a class is real, grep the built `tailwind.css` for it.
- **Nested colour keys with a hyphen** (e.g. `primary["on-dark"]`) produce no
  usable class — `text-primary-on-dark` is ambiguous between colour and shade.
  Accessibility tokens are deliberately flat: `onDarkGreen`, `onBlack`,
  `onBeigeMuted`.
- **A stale `xl:` variant note:** under the Play CDN some `xl:` variants did
  not apply, and a few rules were moved into `styles.css` under a media query
  with a winning selector (`a.chip-filter` beats `.bg-white`) to work around
  it. Those workarounds are harmless and still in place, but the underlying
  CDN bug is gone — don't add new ones on that reasoning without confirming
  the variant genuinely fails in the compiled CSS.
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
- **Never put a backtick inside an HTML comment in `scripts.js`.** Nearly all
  of that file's markup is in template literals, so a backtick in a comment
  **ends the string** and turns the rest into expressions. The header renders
  completely empty and nothing reaches the console, because it throws inside a
  function called during boot. `node --check` does not catch it — the result is
  still valid JavaScript. This cost two debugging rounds, so `build.py` now
  fails the build on it. Write `.mega-cat`, not the backticked form.
- **Icons are wrapper-driven.** Every glyph in `ICON` is `w-full h-full` +
  `currentColor`; the wrapper sets size and colour. Don't reintroduce a size
  class on the `<svg>` — it silently fights the wrapper.
- **Figma asset exports can be pre-transformed.** The logo exported upside-down
  and stretched (net vertical flip + `preserveAspectRatio="none"`). Several
  icons carry `preserveAspectRatio="none"` too. Check exported SVGs render.
- **`neutral.secondary` is for light surfaces only.** It inverts badly on black
  (3.29:1); use `onBlack` there.
- **`overflow-x-hidden` silently kills `position: sticky` in its subtree.**
  `hidden` on one axis forces the other to `auto`, which makes the element a
  scroll container — and a scroll container is what a sticky descendant sticks
  to, so it resolves against a box that never scrolls and simply does nothing.
  No error, no warning. `<main>` is **`overflow-x-clip`** for exactly this
  reason (see `page()` in components.py); `clip` clips identically without
  creating a scroll container. If a sticky element "does nothing", walk its
  ancestors for an overflow that is not `visible` or `clip` before touching the
  element itself.
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
- **Tap targets: 44px is the target, 24px is the floor.** The "≥44px, audited
  and passing" claim does **not** hold site-wide — see `HANDOFF.md` §11 and
  `DESIGN-NOTES.md` §7 for the surviving exceptions and why each was a layout
  decision rather than a size tweak. Treat WCAG 2.2 **2.5.8 (24×24, AA)** as
  the hard line and 2.5.5 (44px, AAA) as the goal. A control under 24px only
  passes if a 24px circle on its centre clears its neighbours', so for a row
  of small controls the rule binds **`size + gap >= 24`, not the gap alone** —
  which means you can spend that budget on either. The carousel dots pay it
  with a 14px dot and a 10px gap; paying it all out of the gap (10px dot, 14px
  gap) satisfied the checker and looked wrong, and was rejected. Never tighten
  such a gap without widening the control by the same amount.

## How to verify

```bash
npm install                               # once; Tailwind CLI (v3) for the CSS build
python3 build/build.py                    # 31 page(s) + 99 fanned-out, no missing assets,
                                          # and rebuilds static-export/tailwind.css
node --check static-export/scripts.js
grep -ril 'koueider\|kouider' static-export/   # must return nothing
git status --porcelain                    # rebuild must produce no diff
python3 build/serve.py                    # http://localhost:8000, always
```

Then in the browser run the **sweep** in `HANDOFF.md` §5 — it loads all 31 pages
in a same-origin iframe at 320/360/375/390/414 and reports horizontal overflow
plus WCAG contrast. Current baseline: **31/31 clean at every width, ~7600 text
nodes checked, 0 contrast failures.** The sweep's page list is the 31 core
pages; the 99 generated product pages share one layout, so sweep a
representative sample rather than all of them (multi-size + gallery, e.g.
`product-1322`; single-image + no client copy, e.g. `product-1631`).

**Seed the cart before you quote that number.** An earlier "31/31 clean" was
measured against an emptied cart, so no cart line ever rendered and a 13px
overflow at 320 went unnoticed. `localStorage.removeItem("abuauf:cart")` before
sweeping re-seeds it. Seed **several products, some at a two-digit quantity** —
card steppers only render for products that are in the cart, and the two-digit
case is the one that overflows.

The sweep distinguishes real overflow from intentional `line-clamp`/ellipsis
truncation. If you quote a number, know which you're quoting.

## Accessibility baseline

Passes **WCAG 2.1 AA** (4.5:1 body, 3:1 large) across all 31 pages, verified
against computed styles. Don't regress it; re-run the sweep after any colour
change, and read the tap-target note under "Layout constants" before changing
a control's size or spacing.

**The sweep's contrast pass is scoped to `main`.** This was originally a
workaround for the Play CDN not styling injected chrome inside an offscreen
iframe (110 false dark-on-dark failures once). The CDN is gone and the chrome
is styled from a real stylesheet now, so that specific cause is fixed — but
keep the scoping: the chrome is identical on all 130 pages, so measuring it
130 times only adds noise. Verify chrome colours once, in a real page.

Every page carries a skip link to `#main`, and the focus ring is global but
lives on a **zero-specificity `:where(...)`** selector — any Tailwind
`outline-none` beats it and must re-arm the ring on a selector that outranks a
single utility class (`styles.css` does this for three controls already).

## Data

- `static-export/data/catalog.json` — 99 products (`nameAr` + English `name`,
  `categorySlug`, price/sale, `images`, `popularityRank`, `sizes`, and the
  client's own Arabic copy in `descAr`/`descHtmlAr`), 12 categories
- `static-export/data/branches.json` — a list of **25 governorates**, each
  holding its own `branches` array; 316 branches in total. `len()` on the outer
  list gives 25, not 316 — use `catalog.BRANCH_COUNT`, which sums the inner
  ones. **Every `phone` field is empty** and there are no coordinates.

`images` is the product's real gallery, main shot first, and `popularityRank`
is its real position in the client's 653-product store (1 = best selling).
Both are fetched, never authored — the product page's gallery, best-seller
badge and social-proof line all key off them, so a product loses its badge when
the client's sales say it should. A missing `popularityRank` means "not a best
seller"; a one-entry `images` means the client has only shot the product once,
and `product_gallery()` drops the thumbnail strip rather than render a
one-item carousel.

`sizes` is the real answer to "what weights is this sold in, and for how
much". **Abu Auf do not use product variations** — the Store API returns
`type: "simple"`, `variations: []`, `attributes: []`, `weight: ""` for
everything. Each size is a separate SKU with the weight in its name, so
`fetch_sizes.py` recovers them by grouping the store on the name with the size
suffix stripped. 41 base products across their store are sold in more than one
size; 10 of our 99. Each entry carries that SKU's own `price` and `id`, and
`size_chips()` renders nothing below two sizes rather than imply a choice that
does not exist.

Scrapers: `build/scrape_assets.py`, `build/fetch_arabic_names.py`,
`build/fill_missing_names.py`, `build/fetch_galleries.py`,
`build/fetch_popularity.py`, `build/fetch_sizes.py`,
`build/fetch_descriptions.py`.

`descAr`/`descHtmlAr` are the client's own Arabic `short_description` and
benefits `description` HTML, pulled by `fetch_descriptions.py` from the
product detail pages' flight payload (the Store API truncates them, and only
in English). 97 of 99 products have them; the two that don't (62393, 1631)
render without a description — same rule as the branch phones, absence over
invention. The per-product pages key off these.

**`fetch_galleries.py` compares images by content, not by URL.** Every product's
API image list starts with the same photograph twice — a 600px `-thumb` and a
1400px `-gal` — so taking the list at face value gives every gallery two
identical opening thumbnails. Re-encodes measure 0.2–3.5 mean levels apart,
genuinely different photographs 140–190, and the threshold sits between them.
It writes into `products/gallery/`, deliberately a subdirectory:
`isolate_products.py` uses a non-recursive `listdir`, so lifestyle shots never
reach the white-background flood fill — their backgrounds are the photograph.

**`build/isolate_products.py`** cuts the white studio background out of the
product photos (border-connected flood fill, so white *inside* packaging
survives). Idempotent — it skips anything that already has alpha. **Run it
after any re-scrape**, or the new files will draw white rectangles inside the
`#EDEFEB` card plate.

Abu Auf's public routes are `/ar/category/<slug>` and `/ar/products/<slug>` —
**not** `/product-category/...`, which 404s. Product names are English in the
WooCommerce Store API under every locale hint; the Arabic ones are
server-rendered into the storefront's Next.js flight payload.

## Before launch

See `DESIGN-NOTES.md`. **Blocking:** the three legal pages are in-house
placeholder and must be replaced with the client's legal copy. Also outstanding:
branch phone numbers, and sign-off on every in-house English and Arabic string.
(Sale prices are **no longer** outstanding — `regular`/`sale`/`onSale` are real
API fields and 6 of 99 products carry a genuine discount. See DESIGN-NOTES §1.)

### Deploying to GitHub Pages

Checked and clean: no root-absolute paths (so a `/repo/` subpath works), no
case-mismatched asset references (Pages is case-sensitive, macOS is not), no
underscore-prefixed files, and `static-export/.nojekyll` is present so Pages
serves the directory as-is. Publish **`static-export/`** as the site root, not
the repo root. Every asset reference resolves — 436 checked, 0 missing.

**The Play CDN is gone (2026-07-22).** Tailwind is now compiled at build time
by the CLI into `static-export/tailwind.css` — one 30KB cacheable file instead
of ~120KB of JavaScript that had to scan the DOM and generate the stylesheet on
every visit. `python3 build/build.py` runs the CSS build as its last step and
**fails the build** if it cannot, so the stylesheet can never go stale against
the markup. Config is `tailwind.config.js` at the repo root; `tw-config.js` is
deleted. `npm install` once, then the normal build command is all you need.

Also still true at deploy time: the reviews and the `4.8 (126 تقييم)` rating on
the product page are invented placeholder (DESIGN-NOTES §1), the checkout CTA
does not validate its own form (§3), and `SITE_ORIGIN` is empty so canonical
and `og:url` are not emitted (§3).
