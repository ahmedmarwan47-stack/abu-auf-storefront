"""Order confirmation — Figma 'Thanks' (268:11025)."""
from catalog import e, in_category, money, rail_products
from components import carousel, page, product_card, section_heading

SLUG = "thank-you.html"

DELIVERY_FEE = 30.0
ORDER_NO = "304585"

STEPS = [
    ("تم الطلب", "بأنتظار تأكيد متجر", True),
    ("جاري تجهيز الطلب", "سيتم تجهيز الطلب قريباً", True),
    ("جاري تجهيز الطلب", "طلبك في الطريق إليك", False),
    ("تم تسليم الطلب", "سعدنا بخدمتك ونود أن تراك مرة أخرى", False),
]

CUSTOMER = [
    ("الاسم الأول", "محمد"), ("اسم العائلة", "عادل"),
    ("البريد الالكتروني", "MOSAWABI15@GMAIL.COM"),
    ("رقم الهاتف", "01148822922"),
]

DELIVERY = [
    ("الميعاد المتوقع للتوصيل", "23 مارس 2026"),
    ("المدينة", "القاهرة"), ("الحي", "القاهرة الجديدة"), ("المنطقة", "التجمع"),
    ("رقم العقار و الشارع", "شارع 5 عقار رقم 4"),
    ("الطابق", "5"), ("الشقة", "2"),
]

CHECK = ('<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4">'
         '<path d="m5 13 4 4L19 7" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _rows(pairs):
    return "".join(
        f'<div class="flex flex-col gap-0.5">'
        f'<span class="text-neutral-secondary text-xs">{e(k)}</span>'
        f'<span class="font-semibold text-[#062A1C] text-sm break-words">{e(v)}</span></div>'
        for k, v in pairs
    )


def build():
    items = in_category("Dates & Dried Fruits", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE
    more = rail_products("Nuts | Seeds & Crackers", "Snacks", limit=10)

    steps_html = "".join(f"""
              <li class="flex flex-col flex-1 items-center gap-2 text-center">
                <span class="place-items-center grid rounded-full size-8 {'bg-primary text-white' if done else 'bg-interaction-base text-neutral-secondary'}">
                  {CHECK if done else f'<span class="font-semibold text-sm latin">{i + 1}</span>'}
                </span>
                <span class="font-semibold text-[#062A1C] text-sm">{e(heading)}</span>
                <span class="max-w-[160px] text-neutral-secondary text-xs leading-5">{e(sub)}</span>
              </li>""" for i, (heading, sub, done) in enumerate(STEPS))

    lines = "".join(f"""
                <div class="flex items-center gap-3 py-3 border-neutral-divider border-b last:border-0">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-16 h-16 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-[#062A1C] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                    <span class="text-neutral-secondary text-xs">250 جم</span>
                    <span class="text-neutral-secondary text-xs">عدد <span class="latin">1</span></span>
                  </div>
                  <span class="font-bold text-[#062A1C] text-sm latin shrink-0">EGP {money(p['price'])}</span>
                </div>""" for p in items)

    body = f"""
      <section class="pt-10 pb-6">
        <div class="flex flex-col gap-3 mx-auto px-4 max-w-[1200px]">
          <div class="flex items-center gap-3">
            <span class="place-items-center grid bg-primary rounded-full text-white size-8">{CHECK}</span>
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">شكراً لك</h1>
          </div>
          <p class="font-semibold text-[#062A1C] text-base">تم تقديم طلبك بنجاح</p>
          <p class="text-neutral-secondary text-sm leading-7">
            إذا كانت لديك أسئلة حول طلبك، يمكنك مراسلتنا عبر البريد الإلكتروني على
            <a href="mailto:info@abuauf.com" class="font-semibold text-cta underline latin">INFO@ABUAUF.COM</a>
            أو الاتصال بنا على <a href="tel:19969" class="font-semibold text-cta underline latin">19969</a>
          </p>
        </div>
      </section>

      <!-- ========================== ORDER TRACKER ========================== -->
      <section class="pb-8">
        <div class="mx-auto px-4 max-w-[1200px]">
          <ol class="flex md:flex-row flex-col gap-6 md:gap-2 bg-white shadow-custom4 p-6 rounded-[20px]">{steps_html}
          </ol>
        </div>
      </section>

      <!-- ============================ ORDER DETAIL ============================ -->
      <section class="pb-12">
        <!-- The order-detail block sits in a narrower 1200px column (Ahmed,
             2026-08-02): a full 1536 made the order box huge for its few items
             and the customer column a long narrow strip. Order stays the wider
             box, the customer info is 2-up so it is no longer a tall ribbon,
             and the two now read as a balanced pair. -->
        <div class="items-stretch gap-6 xl:gap-8 grid grid-cols-1 lg:grid-cols-[1fr_400px] mx-auto px-4 max-w-[1200px]">
          <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px] min-w-0">
            <h2 class="font-bold text-[#062A1C] text-xl">طلب رقم <span class="latin">#{ORDER_NO}</span></h2>
            <div class="flex flex-col">{lines}
            </div>
            <!-- mt-auto sinks the totals to the bottom so the (shorter) order box
                 fills the height the taller customer box sets — the two columns
                 are items-stretch, so they end level (Ahmed, 2026-08-02). -->
            <div class="flex flex-col gap-2 mt-auto pt-3 border-neutral-divider border-t text-sm">
              <div class="flex justify-between">
                <span class="text-neutral-secondary">مصاريف التوصيل</span>
                <span class="font-semibold text-[#062A1C] latin">EGP {money(DELIVERY_FEE)}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-neutral-secondary">الإجمالي</span>
                <span class="font-semibold text-[#062A1C] latin">EGP {money(subtotal)}</span>
              </div>
            </div>
            <div class="flex justify-between items-center pt-3 border-neutral-divider border-t">
              <span class="font-bold text-[#062A1C] text-base">الإجمالي</span>
              <span class="font-bold text-[#062A1C] text-2xl latin">EGP {money(total)}</span>
            </div>
          </div>

          <div class="flex flex-col gap-5 bg-interaction-base p-6 rounded-[20px]">
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#062A1C] text-base">بيانات العميل</h2>
              <div class="gap-4 grid sm:grid-cols-2">{_rows(CUSTOMER)}
              </div>
            </div>
            <div class="flex flex-col gap-3 pt-5 border-neutral-divider border-t">
              <h2 class="font-bold text-[#062A1C] text-base">بيانات التوصيل</h2>
              <div class="gap-4 grid sm:grid-cols-2">{_rows(DELIVERY)}
              </div>
            </div>
            <a href="my-account-orders.html" class="bg-cta hover:bg-cta-hover px-8 py-3 rounded-full font-semibold text-white text-sm transition-colors self-end">حالة الطلب</a>
          </div>
        </div>
      </section>

      <!-- ============================= SHOP MORE ============================= -->
      <section class="pb-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>"""

    return page("تم استلام طلبك | أبو عوف",
                "شكراً لك — تم تقديم طلبك بنجاح في أبو عوف.",
                body, "thank-you", "/thank-you")
