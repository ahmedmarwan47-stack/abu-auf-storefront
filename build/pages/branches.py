"""Branch locator — Figma 'Branches' (4111:22891). Real data from data/branches.json."""
import json, os
from catalog import EXPORT, e
from components import page, page_header

SLUG = "branches.html"
DATA = json.load(open(os.path.join(EXPORT, "data", "branches.json"), encoding="utf-8"))

PIN = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z" '
       'stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.7"/></svg>')


def build():
    total = sum(len(g["branches"]) for g in DATA)
    govs = sorted(DATA, key=lambda g: -len(g["branches"]))

    tabs = "".join(
        f'<button type="button" class="tab-btn{" is-active" if i == 0 else ""} pb-2 font-semibold text-sm whitespace-nowrap" '
        f'data-tab="g{i}">{e(g["gov"])} <span class="latin">({len(g["branches"])})</span></button>'
        for i, g in enumerate(govs))

    panels = ""
    for i, g in enumerate(govs):
        cards = "".join(f"""
              <article class="flex gap-3 bg-white shadow-custom4 p-5 rounded-2xl">
                <span class="mt-0.5 text-cta shrink-0">{PIN}</span>
                <div class="flex flex-col gap-1 min-w-0">
                  <h3 class="font-bold text-[#062A1C] text-base">{e(b['title'])}</h3>
                  <p class="text-neutral-secondary text-sm leading-6">{e(b['address']) or '—'}</p>
                </div>
              </article>""" for b in g["branches"])
        panels += (f'<div class="tab-panel" data-panel="g{i}"{"" if i == 0 else " hidden"}>'
                   f'<div class="gap-4 grid md:grid-cols-2 xl:grid-cols-3">{cards}</div></div>')

    body = f"""{page_header("فروع أبو عوف", [("الرئيسية", "index.html"), ("الفروع", None)])}

      <section class="py-6">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          <p class="mb-8 max-w-[720px] text-neutral-secondary text-base xl:text-lg leading-8">
            يوجد أكثر من <span class="latin">{total}</span> فرع لأبو عوف في
            <span class="latin">{len(DATA)}</span> محافظة في مصر — اختر محافظتك لتجد أقرب فرع إليك.
          </p>
          <div data-tabs>
            <div class="flex gap-6 mb-8 pb-1 border-neutral-divider border-b overflow-x-auto no-scrollbar">{tabs}</div>
            {panels}
          </div>
        </div>
      </section>"""

    return page("فروع أبو عوف | أبو عوف",
                f"أكثر من {total} فرع لأبو عوف في مصر — اعثر على أقرب فرع إليك.",
                body, "branches", "/branches")
