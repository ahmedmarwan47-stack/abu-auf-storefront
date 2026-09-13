"""
Shared data access for the Abu Auf static build.

Everything page builders know about products, categories and prices comes
through here, so a change to (say) price formatting or which products feed a
rail happens in one place and reaches every page on the next build.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = os.path.join(ROOT, "static-export")
CATALOG_PATH = os.path.join(EXPORT, "data", "catalog.json")

_data = json.load(open(CATALOG_PATH, encoding="utf-8"))


def _clean_name(s):
    """
    Repair the two ways the scrape damages a product name.

    The Store API returns English names with their entities still encoded
    (`Gift Basket &#8220;Small&#8221;`). Those reach the page as attribute
    values, so the language toggle painted the literal `&#8220;` on screen.

    The Arabic names come out of the storefront's flight payload, where the
    same quoted suffix is a JSON string escape — and for three products the
    quoted part was lost and only its backslashes survived
    (`سلة هدايا \\`). A trailing backslash is never part of a real name, so
    strip it rather than print it.

    Deliberately NOT rewritten into catalog.json: the scrapers own that file
    and would undo it. Cleaning on load means a re-scrape stays fixed.
    """
    s = html.unescape(str(s or ""))
    s = s.replace("\\", " ")
    return " ".join(s.split())


for _p in _data["products"]:
    for _k in ("name", "nameAr"):
        if _p.get(_k):
            _p[_k] = _clean_name(_p[_k])
    for _sz in _p.get("sizes") or []:
        for _k in ("name", "nameAr", "label"):
            if _sz.get(_k):
                _sz[_k] = _clean_name(_sz[_k])

PRODUCTS = _data["products"]

# Rank within the product's OWN category, derived from the same real
# `popularityRank` (WooCommerce total-sales order across the client's whole
# 653-product store). Nothing is invented here — it is the existing ranking,
# read at a narrower scope.
#
# Why it exists: the store-wide top 20 is dominated by snacks and offers, so
# most categories had no badged product at all and a shopper browsing spices
# saw the signal nowhere. "Best seller in spices" is a true statement about a
# spice that outsells the other spices, and it is the claim a category page
# can actually support.
#
# Products with no popularityRank are left unranked rather than sorted last:
# absent data is not a low ranking.
_by_category = {}
for _p in PRODUCTS:
    if _p.get("popularityRank"):
        _by_category.setdefault(_p.get("category"), []).append(_p)
for _cat, _members in _by_category.items():
    _members.sort(key=lambda x: x["popularityRank"])
    for _i, _m in enumerate(_members, start=1):
        _m["categoryRank"] = _i
        _m["categorySize"] = len(_members)
CATEGORIES = _data["categories"]
BY_API_NAME = {c["name"]: c for c in CATEGORIES}
BY_SLUG = {c["slug"]: c for c in CATEGORIES if c.get("slug")}

# Real branch count, read from the branches file rather than typed in, so the
# product page's "N فرع" can never drift from branches.html.
# The file is a list of GOVERNORATES, each holding its own branches — summing
# the inner lists gives 316; taking len() of the outer one gives 25, which is
# the governorate count and the easy mistake to make here.
_BRANCHES_PATH = os.path.join(EXPORT, "data", "branches.json")
try:
    _govs = json.load(open(_BRANCHES_PATH, encoding="utf-8"))
    BRANCH_COUNT = sum(len(g.get("branches") or []) for g in _govs)
except (OSError, AttributeError, TypeError, ValueError):
    _govs = []
    BRANCH_COUNT = 0

# The governorate groups themselves, for anything that needs the branches and
# not just how many there are — the checkout store picker builds its tree from
# this. Exposed here rather than re-opening the file per caller, so there is
# one reader and one failure mode.
BRANCH_GROUPS = _govs


def size_count(p):
    """
    How many real SKUs this product is sold as (`sizes` in catalog.json, written
    by fetch_sizes.py — Abu Auf use no product variations, so each weight is its
    own SKU with its own id and price).

    >= 2 is the interesting case: the product card cannot honestly add "the
    product" to the cart, because there is no such thing — there is a 50 g SKU
    at 74 and a 400 g SKU at 500. One helper so the card, the bundle and the
    build's own checks all agree on what "has sizes" means.
    """
    return len(p.get("sizes") or [])


# Units Abu Auf actually use in their Arabic product names, longest-first so
# "جرام" is never matched as "جم" + a stray letter. Measured off all 99 names:
# جم 71, جرام 7, قطعة 3, قطع 1. كجم/كيلو/مل/لتر appear in none of our 99 but are
# in the client's wider store, so they are accepted rather than waiting to break.
_PACK_UNITS = "كجم|كيلو|جرام|جم|قطعة|قطع|مل|لتر"

# The number+unit run, anchored at the END of the name — optionally followed by
# a parenthetical, because several offer names carry the pack weight before a
# "(1+1 مجانا)" tail. Anchoring matters: an unanchored search would pull the
# "3" out of "عرض بريتزل (اشتري 3 بسعر أقل)" and call it a pack size.
_PACK_RE = re.compile(
    r"(?P<num>\d+(?:[.,]\d+)?)\s*(?P<unit>" + _PACK_UNITS + r")"
    r"[^\u0600-\u06FF\w]*(?:\([^)]*\))?\s*$"
)


def pack_label(p):
    """
    "80 جم", "12 قطعة", or "" — the pack size, READ OFF the client's own Arabic
    name, never invented.

    Abu Auf carry no weight field at all: the Store API returns `weight: ""` for
    every product (CLAUDE.md), and the size lives in the name instead — which is
    exactly why fetch_sizes.py has to recover sibling SKUs by stripping that
    suffix. So the name is the only place this figure exists, and parsing it is
    reading real data rather than deriving a new one.

    82 of our 99 products yield a label. The 17 that do not are gift boxes,
    baskets, trays and multi-item offers — things that genuinely have no single
    pack size ("عرض معمول (1 سادة + 1 قرفة + ...)"). They get no tag rather than
    a guessed one, the same rule that left the branch phones missing.
    """
    m = _PACK_RE.search((p.get("nameAr") or "").strip())
    if not m:
        return ""
    num = m.group("num").replace(",", ".")
    # 250.0 -> 250, but 1.5 kept.
    if num.endswith(".0"):
        num = num[:-2]
    return num + " " + m.group("unit")


def e(s):
    """Escape for HTML attribute/text context."""
    return html.escape(str(s or ""), quote=True)


def title(p):
    """Display name — Arabic where we have it, English as a fallback."""
    return p.get("nameAr") or p["name"]


def money(v):
    """450.0 -> '450'  |  45.99 -> '45.99'"""
    return f"{v:.2f}".rstrip("0").rstrip(".") if v % 1 else f"{int(v)}"


def in_category(api_name, limit=None):
    out = [p for p in PRODUCTS if p["category"] == api_name]
    return out[:limit] if limit else out


def rail_products(*api_names, limit=12):
    """Products for a carousel, de-duplicated across the given categories."""
    seen, out = set(), []
    for name in api_names:
        for p in in_category(name):
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            out.append(p)
            if len(out) >= limit:
                return out
    return out


def new_arrivals(limit=12):
    """
    Products for the home page's "وصل حديثاً" rail, in two tiers.

    FIRST the client's own New Arrivals category — genuinely new, from their
    taxonomy, no inference. Their live category counts 130; our scrape holds 4,
    which is why this cannot stop there: a four-card rail does not fill a
    desktop row and has nothing to scroll (Ahmed rejected that look).

    THEN the rest of the catalogue by descending id, which is this project's
    existing proxy for "newest" — `_listing.py`'s `وصل حديثاً` sort already
    orders by id for exactly the same reason, because no publish-date field
    exists anywhere in the client's data. Using the same proxy here keeps the
    home rail and the listing sort telling one story rather than two.

    It IS a proxy, and the second tier is therefore inference rather than the
    client saying "this is new". Flagged in DESIGN-NOTES §1 with everything else
    that needs real data; a re-scrape of the full New Arrivals category makes
    the fill unnecessary.
    """
    out = list(in_category("New Arrivals"))
    seen = {p["id"] for p in out}
    for p in sorted(PRODUCTS, key=lambda x: x.get("id", 0), reverse=True):
        if len(out) >= limit:
            break
        # Gift sets are skipped in the FILL tier. They hold eight of the ten
        # highest ids, so unfiltered this rail came out as six Ramadan boxes —
        # sitting immediately below the gifts banner, which is the section that
        # already sells exactly those. A layout call, not a data one: a gift set
        # that really is new still arrives through the first tier above.
        if p.get("category") == "Gifting & Sharing":
            continue
        if p["id"] not in seen:
            seen.add(p["id"])
            out.append(p)
    return out[:limit]


def category(api_name):
    return BY_API_NAME.get(api_name)


def nav_categories():
    return [c for c in CATEGORIES if c.get("nav")]


def home_categories():
    return [c for c in CATEGORIES if c.get("home")]
