---
name: abu-auf-asset-sources
description: "Where Abu Auf design tokens, components, imagery and catalog data are pulled from"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b67875d9-f07b-4d28-ac77-3ca0f2c20ad5
  modified: 2026-07-21T08:25:06.547Z
---

Verified working sources for the Abu Auf rebrand (see [[abu-auf-rebrand-decisions]]):

- **Figma file** `tQiydoANmIdYWq0IfmTsMz` — reachable via the Figma MCP. Pages:
  `162:4801` Web (~50 full page designs, covers all 29 routes), `3487:22749`
  Home - Products, `821:44658` Mobile, `56:2095` Components, `0:1` Draft + Old.
  Components page has 17 sections including Header `150:7367`, Footer
  `821:44659`, Icons `155:3517`, Social Icons `4839:34284`.
  Web home frame is `4842:55826`; web header frame is `5061:24238`.
- **Design tokens** — `get_variable_defs` on any node returns the bound
  variables. Core: Primary/Green `#185039`, Interaction/Primary CTA `#163300`,
  Primary Hover `#185039`, Accent/Secondary Yellow `#EDC843`, Primary/Beige
  `#E8DFD0`, Interaction/Base `#EDEFEB`. Arabic face is **Baloo Bhaijaan 2**,
  Latin is **Inter** — both on Google Fonts.
- **Imagery** — `backend.abuauf.com/wp-content/uploads/...` serves directly over
  plain curl with a browser UA. No auth.
- **Catalog** — WooCommerce Store API at
  `backend.abuauf.com/wp-json/wc/store/v1/products` and `/products/categories`
  is public, no auth. Prices are in **minor units** (`45000` = 450.00 EGP) and
  product names come back **English only**; `?lang=ar` does not translate them.
  Arabic product names must be scraped from the `www.abuauf.com` storefront HTML.

Note: the Koueider export and the Abu Auf Figma share design-system lineage —
`#A8200D` error, `#346853` green, `#D9D9D9` divider, `#C6C6C6` disabled,
`#777777` secondary, `#868685` outline are identical in both.
