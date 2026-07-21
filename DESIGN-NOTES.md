# Abu Auf rebuild — design & accessibility notes

Notes from building the static export against the Abu Auf Figma
(`tQiydoANmIdYWq0IfmTsMz`).

## Colour contrast — FIXED, and it diverges from the Figma

**The build now passes WCAG 2.1 AA everywhere** (4.5:1 body, 3:1 large text).
Achieving that required deviating from the Figma in the places listed below.
**The designer should be told**, because the Figma is still the failing version.

Verified live in-browser (computed styles, not theory) — 0 failures across
`index` (206 text nodes), `checkout` (109), `my-account` (154) and
`shop-category` (148).

| Where | Figma | Ratio | Now | Ratio |
|-------|-------|-------|-----|-------|
| Footer column headings + HQ address | `#185039` on `#062B1C` | **1.64:1** | `onDarkGreen #7FA894` | 5.79:1 |
| Secondary text everywhere (546 uses) | `#777777` | 4.48 / 3.87 / 3.39 on white / base / beige | `neutral.secondary #5F5F5F` | 6.39 / 5.52 / 4.83 |
| Legal-bar text on black | — | — | `onBlack #949494` | 6.92:1 |
| Newsletter placeholder on beige | `#ABA08F` | **1.95:1** | `onBeigeMuted #6B6255` | 4.54:1 |
| Utility-bar links on beige | `text-white` (bug) | **1.32:1** | `#5F5035` | 5.92:1 |
| Tab buttons | `#777777` | 4.48:1 | `#5F5F5F` | 6.39:1 |
| Mobile drawer links | `#868685` / `#bbbbbb` | 3.64 / 1.92 | `neutral.secondary` | 6.39:1 |
| Breadcrumb `/` separators | `#C6C6C6` | 1.71:1 | `aria-hidden` + `neutral.outline` | decorative |

Two of those were **my own bugs**, not the Figma's: the utility-bar links kept
`text-white` from the old navy bar after I recoloured it beige (invisible text),
and `.tab-btn` in `styles.css` hardcoded `#777777` instead of using the token.

### Gotcha worth knowing

`neutral.secondary` is tuned for **light** surfaces and inverts badly on black
(3.29:1) — that is why `onBlack` exists as a separate token. Don't reuse
`text-neutral-secondary` on dark backgrounds.

### Tailwind Play CDN gotcha

A nested colour key containing a hyphen — e.g. `primary["on-dark"]` — does
**not** produce a usable class. `text-primary-on-dark` is ambiguous between
colour name and shade, so it silently resolves to nothing and the element falls
back to the inherited body colour. This cost a debugging cycle: the ratios were
correct on paper while the browser was still painting the old colour. The
accessibility tokens are therefore **flat** (`onDarkGreen`, `onBlack`,
`onBeigeMuted`). Always verify colour changes with computed styles in the
browser, not by reading the config.

## Content gaps — needs client copy before launch

Everything below is written in-house in Abu Auf's voice and product categories.
It is plausible and on-brand, but it is **not** the client's approved copy.

| Where | Status |
|-------|--------|
| FAQs (`build/pages/faqs.py`) | 9 Q&As written in-house. Delivery times, minimum order (100 EGP) and the 14-day return window are **assumptions** — confirm before launch. |
| Legal pages (privacy, terms, return policy) | Written in-house. **Must be replaced with the client's legal text** — do not launch on these. |
| Blog & recipes (`build/pages/_posts.py`) | 6 posts written in-house; the live blog is client-rendered so its Arabic copy is not scrapable. |
| Reviews on the home page | 4 invented testimonials with invented names. Real reviews exist at `/apis/v2/get-all` (rating + author, English) if you want them wired up. |
| Account pages | Sample customer "محمد عادل", order numbers and wallet balances are illustrative. |

Also outstanding:

- **"صحارة ديلايتس" promo section** (Figma `753:34833`) is omitted from the home
  page pending that sub-brand's logo and product assets.
- **Branch titles are English.** `ar_title` is blank for every branch in the
  client's CMS, so `branches.html` shows the English name with the Arabic
  address. Presented as-is rather than machine-translated.

## Resolved

