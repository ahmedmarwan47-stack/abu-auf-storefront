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

from catalog import PRODUCTS, e, in_category, money, rail_products, title
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

# Generic benefit trio, shown on the products the client never wrote benefit
# copy for (35 of 99). It used to be the site-service strip (delivery / returns
# / branch count), which read as a delivery notice sitting where every other
# product shows benefits — a developer opening two pages saw two different
# spec rows (Ahmed, 2026-07-29: "make it generic for consistency and developer
# hand-off, I don't want to confuse them"). Now the spec row is product benefits
# on all 99: the client's own lines where they exist, this generic set where
# they don't.
#
# Brand-level reassurance only — no auditable supply-chain claim (nothing like
# "third-party tested"), same restraint as the hero copy. Still OUR unsigned
# Arabic; flagged in DESIGN-NOTES pending client sign-off like every other
# in-house string in this build. Single-line tiles (empty subtitle) so they
# match the shape of the client-benefit tiles beside them.
GENERIC_BENEFITS = [
    ("leaf", "منتج مختار بعناية", ""),
    ("bolt", "طازج وعالي الجودة", ""),
    ("shield", "جودة أبو عوف المضمونة", ""),
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

# Generic product FAQ — IDENTICAL on all 99 pages by design (Ahmed, 2026-07-29).
# There is no per-product FAQ data in the catalogue, and this project does not
# invent product content, so every answer here restates something the site
# already commits to elsewhere: the two-hour delivery row on this same page, the
# 14-day window on return-policy.html, and the size chips above. Storage and
# freshness are generic handling advice, not a claim about this SKU. Making it
# uniform is the point — the developer handoff gets one FAQ component that is the
# same on every page rather than a section that appears only where data exists.
_P = 'class="text-neutral-800 leading-7"'
FAQ_ITEMS = [
    ("كم يستغرق توصيل الطلب؟",
     f'<p {_P}>التوصيل خلال ساعتين داخل القاهرة الكبرى، ويصل إلى باقي المحافظات حسب المنطقة. يمكنك تغيير منطقة التوصيل من أعلى الصفحة.</p>'),
    ("هل يمكنني استرجاع المنتج؟",
     f'<p {_P}>نعم، يمكنك الاسترجاع خلال 14 يوماً من تاريخ الاستلام وفق سياسة الاسترجاع المتبعة.</p>'),
    ("كيف أحافظ على المنتج طازجاً؟",
     f'<p {_P}>يُحفظ المنتج في مكان جاف بعيداً عن الرطوبة وأشعة الشمس المباشرة ومصادر الحرارة للحفاظ على نكهته وطزاجته.</p>'),
    ("هل تتوفر أحجام أو عبوات أخرى؟",
     f'<p {_P}>تختلف الأحجام المتاحة حسب المنتج، وتظهر خيارات الحجم أعلى الصفحة عند توفر أكثر من عبوة.</p>'),
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
    # falls back to GENERIC_BENEFITS — a generic PRODUCT-benefit trio, not the
    # old service strip — only where the client wrote no benefits at all (35 of
    # 99), so the spec row reads as benefits on every page.
    trust_html = trust_row(BENEFIT_ITEMS) if hero else product_benefits(p, GENERIC_BENEFITS)

    # Related products — an INTERACTIVE "you may also like" widget in the sticky
    # media column (Ahmed, 2026-07-29): each row a checkbox, a running total and
    # an "add all" button, reusing the bundle machinery in scripts.js. It is a
    # [data-bundle] box with NO data-product and no data-bundle-base, so both the
    # total and the add cover the RELATED items only — the current product is not
    # folded in the way "frequently bought together" folds it (productFrom walks
    # up and finds no [data-product] host on this side, so the base is empty).
    # Capped to four so the media side stays shorter than the scrollable info
    # side; dropped entirely when the category has no companions.
    related_list = ""
    if similar:
        picks = similar[:4]
        related_total = sum(x["price"] for x in picks)
        rows = "".join(bundle_item(x) for x in picks)
        related_list = f"""
          <div data-bundle class="flex flex-col bg-white shadow-custom4 p-4 xl:p-5 rounded-[20px]">
            <h2 class="mb-1 px-2 font-bold text-[#062A1C] text-base xl:text-lg">قد يعجبك أيضاً</h2>
            <div class="flex flex-col">{rows}
            </div>
            <div class="flex flex-wrap justify-between items-center gap-3 mt-3 px-2 pt-3 border-neutral-divider border-t">
              <div class="flex flex-col">
                <span class="text-neutral-secondary text-xs">الإجمالي</span>
                <span class="font-bold text-[#062A1C] text-lg latin" data-bundle-total>EGP {money(related_total)}</span>
              </div>
              <button type="button" data-bundle-add class="bg-cta hover:bg-cta-hover px-5 py-2.5 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors">أضف الكل للسلة</button>
            </div>
          </div>"""

    # Generic FAQ, same on every page — sits in the scrollable info column
    # beneath the client's benefits accordion. See FAQ_ITEMS for why it is
    # uniform rather than per-product.
    faq_html = f"""
            <div class="flex flex-col gap-2">
              <h2 class="mt-1 font-bold text-[#062A1C] text-lg xl:text-xl">الأسئلة الشائعة</h2>
              {accordion(FAQ_ITEMS)}
            </div>"""

    # Breadcrumb category read off the product, not typed in — it said
    # "التمور والفواكه المجففة" on a coffee page until this was made dynamic.
    body = f"""{page_header("", [("الرئيسية", "index.html"),
                                 (p.get("categoryAr") or "المنتجات", "shop-category.html"),
                                 (title(p), None)])}

      <!-- ============================ PRODUCT ============================ -->
      <section class="pt-6 pb-12">
        <div class="items-start gap-8 xl:gap-12 grid lg:grid-cols-2 mx-auto px-4 max-w-[1536px]">

          <!-- Media column FIRST in the DOM, so it leads the reading order in
               both directions: in RTL (the default) first means the RIGHT
               column, in LTR the left one. It holds the gallery AND the related
               list, and the WHOLE column is the sticky one now — `items-start`
               on the grid is load-bearing, it is what lets a grid child be
               shorter than its row so sticky has room to move. Sticky scoped to
               lg; below it the columns stack and there is nothing to scroll
               past. Works only because <main> is overflow-x-clip (see page()).
               On mobile the gallery and related list simply stack in DOM order
               (gallery, then related) — Ahmed asked to leave the mobile order
               as-is rather than reorder the related list to the bottom. -->
          <div class="flex flex-col gap-6 min-w-0 lg:self-start lg:sticky lg:top-[60px]">
          {product_gallery(p.get("images") or [p["image"]], title(p), p)}
          {related_list}
          </div>

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
                {sold_proof(p)}
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
            <!-- data-buy-block: the sticky re-CTA watches this row and appears
                 once it has scrolled above the viewport. -->
            <div data-buy-block class="flex items-center gap-3">
{qty_stepper(cart_bound=True)}
              <button type="button" data-buy-cta class="flex-1 bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">
                اشتري الان
              </button>
            </div>

            <!-- Divider between the CTA and the product specs below it. It is a
                 plain flex child, so it sits inside the card's own p-6/xl:p-8
                 padding and lines up with every other row rather than bleeding
                 to the card edges (Ahmed, 2026-07-29). -->
            <div class="border-neutral-divider border-t" role="separator"></div>

            {trust_html}

            <div class="flex flex-wrap justify-between items-center gap-3 bg-interaction-base px-4 py-3 rounded-xl">
              <span class="flex items-center gap-2 font-semibold text-primary text-sm">
                <span class="place-items-center grid bg-primary rounded-full text-white size-5 text-xs">✓</span>
                التوصيل خلال ساعتين في القاهرة الكبرى
              </span>
              <button type="button" data-open="location" class="font-semibold text-cta text-sm underline">تغيير المنطقة</button>
            </div>

            {acc_html}
            {faq_html}
          </div>
        </div>
      </section>

      <!-- ============================= RECIPES ============================= -->
      <section data-reveal class="bg-interaction-base py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("وصفات بالمنتج")}
          <div class="gap-6 xl:gap-8 grid lg:grid-cols-2">{"".join(recipe_card(*r) for r in RECIPES)}
          </div>
        </div>
      </section>

      <!-- =========================== MORE FROM US =========================== -->
      <section data-reveal class="pb-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر من أبو عوف", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>

      <!-- ========================= STICKY BUY BAR =========================
           A re-CTA that appears once the real buy block scrolls above the
           viewport: fixed to the BOTTOM on mobile, and under the sticky nav at
           the TOP on desktop (lg). It owns no state — its −/＋ and CTA forward
           to the real cart-bound stepper and buy button, and its title/price/
           quantity mirror them, so there is one writer of the cart. Enter/exit
           and the hidden rest state live in styles.css (.sticky-buybar); JS
           only toggles .is-visible. -->
      <div data-sticky-buybar aria-hidden="true"
           class="sticky-buybar fixed inset-x-0 bottom-0 lg:bottom-auto lg:top-12 z-30
                  bg-white border-neutral-divider border-t lg:border-t-0 lg:border-b">
        <div class="flex items-center gap-3 lg:gap-6 mx-auto px-4 max-w-[1536px] py-3">
          <img src="{e(p['image'])}" alt=""
               class="hidden sm:block bg-interaction-base p-1 rounded-xl w-12 xl:w-14 h-12 xl:h-14 object-contain shrink-0" />
          <div class="flex flex-col flex-1 min-w-0">
            <p class="font-bold text-[#062A1C] text-sm xl:text-base truncate">{e(title(p))}</p>
            <span data-sticky-price class="font-bold text-primary text-sm xl:text-base latin">EGP {money(p['price'])}</span>
          </div>
          <!-- Quantity mirror — buttons forward to the real cart-bound stepper.
               dir="ltr" so the + always sits on the RIGHT (Ahmed, 2026-07-29):
               in the page's RTL flow the − would otherwise take the right slot.
               The digit is latin already, so forcing LTR here changes nothing
               but the button order. -->
          <div dir="ltr" class="inline-flex items-center gap-1 bg-white p-1 border border-neutral-divider rounded-full shrink-0">
            <button type="button" data-sticky-step="-1" aria-label="إنقاص"
                    class="place-items-center grid border border-neutral-divider hover:bg-interaction-base rounded-full size-9 text-[#062A1C] transition-colors"><span class="w-4 h-4">{ICON['minus']}</span></button>
            <span data-sticky-qty class="min-w-[2ch] font-bold text-[#062A1C] text-sm text-center latin">1</span>
            <button type="button" data-sticky-step="1" aria-label="زيادة"
                    class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full size-9 text-white transition-colors"><span class="w-4 h-4">{ICON['plus']}</span></button>
          </div>
          <!-- Buy now — forwards to the real buy CTA, which opens the side cart
               after the quantity is set (Ahmed, 2026-07-29). This mirrors the
               main block's own button; it is deliberately NOT a plain add. -->
          <button type="button" data-sticky-buy
                  class="bg-cta hover:bg-cta-hover px-5 xl:px-8 py-2.5 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors shrink-0">اشتري الان</button>
        </div>
      </div>"""

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
