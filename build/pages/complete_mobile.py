"""Mobile-number capture for a Google account that has none (Ahmed, 2026-09-23).

Google hands back a verified email, a name and a picture — never a phone. Abu
Auf's whole account model is keyed on the mobile: the OTP IS the sign-in
(see login.py), orders are tracked against it, and the courier calls it. So a
Google sign-in that lands with no mobile on file cannot complete, and is routed
here instead of straight into the dashboard.

The flow: login/register Google button -> Auth.startGoogle() -> this page ->
verify.html (the SAME shared OTP step every other sign-in uses) -> dashboard.
A Google account that DOES already carry a mobile skips this page entirely;
`initGoogleAuth()` in scripts.js makes that call, not this module.

Arriving here with no pending Google flow bounces to /login, the same guard
verify.py relies on.
"""
from _auth import auth_page
from catalog import e
from components import phone_field

SLUG = "complete-mobile.html"

ICON_SHIELD = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" class="w-full h-full">'
               '<path d="M12 3 5 6v5.5c0 4.2 2.9 8.1 7 9.5 4.1-1.4 7-5.3 7-9.5V6l-7-3Z" '
               'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
               '<path d="m9.2 12.2 2 2 3.6-3.9" stroke="currentColor" stroke-width="1.7" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_TRUCK = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" class="w-full h-full">'
              '<path d="M3 7h10v9H3V7Zm10 3h4l3 3v3h-7v-6Z" stroke="currentColor" '
              'stroke-width="1.7" stroke-linejoin="round"/>'
              '<circle cx="7" cy="18" r="1.8" stroke="currentColor" stroke-width="1.7"/>'
              '<circle cx="17" cy="18" r="1.8" stroke="currentColor" stroke-width="1.7"/></svg>')
ICON_CHAT = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" class="w-full h-full">'
             '<path d="M21 12a8 8 0 0 1-8 8H4l2-3.2A8 8 0 1 1 21 12Z" stroke="currentColor" '
             'stroke-width="1.7" stroke-linejoin="round"/></svg>')

WHY = [
    (ICON_SHIELD, "رقم الموبايل هو وسيلة تسجيل دخولك — بنبعتلك رمز تحقق عليه في كل مرة."),
    (ICON_TRUCK, "مندوب التوصيل بيتواصل معاك على الرقم ده لتأكيد موعد وصول الطلب."),
    (ICON_CHAT, "هتوصلك إشعارات حالة الطلب ونقاط محفظتك على نفس الرقم."),
]


def _why_list():
    rows = "".join(
        f"""
                  <li class="flex items-start gap-3">
                    <span class="place-items-center grid bg-white rounded-full text-cta size-8 shrink-0 p-1.5">{icon}</span>
                    <span class="text-neutral-800 text-sm leading-6">{e(text)}</span>
                  </li>"""
        for icon, text in WHY
    )
    return f"""
                <ul class="flex flex-col gap-3.5" role="list">{rows}
                </ul>"""


def build():
    # The Google identity strip. It ships with placeholder glyphs and is
    # painted from the pending record at runtime ([data-google-name] /
    # [data-google-email] / [data-google-initial]) — never baked in, the same
    # rule the checkout address chooser follows. data-i18n-skip because the
    # name and email belong to the SHOPPER: the i18n walk is keyed on exact
    # Arabic strings and would happily rewrite a person's name.
    identity = """
              <div data-i18n-skip class="flex items-center gap-3 bg-interaction-base p-3 rounded-2xl">
                <span data-google-initial aria-hidden="true"
                      class="place-items-center grid bg-cta rounded-full font-bold text-white text-lg size-11 shrink-0">—</span>
                <span class="flex flex-col min-w-0">
                  <span data-google-name class="font-semibold text-[#062A1C] text-sm truncate">—</span>
                  <span data-google-email class="text-neutral-secondary text-xs truncate latin" dir="ltr">—</span>
                </span>
              </div>"""

    form = f"""
              <p class="text-neutral-secondary text-sm text-center leading-7">
                تم تسجيل دخولك بحساب جوجل بنجاح. فاضل خطوة واحدة — ضيف رقم موبايلك
                عشان نقدر نأمّن حسابك ونوصّلك طلباتك.
              </p>
{identity}
{phone_field("رقم الموبايل", "mobile", required=True, country_select=True,
             error_id="mobile-error",
             help_text="هنبعتلك كود تأكيد من 6 أرقام على الرقم ده.")}
{_why_list()}
              <button type="submit" data-mobile-submit
                      class="btn-elevate bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">متابعة</button>
              <p class="text-neutral-secondary text-xs text-center leading-6">
                باستكمال التسجيل أنت موافق على
                <a href="terms-conditions.html" class="font-semibold text-cta underline">الشروط والأحكام</a>.
              </p>
              <!-- py-3 is not decoration: the label alone is a 20px-tall
                   STANDALONE target, under the 24px WCAG 2.2 AA floor (2.5.8).
                   The inline "الشروط والأحكام" link above needs no such
                   padding — it sits in a sentence, which 2.5.8 exempts. -->
              <button type="button" data-google-cancel
                      class="link-sweep self-center px-3 py-3 font-semibold text-neutral-secondary text-sm">تسجيل الدخول بحساب آخر</button>"""

    # Same convention as verify.py: the 3D icon sits bare above the heading,
    # no tinted disc behind it. profile-3d because this step is the account
    # setup finishing, not an OTP — the OTP icon belongs to the next page.
    hero = '<img src="images/abuauf/icons/profile-3d.png" alt="" class="w-20 h-20 object-contain" />'
    return auth_page("أضف رقم موبايلك | أبو عوف",
                     "أضف رقم موبايلك لإكمال تسجيل الدخول بحساب جوجل في أبو عوف.",
                     "أضف رقم موبايلك", form, "complete-mobile", "/complete-mobile",
                     "إضافة رقم الموبايل", side=False, social=False,
                     # `novalidate` with `required` still ON the input: the
                     # attribute keeps the semantics for assistive tech and
                     # for a JS-less fallback, while novalidate hands the
                     # empty-field case to the page's own inline message.
                     # Without it the browser swallows the submit event and
                     # paints a native bubble instead — an untranslated,
                     # untinted tooltip that vanishes on the next click,
                     # inside an Arabic RTL form.
                     form_attrs="data-google-mobile-form novalidate", hero=hero)
