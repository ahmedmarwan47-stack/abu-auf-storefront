"""
Shared UI components for the Abu Auf static build.

THIS IS THE SINGLE SOURCE OF TRUTH for any markup that appears on more than
one page — product cards, category tiles, section headings, buttons, badges.
Edit a component here, run `python3 build/build.py`, and the change lands on
every page that uses it.

Split of responsibilities:
  * Chrome that is injected at runtime — header, footer, cart drawer, search,
    mobile menu — lives in static-export/scripts.js and updates with no
    rebuild at all.
  * Design tokens — colour, type scale, radii, shadows — live in
    static-export/tw-config.js and likewise need no rebuild.
  * Everything else (page content) is composed from the functions below and
    baked into static HTML so pages stay standalone and work from file://.
"""
import html as html_mod
import re

from catalog import e, money, title

# --------------------------------------------------------------------------
# Icons — generic UI glyphs. Brand marks and Figma-authored icons are real
# asset files under images/abuauf/, never hand-drawn here.
# --------------------------------------------------------------------------
ICON = {
    "heart": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z" '
             'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
    "heart_full": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">'
                  '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z"/></svg>',
    "expand": '<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4">'
              '<path d="M9 3H3v6M15 3h6v6M15 21h6v-6M9 21H3v-6" stroke="currentColor" '
              'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"/>'
             '<path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    # Horizontal chevron — carousel arrows, "read more" links. Mirrored in RTL
    # by the caller with rtl:scale-flip / ltr:scale-flip.
    "arrow": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<path d="M15 6 9 12l6 6" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # Vertical chevron — accordions and dropdowns, where direction is not
    # affected by writing direction.
    "chevron": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
               '<path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # --- Product-page trust row and social proof -------------------------
    # Wrapper-driven like everything else in here: no size class on the svg,
    # `currentColor` throughout, so the caller owns colour and scale.
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-full h-full">'
            '<path d="M12 2.6l2.9 5.9 6.5.95-4.7 4.58 1.11 6.47L12 17.44 '
            '6.19 20.5 7.3 14.03 2.6 9.45l6.5-.95L12 2.6Z"/></svg>',
    "flame": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-full h-full">'
             '<path d="M12.9 2.3c.26 2.2-.53 3.63-1.86 4.9-1.3 1.24-2.9 2.4-3.7 4.6a6.9 6.9 0 0 0 '
             '2.03 7.7c-.5-1.5-.3-3.1.86-4.2.9-.86 1.5-1.7 1.8-2.8.9 1 1.5 2 1.7 3.2.2 1.2 0 2.4-.5 3.6a6.9 '
             '6.9 0 0 0 3.6-6.2c-.05-3.6-2.3-5.9-3.94-10.8Z"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h8A1.5 1.5 0 0 1 14 7.5V16H3V7.5Z" '
             'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
             '<path d="M14 10h3.2c.4 0 .8.18 1.1.5l2.2 2.4c.3.3.5.7.5 1.1V16h-7v-6Z" '
             'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
             '<circle cx="7" cy="17.5" r="1.9" stroke="currentColor" stroke-width="1.6"/>'
             '<circle cx="17" cy="17.5" r="1.9" stroke="currentColor" stroke-width="1.6"/></svg>',
    "return": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
              '<path d="M4 5v5h5" stroke="currentColor" stroke-width="1.7" '
              'stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M4.6 10a8 8 0 1 1-.4 5" stroke="currentColor" stroke-width="1.7" '
              'stroke-linecap="round"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M20 4c0 9-5.2 13-11 13a5.6 5.6 0 0 1-5-2.6C6.5 7.6 12.3 4.6 20 4Z" '
            'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
            '<path d="M4 20c1.6-4.6 4.6-7.7 9-9.6" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M13.2 2.5 5 13.4h5.6L9.8 21.5 18 10.6h-5.6l.8-8.1Z" stroke="currentColor" '
            'stroke-width="1.6" stroke-linejoin="round"/></svg>',
    # Stepper glyphs. SVG, not the ASCII −/+ they replace: a text glyph sits
    # on a baseline inside a line box, so grid-centring the box still leaves
    # the mark itself optically off-centre (Ahmed flagged it on the product
    # stepper). A viewBox-centred path has no baseline to drift on.
    "plus": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round"/></svg>',
    "minus": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M5 12h14" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
              '<path d="M12 3.2 5 5.8v5.4c0 4.2 2.9 7.6 7 9.6 4.1-2 7-5.4 7-9.6V5.8L12 3.2Z" '
              'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
              '<path d="m9.2 11.8 2 2 3.6-3.8" stroke="currentColor" stroke-width="1.6" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "store": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M4 9.5V19a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9.5" stroke="currentColor" '
             'stroke-width="1.6" stroke-linejoin="round"/>'
             '<path d="M3.2 6.2 4.6 4h14.8l1.4 2.2a3 3 0 0 1-5.4 2.6 3 3 0 0 1-5.4 0 3 3 0 0 1-5.4 0 '
             '3 3 0 0 1-1.4-2.6Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
             '<path d="M10 20v-4.5h4V20" stroke="currentColor" stroke-width="1.6" '
             'stroke-linejoin="round"/></svg>',
}


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------
def button(label, href="#", variant="primary", size="md", extra=""):
    """variant: primary | secondary | ghost"""
    sizes = {
        "sm": "px-6 py-2.5 text-sm",
        "md": "px-8 py-3 text-base",
        "lg": "px-8 py-4 text-base xl:text-lg",
    }
    variants = {
        "primary": "bg-cta hover:bg-cta-hover text-white",
        "secondary": "border border-cta text-cta hover:bg-interaction-base",
        "accent": "bg-accent-yellow hover:bg-accent-500 text-[#062A1C]",
    }
    return (f'<a href="{href}" class="inline-flex justify-center items-center rounded-full '
            f'font-semibold transition-colors {sizes[size]} {variants[variant]} {extra}">{e(label)}</a>')


def section_heading(heading, cta_label=None, cta_href="#", centered=False):
    """Section title with an optional trailing link — Figma 'Section Header'."""
    if centered:
        return (f'<h2 class="mb-10 xl:mb-12 font-bold text-[#062A1C] text-3xl xl:text-4xl '
                f'text-center">{e(heading)}</h2>')
    cta = button(cta_label, cta_href, "secondary", "sm") if cta_label else ""
    return (f'<div class="flex flex-wrap justify-between items-center gap-4 mb-10">'
            f'<h2 class="font-bold text-[#062A1C] text-3xl xl:text-4xl">{e(heading)}</h2>{cta}</div>')


def carousel(slides_html, gap=24, arrows_top="130px", autoplay=False, dots=False, extra=""):
    """
    Direction-agnostic carousel shell. The JS in scripts.js drives it on a
    logical scroll axis so it behaves identically in RTL and LTR.
    """
    return f"""
          <div class="relative carousel {extra}"{' data-autoplay' if autoplay else ''} style="--carousel-gap:{gap}px">
            <div class="carousel-track">{slides_html}
            </div>
            <button type="button" class="hidden xl:grid top-[{arrows_top}] -start-5 absolute place-items-center bg-white shadow-custom3 rounded-full text-cta transition size-11 carousel-prev" aria-label="السابق">
              <span class="rtl:scale-flip">{ICON['arrow']}</span>
            </button>
            <button type="button" class="hidden xl:grid top-[{arrows_top}] -end-5 absolute place-items-center bg-white shadow-custom3 rounded-full text-cta transition size-11 carousel-next" aria-label="التالي">
              <span class="ltr:scale-flip">{ICON['arrow']}</span>
            </button>
            {'<div class="flex justify-center mt-4 carousel-dots"></div>' if dots else ''}
          </div>"""


