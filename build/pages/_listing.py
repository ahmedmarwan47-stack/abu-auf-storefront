"""
Shared product-listing layout — Figma 'Collection' (173:17211).

Both shop.html (everything) and shop-category.html (one category) are the same
view with different data, so they share this builder. Change the listing here
and both pages follow.
"""
from catalog import e
from components import chip, page, page_header, product_grid, sort_select

SORT_OPTIONS = [
    ("popular", "الأكثر مبيعاً"),
    ("newest", "وصل حديثاً"),
    ("price-asc", "السعر: من الأقل"),
    ("price-desc", "السعر: من الأعلى"),
]


def listing(title_text, description, heading, trail, chips, products,
            page_id, path, intro=None, active_chip=None):
    chip_html = "".join(
        chip(label, href, active=(label == active_chip)) for label, href in chips
    )
    intro_html = (
        f'<p class="max-w-[720px] text-neutral-secondary text-base xl:text-lg leading-8">{e(intro)}</p>'
        if intro else ""
    )

    body = f"""{page_header(heading, trail)}

      <!-- ============================== FILTERS ============================== -->
      <section class="pt-6">
        <div class="flex flex-col gap-6 mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          {intro_html}
          <div class="flex justify-between items-center gap-4">
            <div class="flex gap-2 -mx-1 px-1 overflow-x-auto no-scrollbar">{chip_html}
            </div>
{sort_select(SORT_OPTIONS)}
          </div>
        </div>
      </section>

      <!-- ============================== PRODUCTS ============================== -->
      <section class="py-8 xl:py-10">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          <p class="mb-6 text-neutral-secondary text-sm">
            <span class="latin">{len(products)}</span> منتج
          </p>
          {product_grid(products)}
          <div class="flex justify-center mt-12">
            <button type="button" class="hover:bg-interaction-base px-10 py-3 border border-cta rounded-full font-semibold text-cta text-base transition-colors">
              عرض المزيد
            </button>
          </div>
        </div>
      </section>"""

    return page(title_text, description, body, page_id, path)
