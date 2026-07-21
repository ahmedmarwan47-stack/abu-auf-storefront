"""
Checkout — Figma 'Checkout > Info' (173:17235).

Header and footer collapse to the minimal checkout variants automatically:
scripts.js keys off data-page="checkout" via isCheckout().
"""
from _geo import CAIRO_AREAS, GOVERNORATES
from catalog import e, in_category, money
from components import (
    ICON, breadcrumb, field, page, points_banner, radio_card, select_field,
)

SLUG = "checkout.html"

DELIVERY_FEE = 10.0

STEPS = ["سلة التسوق", "بيانات العميل", "طريقة الدفع", "تأكيد عملية الشراء"]

ICON_GIFT = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
             '<path d="M20 12v9H4v-9M22 7H2v5h20V7ZM12 21V7M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7Z'
             'M12 7h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7Z" stroke="currentColor" stroke-width="1.7" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_BAG = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
            '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6ZM3 6h18M16 10a4 4 0 0 1-8 0" '
            'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_CAL = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
            '<rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.7"/>'
            '<path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>')
ICON_TRUCK = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
              '<path d="M1 3h13v13H1zM14 8h4l3 3v5h-7V8ZM7.5 19a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM19.5 19a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" '
              'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_STORE = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
              '<path d="M3 9 4.5 4h15L21 9M3 9h18M3 9v11h18V9M9 20v-6h6v6" stroke="currentColor" '
              'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def build():
    items = in_category("Dates & Dried Fruits", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE

    SEP = '<span class="text-neutral-disabled">/</span>'
    step_parts = []
    for i, s in enumerate(STEPS):
        current = i == 1
        dot = ("bg-cta text-white" if current
               else "bg-interaction-base text-neutral-secondary")
        text = ("font-semibold text-[#062A1C]" if current
                else "text-neutral-secondary")
        sep = "" if i == len(STEPS) - 1 else SEP
        step_parts.append(
            f'<span class="flex items-center gap-2">'
            f'<span class="place-items-center grid rounded-full size-5 text-xs latin {dot}">{i + 1}</span>'
            f'<span class="{text} text-sm">{e(s)}</span>{sep}</span>'
        )
    steps_html = "".join(step_parts)

    summary_lines = "".join(f"""
                <div class="flex items-center gap-3">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-16 h-16 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-[#062A1C] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                    <span class="text-neutral-secondary text-xs">250 جم</span>
                  </div>
                  <span class="font-bold text-[#062A1C] text-sm latin shrink-0">EGP {money(p['price'])}</span>
                </div>""" for p in items)

    body = f"""
      <section class="py-8">
        <div class="items-start gap-10 grid lg:grid-cols-[1fr_380px] mx-auto px-4 xl:px-[120px] max-w-[1600px]">

          <!-- RTL start: form -->
          <div class="flex flex-col gap-8">
            <div class="flex flex-col gap-3">
              <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">إتمام عملية الشراء بأمان</h1>
              <nav aria-label="خطوات الشراء" class="flex flex-wrap items-center gap-2">{steps_html}</nav>
            </div>

            <form class="flex flex-col gap-8">
              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-[#062A1C] text-lg">نوع الطلب</legend>
                <div class="flex sm:flex-row flex-col gap-4">
{radio_card("order-type", "normal", "طلب عادي", "", ICON_BAG, checked=True)}
{radio_card("order-type", "gift", "إهداء الطلب", "", ICON_GIFT)}
                </div>
              </fieldset>

              <fieldset class="flex flex-col gap-4">
                <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
                  <legend class="font-bold text-[#062A1C] text-lg">بيانات العميل</legend>
                  <p class="text-neutral-secondary text-sm">
                    هل لديك حساب بالفعل؟
                    <a href="login.html" class="font-semibold text-cta underline">تسجيل الدخول</a>
                  </p>
                </div>
                <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", required=True)}
{field("الاسم الاخير", "last-name", required=True)}
                </div>
{field("البريد الالكتروني", "email", "email", required=True)}
{field("رقم الهاتف", "phone", "tel", required=True)}
              </fieldset>

              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-[#062A1C] text-lg">وقت التوصيل</legend>
                <div class="flex sm:flex-row flex-col gap-4">
{radio_card("delivery-time", "now", "اليوم", "في غضون 60 دقيقة", ICON_CAL, checked=True)}
{radio_card("delivery-time", "later", "أختار تاريخ", "حدد اليوم والوقت المناسب", ICON_CAL)}
                </div>
              </fieldset>

              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-[#062A1C] text-lg">طريقة التوصيل</legend>
                <div class="flex sm:flex-row flex-col gap-4">
{radio_card("delivery-method", "delivery", "توصيل", "بإضافة مصاريف اضافية", ICON_TRUCK, checked=True)}
{radio_card("delivery-method", "pickup", "الاستلام من المتجر", "", ICON_STORE)}
                </div>
              </fieldset>

              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-[#062A1C] text-lg">عنوان التوصيل</legend>
{select_field("المدينة", "city", GOVERNORATES, required=True)}
                <div class="gap-4 grid sm:grid-cols-2">
{select_field("الحي", "district", CAIRO_AREAS, required=True)}
{select_field("المنطقة", "area", CAIRO_AREAS, required=True)}
                </div>
{field("رقم العقار و الشارع", "street", required=True)}
                <div class="flex flex-col gap-2">
                  <span class="font-medium text-neutral-secondary text-sm">نوع العقار<span class="text-accent-error">*</span></span>
                  <div class="flex items-center gap-6">
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="property-type" value="apartment" checked class="accent-[#163300] w-4 h-4" />
                      <span class="text-[#062A1C] text-sm">شقة</span>
                    </label>
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="property-type" value="villa" class="accent-[#163300] w-4 h-4" />
                      <span class="text-[#062A1C] text-sm">فيلا</span>
                    </label>
                  </div>
                </div>
                <div class="gap-4 grid grid-cols-2 max-w-[320px]">
{field("الطابق", "floor")}
{field("رقم الشقة", "apartment", required=True)}
                </div>
              </fieldset>

              <a href="thank-you.html" class="bg-cta hover:bg-cta-hover py-4 rounded-full w-full font-semibold text-white text-base text-center transition-colors">
                أكمل إلى الدفع
              </a>
            </form>
          </div>

          <!-- RTL end: summary -->
          <aside class="lg:top-4 lg:sticky flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
            <div class="flex justify-between items-center">
              <h2 class="font-bold text-[#062A1C] text-xl">ملخص السلة</h2>
              <a href="cart.html" class="hover:bg-interaction-base px-4 py-1.5 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">تعديل</a>
            </div>
            <div class="flex flex-col gap-4">{summary_lines}
            </div>
{points_banner(100, 100)}
            <button type="button" class="flex items-center gap-2 font-semibold text-cta text-sm underline self-start">
              هل لديك برومو كود؟
            </button>
            <div class="flex flex-col gap-2 pt-3 border-neutral-divider border-t text-sm">
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
          </aside>
        </div>
      </section>"""

    return page("إتمام عملية الشراء | أبو عوف",
                "أكمل بيانات التوصيل وأتمم طلبك من أبو عوف بأمان.",
                body, "checkout", "/checkout")
