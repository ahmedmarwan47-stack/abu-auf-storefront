"""Sign in — Figma 'Account Sign In/ Create Account' (205:10427)."""
from _auth import auth_page, password_field
from components import field

SLUG = "login.html"


def build():
    form = f"""
{field("البريد الالكتروني", "email", "email", required=True)}
{password_field()}
              <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">تسجيل الدخول</button>
              <a href="forget-password.html" class="font-semibold text-cta text-sm text-center underline">نسيت كلمة المرور الخاصة بي</a>"""
    return auth_page("تسجيل الدخول | أبو عوف",
                     "سجل الدخول إلى حسابك في أبو عوف لمتابعة طلباتك ونقاط محفظتك.",
                     "تسجيل الدخول", form, "login", "/login", "تسجيل الدخول")
