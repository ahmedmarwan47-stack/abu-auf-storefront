#!/usr/bin/env python3
"""
Add Arabic product names to data/catalog.json.

The WooCommerce Store API only exposes English names, but the Arabic
storefront server-renders them into its Next.js flight payload at
  https://www.abuauf.com/ar/category/<slug>
keyed by the same product slug the Store API returns. So we scrape those
pages, build a slug -> Arabic-name map, and merge it in.
"""
import json
import os
import re
import time
import urllib.request

ROOT = "/Users/ahmed/order-base-ecommerce/static-export"
CATALOG = os.path.join(ROOT, "data", "catalog.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Category routes the storefront actually exposes, plus every slug in our
# catalog — extras just 404 harmlessly and are skipped.
SITE_CATEGORIES = [
    "coffee-beverage", "nuts-crackers", "healthy-snacks", "dates-dried-fruits",
    "kitchen-baking", "gifting-seasonal", "offers-promotions",
    "candy-wafers-biscuits-maamoul", "ramadan-products",
]


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Accept-Language": "ar"})
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ! {url}: {e}")
        return ""


def flight_blob(html):
    """Concatenate and unescape the Next.js RSC flight rows."""
    rows = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S)
    blob = "".join(rows)
    # The rows are JS string literals: \uXXXX and \" escapes, but the bytes
    # underneath are UTF-8. unicode_escape decodes per-byte as latin-1, so
    # round-trip back through latin-1 to recover the real characters.
    blob = blob.encode("utf-8", "ignore").decode("unicode_escape", "ignore")
    try:
        blob = blob.encode("latin-1", "ignore").decode("utf-8", "ignore")
    except Exception:
        pass
    return blob


def extract(blob):
    """slug -> Arabic name, from the product objects in the payload."""
    out = {}
    for slug, _gap, name in re.findall(
        r'"slug":"([a-z0-9\-]{3,90})"(.{0,400}?)"name":"([^"]{2,120})"', blob, re.S
    ):
        if not re.search(r"[؀-ۿ]", name):
            continue  # not Arabic — skip
        name = (name.replace("&#8211;", "–").replace("&amp;", "&")
                    .replace("&#8217;", "'").strip())
        out.setdefault(slug, name)
    return out


def main():
    cat = json.load(open(CATALOG, encoding="utf-8"))
    slugs = {c["slug"] for c in cat["categories"] if c.get("slug")}
    routes = list(dict.fromkeys(SITE_CATEGORIES + sorted(slugs)))

    names = {}
    for slug in routes:
        for page in (1, 2, 3):
            url = f"https://www.abuauf.com/ar/category/{slug}"
            if page > 1:
                url += f"?page={page}"
            html = fetch(url)
            if not html:
                break
            found = extract(flight_blob(html))
            new = {k: v for k, v in found.items() if k not in names}
            names.update(new)
            print(f"  {slug} p{page}: +{len(new)} (total {len(names)})")
            if len(found) == 0:
                break
            time.sleep(0.4)

    # merge
    hit = miss = 0
    for p in cat["products"]:
        ar = names.get(p.get("slug"))
        if ar:
            p["nameAr"] = ar
            hit += 1
        else:
            miss += 1

    json.dump(cat, open(CATALOG, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(f"\nArabic names collected: {len(names)}")
    print(f"catalog products matched: {hit}/{hit + miss}")
    if miss:
        print("unmatched slugs (first 15):")
        for p in cat["products"]:
            if "nameAr" not in p and miss:
                print("   ", p.get("slug"))
                miss -= 1
                if miss <= 0 or miss < 1:
                    pass
        # cap output
    print("\nsample:")
    for p in cat["products"][:8]:
        print(f"   {p.get('nameAr', '(none)')}   <-  {p['name'][:45]}")


if __name__ == "__main__":
    main()
