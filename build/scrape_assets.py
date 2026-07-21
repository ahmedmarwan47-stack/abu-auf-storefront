#!/usr/bin/env python3
"""
Pull Abu Auf brand + product assets into the static export.

Sources (both public, no auth):
  - backend.abuauf.com/wp-content/uploads/...   image host
  - backend.abuauf.com/wp-json/wc/store/v1/...  WooCommerce Store API

Writes images under static-export/images/abuauf/ and a catalog JSON the
pages can be built from. Re-runnable: existing files are skipped.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = "/Users/ahmed/order-base-ecommerce/static-export"
IMG = os.path.join(ROOT, "images", "abuauf")
DATA = os.path.join(ROOT, "data")
API = "https://backend.abuauf.com/wp-json/wc/store/v1"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Storefront categories.
#   api    — exact name from the Store API
#   ar     — Arabic label, taken from the live abuauf.com storefront so it
#            matches the Figma designs verbatim
#   home   — appears in the 6-card category grid on the home page
#   nav    — appears in the green category bar in the header
CATEGORIES = [
    {"api": "Offers & Promotions",     "ar": "العروض والخصومات",        "nav": True},
    {"api": "Nuts | Seeds & Crackers", "ar": "مكسرات وحبوب ومقرمشات",  "nav": True,  "home": True},
    {"api": "Coffee & Beverages",      "ar": "قهوة ومشروبات",           "nav": True,  "home": True},
    {"api": "Dates & Dried Fruits",    "ar": "تمور وفواكه مجففة",       "nav": True,  "home": True},
    {"api": "Snacks",                  "ar": "سناكس صحية",              "nav": True,  "home": True},
    {"api": "Kitchen & Baking",        "ar": "اساسيات المطبخ",          "nav": True,  "home": True},
    {"api": "Spices",                  "ar": "البهارات والزيوت",        "nav": True},
    {"api": "Gifting & Sharing",       "ar": "الهدايا والمشاركة",       "nav": True,  "home": True},
    # Secondary rails used on the home page and listing pages.
    {"api": "Best Selling",            "ar": "الأكثر مبيعاً"},
    {"api": "New Arrivals",            "ar": "وصل حديثاً"},
    {"api": "Confectionary",           "ar": "الحلويات"},
    {"api": "Baked Snacks & Biscuits", "ar": "مخبوزات وبسكويت"},
]


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except Exception as e:
            if i == tries - 1:
                print(f"  ! {url} -> {e}", file=sys.stderr)
                return None
            time.sleep(1.5 * (i + 1))


def get_json(url):
    b = get(url)
    if not b:
        return None
    try:
        return json.loads(b)
    except Exception:
        return None


def save(url, subdir, name=None):
    """Download url into IMG/subdir. Returns the export-relative path."""
    if not url:
        return None
    clean = url.split("?")[0]
    name = name or os.path.basename(urllib.parse.urlparse(clean).path)
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name)
    d = os.path.join(IMG, subdir)
    os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, name)
    rel = f"images/abuauf/{subdir}/{name}"
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return rel
    b = get(clean)
    if not b or len(b) < 200:
        return None
    with open(dest, "wb") as f:
        f.write(b)
    return rel


def strip(s):
    """WooCommerce returns HTML entities and tags in names/descriptions."""
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in [("&#8211;", "–"), ("&#8217;", "'"), ("&amp;", "&"),
                 ("&quot;", '"'), ("&#039;", "'"), ("&nbsp;", " "),
                 ("&#215;", "×"), ("&hellip;", "…")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def money(prices):
    """Store API returns minor units; currency_minor_unit says how many."""
    try:
        minor = int(prices.get("currency_minor_unit", 2))
        val = int(prices.get("price", 0)) / (10 ** minor)
        reg = int(prices.get("regular_price", 0)) / (10 ** minor)
        sale = int(prices.get("sale_price", 0)) / (10 ** minor)
        return {"price": val, "regular": reg,
                "sale": sale if sale and sale < reg else None,
                "currency": prices.get("currency_code", "EGP")}
    except Exception:
        return {"price": 0, "regular": 0, "sale": None, "currency": "EGP"}


def main():
    os.makedirs(DATA, exist_ok=True)
    out = {"categories": [], "products": []}

    print("== categories ==")
    cats = get_json(f"{API}/products/categories?per_page=100") or []
    by_name = {strip(c["name"]): c for c in cats}
    missing = []
    for spec in CATEGORIES:
        c = by_name.get(spec["api"])
        if not c:
            missing.append(spec["api"])
            continue
        img = (c.get("image") or {}).get("src")
        rel = save(img, "categories") if img else None
        out["categories"].append({
            "id": c["id"], "name": strip(c["name"]), "ar": spec["ar"],
            "slug": c.get("slug"), "count": c.get("count"), "image": rel,
            "nav": bool(spec.get("nav")), "home": bool(spec.get("home")),
        })
        flags = ("nav" if spec.get("nav") else "   ") + ("/home" if spec.get("home") else "")
        print(f"  {c['count']:>4}  {spec['ar']:<24} {strip(c['name']):<28} "
              f"{'img' if rel else '---'}  {flags}")
    if missing:
        print(f"  !! not found in API: {missing}")

    print("== products ==")
    seen = set()
    for c in out["categories"]:
        items = get_json(
            f"{API}/products?per_page=12&category={c['id']}&orderby=popularity") or []
        kept = 0
        for p in items:
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            imgs = p.get("images") or []
            rel = save(imgs[0]["src"], "products") if imgs else None
            if not rel:
                continue
            out["products"].append({
                "id": p["id"], "name": strip(p.get("name")),
                "slug": p.get("slug"), "category": c["name"],
                "categoryAr": c["ar"], "categorySlug": c.get("slug"),
                "image": rel,
                "shortDesc": strip(p.get("short_description"))[:180],
                "onSale": bool(p.get("on_sale")),
                "inStock": (p.get("is_in_stock", True)),
                **money(p.get("prices") or {}),
            })
            kept += 1
        print(f"  {c['name']}: {kept}")

    with open(os.path.join(DATA, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"\ncategories={len(out['categories'])} products={len(out['products'])}")


if __name__ == "__main__":
    main()
