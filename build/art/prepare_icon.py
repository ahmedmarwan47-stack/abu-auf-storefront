"""
Turn a supplied 3D icon render into the transparent PNG the site references.

The client's icons arrive as square renders on a **white** studio background.
Every 3D icon on this site sits on a coloured surface — the utility bar is
beige #E8DFD0, the account tiles are #EDEFEB — so a white-backed file draws a
white box inside the plate. Same defect, same cure as the product photos, so
this does not reimplement the cut: it imports `flood_background` and
`soft_alpha` from `isolate_products.py`, which are border-connected (white
*inside* the artwork survives) and ramp the edge alpha so no white halo is left
behind.

On top of that it does the two things an icon needs and a product photo does
not: trim to the artwork's own alpha bounds — the client's 3D set is trimmed
(voucher-3d.png is 256x186, not a padded square), so an untrimmed icon reads
smaller than its neighbours in the same box — and downscale, because the
renders arrive around 1200px for something that paints at 22.

    python3 build/art/prepare_icon.py <source> <dest.png> [max-edge]

Idempotent in the way that matters: it never writes over its source, and a
source that already carries alpha keeps it (the cut is skipped, the trim and
the resize still run).
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from isolate_products import already_isolated, flood_background, soft_alpha  # noqa: E402

DEFAULT_MAX_EDGE = 256
# Keep a hair of padding after the trim so the soft shadow is not clipped flush
# against the frame.
PAD = 4


def prepare(src, dst, max_edge=DEFAULT_MAX_EDGE):
    im = Image.open(src)

    if already_isolated(im):
        out = im.convert("RGBA")
    else:
        rgb = np.array(im.convert("RGB"))
        bg = flood_background(rgb)
        share = bg.mean()
        if share < 0.005:
            raise SystemExit("%s has no white border to cut" % src)
        if share > 0.985:
            raise SystemExit("%s: the fill ran away through the artwork" % src)
        out = Image.fromarray(np.dstack([rgb, soft_alpha(rgb, bg)]))

    box = out.getbbox()  # alpha-aware: the bounds of everything not fully clear
    if box:
        l, t, r, b = box
        out = out.crop((max(0, l - PAD), max(0, t - PAD),
                        min(out.width, r + PAD), min(out.height, b + PAD)))

    if max(out.size) > max_edge:
        scale = max_edge / float(max(out.size))
        out = out.resize((max(1, round(out.width * scale)),
                          max(1, round(out.height * scale))), Image.LANCZOS)

    out.save(dst, "PNG", optimize=True)
    print("%s -> %s  %dx%d  %d bytes" % (src, dst, out.width, out.height, os.path.getsize(dst)))


USAGE = "usage: python3 build/art/prepare_icon.py <source> <dest.png> [max-edge]"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(USAGE)
    prepare(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_MAX_EDGE)
