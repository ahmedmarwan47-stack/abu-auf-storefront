"""Shop — all products. Figma 'Collection' (173:17211)."""
from _listing import listing
from catalog import PRODUCTS, nav_categories

SLUG = "shop.html"


def build():
    chips = [("كل المنتجات", "shop.html")] + [
        (c["ar"], "shop-category.html") for c in nav_categories()
    ]
    return listing(
        title_text="كل المنتجات | أبو عوف",
        description="تصفح كل منتجات أبو عوف: قهوة، مكسرات، تمور وفواكه مجففة، "
                    "سناكس صحية، بهارات وهدايا.",
        heading="كل المنتجات",
        trail=[("الرئيسية", "index.html"), ("كل المنتجات", None)],
        chips=chips,
        products=PRODUCTS,
        page_id="shop",
        path="/shop",
        active_chip="كل المنتجات",
    )