- **Arabic product names — solved.** The WooCommerce Store API only ever returns
  English names (`?lang=ar`, `Accept-Language: ar` and `X-WPML-Language: ar` all
  return English). But the Arabic storefront *server-renders* names into its
  Next.js RSC flight payload at `https://www.abuauf.com/ar/category/<slug>`,
  keyed by the same product slug the Store API returns. Category routes only
  render their first page, so the remainder were fetched per product from
  `/ar/products/<slug>`. Coverage is now **99/99**, stored as `nameAr` in
  `static-export/data/catalog.json`. Scripts:
  `fetch_arabic_names.py` and `fill_missing_names.py`.
  Note the site's public routes are `/ar/category/<slug>` and
  `/ar/products/<slug>` — **not** `/product-category/…`, which 404s.

- **Live site vs Figma — HQ address differs.** The Figma footer says "المنطقة
  الصناعية 31-33، التجمع الثالث، القاهرة الجديدة، مصر"; the live site says
  "مبني 05 B ميدهاوس ، الحرم الجامعي ، المنطقة الخامسة - طريق السخنة" and also
  shows a tax number. The build currently uses the Figma address. Worth
  confirming which is current before launch.

## Figma export quirks worth knowing

- The **logo** exports pre-flipped: its Figma wrapper carries
  `-rotate-180 -scale-x-100` (a net vertical flip) plus
  `preserveAspectRatio="none"`. Raw, it renders upside down and stretched. The
  flip is baked into `images/abuauf/brand/logo-abuauf-white.svg`.
- The footer payment strip's first mark is **Etisalat Cash**, not Meeza, and
  ships as white artwork on an opaque black plate — it must not be placed on a
  white chip.
- The Figma footer carries a **"Web Design by MITCH DESIGNS"** credit. Retained
  at the client's request.

## Mobile pass — deviations from the Figma `Mobile` page

The account shell is built from `Account > Overview` (`383:33392`) and
`Account > menu bottom sheet` (`973:47270`). Two intentional divergences:

- **The sheet lists seven nav rows; the Figma draws six.** The Figma omits
  `نقاطي`, but `my-account-point.html` exists and is reachable from the desktop
  sidebar. Both the sidebar and the sheet render from the single `NAV` list in
  `build/pages/_account.py`, so dropping it from the sheet would have meant
  hard-coding a second, divergent list. Flagging rather than silently
  reconciling: **ask the designer whether `نقاطي` is being retired**, and if so
  remove the page, not just the row.
- **`تأكيد` closes the sheet; it does not confirm a selection.** In the Figma
  the rows look selectable with `تأكيد` committing the choice. Here each row is
  a plain link that navigates on tap, which is the standard pattern and keeps
  the sheet keyboard- and screen-reader-navigable. `تأكيد` is retained for
  visual fidelity but is a dismiss. Worth confirming the designer intended
  select-then-confirm rather than tap-to-navigate.

### Duplicate frames on the Figma `Mobile` page

Several routes have more than one frame — two `Home`, four `Collection`, two
`Cart`, two `Product`, three `Account > Wallet`, two `Checkout > Info`. Nothing
marks which is current. Any page built against one of these needs the canonical
frame confirmed first.

### Canonical frame choices (duplicates resolved by "most built-out")

Ahmed's call: where the `Mobile` page has duplicates, build against the most
built-out frame and record the choice here. Each is an inference from
completeness, **not** confirmation from the designer — worth a check before
launch.

| Route | Chosen | Passed over | Basis |
|---|---|---|---|
| Product | `918:34326` (4723px) | `350:25883` (4038px) | 685px more content; includes the FBT block |
| Cart | `804:32907` (3007px) | `359:18661` (2786px) | 221px more content |
| Home | `2595:60104` | `753:30987` | **Confirmed by Ahmed**, not inferred |

`Home` could not be resolved by completeness — both frames are exactly
12361.52px tall. Ahmed supplied `2595:60104` directly, so that one is settled
rather than assumed.

`Collection` has four frames (`350:17805`, `1290:41915`, `1002:40281`,
`973:48168`), two of them identical at 2593px. Still unresolved — no listing
page has been built against a mobile frame yet.

### Product page — price display deviates from the Figma

The Figma product frame shows a struck-through original (`EGP55.99`) beside a
discounted price in an `EGP` badge. The build renders a single yellow price
chip, because `catalog.json` carries one price per product with no compare-at
field. Showing a fake "was" price would be inventing data. Needs either a real
sale price in the catalogue or the designer's sign-off on the single-price
treatment.

