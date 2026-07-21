"""Orders list — Figma 'Account > Orders' (312:27084)."""
from _account import ORDERS, STATUS_STYLE, account_page, card
from catalog import e, money

SLUG = "my-account-orders.html"


def build():
    rows = "".join(f"""
                  <tr class="border-neutral-divider border-b last:border-0">
                    <td class="py-4 font-semibold text-[#062A1C] text-sm latin">{no}</td>
                    <td class="py-4 text-neutral-secondary text-sm">{e(date)}</td>
                    <td class="py-4"><span class="inline-flex px-3 py-1 rounded-full font-semibold text-xs {STATUS_STYLE[tone]}">{e(status)}</span></td>
                    <td class="py-4 font-semibold text-[#062A1C] text-sm latin">EGP {money(total)}</td>
                    <td class="py-4 text-end"><a href="my-account-order.html" class="hover:bg-interaction-base px-4 py-1.5 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">عرض</a></td>
                  </tr>""" for no, date, status, tone, total in ORDERS * 2)

    table = f"""
              <div class="overflow-x-auto">
                <table class="w-full min-w-[560px]">
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
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">طلباتي</h1>
            {card("", table)}"""

    return account_page("طلباتي | أبو عوف", "تابع كل طلباتك من أبو عوف.",
                        content, "my-account-orders", "/my-account/orders",
                        "طلباتي", "my-account-orders.html")
