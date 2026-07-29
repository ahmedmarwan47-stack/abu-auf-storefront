# Handoff — Abu Auf static storefront

Everything a fresh session (or a human) needs to continue this work without
re-deriving it or undoing it. `CLAUDE.md` is the short operating brief and loads
automatically; `DESIGN-NOTES.md` is the register of deviations, placeholders and
open questions. This file is the reasoning behind both.

---

## 1. Where the project stands

A 29-page static export of the **Koueider** storefront was rebranded to
**Abu Auf**, rebuilt page by page against the Abu Auf Figma, then given a full
mobile pass and a working commerce layer.

| | |
|---|---|
| Pages | 31 core + 99 generated product pages (`product-<id>.html`, one per product) |
| Koueider references | zero, verified across every file |
| Products | 99, real names (Arabic + English), prices, images |
| Product copy | client's own Arabic description + benefits on 97 / 99 (`fetch_descriptions.py`) |
| Product photography | 296 real gallery shots; 73 / 99 have a multi-shot gallery |
| Best-seller signal | real popularity rank for all 99, against the client's 653-product store |
| Size options | real multi-size SKUs with real prices; 10 / 99 products have them |
| Branches | 316 across 25 governorates, real |
| Accessibility | WCAG 2.1 AA, 0 failures across all 31 pages; tap targets ≥44px |
| Responsive | verified clean at 320 / 360 / 375 / 390 / 414 |
| Cart | real state, persisted, with an event API |
| Favourites | real state, persisted, with an event API |
| Filters / nav routes | genuinely functional over real catalogue data |
| Language | direction + chrome + UI strings switch; prose does not (by design) |
| Baseline commit | `f4dde89` — the pristine Koueider export, for diffing |

---

## 2. Decisions the client made — do not silently reverse these

Each was an explicit answer from Ahmed, not an assumption.

| Decision | Choice | Why it matters |
|---|---|---|
| **Fidelity** | Rebuild against Figma page by page — *not* a colour reskin | The Figma covers ~all 29 original routes, and the RTL flip rewrote layout anyway |
| **Language** | Arabic-first, `dir="rtl"` default. Not bilingual | Matches the live abuauf.com, which is Arabic-only. The language toggle added later is a direction/UI test harness, **not** a reversal — see §6 |
| **Copy** | Real Abu Auf content wherever reachable | Not placeholder-by-default |
| **Imagery** | Majority scraped from abuauf.com; minority from Figma | Client confirmed rights |
| **Responsive** | Desktop first, then a dedicated mobile pass | Mobile pass is now **done** |
| **Components** | Shared, so a tweak reflects site-wide | Ahmed asked for explicit confirmation — treat as a hard requirement |
| **Agency credit** | **Keep** "Web Design by MITCH DESIGNS" | I removed it once; Ahmed asked for it back. Don't remove it again |
| **Contrast** | **Fix it**, diverging from the Figma | Originally flagged-but-preserved; Ahmed asked for them fixed |
| **Live site over Figma** | Where abuauf.com and the Figma disagree on chrome, match the live site | Ahmed supplied live screenshots and asked for parity |
| **Canonical Figma frames** | Where the `Mobile` page has duplicates, use the most built-out and flag the choice | Ahmed's call. He confirmed `Home` and `Collection` directly |
| **Workflow** | Straight through, one commit per page/batch | So any change can be reviewed or reverted independently |

### Working principles Ahmed reinforced

- **Ask before executing on anything ambiguous.**
- **Push back on "impossible".** When I reported the Arabic product names were
  unreachable, he said *"can't you get them from their website? it is already
  arabic."* He was right — I had guessed the wrong URL shape. That single push
  turned 0 Arabic names into 99. **Re-check your own dead ends.**
- **Flag, don't silently alter, the client's design system.**
- **Label invented copy as placeholder.** Never let it pass as client-approved.
- **Check the details, not just the headline.** He asked whether the resized
  header/footer actually matched *inside* — fonts and icons, not just heights.
  They didn't. That question found a whole class of mismatches.

---

## 3. Architecture, and why

