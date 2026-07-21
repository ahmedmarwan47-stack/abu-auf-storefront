"""
Cut the white studio background out of the product photos.

Why this exists
---------------
101 of the 110 files in `static-export/images/abuauf/products` arrived from the
client's CDN as opaque JPEG-style photos on a pure-white studio sweep. The card
plate is `bg-interaction-base` (#EDEFEB, the same value the live site uses), so
every one of those rendered as a white rectangle floating inside the beige
plate — a container inside the container. The handful that already carried an
alpha channel looked correct, which is what made the inconsistency obvious.

The fix is to isolate the product, not to repaint the plate: recolouring the
plate to white would hide the seam but also throw away the Figma/live surface
colour, and the 7 already-transparent files would then be the odd ones out.

How it works
------------
A flood fill of near-white pixels seeded from the image border, 4-connected.
Border-connected only — that is the whole point. A plain "every white pixel
becomes transparent" pass punches holes through white packaging, labels and
highlights; those regions are white but they are *enclosed* by product, so the
fill never reaches them.

Edge pixels get a soft alpha ramp so the cut-out does not leave a hard white
halo where the photo was anti-aliased against its background.

Safety
------
- Idempotent: a file that already has a meaningful alpha channel is skipped, so
  re-running never re-processes and never compounds lossy re-encoding.
- The images are tracked in git, so `git checkout` restores the originals.
- Run it explicitly. `build.py` does NOT call this — it is an asset
  preparation step, not part of the page build.

Usage
-----
    python3 build/isolate_products.py                    # the product folder
    python3 build/isolate_products.py --dry-run          # report only
    python3 build/isolate_products.py path/to/a.webp ... # specific files

Only run this on artwork that sits on a COLOURED plate. Full-bleed hero
banners and the photo blocks on the export page are displayed on white, where
a white background is correct and cutting it out would do nothing but throw
away image quality. `site/Abu-Auf-flags.webp` needed it because it renders
inside an `info_card`, whose surface is #EDEFEB.
"""
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

PRODUCT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static-export", "images", "abuauf", "products",
)

# A pixel counts as background only if every channel is at least this bright.
# 238 keeps genuine off-white product surfaces (which photograph around
# 225-235) while still catching JPEG noise in the sweep itself.
WHITE_MIN = 238
# Pixels between SOFT_MIN and WHITE_MIN that touch the background get a partial
# alpha, which is what kills the halo.
SOFT_MIN = 205
WEBP_QUALITY = 90


def flood_background(rgb):
    """Mask of near-white pixels reachable from the border. 4-connected."""
    h, w = rgb.shape[:2]
    near_white = np.all(rgb >= WHITE_MIN, axis=2)

    bg = np.zeros((h, w), dtype=bool)
    q = deque()

    def seed(y, x):
        if near_white[y, x] and not bg[y, x]:
            bg[y, x] = True
            q.append((y, x))

    for x in range(w):
        seed(0, x)
        seed(h - 1, x)
    for y in range(h):
        seed(y, 0)
        seed(y, w - 1)

    while q:
        y, x = q.popleft()
        if y > 0:
            seed(y - 1, x)
        if y < h - 1:
            seed(y + 1, x)
        if x > 0:
            seed(y, x - 1)
        if x < w - 1:
            seed(y, x + 1)
    return bg


def soft_alpha(rgb, bg):
    """0 inside the background, 255 on the product, ramped in between."""
    alpha = np.where(bg, 0, 255).astype(np.uint8)

    # Dilate the background by one pixel to find the boundary band.
    nb = np.zeros_like(bg)
    nb[1:, :] |= bg[:-1, :]
    nb[:-1, :] |= bg[1:, :]
    nb[:, 1:] |= bg[:, :-1]
    nb[:, :-1] |= bg[:, 1:]
    band = nb & ~bg

    lum = rgb.max(axis=2).astype(np.float32)
    # Bright band pixels are mostly leftover sweep; fade them out.
    ramp = np.clip((WHITE_MIN - lum) / float(WHITE_MIN - SOFT_MIN), 0.0, 1.0)
    ramped = (ramp * 255.0).astype(np.uint8)
    alpha[band] = np.minimum(alpha[band], ramped[band])
    return alpha


def already_isolated(im):
    """True if the file carries an alpha channel that actually does something."""
    if im.mode not in ("RGBA", "LA", "P"):
        return False
    a = im.convert("RGBA").split()[-1]
    lo, hi = a.getextrema()
    return lo < 250  # some genuine transparency present


def process(path, dry_run=False):
    im = Image.open(path)
    fmt = (im.format or "").upper()

    if already_isolated(im):
        return "skipped-has-alpha", None

    rgb = np.array(im.convert("RGB"))
    bg = flood_background(rgb)
    share = bg.mean()

    # Nothing meaningful to cut, or the fill escaped through the product and
    # ate the whole frame — either way, leave the file alone.
    if share < 0.005:
        return "skipped-no-white-border", None
    # 0.985, not 0.95: a single raisin on a 600x600 sweep legitimately leaves
    # ~95% background. Only a fill that has plainly escaped through the product
    # and consumed the frame should be rejected.
    if share > 0.985:
        return "skipped-fill-ran-away", None

    if dry_run:
        return "would-isolate", share

    alpha = soft_alpha(rgb, bg)
    out = Image.fromarray(np.dstack([rgb, alpha]))  # RGBA inferred from shape

    if fmt == "PNG" or path.lower().endswith(".png"):
        out.save(path, "PNG", optimize=True)
    else:
        out.save(path, "WEBP", quality=WEBP_QUALITY, method=6)
    return "isolated", share


def main():
    dry = "--dry-run" in sys.argv
    explicit = [a for a in sys.argv[1:] if not a.startswith("--")]
    if explicit:
        paths = [os.path.abspath(a) for a in explicit]
        where = "%d file(s) given on the command line" % len(paths)
    else:
        paths = [
            os.path.join(PRODUCT_DIR, f) for f in sorted(os.listdir(PRODUCT_DIR))
            if not f.startswith(".") and f.lower().endswith((".webp", ".png", ".jpg", ".jpeg"))
        ]
        where = "%d file(s) in %s" % (len(paths), PRODUCT_DIR)

    tally = {}
    for path in paths:
        fn = os.path.basename(path)
        try:
            status, share = process(path, dry)
        except Exception as exc:  # noqa: BLE001 - report, never abort the batch
            status, share = "ERROR: %s" % exc, None
        tally[status] = tally.get(status, 0) + 1
        if status.startswith("ERROR") or explicit:
            print("  %-34s %s" % (fn, status))

    print(where)
    for k in sorted(tally):
        print("  %-26s %3d" % (k, tally[k]))
    if dry:
        print("\n(dry run — nothing written)")


if __name__ == "__main__":
    main()
