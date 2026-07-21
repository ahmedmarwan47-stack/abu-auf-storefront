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