def breadcrumb(trail):
    """trail: [(label, href|None)] — the last item is the current page."""
    parts = []
    for i, (label, href) in enumerate(trail):
        last = i == len(trail) - 1
        if last or not href:
            parts.append(f'<span class="font-semibold text-[#062A1C]">{e(label)}</span>')
        else:
            parts.append(
                f'<a href="{href}" class="text-neutral-secondary hover:text-primary transition-colors">{e(label)}</a>'
                # Decorative separator: hidden from assistive tech, and
                # toned up from #C6C6C6 (1.71:1) so it is still visible.
                f'<span aria-hidden="true" class="text-neutral-outline">/</span>')
    return (f'<nav aria-label="مسار التنقل" class="flex flex-wrap items-center gap-2 text-sm">'
            f'{"".join(parts)}</nav>')


def chip(label, href="#", active=False, filter_slug=None):
    """Filter pill — Figma 'Chip Button'.

    The mobile Collection frame (350:17805) fills inactive chips with
    interaction-base and drops the outline; the desktop Web frame keeps the
    white-on-outline treatment. Carry both rather than pick one.
    """
    style = ("bg-cta text-white border-cta" if active
             else "chip-filter bg-white text-[#062A1C] border-neutral-divider hover:border-cta")
    # `filter_slug` turns the chip into a live client-side filter; without it
    # the chip stays a plain link. The href is kept either way so the control
    # still means something with JS off.
    attr = f' data-filter="{e(filter_slug)}"' if filter_slug else ""
    # min-h-11 = 44px: WCAG 2.5.5 / HIG minimum tap target. At px-5 py-2 these
    # measured 38px, which is a miss on a phone.
    return (f'<a href="{href}"{attr} class="inline-flex items-center min-h-11 px-5 py-2 border rounded-full '
            f'font-semibold text-sm whitespace-nowrap transition-colors {style}">{e(label)}</a>')


_SORT_ICON = ('<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4" aria-hidden="true">'
              '<path d="M7 4v16m0 0-3-3m3 3 3-3M17 20V4m0 0-3 3m3-3 3 3" '
              'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
              'stroke-linejoin="round"/></svg>')


def sort_select(options, label="ترتيب حسب"):
    """Sort control.

    The mobile Collection frame (350:17805) shows this bare — a sort glyph and
    the current value, no chrome and no 'ترتيب حسب' prefix. The desktop frame
    keeps the outlined pill with its label, so the chrome is xl-only.
    """
    opts = "".join(f'<option value="{e(v)}">{e(t)}</option>' for v, t in options)
    return f"""
            <label class="inline-flex items-center gap-2 xl:bg-white px-0 xl:px-4 py-2 border border-transparent xl:border-neutral-divider rounded-full shrink-0">
              <span class="xl:hidden text-cta">{_SORT_ICON}</span>
              <span class="hidden xl:inline text-neutral-secondary text-sm">{e(label)}</span>
              <select class="select-sort bg-transparent font-semibold text-[#062A1C] text-sm outline-none cursor-pointer appearance-none xl:appearance-auto border-0 xl:border xl:border-neutral-divider">{opts}</select>
            </label>"""


def page_header(heading, trail=None):
    """
    Breadcrumb + page title block used by every inner page.

    `heading` is empty on the pages that carry their own title further down
    (product, blog post, account, auth). Those must emit NO h1 here: an empty
    one is announced as a blank level-1 heading and left every one of those
    113 pages with two h1s, the first of them silent.
    """
    crumbs = f"{breadcrumb(trail)}" if trail else ""
    head = (
        f'\n          <h1 class="font-bold text-[#062A1C] text-3xl xl:text-5xl">{e(heading)}</h1>'
        if heading
        else ""
    )
    return f"""
      <section class="pt-6">
        <div class="flex flex-col gap-4 mx-auto px-4 max-w-[1536px]">
          {crumbs}{head}
        </div>
      </section>"""


def product_grid(products, cols="grid-cols-2 md:grid-cols-3 xl:grid-cols-4", attrs=""):
    """`attrs` lets a caller tag the grid (e.g. the favourites page marks its
    own with data-favs-grid) without duplicating the card markup."""
    cards = "".join(product_card(p, slide=False) for p in products)
    extra = (" " + attrs) if attrs else ""
    return f'<div data-product-grid{extra} class="gap-4 xl:gap-6 grid {cols}">{cards}\n          </div>'


def rating(score="4.8", count=None):
    """
    Five marks that actually show the score. 4.8 draws four full and the fifth
    filled 80% of the way across — a row of five identical full marks beside
    the text "4.8" contradicts itself, which is what this used to do.

    The partial mark is one glyph layered over another and clipped by width,
    not a second half-glyph asset: the empty and full states stay the same
    shape, so nothing can drift if the icon is ever redrawn. The clip is on the
    INLINE axis via a logical inset, so in RTL it fills from the right like the
    row does.

    Marks are STARS by Ahmed's direction (2026-07-22). They started as the
    brand heart; on the product page a row of hearts read as favourites, not
    reviews — the same glyph the card's save button uses, one gesture away.
    The heart stays for favourites only.
    """
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0

    marks = []
    for i in range(5):
        # How much of THIS mark is filled: 1 for a whole one, the remainder on
        # the boundary mark, 0 after it.
        fill = max(0.0, min(1.0, value - i))
        if fill >= 0.999:
            marks.append(f'<span class="rating-mark is-full">{ICON["star"]}</span>')
        elif fill <= 0.001:
            marks.append(f'<span class="rating-mark">{ICON["star"]}</span>')
        else:
            pct = round(fill * 100)
            marks.append(
                f'<span class="rating-mark">{ICON["star"]}'
                f'<span class="rating-mark__fill" style="width:{pct}%">{ICON["star"]}</span>'
                f'</span>')
    tail = (f'<span class="text-neutral-secondary text-sm">(<span class="latin">{count}</span> تقييم)</span>'
            if count else "")
    return (f'<div class="flex items-center gap-1.5">'
            f'<span class="rating-marks flex items-center" role="img" '
            f'aria-label="{e(score)} من 5">{"".join(marks)}</span>'
            f'<span class="font-semibold text-[#062A1C] text-sm latin">{e(score)}</span>{tail}</div>')


def variant_chips(options, name="variant"):
    """Generic chip selector. options: [(label, active)] — no pricing."""
    items = "".join(
        f'<label class="cursor-pointer">'
        f'<input type="radio" name="{e(name)}" class="peer sr-only"{" checked" if active else ""} />'
        f'<span class="inline-flex items-center px-5 py-2 border border-neutral-divider rounded-full '
        f'font-semibold text-[#062A1C] text-sm transition-colors peer-checked:bg-cta '
        f'peer-checked:border-cta peer-checked:text-white">{e(label)}</span></label>'
        for label, active in options
    )
    return f'<div class="flex flex-wrap gap-2">{items}</div>'


