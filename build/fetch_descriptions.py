#!/usr/bin/env python3
"""
Add the client's own Arabic descriptions to data/catalog.json.

The WooCommerce Store API truncates `short_description` mid-sentence and only
in English, but the Arabic storefront server-renders the full copy into the
product detail page's Next.js flight payload at
  https://www.abuauf.com/ar/products/<slug>
as two fields on the main product object:

  short_description  — a plain-text Arabic paragraph
  description        — Arabic benefit lists as HTML (<strong>/<ul>/<li>)

We store them as `descAr` and `descHtmlAr`. Like every other fetched field,
these are the client's words, not ours — a product without them renders
without a description rather than with an invented one.
"""
import json
import os
import re
import time

from fetch_arabic_names import fetch, flight_blob

ROOT = "/Users/ahmed/order-base-ecommerce/static-export"
CATALOG = os.path.join(ROOT, "data", "catalog.json")

ARABIC = re.compile(r"[؀-ۿ]")
STR = r'((?:[^"\\]|\\.)*)'
# On the detail page the main product object carries description and
# short_description back to back, immediately followed by "sku" — the related
# rail products carry neither, so this pair only matches the page's own
# product. Verified on roasted-cashew-275-gm-offer.
PAIR = re.compile(r'"description":"' + STR + r'","short_description":"' + STR + r'","sku"')


def unescape(s):
    """The blob is once-unescaped already; strings still carry JSON escapes."""
    s = (s.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\r", "\n")
          .replace("\\t", " ").replace('\\"', '"').replace("\\/", "/"))
    s = s.replace("&#8211;", "–").replace("&amp;", "&").replace("&#8217;", "'")
    s = s.replace("&nbsp;", " ")
    return re.sub(r"[ \t]+", " ", s).strip()


def main():
    cat = json.load(open(CATALOG, encoding="utf-8"))
    hit = skipped = 0
    for i, p in enumerate(cat["products"], 1):
        slug = p.get("slug")
        if not slug:
            skipped += 1
            continue
        html = fetch(f"https://www.abuauf.com/ar/products/{slug}")
        if not html:
            skipped += 1
            continue
        m = PAIR.search(flight_blob(html))
        if not m:
            print(f"  {i:>2} {slug}: no description pair")
            skipped += 1
            continue
        desc, short = unescape(m.group(1)), unescape(m.group(2))
        got = []
        # Arabic-only: an English fallback string here would silently violate
        # the Arabic-first rule on 31 pages at once.
        if short and ARABIC.search(short):
            p["descAr"] = short
            got.append("short")
        if desc and ARABIC.search(desc):
            p["descHtmlAr"] = desc
            got.append("long")
        hit += bool(got)
        print(f"  {i:>2} {slug}: {'+'.join(got) or 'nothing arabic'}")
        time.sleep(0.35)

    json.dump(cat, open(CATALOG, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\nproducts with fetched Arabic copy: {hit}/{len(cat['products'])}"
          f" ({skipped} skipped)")


if __name__ == "__main__":
    main()
