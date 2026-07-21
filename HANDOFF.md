# Handoff — Abu Auf static storefront

Everything a fresh Claude session (or a human) needs to continue this work
without re-deriving it or undoing it. `CLAUDE.md` is the short operating brief
and loads automatically; this file is the reasoning behind it.

---

## 1. What was done

A 29-page static export of the **Koueider** storefront (built on OrderBase) was
rebranded to **Abu Auf**, rebuilt page by page against the Abu Auf Figma.

| | |
|---|---|
| Pages | 29 / 29 rebuilt |
| Koueider references | zero, verified across every file |
| Products | 99, real names (Arabic + English), prices, images |
| Branches | 316 across 25 governorates, real |
| Accessibility | passes WCAG 2.1 AA, verified in-browser |
| Baseline commit | `f4dde89` — the pristine Koueider export, for diffing |

---

## 2. Decisions the client made — do not silently reverse these

Each was an explicit answer from Ahmed, not an assumption.

| Decision | Choice | Why it matters |
|---|---|---|
| **Fidelity** | Rebuild against Figma page by page — *not* a colour reskin | The Figma covers ~all 29 routes, and the RTL flip rewrote layout anyway, so a reskin would have cost nearly the same and left Koueider's page compositions underneath |
| **Language** | Arabic-first, `dir="rtl"` default. Not bilingual | Matches the live abuauf.com, which is Arabic-only |
| **Copy** | Real Abu Auf content wherever reachable | Not placeholder-by-default |
| **Imagery** | Majority scraped from abuauf.com; minority exported from Figma | Client confirmed rights |
| **Responsive** | Desktop first; dedicated mobile pass against the Figma `Mobile` page still **outstanding** | Avoided building every page twice |
| **Components** | Shared, so a tweak reflects site-wide | Ahmed asked for explicit confirmation of this — treat it as a hard requirement |
| **Agency credit** | **Keep** "Web Design by MITCH DESIGNS" | I removed it; Ahmed asked for it back. Don't remove it again |
| **Contrast** | **Fix it**, diverging from the Figma | Originally I flagged-but-preserved the failures; Ahmed later asked for them fixed |
| **Workflow** | Straight through, one commit per page/batch | So any page can be reviewed or reverted independently |

### Working principles Ahmed reinforced

- **Ask before executing on anything ambiguous.** The project opened with
  "before you execute anything, ensure that you understand everything and ask me."
- **Push back on "impossible".** When I reported the Arabic product names were
  unreachable, Ahmed said *"can't you get them from their website? it is already
  arabic."* He was right — I had guessed the wrong URL shape. That single push
  turned 0 Arabic names into 99. **Re-check your own dead ends.**
- **Flag, don't silently alter, the client's design system** — until told otherwise.
- **Label invented copy as placeholder.** Never let it pass as client-approved.

---

## 3. Architecture, and why

Two layers, deliberately:

**Runtime (no rebuild).** `tw-config.js`, `scripts.js`, `styles.css`. Change a
token or the header and every page updates on refresh.

**Build-time (`python3 build/build.py`).** Page content is generated from shared
components so a card changes everywhere at once.

Why not render everything client-side and skip the build? Because the export's
defining property is that each page is standalone static HTML that works from
`file://` and needs no runtime data fetching. Client-side rendering would cost
that and the SEO. The build step is the price of keeping it.

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

1. **RTL broke the carousel.** It drove `scrollLeft`, which reports *negative* in
   RTL, collapsing the homepage to a ~500px column. Rewritten onto a logical
   scroll axis with the RTL reporting style feature-detected.
2. **The Figma logo exports upside-down and stretched** — its wrapper carried a
   net vertical flip plus `preserveAspectRatio="none"`. The flip is baked into
   `images/abuauf/brand/logo-abuauf-white.svg`.
3. **Sticky nav went transparent** — it inherited its background from the
   masthead, so `position: fixed` left it floating invisibly. It now carries
   `bg-primary` itself.
4. **Tabs did nothing visible** — active colour was hardcoded per button.
   Now driven by `.tab-btn.is-active` in CSS.
5. **Two nav items active at once** — القهوة and المشروبات shared a slug.
6. **The overlays were missed until the final sweep.** The cart drawer still
   listed Koueider cakes and the drawer, search modal and location sheet were
   all English — on *every* page. Caught only by an asset audit. **When
   rebranding, remember the JS-injected chrome, not just the pages.**
7. **A mislabelled payment mark** — Etisalat Cash, not Meeza, and white-on-black
   so it must not sit on a white chip.
