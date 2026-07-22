"""
Shared data access for the Abu Auf static build.

Everything page builders know about products, categories and prices comes
through here, so a change to (say) price formatting or which products feed a
rail happens in one place and reaches every page on the next build.
"""
import html
import json
import os

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
    BRANCH_COUNT = 0


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


def category(api_name):
    return BY_API_NAME.get(api_name)


def nav_categories():
    return [c for c in CATEGORIES if c.get("nav")]


def home_categories():
    return [c for c in CATEGORIES if c.get("home")]
