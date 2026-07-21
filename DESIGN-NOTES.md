# Abu Auf rebuild — design & accessibility notes

Running list of issues found while building the static export against the
Abu Auf Figma (`tQiydoANmIdYWq0IfmTsMz`). **The build matches the Figma in every
case below** — nothing here has been silently "fixed". These are for the
designer to rule on.

## Colour contrast

WCAG 2.1 AA requires 4.5:1 for body text and 3:1 for large text (≥24px, or
≥19px bold).

| # | Where | Foreground | Background | Ratio | Verdict |
|---|-------|-----------|------------|-------|---------|
| 1 | Footer HQ address | `#185039` Primary/Green | `#062B1C` footer green | ~1.4:1 | **Fails badly.** Body-size text, effectively unreadable. |
| 2 | Footer column headings ("أقسام المنتجات", "عن الشركة", "المساعدة") | `#185039` | `#062B1C` | ~1.4:1 | **Fails.** Same pairing; these are 16px bold. |
| 3 | Footer legal / copyright | `#777777` Interaction/Secondary Text | `#000000` | ~4.4:1 | Marginal — just under 4.5:1 at 16px. |
| 4 | Utility bar links | `#5F5035` | `#E8DFD0` Primary/Beige | ~5.6:1 | Passes. |

**Recommendation for 1 and 2:** lift the green to roughly `#7FA894` (≈4.6:1 on
`#062B1C`), or use `Primary/Beige #E8DFD0` at reduced opacity. Either keeps the
green-family look while becoming legible. Needs a designer decision because it
changes a token pairing used across the footer on every page.

## Content gaps

- **"صحارة ديلايتس" promo section** (Figma `753:34833`) is omitted from the home
  page pending that sub-brand's logo and product assets.

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