### Listing pages — mobile filter treatment

Figma `Collection` `350:17805` (confirmed by Ahmed; four frames exist, two of
them identical at 2593px, so completeness could not pick one).

Mobile diverges from desktop in two ways, so both are carried rather than one
replacing the other:

- **Inactive chips** are filled with interaction-base and lose their outline;
  desktop keeps white-on-outline.
- **The sort control** is bare — a sort glyph plus the current value, no
  chrome and no `ترتيب حسب` prefix. Desktop keeps the outlined pill and label.

The chip rule lives in `styles.css` under a media query, not as
`bg-interaction-base xl:bg-white`. The Play CDN did not apply the `xl:` variant
to these anchors: an identical probe element created at runtime resolved to
white at 1440 while the chips themselves stayed filled. `a.chip-filter`
(0,1,1) outranks Tailwind's `.bg-white` (0,1,0), so the authored rule wins
regardless of what the CDN emits or in what order.

**Caution for whoever verifies this next:** `getComputedStyle` read from the
top-level document after a viewport resize returned stale values here — a
no-media `!important` rule appeared to have no effect, which is impossible.
Screenshots and same-origin iframe measurements were both accurate. Prefer
those; if computed styles contradict a screenshot, distrust the computed style.

### Checkout — mobile ordering, and one gap

Figma `Checkout > Info` `753:36339` (2554px), taken over `753:34950` (2242px)
per the most-built-out rule. Inferred from completeness, not confirmed.

The Figma puts the order summary **between** the page header and the form body
on mobile. That was impossible while the `h1` and step nav lived inside the form
column, so the header is now its own grid item spanning both columns at `lg`.
Desktop is unchanged — every `order` resets at `lg` and the header row is short
and right-aligned, so it occupies the same visual position as before.

**Not implemented: the summary is collapsible in the Figma.** The mobile frame
shows a chevron on `ملخص السلة`, so it opens and closes; the build renders it
always-expanded with a `تعديل` link instead. Making it collapse on mobile while
staying static on desktop is a behavioural change, not a layout one, so it is
flagged rather than guessed at. Worth asking whether the collapse is required or
whether always-visible is acceptable — on a checkout page, hiding the total
behind a tap is a real conversion decision, not just a styling one.

### Auth pages — form leads on mobile

Figma `Account Sign In/ Create Account` `368:21314`. The create-account panel is
DOM-first so RTL puts it in the right column at `lg`; the mobile frame leads
with the sign-in form, so below `lg` the panel moves to the end. Social buttons
reordered to Google-then-Facebook to match the frame. Covers all four pages
built on `_auth.py`.

### Branches — two Figma elements are blocked on missing data

Figma `426:33692`. The governorate filters now render as pills below xl,
scoped via `.tabs-chips` because `.tab-btn` is shared with the home page.

**Not built, and not fakeable:**

- **Per-branch phone numbers.** The frame shows a phone row on every card.
  `branches.json` has a `phone` field on all 316 branches and **every one of
  them is empty** — the client's CMS has never populated it. Inventing numbers
  for real retail locations would send customers to wrong numbers, so the row
  is omitted entirely rather than filled with placeholders.
- **`اتجاهات` (directions) links.** Need coordinates or Maps URLs per branch;
  `branches.json` carries only `title`, `slug`, `address` and the empty
  `phone`. Nothing to link to.

Both need the client to populate the CMS. Until then these cards will not match
the frame, and that is the correct outcome — the alternative is a store locator
that lies. The card badges (`فرع أبو عوف`, `متاح توصيل`) are also absent for
the same reason: no field distinguishes branch type or delivery availability.

## Listing filters — now real, and what still cannot filter

Previously every category chip on `shop.html` and every `/shop/<slug>` route in
the nav resolved to `shop-category.html`, which shows **coffee** whatever you
picked. Tapping `المكسرات` in the navbar showed coffee. This was not a styling
bug; the controls were tappable and did the wrong thing.

**Now working, off real catalogue data:**

- Category chips filter the grid client-side over the cards already in the DOM
  (no fetch, still works from `file://`). Verified: all 9 chips return only
  their own category, with counts matching `catalog.json` exactly — 12 / 8 / 12
  / 12 / 8 / 12 / 8 / 11.
