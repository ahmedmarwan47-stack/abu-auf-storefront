"""
Shared account-area shell — Figma 'Account > Overview' (312:13041).

All eight my-account pages are this sidebar plus a content column, so the
sidebar, membership badge and help links are defined once here.
"""
from catalog import e
from components import page, page_header

CUSTOMER = {"name": "محمد", "full": "محمد عادل",
            "email": "mosawabi15@gmail.com", "phone": "0109809839",
            "tier": "عضوية ذهبية", "wallet": 1200, "points": 120}

I = {
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V10Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "orders": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6ZM3 6h18M16 10a4 4 0 0 1-8 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    "heart": '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.7"/>',
    "wallet": '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z" stroke="currentColor" stroke-width="1.7"/><path d="M16 12h3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "user": '<circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.7"/><path d="M4 21a8 8 0 0 1 16 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "out": '<path d="M15 17l5-5-5-5M20 12H9M12 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    # Chevron points to the inline end (left in RTL), matching the Figma rows.
    "chev": '<path d="m15 6-6 6 6 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
}

NAV = [
    ("الرئيسية", "my-account.html", "home"),
    ("طلباتي", "my-account-orders.html", "orders"),
    ("المفضلة", "my-account-favorites.html", "heart"),
    ("عناويني", "my-account-addresses.html", "pin"),
    ("محفظتي", "my-account-wallet.html", "wallet"),
    ("نقاطي", "my-account-point.html", "star"),
    ("بيانات الحساب", "my-account-profile.html", "user"),
]


def _icon(key, cls="w-5 h-5"):
    return f'<svg viewBox="0 0 24 24" fill="none" class="{cls}">{I[key]}</svg>'


def sidebar(active_slug):
    items = "".join(f"""
              <a href="{href}" class="flex items-center gap-3 px-4 py-3 rounded-xl font-semibold text-base transition-colors {'bg-interaction-base text-[#062A1C]' if href == active_slug else 'text-neutral-800 hover:bg-interaction-base'}">
                <span class="text-cta">{_icon(icon)}</span>{e(label)}
              </a>""" for label, href, icon in NAV)

    return f"""
          <aside class="hidden lg:flex flex-col gap-1 bg-white shadow-custom4 p-5 rounded-[20px] lg:sticky lg:top-4 min-w-0 h-max">
            <span class="bg-accent-yellow px-3 py-1 rounded-full font-semibold text-[#062A1C] text-xs self-start">{e(CUSTOMER['tier'])}</span>
            <h2 class="mt-2 mb-3 font-bold text-[#062A1C] text-xl">مرحبا {e(CUSTOMER['name'])}</h2>
            {items}
            <div class="flex flex-col gap-2 mt-4 pt-4 border-neutral-divider border-t">
              <span class="font-semibold text-neutral-secondary text-sm">تحتاج مساعدة؟</span>
              <a href="faqs.html" class="link-sweep self-start font-semibold text-cta text-sm">الأسئلة المتداولة</a>
              <a href="contact-us.html" class="link-sweep self-start font-semibold text-cta text-sm">تواصل معنا</a>
              <!-- Only meaningful while the demo session is active, so it is
                   hidden for signed-out visitors by [data-authed-only]. -->
              <button type="button" data-logout data-authed-only hidden
                      class="flex items-center gap-2 mt-2 font-semibold text-accent-error text-sm text-start min-h-11">تسجيل الخروج</button>
            </div>
            <a href="index.html" class="flex justify-center items-center gap-2 mt-4 py-3 border border-neutral-divider hover:border-cta rounded-full font-semibold text-[#062A1C] text-sm transition-colors">
              {_icon('out', 'w-4 h-4')} تسجيل الخروج
            </a>
          </aside>"""


def _active_label(active_slug):
    for label, href, _icon_key in NAV:
        if href == active_slug:
            return label
    return NAV[0][0]


