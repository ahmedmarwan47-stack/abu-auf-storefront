"""Shopping cart — Figma 'Cart' (4231:22875)."""
from catalog import in_category, money, rail_products
from components import (
    accordion, cart_line, carousel, page, page_header, points_banner,
    product_card, section_heading,
)

SLUG = "cart.html"

DELIVERY_FEE = 10.0
MIN_ORDER = 100.0


def build():
    items = [(p, 1) for p in in_category("Dates & Dried Fruits", 3)]
    subtotal = sum(p["price"] * q for p, q in items)
    total = subtotal + DELIVERY_FEE
    short = max(0, MIN_ORDER - subtotal)

    lines = "".join(cart_line(p, q) for p, q in items)
    more = rail_products("Nuts | Seeds & Crackers", "Snacks", limit=10)

    note_panel = """
                      <div class="flex flex-col gap-3">
                        <textarea rows="3" placeholder="أضف ملاحظة"
                                  class="bg-white px-4 py-3 border-2 border-neutral-divider focus:border-cta rounded-xl outline-none w-full text-[#062A1C] text-sm transition-colors"></textarea>
                        <button type="button" class="bg-cta hover:bg-cta-hover px-6 py-2 rounded-full font-semibold text-white text-sm transition-colors self-end">أضف</button>
                      </div>"""

    below_min = short > 0
    order_btn = (
        f'<button type="button" disabled class="bg-neutral-disabled py-4 rounded-full w-full '
        f'font-semibold text-white text-base cursor-not-allowed">أطلب الآن</button>'
        if below_min else
        '<a href="checkout.html" class="block bg-cta hover:bg-cta-hover py-4 rounded-full '
        'w-full font-semibold text-white text-base text-center transition-colors">أطلب الآن</a>'
    )
    warning = (
        f'<p class="flex items-start gap-2 text-accent-error text-xs leading-5">'
        f'<span aria-hidden="true">⚠</span>'
        f'متبقي <span class="latin">EGP {money(short)}</span> لاستكمال الحد الأدنى للطلب</p>'
        if below_min else ""
    )

    body = f"""{page_header("سلة التسوق", [("الرئيسية", "index.html"), ("سلة التسوق", None)])}

      <!-- ============================== CART ============================== -->
      <section class="py-8 xl:py-10">
        <div class="items-start gap-6 lg:gap-8 grid grid-cols-1 lg:grid-cols-[380px_1fr] mx-auto px-4 max-w-[1536px]">

          <!-- RTL start: summary. DOM-first so RTL puts it in the right column
               at lg; the Figma mobile cart (804:32907) leads with the line
               items and drops the summary beneath them, so below lg it moves
               visually to the end. -->
          <aside class="flex flex-col gap-4 lg:sticky lg:top-4 order-last lg:order-none min-w-0">
            <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              <h2 class="font-bold text-[#062A1C] text-xl">ملخص السلة</h2>
              <div class="flex flex-col gap-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-neutral-secondary">مصاريف التوصيل</span>
                  <span class="font-semibold text-[#062A1C] latin">EGP {money(DELIVERY_FEE)}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-neutral-secondary">الإجمالي</span>
                  <span class="font-semibold text-[#062A1C] latin" data-cart-subtotal>EGP {money(subtotal)}</span>
                </div>
              </div>
              <button type="button" class="flex items-center gap-2 font-semibold text-cta text-sm underline self-start">
                هل لديك برومو كود؟
              </button>
              <div class="flex justify-between items-center pt-3 border-neutral-divider border-t">
                <span class="font-bold text-[#062A1C] text-base">الإجمالي</span>
                <span class="font-bold text-[#062A1C] text-2xl latin" data-cart-total>EGP {money(total)}</span>
              </div>
{points_banner()}
              {order_btn}
              {warning}
            </div>

            <div class="bg-white shadow-custom4 px-6 py-2 rounded-[20px]">
              {accordion([("أضف ملاحظات على الطلب", note_panel)])}
            </div>
          </aside>

          <!-- RTL end: line items -->
          <div class="bg-white shadow-custom4 px-6 py-2 rounded-[20px] min-w-0" data-cart-lines>{lines}
          </div>
        </div>
      </section>

      <!-- =========================== SHOP MORE =========================== -->
      <section class="py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>"""

    return page("سلة التسوق | أبو عوف",
                "راجع منتجاتك وأتمم طلبك من أبو عوف.",
                body, "cart", "/cart")
