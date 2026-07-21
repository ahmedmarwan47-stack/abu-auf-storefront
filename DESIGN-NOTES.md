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

- **Product names are English only.** The public WooCommerce Store API returns
  English `name` values for every product; `?lang=ar`, `Accept-Language: ar` and
  `X-WPML-Language: ar` all return the same. The live storefront is a
  client-rendered Next.js app, so the Arabic names are not in its served HTML
  either. The Arabic set exists somewhere (the live site displays it) but is not
  publicly reachable. Currently the build shows the real English names on an
  otherwise fully Arabic page. **Needs a decision** — see the project README
  discussion or ask the client for a name export.

- **"صحارة ديلايتس" promo section** (Figma `753:34833`) is omitted from the home
  page pending that sub-brand's logo and product assets.

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