- `/shop/<slug>` nav routes open `shop.html#<slug>`, pre-filtered. Distinct nav
  destinations went from 1 to 14. Sub-category routes fall back to their parent
  via `MAIN_MENU`, so `/shop/turkish-coffee` lands on coffee rather than
  nowhere.
- Sorting: price low→high and high→low sort on the real `price`/`sale` field.

**Sort options that are not what their label claims:**

| Option | Reality |
|---|---|
| `السعر: من الأقل` / `من الأعلى` | real — sorts on price |
| `وصل حديثاً` | sorts by product **id** descending. WooCommerce ids rise over time so this approximates recency, but the catalogue carries **no publish date** — it is a proxy, not a fact |
| `الأكثر مبيعاً` | **does nothing** — restores catalogue order. There is no sales data in `catalog.json`. It is the default, so the page looks correct, but it is not ranking by popularity |

Getting these honest needs `date_created` and a sales/popularity figure in the
scraped catalogue.

**Sub-category chips on `shop-category.html` still do not filter.** They are
deliberately left as plain links. `catalog.json` has `category` / `categorySlug`
and **no sub-category field**, and the seven labels come from the Figma, not the
data. Checked against the 12 real coffee products: `القهوة`, `قهوة مطحونة طازجة`,
`إسبريسو` and `مشروبات ساخنة` match **zero** products each. Wiring them would
empty the grid on four of seven taps, which is worse than not filtering. Needs
the client's sub-category taxonomy.

## Tap targets

Audited every interactive control at 390×844 against the 44px minimum (WCAG
2.5.5 / HIG). Before: the hamburger was **32×30**, the location bar 38px, filter
chips 38px, and 10 of 18 mobile-drawer items under 44. All now pass, verified by
hit-testing each control's centre point after scrolling it into view.

Two nav items go nowhere real: `المكافآت` and `منتجات أبو عوف خارج مصر` both
fall through to `index.html`, because `/rewards` and `/export` were never built.
The Figma has frames for both (`973:40830`, `426:29955`). Until they exist, those
two nav entries silently return the user to the homepage.

## Viewport coverage

Swept all 29 pages at **320 / 360 / 375 / 390 / 414** px. Clean at every width,
0 contrast failures (3871 text nodes). 320px needed two fixes to the recipe
card — `min-w-0` on the text column beside its fixed 160px image, then
`break-words` on the heading once the column could actually shrink.

### Location picker — sheet on phones, dialog on desktop

The location overlay was a bottom sheet at every width, including 1440px, where
a full-width panel pinned to the bottom edge reads as a mobile pattern dropped
into a desktop window. The live site opens it as a popup there.

`.bottom-sheet--modal` now switches it to a centred dialog from xl: 420px wide,
22px radius, fade-and-scale instead of slide-up, drag handle hidden (it means
nothing once the panel is not draggable). Below xl it is unchanged — full
width, pinned to the bottom, handle visible.

Centring uses `inset-inline: 0` + `margin-inline: auto` rather than
`left`/`right`, so it holds in RTL. The modifier is on the location sheet only;
the account menu sheet stays a sheet because it is `lg:hidden` and never
appears on desktop.

## Products dropdown and cart drawer — matched to the live site

Both built from screenshots of the live abuauf.com that Ahmed supplied.

### Products dropdown (desktop)

`المنتجات` opened the **mobile side drawer** at every width. The live site opens
a full-width dropdown under the button on desktop. There is now a three-column
panel in RTL order — categories, the active category's sub-categories, a
product rail — that opens on click, switches column two on hover or focus, and
closes on outside click or Escape. Phones are unchanged: the drawer is still
the right control there, and the panel is `hidden lg:block`.

**`الاكثر مبيعا` in column three is not ranked by sales.** It is four real
catalogue items, hard-coded, because `scripts.js` has no access to
`catalog.json` at runtime by design (no fetch — pages must work from
`file://`). Same underlying gap as the `الأكثر مبيعاً` sort option: there is no
sales data anywhere in the scrape. Swap these for a real best-seller list once
the client provides one.

### Cart drawer

Rebuilt to match: price chip per line, `العدد`, a 44px stepper, `حذف`, a
`قد يعجبك أيضا` upsell block, delivery-fee line, and the split
`عرض السلة` / `اتمام الشراء` footer.

