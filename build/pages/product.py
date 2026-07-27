"""Product detail — Figma 'Product' (383:33745).

One layout, NINETY-NINE pages. `build()` still writes product.html (the worked
example below), and `build_many()` writes product-<id>.html for every product
in the catalogue — before that, every card on the site linked to the same
single page, so clicking any product opened the coffee. The card links in
components.py carry the id; the build fails loudly if a page goes missing.

What differs per page is only what we genuinely have per product:

  * name, prices, gallery, sizes, badge, social proof — catalog.json fields,
    all fetched
  * description — the client's own Arabic `short_description`
    (`descAr`, fetched by build/fetch_descriptions.py); omitted when absent
  * the "الفوائد" accordion — the client's own Arabic `description` HTML
    (`descHtmlAr`, same scraper), sanitised down to lists and emphasis

The hero keeps its hand-curated copy (translated from the client's English,
flagged in DESIGN-NOTES); nothing else gets invented prose. A product the
client never wrote copy for renders without a description rather than with
ours — same rule as the branch phone numbers.
"""
import re
from html import unescape

from catalog import BRANCH_COUNT, PRODUCTS, e, in_category, money, rail_products, title
from components import (
    ICON, accordion, best_seller_badge, button, carousel, page, page_header,
    product_card, product_gallery, qty_stepper, rating, recipe_card,
    size_chips, sold_proof, trust_row, product_benefits, bundle_item, section_heading,
)

SLUG = "product.html"


def product_slug(p):
    """The output filename for a product's own page — used by components.py
    for card links, so the two can never drift apart."""
    return f"product-{p.get('id', 0)}.html"


# Worked example, chosen so that EVERY signal on this page is real:
#
#   * 3 real size SKUs — 50/100/200 جم at 69/82.5/220 EGP — so the size chips
#     genuinely move the price instead of miming it. Only 10 of our 99
#     products are sold in more than one size at all.
#   * 3 real gallery photographs from the client's CDN.
#   * Rank #12 of their 653-product store, so the best-seller badge and the
#     social-proof line are earned rather than asserted.
#
# It is coffee rather than the Figma's chocolate dates. That is the trade:
# the dates product has a richer gallery (9 shots) but is a single-size SKU,
# so it cannot demonstrate the size-to-price behaviour at all. Ahmed asked for
# the weight to drive the price, and the only honest way to show that is a
# product that really is sold by weight. Reorder this list to change it back.
def _hero():
    for want in ("قهوة بن برازيلى سادة فاتح",
                 "تمر صحاري بالشيكولاته و اللوز",
                 "معمول بعجوه المجدول مغطى بالشيكولاته"):
        for p in PRODUCTS:
            if want in (p.get("nameAr") or ""):
                return p
    return in_category("Dates & Dried Fruits")[0]


# All the descriptive copy below belongs to the hero product above. It used to
# describe chocolate-stuffed dates, which stopped being true the moment the
# hero became coffee — a page whose body copy contradicts its own title is
# worse than one with thin copy.
#
# The wording is a translation of the client's OWN English `shortDesc` for this
# SKU ("Enjoy the delicate, bright flavors of Abu Auf's light-roasted Brazilian
# coffee... smooth, refreshing brew, perfect for those who appreciate a lighter
# roast") plus what the product's real name states — light roast, Brazilian
# beans. So it restates client copy rather than inventing claims.
#
# It is still OUR Arabic, and unsigned-off, exactly like every other
# translated string in this build. Flagged in DESIGN-NOTES. Note what is
# deliberately absent: no health or nutrition claim, and nothing like the
# reference design's "third-party tested" / "100% vegan", which are auditable
# statements about a supply chain that nobody at Abu Auf has made.
DESCRIPTION = (
    "استمتع بالنكهات الخفيفة والمشرقة من بن أبو عوف البرازيلي فاتح التحميص. "
    "مذاق ناعم ومنعش، مثالي لمن يفضلون التحميص الفاتح في فنجانهم اليومي."
)

BENEFIT_ITEMS = [
    ("leaf", "تحميص فاتح", "نكهة خفيفة ومشرقة"),
    ("bolt", "بن برازيلي", "حبوب مختارة بعناية"),
    ("shield", "مذاق ناعم", "مناسب للتحضير اليومي"),
]