Three layers, deliberately. See `CLAUDE.md` for the file-by-file table.

**Runtime** (`styles.css`, `scripts.js`) — chrome,
behaviour. Change and refresh; no rebuild.

**Build-time** (`python3 build/build.py`) — page content generated from shared
components so a card changes everywhere at once.

**Client state** (inside `scripts.js`) — the cart store. Persisted to
`localStorage`, no fetch, so it works from `file://` like everything else.

Why not render everything client-side and skip the build? Because the export's
defining property is that each page is standalone static HTML that works from
`file://` with no runtime data fetching. Client-side rendering would cost that
and the SEO. The build step is the price of keeping it.

```
build/
├── build.py            # builds all pages; fails on unresolved assets
├── components.py       # SINGLE SOURCE OF TRUTH for shared markup
├── catalog.py          # data access + price/name formatting
├── scrape_assets.py    # products, categories, images
├── fetch_arabic_names.py / fill_missing_names.py
└── pages/
    ├── _listing.py _auth.py _account.py _legal.py   # shared layouts
    ├── _geo.py _posts.py                            # shared data
    └── home.py shop.py product.py … (31 pages)
```

---

## 4. Bugs already found and fixed — don't reintroduce

**From the rebrand phase:**

1. **RTL broke the carousel.** It drove `scrollLeft`, which reports *negative* in
   RTL. Rewritten onto a logical scroll axis with the reporting style
   feature-detected.
2. **The Figma logo exports upside-down and stretched** — net vertical flip plus
   `preserveAspectRatio="none"`. The flip is baked into the asset.
3. **Sticky nav went transparent** — it inherited its background from the
   masthead. It now carries `bg-primary` itself.
4. **Tabs did nothing visible** — active colour was hardcoded per button.
5. **Two nav items active at once** — القهوة and المشروبات shared a slug.
6. **The overlays were missed until the final sweep.** The cart drawer still
   listed Koueider cakes and the drawer, search and location sheet were all
   English — on *every* page. **When rebranding, remember the JS-injected
   chrome, not just the pages.**
7. **A mislabelled payment mark** — Etisalat Cash, not Meeza, white-on-black.

**From the mobile/functionality phase:**

8. **`min-w-0` / missing base grid columns.** Four pages declared
   `lg:grid-cols-[Npx_1fr]` with no base rule, collapsing below `lg` to one
   max-content column; a top-level `overflow-x-hidden` then ate the overhang so
   page scroll read 0 and nothing looked wrong. The account shell clipped 249px
   this way.
9. **The cart line item squeezed its title to zero width.** Thumb, stepper and
   price chip were all `shrink-0` and with gaps exceeded the row, so the `flex-1`
   title got 0px — **product names were invisible in the cart on mobile.**
10. **Filter chips and nav categories all led to the same page.** Every
    `/shop/<slug>` resolved to `shop-category.html`, which shows coffee. Tapping
    "المكسرات" showed coffee. They were tappable and did the wrong thing.
11. **`[data-add-to-cart]` had no handler at all.** Clicking "اضف الى السلة"
    anywhere did nothing.
12. **The `hidden` attribute lost to Tailwind's `.flex`**, so all eight
    mega-menu sub-lists rendered stacked at once.
13. **Contrast:** see `DESIGN-NOTES.md`. Two of those were my own regressions.

**From the favourites phase — all three are the same "looks live, isn't" class
as 10 and 11 above:**

14. **The favourite heart had no handler at all** — 184 inert buttons across 7
    pages, and `my-account-favorites.html` hard-coded six products that nothing
    could reach. Now a real store; see `DESIGN-NOTES.md` §9.
15. **The cart drawer's two upsell "اضف" buttons did nothing.** They had
    `data-add-to-cart` but no `[data-product]` ancestor, so `productFrom()`
    returned `null` and the click handler returned silently.
16. **`CART_SEED` keyed its lines by barcode, not catalogue id**, so adding a
    seeded product from its own card produced **two lines for one product**.
    Reproduced, fixed, re-verified. Any seed must use catalogue ids.

