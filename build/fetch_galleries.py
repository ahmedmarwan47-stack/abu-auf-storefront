"""
Pull the real per-product gallery photography off Abu Auf's own endpoint.

Why this exists
---------------
`catalog.json` shipped exactly one image per product, because the original
scrape kept `images[0]` and dropped the rest. The client's WooCommerce Store
API actually carries **up to nine images per product**, and for most of the
catalogue the extras are genuine lifestyle photography — the bar on a coloured
sweep, the bar broken open, ingredients scattered around it — not re-crops of
the studio shot. 68 of our 99 products have three or more.

That is real client data sitting behind an endpoint we already use, so per the
"real data over invented data" rule it gets fetched rather than invented.

The de-duplication problem
--------------------------
Every product's image list starts with the same photograph twice: a 600x600
`-thumb` and a 1400x1400 `-gal` (or `-1-1` / `-1_11zon`). Different bytes,
different dimensions, same picture. Taking the list at face value would give
every product a gallery whose first two thumbnails are identical, which looks
like a bug.

So images are compared by content, not by URL: each is downscaled to 32x32
greyscale and kept only if it differs from everything already kept by more than
DISTINCT_THRESHOLD mean levels. Measured separation is unambiguous — re-encodes
of one shot land at 0.2-3.5, genuinely different photographs at 140-190. The
threshold sits an order of magnitude away from both.

What it writes
--------------
- Extra photos into `images/abuauf/products/gallery/`, resized to fit 900px.
  A SEPARATE directory on purpose: `isolate_products.py` reads the product
  folder with a non-recursive listdir, so gallery shots never reach the
  white-background flood fill. They must not — their backgrounds are part of
  the photograph, and cutting them out would destroy the shot.
- An `images` list on every product in `catalog.json`, main image first.
  Products with no extras get a one-entry list, so consumers never branch.

Usage
-----
    python3 build/fetch_galleries.py              # all products
    python3 build/fetch_galleries.py --dry-run    # report, download nothing
    python3 build/fetch_galleries.py --limit 5    # first 5, for a smoke test
"""
import io
import json
import os
import sys
import urllib.request

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python3 -m pip install pillow")

API = "https://backend.abuauf.com/wp-json/wc/store/v1"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = os.path.join(ROOT, "static-export")
CATALOG = os.path.join(EXPORT, "data", "catalog.json")
GALLERY_DIR = os.path.join(EXPORT, "images", "abuauf", "products", "gallery")
REL_DIR = "images/abuauf/products/gallery"

# Mean 0-255 difference below which two images are "the same picture".
# Re-encodes measure 0.2-3.5; distinct photographs measure 140+.
DISTINCT_THRESHOLD = 12
MAX_EDGE = 900          # gallery shots are served at 1400px; that is overkill
JPEG_QUALITY = 82


def fetch(url, binary=False, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
            return raw if binary else json.loads(raw)
        except Exception as exc:                       # noqa: BLE001
            if attempt == tries - 1:
                print(f"  ! {url} -> {exc}", file=sys.stderr)
                return None
    return None


def fingerprint(img):
    """32x32 greyscale, as a flat list of levels."""
    return list(img.convert("L").resize((32, 32), Image.BILINEAR).getdata())


def mean_diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def main(argv):
    dry = "--dry-run" in argv
    limit = None
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])

    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)
    products = catalog["products"] if isinstance(catalog, dict) else catalog
    if limit:
        products = products[:limit]

    if not dry:
        os.makedirs(GALLERY_DIR, exist_ok=True)

    total_extra = 0
    with_gallery = 0

    for n, product in enumerate(products, 1):
        pid = product.get("id")
        main_rel = product.get("image")
        api = fetch(f"{API}/products/{pid}")
        if not api:
            product["images"] = [main_rel]
            continue

        srcs = [im.get("src") for im in (api.get("images") or []) if im.get("src")]
        name = (product.get("nameAr") or product.get("name") or "")[:38]
        print(f"[{n}/{len(products)}] {pid} {name} — {len(srcs)} listed")

        # The local main image is authoritative for slot 0: it has already been
        # background-isolated by isolate_products.py, and re-downloading it
        # would put the white studio sweep back.
        kept_prints = []
        extras = []

        local_main = os.path.join(EXPORT, main_rel) if main_rel else None
        if local_main and os.path.exists(local_main):
            try:
                with Image.open(local_main) as im:
                    # Flatten alpha against white so the cut-out main image is
                    # comparable with the opaque originals from the CDN.
                    flat = Image.new("RGB", im.size, "white")
                    flat.paste(im, mask=im.convert("RGBA").split()[-1])
                    kept_prints.append(fingerprint(flat))
            except Exception as exc:                   # noqa: BLE001
                print(f"    ! could not read local main: {exc}", file=sys.stderr)

        for src in srcs:
            raw = fetch(src, binary=True)
            if not raw:
                continue
            try:
                img = Image.open(io.BytesIO(raw)).convert("RGB")
            except Exception:                          # noqa: BLE001
                continue
            fp = fingerprint(img)
            dup = next((d for d in (mean_diff(fp, k) for k in kept_prints)
                        if d < DISTINCT_THRESHOLD), None)
            if dup is not None:
                print(f"    = {os.path.basename(src)} (same picture, diff {dup:.1f})")
                continue
            kept_prints.append(fp)

            base = os.path.basename(src.split("?")[0])
            stem = os.path.splitext(base)[0]
            out_rel = f"{REL_DIR}/{stem}.webp"
            out_abs = os.path.join(EXPORT, out_rel)
            if not dry:
                img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
                img.save(out_abs, "WEBP", quality=JPEG_QUALITY, method=6)
            extras.append(out_rel)
            print(f"    + {base}")

        product["images"] = ([main_rel] if main_rel else []) + extras
        total_extra += len(extras)
        if extras:
            with_gallery += 1

    print(f"\n{with_gallery} product(s) gained a gallery, {total_extra} extra photo(s)")

    if dry:
        print("dry run — catalog.json not written")
        return 0

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, ensure_ascii=False, indent=2)
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
