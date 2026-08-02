"""
Shared account-area shell — Figma 'Account > Overview' (312:13041).

All eight my-account pages are this sidebar plus a content column, so the
sidebar, membership badge and help links are defined once here.
"""
from catalog import e, in_category, money, title as _ptitle
from components import WALLET_BALANCE, page, page_header

# `wallet` comes from components.WALLET_BALANCE rather than a second literal:
# the cart/checkout wallet toggle offers to spend this exact balance, so if the
# two drifted the shopper would be offered money this page says they do not
# have. Same failure the old points banner shipped with — 100 on one page, 120
# on the other.
CUSTOMER = {"name": "محمد", "full": "محمد عادل",
            "email": "mosawabi15@gmail.com", "phone": "0109809839",
            "tier": "عضوية ذهبية", "wallet": WALLET_BALANCE, "points": 120}

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


DELIVERY_FEE = 30.0


def _oitems(cat, qtys):
    prods = in_category(cat, len(qtys))
    return [(p, q) for p, q in zip(prods, qtys)]


# Orders carry their own line items now (Ahmed, 2026-08-02) so the detail drawer
# can list them and the dashboard can offer a real re-order. Still placeholder —
# there is no orders endpoint (DESIGN-NOTES) — but each order's total is derived
# from its items + delivery, so the list row and the drawer agree instead of the
# decoupled 490 the old tuple carried. `step` is how far the tracker has advanced
# (0..3); a cancelled order shows no tracker.
ORDERS = [
    {"no": "#30941", "date": "28 مارس 2026", "status": "تحت التحضير",
     "tone": "amber", "step": 1, "items": _oitems("Dates & Dried Fruits", [1, 2])},
    {"no": "#30942", "date": "21 مارس 2026", "status": "ملغي",
     "tone": "red", "step": 0, "items": _oitems("Nuts | Seeds & Crackers", [2, 1])},
    {"no": "#30943", "date": "14 مارس 2026", "status": "مكتمل",
     "tone": "green", "step": 3, "items": _oitems("Snacks", [1, 1, 1])},
]

STATUS_STYLE = {
    "amber": "bg-accent-yellow text-[#062A1C]",
    "red": "bg-accent-error text-white",
    "green": "bg-primary text-white",
}

