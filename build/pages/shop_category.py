"""
Category listing — Figma 'Collection' (173:17211).

Stands in for every /shop/<category> route in the static export. Coffee is the
worked example, matching the Figma and the live abuauf.com coffee category; the
chips are that category's REAL sub-categories.

The sub-category chips are LIVE filters, keyed off each product's real
membership. `fetch_subcategories.py` reads every product's `categories[]` from
the Store API and writes the child-category slugs into `subCats`, so `_subcat`
is now a lookup, not the old keyword guess. The slugs and Arabic labels below
are Abu Auf's own (read off the live coffee category's filter bar).

Because our catalogue is a 99-product subset, most coffee sub-categories hold
none of our products; `build()` drops every empty chip, so only the
sub-categories our sample actually covers are shown.
"""
from _listing import listing
from catalog import in_category

SLUG = "shop-category.html"

CATEGORY_AR = "القهوة"
INTRO = ("أكثر من 30 نكهة قهوة لذيذة تنعش الحواس — من التركي والبرازيلي "
         "للإسبريسو والقهوة المطحونة طازة، محمصة على أصولها ومعبأة تحافظ على "
         "الريحة لآخر فنجان.")

# Chip label → real sub-category slug, in the live site's order. "all" shows
# everything; every other slug is a real child of category 34 (Coffee &
# Beverages) and matches the `subCats` written by fetch_subcategories.py.
SUBCATEGORIES = [
    ("القهوة", "all"),
    ("قهوة تركي معبأة", "turkish-coffee-packed"),
    ("قهوة برازيلي معبأة", "brazilian-coffee-packed"),
    ("قهوة مطحونة فريش", "fresh-grounded-coffee"),
    ("قهوة سريعة التحضير", "instant-coffee"),
    ("إسبريسو", "espresso"),
    ("قهوة بالنكهات", "flavored-coffee"),
    ("قهوة فرنسية", "french-coffee"),
    ("مشروبات ساخنه", "hot-drinks"),
    ("قهوة خضراء", "green-coffee"),
    ("قهوة عربي", "arabic-coffee"),
    ("عصائر", "juices"),
]

# The real child slugs of Coffee & Beverages, so a product's coffee
# sub-category is picked out of its full `subCats` (which can also list
# cross-listed parents like offers/ramadan). A coffee SKU carries exactly one
# of these in our data; the first is its chip. Anything with none falls back to
# the parent slug, so it shows only under "all", never under a wrong chip.
_COFFEE_SUBS = {slug for _, slug in SUBCATEGORIES if slug != "all"}


def _subcat(p):
    for slug in p.get("subCats", []):
        if slug in _COFFEE_SUBS:
            return slug
    return "coffee-beverage"


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
