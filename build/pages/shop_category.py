"""
Category listing — Figma 'Collection' (173:17211).

Stands in for every /shop/<category> route in the static export. Coffee is the
worked example, matching the Figma; the chips are that category's real
sub-categories.
"""
from _listing import listing
from catalog import in_category

SLUG = "shop-category.html"

CATEGORY_AR = "القهوة"
INTRO = ("أكثر من 30 نكهة قهوة لذيذة تنعش الحواس — من التركي والبرازيلي "
         "للإسبريسو والقهوة المطحونة طازة، محمصة على أصولها ومعبأة تحافظ على "
         "الريحة لآخر فنجان.")

SUBCATEGORIES = [
    "القهوة", "قهوة تركي", "قهوة برازيلي", "قهوة مطحونة طازجة",
    "إسبريسو", "قهوة سريعة التحضير", "مشروبات ساخنة",
]


def build():
    return listing(
        title_text=f"{CATEGORY_AR} | أبو عوف",
        description="تسوق قهوة أبو عوف: تركي، برازيلي، إسبريسو وقهوة مطحونة طازة "
                    "بأفضل الأسعار وتوصيل لكل مصر.",
        heading=CATEGORY_AR,
        trail=[("الرئيسية", "index.html"), ("المنتجات", "shop.html"), (CATEGORY_AR, None)],
        chips=[(s, "shop-category.html") for s in SUBCATEGORIES],
        products=in_category("Coffee & Beverages"),
        page_id="shop-category",
        path="/shop/coffee-beverage",
        intro=INTRO,
        active_chip=CATEGORY_AR,
    )
