# Abu Auf rebuild — design & accessibility notes

The register of **every deviation, placeholder and open question** in this build.
`CLAUDE.md` is the operating brief; `HANDOFF.md` is the history and rationale.

Organised by what you need it for, not by when it was written:

1. [Blocked on client data](#1-blocked-on-client-data) — cannot be done honestly without them
2. [Placeholder copy needing sign-off](#2-placeholder-copy-needing-sign-off)
3. [Deliberate deviations from the Figma](#3-deliberate-deviations-from-the-figma)
4. [Where the live site beat the Figma](#4-where-the-live-site-beat-the-figma)
5. [Canonical Figma frames](#5-canonical-figma-frames)
6. [Open questions for the designer](#6-open-questions-for-the-designer)
7. [Colour contrast](#7-colour-contrast)
8. [Technical traps](#8-technical-traps)
9. [Resolved](#9-resolved)

---

## 1. Blocked on client data

**These are not oversights. Each was left missing rather than invented.**

### Branch phone numbers and directions — `branches.html`

The Figma (`426:33692`) shows a phone row and an `اتجاهات` link on every branch
card. `branches.json` has a `phone` field on all **316** branches and **every
single one is empty**; there are no coordinates either.

Inventing numbers for real retail locations would send customers to wrong
numbers. A store locator that lies is worse than one missing a row. The card
badges (`فرع أبو عوف`, `متاح توصيل`) are absent for the same reason — no field
distinguishes branch type or delivery availability.

**Needs:** the client to populate the CMS.

### Product compare-at price — `product.html`

The Figma shows a struck-through original beside a discounted price.
`catalog.json` carries one price per product with no compare-at field. Showing a
fake "was" price is fabricating a discount.

**Needs:** real sale prices in the catalogue, or sign-off on the single-price
treatment.

### Sub-category filtering — `shop-category.html`

The seven sub-category chips do not filter, deliberately. `catalog.json` has
`category`/`categorySlug` and **no sub-category field**, and the labels come from
the Figma rather than the data. Checked against the 12 real coffee products:
`القهوة`, `قهوة مطحونة طازجة`, `إسبريسو` and `مشروبات ساخنة` match **zero**
products each. Wiring them would empty the grid on four of seven taps.

**Needs:** the client's sub-category taxonomy.

### Sort options that aren't what their label claims

| Option | Reality |
|---|---|
| `السعر: من الأقل` / `من الأعلى` | **real** — sorts on the price field |
| `وصل حديثاً` | sorts by product **id** descending. Ids rise over time so it approximates recency, but there is **no publish date** in the catalogue |
| `الأكثر مبيعاً` | **does nothing** — restores catalogue order. There is no sales data anywhere in the scrape |

The `الاكثر مبيعا` rail in the products mega-panel is four real catalogue items,
hard-coded, for the same reason — plus `scripts.js` has no runtime access to
`catalog.json` by design.

**Needs:** `date_created` and a sales/popularity figure in the scrape.

### Two navbar items lead nowhere

`المكافآت` and `منتجات أبو عوف خارج مصر` fall through to `index.html` because
`/rewards` and `/export` were never built. The Figma has frames for both
(`973:40830`, `426:29955`).

---

## 2. Placeholder copy needing sign-off

Everything below is written in-house in Abu Auf's voice. It is plausible and
on-brand, and it is **not** the client's approved copy.

| Where | Status |
|---|---|
| **Legal pages** (privacy, terms, return policy) | Written in-house. **Must be replaced with the client's legal text — do not launch on these.** |
| FAQs (`build/pages/faqs.py`) | 9 Q&As. Delivery times, 100 EGP minimum order and the 14-day return window are **assumptions** |
| Blog & recipes (`build/pages/_posts.py`) | 6 posts; the live blog is client-rendered so its Arabic copy is not scrapable |
| Home page reviews | 4 invented testimonials with invented names. Real reviews exist at `apis/v2/get-all` |
| Account pages | Sample customer "محمد عادل", order numbers and wallet balances are illustrative |
| **All English strings** in the `EN` dictionary in `scripts.js` | Standard commerce terminology written in-house — `Offers & Discounts`, `Checkout`, `View cart`. Not the client's wording. **Product names are the one exception** — those are real catalogue data |

### Cart figures disagree with the live site

The build uses `DELIVERY_FEE = 10` and `MIN_ORDER = 100`, mirrored between
`build/pages/cart.py` and the drawer in `scripts.js` so the two surfaces can
never quote different numbers.

**The live site shows a 30 EGP delivery fee and a shortfall implying a 150 EGP
minimum.** Ours are assumptions. Confirm the real figures and change them in
both places — it also affects checkout and thank-you.

The below-minimum state (disabled checkout + shortfall warning) is implemented
but not visible in the demo, since the seeded cart exceeds the minimum.

### Other content gaps

- **`صحارة ديلايتس` promo section** (Figma `753:34833`) omitted pending assets.
- **Branch titles are English.** `ar_title` is blank for every branch in the
  client's CMS, so `branches.html` shows the English name with the Arabic
  address. Presented as-is rather than machine-translated.
- **HQ address differs** between the Figma footer and the live site. The build
  uses the Figma's. Worth confirming which is current.

---

## 3. Deliberate deviations from the Figma

### Contrast — sanctioned by Ahmed

See §7. The build intentionally diverges from the Figma to pass WCAG AA. **The
designer should be told**, because the Figma is still the failing version.

### Account menu sheet lists seven rows; the Figma draws six

The Figma omits `نقاطي`, but `my-account-point.html` exists and is linked from
the desktop sidebar. Both the sidebar and the sheet render from one `NAV` list,
so dropping it from the sheet would mean maintaining a second divergent list.
**Ask whether `نقاطي` is being retired** — and if so remove the page, not just
the row.

### `تأكيد` closes the account sheet rather than confirming a selection

In the Figma the rows look selectable with `تأكيد` committing the choice. Here
each row is a plain link that navigates on tap, which is standard and keeps the
sheet keyboard- and screen-reader-navigable. `تأكيد` is retained for visual
fidelity but is a dismiss.

### Checkout summary is not collapsible

The Figma mobile frame shows a chevron on `ملخص السلة`. The build renders it
expanded with a `تعديل` link. Left as-is at Ahmed's direction — on a checkout
page, putting the order total behind a tap is a conversion decision, not a
styling one.

### Language toggle exists at all

`HANDOFF.md` §2 records **"Arabic-first, not bilingual"** as a client decision.
The toggle is a direction/UI test harness, not a reversal. See `HANDOFF.md` §6
for exactly what it does and doesn't translate.

---

## 4. Where the live site beat the Figma

Ahmed supplied live screenshots and asked for parity with abuauf.com. Where the
live site and the Figma disagree on chrome, **the live site wins**. All values
below were measured in the browser on abuauf.com at 1920, not eyeballed.

### Layout constants

| | Live | Ours |
|---|---|---|
| Content container | 1536px, bars full-bleed behind | 1536px |
| Utility bar / masthead / nav | 33 / 79 / 48 (total 161) | 33 / 79 / 48 (160) |
| Footer (CTA + main + legal) | 306 / 390 / 68 (total 764) | 305 / 462 (767) |
| Cart & search buttons | 48×48 both | 48×48 both |

Before this, containers were `max-w-[1920px]` with `xl:px-[190px]` — near-right
at 1920 but a 1060px column at 1440 against the live site's ~1408 — and the
masthead and nav had no max-width at all, running to 1745px.

### Masthead is one pill, not three

This is why our header read heavier even at the correct height.

| Control | Live |
|---|---|
| `المنتجات` | **18px / 500**, filled pill, h48, padding 8/16, gap 12 |
| Delivery | **13px / 400**, plain link, **no pill** |
| `تسجيل الدخول` / `الحساب` | **13px / 400**, plain link, **no pill** |

### Chrome typography

| Element | Live |
|---|---|
| Nav row links | 16px / 600 |
| Footer column links | 16px / 400 |
| Footer column headings | 16px / 700 |
| Utility bar links | 13px / 600 |
| Footer logo | 180×46 |
| Hotline | 36px / 700 |
| CTA subtitle / input / button | 20/600, 16/400, 16/700 |

The newsletter field also has a mail glyph the build was missing.

### Nav hover, lifted from their stylesheet

Read out of `8939158812c59106.css` rather than approximated:

```css
.hoverFromCenter:after { border-bottom: 4px solid #dcc498; transform: scaleX(0);
                         transition: transform .25s ease-in-out; }
.active:after, .hoverFromCenter:hover:after { transform: scaleX(1); }
```

Our nav already had a `#DCC498` bar but faded it with **opacity**. It now scales
from centre on the same curve. Note Tailwind's `ease-in-out` is
`cubic-bezier(0.4,0,0.2,1)` while CSS `ease-in-out` is `(0.42,0,0.58,1)` — the
build uses the arbitrary value so the easing matches exactly.

### Products dropdown, cart drawer, location picker

- **`المنتجات` opens a three-column dropdown on desktop** (categories →
  sub-categories → product rail), not the mobile side drawer it used to open at
  every width. Switches on hover *and* focus; closes on outside click or Escape.
  Phones keep the drawer (`hidden lg:block`).
- **Cart drawer** rebuilt to match: price chip per line, `العدد`, 44px stepper,
  `حذف`, `قد يعجبك أيضا` upsell, delivery line, split
  `عرض السلة` / `اتمام الشراء` footer.
- **Location picker** is a bottom sheet on phones and a centred 420px dialog
  from `xl` — the live site opens a popup there. Centring uses `inset-inline` +
  `margin-inline`, not `left`/`right`, so it holds in RTL.

---

## 5. Canonical Figma frames

The `Mobile` page has duplicate frames with nothing marking which is current.
Ahmed's rule: **use the most built-out and record the choice.** Entries marked
*inferred* are completeness judgements, not designer confirmation.

| Route | Chosen | Passed over | Basis |
|---|---|---|---|
| Home | `2595:60104` | `753:30987` | **Confirmed by Ahmed** (both 12361.52px, so completeness couldn't decide) |
| Collection | `350:17805` | 3 others, two identical at 2593px | **Confirmed by Ahmed** |
| Product | `918:34326` (4723px) | `350:25883` (4038px) | *inferred* — 685px more content, includes the FBT block |
| Cart | `804:32907` (3007px) | `359:18661` (2786px) | *inferred* — 221px more content |
| Checkout > Info | `753:36339` (2554px) | `753:34950` (2242px) | *inferred* |

Other frames used: `Account > Overview` `383:33392`, `Account > menu bottom
sheet` `973:47270`, auth `368:21314`, branches `426:33692`.

Still unresolved: `Account > Wallet` has three frames, none yet built against.

---

## 6. Open questions for the designer

1. Is `نقاطي` being retired? (§3)
2. Was select-then-confirm intended for the account sheet, or tap-to-navigate? (§3)
3. Should the checkout summary collapse on mobile? (§3)
4. The Figma still contains the contrast failures the build diverges from. (§7)
5. The live site differs from the Figma on chrome sizing, the masthead pills and
   the location picker. Which is authoritative going forward? (§4)
6. Confirm the inferred canonical frames. (§5)
7. Which HQ address is current? (§2)

---

## 7. Colour contrast

**The build passes WCAG 2.1 AA everywhere** (4.5:1 body, 3:1 large). Achieving
that required deviating from the Figma. Verified live against computed styles —
currently **0 failures across all 29 pages, ~4300 text nodes**.

| Where | Figma | Ratio | Now | Ratio |
|-------|-------|-------|-----|-------|
| Footer column headings + HQ address | `#185039` on `#062B1C` | **1.64:1** | `onDarkGreen #7FA894` | 5.79:1 |
| Secondary text everywhere (546 uses) | `#777777` | 4.48 / 3.87 / 3.39 | `neutral.secondary #5F5F5F` | 6.39 / 5.52 / 4.83 |
| Legal-bar text on black | — | — | `onBlack #949494` | 6.92:1 |
| Newsletter placeholder on beige | `#ABA08F` | **1.95:1** | `onBeigeMuted #6B6255` | 4.54:1 |
| Utility-bar links on beige | `text-white` (bug) | **1.32:1** | `#5F5035` | 5.92:1 |
| Tab buttons | `#777777` | 4.48:1 | `#5F5F5F` | 6.39:1 |
| Mobile drawer links | `#868685` / `#bbbbbb` | 3.64 / 1.92 | `neutral.secondary` | 6.39:1 |
| Breadcrumb `/` separators | `#C6C6C6` | 1.71:1 | `aria-hidden` + `neutral.outline` | decorative |

Two of those were **my own bugs**, not the Figma's: the utility-bar links kept
`text-white` after I recoloured the bar beige (invisible text), and `.tab-btn`
hardcoded `#777777` instead of the token.

**Tap targets** are separately audited at ≥44px (WCAG 2.5.5). Before that pass
the hamburger was 32×30, the location bar 38px, filter chips 38px, and 10 of 18
mobile-drawer items under 44.

---

## 8. Technical traps

### `neutral.secondary` is for light surfaces only

It inverts badly on black (3.29:1) — that is why `onBlack` exists. Don't reuse
`text-neutral-secondary` on dark backgrounds.

### Tailwind Play CDN — nested colour keys

A key containing a hyphen (e.g. `primary["on-dark"]`) produces **no usable
class**; `text-primary-on-dark` is ambiguous between colour and shade and
silently falls back to the inherited colour. This cost a debugging cycle where
the ratios were right on paper while the browser painted the old colour.
Accessibility tokens are therefore **flat**: `onDarkGreen`, `onBlack`,
`onBeigeMuted`.

### Tailwind Play CDN — `xl:` variants that never apply

On the filter chips the CDN did not apply `xl:` variants at all: an identical
probe element created at runtime resolved to white at 1440 while the real chips
stayed filled. Where this bites, author the rule in `styles.css` under a media
query with a selector that wins on specificity — `a.chip-filter` (0,1,1) beats
Tailwind's `.bg-white` (0,1,0) regardless of emit order.

### The `hidden` attribute loses to any author `display` rule

`hidden` only sets `display:none` via the UA stylesheet, so an element carrying
both `hidden` and Tailwind's `.flex` stays visible — all eight mega-menu
sub-lists rendered stacked at once. `styles.css` now carries
`[hidden] { display: none !important; }`. Anything toggling `hidden` on a
flex/grid element depends on that rule.

### `min-w-0`, and grids with no base column rule

The most common bug class here. A `flex-1` child has `min-width: auto` and
cannot shrink below its content, so it pushes its parent wider; a top-level
`overflow-x-hidden` then hides the overhang and page scroll reads 0, so nothing
looks wrong. Likewise `lg:grid-cols-[Npx_1fr]` **with no base rule** collapses
below `lg` to a single max-content column — this hit the account shell, cart,
thank-you and the product FBT block. Grep for both patterns when adding a
two-column layout.

### Figma exports can be pre-transformed

The logo exports upside-down and stretched: its wrapper carries
`-rotate-180 -scale-x-100` (a net vertical flip) plus
`preserveAspectRatio="none"`. The flip is baked into
`images/abuauf/brand/logo-abuauf-white.svg`. Several icons also carry
`preserveAspectRatio="none"` — `icon-grid.svg` does, though its viewBox is
near-square so distortion there is under 0.01%.

### The footer payment strip

The first mark is **Etisalat Cash**, not Meeza, and ships as white artwork on an
opaque black plate — it must not be placed on a white chip.

### Verify on a fresh port, and trust screenshots over computed styles

`python3 -m http.server` sends no cache headers and browsers hold `scripts.js`
and `styles.css` hard. **Two separate "this is still wrong" reports in this
project were a stale port, not a bug.** Bump the port every time, and confirm
what the server is rooted at.

Separately: `getComputedStyle` read from the top-level document **right after a
viewport resize returned stale values** — a no-media `!important` rule appeared
to have no effect, which is impossible. Screenshots and same-origin iframe
measurements were both accurate. **If a computed style contradicts a screenshot,
distrust the computed style.**

### The cart renderer is a keyed reconcile on purpose

`renderCart()` updates rows in place rather than replacing the list with
`innerHTML`. Wholesale replacement destroys nodes mid-transition and drops
focus, which makes row-level micro-interactions impossible. Don't "simplify" it.
One consequence: `remove()` detaches the node in the same render, so exit
animations should animate first and call `remove()` on completion.

---

## 9. Resolved

- **Arabic product names — solved.** The WooCommerce Store API only ever returns
  English names (`?lang=ar`, `Accept-Language: ar` and `X-WPML-Language: ar` all
  return English). But the Arabic storefront *server-renders* names into its
  Next.js RSC flight payload at `https://www.abuauf.com/ar/category/<slug>`,
  keyed by the same product slug the Store API returns. Category routes only
  render their first page, so the remainder were fetched per product from
  `/ar/products/<slug>`. Coverage is **99/99**, stored as `nameAr` in
  `catalog.json`. Scripts: `fetch_arabic_names.py`, `fill_missing_names.py`.
  The public routes are `/ar/category/<slug>` and `/ar/products/<slug>` —
  **not** `/product-category/…`, which 404s.

- **Filters and nav routes now work over real data.** Every `/shop/<slug>` used
  to resolve to `shop-category.html`, which shows coffee — tapping `المكسرات`
  showed coffee. Category chips now filter client-side over the cards already in
  the DOM (no fetch, still works from `file://`), verified: all 9 chips return
  only their own category with counts matching `catalog.json` exactly
  (12/8/12/12/8/12/8/11). Nav destinations went from 1 to 14.

- **The cart is real state.** `[data-add-to-cart]` previously had no handler at
  all. See `CLAUDE.md` for the `window.abuaufCart` API and the `cart:change`
  event contract.

- **The Figma footer carries a "Web Design by MITCH DESIGNS" credit.** Retained
  at the client's request — do not remove it again.