Figures mirror `build/pages/cart.py` — `DELIVERY_FEE = 10`, `MIN_ORDER = 100` —
so the drawer and the cart page can never quote different numbers. **Both are
our assumptions and both disagree with the live site**, which shows a 30 EGP
delivery fee and a shortfall implying a 150 EGP minimum (40 in cart, 110
remaining). Worth confirming the real figures and changing them in one place.

**The below-minimum state is not visible in the demo.** The disabled
`اتمام الشراء` and the shortfall warning are implemented and mirror the cart
page's logic, but the sample cart totals 292.50 against a 100 minimum, so the
branch never renders. To see it, lower the demo quantities or raise
`MIN_ORDER`.

### A CSS trap worth knowing

The `hidden` attribute only sets `display:none` through the UA stylesheet, so
**any** author display rule beats it — an element carrying both `hidden` and
Tailwind's `.flex` stays visible. All eight sub-category lists rendered stacked
on top of each other until `[hidden] { display: none !important; }` went into
`styles.css`. Anything in this codebase toggling the `hidden` attribute on a
flex or grid element depends on that rule.

## Header, CTA band and footer resized against the live site

These were noticeably taller than abuauf.com. Rather than eyeball the
screenshots, the live site was opened in the browser and measured directly at
1920px. Targets and results:

| Band | Live | Was | Now |
|---|---|---|---|
| Utility bar | 33 | 36 | 33 |
| Masthead | 79 | 100 | 79 |
| Nav row | 48 | 54 | 48 |
| **Header total** | **161** | **190** | **160** |
| CTA band | 306 | 317 | 305 |
| Footer body | 458 | 494 | 462 |
| **Footer total** | **764** | **811** | **767** |

The masthead pills (`المنتجات`, delivery, account) dropped from `py-[18px]` to
`py-3` so they still fit the shorter bar.

## Language switcher — real direction toggle, not a translation

Replicated from the live site, measured not guessed: a 288px panel headed
`اللغة` with `English` and `العربية` rows, a flag per row and a check on the
active one. Choice persists in `localStorage` across pages.

**It flips `dir` and `lang` on `<html>`, and nothing else.** That makes the
RTL↔LTR layout genuinely testable — logical properties, mirrored components
and text alignment all flip, verified across pages — but the copy stays
Arabic.

This is deliberate. Every string in this build is Arabic; there is no English
content to switch to, and machine-translating a client's storefront would be
inventing copy on their behalf. Note this also brushes against a recorded
client decision: HANDOFF §2 has **"Arabic-first, not bilingual"** as an
explicit choice, on the grounds that the live site is Arabic-only. The toggle
does not reverse that — it is a test harness for direction.

**Real bilingual support is a separate, much larger piece of work** and needs,
at minimum: English copy for every page, English UI strings for the chrome in
`scripts.js`, and a decision on URL strategy (`/en/` routes vs a runtime
switch). English product names already exist in `catalog.json` as `name`, so
the catalogue is the one part already covered.

## Cart is now real state, not markup

Before this, `[data-add-to-cart]` had **no handler at all** — clicking "اضف الى
السلة" anywhere did nothing — and the steppers only incremented a number in the
DOM. The drawer and cart page were hard-coded HTML.

There is now a cart store in `scripts.js`, exposed as `window.abuaufCart`:

```js
abuaufCart.items()            // [{id, name, price, image, qty}]
abuaufCart.add(product, qty)  // merges quantity if the id is already in
abuaufCart.setQty(id, qty)    // qty < 1 removes the line
abuaufCart.remove(id)
abuaufCart.clear()
abuaufCart.count()            // total units
abuaufCart.subtotal()         // EGP
abuaufCart.find(id)
```

State persists in `localStorage` under `abuauf:cart`, so it survives navigation
between the standalone pages. No fetch — product details are read straight off
`[data-product]` markup (`data-id/-name/-price/-image` on every product card and
the product page), so it still works from `file://`.

### The hook for micro-interactions

Every mutation dispatches `cart:change` on `document`:

```js
document.addEventListener("cart:change", (e) => {
  e.detail.reason    // "add" | "qty" | "remove" | "clear" | "init"
  e.detail.product   // the item involved (null for clear/init)
  e.detail.items     // full array after the change
  e.detail.count
  e.detail.subtotal
});
```

**The renderer is a keyed reconcile, not an `innerHTML` swap.** This matters:
replacing the list wholesale destroys nodes mid-transition and drops focus,
which makes row-level animation impossible. Rows that survive a change keep
their DOM node and any state on it — verified by tagging a row, changing its
quantity, and confirming the same node and the custom attribute survived. Only
genuinely new or removed rows are created or detached.

