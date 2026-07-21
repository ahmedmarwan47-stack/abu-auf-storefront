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
            {'<div class="flex justify-center gap-2 mt-4 carousel-dots"></div>' if dots else ''}
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
                f'<span class="text-neutral-disabled">/</span>')
    return (f'<nav aria-label="مسار التنقل" class="flex flex-wrap items-center gap-2 text-sm">'
            f'{"".join(parts)}</nav>')


def chip(label, href="#", active=False):
    """Filter pill — Figma 'Chip Button'."""
    style = ("bg-cta text-white border-cta" if active
             else "bg-white text-[#062A1C] border-neutral-divider hover:border-cta")
    return (f'<a href="{href}" class="inline-flex items-center px-5 py-2 border rounded-full '
            f'font-semibold text-sm whitespace-nowrap transition-colors {style}">{e(label)}</a>')


def sort_select(options, label="ترتيب حسب"):
    opts = "".join(f'<option value="{e(v)}">{e(t)}</option>' for v, t in options)
    return f"""
            <label class="inline-flex items-center gap-2 bg-white px-4 py-2 border border-neutral-divider rounded-full shrink-0">
              <span class="text-neutral-secondary text-sm">{e(label)}</span>
              <select class="bg-transparent font-semibold text-[#062A1C] text-sm outline-none cursor-pointer">{opts}</select>
            </label>"""


def page_header(heading, trail=None):
    """Breadcrumb + page title block used by every inner page."""
    crumbs = f"{breadcrumb(trail)}" if trail else ""
    return f"""
      <section class="pt-6">
        <div class="flex flex-col gap-4 mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          {crumbs}
          <h1 class="font-bold text-[#062A1C] text-3xl xl:text-5xl">{e(heading)}</h1>
        </div>
      </section>"""


def product_grid(products, cols="grid-cols-2 md:grid-cols-3 xl:grid-cols-4"):
    cards = "".join(product_card(p, slide=False) for p in products)
    return f'<div class="gap-4 xl:gap-6 grid {cols}">{cards}\n          </div>'


def rating(score="4.8", count=None):
    hearts = "".join(f'<span class="text-accent-yellow">{ICON["heart_full"]}</span>' for _ in range(5))
    tail = (f'<span class="text-neutral-secondary text-sm">(<span class="latin">{count}</span> تقييم)</span>'
            if count else "")
    return (f'<div class="flex items-center gap-2">'
            f'<span class="flex items-center gap-0.5">{hearts}</span>'
            f'<span class="font-semibold text-[#062A1C] text-sm latin">{e(score)}</span>{tail}</div>')


def variant_chips(options, name="variant"):
    """Size / weight selector. options: [(label, active)]"""
    items = "".join(
        f'<label class="cursor-pointer">'
        f'<input type="radio" name="{e(name)}" class="peer sr-only"{" checked" if active else ""} />'
        f'<span class="inline-flex items-center px-5 py-2 border border-neutral-divider rounded-full '
        f'font-semibold text-[#062A1C] text-sm transition-colors peer-checked:bg-cta '
        f'peer-checked:border-cta peer-checked:text-white">{e(label)}</span></label>'
        for label, active in options
    )
    return f'<div class="flex flex-wrap gap-2">{items}</div>'


