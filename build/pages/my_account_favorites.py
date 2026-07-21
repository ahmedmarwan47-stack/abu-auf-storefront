"""Favourites — Figma 'Account > Favorites > Products' (978:48796)."""
from _account import account_page
from catalog import PRODUCTS
from components import product_grid

SLUG = "my-account-favorites.html"


def build():
    # The whole catalogue ships in the DOM and scripts.js reveals whichever
    # products are actually saved in `abuauf:favs`, hiding the rest. This is
    # the same "filter what is already rendered" approach the listing chips
    # use: the card markup still comes from components.product_card alone,
    # and the page needs no fetch, so it keeps working from file://.
    #
    # This page used to hard-code six products regardless of what the shopper
    # had hearted — the hearts themselves were inert, so nothing could have
    # reached it anyway. Those same six are now the first-visit seed in
    # scripts.js (FAVS_SEED), so a fresh browser still sees this design.
    content = f"""
            <div class="flex items-baseline gap-2">
              <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">المفضلة</h1>
              <span class="text-neutral-secondary text-sm">(<span class="latin" data-favs-count>0</span> منتج)</span>
            </div>
            {product_grid(PRODUCTS, "grid-cols-1 sm:grid-cols-2 xl:grid-cols-3", attrs="data-favs-grid")}
            <div data-favs-empty hidden class="flex flex-col items-center gap-3 py-16 text-center">
              <p class="font-bold text-[#062A1C] text-lg">لا توجد منتجات في المفضلة</p>
              <p class="text-neutral-secondary text-sm">المنتجات اللي تحفظها هتظهر هنا.</p>
              <a href="shop.html"
                 class="flex justify-center items-center bg-cta hover:bg-cta-hover mt-2 px-6 rounded-full min-h-11 font-semibold text-white text-sm transition-colors">تصفح المنتجات</a>
            </div>"""
    return account_page("المفضلة | أبو عوف", "المنتجات اللي حفظتها في المفضلة.",
                        content, "my-account-favorites", "/my-account/favorites",
                        "المفضلة", "my-account-favorites.html")