One consequence worth knowing when you build exit animations: `remove()` detaches
the node as part of the same render. If you want a row to animate out, animate
first and call `remove()` on completion.

### Seeding

A first-ever visit (no `abuauf:cart` key) seeds two real catalogue items so a
fresh browser doesn't land on an empty cart. An **empty array** is respected as
a shopper who deliberately emptied their cart, and is never re-seeded.

Server-rendered cart rows carry `data-cart-static` and are cleared the first
time the store paints, so the page is not blank without JS but never shows
duplicates with it.

## Content width now matches the live site (1536px)

Measured on abuauf.com: both the utility bar and the masthead sit in a
`container mx-auto max-w-screen-2xl` = **1536px**, with the coloured bars
full-bleed behind them.

Ours used `max-w-[1920px]` with `xl:px-[190px]`. That coincidentally lands near
1536 at a 1920 viewport, but is wrong everywhere else — at 1440 it gave a
1060px content column against the live site's ~1408. The header and nav rows had
no max-width at all and ran to 1745px.

All 36 container declarations across `build/` and `scripts.js` are now
`mx-auto px-4 max-w-[1536px]`, and the masthead and nav rows are constrained to
1536 too. Verified at 1920: every content container 1536, masthead 1536, nav
1536.

## Cart and search buttons unified

The cart button was `size-[60px]` next to a `size-12` search button. The live
site has both at **48×48**; ours now match, with the glyph and count badge
scaled to suit.

## Language panel stacking

The panel opened *behind* the nav bar. The utility bar that hosts it was
`z-40` while the masthead was also `z-40` and later in the DOM, so the masthead
and its nav painted over the panel. The utility bar is now `z-50`. Verified by
hit-testing a point near the panel's bottom edge — the panel is what is on top.

**If you add another header layer, keep the order:** utility bar `z-50` >
masthead `z-40` > nav `z-30`. Anything that opens a dropdown must live in a bar
above whatever it needs to overlap.

## Note on verifying: use a fresh port

`python3 -m http.server` sends no cache headers, so browsers hold on to
`scripts.js` and `styles.css` hard. Several "this still looks wrong" moments in
this project have turned out to be a stale port or a cached asset. Always bump
the port when checking a CSS/JS change, and confirm what the server is actually
rooted at.

## Chrome typography corrected against the live site

Ahmed asked whether the resized bands actually matched *inside* — fonts and
icons, not just heights. Probing both sites at 1920 found they did not:

| Element | Live | Was | Now |
|---|---|---|---|
| Nav row links | 16px / 600 | **20px** | 16 / 600 |
| Masthead pills (`المنتجات`, delivery, account) | 16px | **20px** | 16px |
| Footer column links | 16px / 400 | **20px / 600** | 16 / 400 |
| Utility bar links | 13px / 600 | 14 / 500 | 13 / 600 |
| Footer logo | 180×46 | 150×50 | 180×46 |
| Hotline | 36px | 32px | 36px |
| Newsletter field | has a mail glyph | **missing** | added |

The bands were the right *height* but the type inside was a size too large
throughout, which is why they still read as heavier. Footer padding went back to
`xl:py-12` once the links shrank; final: header 160 (live 161), footer 767
(live 764), CTA band 305 (live 306).

## Language switching — what it now does

`t()` maps chrome strings to English, keyed by the Arabic original. Choosing a
language re-renders the JS-injected header, footer and overlays, so nav,
masthead, utility links, footer columns and cart chrome all switch — and
product titles swap to `catalog.json`'s real English `name`.

**What is still Arabic in English mode, and why:**

- **All page body copy** — headings, intros, FAQ answers, legal text, blog
  posts, form labels and the build-time buttons on cards. It is baked at build
  time and there is no English source. Machine-translating a client's storefront
  would be inventing content on their behalf.
- Translating it properly means either English copy for all 29 pages, or a
  build that emits `/en/` variants. Either is a real project, not a toggle.

**The English chrome strings in `EN` are placeholder**, written in-house as
standard commerce terminology (`Offers & Discounts`, `Checkout`, `View cart`).
They are not the client's approved wording and need sign-off — the same status
as the FAQ figures and legal text. Product names are the exception: those come
from the catalogue and are real.
