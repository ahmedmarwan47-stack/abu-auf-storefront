"""Wallet — Figma 'Account > Wallet' (312:24917)."""
from _account import CUSTOMER, account_page, card

SLUG = "my-account-wallet.html"

TXNS = [
    ("28 مارس 2026", "استرداد من طلب #30941", "+120"),
    ("21 مارس 2026", "خصم على طلب #30942", "-100"),
    ("14 مارس 2026", "مكافأة تسجيل", "+200"),
]


def build():
    rows = "".join(f"""
                  <tr class="border-neutral-divider border-b last:border-0">
                    <td class="py-4 text-neutral-secondary text-sm">{date}</td>
                    <td class="py-4 text-[#062A1C] text-sm">{label}</td>
                    <td class="py-4 font-semibold text-sm latin text-end {'text-primary' if amount.startswith('+') else 'text-accent-error'}">EGP {amount}</td>
                  </tr>""" for date, label, amount in TXNS)

    content = f"""
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">محفظتي</h1>
            <div class="flex flex-col items-center gap-2 bg-primary p-8 rounded-[20px] text-white text-center">
              <span class="text-white/70 text-sm">رصيد محفظتي</span>
              <span class="font-bold text-4xl latin">EGP {CUSTOMER['wallet']}</span>
            </div>
            {card("سجل المعاملات", f'''<div class="overflow-x-auto"><table class="w-full min-w-[420px]">
              <tbody>{rows}</tbody></table></div>''')}"""

    return account_page("محفظتي | أبو عوف", "رصيد محفظتك وسجل المعاملات.",
                        content, "my-account-wallet", "/my-account/wallet",
                        "محفظتي", "my-account-wallet.html")