def size_chips(p):
    """
    Real size options with real prices, from `sizes` in catalog.json
    (written by `fetch_sizes.py` — each one is a separate live SKU).

    Renders nothing at all unless the product genuinely has more than one size.
    The three chips this replaces — 500/250/100 جم — were invented, inert, and
    contradicted the 300 جم product they sat beneath.

    Each chip carries the size's own price and product id, so scripts.js can
    repoint the price AND the cart at the SKU actually chosen. Selecting 200 جم
    must not add the 100 جم SKU to the basket.
    """
    sizes = p.get("sizes") or []
    if len(sizes) < 2:
        return ""

    # Pre-select the size this page's product IS, not simply the first chip.
    current = p.get("id")
    if not any(str(s.get("id")) == str(current) for s in sizes):
        current = sizes[0].get("id")

    chips = "".join(
        f'<label class="cursor-pointer">'
        f'<input type="radio" name="size" class="peer sr-only"'
        f'{" checked" if str(s.get("id")) == str(current) else ""} '
        f'data-size-option data-size-id="{e(str(s.get("id")))}" '
        f'data-size-price="{s.get("price", 0)}" data-size-label="{e(s.get("label", ""))}" />'
        f'<span class="inline-flex items-center px-5 py-2 border border-neutral-divider rounded-full '
        f'font-semibold text-[#062A1C] text-sm transition-colors peer-checked:bg-cta '
        f'peer-checked:border-cta peer-checked:text-white latin">{e(s.get("label", ""))}</span>'
        f'</label>'
        for s in sizes
    )
    return f"""
            <div class="flex flex-col gap-2">
              <span class="font-semibold text-neutral-secondary text-xs">اختر الحجم</span>
              <div class="flex flex-wrap gap-2" data-size-chips>{chips}
              </div>
            </div>"""


def qty_stepper():
    """
    The reference Ahmed supplied draws the stepper as a padded container with
    the buttons as their own bordered shapes floating inside it — the padding
    between container and buttons is the point. Ours keeps that construction
    in this design system: circles rather than squares, the + carries the CTA
    fill (it is the "more" affordance, the louder of the two), the − stays
    quiet on a hairline. Buttons stay size-11: the reference's ~32px buttons
    would regress the audited 44px tap-target floor.
    """
    return f"""
              <div data-stepper class="inline-flex items-center gap-1 bg-white p-1 border border-neutral-divider rounded-full">
                <button type="button" data-step="-1" class="place-items-center grid border border-neutral-divider hover:bg-interaction-base rounded-full size-11 text-[#062A1C] transition-colors" aria-label="إنقاص"><span class="w-5 h-5">{ICON['minus']}</span></button>
                <span data-qty class="min-w-[2.5ch] font-bold text-[#062A1C] text-base text-center latin">1</span>
                <button type="button" data-step="1" class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full size-11 text-white transition-colors" aria-label="زيادة"><span class="w-5 h-5">{ICON['plus']}</span></button>
              </div>"""


def accordion(items, multi=False):
    """items: [(heading, inner_html)] — first is open."""
    rows = "".join(f"""
                <div class="accordion-item border-neutral-divider border-b{' is-open' if i == 0 else ''}">
                  <button type="button" class="accordion-trigger flex justify-between items-center gap-4 py-4 w-full text-start">
                    <span class="font-bold text-[#062A1C] text-base">{e(heading)}</span>
                    <span class="accordion-chevron text-cta">{ICON['chevron']}</span>
                  </button>
                  <div class="accordion-panel">
                    <div class="pb-4 text-neutral-800 text-sm leading-7">{body}</div>
                  </div>
                </div>""" for i, (heading, body) in enumerate(items))
    return f'<div data-accordion{" data-accordion-multi" if multi else ""}>{rows}\n              </div>'


def product_gallery(images, alt):
    """
    Main image with a selectable thumbnail strip — RTL puts thumbs on the far
    side. `images` is the product's real `images` list from catalog.json, main
    shot first; `fetch_galleries.py` fills it from the client's own CDN.

    The strip is suppressed entirely at one image, because a lone thumbnail
    under a photo reads as a broken carousel rather than a choice. 26 of the 99
    products are in that state today (see DESIGN-NOTES) — they degrade to
    exactly the single-image layout this page had before.

    Selection state is `aria-pressed` on the button and nothing else, the same
    contract the favourites heart uses, so the accessible state and the painted
    state cannot drift; styles.css draws the ring off that selector.
    """
    images = [i for i in (images or []) if i]
    if not images:
        return ""
    main_img = images[0]

    # The main shot is a background-isolated cutout and has to sit INSIDE the
    # plate with padding, contained. Every other shot is a real photograph with
    # its own background, and containing those leaves the photo floating in a
    # letterboxed island of #EDEFEB — the "weird appearance". Those fill the
    # frame edge to edge instead. `fetch_galleries.py` puts gallery shots in
    # their own directory, which is exactly the signal for which is which.
    def _is_photo(path):
        return "/gallery/" in path

    if len(images) == 1:
        strip = ""
    else:
        thumb_html = "".join(f"""
                <button type="button" data-gallery-thumb aria-pressed="{'true' if i == 0 else 'false'}"
                        aria-label="عرض الصورة {i + 1} من {len(images)}"
                        data-fill="{'cover' if _is_photo(t) else 'contain'}"
                        class="gallery-thumb bg-interaction-base rounded-xl w-20 h-20 shrink-0 overflow-hidden{'' if _is_photo(t) else ' p-2'}">
                  <img src="{e(t)}" alt=""
                       class="w-full h-full {'object-cover' if _is_photo(t) else 'object-contain'}" loading="lazy" />
                </button>""" for i, t in enumerate(images))
        # The vertical strip is capped to the height of the plate beside it and
        # scrolls past that. Without the cap, nine 80px thumbnails stack 720px
        # tall, make themselves the tallest thing in the row and drag the whole
        # product header down with them — the richest galleries, which are the
        # ones worth having, broke the layout worst. The cap is the plate's own
        # box: p-6 + 300 at md, p-10 + 440 at xl.
        strip = f"""
            <div class="flex md:flex-col gap-3 md:max-h-[348px] xl:max-h-[520px]
                        overflow-x-auto md:overflow-x-hidden md:overflow-y-auto no-scrollbar shrink-0">{thumb_html}
            </div>"""

    return f"""
          <!-- DOM order puts the info column first so RTL lands it in the right
               column at lg. The Figma mobile product frame (918:34326) leads
               with the media, so pull it above the info below lg — visually
               only, leaving the desktop column order untouched. -->
          <div data-gallery class="flex md:flex-row flex-col-reverse gap-4 order-first lg:order-none min-w-0">{strip}
            <!-- The plate keeps its own padding for the cut-out main shot;
                 scripts.js swaps data-fill to "cover" for the photographs,
                 which drops the padding and lets them bleed to the rounded
                 corners. Both states are the same box, so switching between
                 them never resizes the column. -->
            <!-- Fixed height on the PLATE, not the image, with border-box
                 padding. The two fill modes then swap the padding without the
                 outer box moving a pixel — otherwise switching to a photograph
                 would shrink the column by the padding it just dropped, and
                 the whole page would jump on every thumbnail click. The height
                 is also what the thumbnail strip is capped to. -->
            <div data-gallery-plate data-fill="{'cover' if '/gallery/' in main_img else 'contain'}"
                 class="gallery-plate flex-1 bg-interaction-base rounded-[20px] min-w-0 overflow-hidden
                        h-[348px] xl:h-[520px]">
              <img data-gallery-main src="{e(main_img)}" alt="{e(alt)}"
                   class="mx-auto w-full h-full" />
            </div>
          </div>"""