**From the UI audit — all six were pre-existing and site-wide:**

17. **The header sat 64px inside the page content edge on all 31 pages.**
    `px-4 xl:px-20` wrapped the bands *outside* `max-w-[1536px]`, so the cap
    never bound. Live's offset is zero.
18. **The logo was the wrong artwork** — hand-derived SVG, all-white, **green
    leaf missing**, drawn at aspect 3.0 against the real mark's 3.91. Replaced
    with the client's own file.
19. **`icon-leaf.svg` never existed**; 8 broken images per page, hidden by an
    `onerror` that set `display:none`. Silent failure by construction.
20. **The language switch only applied to the page you clicked on** —
    `translateDocument()` ran on toggle, never on load. English coverage was
    ~26%; it is now ~75%.
21. **The sticky nav never stuck.** `.relative` in the base classes beat the
    added `.fixed` on source order. Now driven from `styles.css` on a
    higher-specificity selector.
22. **Cart rows overflowed 13px at 320** — missed by the baseline sweep because
    it ran against an emptied cart. **Seed the cart before quoting the sweep.**

**From the visual polish pass:**

23. **Product photos drew a white rectangle inside the beige card plate** —
    101 of 110 were opaque photos on a white sweep. Now cut out by
    `build/isolate_products.py`.
24. **Icons fought their wrappers.** Every glyph carried its own size class, so
    a chevron in a `w-6 h-6` span drew at 16px and breadcrumb arrows overflowed
    their box. All glyphs are `w-full h-full` + `currentColor` now.
25. **A backtick inside an HTML comment in `scripts.js` blanked the entire
    header.** It ends the template literal. Cost two rounds; `build.py` now
    fails on it. `node --check` cannot catch this.
26. **Selected and hovered were the same colour in the products mega-panel**,
    so the column read as permanently hovered.

---

## 5. How to verify you haven't broken anything

```bash
cd /path/to/order-base-ecommerce

npm install                       # once; Tailwind CLI for the CSS build
python3 build/build.py            # 31 page(s) + 99 fanned-out, no missing assets;
                                  # also rebuilds static-export/tailwind.css
node --check static-export/scripts.js
grep -ril 'koueider\|kouider' static-export/    # must return nothing
git status --porcelain            # a rebuild must produce no diff

python3 build/serve.py                              # http://localhost:8000
```

> **One port, 8000, and never `python3 -m http.server`.** That module sends no
> cache headers, so browsers hold `scripts.js`/`styles.css` hard — two "this is
> still wrong" reports in this project were a stale asset, not a bug. This used
> to be worked around by bumping the port on every check, which meant the URL
> moved constantly and every open tab went stale; Ahmed asked for that to stop.
> `build/serve.py` sends `Cache-Control: no-store` instead, so a plain refresh
> on a fixed URL is always current. It is rooted at `static-export/` wherever
> you run it from, is a no-op if already running, and will not silently pick a
> different port — if 8000 is taken by something else it says so and stops.

Then open any page and paste the **sweep** below into the console. It loads all
31 pages in a same-origin iframe at a given width and reports real horizontal
overflow plus WCAG contrast.

**Current baseline: `31/31` clean at 320 / 360 / 375 / 390 / 414, ~7600 text
nodes checked, 0 contrast failures.**

**Seed the cart with more than one item, and give some lines a two-digit
quantity.** Product cards now swap their add button for a `−/n/+` stepper when
the product is in the cart, so an empty cart means the sweep never measures
that control at all — the same blind spot that let a 13px cart-line overflow
through once already. A two-digit quantity is what pushes the stepper past its
comfortable width; that is the case that actually overflowed during this work.
Three digits will trip the *cart drawer's* fixed-width qty span, which is a
known pre-existing clip (DESIGN-NOTES §7) and not a regression.

