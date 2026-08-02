"""Account overview — Figma 'Account > Overview' (312:13041)."""
from _account import (
    CUSTOMER, ORDERS, account_page, card, order_drawer, order_tracking_card,
    reorder_card,
)
from catalog import e

SLUG = "my-account.html"


def build():
    # The dashboard is interactive now, not a data dump (Ahmed, 2026-08-02):
    # a current-order tracker and a last-order re-order, with a link out to the
    # full orders list rather than the whole table inline.
    current = next((o for o in ORDERS if o["tone"] == "amber"), ORDERS[0])
    last = next((o for o in ORDERS if o["tone"] == "green"), ORDERS[-1])

    content = f"""
            <div class="flex items-center gap-3 bg-interaction-base px-5 py-4 rounded-xl">
              <span class="place-items-center grid bg-primary rounded-full text-white size-7 text-sm">✓</span>
              <span class="font-semibold text-[#062A1C] text-sm">شكرا لتسجيلك حساب معنا !</span>
            </div>

            <div class="flex flex-wrap justify-between items-start gap-4">
              <div class="flex flex-col gap-1">
                <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">صفحة حسابي الرئيسية</h1>
                <p class="text-neutral-secondary text-sm">يمكنك إدارة الطلبات والمحفظة ومعلومات الحساب الخاصة بك هنا.</p>
              </div>
              <div class="flex flex-col items-center gap-1 bg-white shadow-custom4 px-6 py-4 border-2 border-primary rounded-xl">
                <span class="font-bold text-[#062A1C] text-xl latin" data-wallet-amount>EGP {CUSTOMER['wallet']}</span>
                <span class="text-neutral-secondary text-xs">رصيد محفظتي</span>
              </div>
            </div>

            <div class="flex flex-col gap-4">
              <div class="flex flex-wrap justify-between items-center gap-3">
                <h2 class="font-bold text-[#062A1C] text-lg">طلباتي</h2>
                <a href="my-account-orders.html" class="hover:bg-interaction-base px-5 py-2 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">كل الطلبات</a>
              </div>
              {order_tracking_card(current)}
              {reorder_card(last)}
            </div>

            {card("شارك الموقع مع الأصحاب والعائلة", '''
              <p class="text-neutral-secondary text-sm">أنسخ الرابط أدناه وشاركه مع عائلتك وأصدقائك واحصل على خصومات حصرية</p>
              <div class="flex items-center gap-2 bg-interaction-base px-4 py-2 rounded-xl">
                <span data-ref-link class="flex-1 min-w-0 text-neutral-secondary text-xs truncate latin">WWW.ABUAUF.COM/REF/1-0200,20409</span>
                <button type="button" data-copy-ref class="bg-cta hover:bg-cta-hover px-4 py-1.5 rounded-full font-semibold text-white text-xs transition-colors">نسخ</button>
              </div>''')}

            <h2 class="font-bold text-[#062A1C] text-lg">بياناتي</h2>
            <div class="gap-6 grid md:grid-cols-2">
              {card("بيانات الحساب", f'''
                <div class="flex flex-col gap-1 text-sm">
                  <span class="text-[#062A1C]">{e(CUSTOMER['full'])}</span>
                  <span class="text-neutral-secondary latin">{e(CUSTOMER['email'])}</span>
                  <span class="text-neutral-secondary latin">{e(CUSTOMER['phone'])}</span>
                </div>''', "تعديل", "my-account-profile.html")}
              {card("عنواني الرئيسي", '''
                <div class="flex flex-col gap-1 text-neutral-secondary text-sm">
                  <span>شقة 3 - 220 شارع الحرية - الدور الأول</span>
                  <span>مصر الجديدة</span>
                  <span>القاهرة، مصر</span>
                </div>''', "تعديل", "my-account-addresses.html")}
            </div>
            {order_drawer(ORDERS)}"""

    return account_page("حسابي | أبو عوف",
                        "إدارة طلباتك وعناوينك ومحفظتك في أبو عوف.",
                        content, "my-account", "/my-account",
                        "حسابي", "my-account.html")
