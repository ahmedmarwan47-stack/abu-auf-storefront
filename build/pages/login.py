"""Sign in — Figma 'Account Sign In/ Create Account' (205:10427)."""
from _auth import auth_page, password_field
from components import field

SLUG = "login.html"

# Kept in step with DEMO_USER in static-export/scripts.js. Printed on the page
# on purpose: this is a static export with no backend, and the credentials are
# hard-coded in client-side JS anyway, so there is nothing to protect. It
# exists so the signed-in chrome and the favourites flow can be walked end to
# end. Both must go with the demo auth before launch — see DESIGN-NOTES.
DEMO_EMAIL = "demo@abuauf.com"
DEMO_PASSWORD = "AbuAuf2026"

DEMO_CALLOUT = f"""
              <div class="flex flex-col gap-2 bg-interaction-base p-4 border border-neutral-divider rounded-xl">
                <p class="font-bold text-[#062A1C] text-sm">حساب تجريبي للاختبار</p>
                <p class="text-neutral-secondary text-xs leading-5">استخدم البيانات دي لتجربة تسجيل الدخول والمفضلة:</p>
                <dl class="flex flex-col gap-1 text-sm">
                  <div class="flex items-center gap-2">
                    <dt class="text-neutral-secondary">Email</dt>
                    <dd class="font-semibold text-[#062A1C] latin">{DEMO_EMAIL}</dd>
                  </div>
                  <div class="flex items-center gap-2">
                    <dt class="text-neutral-secondary">Password</dt>
                    <dd class="font-semibold text-[#062A1C] latin">{DEMO_PASSWORD}</dd>
                  </div>
                </dl>
                <button type="button" data-demo-fill
                        class="btn-elevate self-start bg-white hover:bg-interaction-tertiary-hover mt-1 px-4 border border-cta rounded-full min-h-11 font-semibold text-cta text-sm">املأ البيانات تلقائياً</button>
              </div>"""


def build():
    form = f"""{DEMO_CALLOUT}
{field("البريد الالكتروني", "email", "email", required=True)}
{password_field()}
              <button type="submit" class="btn-elevate bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base">تسجيل الدخول</button>
              <a href="forget-password.html" class="link-sweep self-center font-semibold text-cta text-sm">نسيت كلمة المرور الخاصة بي</a>"""
    return auth_page("تسجيل الدخول | أبو عوف",
                     "سجل الدخول إلى حسابك في أبو عوف لمتابعة طلباتك ونقاط محفظتك.",
                     "تسجيل الدخول", form, "login", "/login", "تسجيل الدخول",
                     form_attrs="data-login-form")