# --------------------------------------------------------------------------
# Social proof and reassurance
# --------------------------------------------------------------------------
# Below this rank a product stops being called a best seller. 20 of a real
# 653-product store is the top ~3%, which keeps the badge meaning something —
# a badge every product carries is decoration, not proof.
BEST_SELLER_RANK = 20


# How high a product must place inside its own category to be called a best
# seller there. Deliberately small, and paired with the CATEGORY_MIN below.
BEST_SELLER_CATEGORY_RANK = 3

# A category has to be big enough for "best seller in it" to mean anything.
# Top-3 of a four-product category is not a distinction, it is a rounding
# error — three quarters of the shelf would wear the badge.
BEST_SELLER_CATEGORY_MIN = 6


def _best_seller_label(p):
    """
    The badge text for a product, or "" if it has not earned one.

    Two tiers, both derived from the SAME real `popularityRank`
    (`fetch_popularity.py`, walking the Store API's `orderby=popularity` —
    WooCommerce's own total-sales ordering across the client's 653-product
    store). Nothing here is invented; the second tier just reads that ranking
    at a narrower scope.

      1. Top 20 store-wide      -> "الأكثر مبيعاً"
      2. Top 3 of its category  -> "الأكثر مبيعاً في <category>"

    Why the second tier exists: the store-wide top 20 is dominated by snacks
    and offers, so most categories had no badged product at all and a shopper
    browsing spices never saw the signal. A spice that outsells the other
    spices genuinely is the best selling spice.

    The store-wide label wins where both apply — it is the stronger claim, and
    two badges on one card would compete.
    """
    rank = p.get("popularityRank")
    if not rank:
        return ""
    if rank <= BEST_SELLER_RANK:
        return "الأكثر مبيعاً"
    if (
        p.get("categoryRank", 99) <= BEST_SELLER_CATEGORY_RANK
        and p.get("categorySize", 0) >= BEST_SELLER_CATEGORY_MIN
        and p.get("categoryAr")
    ):
        return f"الأكثر مبيعاً في {p['categoryAr']}"
    return ""


def best_seller_badge(p):
    """
    Renders only for products the client's own store actually ranks that high.
    A product silently loses the badge when the client's sales say it should.
    See `_best_seller_label` for the two tiers.
    """
    label = _best_seller_label(p)
    if not label:
        return ""
    # self-start, or the badge stretches to the full column width: it is a
    # child of a flex-col, where the default align-items is stretch and
    # inline-flex does nothing to stop it.
    #
    # The glyph wrapper is `grid place-items-center` and the label gets
    # `leading-none`, the same treatment the header icons needed. Without it
    # the star sits on the text baseline rather than on the text's optical
    # centre, and rides visibly low in the pill — Arabic ascenders make the
    # line box taller than the glyph, so "align to the line" and "align to the
    # letters" are not the same thing here.
    #
    # top-[2px]: Baloo Bhaijaan 2 carries a very deep descent (8px per 12px
    # em against an ink descent of ~3px for this label), so a vertically
    # centred line box paints the letters ~2px above the pill's optical
    # centre — Ahmed read the text as hugging the top. Measured with canvas
    # actualBoundingBox metrics, not eyeballed; the ink centre sits 1.9px
    # above the box centre at text-xs. `relative`, because transforms do not
    # apply to inline boxes.
    return ('<span class="inline-flex self-start items-center gap-1.5 bg-accent-yellow px-3 py-1.5 '
            'rounded-full font-bold text-[#062A1C] text-xs">'
            f'<span class="place-items-center grid w-3.5 h-3.5 shrink-0">{ICON["star"]}</span>'
            f'<span class="relative top-[2px] leading-none">{e(label)}</span></span>')


def sold_proof(p):
    """
    The encouragement line beside the rating.

    Deliberately a RANK, not a unit count. The live-site pattern this mirrors
    reads "500+ sold this week", but no public endpoint carries absolute sales
    volume, and inventing one would be exactly the kind of fabricated metric
    this project keeps out. A rank is real, checkable, and carries the same
    "other people are buying this" push. Swap it for a true count the moment
    the client exposes one — see DESIGN-NOTES.
    """
    rank = p.get("popularityRank")
    if not rank:
        return ""
    if rank <= BEST_SELLER_RANK:
        # Round up to a friendly bucket so the line reads as a claim, not a
        # lookup.
        bucket = 10 if rank <= 10 else BEST_SELLER_RANK
        scope = "في أبو عوف"
    elif (
        p.get("categoryRank", 99) <= BEST_SELLER_CATEGORY_RANK
        and p.get("categorySize", 0) >= BEST_SELLER_CATEGORY_MIN
        and p.get("categoryAr")
    ):
        # Tracks the badge exactly, on purpose. A product wearing "best seller
        # in spices" with no proof line beside it, or the reverse, is the same
        # split-signal problem the badge tiers were added to remove.
        bucket = BEST_SELLER_CATEGORY_RANK
        scope = f"في {p['categoryAr']}"
    else:
        return ""
    # The copy is ONE flex child, not loose text nodes beside the glyph.
    # Bare text and the <span class="latin"> around the number were each their
    # own flex item, so they wrapped independently — with a long category name
    # the line broke as "ضمن / أفضل" with the numeral stranded between the two
    # lines. Wrapping the sentence makes it flow as a sentence. `items-start`
    # so the flame stays on the first line rather than centring against a
    # two-line block.
    return ('<span class="inline-flex items-start gap-1.5 font-semibold text-accent-error text-sm">'
            f'<span class="mt-0.5 w-4 h-4 shrink-0">{ICON["flame"]}</span>'
            f'<span>ضمن أفضل <span class="latin">{bucket}</span> مبيعاً {e(scope)}</span></span>')


def trust_row(items):
    """
    The icon/title/subtitle reassurance strip that sits under the CTA.

    items: [(icon_key, title, subtitle)]. `subtitle` may be empty, in which
    case its line is not rendered at all — a benefit taken from the client's
    own copy is one sentence, not a title with a caption under it, and an
    empty span still costs its line-height and made those tiles sit unevenly
    against three-line neighbours.

    The column count follows the item count so a product with two benefits
    gets two columns rather than a hole where a third should be.

    Every claim here must already be made somewhere else on this site — these
    restate the delivery and returns policy and the real branch count, or they
    are the client's own product copy. Nothing asserts a new product claim
    like "third-party tested" that nobody has signed off.
    """
    if not items:
        return ""
    cols = {1: "grid-cols-1", 2: "grid-cols-2"}.get(len(items), "grid-cols-3")
    cells = ""
    for icon, title_, sub in items:
        sub_html = (
            f'\n                <span class="text-neutral-secondary text-xs leading-4">{e(sub)}</span>'
            if sub else ""
        )
        cells += f"""
              <div class="flex flex-col items-center gap-2 text-center">
                <span class="place-items-center grid bg-interaction-base rounded-full text-cta size-11 shrink-0">
                  <span class="w-5 h-5">{ICON[icon]}</span>
                </span>
                <span class="font-semibold text-[#062A1C] text-sm text-balance leading-5 line-clamp-3">{e(title_)}</span>{sub_html}
              </div>"""
    return f"""
            <div class="gap-4 grid {cols} pt-1">{cells}
            </div>"""


