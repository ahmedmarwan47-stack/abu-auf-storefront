"""Profile — Figma 'Account > Profile' (312:14548)."""
from _account import CUSTOMER, account_page, card
from components import field

SLUG = "my-account-profile.html"


def build():
    form = f"""
              <form class="flex flex-col gap-5">
                <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", value="محمد", required=True)}
{field("الاسم الاخير", "last-name", value="عادل", required=True)}
                </div>
{field("البريد الالكتروني", "email", "email", value=CUSTOMER['email'], required=True)}
{field("رقم الهاتف", "phone", "tel", value=CUSTOMER['phone'], required=True)}
                <button type="submit" class="bg-cta hover:bg-cta-hover py-3.5 rounded-full font-semibold text-white text-sm transition-colors self-start px-10">حفظ التعديلات</button>
              </form>"""

    pwd = """
              <form class="flex flex-col gap-5">
                <p class="text-neutral-secondary text-sm">لتغيير كلمة المرور، أدخل كلمة المرور الحالية ثم الجديدة.</p>
                <a href="reset-password.html" class="px-10 py-3.5 border border-cta rounded-full font-semibold text-cta text-sm text-center hover:bg-interaction-base transition-colors self-start">تغيير كلمة المرور</a>
              </form>"""

    content = f"""
            <h1 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">بيانات الحساب</h1>
            {card("المعلومات الشخصية", form)}
            {card("كلمة المرور", pwd)}"""

    return account_page("بيانات الحساب | أبو عوف", "عدّل بياناتك الشخصية وكلمة المرور.",
                        content, "my-account-profile", "/my-account/profile",
                        "بيانات الحساب", "my-account-profile.html")