def mobile_nav(active_slug):
    """Figma 'Account > menu bottom sheet' (973:47270).

    A 300px sidebar has nowhere to go on a 375px screen, so below `lg` it
    collapses to a selector row that opens a sheet. Both the sidebar and this
    sheet render from NAV, so a new account page appears in both or neither.
    """
    rows = "".join(f"""
              <a href="{href}" class="flex items-center gap-3 px-1 py-4 border-neutral-divider border-b font-semibold text-base {'text-cta' if href == active_slug else 'text-[#062A1C]'}">
                <span class="text-cta shrink-0">{_icon(icon)}</span>
                <span class="flex-1 min-w-0 truncate">{e(label)}</span>
                <span class="text-neutral-secondary shrink-0">{_icon('chev', 'w-4 h-4')}</span>
              </a>""" for label, href, icon in NAV)

    return f"""
          <div class="lg:hidden flex flex-col gap-3 min-w-0">
            <span class="bg-accent-yellow px-3 py-1 rounded-full font-semibold text-[#062A1C] text-xs self-start">{e(CUSTOMER['tier'])}</span>
            <h2 class="font-bold text-[#062A1C] text-xl">مرحبا {e(CUSTOMER['name'])}</h2>
            <button type="button" data-open="accountMenu" class="flex justify-between items-center gap-3 bg-white px-5 py-3.5 border border-neutral-divider rounded-full w-full font-semibold text-[#062A1C] text-base">
              <span class="flex items-center gap-3 min-w-0">
                <span class="text-cta shrink-0">{_icon('menu')}</span>
                <span class="truncate">{e(_active_label(active_slug))}</span>
              </span>
              <span class="-rotate-90 text-neutral-secondary shrink-0">{_icon('chev', 'w-4 h-4')}</span>
            </button>
          </div>

          <div data-sheet="account-menu" class="lg:hidden bottom-sheet">
            <div class="bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
            <div class="flex justify-between items-center mb-2">
              <h2 class="font-bold text-[#062A1C] text-lg">القائمة</h2>
              <button type="button" data-close class="place-items-center grid hover:bg-interaction-base border border-neutral-divider rounded-full w-8 h-8 text-[#062A1C]" aria-label="إغلاق">{_icon('close', 'w-4 h-4')}</button>
            </div>
            <nav class="flex flex-col">{rows}
            </nav>
            <button type="button" data-close class="bg-cta hover:bg-cta-hover mt-4 py-3 rounded-full w-full font-semibold text-white transition-colors">تأكيد</button>
          </div>"""


def account_page(title_text, description, content, page_id, path,
                 crumb, active_slug):
    body = f"""{page_header("", [("الرئيسية", "index.html"), ("حسابي", "my-account.html"), (crumb, None)])}

      <section class="py-6 xl:py-8">
        <div class="items-start gap-6 xl:gap-8 grid grid-cols-1 lg:grid-cols-[300px_1fr] mx-auto px-4 max-w-[1536px]">
{mobile_nav(active_slug)}
{sidebar(active_slug)}
          <div class="flex flex-col gap-6 min-w-0">{content}
          </div>
        </div>
      </section>"""
    return page(title_text, description, body, page_id, path)


def card(heading, inner, cta=None, cta_href="#"):
    action = (f'<a href="{cta_href}" class="hover:bg-interaction-base px-5 py-2 border '
              f'border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs '
              f'transition-colors">{e(cta)}</a>') if cta else ""
    # h2, not h3: these cards are the account page's top-level sections and
    # the only heading above them is the page h1, so h3 skipped a level and
    # broke heading-by-heading navigation on all seven account pages.
    head = (f'<div class="flex justify-between items-center gap-3">'
            f'<h2 class="font-bold text-[#062A1C] text-base">{e(heading)}</h2>{action}</div>'
            ) if heading else ""
    return (f'<div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">'
            f'{head}{inner}</div>')


ORDERS = [
    ("#30941", "28 مارس 2026", "تحت التحضير", "amber", 490.0),
    ("#30942", "21 مارس 2026", "ملغي", "red", 490.0),
    ("#30943", "14 مارس 2026", "مكتمل", "green", 490.0),
]

STATUS_STYLE = {
    "amber": "bg-accent-yellow text-[#062A1C]",
    "red": "bg-accent-error text-white",
    "green": "bg-primary text-white",
}