# Lines that are a spec, not a benefit. The client's benefit lists sometimes
# open or close with the pack weight ("100جرام"), which is already printed on
# the size chips and reads as filler in a benefit tile.
_SPEC_ONLY = re.compile(r"^[\d\s.,]*(جرام|جم|كجم|مل|لتر|g|gm|kg|ml)?[\d\s.,]*$", re.I)


def benefit_bullets(p, limit=3):
    """The client's own benefit lines for this product, cleaned to plain text."""
    raw = p.get("descHtmlAr") or ""
    out = []
    for frag in re.findall(r"<li[^>]*>(.*?)</li>", raw, re.S):
        text = re.sub(r"<[^>]+>", "", frag)
        text = " ".join(html_mod.unescape(text).split())
        if text and not _SPEC_ONLY.match(text):
            out.append(text)
    return out[:limit]


# Generic quality glyphs. Deliberately not claim-bearing — they decorate the
# client's sentence, they do not add a meaning of their own the way a "vegan"
# or "tested" mark would.
_BENEFIT_ICONS = ("leaf", "bolt", "shield")


def product_benefits(p, fallback):
    """
    The strip under the CTA, built from the client's OWN benefit copy.

    Only the single hero product used to get product benefits here; the other
    98 got the site-service trio (delivery / returns / branch count), so a
    shopper moving from the hero to any other product saw the product tiles
    replaced by delivery notes and the page read as a different template.
    That was the complaint.

    Coverage is the honest limit of the data: 64 of 99 products have at least
    two usable benefit lines in `descHtmlAr`. The remaining 35 have none — the
    client never wrote them — so those keep the service strip rather than
    getting invented copy. Absence over invention, same rule as the branch
    phone numbers.
    """
    bullets = benefit_bullets(p)
    if len(bullets) < 2:
        return trust_row(fallback)
    return trust_row([(_BENEFIT_ICONS[i], b, "") for i, b in enumerate(bullets)])


# --------------------------------------------------------------------------
# Forms — Figma 'Input Field' section (150:4622)
# --------------------------------------------------------------------------
# Autofill tokens, inferred from the field name rather than passed at every
# call site — the names are already semantic, and doing it here means no
# checkout or auth field can be added later without one.
#
# Not cosmetic: with no autocomplete attribute anywhere, a browser or
# password manager could not fill a single field on the 10-field checkout,
# which on a phone is most of the work of ordering.
_AUTOCOMPLETE = {
    "first-name": "given-name",
    "last-name": "family-name",
    "name": "name",
    "email": "email",
    "phone": "tel",
    "city": "address-level2",
    "district": "address-level3",
    "area": "address-level3",
    "street": "address-line1",
    "floor": "address-line2",
    "apartment": "address-line2",
    "line1": "address-line1",
    "line2": "address-line2",
    "postcode": "postal-code",
}

# type=tel already summons a numeric keypad; these are the free-text fields
# that hold digits and would otherwise open a full QWERTY on a phone.
_INPUTMODE = {"floor": "numeric", "apartment": "numeric", "postcode": "numeric"}


def _field_hints(name, type_, autocomplete=None):
    ac = autocomplete or _AUTOCOMPLETE.get(name)
    if ac is None and type_ == "password":
        ac = "current-password"
    im = _INPUTMODE.get(name)
    out = ""
    if ac:
        out += f' autocomplete="{e(ac)}"'
    if im:
        out += f' inputmode="{e(im)}"'
    return out


def field(label, name, type_="text", required=False, value="", placeholder="",
          wrap="", autocomplete=None):
    star = '<span class="text-accent-error">*</span>' if required else ""
    hints = _field_hints(name, type_, autocomplete)
    return f"""
                <div class="flex flex-col gap-1.5 {wrap}">
                  <label for="{e(name)}" class="font-medium text-neutral-secondary text-sm">{e(label)}{star}</label>
                  <input type="{e(type_)}" id="{e(name)}" name="{e(name)}"{' required' if required else ''}{hints}
                         value="{e(value)}" placeholder="{e(placeholder)}"
                         class="bg-white px-4 py-3 border-2 border-neutral-divider focus:border-cta rounded-xl outline-none w-full text-[#062A1C] text-base transition-colors" />
                </div>"""


def select_field(label, name, options, required=False, wrap=""):
    star = '<span class="text-accent-error">*</span>' if required else ""
    opts = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in options)
    hints = _field_hints(name, "select")
    return f"""
                <div class="flex flex-col gap-1.5 {wrap}">
                  <label for="{e(name)}" class="font-medium text-neutral-secondary text-sm">{e(label)}{star}</label>
                  <select id="{e(name)}" name="{e(name)}"{' required' if required else ''}{hints}
                          class="select-control bg-white px-4 py-3 border-2 border-neutral-divider focus:border-cta rounded-xl outline-none w-full text-[#062A1C] text-base transition-colors">
                    <option value="">اختر</option>{opts}
                  </select>
                </div>"""


def radio_card(name, value, heading, sub="", icon="", checked=False, accent=False):
    """Big selectable card — order type, delivery time, delivery method.

    The trailing glyph is a real radio indicator (`.radio-dot`, styles.css),
    not the chevron this used to end with — a chevron promises navigation,
    but choosing here only selects (Ahmed asked for styled radio buttons,
    2026-07-22). `h-full` on the face: paired cards share a flex row, so the
    one without a subtitle used to stand shorter than its neighbour.

    accent=True is the gift treatment — the icon sits on an accent-yellow
    chip and the checked card takes a warm wash (`.radio-card-accent`), so
    إهداء reads as an occasion while the default order stays logistics.
    """
    sub_html = f'<span class="text-neutral-secondary text-xs">{e(sub)}</span>' if sub else ""
    icon_html = (
        f'<span class="place-items-center grid bg-accent-yellow rounded-full size-10 text-[#062A1C] shrink-0">{icon}</span>'
        if accent else f'<span class="text-cta">{icon}</span>'
    )
    return f"""
                <label class="flex-1 cursor-pointer">
                  <input type="radio" name="{e(name)}" value="{e(value)}" class="peer sr-only"{' checked' if checked else ''} />
                  <span class="flex justify-between items-center gap-3 bg-white px-5 py-4 border-2 border-neutral-divider peer-checked:border-cta rounded-xl transition-colors h-full{' radio-card-accent' if accent else ''}">
                    <span class="flex items-center gap-3">
                      {icon_html}
                      <span class="flex flex-col">
                        <span class="font-semibold text-[#062A1C] text-base">{e(heading)}</span>
                        {sub_html}
                      </span>
                    </span>
                    <span class="radio-dot shrink-0" aria-hidden="true"></span>
                  </span>
                </label>"""


