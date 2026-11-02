"""
Mix-and-match offers ("كوّن عرضك") — the single source of truth.

The mechanic is the one the smart-light bundle builder proved out
(github.com/ahmedmarwan47-stack/smart-light, `mirror/_bundle/bundle.js`),
fitted to this storefront and to Abu Auf's own offer pages
(abuauf.com/offers/<slug>):

  * an offer is ONE card in the grid and ONE fixed price;
  * opening it shows a builder: the shopper spreads `size` units across the
    offer's flavours however they like;
  * any mix totalling exactly `size` costs `price` — the price never moves with
    the mix;
  * the finished offer lands in the cart as ONE line, with the mix written
    under its name, and a quantity counter like any other product.

The offer page is the PRODUCT page (product.py `_render(p, offer=...)`) of the
offer's `base` SKU, with the builder standing in for the size chips, price and
buy block — so it carries every section a product page carries, and a change
to the product page reaches it on the next build.

Change an offer here — rename it, resize it, add a flavour — and the card on
the shop grid, the card in the home "offers" rail, the offer page and the cart
line all follow. Nothing about an offer is typed anywhere else.

WHAT IS REAL (DESIGN-NOTES §1, "Mix-and-match offers")
------------------------------------------------------
`maamoul` is built from data already in catalog.json: the client sells this
exact offer as four fixed SKUs (1571, 1572, 39400, 62393), each FOUR boxes for
EGP 250 against a regular EGP 325, across five flavours. The builder is those
four SKUs generalised into one choice.
  * price / compare-at / size / flavours — those SKUs' own fields and names.
  * "12 قطعة" per box — printed on every box in the client's own photographs.
  * photos — the client's own shots of those SKUs; each flavour's picture is
    that flavour's box cropped out of them (images/abuauf/offers/).
  * `max_each` = 2 — no real SKU carries more than two of one flavour, so the
    builder never offers a mix the client has never sold.
  * in-house: the offer's Arabic/English name and the builder sentence.
"""

BUNDLES = [
    {
        "slug": "maamoul-offer-any-4-boxes",
        # Stable numeric key for the listing's "newest" sort, which compares
        # data-id as a number. Out of the catalogue's id range on purpose.
        "num_id": 900001,
        # The catalogue SKU whose product page this offer page is built from:
        # its rank, points, reviews block, related list and rails are the
        # offer's. `sources` are the fixed SKUs this builder generalises; their
        # own pages link here.
        "base": 1571,
        "sources": [1571, 1572, 39400, 62393],
        "name_ar": "عرض معمول - اختر 4 علب",
        "name_en": "Maamoul offer - pick any 4 boxes",
        "tagline_ar": "اختر 4 علب معمول بالنكهات اللي تحبها — بسعر ثابت",
        # First sentence is the client's own copy for SKU 1571 (descAr); the
        # second replaces its fixed flavour list, which the builder makes untrue.
        "desc_ar": ("حلي فنجان القهوة اليومي المفضل لديك وأضف له لمسة عربية غنية بألذ "
                    "النكهات مع عرض المعمول من أبوعوف الحصري. اختار 4 علب ووزّعها على "
                    "النكهات الخمسة زي ما تحب — السعر ثابت مهما اختلف الاختيار."),
        "desc_en": ("Sweeten your favourite daily cup of coffee with a rich Arabian "
                    "touch from Abu Auf's exclusive maamoul offer. Pick 4 boxes and "
                    "spread them across the five flavours however you like — the "
                    "price stays the same whatever you choose."),
        "unit_ar": "علبة",
        "unit_plural_ar": "علب",
        "unit_plural_en": "boxes",
        "pack_ar": "12 قطعة",      # printed on every box
        "pack_en": "12 pieces",
        "size": 4,
        "price": 250,
        "compare_at": 325,         # the four real SKUs' own `regular`
        "max_each": 2,
        "images": [
            "images/abuauf/products/330-thumb.webp",
            "images/abuauf/products/331-thumb.webp",
            "images/abuauf/products/332-thumb.webp",
            "images/abuauf/products/349-thumb.webp",
        ],
        "items": [
            {"key": "plain",           "short": "سادة",          "ar": "معمول سادة",              "en": "Plain",           "img": "images/abuauf/offers/maamoul-plain.webp"},
            {"key": "cinnamon",        "short": "قرفة",          "ar": "معمول بالقرفة",           "en": "Cinnamon",        "img": "images/abuauf/offers/maamoul-cinnamon.webp"},
            {"key": "chocolate",       "short": "شيكولاتة",      "ar": "معمول بالشيكولاتة",       "en": "Chocolate",       "img": "images/abuauf/offers/maamoul-chocolate.webp"},
            {"key": "white-chocolate", "short": "شيكولاتة بيضاء", "ar": "معمول بالشيكولاتة البيضاء", "en": "White Chocolate", "img": "images/abuauf/offers/maamoul-white-chocolate.webp"},
            {"key": "strawberry",      "short": "فراولة",        "ar": "معمول بالفراولة",         "en": "Strawberry",      "img": "images/abuauf/offers/maamoul-strawberry.webp"},
        ],
    },
]


def units_ar(b, n):
    """Arabic count noun: 3..10 take the plural (4 علب), everything else the
    singular (1 علبة, 11 علبة)."""
    return b["unit_plural_ar"] if 3 <= n <= 10 else b["unit_ar"]


def pack_line(b):
    """"4 علب · 12 قطعة لكل علبة" and its English twin, built in ONE place so
    the page and the i18n dictionary cannot drift apart."""
    ar = f"{b['size']} {units_ar(b, b['size'])}"
    en = f"{b['size']} {b['unit_plural_en']}"
    if b.get("pack_ar"):
        ar += f" · {b['pack_ar']} لكل {b['unit_ar']}"
        en += f" · {b['pack_en']} each"
    return ar, en


def offer_slug(b):
    """Output filename for an offer's page — used by the cards and the page
    builder alike, so a card can never link to a page that was not built."""
    return f"offer-{b['slug']}.html"


def offer_for_source(pid):
    """The offer a fixed catalogue SKU belongs to, if any."""
    return next((b for b in BUNDLES if pid in b.get("sources", [])), None)