# The reassurance strip every OTHER product page carries, so the layout is
# uniform across all 99 (Ahmed, 2026-07-22 — a product opened after the hero
# looked like a different template). Exactly what trust_row's contract asks
# for: every claim restates something this site already says elsewhere —
# the two-hour delivery row lower on this same page, the 14-day window on
# return-policy.html, and the real branch count from branches.json. The
# branch number is computed, not typed, so it moves with the data.
SERVICE_ITEMS = [
    ("truck", "توصيل خلال ساعتين", "في القاهرة الكبرى"),
    ("return", "استرجاع خلال 14 يوم", "من تاريخ الاستلام"),
    ("store", f"+{BRANCH_COUNT} فرعاً في مصر", "في 25 محافظة"),
]

BENEFITS = """
                      <ul class="flex flex-col gap-2 ps-5 list-disc">
                        <li>نكهات خفيفة ومشرقة من التحميص الفاتح</li>
                        <li>حبوب برازيلية مختارة بعناية</li>
                        <li>مذاق ناعم ومنعش مناسب للتحضير اليومي</li>
                      </ul>"""

STORAGE = """
                      <ul class="flex flex-col gap-2 ps-5 list-disc">
                        <li>يحفظ في عبوة محكمة الغلق بعيداً عن الرطوبة</li>
                        <li>بعيداً عن أشعة الشمس المباشرة ومصادر الحرارة</li>
                        <li>يفضل الطحن قبل التحضير مباشرة للحفاظ على النكهة</li>
                      </ul>"""

RECIPES = [
    ("images/abuauf/site/4-1-1.webp", "الوصفات", "كيكة التمر بالقرفة والشيكولاتة البيضاء",
     "وصفة سهلة تجمع بين حلاوة التمر ودفء القرفة، جاهزة في أقل من ساعة.", 45),
    ("images/abuauf/site/big.webp", "الوصفات", "فتوتشيني ألفريدو دجاج مع الكاجو",
     "طبق كريمي غني بالمكسرات، مناسب لعشاء سريع في نص ساعة.", 30),
]


# The client's `description` HTML is WordPress output — strong/ul/li plus
# whatever a content editor once pasted in. Keep only the structural tags the
# accordion can style and drop every attribute; anything else is stripped to
# its text. `.desc-rich` in styles.css restores the list treatment the hero's
# hand-written markup carries inline.
_ALLOWED_TAGS = {"strong", "b", "em", "ul", "ol", "li", "p", "br"}


def _clean_client_html(html):
    def keep(m):
        tag = m.group(2).lower()
        return f"<{m.group(1)}{tag}>" if tag in _ALLOWED_TAGS else ""
    cleaned = re.sub(r"<(/?)([a-zA-Z0-9]+)[^>]*/?>", keep, html)
    return f'<div class="desc-rich">{cleaned}</div>'


def _plain(text):
    """Strip markup out of a field that is supposed to be plain prose.

    `descAr` is the client's `short_description` and goes through e() into a
    <p>, so anything tag-shaped inside it escapes and renders as LITERAL
    VISIBLE MARKUP. It does contain such things: 20 of the 99 products carry
    pasted editor debris in that field — `<span data-sheets-root="1">` from a
    Google Sheets paste, `x_MsoListParagraph` from Word, and on product-8543 a
    whole `<div class="... AIPRM__conversation__response">` wrapper, which is
    what a ChatGPT web export leaves behind. Those pages were printing raw
    angle brackets at the shopper in body copy.

    Fixed here rather than in the scraped JSON on purpose: catalog.json is
    fetched data and is meant to stay a faithful copy of what the client's
    endpoints return (CLAUDE.md, "real data over invented data"). Laundering
    it in place would mean the next re-scrape silently reintroduces this. The
    presentation layer is the right place to be defensive about it, and the
    underlying data problem is the client's to fix — flagged in DESIGN-NOTES.
    """
    if not text:
        return ""
    stripped = re.sub(r"<[^>]*>", " ", text)
    return re.sub(r"\s+", " ", unescape(stripped)).strip()


