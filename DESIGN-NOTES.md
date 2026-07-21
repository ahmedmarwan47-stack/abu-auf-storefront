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

### Product reviews — the client's endpoint is test data, not reviews

`HANDOFF.md` used to list "real reviews at `apis/v2/get-all`" as ready-to-build.
**It isn't.** The endpoint returns HTTP 200 and exactly **10 rows**, and every
one of them is:

| Field | Value across all 10 |
|---|---|
| `comment_author` | `John` |
| `comment_content` | `comment` |
| `rating` | `5` |
| `comment_date` | all on 2024-09-17, within 11 minutes |

That is a QA smoke test someone left in the database, not customer feedback.
Swapping the four invented Arabic testimonials for ten identical
`John / "comment" / 5★` rows would be **worse** than the placeholder: it would
put visibly fake reviews on the storefront and read as broken.

So the invented testimonials stay, still flagged as placeholder. Do not "fix"
this by wiring the endpoint.

**Needs:** the client to collect real reviews, or sign-off on dropping the
section.

### Rewards body copy — the client's own page is lorem ipsum

`rewards.html` now exists (the nav used to fall through to `index.html`), but it
is deliberately thin. **The live abuauf.com/rewards is itself unfinished:** its
H1 is real, its body is Arabic lorem ipsum
(`لوريم سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت...`). There was no real copy
to scrape.

What is on our page is real — the live H1 and hero image — plus links to the
account points and wallet pages that already exist. No rewards programme was
invented. Contrast `export.html`, which is built entirely from the client's real
copy scraped off `/export`.

**Needs:** the client to write their rewards copy.

---

### Demo sign-in — must be removed before launch

`login.html` prints a working demo credential pair
(`demo@abuauf.com` / `AbuAuf2026`) and `scripts.js` carries a `window.abuaufAuth`
store that checks it **in client-side JavaScript**. It exists so the signed-in
chrome and the favourites flow can be walked end to end in a static export with
no backend.

**This is not authentication.** The credentials are hard-coded and readable by
anyone who opens the file — printing them on the page gives away nothing that
was not already public. It is a fixture, and it must be replaced wholesale by
the real backend session before launch, along with the callout block in
`build/pages/login.py` (`DEMO_EMAIL` / `DEMO_PASSWORD`) and the `[data-logout]`
control in the account sidebar.

Signed-in state drives `[data-account-link]` / `[data-account-label]` in the
masthead and `[data-authed-only]` / `[data-anon-only]` anywhere; wiring a real
session to the same attributes keeps the chrome working.

## 2. Placeholder copy needing sign-off

Everything below is written in-house in Abu Auf's voice. It is plausible and
on-brand, and it is **not** the client's approved copy.

| Where | Status |
|---|---|
| **Legal pages** (privacy, terms, return policy) | Written in-house. **Must be replaced with the client's legal text — do not launch on these.** |
| FAQs (`build/pages/faqs.py`) | 9 Q&As. Delivery times and the 14-day return window are **assumptions**. The minimum order now reads 150 EGP, matching the live site and the cart constants |
| Blog & recipes (`build/pages/_posts.py`) | 6 posts; the live blog is client-rendered so its Arabic copy is not scrapable |
| Home page reviews | 4 invented testimonials with invented names. **There is no real substitute** — see below |
| Account pages | Sample customer "محمد عادل", order numbers and wallet balances are illustrative |
| **All English strings** in the `EN` dictionary in `scripts.js` | Standard commerce terminology written in-house — `Offers & Discounts`, `Checkout`, `View cart`. Not the client's wording. **Product names are the one exception** — those are real catalogue data |

### Cart figures — now matching the live site

The build uses `DELIVERY_FEE = 30` and `MIN_ORDER = 150`, mirrored between
`build/pages/cart.py` and the drawer in `scripts.js` so the two surfaces can
never quote different numbers.

These were `10` / `100` until the live site was checked — it shows a **30 EGP
delivery fee** and a shortfall implying a **150 EGP minimum**, so both were
corrected across `cart.py`, `checkout.py`, `thank_you.py`,
`my_account_order.py` and `scripts.js`. Still worth confirming with the client,
since 150 is inferred from a 40 EGP cart showing 110 remaining rather than
stated anywhere.

The below-minimum state (disabled checkout + shortfall warning) is implemented
but not visible in the demo, since the seeded cart exceeds the minimum.

### Mobile masthead: live has a store icon we cannot replicate

