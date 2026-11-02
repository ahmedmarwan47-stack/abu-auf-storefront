"""Shop — all products. Figma 'Collection' (173:17211)."""
from _listing import listing
from bundles import BUNDLES
from catalog import PRODUCTS, nav_categories
from components import bundle_card

SLUG = "shop.html"


def build():
    # Three-item chips are live filters. Every slug here is a real
    # `categorySlug` from catalog.json, so each one has products behind it —
    # previously these all linked to shop-category.html, which shows coffee
    # whatever you picked.
    chips = [("كل المنتجات", "#all", "all")] + [
        (c["ar"], "#" + c["slug"], c["slug"]) for c in nav_categories()
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
        # The mix-and-match offers lead the grid, as the smart-light bundles
        # lead their carousel; they carry data-cat="offers-promotions", so the
        # العروض chip (and the nav's /shop/offers-promotions route) finds them.
        lead=("".join(bundle_card(b, slide=False) for b in BUNDLES), len(BUNDLES)),
    )
