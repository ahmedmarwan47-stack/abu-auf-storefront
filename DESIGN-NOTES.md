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

### Two gift baskets are indistinguishable in Arabic

Three products came out of the scrape with damaged names. `catalog.py` now
repairs what it can on load — `html.unescape` for the English side, which was
shipping literal `&#8220;` to the page in English mode, and stripping the
stray backslashes on the Arabic side:

| id | Arabic (was) | English |
|---|---|---|
| 1269 | `سلة هدايا \\` | Gift Basket "Small" |
| 1270 | `سلة هدايا \\` | Gift Basket "Medium" |
| 10549 | `لب سورى مقشر \\` | Raw Sunflower Seeds "Raw" – 450 g |

The backslashes are all that survived of a quoted size suffix in the
storefront's flight payload. So **1269 and 1270 are now both plain
`سلة هدايا`** — same name, same page title, adjacent in the shop grid, with
nothing to tell them apart but the price.

The English says Small and Medium. Writing `صغيرة`/`وسط` into the Arabic would
be **authoring product names for the client**, which is the line this project
does not cross — same rule as the branch phone numbers. Left identical and
flagged.

**Needs:** the client to confirm the real Arabic names, or a re-scrape that
recovers the suffix.

### ~~Product compare-at price~~ — RESOLVED, and the struck prices are real

This entry used to read "`catalog.json` carries one price per product with no
compare-at field". **That is out of date** — re-checked 2026-07-22. The
catalogue now carries `regular`, `sale` and `onSale` straight from the Store
API, and exactly **6 of 99** products are genuinely discounted (`regular` and
`price` differ on those 6 and no others).

So the struck-through `EGP 325 → EGP 250` on the listing grid is the client's
own pricing, not a fabricated discount, and a product loses the treatment the
moment the client's sale ends. Left here rather than deleted because the old
wording would otherwise lead a reader to assume the opposite.

### Sub-category filtering — `shop-category.html`

The sub-category chips now filter live (Ahmed, 2026-08-03). `catalog.json` still
has **no sub-category field** — every coffee SKU is just `categorySlug`
`coffee-beverage` — so the sub-category is **derived from the product's Arabic
name by keyword** in `shop_category.py::_subcat` (priority-ordered: تركي →
برازيلي → سريعة التحضير → إسبريسو → عرب → else fresh-ground). `product_card(cat=…)`
lets the page write that derived slug into each card's `data-cat`, which
`initListing` already filters on; making the chips live also turns the Sort
dropdown on (it shares `initListing`).

This is **derived, not real, data.** Chips that match zero products are dropped
so none reads as broken — with the 12-product sample that removes **إسبريسو**
(6 chips ship, not 7). Current split: fresh-ground 4, برازيلي 4, سريعة التحضير 2,
تركي 1, مشروبات ساخنة 1 (`قهوة عربى`).

**Needs:** the client's real sub-category taxonomy — then replace `_subcat` with
a lookup and restore the dropped chip(s).

### Sort options that aren't what their label claims

| Option | Reality |
|---|---|
| `السعر: من الأقل` / `من الأعلى` | **real** — sorts on the price field |
| `وصل حديثاً` | sorts by product **id** descending. Ids rise over time so it approximates recency, but there is **no publish date** in the catalogue |
| `الأكثر مبيعاً` | **does nothing** — restores catalogue order. There is no sales data anywhere in the scrape |

The `الاكثر مبيعا` rail that used to sit in the products mega-panel (four
hard-coded catalogue items) was **removed in the 2026-08-03 mega-menu redesign**
(see that section below). It showed the *same* four products under every
category, which reads as incoherent in a per-category preview. If a best-seller
strip returns, it should be **per-category**, driven by the `popularityRank`
every product already carries — `scripts.js` can reach `catalog.json` at runtime
now that site search fetches it (§3), so the data is no longer the blocker; the
coherence question is.

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

Confirmed again from the Store API while building the product page's social
proof: every product returns `average_rating: "0"` and `review_count: 0`. The
`4.8 (126 تقييم)` on `product.html` is therefore still invented placeholder —
it is the one number in that header block that is not real.

### The wallet discount works, but the balance is still fiction

**Replaced the points banner entirely (Ahmed, 2026-07-26): a toggle, and the
WALLET balance rather than points.** The banner spoke in two currencies at once
— "you have 100 points, so you can take EGP 100 off" — which made the shopper
hold a conversion rate in their head to understand the offer, and the rate was
invented anyway. The wallet is already denominated in the same unit as the
bill, so the control can simply say what it will do.

`wallet_toggle()` in components.py renders a `<label>` + checkbox (never a
button — on checkout it sits inside the place-order form, where an untyped
button submits it). scripts.js stores the amount under `abuauf:walletApplied`,
renders a **"خصم المحفظة"** row in the cart summary, the drawer and checkout,
and **caps it at the order's own worth**, so a EGP 1,200 balance against a
EGP 322.50 order discounts 322.50 and the total floors at zero rather than
going negative. Toggling on fires a short particle burst (`celebrate()`),
skipped under `prefers-reduced-motion`.

**`WALLET_BALANCE` in components.py is the single source**, and
`pages/_account.py` reads `CUSTOMER["wallet"]` from it. That constant exists
because its predecessor did not: the points banner defaulted to 100 in one
place and was called with 120 in another, so the cart and the account page
quoted different balances for months.

What remains demo: the balance itself — no wallet endpoint exists — and the
discount is applied client-side only.

**Needs:** a wallet endpoint, and confirmation of the real balance.

### Checkout pickers — branches are real, delivery slots are not

Both were built to the `orderbase-checkout` blueprint (2026-07-26).

**Store picker — real.** Governorate → branch over all **316** of the client's
branches, baked into `checkout.html` at build time as JSON so it works from
`file://` like everything except search. It is two levels, not the blueprint's
City → Area → branch: `branches.json` carries **no area field**, so a third
level could only be invented. Branch addresses are shown because four branches
in one governorate are otherwise indistinguishable; `phone` is omitted, since
all 316 are empty.

**Schedule picker — days real, slots invented.** The seven days are computed
from the device clock at open time (never baked — a build-time date list is
wrong the next morning and would offer a slot in the past). The six two-hour
windows are **in-house placeholder**: the client publishes no delivery windows
anywhere. `SCHED_SLOTS` in `scripts.js` is the single place to change them.

**Needs:** the client's real delivery windows, and confirmation that pickup
branches should be filterable by area (which needs the CMS field first).

### Promo code — real, and it is the one the site already advertises

`هل لديك برومو كود؟` was a `<button>` with no handler on both cart and
checkout — live-looking and inert, the same class as the four dead controls in
`HANDOFF.md` §4. It now opens a field and applies a real discount.

The only code is **`DISCOUNT10` (10%)**, because that is what the site's own
announcement bar advertises on every page. Adding a second would be inventing
an offer. **Keep the bar and `PROMO_CODES` in sync** — a bar advertising a code
checkout rejects is worse than no bar.

The discount is computed from the live subtotal on every render rather than
banked as an amount: a percentage stored in EGP goes stale the moment the
basket changes and keeps discounting a line already removed.

The field now also rides in the **cart drawer** (Ahmed, 2026-08-02), above the
total, so a shopper can apply a code without leaving the drawer. It reuses the
same `[data-promo*]` contract as the page field, so `syncPromoUI` keeps the two
in step and a code applied in either shows applied in both. The handlers were
made **field-scoped** (`applyPromo(wrap)`, `closest("[data-promo]")`) rather
than `document.querySelector` first-match, because two fields now coexist on
`cart.html` — a bare first-match would read and message the wrong one. Enter
inside the input now applies too (it was Apply-button-only before). Placeholder
is `أدخل كود الخصم`; the input border is a **single** divider that darkens to
the CTA ink on focus — no second ring (same "one border" treatment as the
search field above).

### Social proof — the rank is real, an absolute sold-count is not

