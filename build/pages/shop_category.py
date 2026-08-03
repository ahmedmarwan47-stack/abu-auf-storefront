"""
Category listing — Figma 'Collection' (173:17211).

Stands in for every /shop/<category> route in the static export. Coffee is the
worked example, matching the Figma; the chips are that category's real
sub-categories.

The sub-category chips are LIVE filters. There is no sub-category taxonomy on
the products, though — every coffee SKU is just categorySlug "coffee-beverage" —
so each product's sub-category is DERIVED from its Arabic name by keyword (see
_subcat). Best effort, flagged in DESIGN-NOTES; when the client ships a real
taxonomy this classifier is the one thing to replace.
"""
from _listing import listing
from catalog import in_category

SLUG = "shop-category.html"

CATEGORY_AR = "القهوة"
INTRO = ("أكثر من 30 نكهة قهوة لذيذة تنعش الحواس — من التركي والبرازيلي "
         "للإسبريسو والقهوة المطحونة طازة، محمصة على أصولها ومعبأة تحافظ على "
         "الريحة لآخر فنجان.")

# Chip label → filter slug (the sub-category routes in MAIN_MENU). Figma order.
# "all" is the "show everything" chip; the rest filter on the derived slug.
SUBCATEGORIES = [
    ("القهوة", "all"),
    ("قهوة تركي", "turkish-coffee"),
    ("قهوة برازيلي", "brazilian-coffee"),
    ("قهوة مطحونة طازجة", "fresh-grounded-coffee"),
    ("إسبريسو", "espresso"),
    ("قهوة سريعة التحضير", "instant-coffee"),
    ("مشروبات ساخنة", "hot-drinks"),
]

# Name-keyword → slug, in PRIORITY order: a product is assigned to the first
# slug whose keyword its name carries, so "برازيلى محوج" is brazilian, not the
# spiced/ground default. Anything unmatched (plain/spiced أبو عوف beans) is
# fresh-ground, the sensible catch-all for whole/ground coffee.
_SUBCAT_RULES = [
    ("turkish-coffee",   ("تركي",)),
    ("brazilian-coffee", ("برازيل",)),
    ("instant-coffee",   ("سريعة التحضير", "سريعه", "سريعة التحضير")),
    ("espresso",         ("إسبريسو", "اسبريسو", "اسبرسو", "espresso")),
    ("hot-drinks",       ("عرب",)),
]
_DEFAULT_SUBCAT = "fresh-grounded-coffee"


def _subcat(p):
    name = p.get("nameAr", "") or ""
    for slug, keywords in _SUBCAT_RULES:
        if any(k in name for k in keywords):
            return slug
    return _DEFAULT_SUBCAT


def build():
    products = in_category("Coffee & Beverages")

    # Count products per derived sub-category, then drop any sub-category chip
    # with zero products (e.g. إسبريسو in this sample) — an empty filter reads
    # as broken. The "all" chip always stays.
    counts = {}
    for p in products:
        counts[_subcat(p)] = counts.get(_subcat(p), 0) + 1
    chips = [
        (label, "shop-category.html", slug)
        for (label, slug) in SUBCATEGORIES
        if slug == "all" or counts.get(slug, 0) > 0
    ]

    return listing(
        title_text=f"{CATEGORY_AR} | أبو عوف",
        description="تسوق قهوة أبو عوف: تركي، برازيلي، إسبريسو وقهوة مطحونة طازة "
                    "بأفضل الأسعار وتوصيل لكل مصر.",
        heading=CATEGORY_AR,
        trail=[("الرئيسية", "index.html"), ("المنتجات", "shop.html"), (CATEGORY_AR, None)],
        chips=chips,
        products=products,
        page_id="shop-category",
        path="/shop/coffee-beverage",
        intro=INTRO,
        active_chip=CATEGORY_AR,
        cat_of=_subcat,
    )