# --------------------------------------------------------------------------
# Cart
# --------------------------------------------------------------------------
def cart_line(p, qty=1, weight="250 جم"):
    from catalog import money, title as _title
    return f"""
              <!-- The thumb, stepper and price chip are all shrink-0 and with
                   gaps come to ~302px, so in a 295px column they squeezed the
                   title to zero width — product names vanished on mobile. Let
                   the row wrap below sm so the stepper and price drop to a
                   second line, and hold a floor under the title. -->
              <!-- data-cart-static: server-rendered so the page is not blank
                   without JS, but the cart store owns this list once it boots
                   and clears these on its first render. -->
              <article data-cart-static class="flex flex-wrap sm:flex-nowrap items-center gap-4 py-5 border-neutral-divider border-b">
                <img src="{e(p['image'])}" alt="{e(_title(p))}" class="bg-interaction-base p-2 rounded-xl w-20 h-20 object-contain shrink-0" loading="lazy" />
                <div class="flex flex-col flex-1 gap-1 min-w-[7rem]">
                  <h3 class="font-semibold text-[#062A1C] text-base line-clamp-2">{e(_title(p))}</h3>
                  <span class="text-neutral-secondary text-xs">{e(weight)}</span>
                  <button type="button" class="mt-1 text-accent-error text-xs underline self-start">حذف</button>
                </div>
                <div data-stepper class="inline-flex items-center gap-1 p-1 border border-neutral-divider rounded-full shrink-0">
                  <button type="button" data-step="-1" class="place-items-center grid size-9 text-[#062A1C] transition-colors hover:bg-interaction-base rounded-full" aria-label="إنقاص"><span class="w-4 h-4">{ICON['minus']}</span></button>
                  <span data-qty class="min-w-[2ch] font-semibold text-[#062A1C] text-sm text-center latin">{qty}</span>
                  <button type="button" data-step="1" class="place-items-center grid size-9 bg-cta hover:bg-cta-hover text-white transition-colors rounded-full" aria-label="زيادة"><span class="w-4 h-4">{ICON['plus']}</span></button>
                </div>
                <span class="bg-accent-yellow px-2 py-0.5 rounded font-bold text-[#062A1C] text-sm latin shrink-0">EGP {money(p['price'])}</span>
              </article>"""


def points_banner(points=100, discount=100):
    """
    Live control, not decoration: scripts.js applies `discount` to the cart
    totals when the button is pressed and stores it under abuauf:pointsDiscount,
    so it survives the trip from cart to checkout. Pressing again cancels it.
    Defaults are 100/100 so the cart and checkout describe the SAME wallet —
    they used to say 120 points on one page and 100 on the other.

    The points themselves are demo state (no wallet endpoint exists) — see
    DESIGN-NOTES. The button had no handler at all until Ahmed pressed it.
    """
    return f"""
            <div data-points-banner data-points-discount="{discount}" class="flex justify-between items-center gap-3 bg-accent-yellow p-4 rounded-xl">
              <!-- Two copies of the message, one per state, toggled by
                   syncPointsUI. With one copy the banner kept promising
                   "لديك 100 نقطة" AFTER the points were spent — the state
                   changed under it and the words did not (Ahmed,
                   2026-07-22). -->
              <span class="font-semibold text-[#062A1C] text-sm leading-6" data-points-idle>
                لديك <span class="latin">{points}</span> نقطة في محفظتك<br />ويمكنك خصم <span class="latin">EGP {discount}</span>
              </span>
              <span class="font-semibold text-[#062A1C] text-sm leading-6" data-points-used hidden>
                استخدمت <span class="latin">{points}</span> نقطة من محفظتك<br />وتم خصم <span class="latin">EGP {discount}</span> من الإجمالي
              </span>
              <button type="button" data-points-apply class="bg-cta hover:bg-cta-hover px-4 py-2 rounded-full font-semibold text-white text-xs whitespace-nowrap transition-colors">خصم المبلغ</button>
            </div>"""


def bundle_item(p, checked=True):
    """
    One row of the 'frequently bought together' checklist.

    Carries the full `data-product` payload. It used to be presentation only,
    so the section's "أضف الجميع الى السلة" button had nothing to add:
    productFrom() walks up to the nearest [data-product] and bails without
    one, so the handler returned silently and the button did nothing — the
    same defect already fixed once on the upsell rail in scripts.js.
    """
    from catalog import money, title as _title
    return f"""
                <label data-product data-bundle-item
                       data-id="{e(p.get('id', 0))}" data-name="{e(_title(p))}"
                       data-price="{e(p['price'])}" data-image="{e(p['image'])}"
                       class="flex items-center gap-3 py-2 cursor-pointer">
                  <input type="checkbox" data-bundle-check{' checked' if checked else ''} class="accent-[#163300] shrink-0 rounded w-5 h-5" />
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base shrink-0 p-1 rounded-lg w-12 h-12 object-contain" loading="lazy" />
                  <span class="flex-1 min-w-0 text-[#062A1C] text-sm leading-5 line-clamp-2">{e(_title(p))}</span>
                  <span class="bg-accent-yellow px-2 py-0.5 rounded font-bold text-[#062A1C] text-xs latin shrink-0">EGP {money(p['price'])}</span>
                </label>"""


