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
| Pages | 29 / 29 |
| Koueider references | zero, verified across every file |
| Products | 99, real names (Arabic + English), prices, images |
| Branches | 316 across 25 governorates, real |
| Accessibility | WCAG 2.1 AA, 0 failures across all 29 pages; tap targets ≥44px |
| Responsive | verified clean at 320 / 360 / 375 / 390 / 414 |
| Cart | real state, persisted, with an event API |
| Filters / nav routes | genuinely functional over real catalogue data |
| Language | direction + chrome + UI strings switch; prose does not (by design) |
| Baseline commit | `f4dde89` — the pristine Koueider export, for diffing |

---

## 2. Decisions the client made — do not silently reverse these

Each was an explicit answer from Ahmed, not an assumption.

| Decision | Choice | Why it matters |
|---|---|---|
| **Fidelity** | Rebuild against Figma page by page — *not* a colour reskin | The Figma covers ~all 29 routes, and the RTL flip rewrote layout anyway |
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

**Runtime** (`tw-config.js`, `styles.css`, `scripts.js`) — tokens, chrome,
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
    └── home.py shop.py product.py … (29 pages)
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

---

## 5. How to verify you haven't broken anything

```bash
cd /path/to/order-base-ecommerce

python3 build/build.py            # must report 29 pages, no missing assets
node --check static-export/scripts.js
grep -ril 'koueider\|kouider' static-export/    # must return nothing
git status --porcelain            # a rebuild must produce no diff

(cd static-export && python3 -m http.server 9200)   # USE A FRESH PORT
```

> **Always bump the port.** `http.server` sends no cache headers and browsers
> hold `scripts.js`/`styles.css` hard. Two "this is still wrong" reports in this
> project were a stale port, not a bug. Confirm the root too:
> `lsof -a -p $(lsof -ti tcp:9200) -d cwd -Fn`

Then open any page and paste the **sweep** below into the console. It loads all
29 pages in a same-origin iframe at a given width and reports real horizontal
overflow plus WCAG contrast.

**Current baseline: `29/29` clean at 320 / 360 / 375 / 390 / 414, ~4300 text
nodes checked, 0 contrast failures.**

```js
window.__sweep = async function (W) {
  const pages = ["about","blog","blogs","branches","cart","checkout","contact-us","faqs","forget-password","index","login","my-account-addresses","my-account-favorites","my-account-order","my-account-orders","my-account-point","my-account-profile","my-account-wallet","my-account","privacy-policy","product","register","reset-password","return-policy","shop-category","shop","store-closed","terms-conditions","thank-you"];
  const f = document.createElement("iframe");
  f.style.cssText = "position:fixed;left:-9999px;top:0;border:0;height:844px;width:" + W + "px";
  document.body.appendChild(f);
  let clean = 0, cFail = 0, cTotal = 0; const probs = [];
  for (const p of pages) {
    await new Promise(r => { f.onload = () => setTimeout(r, 140); f.src = "/" + p + ".html"; });
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
  return { width: W, clean: clean + "/29", problems: probs, contrastChecked: cTotal, contrastFailures: cFail };
};
await window.__sweep(390);
```

Run one width per call — four widths in a single call exceeds the 30s tool
timeout.

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

Real bilingual support means English copy for all 29 pages plus a URL strategy
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
3. **Real sale prices** — `catalog.json` has one price per product, so the
   Figma's struck-through compare-at price is not rendered.
4. **Sub-category taxonomy.** No field exists; four of the seven Figma
   sub-category labels match zero real products, so those chips don't filter.
5. **Sales / publish-date data.** `الأكثر مبيعاً` restores catalogue order and
   `وصل حديثاً` sorts by id as a proxy. Neither is a real ranking.
6. **Sign-off on every in-house string**, Arabic and English.

**Ready to build when you are:**

7. **Micro-interactions** on the cart — the `cart:change` event API and keyed
   reconcile exist precisely for this.
8. **`/rewards` and `/export` pages.** Two navbar items currently fall through to
   the homepage. Figma frames exist (`973:40830`, `426:29955`).
9. **Cart drawer upsell buttons and favourite hearts** are not wired.
10. **`صحارة ديلايتس` home section** (Figma `753:34833`), pending assets.
11. **Checkout summary collapse** — the Figma has it collapsible; left expanded
    at Ahmed's direction.
12. **Real reviews** could replace the invented testimonials via `apis/v2/get-all`.
13. **Tell the designer** the Figma still contains the contrast failures the
    build diverges from, and that the live site differs from the Figma on
    several chrome details.

**Not yet tested anywhere:** the site has **never been opened in Safari or on a
physical device**. All verification has been Chromium at emulated viewports.
iOS-specific behaviour — `100vh`, safe-area insets, momentum scroll, real touch
— is unverified. Worth one pass on a real iPhone before launch.