At 390 the live masthead runs `cart · search · [logo] · store · hamburger`,
with the store and hamburger grouped in a white pill. Ours now matches except
for the **store/branches icon** — no such glyph exists anywhere in the project
(`ICON` carries account, search, location, menu, close, chevronDown, cart,
arrowRight, arrowLeft, phone) and the live site renders its icons inline, so
there was nothing to scrape. **Left out rather than invented.** The search
button is new: mobile previously had no way to search at all.

Live packs those controls at 36×36; ours stay 44×44 for WCAG 2.5.5, the
standing accessibility deviation.

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
| Masthead logo | **120×31** (aspect 3.91) | 120×31 |

### The header was 64px narrower than the page, on every page

The three header bands were wrapped in `px-4 xl:px-20`, with `max-w-[1536px]`
on the *inner* container. Because the 80px was subtracted **before** the cap
applied, the cap never bound: at a 1440 viewport the logo's outer edge landed
at 1345 while page content and the footer ran to 1409. Measured at **exactly
64px on all 31 pages**.

On the live site that offset is **zero** — the logo's outer edge sits precisely
on the content container edge. Fixed by moving the inline padding off the
full-bleed background element and onto the inner `mx-auto px-4 max-w-[1536px]`
container, which is the same container the rest of the site uses. The
mega-panel's cap came down from 1600 to 1536 at the same time, since it hangs
off a now-full-bleed parent and would otherwise have been 64px wider than the
nav above it.

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
currently **0 failures across all 31 pages, ~5000 text nodes** (the count rose
from ~4500 when the favourites page went from 6 cards to the full catalogue).

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

**Tap targets** were audited at ≥44px (WCAG 2.5.5). Before that pass the
hamburger was 32×30, the location bar 38px, filter chips 38px, and 10 of 18
mobile-drawer items under 44.

### That tap-target claim is no longer accurate — open issue

A fresh measurement of `cart.html` at 390 found **58 controls under 44×44**.
Most are inline text links inside a block of text, which WCAG 2.5.5 explicitly
exempts, but several are discrete controls that are not exempt:

| Control | Size | Where |
|---|---|---|
| Stepper `−` / `+` | **32×32** | every cart line, drawer and cart page |
| `حذف` remove | **24 wide** (44 tall) | every cart line |
| `خصم المبلغ` apply promo | 89×**34** | cart page |
| `أضف` | 76×**36** | cart page |

Left as-is deliberately: enlarging the stepper to 44px pushes the row back over
its 320px budget (44+16+44+8+16+2 = 130, plus `حذف` and the gap = 162 against
141 available), so it needs a layout decision — wrap the row, or move `حذف` —
not a size tweak. **Flagged rather than silently redesigned.** Re-audit the
whole site's tap targets before trusting the "≥44px, audited and passing"
claim elsewhere.

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

- **Favourites are real state.** The heart on the product card was inert markup
  — **184 buttons across 7 pages with no handler anywhere in `scripts.js`**.
  There is now a `window.abuaufFavs` store built to the same contract as the
  cart (localStorage `abuauf:favs`, `favs:change` event, no fetch), and
  `my-account-favorites.html` renders from it instead of hard-coding six
  products. Saved state is carried by `aria-pressed` alone so the accessible
  state and the painted state cannot drift; `styles.css` swaps the glyph off
  that selector. The page ships the whole catalogue hidden and reveals what is
  saved — the same "filter what is already rendered" approach the listing chips
  use, which keeps card markup in `components.py` alone. The six products the
  page used to hard-code are now `FAVS_SEED`, so a fresh browser sees the same
  design. Verified: 6 seeded → toggle off → 5, persists across pages, empty
  state at 0, hearts 44×44, 31/31 sweep still clean.

- **Two dead "اضف" buttons in the cart drawer.** The upsell rows carried
  `data-add-to-cart` but had no `[data-product]` ancestor, so `productFrom()`
  returned `null` and the handler returned silently — the buttons did nothing
  at all. Same class as the dead nav routes. Both rows are now `[data-product]`
  hosts with real catalogue ids.

- **A fabricated product was on display in the cart drawer.** The first upsell
  row was `مارشميلو بطيخ - 60 جرام` at EGP 30 — it matches **no product in
  `catalog.json`** and was illustrated with the photograph of a *different*
  real product (`قراصيا بدون نواه`, id 1445). Replaced with a real catalogue
  item at the same price (`كرانبيري - 25 جم`, id 1631) so the layout is
  unchanged. The code comment above it claimed "real catalogue items", which
  was true of the second row only.

