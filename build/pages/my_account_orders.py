"""Orders list — Figma 'Account > Orders' (312:27084)."""
from _account import ORDERS, account_page, card, order_drawer, order_rows

SLUG = "my-account-orders.html"


def build():
    # Whole-row-clickable table + a shared detail drawer (Ahmed, 2026-08-02):
    # the row markup and the drawer both come from _account.py, so the list page
    # and the dashboard stay in step.
    table = f"""
              <div class="overflow-x-auto">
                <table class="w-full min-w-[560px]">
                  <thead>
                    <tr class="border-neutral-divider border-b text-neutral-secondary text-xs">
                      <th class="py-3 ps-2 font-medium text-start">رقم الطلب</th>
                      <th class="py-3 font-medium text-start">التاريخ</th>
                      <th class="py-3 font-medium text-start">حالة الطلب</th>
                      <th class="py-3 font-medium text-start">المجموع</th>
                      <th class="py-3"></th>
                    </tr>
                  </thead>
                  <tbody>{order_rows(ORDERS)}
                  </tbody>
                </table>
              </div>"""

    content = f"""
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">طلباتي</h1>
            {card("", table)}
            {order_drawer(ORDERS)}"""

    return account_page("طلباتي | أبو عوف", "تابع كل طلباتك من أبو عوف.",
                        content, "my-account-orders", "/my-account/orders",
                        "طلباتي", "my-account-orders.html")
