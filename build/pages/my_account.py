"""Account overview — Figma 'Account > Overview' (312:13041)."""
from _account import CUSTOMER, ORDERS, STATUS_STYLE, account_page, card
from catalog import e, money

SLUG = "my-account.html"


def build():
    rows = "".join(f"""
                  <tr class="border-neutral-divider border-b last:border-0">
                    <td class="py-4 font-semibold text-[#062A1C] text-sm latin">{no}</td>
                    <td class="py-4 text-neutral-secondary text-sm">{e(date)}</td>
                    <td class="py-4"><span class="inline-flex px-3 py-1 rounded-full font-semibold text-xs {STATUS_STYLE[tone]}">{e(status)}</span></td>
                    <td class="py-4 font-semibold text-[#062A1C] text-sm latin">EGP {money(total)}</td>
                    <td class="py-4 text-end"><a href="my-account-order.html" class="hover:bg-interaction-base px-4 py-1.5 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">عرض</a></td>
                  </tr>""" for no, date, status, tone, total in ORDERS)

    orders_table = f"""
              <div class="overflow-x-auto">
                <table class="w-full min-w-[560px] text-start">
                  <thead>
                    <tr class="border-neutral-divider border-b text-neutral-secondary text-xs">
                      <th class="py-3 font-medium text-start">رقم الطلب</th>
                      <th class="py-3 font-medium text-start">التاريخ</th>
                      <th class="py-3 font-medium text-start">حالة الطلب</th>
                      <th class="py-3 font-medium text-start">المجموع</th>
                      <th class="py-3"></th>
                    </tr>
                  </thead>
                  <tbody>{rows}
                  </tbody>
                </table>
              </div>"""

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
                <span class="font-bold text-[#062A1C] text-xl latin">EGP {CUSTOMER['wallet']}</span>
                <span class="text-neutral-secondary text-xs">رصيد محفظتي</span>
              </div>
            </div>

            {card("شارك الموقع مع الأصحاب والعائلة", '''
              <p class="text-neutral-secondary text-sm">أنسخ الرابط أدناه وشاركه مع عائلتك وأصدقائك واحصل على خصومات حصرية</p>
              <div class="flex items-center gap-2 bg-interaction-base px-4 py-2 rounded-xl">
                <span class="flex-1 text-neutral-secondary text-xs truncate latin">WWW.ABUAUF.COM/REF/1-0200,20409</span>
                <button type="button" class="bg-cta hover:bg-cta-hover px-4 py-1.5 rounded-full font-semibold text-white text-xs transition-colors">نسخ</button>
              </div>''')}

            {card("طلباتي الحالية", orders_table, "كل الطلبات", "my-account-orders.html")}

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
            </div>"""

    return account_page("حسابي | أبو عوف",
                        "إدارة طلباتك وعناوينك ومحفظتك في أبو عوف.",
                        content, "my-account", "/my-account",
                        "حسابي", "my-account.html")
