"""Loyalty points — Figma 'Redeem Points' (4695:29916)."""
from _account import CUSTOMER, account_page, card

SLUG = "my-account-point.html"


def build():
    content = f"""
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">نقاطي</h1>
            <div class="flex flex-col items-center gap-2 bg-accent-yellow p-8 rounded-[20px] text-center">
              <span class="text-[#062A1C]/70 text-sm">رصيد النقاط</span>
              <span class="font-bold text-[#062A1C] text-4xl latin">{CUSTOMER['points']}</span>
              <span class="text-[#062A1C] text-sm">يمكنك خصم <span class="latin">EGP 12</span> من طلبك القادم</span>
              <button type="button" class="bg-cta hover:bg-cta-hover mt-2 px-8 py-3 rounded-full font-semibold text-white text-sm transition-colors">استبدال النقاط</button>
            </div>
            {card("إزاي تكسب نقاط؟", '''<ul class="flex flex-col gap-2 ps-5 text-neutral-800 text-sm leading-7 list-disc">
              <li>اكسب نقطة على كل جنيه تشتريه من الموقع</li>
              <li>نقاط إضافية عند تقييم المنتجات اللي اشتريتها</li>
              <li>مكافأة ترحيبية عند إنشاء حساب جديد</li>
            </ul>''')}"""
    return account_page("نقاطي | أبو عوف", "رصيد نقاطك وطرق استبدالها.",
                        content, "my-account-point", "/my-account/points",
                        "نقاطي", "my-account-point.html")