def _render(p):
    hero = p["id"] == _hero()["id"]
    on_sale = p.get("sale") and p["sale"] < p["regular"]
    old_price = (
        f'<span class="text-neutral-secondary text-xl line-through latin">EGP {money(p["regular"])}</span>'
        if on_sale else ""
    )

    # Companions come from the product's OWN category now — the bundle was
    # hardcoded to dates, which read absurdly under a bag of parmesan popcorn.
    # Fewer than two companions and the block is dropped: "بضاعة تُشترى معاً"
    # with one item is a claim the layout itself contradicts.
    bundle = [x for x in in_category(p["category"]) if x["id"] != p["id"]][:3]
    bundle_total = sum(x["price"] for x in bundle) + p["price"]

    similar = [x for x in in_category(p["category"]) if x["id"] != p["id"]][:10]
    more = rail_products("Nuts | Seeds & Crackers", "Coffee & Beverages", limit=10)

    # Description: the hero's curated paragraph, or the client's own Arabic
    # short_description. No fallback prose — absence is honest, filler is not.
    desc = DESCRIPTION if hero else _plain(p.get("descAr"))
    desc_html = (
        f'<p class="text-neutral-800 text-base leading-8">{e(desc)}</p>' if desc else ""
    )

    # Accordion: hero keeps its two curated sections; everything else shows
    # the client's own benefits HTML when they wrote one, nothing otherwise.
    if hero:
        acc_items = [("الفوائد", BENEFITS), ("طريقة الحفظ", STORAGE)]
    elif p.get("descHtmlAr"):
        acc_items = [("الفوائد", _clean_client_html(p["descHtmlAr"]))]
    else:
        acc_items = []
    acc_html = accordion(acc_items) if acc_items else ""

    # Every page carries the strip, and every page that CAN now shows the
    # product's own benefits rather than delivery notes.
    #
    # The hero keeps its hand-written tiles: its own benefits list in
    # catalog.json is a single line reading "100جرام", which is the pack
    # weight the size chips already show, so deriving from it would be a
    # downgrade. Everything else derives from the client's `descHtmlAr`, and
    # falls back to the service trio only where the client wrote no benefits
    # at all (35 of 99).
    trust_html = trust_row(BENEFIT_ITEMS) if hero else product_benefits(p, SERVICE_ITEMS)

    # Rating and social proof share a row, split by a hairline, so the two
    # signals read as one block of evidence. The rating numbers are still
    # placeholder (the client's review endpoint returns average_rating "0"
    # for every product); the proof line beside it is real and renders only
    # for genuinely top-ranked products. Both flagged in DESIGN-NOTES.
    proof = sold_proof(p)
    proof_row = (
        f'<span aria-hidden="true" class="bg-neutral-divider w-px h-4"></span>\n                {proof}'
        if proof else ""
    )

    bundle_section = f"""
      <!-- ==================== FREQUENTLY BOUGHT TOGETHER ==================== -->
      <section data-reveal class="py-8">
        <div class="mx-auto px-4 max-w-[1536px]">
          <!-- data-bundle-base is THIS product's price: the total covers the
               product being viewed plus whichever companions are still
               ticked, so unticking one has to take it back off. -->
          <!-- data-product as well as data-bundle: productFrom() only reads
               a [data-product] host, so without it the block described this
               product but could not contribute it to its own bundle. -->
          <div class="bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px]"
               data-bundle data-product data-bundle-base="{p['price']}"
               data-id="{p.get('id', 0)}" data-name="{e(title(p))}"
               data-price="{p['price']}" data-image="{e(p['image'])}">
            <h2 class="mb-6 font-bold text-[#062A1C] text-xl xl:text-2xl">عادة ما يتم شراؤه معاً: أضف هذه العناصر</h2>
            <div class="items-center gap-6 lg:gap-8 grid grid-cols-1 lg:grid-cols-[1fr_auto]">
              <div class="flex flex-col min-w-0">{"".join(bundle_item(x) for x in bundle)}
              </div>
              <div class="flex flex-col items-center gap-3 bg-interaction-base p-6 rounded-xl">
                <span class="text-neutral-secondary text-sm">الإجمالي</span>
                <span class="font-bold text-[#062A1C] text-2xl latin" data-bundle-total>EGP {money(bundle_total)}</span>
                <!-- data-bundle-add, NOT data-add-to-cart: this button adds
                     several products, so it cannot go through the single
                     product handler, which is exactly why it silently did
                     nothing before. -->
                <button type="button" data-bundle-add class="bg-cta hover:bg-cta-hover px-8 py-3 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors">
                  أضف الجميع الى السلة
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>""" if len(bundle) >= 2 else ""

    similar_section = f"""
      <!-- ========================= SIMILAR PRODUCTS ========================= -->
      <section data-reveal class="py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("منتجات مشابهة", "عرض المزيد", "shop-category.html")}
          {carousel("".join(product_card(x) for x in similar))}
        </div>
      </section>""" if similar else ""

    # Breadcrumb category read off the product, not typed in — it said
    # "التمور والفواكه المجففة" on a coffee page until this was made dynamic.
    body = f"""{page_header("", [("الرئيسية", "index.html"),
                                 (p.get("categoryAr") or "المنتجات", "shop-category.html"),
                                 (title(p), None)])}

      <!-- ============================ PRODUCT ============================ -->
      <section class="pt-6 pb-12">
        <div class="items-start gap-8 xl:gap-12 grid lg:grid-cols-2 mx-auto px-4 max-w-[1536px]">

          <!-- Gallery FIRST in the DOM, so the media leads the reading order in
               both directions: in RTL (the default) first means the RIGHT
               column, in LTR the left one. Both are the side the shopper's eye
               starts on, which is where the product photo belongs.
               `items-start` on the grid above is load-bearing — it is what lets
               the gallery be sticky without the column stretching to the full
               row height and pinning it in place. -->
          {product_gallery(p.get("images") or [p["image"]], title(p))}

          <!-- Details second: the RTL-left / LTR-right column. data-product
               lets the cart store read this product straight off the DOM, same
               as a product card. -->
          <div class="flex flex-col gap-5 bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px]"
               data-product data-id="{p.get('id', 0)}" data-name="{e(title(p))}"
               data-price="{p.get('sale') or p.get('price') or 0}" data-image="{e(p['image'])}">
            <div class="flex flex-col gap-3">
              {best_seller_badge(p)}
              <h1 class="font-bold text-[#062A1C] text-2xl xl:text-4xl leading-tight">{e(title(p))}</h1>
              <div class="flex flex-wrap items-center gap-x-3 gap-y-2">
                {rating("4.8", 126)}
                {proof_row}
              </div>
            </div>
            {desc_html}

            {size_chips(p)}

            <!-- Price responds to both controls above it: the size chips
                 repoint it at that SKU's real price, and the quantity stepper
                 multiplies. data-unit-price is the current SIZE's price, kept
                 separate from the displayed total so the multiply never
                 compounds on itself. -->
            <div class="flex flex-wrap items-center gap-3">
              {old_price}
              <span data-price-display data-unit-price="{p.get('sale') or p.get('price') or 0}"
                    class="bg-accent-yellow px-4 py-1.5 rounded-lg font-bold text-[#062A1C] text-2xl latin">EGP {money(p['price'])}</span>
              <span data-price-breakdown hidden
                    class="text-neutral-secondary text-sm latin"></span>
            </div>

            <!-- The stepper IS the add control (Ahmed, 2026-07-26). There is
                 no "add to cart" press any more: + puts the product in the
                 basket, +/- move that line live, and - at 1 removes it. The
                 counter therefore shows the CART's quantity and reads 0 when
                 the product is not in it — a counter that "syncs directly"
                 cannot sit at 1 while the basket holds none.

                 The button beside it is اشتري الان: it opens the summary
                 drawer to carry on, and adds one first if the basket is empty
                 of this product, so pressing "buy now" always buys something.

                 This is the second pass on this block. The first kept an
                 "اضف الى السلة" button that committed the stepper's number;
                 Ahmed's point is that if the counter is bound to the cart, the
                 commit step has nothing left to do. -->
            <div class="flex items-center gap-3">
{qty_stepper(cart_bound=True)}
              <button type="button" data-buy-cta class="flex-1 bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">
                اشتري الان
              </button>
            </div>

            {trust_html}

            <div class="flex flex-wrap justify-between items-center gap-3 bg-interaction-base px-4 py-3 rounded-xl">
              <span class="flex items-center gap-2 font-semibold text-primary text-sm">
                <span class="place-items-center grid bg-primary rounded-full text-white size-5 text-xs">✓</span>
                التوصيل خلال ساعتين في القاهرة الكبرى
              </span>
              <button type="button" data-open="location" class="font-semibold text-cta text-sm underline">تغيير المنطقة</button>
            </div>

            {acc_html}
          </div>
        </div>
      </section>
{bundle_section}

      <!-- ============================= RECIPES ============================= -->
      <section data-reveal class="bg-interaction-base py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("وصفات بالمنتج")}
          <div class="gap-6 xl:gap-8 grid lg:grid-cols-2">{"".join(recipe_card(*r) for r in RECIPES)}
          </div>
        </div>
      </section>
{similar_section}

      <!-- =========================== MORE FROM US =========================== -->
      <section data-reveal class="pb-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر من أبو عوف", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>"""

    return page(
        f"{title(p)} | أبو عوف",
        f"اشتري {title(p)} من أبو عوف أونلاين — جودة عالية وتوصيل سريع لكل مصر.",
        body, "product",
        f"/products/{p['slug']}" if p.get("slug") else "/product",
    )


def build():
    return _render(_hero())


def build_many():
    """One page per catalogue product, product-<id>.html."""
    return [(product_slug(p), _render(p)) for p in PRODUCTS]
