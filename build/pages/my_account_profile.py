"""Profile — Figma 'Account > Profile' (312:14548).

Rebuilt to the tighter, richer form Ahmed referenced (2026-08-04 screenshot): a
narrow, centred card with an avatar, first/last name, a read-only email, phone,
date of birth and gender, and a full-width save. The account content column is
wide, so the form is CAPPED and centred rather than stretched into 600px-wide
inputs (the "very wide inputs" complaint). The password card is gone — auth is
passwordless now (mobile + OTP), so there is no password to change.
"""
from _account import CUSTOMER, account_page, account_title, card
from components import dob_field, email_readonly, field, gender_field

SLUG = "my-account-profile.html"

def build():
    # Demo DOB — placeholder like the rest of CUSTOMER (no profile endpoint).
    dob_day, dob_month, dob_year = 12, "أبريل", 1996

    form = f"""
              <form class="flex flex-col gap-5">
                <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", value="محمد", required=True)}
{field("الاسم الاخير", "last-name", value="عادل", required=True)}
                </div>

                <!-- Email is read-only here: it is verified separately (the
                     dashboard shows a verify prompt), not edited on this form. -->
{email_readonly(CUSTOMER['email'])}

{field("رقم الهاتف", "phone", "tel", value=CUSTOMER['phone'], required=True)}

{dob_field(dob_day, dob_month, dob_year)}

{gender_field("female")}

                <button type="submit" class="bg-cta hover:bg-cta-hover mt-1 py-3.5 rounded-full w-full font-semibold text-white text-sm transition-colors">حفظ التعديلات</button>
              </form>"""

    content = f"""
            {account_title(SLUG, "بيانات الحساب")}
            <!-- Capped and hugged to the inline START (right in RTL) with
                 me-auto, so the form sits directly under the title rather than
                 floating in the centre of the column (Ahmed, 2026-08-04). The
                 cap keeps the inputs a comfortable width. -->
            <div class="me-auto w-full max-w-[600px]">
              {card("المعلومات الشخصية", form)}
            </div>"""

    return account_page("بيانات الحساب | أبو عوف", "عدّل بياناتك الشخصية.",
                        content, "my-account-profile", "/my-account/profile",
                        "بيانات الحساب", "my-account-profile.html")