_ORDER_STEPS = ["تم الطلب", "جاري التحضير", "في الطريق إليك", "تم التسليم"]
_OCHECK = ('<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="m5 13 4 4L19 7" '
           'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def order_total(o):
    return sum(p["price"] * q for p, q in o["items"]) + DELIVERY_FEE


def _order_tracker(step):
    cells = ""
    for i, label in enumerate(_ORDER_STEPS):
        done = i <= step
        cells += f"""
                <li class="flex flex-col flex-1 items-center gap-1.5 text-center">
                  <span class="place-items-center grid rounded-full size-7 {'bg-primary text-white' if done else 'bg-interaction-base text-neutral-secondary'}">
                    {_OCHECK if done else f'<span class="font-semibold text-xs latin">{i + 1}</span>'}
                  </span>
                  <span class="text-[#062A1C] text-[11px] leading-4">{e(label)}</span>
                </li>"""
    return f'<ol class="flex gap-1">{cells}\n              </ol>'


def _order_lines(o):
    return "".join(f"""
                <div class="flex items-center gap-3 py-3 border-neutral-divider border-b last:border-0">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-14 h-14 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 min-w-0">
                    <span class="font-semibold text-[#062A1C] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                    <span class="text-neutral-secondary text-xs">عدد <span class="latin">{q}</span></span>
                  </div>
                  <span class="font-bold text-[#062A1C] text-sm latin shrink-0">EGP {money(p['price'] * q)}</span>
                </div>""" for p, q in o["items"])


def order_panel(o):
    """One order's full detail, rendered hidden inside the shared drawer and
    revealed by its id when a row is clicked (the favourites 'ship-all, reveal
    one' pattern) — so a shopper can open several orders in turn without leaving
    the list."""
    subtotal = order_total(o) - DELIVERY_FEE
    tracker = "" if o["tone"] == "red" else f'<div class="pb-1">{_order_tracker(o["step"])}</div>'
    return f"""
              <div data-order-panel data-order-id="{e(o['no'])}" hidden class="flex flex-col gap-4">
                <div class="flex flex-wrap justify-between items-center gap-2">
                  <h3 class="font-bold text-[#062A1C] text-base">طلب رقم <span class="latin">{e(o['no'])}</span></h3>
                  <span class="inline-flex px-3 py-1 rounded-full font-semibold text-xs {STATUS_STYLE[o['tone']]}">{e(o['status'])}</span>
                </div>
                {tracker}
                <div class="flex flex-col">{_order_lines(o)}
                </div>
                <div class="flex flex-col gap-2 pt-3 border-neutral-divider border-t text-sm">
                  <div class="flex justify-between"><span class="text-neutral-secondary">الإجمالي الفرعي</span><span class="font-semibold text-[#062A1C] latin">EGP {money(subtotal)}</span></div>
                  <div class="flex justify-between"><span class="text-neutral-secondary">مصاريف التوصيل</span><span class="font-semibold text-[#062A1C] latin">EGP {money(DELIVERY_FEE)}</span></div>
                  <div class="flex justify-between items-center pt-2 border-neutral-divider border-t"><span class="font-bold text-[#062A1C]">الإجمالي</span><span class="font-bold text-[#062A1C] text-lg latin">EGP {money(order_total(o))}</span></div>
                </div>
                <div class="flex flex-col gap-1 bg-interaction-base p-3 rounded-xl text-neutral-secondary text-sm">
                  <span class="font-semibold text-[#062A1C]">عنوان التوصيل</span>
                  <span>شقة 3 - 220 شارع الحرية - الدور الأول</span>
                  <span>مصر الجديدة، القاهرة</span>
                </div>
              </div>"""


def order_drawer(orders):
    """Shared side-drawer holding every order's panel, opened by initOrders in
    scripts.js. Appended to the orders list and the dashboard."""
    panels = "".join(order_panel(o) for o in orders)
    # --left so it opens from the RIGHT in RTL — the OPPOSITE side to the cart
    # drawer (which is --right / left in RTL), at Ahmed's request. Its width is
    # widened past the 340px --left default in styles.css.
    return f"""
    <aside data-drawer="order" class="side-drawer side-drawer--left" aria-label="تفاصيل الطلب">
      <button type="button" data-close aria-label="إغلاق" class="drawer-close place-items-center grid bg-white shadow-custom3 rounded-full size-8 text-[#062A1C]">{_icon('close', 'w-3.5 h-3.5')}</button>
      <div class="flex justify-between items-center px-5 py-4 border-neutral-divider border-b">
        <h2 class="font-bold text-[#062A1C] text-lg">تفاصيل الطلب</h2>
      </div>
      <div class="flex-1 px-5 py-4 overflow-y-auto" data-order-panels>{panels}
      </div>
    </aside>"""


def order_rows(orders):
    """The orders table body — the WHOLE row is the target now (Ahmed,
    2026-08-02), opening the detail drawer, not a bordered 'view' button. A
    chevron is the affordance; role/tabindex + the keydown handler in scripts.js
    keep it keyboard-operable."""
    return "".join(f"""
                  <tr data-order-open="{e(o['no'])}" tabindex="0" role="button" aria-label="عرض تفاصيل الطلب {e(o['no'])}" class="group border-neutral-divider border-b last:border-0 cursor-pointer hover:bg-interaction-base focus-visible:bg-interaction-base transition-colors">
                    <td class="py-4 ps-2 font-semibold text-[#062A1C] text-sm latin">{e(o['no'])}</td>
                    <td class="py-4 text-neutral-secondary text-sm">{e(o['date'])}</td>
                    <td class="py-4"><span class="inline-flex px-3 py-1 rounded-full font-semibold text-xs {STATUS_STYLE[o['tone']]}">{e(o['status'])}</span></td>
                    <td class="py-4 font-semibold text-[#062A1C] text-sm latin">EGP {money(order_total(o))}</td>
                    <td class="py-4 pe-2 text-end"><span class="inline-flex justify-center items-center text-neutral-secondary group-hover:text-cta transition-colors size-8">{_icon('chev', 'w-4 h-4')}</span></td>
                  </tr>""" for o in orders)


def order_tracking_card(o):
    """Dashboard 'current order' widget — status + live tracker + a button that
    opens the same detail drawer."""
    return f"""
            <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              <div class="flex flex-wrap justify-between items-center gap-2">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-[#062A1C] text-base">تتبع طلبك الحالي</span>
                  <span class="font-semibold text-neutral-secondary text-sm latin">{e(o['no'])}</span>
                </div>
                <span class="inline-flex px-3 py-1 rounded-full font-semibold text-xs {STATUS_STYLE[o['tone']]}">{e(o['status'])}</span>
              </div>
              {_order_tracker(o['step'])}
              <button type="button" data-order-open="{e(o['no'])}" class="self-start bg-cta hover:bg-cta-hover px-6 py-2.5 rounded-full font-semibold text-white text-sm transition-colors">تفاصيل الطلب</button>
            </div>"""


def reorder_card(o):
    """Dashboard 'last order' widget with a real re-order button — the hidden
    [data-reorder-item] payloads let scripts.js add the whole order back to the
    cart in one press."""
    items_data = "".join(
        f'<span data-reorder-item data-id="{e(p.get("id", 0))}" data-name="{e(_ptitle(p))}" '
        f'data-price="{p["price"]}" data-image="{e(p["image"])}" data-qty="{q}" hidden></span>'
        for p, q in o["items"]
    )
    thumbs = "".join(
        f'<img src="{e(p["image"])}" alt="" class="bg-interaction-base p-1 rounded-lg w-12 h-12 object-contain shrink-0" loading="lazy" />'
        for p, q in o["items"][:4]
    )
    return f"""
            <div data-reorder-card class="flex flex-wrap justify-between items-center gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              {items_data}
              <div class="flex items-center gap-3 min-w-0">
                <div class="flex gap-1 shrink-0">{thumbs}
                </div>
                <div class="flex flex-col min-w-0">
                  <span class="font-bold text-[#062A1C] text-sm">آخر طلب <span class="latin">{e(o['no'])}</span></span>
                  <span class="text-neutral-secondary text-xs">{e(o['date'])} · <span class="latin">EGP {money(order_total(o))}</span></span>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button type="button" data-order-open="{e(o['no'])}" class="hover:bg-interaction-base px-4 py-2 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">التفاصيل</button>
                <button type="button" data-reorder class="bg-cta hover:bg-cta-hover px-5 py-2 rounded-full font-semibold text-white text-xs transition-colors">إعادة الطلب</button>
              </div>
            </div>"""