```js
window.__sweep = async function (W) {
  // The last two are samples of the 99 generated product pages, which share
  // one layout: product-1322 is the rich case (multi-shot gallery, client
  // copy, best-seller strip), product-1631 the thin one (single image, no
  // client copy at all). Sweeping all 99 buys nothing over these two.
  const pages = ["about","blog","blogs","branches","cart","checkout","contact-us","export","faqs","forget-password","index","login","my-account-addresses","my-account-favorites","my-account-order","my-account-orders","my-account-point","my-account-profile","my-account-wallet","my-account","privacy-policy","product","register","reset-password","return-policy","rewards","shop-category","shop","store-closed","terms-conditions","thank-you","product-1322","product-1631"];
  const f = document.createElement("iframe");
  f.style.cssText = "position:fixed;left:-9999px;top:0;border:0;height:844px;width:" + W + "px";
  document.body.appendChild(f);
  let clean = 0, cFail = 0, cTotal = 0; const probs = [];
  for (const p of pages) {
    await new Promise(r => { f.onload = () => setTimeout(r, 140); f.src = "/" + p + ".html"; });
    // MANDATORY since the reveal went site-wide: every <section> on every page
    // starts at opacity 0 until the observer (or its 2.5s failsafe) fires, and
    // IntersectionObserver does not fire in a hidden/offscreen document — so
    // without this line most of the page measures as invisible and the sweep
    // silently reports a clean run it never actually made.
    f.contentDocument.querySelectorAll("[data-reveal]")
      .forEach(el => el.setAttribute("data-reveal", "in"));
    await new Promise(r => setTimeout(r, 100));
    const d = f.contentDocument, w = f.contentWindow, bad = [];
    d.querySelectorAll("body *").forEach(el => {
      const cs = w.getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const over = el.scrollWidth - el.clientWidth;
      // line-clamp / ellipsis truncation is intentional, not an overflow bug
      const byDesign = cs.overflow === "hidden" && (cs.textOverflow === "ellipsis" || cs.webkitLineClamp !== "none");
      if (over > 4 && el.clientWidth > 0 && cs.overflowX !== "auto" && cs.overflowX !== "scroll" && !byDesign)
        bad.push({ cls: (el.className || "").toString().slice(0, 40), over });
    });
    const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    const P = s => { const m = s.match(/[\d.]+/g).map(Number); return { r: m[0], g: m[1], b: m[2], a: m.length > 3 ? m[3] : 1 }; };
    const L = s => { const c = P(s); return 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b); };
    const R = (a, b) => { const la = L(a), lb = L(b), hi = Math.max(la, lb), lo = Math.min(la, lb); return (hi + 0.05) / (lo + 0.05); };
    const isT = c => !c || P(c).a === 0;
    const bgOf = el => { let n = el; while (n) { const b = w.getComputedStyle(n).backgroundColor; if (!isT(b)) return b; n = n.parentElement; } return "rgb(255,255,255)"; };
    const inHid = el => { let n = el; while (n && n !== d.body) { if (w.getComputedStyle(n).display === "none") return true; n = n.parentElement; } return false; };
    d.querySelectorAll("body *").forEach(el => {
      if (el.getAttribute("aria-hidden") === "true") return;
      const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(" ");
      if (!own || inHid(el)) return;
      const rr = el.getBoundingClientRect(); if (!rr.width || !rr.height) return;
      const cs = w.getComputedStyle(el);
      if (+cs.opacity === 0 || cs.visibility === "hidden") return;
      const size = parseFloat(cs.fontSize), weight = +cs.fontWeight || 400;
      const need = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3 : 4.5;
      cTotal++;
      if (R(cs.color, bgOf(el)) < need) cFail++;
    });
    const po = d.documentElement.scrollWidth - d.documentElement.clientWidth;
    if (bad.length || po) probs.push({ page: p, pageOver: po, worst: bad[0] || null }); else clean++;
  }
  f.remove();
  return { width: W, clean: clean + "/" + pages.length, problems: probs, contrastChecked: cTotal, contrastFailures: cFail };
};
await window.__sweep(390);
```

Run one width per call, and **split the page list into two batches of ~15** —
all 31 pages in one call exceeds the 30s tool timeout.

### Two traps this sweep was written around

- Testing transparency with a regex like `/, 0\)$/` also matches **any colour
  whose blue channel is 0** — including the CTA green `rgb(22,51,0)`.
