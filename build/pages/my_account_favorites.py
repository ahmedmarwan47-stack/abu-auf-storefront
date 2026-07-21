"""Favourites — Figma 'Account > Favorites > Products' (978:48796)."""
from _account import account_page
from catalog import rail_products
from components import product_grid

SLUG = "my-account-favorites.html"


def build():
    favs = rail_products("Nuts | Seeds & Crackers", "Coffee & Beverages", limit=6)
    content = f"""
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">المفضلة</h1>
            {product_grid(favs, "grid-cols-1 sm:grid-cols-2 xl:grid-cols-3")}"""
    return account_page("المفضلة | أبو عوف", "المنتجات اللي حفظتها في المفضلة.",
                        content, "my-account-favorites", "/my-account/favorites",
                        "المفضلة", "my-account-favorites.html")
