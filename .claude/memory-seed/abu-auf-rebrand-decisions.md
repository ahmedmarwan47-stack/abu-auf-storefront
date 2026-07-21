---
name: abu-auf-rebrand-decisions
description: Locked scope decisions for rebranding the OrderBase/Koueider static export into Abu Auf
metadata: 
  node_type: memory
  type: project
  originSessionId: b67875d9-f07b-4d28-ac77-3ca0f2c20ad5
  modified: 2026-07-21T08:24:50.629Z
---

The `order-base-ecommerce` project rebrands a 29-page static export of the
OrderBase/Koueider storefront into **Abu Auf** (abuauf.com). Decisions agreed
2026-07-21, before implementation started:

- **Fidelity:** rebuild pages against the Abu Auf Figma designs page by page —
  not a colour reskin. Chosen because the Figma covers ~all 29 routes and the
  Arabic RTL flip rewrites layout everywhere regardless.
- **Language:** Arabic-first, `dir="rtl"` default. Not bilingual.
- **Copy:** real Abu Auf content, not placeholder.
- **Imagery:** majority scraped from abuauf.com; a minority exported from Figma.
- **Responsive:** desktop first against the Figma `Web` page; a dedicated mobile
  pass against the Figma `Mobile` page comes after desktop is signed off.
- **Working style:** edit `static-export/` in place, with git as the undo. The
  repo was initialised for this project; commit `f4dde89` is the pristine
  Koueider baseline.

Source of truth for design tokens is the Figma **variables**, not eyeballed
hexes. See [[abu-auf-asset-sources]].
