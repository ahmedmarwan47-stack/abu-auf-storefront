---
name: abu-auf-build-system
description: "How the Abu Auf static export is edited — two layers, runtime vs build-time components"
metadata: 
  node_type: memory
  type: project
  originSessionId: b67875d9-f07b-4d28-ac77-3ca0f2c20ad5
  modified: 2026-07-21T10:03:18.548Z
---

The Abu Auf export has **two editing layers**. Ahmed explicitly asked that
tweaks reflect site-wide, so respect this split:

1. **Runtime — no rebuild.** `static-export/tw-config.js` (design tokens),
   `static-export/scripts.js` (header, footer, cart drawer, search, mobile
   menu, all behaviour), `static-export/styles.css`. Editing these updates
   every page on refresh.
2. **Build-time components.** `build/components.py` is the single source of
   truth for cross-page markup; `build/catalog.py` for data access;
   `build/pages/<name>.py` one per page, with `_`-prefixed modules being
   shared layouts (`_listing`, `_auth`, `_account`, `_legal`, `_geo`,
   `_posts`). Run `python3 build/build.py` to regenerate all 29 pages — it
   fails loudly on unresolved asset references.

Never hand-edit the generated `.html` files — the next build overwrites them.

Local Python is **3.9**: f-strings there reject backslashes in the expression
part. Data lives in `static-export/data/catalog.json` (99 products with
`nameAr`) and `branches.json` (316 branches).

See [[abu-auf-rebrand-decisions]] and [[abu-auf-asset-sources]].
