"""
Record each product's real best-seller rank from Abu Auf's own store.

Why this exists
---------------
The product page wanted a "best seller" badge and a line of social proof next
to the rating. Both are the kind of thing that is trivial to invent and wrong
to invent — the catalogue already carries an invented 4.8/126 rating precisely
because the client's review endpoint returns nothing (`average_rating: "0"`,
`review_count: 0` on every product), and that is flagged as placeholder.

But a genuine popularity signal *is* available: the Store API supports
`orderby=popularity`, which is WooCommerce's own total-sales ordering. Walking
the whole catalogue in that order gives every product a real rank against the
real store. So the badge is earned rather than asserted, and a product stops
being a "best seller" the moment the client's sales say it is not.

What it does NOT give us
------------------------
Absolute unit counts. There is no public field for "500 sold this week" — that
needs a sales feed the client would have to expose. The page therefore shows a
rank-derived line ("among the top N best sellers"), which is true and carries
the same encouragement, instead of a fabricated number. See DESIGN-NOTES.

What it writes
--------------
`popularityRank` (1 = best selling) on every product in `catalog.json` that
appears in the ranked walk. Products the API does not rank are left without the
key, and callers must treat a missing rank as "not a best seller".

Usage
-----
    python3 build/fetch_popularity.py
    python3 build/fetch_popularity.py --dry-run
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

    ranked = []
    for page in range(1, MAX_PAGES + 1):
        batch = get(f"{API}/products?per_page=100&page={page}&orderby=popularity")
        if not batch:
            break
        ranked.extend(batch)
        print(f"  page {page}: {len(batch)} product(s)")
        if len(batch) < 100:
            break
    if not ranked:
        sys.exit("no products returned — refusing to blank existing ranks")

    rank_by_id = {str(p["id"]): i + 1 for i, p in enumerate(ranked)}
    print(f"\nranked {len(rank_by_id)} product(s) across the whole store")

    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)
    products = catalog["products"] if isinstance(catalog, dict) else catalog

    hits = 0
    for product in products:
        rank = rank_by_id.get(str(product.get("id")))
        if rank:
            product["popularityRank"] = rank
            hits += 1
        else:
            product.pop("popularityRank", None)

    print(f"{hits} of our {len(products)} product(s) carry a rank")
    top = sorted((p for p in products if p.get("popularityRank")),
                 key=lambda p: p["popularityRank"])[:10]
    for p in top:
        print(f"  #{p['popularityRank']:<4} {(p.get('nameAr') or p.get('name') or '')[:48]}")

    if dry:
        print("dry run — catalog.json not written")
        return 0

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, ensure_ascii=False, indent=2)
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
