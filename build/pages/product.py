"""Product detail — Figma 'Product' (383:33745)."""
from catalog import PRODUCTS, e, in_category, money, rail_products, title
from components import (
    ICON, accordion, button, carousel, page, page_header, product_card,
    product_gallery, qty_stepper, rating, recipe_card, variant_chips,
    bundle_item, section_heading,
)

SLUG = "product.html"

# Worked example: a real catalogue item, chosen to match the Figma's
# chocolate-dates hero.
def _hero():
    for want in ("معمول بعجوه المجدول مغطى بالشيكولاته",
                 "تمر مجدول محشو بالمكسرات"):
        for p in PRODUCTS:
            if want in (p.get("nameAr") or ""):
                return p
    return in_category("Dates & Dried Fruits")[0]


DESCRIPTION = (
    "تمر مجدول فاخر محشو بالمكسرات ومغطى بطبقة من الشيكولاتة الغنية — تحلية "
    "طبيعية بدون سكر مضاف، مثالية للضيافة أو كهدية. كل قطعة متغلفة بعناية "
    "للحفاظ على طزاجتها وقوامها الطري."
)

BENEFITS = """
                      <ul class="flex flex-col gap-2 ps-5 list-disc">
                        <li>مصدر طبيعي للطاقة والألياف الغذائية</li>
                        <li>غني بالبوتاسيوم والمغنيسيوم</li>
                        <li>بدون سكر مضاف أو ألوان صناعية</li>
                      </ul>"""

STORAGE = """
                      <ul class="flex flex-col gap-2 ps-5 list-disc">
                        <li>يحفظ في مكان جاف وبعيد عن أشعة الشمس المباشرة</li>
                        <li>يفضل الحفظ في الثلاجة بعد الفتح</li>
                        <li>يستهلك خلال 3 شهور من تاريخ الفتح</li>
                      </ul>"""

RECIPES = [
    ("images/abuauf/site/4-1-1.webp", "الوصفات", "كيكة التمر بالقرفة والشيكولاتة البيضاء",
     "وصفة سهلة تجمع بين حلاوة التمر ودفء القرفة، جاهزة في أقل من ساعة.", 45),
    ("images/abuauf/site/big.webp", "الوصفات", "فتوتشيني ألفريدو دجاج مع الكاجو",
     "طبق كريمي غني بالمكسرات، مناسب لعشاء سريع في نص ساعة.", 30),
]


def build():
    p = _hero()
    on_sale = p.get("sale") and p["sale"] < p["regular"]
    old_price = (
        f'<span class="text-neutral-secondary text-xl line-through latin">EGP {money(p["regular"])}</span>'
        if on_sale else ""
    )

    bundle = [x for x in in_category("Dates & Dried Fruits") if x["id"] != p["id"]][:3]
    bundle_total = sum(x["price"] for x in bundle) + p["price"]

    similar = [x for x in in_category(p["category"]) if x["id"] != p["id"]][:10]
    more = rail_products("Nuts | Seeds & Crackers", "Coffee & Beverages", limit=10)

    body = f"""{page_header("", [("الرئيسية", "index.html"),
                                 ("التمور والفواكه المجففة", "shop-category.html"),
                                 (title(p), None)])}

      <!-- ============================ PRODUCT ============================ -->
      <section class="pt-6 pb-12">
        <div class="items-start gap-8 xl:gap-12 grid lg:grid-cols-2 mx-auto px-4 xl:px-[190px] max-w-[1920px]">

          <!-- RTL start: details -->
          <div class="flex flex-col gap-5 bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px]">
            <div class="flex flex-col gap-3">
              <h1 class="font-bold text-[#062A1C] text-2xl xl:text-4xl leading-tight">{e(title(p))}</h1>
              {rating("4.8", 126)}
            </div>
            <p class="text-neutral-800 text-base leading-8">{e(DESCRIPTION)}</p>

            {variant_chips([("500 جم", False), ("250 جم", True), ("100 جم", False)], "weight")}

            <div class="flex items-center gap-3">
              {old_price}
              <span class="bg-accent-yellow px-4 py-1.5 rounded-lg font-bold text-[#062A1C] text-2xl latin">EGP {money(p['price'])}</span>
            </div>

            <div class="flex items-center gap-3">
{qty_stepper()}
              <button type="button" data-add-to-cart class="flex-1 bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">
                اضف الى السلة
              </button>
            </div>
            <a href="checkout.html" class="py-3.5 border border-cta rounded-full font-semibold text-cta text-base text-center hover:bg-interaction-base transition-colors">
              اشتري الان
            </a>

            <div class="flex flex-wrap justify-between items-center gap-3 bg-interaction-base px-4 py-3 rounded-xl">
              <span class="flex items-center gap-2 font-semibold text-primary text-sm">
                <span class="place-items-center grid bg-primary rounded-full text-white size-5 text-xs">✓</span>
                التوصيل خلال ساعتين في القاهرة الكبرى
              </span>
              <button type="button" data-open="location" class="font-semibold text-cta text-sm underline">تغيير المنطقة</button>
            </div>

            {accordion([("الفوائد", BENEFITS), ("طريقة الحفظ", STORAGE)])}
          </div>

          <!-- RTL end: gallery -->
          {product_gallery(p["image"], [p["image"]], title(p))}
        </div>
      </section>

      <!-- ==================== FREQUENTLY BOUGHT TOGETHER ==================== -->
      <section class="py-8">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          <div class="bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px]">
            <h2 class="mb-6 font-bold text-[#062A1C] text-xl xl:text-2xl">عادة ما يتم شراؤه معاً: أضف هذه العناصر</h2>
            <div class="items-center gap-6 lg:gap-8 grid grid-cols-1 lg:grid-cols-[1fr_auto]">
              <div class="flex flex-col min-w-0">{"".join(bundle_item(x) for x in bundle)}
              </div>
              <div class="flex flex-col items-center gap-3 bg-interaction-base p-6 rounded-xl">
                <span class="text-neutral-secondary text-sm">الإجمالي</span>
                <span class="font-bold text-[#062A1C] text-2xl latin">EGP {money(bundle_total)}</span>
                <button type="button" data-add-to-cart class="bg-cta hover:bg-cta-hover px-8 py-3 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors">
                  أضف الجميع الى السلة
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================= RECIPES ============================= -->
      <section class="bg-interaction-base py-12">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          {section_heading("وصفات بالمنتج")}
          <div class="gap-6 xl:gap-8 grid lg:grid-cols-2">{"".join(recipe_card(*r) for r in RECIPES)}
          </div>
        </div>
      </section>

      <!-- ========================= SIMILAR PRODUCTS ========================= -->
      <section class="py-12">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          {section_heading("منتجات مشابهة", "عرض المزيد", "shop-category.html")}
          {carousel("".join(product_card(x) for x in similar))}
        </div>
      </section>

      <!-- =========================== MORE FROM US =========================== -->
      <section class="pb-12">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          {section_heading("تسوق اكتر من أبو عوف", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>"""

    return page(
        f"{title(p)} | أبو عوف",
        f"اشتري {title(p)} من أبو عوف أونلاين — جودة عالية وتوصيل سريع لكل مصر.",
        body, "product", "/product",
    )