# --------------------------------------------------------------------------
# Commerce
# --------------------------------------------------------------------------
def product_card(p, slide=True):
    """
    Product card — Figma 'Stack/ Web' (763:35266).
    Used by home rails, shop grid, category pages, cart upsells and the
    product page's related rail. Change it here, rebuild, it changes everywhere.
    """
    on_sale = p.get("sale") and p["sale"] < p["regular"]
    old = (f'<span class="text-neutral-secondary text-sm line-through latin">EGP {money(p["regular"])}</span>'
           if on_sale else "")
    wrapper = ("carousel-slide w-[260px] xl:w-[300px] shrink-0" if slide else "w-full")
    # Filter/sort keys for the listing pages. Everything here is a real field
    # from catalog.json — `id` doubles as the recency proxy because the
    # catalogue carries no publish date (see DESIGN-NOTES).
    # data-product marks this as something the cart can read; the cart store
    # reads name/price/image straight off the card, so adding to the cart needs
    # no lookup table and still works from file://.
    keys = (f'data-product data-cat="{e(p.get("categorySlug", ""))}" '
            f'data-price="{p.get("sale") or p.get("price") or 0}" '
            f'data-id="{p.get("id", 0)}" '
            f'data-name="{e(title(p))}" '
            # Real English name from catalog.json — used by the language
            # switcher. Not a translation we wrote.
            f'data-name-en="{e(p.get("name") or title(p))}" '
            f'data-image="{e(p["image"])}"')
    return f"""
          <article class="product-card {wrapper}" {keys}>
            <div class="product-card__frame flex flex-col bg-white shadow-custom4 rounded-2xl h-full overflow-hidden">
              <a href="product-{p.get('id', 0)}.html" class="product-card__media block relative bg-interaction-base p-4">
                <img src="{e(p['image'])}" alt="{e(title(p))}"
                     class="mx-auto w-full h-[180px] xl:h-[200px] object-contain" loading="lazy" />
                <span class="product-card__peek bottom-3 start-3 absolute place-items-center grid bg-white/90 hover:bg-white shadow-custom4 rounded-full text-[#062A1C] size-8"
                      aria-hidden="true">{ICON['expand']}</span>
              </a>
              <div class="flex flex-col flex-1 gap-1.5 p-4">
                <h3 class="font-semibold text-[#062A1C] text-base leading-6 line-clamp-2">
                  <a href="product-{p.get('id', 0)}.html" data-product-title class="hover:text-primary transition-colors">{e(title(p))}</a>
                </h3>
                <div class="flex flex-wrap items-center gap-2 mt-auto pt-2">
                  {old}
                  <span class="bg-accent-yellow px-2 py-0.5 rounded font-bold text-[#062A1C] text-sm latin">EGP {money(p['price'])}</span>
                </div>
                <!-- flex-wrap + the SAME flex-basis on both controls.
                     In the 2-column listing grid the card is 128.5px wide at
                     320, so 96.5px of content — which fits neither the add
                     button on one readable line nor the stepper beside the
                     heart. An equal basis makes both wrap to their own line at
                     the same width, so swapping one for the other never
                     changes the card's height.

                     basis, NOT min-width: basis drives the line break AND
                     still lets the control shrink once it is alone on its
                     line. min-width did one or the other, never both — at 104
                     it overflowed the 96.5px card at 320, and at 88 it stayed
                     wedged beside the heart at 414 and squeezed the taps to
                     38px. 104px = 44 + 16 + 44, the stepper at full tap size.

                     `grow shrink basis-*` rather than `flex-1 basis-*`:
                     Tailwind emits the `flex` shorthand after `basis`, so
                     flex-1 would quietly reset the basis to 0. -->
                <div class="flex flex-wrap items-center gap-2 pt-2">
                  <!-- Saved state is carried by aria-pressed alone, so the
                       accessible state and the painted state cannot drift;
                       styles.css swaps the icon off that selector. -->
                  <button type="button" data-fav-toggle aria-pressed="false" aria-label="أضف إلى المفضلة"
                          class="fav-btn btn-elevate place-items-center grid hover:bg-interaction-base border border-neutral-divider rounded-full text-cta shrink-0 size-11"
                          >{ICON['heart']}{ICON['heart_full']}</button>
                  <button type="button" data-add-to-cart
                          class="btn-elevate grow shrink basis-[104px] bg-cta hover:bg-cta-hover py-3 rounded-full font-semibold text-white text-sm">اضف الى السلة</button>
                  <!-- Shown by scripts.js once the product is in the cart, in
                       place of the add button. `hidden` is safe to toggle on a
                       flex container here only because styles.css forces
                       display:none on [hidden] with !important. -->
                  <!-- The number is flex-1 with NO min-w-0, so its own text is
                       its floor and it can never be crushed narrower than the
                       digits — the sweep caught exactly that at 414, a 5px
                       overflow inside the span. The buttons are the ones that
                       give, down to a 36px floor, which only ever happens at a
                       three-digit quantity on a 320px screen. -->
                  <!-- Colour lives in styles.css, not here: this is the light
                       counterpart of the solid CTA button it replaces — the
                       brand's light surface with the CTA green as the ink, so
                       an item already in the cart reads as settled rather than
                       shouting as loudly as the button that put it there. -->
                  <div data-card-stepper hidden
                       class="card-stepper flex grow shrink basis-[104px] min-w-0 items-center rounded-full h-11">
                    <!-- The visible circle is the inner .stepper-face, NOT the
                         button. The face is 36px, inset 4px like the product
                         page's padded counter, while the button stays the
                         full 44px of the control's height — the padding is
                         painted, the tap target is not reduced. Shrinking the
                         button itself would regress the audited 44px floor,
                         and growing the control would resize the card on the
                         add-button swap. -->
                    <button type="button" data-card-step="-1" aria-label="إنقاص"
                            class="place-items-center grid rounded-full size-11 min-w-9"><span class="stepper-face place-items-center grid rounded-full size-9"><span class="w-4 h-4">{ICON['minus']}</span></span></button>
                    <span data-card-qty class="flex-1 font-bold text-base text-center latin">1</span>
                    <button type="button" data-card-step="1" aria-label="زيادة"
                            class="place-items-center grid rounded-full size-11 min-w-9"><span class="stepper-face place-items-center grid rounded-full size-9"><span class="w-4 h-4">{ICON['plus']}</span></span></button>
                  </div>
                </div>
              </div>
            </div>
          </article>"""


def category_tile(cat, label=None, href="shop-category.html"):
    """
    Round category tile — Figma Section 563:31568.
    The CMS category images are photographs with their own backgrounds, not
    transparent cutouts, so they fill the circle rather than float inside it.
    """
    name = label or cat["ar"]
    return f"""
        <a href="{href}" class="group flex flex-col items-center gap-4 text-center">
          <span class="tile-lift relative bg-beige rounded-full w-[220px] xl:w-[250px] h-[220px] xl:h-[250px] overflow-hidden group-hover:scale-[1.03]">
            <img src="{e(cat['image'])}" alt="{e(name)}" class="w-full h-full object-cover" loading="lazy" />
          </span>
          <span class="flex flex-col gap-1">
            <span class="font-bold text-[#062A1C] group-hover:text-primary text-2xl xl:text-3xl transition-colors">{e(name)}</span>
            <span class="font-medium text-neutral-secondary text-base xl:text-xl">تشكيلة متنوعة تبدا من <span class="latin">17</span> جنية</span>
          </span>
        </a>"""


def review_card(name, city, text, score="4.8"):
    """
    The score row is the shared rating() — stars per Ahmed's 2026-07-22
    direction, superseding the Figma's heart component (the heart now means
    favourites and nothing else). It also fixes what the old hand-rolled row
    got wrong: five identical FULL marks beside the text "4.8", the exact
    self-contradiction rating() was built to eliminate. One component, so
    reviews and the product page can never disagree on what a rating looks
    like.
    """
    return f"""
          <article class="flex flex-col gap-4">
            {rating(score)}
            <p class="text-neutral-800 text-base xl:text-lg leading-7">{e(text)}</p>
            <p class="font-semibold text-neutral-secondary text-sm">{e(name)} — {e(city)}</p>
          </article>"""


def blog_card(img, tag, heading, excerpt, href="blog.html"):
    return f"""
        <article class="flex flex-col bg-white shadow-custom4 rounded-2xl overflow-hidden">
          <a href="{href}" class="block bg-interaction-base aspect-[500/366] overflow-hidden">
            <img src="{e(img)}" alt="{e(heading)}" class="w-full h-full hover:scale-105 object-cover transition-transform duration-500" loading="lazy" />
          </a>
          <div class="flex flex-col gap-3 p-6 xl:p-8">
            <span class="font-semibold text-primary text-sm">{e(tag)}</span>
            <h3 class="font-bold text-[#062A1C] text-xl xl:text-2xl leading-8 line-clamp-2">
              <a href="{href}" class="hover:text-primary transition-colors">{e(heading)}</a>
            </h3>
            <p class="text-neutral-secondary text-base leading-7 line-clamp-2">{e(excerpt)}</p>
            <a href="{href}" class="inline-flex justify-center items-center bg-interaction-base hover:bg-cta mt-2 rounded-full text-cta hover:text-white transition-colors self-start size-12" aria-label="اقرأ المزيد">
              <span class="rtl:scale-flip">{ICON['arrow']}</span>
            </a>
          </div>
        </article>"""


