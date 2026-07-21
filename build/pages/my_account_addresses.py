"""Addresses — Figma 'Account > Addresses' (312:16654)."""
from _account import account_page, card

SLUG = "my-account-addresses.html"

ADDRESSES = [
    ("المنزل", "شقة 3 - 220 شارع الحرية - الدور الأول", "مصر الجديدة، القاهرة", True),
    ("العمل", "مبنى 12 - شارع التسعين الشمالي", "التجمع الخامس، القاهرة", False),
]


def build():
    cards = "".join(card(
        label,
        f'''<div class="flex flex-col gap-1 text-neutral-secondary text-sm">
              <span>{line1}</span><span>{line2}</span>
            </div>
            {'<span class="bg-interaction-base px-3 py-1 rounded-full font-semibold text-primary text-xs self-start">العنوان الرئيسي</span>' if default else ''}
            <div class="flex gap-2">
              <button type="button" class="hover:bg-interaction-base px-4 py-1.5 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">تعديل</button>
              <button type="button" class="px-4 py-1.5 font-semibold text-accent-error text-xs">حذف</button>
            </div>''')
        for label, line1, line2, default in ADDRESSES)

    content = f"""
            <div class="flex flex-wrap justify-between items-center gap-3">
              <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">عناويني</h1>
              <button type="button" class="bg-cta hover:bg-cta-hover px-6 py-2.5 rounded-full font-semibold text-white text-sm transition-colors">اضف عنوان</button>
            </div>
            <div class="gap-6 grid md:grid-cols-2">{cards}</div>"""

    return account_page("عناويني | أبو عوف", "إدارة عناوين التوصيل الخاصة بك.",
                        content, "my-account-addresses", "/my-account/addresses",
                        "عناويني", "my-account-addresses.html")
