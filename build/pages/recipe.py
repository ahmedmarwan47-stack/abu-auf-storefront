"""Single recipe — layout after fambeef.org's recipe page, built in our system.

The structure is borrowed (media beside a details card holding a time chip,
the overview, ingredients, numbered method, the products used, share, then a
related-recipes band); every value is ours — the product page's sticky media
column and lg-only white card, recipe_card() for the related band,
product_card() for the products, so cart, favourites and the card stepper all
work here for free.

Every word of the recipe is the CLIENT'S: build/fetch_recipes.py pulls the
Arabic title, intro, ingredients and method off abuauf.com into
data/recipes.json. The labels (المكونات, طريقة الطبخ, الوقت الكلي, حصص,
وصفات مماثلة) are the live recipe page's own strings, read off its flight
payload. What is ours: the "products in this recipe" heading, the share row,
and the product mapping in USES. See DESIGN-NOTES §1.
"""
import json
import os

from catalog import EXPORT, PRODUCTS, e
from components import ICON, page, page_header, product_card, recipe_card, section_heading

SLUG = "recipe.html"

RECIPES = json.load(open(os.path.join(EXPORT, "data", "recipes.json"), encoding="utf-8"))
FEATURED = "date-dark-choco-granola-bars"

# Catalogue products the recipe calls for BY NAME ("زبدة فول سوداني أبو عوف").
# Matched by hand against catalog.json and keyed by catalogue id, the same
# rule the stores follow. The recipe's other Abu Auf ingredients — sokkari
# dates and original granola — are not among our 99 products, so they get no
# card rather than a near-miss one.
USES = {"date-dark-choco-granola-bars": [1402]}

# The client's text, corrected for typos and nothing else. "فوق سوداني" is
# "فول سوداني" mistyped twice in the source; fixed here, not in the data, so a
# re-scrape cannot silently bring it back and the raw JSON stays the client's.
TYPOS = {"الفوق السوداني": "الفول السوداني", "فوق سوداني": "فول سوداني"}

# How many cards the related band shows. Order is the client's own list order
# with this recipe excluded — what the live site's similar-recipes rail does
# (its request passes excluded_slugs), not a curation of ours.
RELATED = 4

# Literal class names, never "grid-cols-" + n — Tailwind only emits what it
# can read as a whole string (CLAUDE.md).
FACT_COLS = {0: "hidden", 1: "grid-cols-1", 2: "grid-cols-2", 3: "grid-cols-3"}


def _fix(s):
    for wrong, right in TYPOS.items():
        s = s.replace(wrong, right)
    return s


def _minutes(n):
    return f'<span class="latin">{e(n)}</span> دقيقة'


def _fact(label, value_html):
    return f"""
            <div class="flex flex-col items-center gap-1 bg-interaction-base px-2 py-4 rounded-2xl text-center">
              <span class="text-neutral-secondary text-xs xl:text-sm">{e(label)}</span>
              <span class="font-bold text-[#062A1C] text-base xl:text-lg">{value_html}</span>
            </div>"""


def _ingredient(text):
    # A static check mark, not a control (Ahmed, 2026-10-28) — the list is
    # read, not ticked off. Decorative, so hidden from assistive tech; the
    # <ul> already announces it as a list.
    return f"""
                <li class="flex items-start gap-3 py-1">
                  <span aria-hidden="true" class="mt-1 w-5 h-5 text-primary shrink-0">{ICON['check']}</span>
                  <span class="text-neutral-800 text-base leading-7">{e(_fix(text))}</span>
                </li>"""


def _step(i, text):
    return f"""
                <li class="flex items-start gap-4">
                  <span aria-hidden="true" class="place-items-center grid bg-primary-light rounded-full font-bold text-primary text-base size-9 shrink-0 latin">{i}</span>
                  <p class="pt-1 text-neutral-800 text-base leading-8">{e(_fix(text))}</p>
                </li>"""


def _share():
    # The page's own address is only known at runtime (SITE_ORIGIN is empty,
    # DESIGN-NOTES §3), so scripts.js fills the network hrefs from location.
    # They ship `hidden` and are revealed once filled: a JS failure degrades
    # to "no share links", never to links that go nowhere. Copying the link
    # reuses the referral copy handler, same button feedback.
    pill = ("inline-flex items-center gap-2 bg-white hover:bg-interaction-base px-4 border "
            "border-neutral-divider rounded-full h-11 font-semibold text-[#062A1C] text-sm transition-colors")
    return f"""
            <div class="flex flex-wrap items-center gap-3">
              <span class="basis-full sm:basis-auto font-semibold text-[#062A1C] text-sm">شارك الوصفة</span>
              <button type="button" data-copy-url class="{pill}">
                <span aria-hidden="true" class="w-4 h-4">{ICON['link']}</span><span data-copy-label>نسخ الرابط</span>
              </button>
              <a data-share-net="whatsapp" hidden target="_blank" rel="noopener" class="{pill}">واتساب</a>
              <a data-share-net="facebook" hidden target="_blank" rel="noopener" class="{pill}">فيسبوك</a>
            </div>"""