def recipe_card(img, tag, heading, excerpt, minutes, href="blog.html"):
    return f"""
        <article class="flex bg-white shadow-custom4 rounded-2xl overflow-hidden">
          <!-- min-w-0: the image is a fixed 160px shrink-0, so without this the
               text column's min-content floor pushed the card ~10px wide at
               320px viewports. -->
          <div class="flex flex-col flex-1 gap-2 p-6 xl:p-8 min-w-0">
            <span class="font-semibold text-primary text-sm">{e(tag)}</span>
            <h3 class="font-bold text-[#062A1C] text-xl xl:text-2xl leading-8 break-words">{e(heading)}</h3>
            <p class="text-neutral-secondary text-base leading-7 line-clamp-2">{e(excerpt)}</p>
            {button("شاهد الوصفة", href, "primary", "sm", "mt-auto")}
          </div>
          <div class="relative w-[160px] xl:w-[320px] shrink-0">
            <img src="{e(img)}" alt="{e(heading)}" class="w-full h-full object-cover" loading="lazy" />
            <span class="top-4 start-4 absolute inline-flex items-center gap-1.5 bg-white/90 px-3 py-1.5 rounded-full font-semibold text-[#062A1C] text-sm">
              {ICON['clock']}<span class="latin">{minutes}</span> د
            </span>
          </div>
        </article>"""


def info_card(img, heading, body, cta_label, cta_href, img_class="w-[100px] h-[100px]"):
    """The paired branches / export cards at the foot of the home page."""
    return f"""
            <div class="flex flex-col items-center gap-4 bg-interaction-base px-6 py-12 xl:py-16 rounded-[20px] text-center">
              <img src="{e(img)}" alt="" class="{img_class} object-contain" loading="lazy" />
              <h3 class="mt-4 font-bold text-[#062A1C] text-2xl xl:text-3xl">{e(heading)}</h3>
              <p class="max-w-[280px] text-neutral-800 text-base xl:text-lg leading-7">{body}</p>
              {button(cta_label, cta_href, "primary", "lg", "mt-4")}
            </div>"""


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------
# Production origin, for canonical and og:url/og:image, which social
# scrapers need as absolute URLs.
#
# Deliberately EMPTY. The build is not deployed yet and abuauf.com is the
# client's existing live site, not this one — pointing canonical at it would
# tell search engines these pages are duplicates of somebody else's. While
# it is empty the shell emits the tags that work without a domain and skips
# the three that do not. Set it once the real host is known; DESIGN-NOTES
# tracks it as a pre-launch item.
SITE_ORIGIN = ""

OG_IMAGE = "images/abuauf/brand/logo-abuauf-white.webp"

# Keep this build out of search results.
#
# It is a pixel-close rebuild of a storefront that is live and trading at
# abuauf.com, and it still carries placeholder legal pages and invented
# reviews. Indexed, it would compete with the client's real site for their own
# brand terms and could land a customer on a demo they believe is real.
#
# NOTE this is a `noindex` META TAG, not a robots.txt `Disallow`. Those are not
# interchangeable and the difference is the usual mistake: `Disallow` stops
# Google *fetching* the page, which means it never reads the noindex — and it
# will still list a URL it has never fetched if something links to it. To be
# reliably absent you have to let the crawler IN and tell it no. robots.txt
# here therefore allows crawling on purpose.
#
# One line to flip when this becomes the real production site.
ALLOW_INDEXING = False


def _social_meta(title_text, description, path):
    """og:/twitter: block. Egypt shares storefront links on WhatsApp far more
    than anywhere else, and a link with no card is a bare grey URL."""
    tags = [
        '<meta name="theme-color" content="#163300" />',
    ]
    if not ALLOW_INDEXING:
        tags.append('<meta name="robots" content="noindex, nofollow" />')
    tags += [
        f'<meta property="og:title" content="{e(title_text)}" />',
        f'<meta property="og:description" content="{e(description)}" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="أبو عوف" />',
        '<meta property="og:locale" content="ar_EG" />',
        '<meta name="twitter:card" content="summary_large_image" />',
    ]
    if SITE_ORIGIN:
        url = SITE_ORIGIN.rstrip("/") + path
        tags.append(f'<link rel="canonical" href="{e(url)}" />')
        tags.append(f'<meta property="og:url" content="{e(url)}" />')
        tags.append(
            f'<meta property="og:image" content="{e(SITE_ORIGIN.rstrip("/") + "/" + OG_IMAGE)}" />'
        )
    return "\n    ".join(tags)


_SECTION_OPEN = re.compile(r"<section(?![^>]*\bdata-reveal\b)(\s|>)")


def _with_reveal(body):
    """
    Tag every top-level `<section>` for the scroll reveal.

    Done here rather than in 37 page files so the entrance is one decision and
    genuinely site-wide — it was previously hand-applied to home, product and
    the auth layout only, so most of the site scrolled dead.

    Sections that already carry `data-reveal` are skipped, so the few places
    that opted in by hand keep exactly the behaviour they had.

    Safe by construction: the hidden state lives behind `.js-reveal`, which JS
    puts on <html> at runtime, and the observer reveals anything already in
    the viewport without animating it. So a page still paints fully with JS
    off, and nothing fades in underneath the shopper on first load — only
    sections they scroll to.
    """
    return _SECTION_OPEN.sub(r"<section data-reveal\1", body)


def page(title_text, description, body, page_id, path, main_class="overflow-x-hidden"):
    """
    Standard document shell. Header, footer and overlays are mount points
    filled at runtime by scripts.js, so chrome changes need no rebuild.
    """
    body = _with_reveal(body)
    social = _social_meta(title_text, description, path)
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{e(title_text)}</title>
    <meta name="description" content="{e(description)}" />
    {social}
    <!-- Abu Auf design system. Tailwind is COMPILED AT BUILD TIME by
         `npm run css` (config: tailwind.config.js) into tailwind.css. It used
         to be the Play CDN, which Tailwind itself warns against in production:
         that shipped ~120KB of JavaScript which then had to scan the DOM and
         generate the stylesheet on every visit, so nothing was styled until it
         finished — a flash of unstyled content on exactly the slow mobile
         connections this storefront is for. Now it is one 30KB cacheable file.

         ORDER IS LOAD-BEARING: tailwind.css first, styles.css second.
         styles.css contains rules whose whole purpose is to beat a utility
         ([hidden] !important, the focus ring re-armed over `outline-none`,
         the sticky-nav selector). Reverse these two and they stop working. -->
    <link rel="stylesheet" href="tailwind.css" />
    <link rel="stylesheet" href="styles.css" />
    <link rel="icon" href="images/abuauf/brand/logo-abuauf-white.webp" />
    <script defer src="scripts.js"></script>
  </head>
  <body data-page="{e(page_id)}" data-path="{e(path)}" class="antialiased bg-white">
    <!-- First focusable thing on the page. The header is three bands and a
         mega-menu, so a keyboard shopper otherwise tabbed through the whole
         of it on every page before reaching any content. Visually hidden
         until focused. -->
    <a href="#main" class="skip-link">تخطي إلى المحتوى</a>

    <!-- Shared header is injected here by scripts.js -->
    <div id="site-header"></div>

    <main id="main" tabindex="-1" class="{main_class}">{body}
    </main>

    <!-- Shared footer is injected here by scripts.js -->
    <div id="site-footer"></div>
  </body>
</html>
"""
