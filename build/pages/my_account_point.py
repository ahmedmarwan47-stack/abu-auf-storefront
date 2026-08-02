"""Loyalty points — Figma 'Redeem Points' (4695:29916)."""
from _account import CUSTOMER, account_page, card

SLUG = "my-account-point.html"


def build():
    content = f"""
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">نقاطي</h1>
            <!-- The redeem button was dead — no handler anywhere (it was never
                 wired the way the addresses page was). scripts.js initPoints now
                 redeems client-side: it zeroes the balance and shows the done
                 state, persisted under abuauf:pointsRedeemed. Placeholder, since
                 points have no live endpoint (DESIGN-NOTES §1). -->
            <div data-points class="flex flex-col items-center gap-2 bg-accent-yellow p-8 rounded-[20px] text-center">
              <span class="text-[#062A1C]/70 text-sm">رصيد النقاط</span>
              <span class="font-bold text-[#062A1C] text-4xl latin" data-points-balance>{CUSTOMER['points']}</span>
              <span class="text-[#062A1C] text-sm" data-points-hint>حوّل نقاطك إلى <span class="latin">EGP 12</span> في رصيد محفظتك</span>
              <button type="button" data-redeem-points class="bg-cta hover:bg-cta-hover mt-2 px-8 py-3 rounded-full font-semibold text-white text-sm transition-colors">استبدال النقاط</button>
              <div data-points-done hidden class="flex flex-col items-center gap-1 mt-2">
                <span class="flex items-center gap-2 font-bold text-[#062A1C]">
                  <span class="place-items-center grid bg-primary rounded-full text-white size-6 text-xs">✓</span>
                  تم تحويل نقاطك إلى المحفظة
                </span>
                <span class="text-[#062A1C]/80 text-sm">تمت إضافة <span class="latin">EGP 12</span> إلى رصيد محفظتك</span>
              </div>
            </div>
            {card("إزاي تكسب نقاط؟", '''<ul class="flex flex-col gap-2 ps-5 text-neutral-800 text-sm leading-7 list-disc">
              <li>اكسب نقطة على كل جنيه تشتريه من الموقع</li>
              <li>نقاط إضافية عند تقييم المنتجات اللي اشتريتها</li>
              <li>مكافأة ترحيبية عند إنشاء حساب جديد</li>
            </ul>''')}"""
    return account_page("نقاطي | أبو عوف", "رصيد نقاطك وطرق استبدالها.",
                        content, "my-account-point", "/my-account/points",
                        "نقاطي", "my-account-point.html")