The product page shows a best-seller badge and a "ضمن أفضل 10 مبيعاً" line.
Both are driven by `popularityRank` in `catalog.json`, written by
`build/fetch_popularity.py`, which walks the Store API's `orderby=popularity`
— WooCommerce's own total-sales ordering — across the client's whole
653-product store. So the badge is earned: a product carries it only while the
client's real sales put it in the top 20, and silently loses it otherwise.

The reference design Ahmed supplied reads **"500+ sold this week"**, and that
specific number could not be sourced. No public endpoint exposes absolute sales
volume, let alone windowed to a week. Rather than fabricate a figure — the
exact failure mode the invented rating above is already flagged for — the page
states the rank, which is true, checkable and carries the same "other people
are buying this" push.

**Needs:** if the client wants a literal unit count, they need to expose a
sales feed. `sold_proof()` in `components.py` is the single place to change.

### Every product now has its own page — and what that multiplied

`build_many()` in `build/pages/product.py` generates `product-<id>.html` for
all 99 catalogue products (Ahmed reported every card opening the same coffee
page). Card links in `components.py` carry the id; `product.html` remains as the
hero's page so nothing that linked to it breaks. (The mega-panel's own featured
tiles carried ids too, but were dropped in the 2026-08-03 mega-menu redesign —
see that section below.) Per-page content is only what we genuinely have per
product:

- **Description and the "الفوائد" accordion are the client's own Arabic**,
  fetched by `build/fetch_descriptions.py` from the storefront's flight
  payload (`descAr` / `descHtmlAr` in `catalog.json`). 97 of 99 products have
  it; **`maamoul-offer-2-chocolate-1-cinnamon-1-plain` (62393) and
  `cranberry-25-gm` (1631) have none** — the client never wrote any — and
  render without a description rather than with invented prose.