- **`CART_SEED` used barcodes as product ids.** The two seeded lines were keyed
  `"6223006310759"` and `"2000102000000"` — barcodes lifted off the image
  filenames, matching no product card's `data-id`. Because `Cart.add()` dedupes
  on id, adding either seeded product **from its own card created a second line
  for the same product** instead of incrementing the first. Reproduced in the
  browser, then fixed to the real catalogue ids `1431` / `1445` and re-verified
  (qty 1 → 2, one line). **Any future seed must use catalogue ids.**

- **The brand logo was the wrong artwork.** `logo-abuauf-white.svg` was five
  paths all filled white — **the green leaf was missing entirely** — and it was
  drawn at 180×60 (aspect 3.0) against the real mark's 3.91, so it was both
  oversized and the wrong shape. Replaced with the client's own asset,
  `abuauf.com/images/logo_white.webp` (524×134), which carries the leaf in
  **#4AA948** (sampled from the file). Now 120×31 in the masthead, matching
  live exactly. The mobile masthead and drawer had also inherited the stretched
  3.0 box (132×44, 110×36) and are now 132×34 and 110×28; the footer's 180×46
  was already the correct aspect and only needed the asset swapped.

- **`icon-leaf.svg` did not exist.** All 8 mega-panel category bullets were
  broken images on every page, and the reference carried
  `onerror="this.style.display='none'"` so they failed **silently** — the build's
  asset check never saw it because the reference lives in `scripts.js`, not in
  generated HTML. The icon is now drawn from the brand mark's own leaf in
  #4AA948, and the `onerror` swallow is gone so the next missing asset is
  visible. **The leaf icon is in-house artwork** derived from the client's logo;
  it is not a Figma export and should be replaced if the designer supplies one.

- **The language switch only ever applied to the page you clicked on.**
  `translateDocument()` was called from `repaintForLang()` alone, which runs on
  the toggle click — **never on page load**. So navigating with English stored
  gave you English chrome (rendered through `t()` at render time) over entirely
  Arabic page copy. Measured coverage in English mode was **17–43% of visible
  text nodes, ~26% average**. Split out as `applyLangToContent()` and called on
  boot as well; coverage is now **59–95%, ~75% average**. The remainder is
  genuine prose with no English source (FAQ answers, About copy, blog posts)
  plus Arabic-only branch names and addresses.

- **Listing filter chips now translate**, using the catalogue's own English
  category names copied verbatim from `catalog.json` — real client data, not
  translations written here.

- **The sticky nav never actually stuck.** `initStickyNav` added Tailwind's
  `fixed`, but the bar's base classes include `relative`; both are single-class
  selectors, so specificity ties and **source order decides** — Tailwind emits
  `.relative` after `.fixed`. The classes were being applied correctly all
  along, they just lost the cascade. Now driven by
  `[data-navbar][data-stuck="true"]` in `styles.css` (0,2,0 beats 0,1,0),
  positioned with `inset-inline` so it holds in RTL. **Same family as the
  `[hidden]` and `xl:` CDN traps** — when a utility silently loses, author the
  rule in `styles.css`.

- **Cart line rows overflowed 13px at 320.** Stepper (122) + `حذف` (24) + gap
  (8) came to 154 inside a 141px column. The documented "31/31 clean" baseline
  missed it because that sweep happened to run against an **emptied cart**, so
  no line ever rendered — worth remembering when quoting the sweep: seed the
  cart first.

- **Product photos are cut out, not sitting on a white tile.** 101 of 110 files
  arrived from the client's CDN as opaque photos on a white studio sweep, and
  the card plate is `bg-interaction-base` (#EDEFEB — the same value the live
  site uses), so each one drew a white rectangle inside the beige plate. The
  handful that shipped with an alpha channel looked right, which is what made
  it obvious. `build/isolate_products.py` flood-fills near-white **from the
  border only**, so white *enclosed* by product — packaging, labels,
  highlights — survives; a naive "all white becomes transparent" pass punches
  holes through bags. Edge pixels get an alpha ramp so there is no halo.
  Idempotent, and the originals are in git. 102 isolated, 7 already had alpha,
  1 was a lone raisin whose background is legitimately 95% of the frame (the
  runaway-fill guard sits at 98.5% for exactly that reason). **Re-run it after
  any re-scrape.**

- **Icon sizes are wrapper-driven now.** Every glyph in `ICON` is
  `w-full h-full` + `currentColor`, so the wrapper decides size and colour.
  They used to carry their own `w-4`/`w-5`/`w-6` and silently fight it: the
  masthead chevrons sat in a `w-6 h-6` span but drew at 16px, the breadcrumb
  arrows drew at 20px inside a 16px box and overflowed, and `menu` was
  hardcoded `width="31" height="30" stroke="white"` so it ignored both.
  Masthead chevrons are now a true 18px at stroke-width 2.4 against 16-18px
  labels.

