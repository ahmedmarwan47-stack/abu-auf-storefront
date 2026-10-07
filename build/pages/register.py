"""Create account — passwordless (mobile + OTP). Figma 'Create Account' (206:9768).

Ahmed, 2026-08-04: registration collects the name, mobile and email — no
password. Submitting hands off to the shared OTP page (verify.html) to verify
the MOBILE; once verified the account is created and signed in. The email is
NOT verified here — that is deferred to a prompt on the dashboard, since it is
not required to start ordering.

Ahmed, 2026-10-07: the shopper now chooses WHERE the code goes — WhatsApp (to
the mobile) or email. The choice rides on the pending record as `channel`, and
verify.html paints its heading and "sent to" line from it. Choosing email
verifies the email at the same step, so the dashboard's email prompt does not
fire for that account; the mobile is then unproven (DESIGN-NOTES §3).
"""
from _auth import ICON_MAIL, auth_page
from components import field, phone_field, radio_card

# WhatsApp brand glyph, brand-coloured like the Google/Facebook marks on the
# same card. Wrapper-sized (w-5 h-5) to match ICON_MAIL beside it.
ICON_WHATSAPP = ('<svg viewBox="0 0 24 24" fill="#25D366" class="w-5 h-5"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 '
                 '1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.2c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm5.8 '
                 '14.03c-.24.68-1.42 1.3-1.95 1.35-.5.05-.97.23-3.27-.68-2.77-1.09-4.52-3.92-4.66-4.1-.13-.18-1.1-1.47-1.1-2.8 '
                 '0-1.34.7-2 .95-2.27.25-.27.54-.34.72-.34h.52c.17 0 .4-.06.62.47.24.56.8 1.94.87 2.08.07.14.12.3.02.48-.09.18-.14.3-.27'
                 '.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.28.14.44.11.6-.07.16-.18'
                 '.69-.8.88-1.08.18-.27.37-.23.62-.14.25.09 1.6.75 1.87.89.28.14.46.2.53.32.07.11.07.66-.17 1.34Z"/></svg>')

SLUG = "register.html"


def build():
    form = f"""
              <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", required=True)}
{field("الاسم الاخير", "last-name", required=True)}
              </div>
{phone_field("رقم الموبايل", "phone")}
{field("البريد الالكتروني", "email", "email", required=True)}
              <!-- Where the OTP goes. Real radios (radio_card), so the checked
                   state IS the submitted value — scripts.js reads
                   [name="otp-channel"]:checked and nothing else. -->
              <fieldset class="flex flex-col gap-1.5">
                <legend class="mb-1.5 font-medium text-neutral-secondary text-sm">استلام رمز التحقق عن طريق</legend>
                <div class="flex sm:flex-row flex-col gap-3">
{radio_card("otp-channel", "whatsapp", "واتساب", "على رقم الموبايل", ICON_WHATSAPP, checked=True)}
{radio_card("otp-channel", "email", "البريد الالكتروني", "على الإيميل", ICON_MAIL)}
                </div>
              </fieldset>
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
                     "أنشئ حساب في أبو عوف برقم موبايلك واكسب نقاط في محفظتك مع كل طلب.",
                     "إنشاء حساب جديد", form, "register", "/register",
                     "إنشاء حساب", side=False, form_attrs="data-register-form")
