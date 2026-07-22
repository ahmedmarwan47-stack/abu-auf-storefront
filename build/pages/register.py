"""Create account — Figma 'Create Account' (206:9768)."""
from _auth import auth_page, password_field
from components import field

SLUG = "register.html"


def build():
    form = f"""
              <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", required=True)}
{field("الاسم الاخير", "last-name", required=True)}
              </div>
{field("البريد الالكتروني", "email", "email", required=True)}
{field("رقم الهاتف", "phone", "tel", required=True)}
{password_field(autocomplete="new-password")}
{password_field("تأكيد كلمة السر", "password-confirm", autocomplete="new-password")}
              <label class="flex items-start gap-2 cursor-pointer">
                <input type="checkbox" required class="mt-1 accent-[#163300] w-4 h-4" />
                <span class="text-neutral-secondary text-sm leading-6">
                  أوافق على <a href="terms-conditions.html" class="font-semibold text-cta underline">الشروط والأحكام</a>
                </span>
              </label>
              <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">إنشاء حساب</button>
              <p class="text-neutral-secondary text-sm text-center">
                لديك حساب بالفعل؟ <a href="login.html" class="font-semibold text-cta underline">تسجيل الدخول</a>
              </p>"""
    return auth_page("إنشاء حساب | أبو عوف",
                     "أنشئ حساب في أبو عوف واكسب نقاط في محفظتك مع كل طلب.",
                     "إنشاء حساب جديد", form, "register", "/register",
                     "إنشاء حساب", side=False)