def qty_stepper():
    return """
              <div data-stepper class="inline-flex items-center gap-1 border border-neutral-divider rounded-full overflow-hidden">
                <button type="button" data-step="-1" class="place-items-center grid hover:bg-interaction-base size-11 font-bold text-[#062A1C] text-xl transition-colors" aria-label="إنقاص">−</button>
                <span data-qty class="min-w-[2ch] font-semibold text-[#062A1C] text-base text-center latin">1</span>
                <button type="button" data-step="1" class="place-items-center grid hover:bg-interaction-base size-11 font-bold text-[#062A1C] text-xl transition-colors" aria-label="زيادة">+</button>
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


def product_gallery(main_img, thumbs, alt):
    """Main image with a thumbnail strip — RTL puts thumbs on the far side."""
    thumb_html = "".join(f"""
              <button type="button" class="bg-interaction-base p-2 border-2 {'border-cta' if i == 0 else 'border-transparent hover:border-neutral-divider'} rounded-xl w-20 h-20 shrink-0 transition-colors">
                <img src="{e(t)}" alt="" class="w-full h-full object-contain" loading="lazy" />
              </button>""" for i, t in enumerate(thumbs))
    return f"""
          <div class="flex md:flex-row flex-col-reverse gap-4">
            <div class="flex md:flex-col gap-3 overflow-x-auto no-scrollbar">{thumb_html}
            </div>
            <div class="flex-1 bg-interaction-base p-6 xl:p-10 rounded-[20px]">
              <img src="{e(main_img)}" alt="{e(alt)}" class="mx-auto w-full max-w-[520px] h-[300px] xl:h-[440px] object-contain" />
            </div>
          </div>"""


def bundle_item(p, checked=True):
    """One row of the 'frequently bought together' checklist."""
    from catalog import money, title as _title
    return f"""
                <label class="flex items-center gap-3 py-2 cursor-pointer">
                  <input type="checkbox"{' checked' if checked else ''} class="accent-[#163300] rounded w-5 h-5" />
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1 rounded-lg w-12 h-12 object-contain" loading="lazy" />
                  <span class="flex-1 text-[#062A1C] text-sm leading-5 line-clamp-2">{e(_title(p))}</span>
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
    return f"""
          <article class="{wrapper}">
            <div class="flex flex-col bg-white shadow-custom4 rounded-2xl h-full overflow-hidden">
              <a href="product.html" class="block relative bg-interaction-base p-4">
                <img src="{e(p['image'])}" alt="{e(title(p))}"
                     class="mx-auto w-full h-[180px] xl:h-[200px] object-contain" loading="lazy" />
                <span class="bottom-3 start-3 absolute place-items-center grid bg-white/85 hover:bg-white rounded-full text-[#062A1C] transition-colors size-8"
                      aria-hidden="true">{ICON['expand']}</span>
              </a>
              <div class="flex flex-col flex-1 gap-1.5 p-4">
                <h3 class="font-semibold text-[#062A1C] text-base leading-6 line-clamp-2">
                  <a href="product.html" class="hover:text-primary transition-colors">{e(title(p))}</a>
                </h3>
                <div class="flex flex-wrap items-center gap-2 mt-auto pt-2">
                  {old}
                  <span class="bg-accent-yellow px-2 py-0.5 rounded font-bold text-[#062A1C] text-sm latin">EGP {money(p['price'])}</span>
                </div>
                <div class="flex items-center gap-2 pt-2">
                  <button type="button" aria-label="أضف إلى المفضلة"
                          class="place-items-center grid hover:bg-interaction-base border border-neutral-divider rounded-full text-cta transition-colors shrink-0 size-11">{ICON['heart']}</button>
                  <button type="button" data-add-to-cart
                          class="flex-1 bg-cta hover:bg-cta-hover py-3 rounded-full font-semibold text-white text-sm transition-colors">اضف الى السلة</button>
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
          <span class="relative bg-beige rounded-full w-[220px] xl:w-[250px] h-[220px] xl:h-[250px] overflow-hidden transition-transform group-hover:scale-[1.03] duration-300">
            <img src="{e(cat['image'])}" alt="{e(name)}" class="w-full h-full object-cover" loading="lazy" />
          </span>
          <span class="flex flex-col gap-1">
            <span class="font-bold text-[#062A1C] group-hover:text-primary text-2xl xl:text-3xl transition-colors">{e(name)}</span>
            <span class="font-medium text-neutral-secondary text-base xl:text-xl">تشكيلة متنوعة تبدا من <span class="latin">17</span> جنية</span>
          </span>
        </a>"""


def review_card(name, city, text, score="4.8"):
    """Rating uses hearts, per the Figma 'Icon/ Heart' rating component."""
    hearts = "".join(f'<span class="text-accent-yellow">{ICON["heart_full"]}</span>' for _ in range(5))
    return f"""
          <article class="flex flex-col gap-4">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-[#062A1C] text-base latin">{e(score)}</span>
              <span class="flex items-center gap-0.5">{hearts}</span>
            </div>
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
          <div class="flex flex-col flex-1 gap-2 p-6 xl:p-8">
            <span class="font-semibold text-primary text-sm">{e(tag)}</span>
            <h3 class="font-bold text-[#062A1C] text-xl xl:text-2xl leading-8">{e(heading)}</h3>
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
def page(title_text, description, body, page_id, path, main_class="overflow-x-hidden"):
    """
    Standard document shell. Header, footer and overlays are mount points
    filled at runtime by scripts.js, so chrome changes need no rebuild.
    """
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{e(title_text)}</title>
    <meta name="description" content="{e(description)}" />
    <!-- Tailwind (Play CDN) + Abu Auf design system -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="tw-config.js"></script>
    <link rel="stylesheet" href="styles.css" />
    <link rel="icon" href="images/abuauf/brand/logo-abuauf-white.svg" />
    <script defer src="scripts.js"></script>
  </head>
  <body data-page="{e(page_id)}" data-path="{e(path)}" class="antialiased bg-white">
    <!-- Shared header is injected here by scripts.js -->
    <div id="site-header"></div>

    <main class="{main_class}">{body}
    </main>

    <!-- Shared footer is injected here by scripts.js -->
    <div id="site-footer"></div>
  </body>
</html>
"""
