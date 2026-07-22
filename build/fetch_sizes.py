"""
Record the real size options a product is sold in, with their real prices.

Why this exists
---------------
The product page carried three weight chips — 500 / 250 / 100 جم — that were
invented, did nothing when clicked, and contradicted the product they sat under
(the page's own product is a 300 جم pack). Ahmed asked for the weight to affect
the price, which is only worth doing against real numbers.

The Store API has no variations to offer: every product comes back
`type: "simple"`, `variations: []`, `attributes: []`, `weight: ""`. Abu Auf do
not model size as a product variation.

What they DO is sell each size as its own SKU, with the size in the product
name — "... - 50 gm", "... - 100 gm", "... - 200 gm". So the sizes are real and
so are their prices; they just have to be recovered by grouping the catalogue
on the product name with the size suffix stripped. Across the client's whole
653-product store that finds 41 base products sold in more than one size,
including the coffees.

What it writes
--------------
`sizes` on each catalogue product: a list of
`{"label": "100 جم", "grams": 100, "price": 110.0, "id": 6347}`, sorted
smallest first, and only when a product genuinely has more than one size. A
product sold in one size gets no key at all, and `size_chips()` renders nothing
— rather than a single chip that implies a choice nobody has.

`id` is the sibling's real product id, so selecting a size can point the cart at
the SKU the shopper actually chose instead of silently keeping the first one.

Caveats
-------
- Grouping is by name, which is the only signal available. Two products whose
  names differ only by size are assumed to be the same product in two sizes.
  Spot-checked against the coffees and the pretzels and it holds.
- Some base names carry two SKUs at the SAME size and different prices (an old
  and a relisted one). The cheaper is kept, on the grounds that a storefront
  showing the higher of two live prices for the identical thing is the worse
  failure.

Usage
-----
    python3 build/fetch_sizes.py
    python3 build/fetch_sizes.py --dry-run
"""
import collections
import html
import json
import os
import re
import sys
import urllib.request

API = "https://backend.abuauf.com/wp-json/wc/store/v1"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "static-export", "data", "catalog.json")

MAX_PAGES = 12
# "Coffee - 100 gm", "Spices -  75gm", "Something – 1 kg"
SIZE_RE = re.compile(r"^(?P<base>.*?)[-–]\s*(?P<num>[\d.]+)\s*(?P<unit>gm|g|kg)\s*$", re.I)


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


def parse_size(name):
    """('light roasted plain coffee', 100) or (None, None)."""
    clean = html.unescape(name or "").replace("&#8211;", "-").replace("–", "-")
    m = SIZE_RE.match(clean.strip())
    if not m:
        return None, None
    grams = float(m.group("num"))
    if m.group("unit").lower() == "kg":
        grams *= 1000
    return re.sub(r"\s+", " ", m.group("base")).strip().lower(), int(grams)


def label_for(grams):
    """Arabic size label. Whole kilos read better as كجم."""
    if grams >= 1000 and grams % 1000 == 0:
        return f"{grams // 1000} كجم"
    return f"{grams} جم"


def main(argv):
    dry = "--dry-run" in argv

    store = []
    for page in range(1, MAX_PAGES + 1):
        batch = get(f"{API}/products?per_page=100&page={page}")
        if not batch:
            break
        store.extend(batch)
        if len(batch) < 100:
            break
    if not store:
        sys.exit("no products returned — refusing to blank existing sizes")
    print(f"walked {len(store)} product(s) in the client's store")

    # base name -> grams -> (price, id), keeping the cheaper on a collision
    groups = collections.defaultdict(dict)
    base_of = {}
    for p in store:
        base, grams = parse_size(p.get("name"))
        if not base:
            continue
        base_of[str(p["id"])] = base
        try:
            price = int(p["prices"]["price"]) / (10 ** int(p["prices"]["currency_minor_unit"]))
        except (KeyError, TypeError, ValueError):
            continue
        prev = groups[base].get(grams)
        if prev is None or price < prev[0]:
            groups[base][grams] = (price, p["id"])

    multi = {b: s for b, s in groups.items() if len(s) > 1}
    print(f"{len(multi)} base product(s) are sold in more than one size")

    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)
    products = catalog["products"] if isinstance(catalog, dict) else catalog

    hits = 0
    for product in products:
        base = base_of.get(str(product.get("id")))
        sizes = multi.get(base) if base else None
        if not sizes:
            product.pop("sizes", None)
            continue
        product["sizes"] = [
            {"label": label_for(g), "grams": g, "price": price, "id": pid}
            for g, (price, pid) in sorted(sizes.items())
        ]
        hits += 1
        name = (product.get("nameAr") or product.get("name") or "")[:34]
        pretty = ", ".join(f"{s['label']}={s['price']:g}" for s in product["sizes"])
        print(f"  {name:<36} {pretty}")

    print(f"\n{hits} of our {len(products)} product(s) gained real size options")

    if dry:
        print("dry run — catalog.json not written")
        return 0

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, ensure_ascii=False, indent=2)
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
