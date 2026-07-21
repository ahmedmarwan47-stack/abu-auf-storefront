#!/usr/bin/env python3
"""
Build the Abu Auf static export.

    python3 build/build.py            # build every page
    python3 build/build.py home shop  # build only these

Each module in build/pages/ exposes SLUG (output filename) and build() ->
HTML string. Shared markup lives in build/components.py, shared data access in
build/catalog.py — edit either and every page picks the change up on the next
run. Runtime chrome (header, footer, overlays) and design tokens live in
static-export/scripts.js and tw-config.js and need no rebuild at all.
"""
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORT = os.path.join(ROOT, "static-export")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pages"))

# Page modules, in build order.
PAGES = [
    "home", "shop", "shop_category", "product", "cart", "checkout",
    "thank_you", "login", "register", "forget_password", "reset_password",
]


def check_assets(name, html):
    """Fail loudly on a reference to a file that isn't in the export."""
    missing = []
    for src in set(re.findall(r'(?:src|srcset|href)="([^"]+)"', html)):
        if src.startswith(("http", "data:", "#", "mailto:", "tel:")):
            continue
        if src.endswith((".html", ".css", ".js")):
            continue
        if not os.path.exists(os.path.join(EXPORT, src)):
            missing.append(src)
    for m in sorted(missing):
        print(f"    ! missing asset: {m}")
    return len(missing)


def main(only=None):
    targets = [p for p in PAGES if not only or p in only]
    if only:
        unknown = set(only) - set(PAGES)
        if unknown:
            print(f"unknown page(s): {', '.join(sorted(unknown))}")
            return 1

    total_missing = 0
    for name in targets:
        mod = importlib.import_module(name)
        html = mod.build()
        dest = os.path.join(EXPORT, mod.SLUG)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
        missing = check_assets(name, html)
        total_missing += missing
        status = "ok" if not missing else f"{missing} missing asset(s)"
        print(f"  {mod.SLUG:<28} {len(html):>8,} bytes   {status}")

    print(f"\nbuilt {len(targets)} page(s)"
          + (f"; {total_missing} broken asset reference(s)" if total_missing else ""))
    return 1 if total_missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or None))