def build():
    r = next(x for x in RECIPES if x["slug"] == FEATURED)
    name = r["nameAr"]
    by_id = {p["id"]: p for p in PRODUCTS}
    uses = [by_id[i] for i in USES.get(r["slug"], []) if i in by_id]

    facts = [_fact("الوقت الكلي", _minutes(r["totalTime"]))] if r.get("totalTime") else []
    if r.get("persons"):
        facts.append(_fact("حصص", f'<span class="latin" dir="ltr">{e(r["persons"])}</span>'))
    if r.get("ingredientsAr"):
        facts.append(_fact("المكونات", f'<span class="latin">{len(r["ingredientsAr"])}</span>'))

    ingredients = "".join(_ingredient(x) for x in r["ingredientsAr"])
    steps = "".join(_step(i, x) for i, x in enumerate(r["stepsAr"], 1))
    divider = '<div class="border-neutral-divider border-t" role="separator"></div>'

    uses_html = ""
    if uses:
        uses_html = f"""
            {divider}
            <div class="flex flex-col gap-4">
              <h2 class="font-bold text-[#062A1C] text-lg xl:text-xl">منتجات أبو عوف في الوصفة</h2>
              <div class="gap-4 grid grid-cols-2 xl:grid-cols-3">{"".join(product_card(p, slide=False) for p in uses)}
              </div>
            </div>"""

    related = [x for x in RECIPES if x["slug"] != r["slug"]][:RELATED]
    related_html = "".join(
        recipe_card(x["image"], "الوصفات", x["nameAr"], x["introAr"], x["totalTime"] or "—")
        for x in related)

    body = f"""{page_header("", [("الرئيسية", "index.html"), (name, None)])}

      <!-- ============================= RECIPE ============================= -->
      <section class="pt-6 pb-12">
        <!-- The media track is CAPPED at 440px rather than half the row: the
             client's only photograph of this recipe is 395x320, and a half-row
             column would draw it at ~2x on desktop. items-start + the sticky
             column follow the product page; both work only because <main> is
             overflow-x-clip (see page()). grid-cols-1 is the base rule an
             lg-only template needs (CLAUDE.md, min-w-0 note). -->
        <div class="items-start gap-8 xl:gap-12 grid grid-cols-1 lg:grid-cols-[minmax(0,440px)_minmax(0,1fr)] mx-auto px-4 max-w-[1536px]">

          <div class="flex flex-col gap-4 min-w-0 lg:self-start lg:sticky lg:top-[60px]">
            <div class="bg-interaction-base rounded-[20px] overflow-hidden">
              <img src="{e(r['image'])}" alt="{e(name)}" width="395" height="320"
                   class="w-full h-auto aspect-[395/320] object-cover" />
            </div>
            <div class="gap-3 grid {FACT_COLS[len(facts)]}">{"".join(facts)}
            </div>
          </div>

          <!-- White card at lg only, as on the product page: on a phone the
               content sits inline with the page grid under the photo. -->
          <article class="flex flex-col gap-6 lg:bg-white lg:shadow-custom4 lg:p-6 xl:p-8 lg:rounded-[20px] min-w-0">
            <div class="flex flex-col gap-3">
              <span class="inline-flex items-center gap-1.5 self-start bg-interaction-base px-3 py-1.5 rounded-full font-semibold text-primary text-sm">
                {ICON['clock']}{_minutes(r['totalTime'])}
              </span>
              <h1 class="font-bold text-[#062A1C] text-2xl xl:text-4xl leading-tight">{e(name)}</h1>
              <p class="text-neutral-secondary text-base xl:text-lg leading-8">{e(r['introAr'])}</p>
            </div>

            {divider}
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#062A1C] text-lg xl:text-xl">المكونات</h2>
              <ul class="flex flex-col gap-1">{ingredients}
              </ul>
            </div>

            {divider}
            <div class="flex flex-col gap-4">
              <h2 class="font-bold text-[#062A1C] text-lg xl:text-xl">طريقة الطبخ</h2>
              <ol class="flex flex-col gap-5">{steps}
              </ol>
            </div>
{uses_html}
            {divider}
{_share()}
          </article>
        </div>
      </section>

      <!-- ============================= RELATED ============================= -->
      <section class="bg-interaction-base py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("وصفات مماثلة")}
          <div class="gap-6 xl:gap-8 grid lg:grid-cols-2">{related_html}
          </div>
        </div>
      </section>"""

    return page(f"{name} | أبو عوف", r["introAr"], body, "recipe", "/recipes/" + r["slug"])
