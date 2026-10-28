#!/usr/bin/env python3
"""
Write the client's own recipes to data/recipes.json and their photos to
images/abuauf/recipes/.

Two sources, because neither holds everything:

  1. The list endpoint the live /recipes page calls —
       /wp-json/apis/v2/posts?post_type=recipe&...
     gives every recipe's slug, Arabic title, Arabic intro (`content_ar`),
     hero photo and times, but no ingredients or method.
  2. The detail page, https://www.abuauf.com/recipes/<slug>, server-renders
     the full post into its Next.js flight payload, including `recipe_data`:
     `ingredients_ar` (<ul>) and `steps_ar` (<ol>), plus `persons`.

Like every other fetched field these are the client's words, not ours. The
times are stored exactly as the client entered them — on at least one recipe
they do not add up (DESIGN-NOTES §1) — and a recipe with no ingredients or
steps is stored with empty lists rather than filled in.

    python3 build/fetch_recipes.py
"""
import html as htmllib
import json
import os
import re
import urllib.request

ROOT = "/Users/ahmed/order-base-ecommerce/static-export"
OUT = os.path.join(ROOT, "data", "recipes.json")
IMG_DIR = os.path.join(ROOT, "images", "abuauf", "recipes")
LIST = ("https://www.abuauf.com/wp-json/apis/v2/posts?post_type=recipe&page=1"
        "&posts_per_page=50&country=EGP&lang=ar"
        "&extra_fields=prep_time%2Ccooking_time%2Ctotal_time%2Cpersons")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) abuauf-static-export"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def flight(page):
    """Concatenate the page's self.__next_f.push([1,"..."]) string chunks."""
    chunks = re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', page, re.S)
    return "".join(json.loads(c) for c in chunks)


def recipe_object(blob):
    """The post object that owns `recipe_data` — decoded whole, not regexed."""
    i = blob.find('"recipe_data"')
    if i < 0:
        return None
    start = blob.rfind('{"ID"', 0, i)
    obj, _ = json.JSONDecoder().raw_decode(blob[start:])
    return obj


def items(fragment):
    """<li> texts of a client HTML list, tags stripped, whitespace collapsed."""
    out = []
    for li in re.findall(r"<li>(.*?)</li>", fragment or "", re.S):
        text = htmllib.unescape(re.sub(r"<[^>]+>", "", li))
        text = re.sub(r"\s+", " ", text).strip().translate(PERSIAN)
        if text:
            out.append(text)
    return out


def text(s):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


# A few client titles are typed with the PERSIAN yeh and keheh (U+06CC, U+06A9)
# — "كوكیز عید المیلاد". They render close enough to pass by eye but are
# different code points: search's fold() does not map them, so the title would
# never match a query typed on an Arabic keyboard. Normalising the code point
# changes no word.
PERSIAN = str.maketrans({"\u06cc": "\u064a", "\u06a9": "\u0643"})


def ar(s):
    return text(s).translate(PERSIAN)


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    posts = json.loads(get(LIST))["posts"]
    recipes = []
    for i, post in enumerate(posts, 1):
        slug = post["slug"]
        detail = recipe_object(flight(get(f"https://www.abuauf.com/recipes/{slug}").decode("utf-8")))
        data = (detail or {}).get("recipe_data") or {}
        extra = post.get("extra_data") or {}

        src = post["image"]["src"]
        name = f"{slug}{os.path.splitext(src)[1]}"
        path = os.path.join(IMG_DIR, name)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(get(src))

        recipes.append({
            "id": post["ID"],
            "slug": slug,
            "name": text(post["title"]),
            "nameAr": ar(post.get("ar_title")),
            "introAr": ar(post.get("content_ar") or (detail or {}).get("ar_content")),
            "image": f"images/abuauf/recipes/{name}",
            "prepTime": data.get("prep_time") or extra.get("prep_time") or "",
            "cookingTime": data.get("cooking_time") or extra.get("cooking_time") or "",
            "totalTime": data.get("total_time") or extra.get("total_time") or "",
            "persons": data.get("persons") or extra.get("persons") or "",
            "ingredientsAr": items(data.get("ingredients_ar")),
            "stepsAr": items(data.get("steps_ar")),
            "created": post.get("created_time", ""),
        })
        r = recipes[-1]
        print(f"  {i:>2} {slug}: {len(r['ingredientsAr'])} ingredients, {len(r['stepsAr'])} steps")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(recipes)} recipes to {OUT}")


if __name__ == "__main__":
    main()