- **The reassurance strip is on every page, and reads as product benefits on
  all 99** — the client's own benefit lines where they exist (65 pages), a
  `GENERIC_BENEFITS` trio where they don't (34), and the hero's hand-written
  tiles (1). The old `SERVICE_ITEMS` delivery/returns/branch strip is gone
  (Ahmed, 2026-07-29 — see the strip's own section below).
- **The bundle block builds from the product's own category** and is dropped
  below two companions.
- **The placeholder `4.8 (126 تقييم)` rating is now on 99 pages, not one.**
  Same status as above — the review endpoint returns zeros for everything —
  but the exposure is multiplied; if the client won't collect reviews, the
  block is now worth dropping site-wide in one edit.
- **The recipes section is identical on all 99 pages** under the heading
  "وصفات بالمنتج", which claims a product affinity the two recipes don't have
  (they are the site's only two recipe cards). Kept for layout parity; needs
  either per-category recipes from the client or a neutral heading.

**Needs:** client copy for the two products above; a decision on the rating
block; sign-off on the recipes heading.

### Product gallery photography — real, but 26 products still have one photo

`fetch_galleries.py` pulled **296 genuine extra photographs** off the client's
own CDN, giving 73 of our 99 products a real multi-shot gallery: the product on
coloured sweeps, opened, styled with its ingredients. This is the client's own
photography, not stock and not invented.

The remaining **26 products have exactly one photograph**, and no amount of
scraping will change that — their API image lists contain the same shot twice,
at 600px and 1400px. `product_gallery()` suppresses the thumbnail strip
entirely at one image, so those products degrade to the single-image layout
rather than showing a one-item carousel.

**Needs:** the client to shoot the missing 26. Once uploaded, a re-run of
`python3 build/fetch_galleries.py` picks them up with no code change.

Gallery shots are painted `cover`, filling the plate edge to edge; the main
shot is painted `contain` inside the plate's padding. That is not a style
preference — the main image is a background-isolated cut-out with no backdrop
of its own and needs the plate's colour around it, while the gallery shots are
finished photographs. Containing a photograph strands it in a letterboxed ring
of `#EDEFEB`, which is what Ahmed flagged as the "weird appearance". The plate
carries a **fixed height** with border-box padding so the two modes swap
without the column resizing, and the `/gallery/` path segment is what tells
them apart.

### Size chips are real SKUs, and there are no product variations

Worth knowing before anyone tries to "finish" the variant selector: **Abu Auf
do not model size as a WooCommerce variation.** Every product returns
`type: "simple"`, `variations: []`, `attributes: []`, `weight: ""`. Each size
is its own product, with the weight in the name.

So the chips are recovered by grouping the store on the de-suffixed name
(`fetch_sizes.py`), and each chip carries that SKU's real price *and its real
product id* — selecting 200 جم repoints `data-price` **and** `data-id`, so the
cart adds the SKU actually chosen. Getting only the price right would put the
wrong item in the basket at the right price, which is worse than doing nothing.

Two caveats baked into the scraper: grouping is by name because that is the
only signal available, and where two live SKUs share a size at different prices
the cheaper wins, on the grounds that showing the higher of two prices for the
identical thing is the worse failure.

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
| Product **specs block** (`SPECS_TAGLINE`/`SPECS_DESC`/`SPECS_POINTS` in `build/pages/product.py`, rendered by `specs_block`) | 2026-08-02: the spec strip is now **uniform on all 99 pages** — a tagline, a description and three leaf-marked sentences — at Ahmed's request for handoff consistency. It replaced the per-product icon/label tiles, which took their text from the client's benefit lines and so ranged from full sentences to single words (`مخبوزة`). Brand-level reassurance, no auditable SKU claim. The client's own benefit copy still shows in the الفوائد accordion. Needs sign-off |
| **الفوائد accordion** — `BENEFITS_UNIFORM` + **طريقة الحفظ** (`STORAGE`) in `build/pages/product.py` | 2026-08-02: every product shows the SAME two accordion sections with the SAME content — one fixed benefits list and one storage list — for identical density and layout (Ahmed's handoff requirement, restated after a first pass still varied). The client's own per-product `descHtmlAr` is deliberately NOT rendered here any more; it is still in `catalog.json` if per-product benefits are wanted later. In-house Arabic, needs sign-off |
| **Order line items + re-order** (`ORDERS` in `build/pages/_account.py`) | 2026-08-02: orders now carry catalogue products as line items so the detail drawer and the dashboard re-order can work. Still placeholder — there is no orders endpoint. Totals derive from the items so the list row and the drawer agree |
| **Points → wallet** (`initPoints` / `syncWalletBalance` in `scripts.js`) | 2026-08-02: the redeem button was dead; it now transfers the points' EGP value (`POINTS_EGP = 12`) into the wallet balance (`abuauf:pointsWallet`, added to `BASE_WALLET = 1200`, mirroring `WALLET_BALANCE`) and every wallet display updates. Demo only — points and wallet have no live endpoint (see §1) |
| **Free-delivery threshold** `FREE_SHIP = 500` (`scripts.js`) | 2026-08-02: the cart's "add X for free delivery" bar and the fee it waives. An in-house number — confirm the client's real free-shipping threshold (or remove) before launch |
| **Demo dead links** (`DEMO_DEAD_PAGES` in `scripts.js`) | 2026-08-02: for the client walkthrough of the shipping cycle, the chrome's links to the static informational pages (about, blog(s), branches, contact, policies, rewards, export, store-closed) resolve to `#` so the demo does not wander into unfinished pages. The shopping/checkout/account flow is untouched. **Empty the set to restore full navigation for launch.** |
| **All English strings** in the `EN` dictionary in `scripts.js` | Standard commerce terminology written in-house — `Offers & Discounts`, `Checkout`, `View cart`. Not the client's wording. **Product names are the one exception** — those are real catalogue data |
| **Gifts home section** (`GIFT_INTRO` / `GIFT_FEATURES` / `GIFT_OCCASIONS` in `build/pages/home.py`) | 2026-08-06: the gifts banner was rewritten from a single tagline + a 2×2 grid of unrelated product-spread photos to a copy-led pitch — intro paragraph, three benefit rows (the client 3D spec icons — shield/leaf/delivery), occasion chips (`رمضان/الأعياد/…`). In-house Arabic, needs sign-off. (The old banner's unconfirmed `20٪` discount eyebrow was removed 2026-08-06 at Ahmed's request.) The hero image is `images/abuauf/site/gifts-isolated.webp`, a **real** Abu Auf gift set (nuts pack, creamy peanut butter jar, Premium Fresh Food pack, Mabrom dates tub, gold ribbon + gift tag, on a base of nuts/dried fruit/oats), generated in Higgsfield from the real product references and background-removed with a border-connected flood + largest-component keep (the studio checkerboard it shipped on was baked-in, not a real alpha channel). Made deliberately large on desktop — its grid track is the wider one (1.18fr vs 0.82fr). To swap in another cut-out, drop a transparent PNG/WebP at the same path — the markup keys off the filename only |

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

### Mega-menu redesign — rail + live preview (Ahmed, 2026-08-03)

Ahmed reported the products mega-panel forced him to "travel with the mouse to
the left to choose from the products." Two causes, both structural:

1. **Distance.** The old layout was three columns (RTL: categories →
   sub-categories → a best-seller rail). Reaching a sub-category or product
   meant dragging the pointer across almost the full panel width.
2. **Diagonal re-trigger.** Categories switched on `mouseenter`, so any vertical
   drift on that journey crossed a *sibling* row and swapped the whole panel out
   from under the cursor.

**New shape — a rail + a preview stage.** The rail (RTL start / right) is one
**link per category**, each carrying its own **photo thumbnail** (Ahmed asked
for the category photos to stay, restyled — they now live in the filters
themselves). Hovering or focusing a row opens that category's preview in the
stage to its left, **in place**; clicking the row shops the whole category in
one hit, so the commonest goal needs no reach at all. The stage puts the
**sub-category tiles nearest the rail** (shortest move) and a **branded photo
hero** — the category image at full size with a `تسوّق الكل` CTA over a
deep-green scrim — on the far side. Categories with no sub-categories (offers,
drinks, spices, gifts) get a single wide hero instead of an empty tile grid.

**The actual fix is hover-intent** (`initMegaMenu`). A category switch is delayed
~110ms, and every fresh `mouseenter` cancels the pending one, so only the row the
pointer **settles** on — the last entered before it dives into the stage — wins;
rows merely brushed in transit never fire. The pending switch is deliberately
**not** cancelled when the pointer leaves a row *toward the stage* (a fast dive
would otherwise drop the very category being aimed at) — only when it leaves the
whole panel. Verified with a synthetic rapid-cross test: brushing rows 2→3→4 at
40ms intervals kept the panel on row 1, and it switched to 4 only once the
pointer settled. Keyboard focus activates immediately; ↑/↓ move between rail
rows; Esc closes; all motion is gated on `prefers-reduced-motion`.

**Selected ≠ hover is preserved** (hard rule 8, reported four times on this very
column). Selection is carried by the leading brand bar, ink, and a leaf-green
**ring on the thumbnail** — persistent, structural marks; hover is only a faint
transient wash. A row that is both shows both; a row that is merely selected
never looks stuck under a pointer that has left.

**Sub-tiles** are a two-up grid of quiet beige targets (≥52px). The `جميع X`
tile spans both columns (it is the primary action and holds the longest string).
Long names **wrap** rather than truncate — two lines fit inside the tile — so
`مكسرات محمصة ومملحة` stays whole at the tightest supported width. The hero track
narrows 300→260 at `lg` to keep the tiles breathing where the container is
tightest; below `lg` the panel is hidden and phones keep the drawer, untouched.

**What was dropped:** the four-item `الاكثر مبيعا` rail (see §2). It was the same
four products under every category, incoherent in a per-category preview.

**Image assignments** (all 8 categories now have one; `MAIN_MENU` in
`scripts.js`):

- Offers → `image-48.png` (a product spread). It is portrait with transparent
  margins, so a centred square crop read as blank; `.mega-cat__thumb img` uses
  `object-position: center 78%` to crop to its products. Square photos ignore
  this, so it is a safe global rule, not a special case.
- Nuts/coffee/dates/healthy/spices → their own webp shots; gifts → the gift-box
  photo (moved off offers, where it belongs).
- **المشروبات (drinks) reuses the coffee photo** — no dedicated hot-drinks image
  exists, and it is a warm beverage either way. A distinct photo would stop the
  rail showing two coffee thumbnails. Same absence-over-invention rule as the
  branch phones; flagged for the client.
- **Perf:** three category images are heavy PNGs (`image-48` 749KB,
  `Healthy_Snaks2` 755KB, `gifts` 650KB). They load lazily on first panel open,
  but resized thumbnails would cut ~2MB off that first open. Worth a pass.

Lives in `megaPanelHTML()` + `initMegaMenu()` (`scripts.js`) and the `.mega-*`
block in `styles.css`.

### Search field focus: a single darkened divider, not the offset ring

Ahmed asked (2026-08-02) to drop the "double border" the search field showed on
focus. The cause: `.search-row:focus-within` painted the global focus treatment
— a `2px solid #163300` outline at `outline-offset: 2px` **plus** a white halo
`box-shadow` — around a row that already carries its own `border-b` divider, so
focus stacked a second, floating border outside the first.

The row is now given a lighter single cue instead: `.search-row:focus-within`
just darkens its existing bottom divider to the brand ink (`#163300`). No ring,
no halo, no offset, no layout shift. This is a **deliberate, scoped** softening
of the site's focus-visible standard (documented in `styles.css` under
"Focus"), justified by the search being a self-contained modal whose **close
button keeps the full global ring** — so a keyboard user is never left with no
focus indicator in that context. The newsletter field, which shares the same
pattern, was **left on the full ring** (it lives in the footer, not a modal).
If the single-divider cue is judged too subtle, the fallback is to restore the
ring for `.search-row` — the rule is a two-line change.

### The best-seller badge has a second, category-relative tier

Ahmed asked (2026-07-22) for more products to carry a best-seller badge. The
store-wide top 20 is dominated by snacks and offers, so most categories had
no badged product at all and a shopper browsing spices never saw the signal.

Two tiers now, **both from the same real `popularityRank`** — this reads the
existing WooCommerce sales ranking at a narrower scope, it does not invent a
second metric:

| Tier | Condition | Label |
|---|---|---|
| Store-wide | rank ≤ 20 of 653 | `الأكثر مبيعاً` |
| Category | top 3 of its category | `الأكثر مبيعاً في <category>` |

Coverage went **20 → 33 of 99**, and from 6 categories to 9. The store-wide
label wins where both apply; two badges on one card would compete.

`BEST_SELLER_CATEGORY_MIN = 6` guards the obvious abuse: top-3 of a
four-product category is not a distinction, it is three quarters of the shelf.

`sold_proof` follows the badge exactly — a product wearing "best seller in
spices" with no proof line beside it is the same split signal the tiers were
added to remove.

**What was NOT done, and why.** Ahmed's first request was a badge on *every*
product. That cannot be honest: on a product ranked #500 the badge asserts a
sale that did not happen, and `ضمن أفضل 20 مبيعاً` is simply false. The
category tier is how far the real data stretches. 66 products still carry no
badge, and should not.

Fixing this also exposed a latent bug in `sold_proof`: its glyph, its bare
text and the `<span class="latin">` around the number were each separate flex
items, so they wrapped independently. With the short `في أبو عوف` it never
wrapped and nobody saw it; with a long category name the line broke as
`ضمن / أفضل` with the numeral stranded between the two lines. The sentence is
now a single flex child.

### Product benefit tiles now come from the client's own copy

Ahmed reported (2026-07-22) that only the coffee product showed benefit
tiles and everything else showed delivery notes. Correct: `trust_row` was
called with `BENEFIT_ITEMS if hero else SERVICE_ITEMS`, so the hand-written
tiles belonged to the single hero product and the other 98 got the
delivery / returns / branch-count strip. A shopper moving from the hero to
any other product saw the page change template.

`product_benefits()` now derives the tiles from the client's own
`descHtmlAr` benefit list. Coverage after the change:

| | pages |
|---|---|
| 3 benefit tiles from client copy | 59 |
| 2 benefit tiles from client copy | 6 |
| generic benefit trio (client wrote no benefits) | 34 |

**Update (2026-07-29):** the 34 fallback pages previously showed the
delivery / returns / branch-count **service strip**, which Ahmed reported read
as a delivery notice sitting where every other product shows benefits — a
developer opening two pages saw two different spec rows. Those 34 now fall back
to `GENERIC_BENEFITS`, a generic **product-benefit** trio (`منتج مختار بعناية`
/ `طازج وعالي الجودة` / `جودة أبو عوف المضمونة`), so the spec row reads as
product benefits on all 99 pages. `SERVICE_ITEMS` and the `BRANCH_COUNT` import
are removed from `product.py`. The generic copy is **in-house Arabic pending
client sign-off** — see §2 — deliberately brand-level with no auditable
supply-chain claim, the same restraint as the hero copy.

**The 34 having no client copy is the honest limit, not an oversight.** Those
products have no benefits list in the scrape at all, and the alternative is
writing product-specific claims on the client's behalf — the same line the
branch phone numbers and the compare-at prices were held to. The generic trio
sidesteps that by staying brand-level rather than making a claim about the SKU.

Two details worth keeping:

- Lines that are only a pack weight (`"100جرام"`) are filtered out. They are
  spec, not benefit, the size chips already show them, and they read as
  filler in a tile.
- The hero keeps its hand-written tiles **because its own benefits list is a
  single line reading `100جرام`** — deriving from it would be a downgrade.
- `trust_row` now drops the subtitle line when there isn't one and picks its
  column count from the item count, so a two-benefit product gets two columns
  rather than a hole.

### Search and cart now ride along on mobile too, on a green plate

Ahmed asked for the desktop ride-along on mobile (2026-07-22). The mobile
masthead scrolls away completely and there is no 48px nav at that width to sit
under, so once you were a screen down the only route back to the cart was
scrolling to the top.

The mobile search/cart group now carries the **same `data-sticky-actions` hook**
as the desktop one, so `initStickyNav` drives both from one handler on one
threshold and they cannot disagree about whether the page has scrolled. Two
things differ from the desktop rule, both forced rather than chosen:

- **It parks at `top: 8px`**, not `top: 60px`. There is no nav to sit beneath.
- **The plate is `#185039`, not translucent white.** The desktop rule's
  `rgba(255,255,255,.92)` works only because the desktop search button carries
  `bg-cta` under a white glyph. The mobile search button is a bare glyph and
  `icon-search.svg` is **white** — on a white plate it disappears entirely.
  Reusing the header's own green keeps both glyphs on exactly the pairing they
  already pass AA against, so this adds no new contrast surface.

Dropping the desktop rule's `backdrop-filter` here was deliberate and not just
thrift: blurring live backdrop pixels under a `position: fixed` element
re-rasterises on every frame of every scroll, which is the same cost the
product-card change below exists to remove.

Overlays are `z-100` against the pill's `z-90`, so opening search, cart or the
menu covers it rather than fighting it — verified, not assumed.

### Two mobile scroll-performance bugs, both measured

Ahmed reported scroll lag and "sometimes it doesn't want to scroll"
(2026-07-22). Two independent causes, both confirmed in the browser:

**1. Every product card held a permanent compositing layer.**
`.product-card__frame` carried an unconditional `will-change: transform` to
prime its 4px hover lift. Counted live: **35 promoted layers on the home page,
99 on `shop.html`** — one per card, held for the life of the page whether or
not the card was ever pointed at. That is the exact misuse MDN warns about, and
on a phone it is paid as scroll jank and memory pressure to prime a transform a
touch device **can never fire**. Removed outright rather than moved to `:hover`:
the compositor already promotes for the duration of a transform transition, so
the hint was buying nothing on desktop either. Now **0 promoted layers**.

All the card `:hover` rules moved behind `@media (hover: hover) and (pointer:
fine)` at the same time, which also fixes a second-order bug — on touch,
`:hover` latches after a tap and stays latched, so a tapped card sat lifted and
zoomed, looking stuck under a pointer that was never there. That is the
`CLAUDE.md` selected-vs-hover rule arrived at from the other direction.
`:focus-within` is deliberately **not** gated, so keyboard focus still reveals
the quick-look chip on a touchscreen laptop.

**2. The carousels were eating vertical scroll.** This is the "won't scroll"
half. A rail is a horizontal scroll container with `scroll-snap-type: x
mandatory`, and the home page stacks four of them down its length — so a thumb
drag beginning on a rail, which is most of the page's height, was a coin toss.
When the browser's gesture disambiguation locked to the horizontal axis the
rail consumed the gesture, the mandatory snap pinned it to the current slide,
and the page did not move at all. It reads as the site freezing, not as a
carousel working. `.carousel-track` now sets `touch-action: pan-x pinch-zoom`,
handing the vertical axis straight back to the page. **`pinch-zoom` is kept
explicitly** — bare `pan-x` would also kill zoom on every rail, trading a WCAG
1.4.4 regression for a scroll fix. `overscroll-behavior-x: contain` stops a
fling off the end of a rail chaining into a browser back-navigation.

Sweep after these changes: `pageOver: 0` everywhere, **0 contrast failures
across ~4,900 text nodes**. The residual `sr-only` and `carousel-dot` offenders
the sweep reports were verified byte-identical against a stashed baseline —
they pre-date this work. `sr-only` is 1px-clipped by design and the sweep's
`byDesign` filter only covers `ellipsis`/`line-clamp`, so it does not catch it.

### The same scroll pass, on desktop (Ahmed, 2026-07-22)

The mobile pass above fixed mobile. Ahmed reported the lag on desktop too, and
the causes were different ones — none of them touched by `touch-action` or by
the `will-change` removal.

**1. A blurred backdrop on a fixed element, held for the whole page.** The
sticky search/cart pill carried `background: rgba(255,255,255,.92)` over
`backdrop-filter: blur(10px)`. A blurred backdrop has to re-read and
re-rasterise whatever is behind it **every frame**, and because the pill sticks
the moment you pass 150px it did that for the entire scrolled length of every
page. The mobile rule had already dropped the blur for exactly this reason —
desktop just never followed. Now an opaque `#fff`, which is strictly *more*
contrast than 92% white over unknown content, so no pairing needed re-checking.

**2. One `update()` per scroll EVENT, not per frame.** `.carousel-track`'s
handler called `requestAnimationFrame(update)` unconditionally, so a burst of
scroll events inside a single frame queued a callback each — and momentum
scrolling and snap-settling both produce exactly that burst. Now latched to one
per frame.

**3. `update()` forced a synchronous layout on every call.** It interleaved
geometry reads with class writes, and reached `getComputedStyle` twice per
call — once inside `getPos()`, which runs on every scroll frame. Direction now
comes from `document.documentElement.dir` (an attribute read, no style recalc,
and `dir` is only ever set on the root element — verified across all 130
pages); the gap is measured once and re-measured only on resize; and every read
happens before the first write. Measured against a reconstruction of the old
shape in the browser: **~1.7x cheaper per call**, on top of the far larger win
from calling it once a frame instead of N times.

**4. Every language switch leaked a listener set and a timer per rail.**
`kInit()` re-runs over the whole document on repaint and `initCarousel` was not
idempotent, so each toggle bound another scroll listener, another resize
listener and another autoplay `setInterval` to every carousel — compounding
scroll work, and autoplay timers fighting each other for the same `scrollLeft`.
Guarded on `data-carousel-ready`. Verified: two full `kInit` re-runs now add
**0** listeners and **0** timers.

**5. Autoplay ran forever.** A bare `setInterval` that kept ticking in a hidden
tab (queueing a smooth-scroll animation nobody could see), kept ticking while
the visitor was reading or dragging the rail, and ran under
`prefers-reduced-motion`. Now stops on `visibilitychange`, stops while a
pointer or the keyboard is inside the carousel, and never starts under reduced
motion. `scroll-behavior: smooth` is gated behind the same preference.

**Frame timing could not be measured in this environment** — the browser pane
reports `visibilityState: "hidden"`, where `requestAnimationFrame` does not
fire and CSS transitions do not advance. The numbers above are counts and
per-call benchmarks, which are real; an fps figure would not have been. (The
same trap made a working `aria-pressed` style look broken: the transitioned
properties were frozen at their start value while the untransitioned one had
already changed.)

### The language switch now covers the whole site, in three passes

Ahmed asked for every string to convert, not just the chrome (2026-07-22).
Measured before: **1,457 of 1,524** distinct Arabic strings had no dictionary
entry — about **70% of every page stayed Arabic** — plus 499 Arabic attribute
values the switch never looked at at all.

Adding keys could not have fixed most of it. `translateDocument()` matched
whole text nodes only, so three surfaces were structurally unreachable:

- **Any run broken by an inline child.** `4.8 (126 تقييم)` is three text nodes
  because the rating and count are `.latin` spans; no fragment of it could
  match any key, however the dictionary was written. Same for the best-seller
  badge, the delivery promise, every account-menu row, every form label with a
  required marker. Fixed with a **template pass**: an element is keyed on its
  content with element children replaced by `{0}`, `{1}`…, so one key covers
  every product, price and rank, and the original child nodes are spliced back
  in — `.latin` spans keep their class, their digits and any state on them.
  Applying a translation that would drop a slot is refused outright: losing a
  price to a typo'd entry is worse than staying in Arabic.
- **Attributes.** `placeholder` / `aria-label` / `title` / `alt` now switch.
- **`<title>` and the meta description.** A page that reads English and titles
  itself in Arabic is half-switched.

The dictionary moved to **`build/i18n.py`**, generated into
`static-export/i18n-en.js` on every build (so it cannot go stale against the
markup, same contract as the Tailwind build). It lives there because that is
the only place that can read `catalog.json` — all 99 product names resolve to
the client's **own English `name` field** rather than being retyped — and
because formulaic families are better looped than listed: gallery labels alone
would be 40 hand-written entries, and the mega-menu's `"تسوق كل " + name` links
are built by *concatenation*, so the string that reaches the DOM is not a
literal anywhere and is now generated from the same category list the nav uses.

It is a plain script, not a fetch, so **translation still works from
`file://`** — search remains the only feature that does not.

Result: **0 untranslated text nodes and 0 untranslated attributes** across a
16-page sample covering every layout. The only Arabic left in English mode is
the **310 branch street addresses**, deliberately — a postal address is not
copy, and transliterating "برج نفرتيتى - تقاطع جمال عبد الناصر" would produce
something a courier cannot use. Governorate *names* do translate, because they
are also section headings.

Round trip ar → en → ar restores `textContent`, element count and comment count
exactly; `index.html` and `cart.html` come back byte-identical. Whitespace
*between* the parts of a templated element is normalised to single spaces and
does not survive — that is the price of a collapsed dictionary key, and HTML
collapses runs of whitespace in text anyway, so nothing moves on screen.

**Status of the English: still placeholder, and now in two tiers.**
`build/i18n.py` splits them deliberately, because they do not carry the same
authority. `UI` is our own interface copy — standard commerce terminology,
written in-house, the same status the chrome strings always had. `COPY`/`COPY2`
is the **client's own marketing and product prose**, translated in-house
because there is no English source for any of it: the Store API returns English
*names* but never English *descriptions*. That is the one place in this project
where we write English for text the client wrote in Arabic. It is honest
translation — nothing machine-translated, nothing claiming more than the Arabic
does — but it is our words for their product and **needs their approval before
launch**.

### Translating the site exposed two latent layout bugs

Both were always there. Arabic simply happened to be short enough to hide them,
which is worth recording: a layout verified in one language is not verified.

- **`<fieldset>` carries a UA `min-inline-size: min-content`**, which outranks
  the `min-width: auto` every other flex/grid child gets and **cannot be
  cancelled by a `min-w-0` utility** — the utility sets `min-width`, the UA
  rule sets `min-inline-size`, and the logical property wins. The checkout
  order-type fieldset held the form at 359px inside a 328px track at 375, and
  the page's `overflow-x-hidden` ate the difference: clipped copy no scrolling
  could reach. `styles.css` now sets `fieldset { min-inline-size: 0 }`
  site-wide. This is the `min-w-0` rule from `CLAUDE.md`, in the one place a
  `min-w-0` class cannot express it.
- **`label { white-space: nowrap }`** sat on the bare element selector,
  inherited from the original static export, and was therefore inherited by
  everything a label wraps — including the checkout order-type cards, a whole
  sentence of body copy that physically could not wrap at any width in any
  language. Now scoped to `.label`, the short stacked caption it was written
  for. A caption may reasonably refuse to wrap; a label that *contains* layout
  must not decide that for its contents.

Also fixed while re-balancing: the cart line's stepper + delete row had a
hand-tuned 320px budget balanced against the Arabic `حذف`. "Remove" is ~21px
wider and put the row 7px over the same 141px column — the identical failure,
one translation later. It now wraps rather than being re-tuned, so it stays
one line wherever it fits and does not need re-balancing for the next language.

**Sweep after all of the above, seeded cart, two lines at two-digit quantity:
33 pages x 2 languages at 375 and at 320 — `pageOver: 0` everywhere, 0 real
overflow, 0 contrast failures across ~1,970 text nodes per language.** The
residual `sr-only` entries the sweep reports pre-date this work (1px-clipped by
design; the `byDesign` filter only covers `ellipsis`/`line-clamp`).

### Product short descriptions were rendering raw markup

Not a design decision — a defect found while auditing translatable text. 20 of
the 99 products carry pasted editor debris inside the client's own
`short_description`: `<span data-sheets-root="1">` from a Google Sheets paste,
`x_MsoListParagraph` from Word, and on `product-8543` an entire
`<div class="… AIPRM__conversation__response">` wrapper, which is what a ChatGPT
web export leaves behind. `descAr` goes through `e()` into a `<p>`, so all of
it escaped and **rendered as literal visible angle brackets in body copy**.

Stripped at render (`_plain()` in `build/pages/product.py`), not in the JSON:
`catalog.json` is fetched data and is meant to stay a faithful copy of what the
client's endpoints return, so laundering it in place would mean the next
re-scrape silently reintroduces this. **The underlying data problem is the
client's to fix** — worth raising with them, since it is in their live product
records, not only in our copy.

### The scroll reveal is site-wide, and carries a failsafe

Ahmed asked for an entrance animation across the whole site (2026-07-22). The
`[data-reveal]` system already existed but had been hand-applied to home,
product and the auth layout only — 14 elements — so most of the site scrolled
dead. It is now injected centrally by `_with_reveal()` in `components.py` onto
every `<section>` of every page, which keeps it one decision rather than 37.

Two properties worth preserving:

- **Above-the-fold sections are never animated.** The observer marks anything
  already in the viewport as revealed without transitioning it, so arriving on
  a page does not trigger a wave of fades. Only content you scroll to moves.
- **A 2.5s failsafe reveals anything still pending.** This is not belt-and-
  braces paranoia: `IntersectionObserver` genuinely does not fire in a hidden
  or backgrounded document — verified here, where even a default-config
  control observer stayed silent and the affected sections rendered visibly
  washed out. Before the reveal went site-wide the cost of that was one home
  rail; now it would be most of every page. The failsafe holds the system's
  founding rule — degrade to *unanimated*, never to *invisible*.

The sweep must force-reveal before measuring or it reads the whole page at
opacity 0. `HANDOFF.md` §5 does this; do not drop that line.

### Search reads `catalog.json` at runtime — the one place that does

Everywhere else the catalogue is baked in at build time on purpose, and
`scripts.js` deliberately had no runtime access to it. Search cannot work that
way: it has to reach products that are not on the current page. So the modal
`fetch`es `data/catalog.json` once, lazily, on first open, and caches it.

Two consequences, both accepted:

- **Search needs HTTP.** It cannot work from `file://`, unlike the category
  chips, which filter cards already in the DOM specifically so they would.
  Everything else on the page still works from `file://`; only search degrades,
  and it degrades to a message rather than a spinner that never resolves.
- **Arabic is folded before matching.** The catalogue writes `قهوة` with a
  `ة` and shoppers type `ه`; `ى`/`ي` and `أ إ آ`/`ا` are used
  interchangeably; tashkeel is never typed. Without folding, `قهوه` returned
  nothing while `قهوة` returned six, which reads as a broken search rather
  than a spelling difference.

The five idle chips are no longer labelled `الأكثر بحثاً`. There is no search
analytics behind this build, so calling them the most-searched was inventing
data — and the old terms (`قهوة تركي`, `بوكس هدايا`) matched **zero**
catalogue products, so every chip was a guaranteed empty result. They are now
`اقتراحات البحث`, counted off the real product names at 5–7 hits each.

### The product page's buy block is now the stepper (Ahmed, 2026-07-26)

Two passes on the same complaint: *"3 actions I should do to continue."* The
block was `[− 1 +] [اضف الى السلة]` plus an `اشتري الان` link — set a quantity,
commit it, then leave the page to find out what was in the basket.

The first pass kept the add button and made it open the summary drawer on
landing. Ahmed's follow-up was the sharper version: **if the counter is bound
to the cart, the commit step has nothing left to do.** So:

- The stepper **is** the add control. `+` on a product that is not in the
  basket is what puts it there; every press after that moves the same line;
  `−` at 1 removes it.
- It therefore reads the CART's quantity and **shows 0 when the product is not
  in it.** A counter that "syncs directly" cannot sit at 1 while the basket
  holds none, and `−` is disabled at 0.
- The button beside it is **`اشتري الان`**: it opens the summary drawer to
  carry on, adding one first if the basket is empty of this product, so "buy
  now" always buys something.
- Every `+` throws a ghost to the cart. With no add button left, that flight is
  the only motion confirming a press reached the basket.

`qty_stepper(cart_bound=True)` marks these with `data-cart-bound`, and
`initSteppers` skips them deliberately — they are driven by the delegated cart
handler instead, so there is exactly one writer. `syncBuyBlock()` repaints them
from the store on every `cart:change`, the same contract `syncCardSteppers()`
uses, so the drawer, the cards and this block can never disagree.

**The gallery moved to the RTL-right column and is sticky** (`lg:sticky
lg:top-[60px]`, matching where `[data-sticky-actions]` parks). This required
changing `<main>` from `overflow-x-hidden` to **`overflow-x-clip`** site-wide:
`hidden` on one axis forces the other to `auto`, which makes `<main>` a scroll
container, and a scroll container is what `sticky` resolves against — the
element silently did nothing. `clip` clips identically without creating one.

### Checkout's CTA is still a link, so its `required` fields never fire

The checkout form has `required` on 12 fields and native validation enabled,
but the primary CTA is an `<a href="thank-you.html">` sitting inside the form
rather than a submit button — so the browser never validates and an order can
be placed with every field empty. The summary and the empty-basket guard were
fixed in this pass; **this was left alone at Ahmed's direction** (2026-07-22),
as converting it to a real submit is a flow decision, not a markup fix.

**Needs:** a decision on whether checkout should validate client-side before
advancing, and what "advancing" means without a backend.

### `SITE_ORIGIN` is empty, so canonical and `og:url` are not emitted

`components.py` gates the three absolute-URL tags behind `SITE_ORIGIN`, which
is deliberately blank. This build is not deployed, and `abuauf.com` is the
client's *existing* live site — pointing canonical at it would tell search
engines these pages are duplicates of someone else's. The relative tags
(og:title, og:description, og:type, og:site_name, og:locale, twitter:card,
theme-color) ship on all 130 pages regardless.

**Needs:** the production host, set once, before launch.

### Hero banners are taller than the artwork, so the sides are cropped

Requested by Ahmed: more height on the home hero. The banners are supplied at
exactly 1440×440 (desktop) and 505×680 (mobile), so height can only come from
cropping — the slide box is now `md:aspect-[1440/470]` / `aspect-[505/728]`
with `object-cover`, about +7%.

**How far this can go is set by one banner.** `UAE-Abuauf-desktop-Ar.webp`
carries the أبو عوف wordmark hard against the trailing edge, its ® at roughly
96% of the width. At 1440/470 the crop is 46px a side and the ® survives with
about 8px to spare; past that the mark starts losing its registered symbol.
Verified by rendering the crop, not by eye. **Re-check this if a banner is
swapped**, and ask the client for taller artwork if more height is wanted —
that is the honest fix.

### Rating marks are stars (Ahmed, 2026-07-22), and 4.8 draws as 4.8

Two things were wrong with the rating: five identical full marks sat next to
the text "4.8", contradicting it, and the marks were spaced far enough apart to
read as five separate objects rather than one score.

The fifth mark is now filled to the exact fraction (80% for 4.8) by layering
one glyph over another and clipping by width, so the empty and full states are
guaranteed the same shape. The clip uses `inset-inline-start`, so it fills from
the right in RTL.

**The marks are stars.** They shipped as the brand heart, flagged here as a
brand decision to be asked about — Ahmed answered on 2026-07-22: stars. The
deciding observation stands on its own: on the product page the heart row sat
one gesture away from the card's *favourites* heart, so a rating read as a
save-count. The heart now means favourites and nothing else; `rating()` is
shared, so the swap is site-wide by construction.

The unfilled remainder is `#E4D9B4`, about 1.9:1 on white. That is deliberate
and not a contrast failure: it is a decorative shape, the row carries
`role="img"` with the score as its label, and the numeric value is printed
beside it in full-contrast text.

### The product page's worked example is no longer the Figma's product

The Figma hero is a chocolate-dates product and the page used to render
`معمول بعجوه المجدول مغطى بالشيكولاته` to match it. That product has exactly
one photograph on the client's CMS, so it could not demonstrate the gallery
Ahmed asked for.

It then became `قهوة بن برازيلى سادة فاتح - 100 جم`, and the reason is worth
recording because it is a genuine trade rather than a preference.

Ahmed asked for the weight chips to move the price. Only **10 of our 99
products are sold in more than one size at all**, and the dates product is not
one of them — it is a single 300 جم SKU, so on that page the chips could only
ever have been theatre. The coffee is the one product that makes *every*
signal on the page real at once:

| Signal | Coffee (current) | Dates (previous) |
|---|---|---|
| Real size SKUs | **3** — 50/100/200 جم at 69/82.5/220 | 1 |
| Real gallery photos | 3 | 9 |
| Popularity rank | **#12** — badge earned | #7 |

The cost is a thinner gallery, 3 shots instead of 9. That was judged the
smaller loss: the gallery still works and still shows real photography, whereas
size-to-price cannot be shown at all without a multi-size product.

`_hero()` falls through a list of names in order, so **both previous picks are
still in it** — move a name to the front to switch the page back. If you do,
note that `DESCRIPTION`, `BENEFITS`, `STORAGE` and `BENEFIT_ITEMS` in that file
all describe the coffee and would need rewriting; the breadcrumb category is
already read off the product and needs nothing.

### The product page's reassurance strip: benefits on the hero, services elsewhere

The three icons under the CTA mirror the reference design's "100% vegan /
60-day guarantee / 3rd-party tested" row. **None of those specific claims are
made about Abu Auf's products by anyone**, so none of them are used. On the
hero the row carries the product's own benefits — light roast, Brazilian
beans, smooth taste — a translation of the client's own English `shortDesc`
for that SKU plus what the product name states.

It first shipped carrying delivery/returns/branch-pickup instead; Ahmed asked
for product benefits, matching the reference. The delivery line still exists on
the page, in its own strip below.

When every product got its own page (2026-07-22), Ahmed asked for the layout
to be uniform across all 99 — so the other 98 pages carry the strip too, with
`SERVICE_ITEMS` in `product.py`: two-hour delivery (restates the row lower on
the same page), 14-day returns (restates return-policy.html), and the branch
count (computed from `branches.json`, never typed). Per-product benefit trios
for 98 products would have been mass invention; service restatements are the
exact use `trust_row()`'s contract describes. The three service strings are
in-house Arabic, unsigned like the rest.

Still unsigned-off, like every translated string in this build. The line worth
holding is the distinction that decided the copy: *"light roast"* restates the
client's own product name, whereas *"third-party tested"* is an auditable claim
about a supply chain. Restate; never invent. `trust_row()` takes its items as
an argument, so a signed-off claim drops straight in.

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

### The saved-favourite heart is pink — a colour outside the design system

Ahmed's direction (2026-07-29): the heart icon should paint solid pink once
saved, rather than the brand CTA green every other "selected" state in this
build uses. Neither the Figma variables nor `tailwind.config.js` define a pink
token anywhere in the palette — this is a deliberate one-off exception, the
conventional red/pink "liked" heart from outside this design system, not a
value pulled from Figma or measured off abuauf.com (their live storefront has
no favourites/wishlist affordance to measure against). Implemented as a literal
`#E11D48` in `styles.css` on `.fav-btn[aria-pressed="true"]` rather than a new
config token, because it is used in exactly one place. **The designer should
be told** — same footing as the WCAG contrast deviation above.

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
| ~~`حذف` remove~~ | ~~**24 wide** (44 tall)~~ | **GONE — see below** |
| ~~`خصم المبلغ` apply promo~~ | ~~89×**34**~~ | **GONE — replaced by the wallet switch, §1** |
| `أضف` | 76×**36** | cart page |
| Card stepper `−` / `+` | 44×44, except **40.7×44** | `shop.html` at 320 only, and only at a 2-digit quantity |

**The `حذف` link is gone (Ahmed, 2026-07-26)** — at quantity 1 the `−` becomes
a trash can and removing is what it does. The behaviour was already that:
`Cart.setQty` removes below 1, so that press always emptied the row and only
the glyph lied about it. Two consequences worth recording:

- It **frees the budget that was blocking the stepper resize.** The arithmetic
  above (162 against 141 available) counted `حذف` and its gap; with both gone
  the row has room, so growing the stepper to 44×44 is now a size tweak rather
  than the layout decision it used to be. **Not done in this pass** — it is a
  separate change and deserves its own measurement.
- One control now carries two meanings, so the accessible name follows the
  glyph: `syncLineDecrement()` swaps `aria-label` between `إنقاص` and `حذف`. A
  screen-reader user hearing "decrease" would otherwise get no warning that the
  next press removes the line entirely.

The same swap is on the product page's stepper, which is now cart-bound (§3).

Re-audit the whole site's tap targets before trusting the "≥44px, audited and
passing" claim elsewhere.

The product-card stepper is the one case that was sized deliberately against
this budget rather than inheriting it. It holds a full 44×44 everywhere except
`shop.html` at exactly 320px with a two-digit quantity, where the card is
128.5px wide — 96.5px of content — and 44 + 16 + 44 = 104 does not fit. The
buttons absorb the 7px rather than the row overflowing, landing at 40.7px. The
alternatives were all worse: a hard 104px floor overflowed the card, and an
88px floor left the control wedged beside the heart at 414 and squeezed the
taps to 38px. See the `basis` note in §8.

### Cart-line quantity clips past two digits — pre-existing, found in passing

`[data-line-qty-num]` in the cart drawer is a fixed `w-4` (16px). Measured: `1`
and `10` fit, `99` is 1px over, `123` is 7px over and visibly clipped. Not
touched, because widening it puts the row back over the 320px budget described
above — the same layout decision that is already blocking the stepper resize.
Only reachable at a quantity of 100+, which takes a hundred taps to reach from
the UI.

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

### `min-width` sizes a flex item; `flex-basis` also breaks the line

Building the product-card stepper burned three rebuild-and-sweep rounds on
this. Two different jobs get confused:

- **When does the control drop to its own line?** That is decided by the item's
  **flex base size**. `min-width` does not participate.
- **How small may it get once it is there?** That is `min-width`.

Using `min-width` for both is a trap with no good value. At `min-w-[104px]`
(the comfortable size) the control could not shrink into the 96.5px card on
`shop.html` at 320, so the row overflowed by 6px. At `min-w-[88px]` it fit, but
it also still *fit beside the heart* at 414, so it never wrapped and the taps
were squeezed to 38px. `grow shrink basis-[104px]` gets both: 104 decides the
wrap, and the control still shrinks to 96.5 once it is alone.

Two riders, both of which bit:

- **Do not write `flex-1 basis-[104px]`.** Tailwind emits the `flex` shorthand
  *after* `basis`, so `flex: 1 1 0%` silently resets the basis to 0 and the
  wrap never happens. Use the longhands, `grow shrink basis-[…]`. Same family
  of bug as the `relative`/`fixed` emit-order trap in CLAUDE.md.
- **A nested flex container needs its own `min-w-0`.** The stepper is itself a
  flex row, so its automatic minimum resolved to its own min-content (103px)
  and it refused to shrink to the 97px row *even though its children could
  shrink*. Measured: buttons at 44 each, `flex-shrink: 1`, `min-width: 36px`,
  and still a 6px overflow. `min-w-0` on the container is what released it.

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

### Serve with no-store, and trust screenshots over computed styles

`python3 -m http.server` sends no cache headers and browsers hold `scripts.js`
and `styles.css` hard. **Two separate "this is still wrong" reports in this
project were a stale asset, not a bug.**

The original remedy was to bump the port on every check. That worked, but it
made the dev URL a moving target — open tabs, bookmarks and anything mid-typed
pointed at a dead port, and Ahmed asked for it to stop. It was a symptom fix:
the problem was never the port, it was the missing headers.

`build/serve.py` sends `Cache-Control: no-store` and serves on **8000, fixed**.
A plain refresh is then always current, verified by editing `styles.css` and
reloading the same URL with no cache-buster. It also refuses to fall back to a
different port on its own — silently moving is the behaviour it exists to end.

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

### A CSS comment block was silently eating the rule after it

Found while adding the ghost styles. The scroll-reveal comment in `styles.css`
closed with `*/`, then carried four more lines of prose, then closed *again*.
Everything after the first `*/` parsed as a selector, and CSS error recovery
swallows a bad qualified rule **up to and including the next `{ }` block** — so
`.js-reveal [data-reveal] { opacity: 0 }`, the rule immediately following, was
being discarded. The reveals were running as a no-op fade-in from full opacity.
Fixed. Worth remembering that a broken comment does not fail loudly in CSS; it
quietly deletes its neighbour.

### A "selected" state must not be painted like a "hover" state

**Reported four times, across two different components.** Now a hard rule in
CLAUDE.md.

*The mega-menu column.* It marks the chosen category, and pointing at a
category is also what chooses it. With selection expressed as a **filled**
background (`#EDEFEB`), the fill stayed behind after the pointer left — so the
column permanently had one row that looked hovered, including the instant the
panel opened and nothing had been touched. An earlier pass tried making hover
and selected *different* fills, which did not help: the problem was never that
they matched, it was that selection was painted in the one visual language a
pointer owns. Now a wash means only "the pointer is here, right now", and
selection is the leading brand bar, the ink colour and the arrow.

*The primary nav underline.* Same bug, and it survived two rounds of me
measuring the wrong thing. Both earlier investigations found every underline at
`scaleX(0)` and concluded the navbar was fine — but they were run on the home
page, where **no category is current**. On a category page one tab carries a
solid `#DCC498` bar permanently, and it was drawn *pixel-identically* to the
hover bar. Nothing was stuck; "you are here" was simply written in the
pointer's handwriting.

Current is now a solid full-width brand bar; hover is a **thinner, half-opacity
white** bar. Neither can be mistaken for the other, and hovering the current
tab keeps the current treatment.

**Two lessons for whoever hits this next.** Reproduce a state-dependent bug on
a page where the state actually exists — a nav "active" bug is invisible on a
page with no active item. And when measuring hover states through the browser
pane, **park the pointer somewhere neutral first**: an automation cursor left
sitting over the nav reported a phantom stuck underline on a tab that was
simply under the mouse.

### Don't reach for `requestAnimationFrame` to kick off a transition

The standard "next frame" trick for starting a CSS transition does not fire in
a backgrounded tab, so the pick-up stage of the add-to-cart flight was skipped
entirely there — and worse, the class could land *after* the throw had already
removed it. `void el.offsetWidth` forces the style flush synchronously and has
no such dependency. This is also why the browser pane is a poor place to verify
mid-animation state: it reports `visibilityState: "hidden"`, so transitions are
registered but never tick.

---

## 9. Resolved

### Full-site UX pass, 2026-07-22

A scenario sweep over all 130 pages and every interactive flow. What it found
and what changed:

- **The checkout summary was static and contradicted the cart.** Its line
  items and totals were baked at build time, so a basket worth EGP 60 was
  checked out against a printed **EGP 322.50** beside two products the shopper
  had never added — while the cart drawer *on the same page* showed the right
  figure. It now carries the cart page's own hooks (`data-cart-lines`,
  `data-cart-subtotal`, `data-cart-total`, `data-cart-discount-row`), so
  `renderCart` owns every figure on both pages. `syncPointsUI`'s parallel
  `data-base-total` mechanism is gone with it — there was one renderer to keep
  correct instead of two to keep agreeing. Verified: cart and checkout now
  print the same subtotal and total for the same basket.

  **Deviation this introduces, flagged rather than silently taken:** reusing
  the cart's `cartLineHTML` means the checkout summary rows now carry a
  `−/n/+` stepper and `حذف`, where the Figma summary is read-only. Editing
  quantities at checkout is a common pattern and it is what makes a second
  renderer unnecessary — but it *is* a design change, and the alternative
  (a dedicated read-only checkout renderer) is exactly the duplicate-source
  problem that produced the EGP 322.50 in the first place. Designer's call.
- **Checkout let an empty basket through.** The cart page had disabled its CTA
  on an empty or below-minimum basket since the minimum-order work; checkout
  never got the same guard, so empty → checkout → thank-you was reachable. The
  CTA now carries `data-cart-checkout` and is gated by the same code path.
- **Site search did nothing at all.** The masthead magnifier opened a modal
  whose input only took focus — no handler, no results, no empty state — and
  whose five "الأكثر بحثاً" chips were all links to the same category page.
  Now a real client-side search (see §3 for the two deviations it introduces).
- **"أضف الجميع الى السلة" was a dead button.** The frequently-bought-together
  block's rows carried no product data, so `productFrom()` found no
  `[data-product]` host and the handler returned silently — the *same* defect
  the upsell rail had already been fixed for. Rows are now `[data-product]`
  hosts, the button has its own `data-bundle-add` handler (it adds several
  products, so it could never have gone through the single-product one), and
  the total answers the checkboxes instead of quoting a price for something
  you just declined. Verified: what the total promises is exactly what lands.
- **113 pages carried an empty `<h1></h1>`.** `page_header("")` is called by
  product, blog, account and auth pages, which title themselves further down.
  It emitted the heading anyway, so those pages had two h1s, the first silent.
  Now emitted only when there is a heading.
- **The home page had no `<h1>` at all** — its outline started at h2, because
  the hero is banner artwork. Given an `sr-only` h1.
- **Eleven pages skipped h1 → h3.** Account cards became h2 (they are the
  page's top-level sections); the listing grids, blog list and branch panels
  got `sr-only` h2s. The branch one doubles as the governorate name, which the
  tab button alone was not exposing to heading navigation.
- **No page had a skip link**, past a three-band header with a mega-menu.
- **Carousel dots failed WCAG 2.2 AA (2.5.8).** 10×10 controls with 8px gaps —
  centres 18px apart, so they failed both the 24px floor and the spacing
  exception that would otherwise excuse them. They now carry a transparent
  24×44 hit area (a `::before` overlay, not padding, which would have pushed
  the dots down). The `gap-2` utility had to come *off the markup* — it ties
  with `.carousel-dots` on specificity and won on emit order, the trap already
  documented in `CLAUDE.md`.

  **The gap and the dot size are one decision, not two.** What 2.5.8 actually
  constrains is the *centre-to-centre* distance: `dot width + gap >= 24`. That
  budget was first paid entirely out of the gap (10px dot, 14px gap) and read
  far too airy — Ahmed pushed back on exactly that. It is now paid out of the
  dot instead: **14px dot, 10px gap**, same 24px centres, same compliance, and
  a gap back near the original 8px feel. Do not tighten the gap again without
  widening the dot by the same amount. Verified by hit-testing rather than by
  computed style: 11px off-centre still hits (the 24px band), 20px above and
  below still hits (the 44px band), and 18px off-centre lands on the
  neighbouring dot — adjacent, with neither a dead zone nor an overlap.
- **Three controls had no focus indicator.** The global ring is on a
  `:where(...)` selector — zero specificity by design — so Tailwind's
  `outline-none` (0,1,0) beat it on the search box, the footer newsletter
  input and the listing sort select. Re-armed on selectors that outrank a
  single utility class. Any new `outline-none` needs the same treatment.
- **The password reveal was a 20×20 target**; now 44×44 around the same glyph.
- **No form field on the site had `autocomplete`.** A browser or password
  manager could not fill one box of the ten-field checkout. Tokens are now
  inferred from the field names in `components.py` (the names were already
  semantic), so a field cannot be added later without one. Register passes
  `new-password` so a manager offers to generate rather than fill.
- **No page had Open Graph, theme-color or canonical.** Storefront links get
  shared on WhatsApp constantly in Egypt and rendered as bare grey URLs.
  og:/twitter:/theme-color now ship on all 130 pages.
- **Three product names were damaged by the scrape** — see §1.
- The cart order-note textarea had a placeholder and no label.

**Empty cart, and a second ungated CTA (Ahmed, 2026-07-22).** The empty cart
was a bare centred `<p>` reading `سلتك فارغة.` — a dead end with nothing to
look at and nowhere to go. Rebuilt to the **same shape as the favourites
empty state** (glyph tile, heading, one supporting line, one CTA) reusing its
exact `تصفح المنتجات` label, so the build's two empty states read as one idea.
It renders in three containers now — drawer, cart page, checkout aside — and
is sized to survive a ~310px column; verified at 0 overflow in all three.

Fixing it surfaced the same defect class as the checkout CTA, on the cart page
itself: `أطلب الآن` (the big 332×54 primary) chose between a disabled
`<button>` and a live `<a>` **at build time**, from the seeded catalogue
subtotal, and then never changed. So it sat fully live over an empty basket
while the drawer's own smaller CTA beside it was correctly greyed out. The
shortfall warning had the same problem. Both are now always rendered and
gated at runtime by `data-cart-checkout` / `data-cart-warning` +
`data-cart-shortfall`. `MIN_ORDER` left `cart.py` with them — the minimum is a
runtime rule, so `scripts.js` holds the only copy rather than two that can
drift. Verified across all three states: empty → both CTAs blocked, warning
hidden; EGP 72.50 → both blocked, warning shows EGP 77.50 remaining; EGP
292.50 → both live, warning hidden.

**Not** a regression, though it looked like one twice, and both are traps for
whoever tests next:

- The **cart badge froze at a stale number** and a `.fly-ghost` stranded in the
  DOM — reproducible only while the automation pane reports `0×0` and
  `visibilityState: "hidden"`. In a correctly-sized frame the badge stayed in
  sync through rapid clicks, off-screen sources and a scroll mid-flight. With
  `innerHeight === 0` the flight's destination clamp degenerates. Measure
  interactions inside a **sized iframe**, never the top-level automation pane.
- The **sweep reported 110 contrast failures** in the injected chrome. The
  Play CDN does not generate utilities for scripts.js-injected markup inside
  an offscreen iframe, so `text-white` never applied and every footer link
  read as dark-on-dark. In the real document it is white on `#062B1C`. The old
  "0 failures" baseline was 0 partly because the footer had not been injected
  yet at 140ms. **The sweep can only speak for build-time markup** — scope it
  to `main` and check the chrome in a real page.

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
