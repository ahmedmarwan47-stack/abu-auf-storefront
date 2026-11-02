"""Mix-and-match offer page — "كوّن عرضك".

One page per offer in build/bundles.py: offer-<slug>.html. The first offer is
this module's own SLUG and the rest fan out through build_many(), so no offer
is written twice.

The page IS the product page. `product._render(base, offer=b)` renders the
offer's base SKU (bundles.py `base`) through the exact product-page layout —
gallery, best-seller badge, rating, social proof, points, description, specs,
delivery strip, benefits/storage accordion, FAQ, the "قد يعجبك أيضاً" list,
reviews, recipes, the "more from Abu Auf" rail, recently viewed and the sticky
bar — and swaps ONLY the purchase controls for the builder below. Nothing on
the product page is cut, and a change to it reaches the offer automatically.

The builder rows are rendered here, once; initOffer() in scripts.js repaints
numbers and disabled states from the JSON config, so focus survives every
press (the same reason the cart drawer is a keyed reconcile, not an innerHTML
swap). With JS off the page is the full product page with a disabled button.
"""
import json

from bundles import BUNDLES, offer_slug, pack_line, units_ar
from catalog import PRODUCTS, e, money
from components import ICON

SLUG = offer_slug(BUNDLES[0])


def _row(b, it):
    sub = (f'<span class="text-neutral-secondary text-xs">{e(b["pack_ar"])}</span>'
           if b.get("pack_ar") else "")
    name = e(it["ar"])
    return f"""
                <li data-offer-row data-key="{e(it['key'])}" data-picked="false"
                    class="offer-row relative flex items-center gap-3 py-3 ps-3 border-neutral-divider border-b last:border-b-0">
                  <img src="{e(it['img'])}" alt="{name}" loading="lazy"
                       class="offer-thumb bg-interaction-base p-1 rounded-xl w-14 h-14 object-contain shrink-0" />
                  <span class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span data-offer-name class="font-semibold text-[#062A1C] text-sm xl:text-base leading-5">{name}</span>
                    {sub}
                  </span>
                  <!-- dir="ltr" pins + to the right, as the cart drawer and the
                       sticky buy bar already do. size-11: the audited 44px. -->
                  <div dir="ltr" role="group" aria-label="{name}"
                       class="inline-flex items-center gap-1 bg-white p-1 border border-neutral-divider rounded-full shrink-0">
                    <button type="button" data-offer-step="-1" disabled aria-label="إنقاص {name}"
                            class="place-items-center grid disabled:opacity-40 border border-neutral-divider hover:bg-interaction-base disabled:hover:bg-transparent rounded-full size-11 text-[#062A1C] transition-colors disabled:cursor-not-allowed"><span class="w-5 h-5">{ICON['minus']}</span></button>
                    <output data-offer-qty aria-live="polite" class="min-w-[2.5ch] font-bold text-[#062A1C] text-base text-center latin">0</output>
                    <button type="button" data-offer-step="1" aria-label="زيادة {name}"
                            class="place-items-center grid bg-cta hover:bg-cta-hover disabled:bg-cta-light rounded-full size-11 text-white disabled:text-neutral-secondary transition-colors disabled:cursor-not-allowed"><span class="w-5 h-5">{ICON['plus']}</span></button>
                  </div>
                </li>"""


def pack_html(b):
    """The pack line under the title, in pack_tag()'s own type."""
    return (f'<span class="font-semibold text-neutral-secondary text-base">'
            f'{e(pack_line(b)[0])}</span>')