8. **Contrast:** see `DESIGN-NOTES.md`. Two of those were my own regressions.

---

## 5. How to verify you haven't broken anything

```bash
cd /path/to/order-base-ecommerce

python3 build/build.py            # must report 29 pages, no missing assets
node --check static-export/scripts.js

cd static-export
grep -ril 'koueider\|kouider' .   # must return nothing
python3 -m http.server 8899
```

Then in a browser at `http://localhost:8899/`, paste the contrast auditor from
§6 into the console on `index`, `checkout`, `my-account` and `shop-category`.
Each must report `failures: 0`.

> Bump the port number when re-verifying CSS/JS — `http.server` caches hard.

---

## 6. Contrast auditor

Paste into the browser console on any page. Reports every visible text node
below WCAG AA.

```js
(() => {
  function lin(c){c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4);}
  function parse(rgb){const m=rgb.match(/[\d.]+/g).map(Number);return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1};}
  function lum(rgb){const c=parse(rgb);return 0.2126*lin(c.r)+0.7152*lin(c.g)+0.0722*lin(c.b);}
  function ratio(a,b){const la=lum(a),lb=lum(b),hi=Math.max(la,lb),lo=Math.min(la,lb);return (hi+0.05)/(lo+0.05);}
  const isTransparent = c => !c || parse(c).a === 0;           // NOT "blue channel is 0"
  const bgOf = el => { let n=el; while(n){const b=getComputedStyle(n).backgroundColor; if(!isTransparent(b)) return b; n=n.parentElement;} return 'rgb(255,255,255)'; };
  const inHidden = el => { let n=el; while(n && n!==document.body){ if(getComputedStyle(n).display==='none') return true; n=n.parentElement;} return false; };
  const out=[];let checked=0;
  document.querySelectorAll('body *').forEach(el=>{
    if(el.getAttribute('aria-hidden')==='true') return;
    const own=[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
    if(!own||inHidden(el)) return;
    const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
    const cs=getComputedStyle(el);
    if(+cs.opacity===0||cs.visibility==='hidden') return;
    const size=parseFloat(cs.fontSize),weight=+cs.fontWeight||400;
    const need=(size>=24||(size>=18.66&&weight>=700))?3:4.5;
    const c=ratio(cs.color,bgOf(el)); checked++;
    if(c<need) out.push({text:own.slice(0,30),cls:(el.className||'').toString().slice(0,50),ratio:+c.toFixed(2),need});
  });
  return {checked, failures: out.length, items: out.slice(0,8)};
})()
```

Two traps this auditor was written around, both of which produced false alarms:
- Testing transparency with a regex like `/, 0\)$/` also matches **any colour
  whose blue channel is 0** — including the CTA green `rgb(22,51,0)`.
- Elements inside a `display:none` subtree report unresolved computed styles.
  Skip them, or you get white-on-white readings for perfectly fine buttons.

---

## 7. Where the data comes from

| Need | Source |
|---|---|
| Design tokens | Figma MCP `get_variable_defs` on file `tQiydoANmIdYWq0IfmTsMz` |
| Page designs | Figma page `Web` `162:4801`; home `4842:55826`; header `5061:24238`; footer `259:11262`; components `56:2095`; mobile `821:44658` |
| Products / categories | `backend.abuauf.com/wp-json/wc/store/v1/products` (public). Prices in **minor units** |
| Arabic product names | Server-rendered into the Next.js flight payload at `www.abuauf.com/ar/category/<slug>`; per-product at `/ar/products/<slug>` |
| Branches | `backend.abuauf.com/wp-json/apis/v2/branches` — returns `{data:[…]}`, Arabic addresses, blank `ar_title` |
| Reviews (unused) | `backend.abuauf.com/wp-json/apis/v2/get-all` — real ratings + authors |
| Imagery | `backend.abuauf.com/wp-content/uploads/…` |

---

## 8. What's left

1. **Mobile pass** against the Figma `Mobile` page (`821:44658`). Agreed to
   follow desktop sign-off; not started.
2. **Client copy** — the three legal pages are placeholder and **block launch**.
   FAQ figures (100 EGP minimum, 2-hour Cairo delivery, 14-day returns) are
   assumptions.
3. **`صحارة ديلايتس` home section** (Figma `753:34833`) omitted, pending that
   sub-brand's assets.
4. **Address discrepancy** — the Figma footer and the live site disagree on the
   HQ address. The build uses the Figma's.
5. **Real reviews** could replace the invented testimonials via `apis/v2/get-all`.
6. **Tell the designer** the Figma still contains the contrast failures the build
   has now diverged from.
