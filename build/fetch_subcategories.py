"""
Record each product's real sub-category membership from Abu Auf's own store.

Why this exists
---------------
`catalog.json` used to carry only a flat top-level `categorySlug` per product,
so a category listing could not filter by sub-category — the coffee page faked
it by GUESSING each SKU's sub-category from keywords in its Arabic name
(`shop_category._subcat`), explicitly flagged as derived-not-real data.

The real membership was there all along: the WooCommerce Store API returns a
`categories[]` array on every product — parent AND child categories, each with
`{id, name, slug}` — and `/products/categories` exposes the taxonomy with a
`parent` id per category. Reading both gives every product its true
sub-categories against the real store, so the coffee chips (and any future
per-category sub-filter) stop being a keyword guess.

What it writes
--------------
`subCats` on every product in `catalog.json`: the ordered list of the real
CHILD-category slugs (parent != 0) that product belongs to. A product with no
child category is given `[]`. Top-level slugs are NOT included — those already
live in `categorySlug`.

Because our catalogue is a 99-product SUBSET of the ~664-product store, many
real sub-categories hold only one or two of our products, and some hold none;
callers that render sub-category chips must drop the empty ones (the coffee
page already does).

Usage
-----
    python3 build/fetch_subcategories.py
    python3 build/fetch_subcategories.py --dry-run
"""
import json
import os
import sys
import urllib.request

API = "https://backend.abuauf.com/wp-json/wc/store/v1"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "static-export", "data", "catalog.json")

MAX_PAGES = 12


def get(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except Exception as exc:                       # noqa: BLE001
            if attempt == tries - 1:
                print(f"  ! {url} -> {exc}", file=sys.stderr)
                return None
    return None


def main(argv):
    dry = "--dry-run" in argv

    # 1. Taxonomy — which category ids are CHILDREN (parent != 0).
    taxonomy = get(f"{API}/products/categories?per_page=100")
    if not taxonomy:
        sys.exit("no taxonomy returned — refusing to blank existing subCats")
    child_ids = {c["id"] for c in taxonomy if c.get("parent")}
    print(f"taxonomy: {len(taxonomy)} categories, {len(child_ids)} children")

    # 2. Walk the whole store, recording each product's child-category slugs in
    #    the order the API lists them (stable, deterministic).
    subs_by_id = {}
    for page in range(1, MAX_PAGES + 1):
        batch = get(f"{API}/products?per_page=100&page={page}")
        if not batch:
            break
        for p in batch:
            subs_by_id[str(p["id"])] = [
                c["slug"] for c in p.get("categories", [])
                if c.get("id") in child_ids
            ]
        print(f"  page {page}: {len(batch)} product(s)")
        if len(batch) < 100:
            break
    if not subs_by_id:
        sys.exit("no products returned — refusing to blank existing subCats")
    print(f"walked {len(subs_by_id)} product(s) across the whole store")

    # 3. Stamp our catalogue.
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)
    products = catalog["products"] if isinstance(catalog, dict) else catalog

    hits = 0
    for product in products:
        subs = subs_by_id.get(str(product.get("id")))
        if subs is None:                       # not found in the walk at all
            product.setdefault("subCats", [])
            continue
        product["subCats"] = subs
        if subs:
            hits += 1

    print(f"{hits} of our {len(products)} product(s) carry >=1 sub-category")
    from collections import Counter
    counts = Counter(s for p in products for s in p.get("subCats", []))
    for slug, n in counts.most_common():
        print(f"  {slug:<34} {n}")

    if dry:
        print("dry run — catalog.json not written")
        return 0

    # indent=1 matches the file scrape_assets.py writes; keep it so the diff
    # is the added subCats lines alone, not a whole-file reformat.
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, ensure_ascii=False, indent=1)
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
