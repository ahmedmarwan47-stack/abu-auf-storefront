#!/usr/bin/env python3
"""
Fill in Arabic names the category sweep missed, by fetching each product's own
page. Category listings only server-render their first page, so ~half the
catalog needs a per-product lookup.

The product name is the first Arabic "name" field in the page's Next.js flight
payload; the site's own chrome (nav labels, account menu) also appears as
"name" fields, so those are filtered out.
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

# Site chrome that also surfaces as "name" fields in the flight payload.
CHROME = {
    "حسابي", "خدمات التصدير", "الموزعين المحليين", "من نحن", "قصتنا",
    "فروعنا", "وصفاتنا", "التصدير", "البلوج", "أتصل بنا", "المنتجات",
    "تسجيل الدخول", "الرئيسية", "السلة", "المفضلة", "طلباتي", "محفظتي",
    "العروض و الخصومات", "قهوة ومشروبات", "مكسرات وحبوب ومقرمشات", "سناكس",
    "تمور وفواكه مجففة", "اساسيات المطبخ", "قسم الهدايا والمشاركة",
}


def fetch(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": UA, "Accept-Language": "ar"})
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def product_name(html):
    rows = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S)
    blob = "".join(rows).encode("utf-8", "ignore").decode("unicode_escape", "ignore")
    try:
        blob = blob.encode("latin-1", "ignore").decode("utf-8", "ignore")
    except Exception:
        pass
    for n in re.findall(r'"name":"([^"]{2,140})"', blob):
        if not re.search(r"[؀-ۿ]", n):
            continue
        n = (n.replace("&#8211;", "–").replace("&amp;", "&")
              .replace("&#8217;", "'").strip())
        if n in CHROME:
            continue
        return n
    return None


def main():
    cat = json.load(open(CATALOG, encoding="utf-8"))
    todo = [p for p in cat["products"] if not p.get("nameAr") and p.get("slug")]
    print(f"fetching {len(todo)} product pages…")

    got = 0
    for i, p in enumerate(todo, 1):
        html = fetch(f"https://www.abuauf.com/ar/products/{p['slug']}")
        name = product_name(html) if html else None
        if name:
            p["nameAr"] = name
            got += 1
            print(f"  {i:>3}/{len(todo)}  {name}")
        else:
            print(f"  {i:>3}/{len(todo)}  -- no name for {p['slug']}")
        time.sleep(0.3)

    json.dump(cat, open(CATALOG, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    total = len(cat["products"])
    have = sum(1 for p in cat["products"] if p.get("nameAr"))
    print(f"\nfilled {got} more; Arabic coverage now {have}/{total}")


if __name__ == "__main__":
    main()