- **The mega-menu caret eased instead of snapping.** It was flipped with an
  inline `style.transform`, which competed with the `transition-transform`
  utility. `.chevron` in `styles.css` owns the transition and the rotation,
  and every chevron on the site shares it.

- **Selected vs hovered are now distinguishable in the products panel.** Both
  painted the identical #EDEFEB, and because hovering a category also
  *activates* it, the whole column read as permanently hovered. Hover is a
  faint wash; selected is a tinted surface with a brand-green bar on the
  leading edge and a revealed arrow.

- **The Christmas tree is gone** — it was a seasonal badge on المكسرات
  (`nav-nuts-badge.png`, now deleted). **The discount glyph moved to the right
  of its label**, which in RTL means rendering it *before* the text.

- **A shared interaction system** lives at the end of `styles.css`: one easing
  token (`--ease-out`), two shadow tokens, and classes for card lift
  (`.product-card__*`), button press (`.btn-elevate`), tile shadow
  (`.tile-lift`) and link underline sweep (`.link-sweep`). Durations are
  120-350ms. All of it collapses under `prefers-reduced-motion: reduce`.
  Prefer extending these over inventing per-component hovers.

- **Fly-to-cart / fly-to-favourites.** This is what the `cart:change` and
  `favs:change` event APIs and the keyed reconcile were built for. `flyTo()`
  clones a bit of the page onto a fixed-position ghost and arcs it to a
  destination; add-to-cart sends the product image to the cart button,
  favouriting sends a filled heart to the account button. A ghost clone rather
  than moving the real node, because the card must stay put and keep working,
  and a fixed ghost is immune to whatever scroll container it started in.

  **The badge is held, the store is not.** `badgeHold` freezes the *displayed*
  count while a ghost is in flight so the number ticks up on landing rather
  than before the item has left. The mutation happens immediately, so state
  and display can never desync — only the paint lags, by ~720ms. Verified:
  mid-flight the store reads 3 while the badge still reads 2; on landing both
  read 3 and the ghost is removed. There is a 1400ms belt-and-braces timeout
  because a backgrounded tab may never fire `onfinish`, and a stranded ghost
  would sit over the page forever.

  Removal never flies — only additions. Under `prefers-reduced-motion` there
  is no ghost at all and the badge updates immediately.

- **The account button gained a favourites counter** (`[data-fav-count]`), so
  the heart has somewhere to land and "the number goes up" is true for
  favourites as well as the cart.

- **New cart glyph.** A solid shopping bag with a stroked handle, replacing a
  Figma-exported basket that carried `preserveAspectRatio="none"` and a
  hardcoded fill — so it neither inherited colour nor scaled honestly. Now
  inline (`ICON.cart`) rather than an `<img>`, so it inherits `currentColor`
  and is wrapper-sized like every other glyph. The cart buttons set
  `text-[#163300]` explicitly; without it the glyph inherited the body text
  colour rather than the brand green.

- **Scroll reveal** on the home and product page sections — the single biggest
  contributor to the site feeling current, and cheap: one IntersectionObserver,
  unobserved after firing. Anything already on screen at load is revealed
  *without* animation so the fold never animates in after the fact.

  **The hidden state is gated behind `.js-reveal`**, which `scripts.js` adds to
  `<html>` only once it runs. Without that gate a JS failure would leave every
  section stuck at `opacity: 0` — invisible content is a far worse failure than
  unanimated content. Verified: all 8 home sections reveal on a full scroll,
  none stranded, and nothing is ever invisible while on screen.

  **When sweeping, force-reveal first** — `d.querySelectorAll('[data-reveal]')
  .forEach(el => el.setAttribute('data-reveal','in'))` — or below-fold sections
  are measured at opacity 0. Doing this raised the checked-node count from
  ~4,500 to ~5,300.

- **`site/Abu-Auf-flags.webp` is cut out too.** It renders inside an
  `info_card`, whose surface is #EDEFEB, so its baked-in white drew the same
  box the product photos did. `isolate_products.py` now takes explicit paths
  for exactly this. **Do not run it on the hero banners or the export-page
  photos** — those are displayed on white, where a white background is correct
  and cutting it out only costs image quality.

- **The Figma footer carries a "Web Design by MITCH DESIGNS" credit.** Retained
  at the client's request — do not remove it again.
