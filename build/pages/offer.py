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

from bundles import BUNDLES, offer_slug, pack_line
from catalog import PRODUCTS, e, money
from components import ICON

SLUG = offer_slug(BUNDLES[0])


def _row(b, it):
    """One flavour, one card — and it stays one card. It never expands into
    variant lines or a picker the way the smart-light rows did: the flavour IS
    the choice, so the stepper on the card is the whole interaction."""
    sub = (f'<span class="text-neutral-secondary text-sm">{e(b["unit_ar"])} {e(b["pack_ar"])}</span>'
           if b.get("pack_ar") else "")
    name = e(it["ar"])
    return f"""
                <li data-offer-row data-key="{e(it['key'])}" data-picked="false"
                    class="offer-row items-center gap-x-3 sm:gap-x-4 gap-y-2 grid grid-cols-[auto_minmax(0,1fr)] sm:grid-cols-[auto_minmax(0,1fr)_auto] bg-white p-3 sm:p-4 border border-neutral-divider rounded-2xl">
                  <!-- One grid, two shapes. From sm: [photo | name | stepper]
                       on one line. Below sm the 44px stepper (~126px) left the
                       name ~50px at 320 and clipped "بالشيكولاتة", so the
                       stepper drops under the name in the same card — the
                       card never opens or closes, it just reflows. -->
                  <img src="{e(it['img'])}" alt="{name}" loading="lazy"
                       class="row-span-2 sm:row-span-1 bg-interaction-base p-1.5 rounded-xl w-20 sm:w-24 h-20 sm:h-24 object-contain" />
                  <span class="flex flex-col gap-1 min-w-0">
                    <span data-offer-name class="font-semibold text-[#062A1C] text-base sm:text-lg leading-6">{name}</span>
                    {sub}
                  </span>
                  <!-- The stepper as a grey track with the buttons inside it.
                       dir="ltr" pins + to the right, as the cart drawer does.
                       size-11: the audited 44px tap target. -->
                  <div dir="ltr" role="group" aria-label="{name}"
                       class="inline-flex justify-self-end sm:justify-self-auto items-center gap-1 bg-interaction-base p-1 rounded-full">
                    <button type="button" data-offer-step="-1" disabled aria-label="إنقاص {name}"
                            class="place-items-center grid disabled:opacity-40 hover:bg-white rounded-full size-11 text-[#062A1C] transition-colors disabled:cursor-not-allowed"><span class="w-5 h-5">{ICON['minus']}</span></button>
                    <output data-offer-qty aria-live="polite" class="min-w-[2.5ch] font-bold text-[#062A1C] text-lg text-center latin">0</output>
                    <button type="button" data-offer-step="1" aria-label="زيادة {name}"
                            class="offer-plus place-items-center grid bg-white disabled:opacity-40 rounded-full size-11 text-[#062A1C] transition-colors disabled:cursor-not-allowed"><span class="w-5 h-5">{ICON['plus']}</span></button>
                  </div>
                </li>"""


def pack_html(b):
    """The pack line under the title, in pack_tag()'s own type."""
    return (f'<span class="font-semibold text-neutral-secondary text-base">'
            f'{e(pack_line(b)[0])}</span>')


def builder_html(b):
    """Stands in for the product page's size chips + price + buy block."""
    size = b["size"]
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

              <!-- Progress, then the cards, then "clear", then the CTA — the
                   smart-light builder's order, so the add button is always the
                   last thing in the builder. One text node per word, so the
                   exact-match dictionary translates each and the English reads
                   "0 of 4 selected". -->
              <div class="flex flex-col gap-3">
                <div class="flex flex-wrap justify-between items-baseline gap-2">
                  <p class="text-[#062A1C] text-base sm:text-lg"><strong data-offer-total class="font-bold text-2xl latin">0</strong> <span>من</span> <span class="latin">{size}</span> <span>تم اختيارها</span></p>
                  <p data-offer-left data-done="false" class="offer-left text-base sm:text-lg">متبقي <span class="latin">{size}</span> للاختيار</p>
                </div>
                <div data-offer-bar role="progressbar" aria-label="تقدّم اختيار العرض" aria-valuemin="0" aria-valuemax="{size}" aria-valuenow="0"
                     class="bg-interaction-base rounded-full h-2 overflow-hidden">
                  <div data-offer-fill class="offer-fill bg-cta rounded-full h-full" style="width:0%"></div>
                </div>
                {cap_note}
              </div>

              <h2 class="sr-only">اختر النكهات</h2>
              <ul data-offer-rows class="flex flex-col gap-3">{rows}
              </ul>

              <div>
                <button type="button" data-offer-clear
                        class="min-h-11 font-semibold text-cta text-base underline underline-offset-4">مسح الكل</button>
              </div>

              <div data-offer-cta-block class="flex flex-col gap-3">
                <button type="button" data-offer-add disabled
                        class="btn-elevate bg-cta hover:bg-cta-hover disabled:bg-neutral-divider py-4 sm:py-5 rounded-full w-full font-semibold text-white disabled:text-neutral-secondary text-base sm:text-lg transition-colors disabled:cursor-not-allowed">
                  <span data-offer-label>أضف <span class="latin">{size}</span> للمتابعة</span>
                </button>
                <p class="text-neutral-secondary text-sm text-center">السعر ثابت مهما اختلف توزيع النكهات.</p>
              </div>
            </div>"""


def sticky_html(b):
    """The product page's sticky bar, for an offer: forwards to
    [data-offer-add], owns no state. Docked at the BOTTOM at every width
    (Ahmed, 2026-11-02: "the CTA should be at the bottom") — the product
    page's own bar moves to the top at lg; this one does not."""
    return f"""
      <div data-offer-sticky aria-hidden="true"
           class="sticky-buybar sticky-buybar--bottom fixed inset-x-0 bottom-0 z-30
                  bg-white border-neutral-divider border-t">
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
