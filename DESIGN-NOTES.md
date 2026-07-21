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