- Elements inside a `display:none` subtree report unresolved computed styles.
  Skip them, or you get white-on-white readings for perfectly fine buttons.

### And one about the tooling itself

`getComputedStyle` read from the top-level document **right after a viewport
resize returned stale values** — a no-media `!important` rule appeared inert,
which cannot be true. Screenshots and same-origin iframe measurements were both
accurate. **If a computed style contradicts a screenshot, distrust the computed
style.** This is why the sweep uses an iframe.

---

## 5b. Session 2026-07-29 — home-page polish, sticky buy bar, product-page restructure

A round of small home-page fixes, a new sticky re-CTA on the product page, and
a real restructure of the product page's layout and data plumbing. All done in
the same three-layer model as always: `build/*.py` for markup, `scripts.js` /
`styles.css` for runtime behaviour, rebuild + `node --check` + the koueider
grep before every commit.

**Home page:**

- Hero carousel arrows now straddle the banner's side border (`inset-inline-*:
  -32px`, half the 64px circle) instead of sitting inset. Had to be scoped to
  `.hero-banners .carousel-prev/-next` in `styles.css` — a Tailwind utility on
  the button tied on specificity with the global `.carousel-prev { -10px }`
  rule and lost on source order (the exact trap CLAUDE.md already warns about).
- Category circles: cut the desktop horizontal gap (1fr tracks were spreading
  three 250px circles across the full 1536px container) by switching to
  `grid-cols-[repeat(3,auto)]` + `justify-center` — gap is now real `gap-x-16`
  (64px), vertical gap untouched. Mobile needs `justify-items-center` alongside
  it, or the fixed-width tile falls to `justify-self:start` or `-right` in a
  now-full-width `1fr` track — lost that once mid-session, caught by the user,
  re-added.
- `.tile-lift:hover` now uses `--lift-shadow-sm` instead of `--lift-shadow` —
  softer hover shadow on category circles only.
- Testimonials (`review_card` in `components.py`) rebuilt to a dark-card
  reference: `#14432f` card, large accent-yellow quote glyph (new `ICON.quote`),
  testimonial text, then an INITIALS avatar (no photo — no real customer
  portraits exist, same no-invention rule as the branch phones) + name + city.
  Grid is now `md:grid-cols-2 xl:grid-cols-4` with a card gap, not the old
  2-column airy text layout.

**Navbar:**

- Search and cart circles were both `bg-cta` at rest, hovering to `bg-cta-hover`
  (`#185039`) — which is the masthead's own background colour, so the search
  button visually disappeared on hover. Both are now `bg-cta` → `hover:bg-
  primary-900` (darker, never matches the masthead). Cart's small count badge
  moved from green-on-white-ring to **yellow-on-green-ring** (`bg-accent-yellow
  ring-primary`) so it reads as cropped into the corner rather than a stuck-on
  dot. Same treatment on the mobile masthead's cart badge.

**Product cards (site-wide, `components.py: product_card`):**

- Removed the favourites heart button; `[data-add-to-cart]` is now `w-full`
  instead of splitting the row with the heart via matched `basis-[104px]`. The
  stepper that replaces it on add is also `w-full` now, so the swap still never
  resizes the card.