def builder_html(b):
    """Stands in for the product page's size chips + price + buy block."""
    size = b["size"]
    units = units_ar(b, size)
    config = {
        "slug": b["slug"],
        "id": "offer:" + b["slug"],
        "name": b["name_ar"],
        "price": b["price"],
        "size": size,
        "maxEach": b.get("max_each"),
        "image": b["images"][0],
        "unit": b["unit_ar"],
        "units": b["unit_plural_ar"],
        "items": [{"key": it["key"], "short": it["short"]} for it in b["items"]],
    }
    # `</` can never appear inside the JSON, so it cannot close the script tag.
    config_json = json.dumps(config, ensure_ascii=False).replace("</", "<\\/")
    old_price = (
        f'<span class="text-neutral-secondary text-xl line-through latin">EGP {money(b["compare_at"])}</span>'
        if b.get("compare_at") else ""
    )
    save_chip = (
        f'<span class="bg-primary px-2.5 py-1 rounded-full font-semibold text-white text-xs">وفّر <span class="latin">EGP {money(b["compare_at"] - b["price"])}</span></span>'
        if b.get("compare_at") else ""
    )
    cap_note = (
        f'<p class="text-neutral-secondary text-xs">حد أقصى <span class="latin">{b["max_each"]}</span> من كل نكهة.</p>'
        if b.get("max_each") else ""
    )
    rows = "".join(_row(b, it) for it in b["items"])
    return f"""
            <div data-offer class="flex flex-col gap-5">
              <script type="application/json" data-offer-config>{config_json}</script>
              <!-- Same yellow marker-band price as every product page. It is
                   the offer's ONE price and never moves with the mix. -->
              <div class="flex flex-wrap items-center gap-3">
                {old_price}
                <span style="line-height:.6" class="bg-accent-yellow px-3 rounded font-bold text-[#062A1C] text-2xl latin">EGP {money(b["price"])}</span>
                {save_chip}
              </div>

              <!-- Progress towards the offer's size. One text node per word,
                   so the exact-match dictionary translates each and the
                   English reads in the same order: "Picked 1 of 4 boxes". -->
              <div class="flex flex-col gap-2.5 bg-interaction-base p-4 rounded-2xl">
                <div class="flex flex-wrap justify-between items-baseline gap-2">
                  <p class="font-semibold text-[#062A1C] text-sm"><span>اخترت</span> <span data-offer-total class="latin">0</span> <span>من</span> <span class="latin">{size}</span> <span>{e(units)}</span></p>
                  <p data-offer-left data-done="false" class="offer-left font-semibold text-sm">متبقي <span class="latin">{size}</span></p>
                </div>
                <div data-offer-bar role="progressbar" aria-label="تقدّم اختيار العرض" aria-valuemin="0" aria-valuemax="{size}" aria-valuenow="0"
                     class="bg-white rounded-full h-2 overflow-hidden">
                  <div data-offer-fill class="offer-fill bg-cta rounded-full h-full" style="width:0%"></div>
                </div>
                {cap_note}
              </div>

              <div class="flex flex-col gap-1">
                <div class="flex justify-between items-center gap-3">
                  <h2 class="font-bold text-[#062A1C] text-lg">اختر النكهات</h2>
                  <button type="button" data-offer-clear hidden
                          class="px-2 min-h-11 font-semibold text-cta text-sm underline">مسح الاختيار</button>
                </div>
                <ul data-offer-rows class="flex flex-col">{rows}
                </ul>
              </div>

              <div data-offer-cta-block class="flex flex-col gap-2">
                <button type="button" data-offer-add disabled
                        class="btn-elevate bg-cta hover:bg-cta-hover disabled:bg-cta-light py-4 rounded-full w-full font-semibold text-white disabled:text-neutral-secondary text-base transition-colors disabled:cursor-not-allowed">
                  <span data-offer-label>اختر <span class="latin">{size}</span> {e(units)} للمتابعة</span>
                </button>
                <p class="text-neutral-secondary text-xs text-center">السعر ثابت مهما اختلف توزيع النكهات.</p>
              </div>
            </div>"""


def sticky_html(b):
    """The product page's sticky bar, for an offer: forwards to
    [data-offer-add], owns no state."""
    return f"""
      <div data-offer-sticky aria-hidden="true"
           class="sticky-buybar fixed inset-x-0 bottom-0 lg:bottom-auto lg:top-12 z-30
                  bg-white border-neutral-divider border-t lg:border-t-0 lg:border-b">
        <div class="flex items-center gap-3 lg:gap-6 mx-auto px-4 max-w-[1536px] py-3">
          <img src="{e(b["images"][0])}" alt=""
               class="hidden sm:block bg-interaction-base p-1 rounded-xl w-12 xl:w-14 h-12 xl:h-14 object-contain shrink-0" />
          <div class="flex flex-col flex-1 min-w-0">
            <p class="font-bold text-[#062A1C] text-sm xl:text-base truncate">{e(b["name_ar"])}</p>
            <span class="text-neutral-secondary text-xs"><span data-offer-total class="latin">0</span> / <span class="latin">{b["size"]}</span> · <span class="font-bold text-primary latin">EGP {money(b["price"])}</span></span>
          </div>
          <button type="button" data-offer-sticky-add tabindex="-1"
                  class="bg-cta hover:bg-cta-hover disabled:bg-cta-light px-5 xl:px-8 py-2.5 rounded-full font-semibold text-white disabled:text-neutral-secondary text-sm whitespace-nowrap transition-colors shrink-0">أضف للسلة</button>
        </div>
      </div>"""


def _base(b):
    return next(p for p in PRODUCTS if p.get("id") == b["base"])


def _page(b):
    from product import _render
    return _render(_base(b), offer=b)


def build():
    return _page(BUNDLES[0])


def build_many():
    return [(offer_slug(b), _page(b)) for b in BUNDLES[1:]]