- **The heart moved to the product-detail page's gallery plate** (`top-4
  end-4`, so it's top-LEFT in RTL — the mirror of the usual top-right spot; use
  `end`, never `left`, so it flips correctly in LTR). It carries its own
  `data-product`/id/name/price/image, because the gallery is a different DOM
  subtree from the details host and `productFrom()` only walks up to the
  *nearest* `[data-product]` ancestor.

**New: sticky buy bar on the product page** (`product.py`, new markup +
`initStickyBuyBar()` in `scripts.js`, `.sticky-buybar` in `styles.css`):

- Appears once `[data-buy-block]` (the real stepper + buy-now row) has
  scrolled *past* the top of the viewport — checked via
  `IntersectionObserver` + `boundingClientRect.top < 0`, not plain
  `!isIntersecting`, so it does not also fire on mobile before the shopper has
  scrolled down TO the block.
- **Desktop:** docks under the sticky nav at `top: 60px`. **Mobile:** docks at
  the bottom, above the safe area.
- **It owns no state.** Its −/＋ buttons and its CTA all forward clicks to the
  real cart-bound stepper and the real `[data-buy-cta]` — never a second
  writer of the cart. Title/price/qty are mirrored via a `MutationObserver` on
  the real nodes plus a `cart:change` listener, so a size-chip change (which
  fires no cart event) still repaints the bar.
- **CTA is "اشتري الان" (buy now), not "اضف الى السلة".** This was tried both
  ways mid-session — briefly changed to a plain add-to-cart, reverted on
  Ahmed's explicit correction. The bar's CTA must mirror the real buy button
  (opens the side cart after the quantity is set), not become a second
  add-only control.
- **+ is always on the visual right**, forced with `dir="ltr"` on just the
  stepper `<div>` — in the page's RTL flow the flex row would otherwise put −
  on the right. The digit is already `latin`, so this changes nothing but
  button order.
- **Collides with `[data-sticky-actions]`** (the floating search/cart pill)
  on desktop, since both dock near the top edge. Fixed by having
  `initStickyBuyBar` toggle `html.buybar-shown`, which `styles.css` uses to
  drop the pill's `top` from 60px to 140px (below the bar) only at `lg` and
  only while the bar is visible — **not** a horizontal-padding hack (tried and
  reverted; the correct fix is vertical separation, per Ahmed).

**Best-seller badge + red "best seller" proof line — now UNIFIED and ALWAYS
VISIBLE on every product page (`components.py`).** This went through two
states this session, worth knowing both:

1. First pass: made both elements always-*emitted* but self-*hiding*
   (`hidden` attribute, `data-best-seller` / `data-sold-proof` markers) when
   the product's real `popularityRank` didn't earn them — "unified template,
   shows/hides itself off the data" was the original ask.
2. Ahmed then clarified he wants them **visibly shown on every product**, not
   just present-but-hidden — for the developer handoff, so no page is ever
   missing the slot. Final state: `_best_seller_label(p) or "الأكثر مبيعاً"`
   and `_sold_proof_label(p) or "ضمن الأكثر مبيعاً في أبو عوف"` — ranked
   products keep their real, earned copy; everywhere else gets a uniform
   fallback string. **This means the badge is no longer purely a data-earned
   signal** on the ~80 unranked products — flagged in `DESIGN-NOTES.md` §1 as
   a deliberate, explicit exception to the project's "real data only" rule.
   The `data-*` markers are left in place for a future developer to wire real
   rank-driven show/hide if that's ever wanted back.

**Product-detail page — layout restructured into two columns, plus a new
generic FAQ:**

- **Sticky media column** (`lg:sticky lg:top-[60px]`, moved off the gallery
  itself and onto a wrapping `<div>`): the photo gallery **plus** a "قد يعجبك
  أيضاً" related-products box, riding down together as one sticky unit. Media
  column height is intentionally capped (related list limited to 4 items) so
  it stays shorter than the scrollable info column — a sticky column taller
  than its sibling has nothing to scroll against.
- **The related box is INTERACTIVE, not a static list.** It reuses the
  existing "frequently bought together" bundle machinery verbatim
  (`bundle_item()`, `[data-bundle]`/`[data-bundle-check]`/`[data-bundle-add]`,
  `syncBundleTotal()` in `scripts.js`) — checkboxes, a running "الإجمالي"
  total, and an "أضف الكل للسلة" add-all button. Deliberately **no**
  `data-product` and **no** `data-bundle-base` on this box (unlike the old
  full-width section), so the total and the add-all cover ONLY the related
  items, not the current product — `productFrom()` finds no host and
  contributes nothing extra. The old full-width "عادة ما يتم شراؤه معاً"
  section below the fold is gone; this replaces it entirely rather than
  duplicating it.
- Went through a mobile-ordering iteration worth knowing: at one point the
  related list was reordered to the bottom on mobile (`order-last
  lg:order-none`) so the buy box would come first. **Ahmed asked to revert
  that** — mobile keeps its natural DOM stacking order (gallery → related →
  buy box → benefits → FAQ). Don't reintroduce the reorder without asking
  again.
- **New generic FAQ accordion** (`FAQ_ITEMS` in `product.py`), identical on
  every product page by design: 4 Q&As (delivery time, returns window,
  storage/freshness, sizes), each answer restating a policy the site commits
  to elsewhere on the same page or on `return-policy.html` — never a new,
  unverifiable claim about the specific SKU. Sits in the scrollable info
  column beneath the client's own benefits accordion.
- **New divider** between the buy-CTA row and the specs/benefits strip below
  it — a plain flex child (`border-t`, no independent padding), so it lines up
  inside the card's existing `p-6 xl:p-8` rather than bleeding to the card
  edges.

**Data-honesty note for whoever picks this up next:** the specs/benefits strip
still only carries real product-specific copy for 64 of 99 products (the ones
with usable `descHtmlAr` benefit lines); the other 35 fall back to the generic
delivery/returns/branches trio, same as before this session — that gap did not
close and can't, without the client writing benefit copy for those SKUs.

---

## 6. The language toggle — what it is and isn't

Ahmed asked for a working language switcher to test RTL. It:

- flips `dir`/`lang` on `<html>` and persists the choice
- re-renders the JS-injected chrome in English
- swaps product titles to `catalog.json`'s **real** English `name`
- walks build-time text nodes and translates exact dictionary matches
  (headings, buttons, sort options, cart labels, empty states), losslessly
  reversible

It does **not** translate prose — FAQ answers, About copy, blog posts, product
descriptions, testimonials. There is no English source for them, and
machine-translating a client's storefront is inventing content.

**The legal pages must never be machine-translated.** They are already in-house
placeholder blocking launch; an invented English translation of an invented
Arabic placeholder is two steps from anything the client could sign off.

Every English string in the `EN` dictionary is **in-house placeholder**
terminology awaiting sign-off. Product names are the one exception.

Real bilingual support means English copy for all 31 pages plus a URL strategy
(`/en/` routes vs runtime switch). That is a project, not a toggle.

---

## 7. Where the data comes from

| Need | Source |
|---|---|
| Design tokens | Figma MCP `get_variable_defs` on `tQiydoANmIdYWq0IfmTsMz` |
| Desktop designs | Figma page `Web` `162:4801`; home `4842:55826`; header `5061:24238`; footer `259:11262`; components `56:2095` |
| Mobile designs | Figma page `Mobile` `821:44658` — canonical frames listed in `DESIGN-NOTES.md` |
| Chrome measurements | **abuauf.com, measured live in the browser** — heights, type, container width, hover rules |
| Products / categories | `backend.abuauf.com/wp-json/wc/store/v1/products` (public). Prices in **minor units** |
| Arabic product names | Next.js flight payload at `www.abuauf.com/ar/category/<slug>`; per-product at `/ar/products/<slug>` |
| Branches | `backend.abuauf.com/wp-json/apis/v2/branches` — Arabic addresses, blank `ar_title`, **empty `phone` on all 316** |
| Reviews (unused) | `backend.abuauf.com/wp-json/apis/v2/get-all` — real ratings + authors |
| Imagery | `backend.abuauf.com/wp-content/uploads/…` |

---

## 8. What's left

**Blocked on the client — cannot be done honestly without them:**

1. **Legal copy** for privacy, terms and returns. **Blocks launch.**
2. **Branch phone numbers and coordinates.** All 316 `phone` fields are empty,
   so the Figma's per-card phone row and `اتجاهات` link are not built. Inventing
   them would send customers to wrong numbers.
   **Rewards body copy** — the client's own `/rewards` page is lorem ipsum, so
   `rewards.html` is deliberately thin (see `DESIGN-NOTES.md` §2).
3. **Real sale prices** — `catalog.json` has one price per product, so the
   Figma's struck-through compare-at price is not rendered.
4. **Sub-category taxonomy.** No field exists; four of the seven Figma
   sub-category labels match zero real products, so those chips don't filter.
5. **Publish-date data.** `وصل حديثاً` sorts by id as a proxy. (`الأكثر مبيعاً`
   is no longer a proxy — `popularityRank` from `fetch_popularity.py` is the
   client's real sales ordering. The home rails could now be re-sorted on it;
   they have not been, to keep that change reviewable on its own.)
6. **Sign-off on every in-house string**, Arabic and English. Now includes the
   product page's benefit strip and its Arabic description, both translations
   of the client's own English product copy.
6b. **An absolute sold-count**, if the "500+ sold this week" pattern is wanted
   literally. No endpoint carries sales volume; the page states a real rank
   instead. One function — `sold_proof()` — changes it.
6c. **Photography for the 26 products that still have a single shot**, and a
   decision on whether the rating glyph should be a star rather than the
   brand's heart (`DESIGN-NOTES.md` §3).
7. **Real product reviews.** `apis/v2/get-all` used to be listed below as ready
   to build. **It is not** — it returns 10 rows of QA test data, every one
   `John` / `"comment"` / 5★, all posted within 11 minutes on 2024-09-17.
   Wiring it would put visibly fake reviews on the storefront. Details in
   `DESIGN-NOTES.md` §1. Needs the client to collect real reviews.

**Ready to build when you are:**

8. **`صحارة ديلايتس` home section** (Figma `753:34833`), pending assets.
9. **Checkout summary collapse** — the Figma has it collapsible; left expanded
    at Ahmed's direction.
10. **Tell the designer** the Figma still contains the contrast failures the
    build diverges from, and that the live site differs from the Figma on
    several chrome details.
11. **Tap targets need a real re-audit.** The "≥44px, audited and passing"
    claim does not hold: `cart.html` alone has steppers at 32×32 and `حذف` at
    24 wide. Fixing the stepper needs a layout decision, not a size tweak —
    see `DESIGN-NOTES.md` §7.
12. **The sticky nav's slide-in animation is unverified.** The bar now
    genuinely reaches `position: fixed`, but the entrance animation could not
    be confirmed: the automation pane freezes animation timelines
    (`playState: "running"` with `currentTime: 0` after 900ms), so the bar
    read as parked at `translateY(-48px)`. A `prefers-reduced-motion` guard is
    in place so it can never end up hidden. **Confirm in a real browser.**
13. **The add-to-cart flight has never been watched at full speed.** Its
    sequencing, geometry and end state are all verified numerically, and the
    picked-up tile has been photographed — but the browser pane reports
    `visibilityState: "hidden"`, so CSS transitions register without ticking
    and the pane will not screenshot a scrolled page at all. **Watch it in a
    real browser** before calling the motion work done.
14. **Product-page interactions carry over to nothing else yet.** Size chips,
    the live price and the gallery only exist on `product.html`, because it is
    the only page that renders a single product. If listing cards ever need a
    size selector, `size_chips()` is already data-driven and would work as-is.

---

### Picking this up in a new session

Start here, in this order:

1. `python3 build/serve.py` → `http://localhost:8000`. **One port, always** —
   see §5. Do not use `python3 -m http.server`.
2. Read `CLAUDE.md` (loads automatically) — rule 8 is new and was earned the
   hard way, four separate reports of the same class of bug.
3. `product.html` is the page with the most recent work on it and the most
   moving parts: real size SKUs driving the price, a real photo gallery with
   two fill modes, a fractional rating, and a real best-seller rank. If you
   change the hero product, re-read `DESIGN-NOTES.md` §3 first — the page's
   descriptive copy is tied to it.
4. Re-run the sweep in §5 after any layout or colour change, **with a seeded
   cart**. Last measured: 31/31 clean at 320 / 375 / 414, 0 contrast failures.

**Not yet tested anywhere:** the site has **never been opened in Safari or on a
physical device**. All verification has been Chromium at emulated viewports.
iOS-specific behaviour — `100vh`, safe-area insets, momentum scroll, real touch
— is unverified. Worth one pass on a real iPhone before launch.
