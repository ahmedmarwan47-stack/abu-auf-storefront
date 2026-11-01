"""Home page — Figma node 4842:55826."""
from catalog import e, home_categories, new_arrivals, rail_products, category
from components import (
    ICON, blog_card, button, carousel, category_tile, info_card, page,
    product_card, recipe_card, review_card, section_heading,
)

SLUG = "index.html"

# New wide client banners (Ahmed, 2026-08-02). Each is ONE 3:1 image used at
# EVERY breakpoint — the earlier 1440x440-desktop / 505x680-mobile pairs are
# retired. The client's art is a self-contained 3:1 composition (product left,
# green text panel with logo + headline + trust row + CTA right), so cropping it
# to the old wide-desktop / portrait-mobile boxes lopped off the logo and the
# trust row. The slide now carries `aspect-[3/1]` at all widths and the source
# is 3:1, so object-cover shows the whole banner with zero crop — desktop ~512
# tall at the 1536 cap, a short wide strip on phones (Ahmed chose wide-on-mobile
# over separate portrait art). One image per slide, so HERO is (image, alt).
# Each hero is a desktop (3:1 wide) banner paired with a PORTRAIT mobile banner
# tailored for phones (Ahmed, 2026-08-02) — the client's own artwork, matched by
# product. The mobile files are 3:4 so they fill the phone frame edge to edge
# without the desktop banner being letterboxed into a thin strip.
#
# Each hero links to ITS OWN category, not the all-products page (Ahmed,
# 2026-08-03): coffee to its dedicated worked-example page, the rest to the
# listing pre-filtered by category hash — the same routing the nav uses
# (CATEGORY_PAGE / shop.html#<slug> in scripts.js). Pistachio is a nut, so it
# shares the nuts landing with the mixed-nuts banner. HERO is
# (desktop_img, mobile_img, alt, href).
HERO = [
    ("hero-coffee.webp", "hero-coffee-mob.webp", "قهوة طازجة تُطحن لك", "shop-category.html"),
    ("hero-pistachio.webp", "hero-pistachio-mob.webp", "فستق أمريكي محمص ومملح", "shop.html#nuts-crackers"),
    ("hero-dates.webp", "hero-dates-mob.webp", "تمور صحراوية فاخرة وطبيعية", "shop.html#dates-dried-fruits"),
    ("hero-nuts-mix.webp", "hero-nuts-mix-mob.webp", "مكسرات مشكلة فاخرة وطبيعية", "shop.html#nuts-crackers"),
]

# The film slide (Mark, 2026-11-01): a 12s 720x1280 popcorn clip, muted and
# looping in the banner, with a play button that opens it full screen WITH
# sound ([data-open="video"], the modal in scripts.js). Headline and button
# copy are the requested English, verbatim — DESIGN-NOTES §1.
#
# It is the SECOND slide on purpose: the seamless loop clones slide one, and a
# cloned film would decode the video twice more for a frame nobody sees.
#
# The clip is portrait and covers the frame at every width (Mark, 2026-11-01:
# full width, cropped). In the 3:1 desktop frame that keeps only the middle
# band of each shot; phones lose far less in their 3:4 frame. Text sits
# bottom-left and the play button top-right, placed with end/start (left and
# right in RTL). dir="ltr" goes on the headline only, to left-align it: on the
# positioned box it would flip that box's own end/start to the other side.
# data-autoplay-hold keeps the carousel on this slide until the clip has
# played through once (initCarousel autoplay).
FILM = {
    "src": "videos/hero-film.mp4",
    "poster": "videos/hero-film-poster.webp",
    "headline": "More Popcorn Flavors, More Moods",
    "cta": "Shop Now",
    # No popcorn category exists; caramel popcorn is the closest landing.
    "href": "product-1331.html",
}


def _film_slide():
    f = FILM
    return f"""
              <div class="carousel-slide w-full">
                <div class="relative bg-[#1b1b1b] rounded-[20px] md:rounded-none w-full md:aspect-[3/1] aspect-[3/4] overflow-hidden hero-film">
                  <video class="block w-full h-full object-cover" data-autoplay-hold
                         src="{f['src']}" poster="{f['poster']}" autoplay muted loop playsinline
                         preload="metadata" aria-hidden="true" tabindex="-1"></video>
                  <div class="absolute inset-0 hero-film__scrim" aria-hidden="true"></div>
                  <button type="button" data-open="video" data-video-src="{f['src']}"
                          class="top-4 md:top-6 start-4 md:start-6 absolute place-items-center grid bg-white/90 hover:bg-white shadow-custom3 rounded-full text-cta transition btn-elevate size-14 md:size-16"
                          aria-label="تشغيل الفيديو بالصوت">
                    <span class="size-6 md:size-7">{ICON['play']}</span>
                  </button>
                  <div class="bottom-6 md:bottom-12 absolute flex flex-col items-end gap-4 md:gap-5 end-5 md:end-16 start-5 md:start-auto max-w-[520px] md:max-w-none" lang="en">
                    <p dir="ltr" class="w-full font-bold text-white text-3xl md:text-5xl leading-tight latin hero-film__headline">{_film_headline(f['headline'])}</p>
                    <a href="{f['href']}" class="inline-flex items-center gap-2 bg-white hover:bg-beige px-7 py-3 rounded-full min-h-11 font-semibold text-[#062A1C] text-base transition-colors latin btn-elevate">
                      {e(f['cta'])}
                    </a>
                  </div>
                </div>
              </div>"""


def _film_headline(text):
    """Break after the comma, so "Flavors," ends line one (Mark, 2026-11-01).
    From md the first line is nowrap and the box drops its width cap, so it
    can never break before "Flavors"; a phone may still wrap inside it."""
    first, _, rest = text.partition(", ")
    if not rest:
        return e(text)
    return f'<span class="md:whitespace-nowrap">{e(first)},</span><br>{e(rest)}'


def _with_film_slide(slides_html):
    """Insert the film as slide two (see FILM for why not slide one)."""
    marker = '<div class="carousel-slide w-full">'
    first_end = slides_html.find(marker, slides_html.find(marker) + 1)
    return slides_html[:first_end] + _film_slide().lstrip("\n") + "\n" + slides_html[first_end:]


CATEGORY_ORDER = [
    ("Dates & Dried Fruits", "التمور والفواكه المجففة"),
    ("Nuts | Seeds & Crackers", "المكسرات"),
    ("Coffee & Beverages", "القهوة"),
    ("Spices", "البهارات والزيوت"),
    ("Snacks", "الوجبات صحية"),
    ("Gifting & Sharing", "الهدايا"),
]

# Gifts section copy (Ahmed, 2026-08-06) — the banner used to carry a single
# tagline and a 2×2 grid of unrelated product-spread photos (snacks, pretzels,
# coffee), none of them gift-specific. It now leads with a proper intro
# paragraph, three benefit rows and a strip of occasion chips, so the section
# reads as an actual pitch for the gifting range rather than a bare headline.
# All in-house Arabic, unsigned like every other string we wrote — flagged in
# DESIGN-NOTES. Nothing here asserts a product claim; it restates the range
# (dates/nuts/dried-fruit boxes) and the site-wide delivery promise.
GIFT_INTRO = "من علب التمور وصواني المكسرات وبوكسات المناسبات — بتغليف أنيق وتوصيل لكل محافظات مصر."

# (3D icon file, heading) — the pre-rendered 3D icons in images/abuauf/icons,
# the same client render family used on the product spec row and the account
# cards (Ahmed, 2026-08-06). spec-delivery is the green scooter carrying a
# gift, which reads for both the range and the delivery line.
GIFT_FEATURES = [
    ("spec-shield.png", "تغليف فخم جاهز للإهداء"),
    ("spec-leaf.png", "تشكيلة مختارة بعناية"),
    ("spec-delivery.png", "توصيل لكل محافظات مصر"),
]

GIFT_OCCASIONS = ["رمضان", "الأعياد", "المناسبات", "التخرّج", "شكراً"]

REVIEWS = [
    ("منى عبد الله", "القاهرة",
     "التمور والمكسرات دايماً طازة وجودتها ثابتة، وبيوصلوا بسرعة. أبو عوف بقى جزء أساسي من تسوق البيت عندنا."),
    ("أحمد فؤاد", "الجيزة",
     "القهوة التركي بتاعتهم أحلى حاجة جربتها، والطحن بيكون مظبوط على حسب طلبك. التغليف كمان بيحافظ على الريحة."),
    ("سارة محمود", "الإسكندرية",
     "طلبت هدايا لمناسبة عائلية والتغليف كان شيك جداً. الأسعار كويسة مقارنة بالجودة اللي بتاخدها."),
    ("كريم سمير", "المنصورة",
     "بحب قسم السناكس الصحية، فيه اختيارات كتير للأطفال واللانش بوكس. الخدمة سريعة والفروع منتشرة."),
]

BLOG = [
    ("images/abuauf/site/1-2.webp", "نصائح", "فوائد المكسرات النيئة لصحة القلب",
     "المكسرات مصدر غني بالدهون الصحية والألياف، وإضافتها لنظامك اليومي أسهل مما تتخيل."),
    ("images/abuauf/site/2-1.webp", "قهوة", "دليلك لاختيار درجة تحميص القهوة",
     "من التحميص الفاتح للغامق، كل درجة ليها طابع مختلف. تعرف على الفرق واختار اللي يناسب ذوقك."),
    ("images/abuauf/site/3-1.webp", "تغذية", "التمور: طاقة طبيعية في كل قطعة",
     "التمور مش بس حلوة المذاق، ده كمان مصدر سريع للطاقة وغنية بالبوتاسيوم والألياف."),
]

RECIPES = [
    ("images/abuauf/site/4-1-1.webp", "مخبوزات", "جرانولا بار بالتمر والمكسرات",
     "مخبوزات الطازة هي أحلى أختيار لنقنقة سريعة او لافكار لذيذة في اللانش بوكس، اختار النوع اللي تحبه.", 25),
    ("images/abuauf/site/big.webp", "مشروبات", "قهوة مثلجة بزبدة الفول السوداني",
     "وصفة سريعة تجمع بين القهوة المطحونة الطازة وزبدة الفول السوداني لمشروب غني ومنعش.", 10),
]

ABOUT_COPY = (
    "تأسست شركة أبو عوف في عام 2010 وأصبحت من أشهر الأسماء في الأسواق لتقديم منتجات القهوة "
    "الطبيعية عالية الجودة والمكسرات وزبد المكسرات والأطعمة الصحية والفاكهة المجففة.. وأكثر. "
    "فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل خطوة في عملية الإنتاج "
    "في أبو عوف تُدار بعناية لضمان إنتاج منتجات عالية الجودة يتم توصيلها بحب وملئها بالمكونات "
    "المغذية من الطبيعة الأم."
)

RAILS = [
    ("best", "الأكثر مبيعاً", ("Best Selling", "Nuts | Seeds & Crackers")),
    ("new", "وصل حديثاً", ("New Arrivals", "Coffee & Beverages")),
    ("offers", "العروض والخصومات", ("Offers & Promotions",)),
]


def build():
    hero_slides = "".join(
        f"""
              <div class="carousel-slide w-full">
                <a href="{href}" class="block relative rounded-[20px] md:rounded-none w-full overflow-hidden">
                  <picture>
                    <source media="(min-width: 768px)" srcset="images/abuauf/site/{d}" />
                    <img src="images/abuauf/site/{m}" alt="{e(alt)}"
                         class="w-full md:aspect-[3/1] aspect-[3/4] object-cover"{' loading="lazy"' if i else ''} />
                  </picture>
                </a>
              </div>"""
        for i, (d, m, alt, href) in enumerate(HERO)
    )
    hero_slides = _with_film_slide(hero_slides)

    tiles = "".join(
        category_tile(category(api), label)
        for api, label in CATEGORY_ORDER
        if category(api)
    )

    tab_btns = "".join(
        f'<button type="button" class="tab-btn{" is-active" if i == 0 else ""} pb-3 '
        f'font-semibold text-lg xl:text-xl" data-tab="{key}">{e(label)}</button>'
        for i, (key, label, _) in enumerate(RAILS)
    )
    tab_panels = "".join(
        f'<div class="tab-panel" data-panel="{key}"{"" if i == 0 else " hidden"}>'
        f'{carousel("".join(product_card(p) for p in rail_products(*cats)))}</div>'
        for i, (key, _, cats) in enumerate(RAILS)
    )

    body = f"""
      <!-- ============================== HERO ============================== -->
      <section class="bg-white pt-4 md:pt-0 w-full">
        <!-- The hero is banner artwork, so the home page had no h1 at all and
             its outline started at h2. Screen readers and search engines both
             read the h1 as the page's name, so it is given here rather than
             painted — the visible identity is the masthead logo. -->
        <h1 class="sr-only">أبو عوف — قهوة ومكسرات وتمور وسناكس صحية</h1>
        <!-- From md up the hero is full bleed, flush under the nav, with
             square corners: 640px tall at 1920 against ~500 inside the
             1536 cap. It stays at the art's own 3:1 - every banner's CTA
             runs to within ~40px of its right edge, so any taller box
             (object-cover trims the sides) cuts the button off. Taller
             needs taller art from the client. Phones keep the gutter and
             the portrait art. -->
        <div class="mx-auto px-4 md:px-0 max-w-[1536px] md:max-w-none">
          <div class="relative carousel hero-banners" data-autoplay data-carousel-seamless style="--carousel-gap:16px">
            <div class="carousel-track">{hero_slides}
            </div>
            <!-- Offset is set in styles.css, scoped to .hero-banners. The arrows
                 used to straddle the banner's side border; with the hero full
                 bleed that border is the screen edge, so they now sit inside
                 it. A start/end utility here would tie on specificity with the
                 global .carousel-prev and lose on source order. -->
            <button type="button" class="hidden md:grid top-1/2 absolute place-items-center bg-white/90 hover:bg-white shadow-custom3 -translate-y-1/2 rounded-full text-cta transition size-16 carousel-prev" aria-label="السابق">
              <span class="rtl:scale-flip">{ICON['arrow']}</span>
            </button>
            <button type="button" class="hidden md:grid top-1/2 absolute place-items-center bg-white/90 hover:bg-white shadow-custom3 -translate-y-1/2 rounded-full text-cta transition size-16 carousel-next" aria-label="التالي">
              <span class="ltr:scale-flip">{ICON['arrow']}</span>
            </button>
            <div class="flex justify-center mt-4 carousel-dots"></div>
          </div>
        </div>
      </section>

      <!-- ========================= SHOP BY CATEGORY ========================= -->
      <section data-reveal class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق منتجاتنا", centered=True)}
          <!-- TWO per row on mobile (Ahmed, 2026-08-02). The old one-per-row was
               forced because the tiles were a FIXED 220px and two of those clip
               at 375px. They are now FLUID below sm (`w-full` + `aspect-square`
               in category_tile), so two share the row via `grid-cols-2` 1fr
               tracks and shrink to fit any phone; gap-x is tightened to match. -->
          <!-- From sm up the columns go back to content-width (`repeat(N,auto)`)
               so the tiles sit at their fixed 220/250 and the group is centred
               with gap-x AS the gap — NOT 1fr tracks, which filled max-w-[1536px]
               and left ~240px of air between the tiles (Ahmed cut that once). -->
          <!-- justify-items-center centres each fixed tile inside its auto track
               on sm+; on mobile the fluid tile fills its 1fr track, so it is a
               no-op there. -->
          <div class="justify-center justify-items-center gap-x-4 sm:gap-x-16 gap-y-8 sm:gap-y-12 grid grid-cols-2 sm:grid-cols-[repeat(2,auto)] lg:grid-cols-[repeat(3,auto)]">{tiles}
          </div>
        </div>
      </section>

      <!-- =========================== PRODUCT RAILS =========================== -->
      <section data-reveal class="bg-white py-8 xl:py-12">
        <div class="mx-auto px-4 max-w-[1536px]" data-tabs>
          <div class="flex justify-center gap-8 xl:gap-12 mb-10 border-neutral-divider border-b">{tab_btns}</div>
{tab_panels}
        </div>
      </section>

      <!-- ============================ GIFTS BANNER ============================
           Copy-led pitch for the gifting range (Ahmed, 2026-08-06): occasion
           chips as an eyebrow, then the title, a short intro, three icon-only
           benefit rows and the CTA; a single ISOLATED gift image fills the
           wider grid track opposite, in place of the old 2×2 grid of
           unrelated product-spread photos.

           Ordering: copy is DOM-first so it takes the RTL-right column at lg;
           the image is second, so it takes the left. On mobile the order is
           flipped with `order-*` so the gift image leads and the copy follows,
           which reads better than a headline over a blank column. -->
      <section data-reveal class="py-8 xl:py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="items-center gap-6 xl:gap-10 grid lg:grid-cols-[1fr_auto] xl:grid-cols-[1fr_570px] bg-beige px-6 xl:px-12 py-8 xl:py-10 rounded-[20px]">
            <div class="flex flex-col gap-5 order-2 lg:order-1">
              <div class="flex flex-wrap gap-2">{"".join(f'''
                <span class="bg-white/70 px-3 py-1 rounded-full font-medium text-primary text-xs">{e(o)}</span>''' for o in GIFT_OCCASIONS)}
              </div>
              <h2 class="font-bold text-[#062A1C] text-4xl xl:text-6xl leading-tight">الهدايا والمناسبات</h2>
              <p class="max-w-xl text-neutral-800 text-base xl:text-lg leading-8">{e(GIFT_INTRO)}</p>
              <ul class="flex flex-col gap-3 mt-1">{"".join(f'''
                <li class="flex items-center gap-2.5">
                  <img src="images/abuauf/icons/{ic}" alt="" class="size-9 xl:size-10 object-contain shrink-0" loading="lazy" />
                  <p class="font-semibold text-[#062A1C] text-sm xl:text-base">{e(t)}</p>
                </li>''' for ic, t in GIFT_FEATURES)}
              </ul>
              {button("تسوق الهدايا", "shop-category.html", "primary", "lg", "mt-3 self-start")}
            </div>
            <!-- At xl the photo column is a fixed 570px wide track and the
                 wrapper stretches to the row height (= copy height, since the
                 card no longer sets a fixed h — that was clipping the CTA).
                 img `h-full w-full object-contain` fits the 3:2 source inside
                 that 570×row_h box; when the copy runs taller than 380px the
                 photo shows small beige stripes above and below rather than
                 being cropped or distorted. The explicit column width is
                 required because a height-driven img has no intrinsic width
                 and a plain `auto` track would collapse to 0. Below xl the
                 photo is width-driven with a cap so the copy column keeps
                 room. -->
            <div class="flex justify-center items-center order-1 lg:order-2 xl:self-stretch">
              <img src="images/abuauf/site/gifts-isolated.d86d0c74.webp"
                   alt="تشكيلة هدايا أبو عوف — شنطة هدايا بشريطة ذهبية تضم مكسرات وزبدة فول سوداني وفواكه مجففة وتمور"
                   class="mx-auto w-full max-w-[640px] lg:max-w-[560px] xl:max-w-none xl:h-full xl:w-full object-contain" loading="lazy" />
            </div>
          </div>
        </div>
      </section>

      <!-- =========================== NEW ARRIVALS ===========================
           Sits below the gifts banner at Ahmed's request (2026-09-13), in the
           same shape as the product page's recommendation rail: a heading and a
           carousel of the standard product_card().

           The products are the client's OWN "New Arrivals" category, not a
           proxy — `وصل حديثاً` elsewhere on this site sorts by id because there
           is no publish-date field, but this category genuinely exists in their
           taxonomy and these four products genuinely sit in it.

           Only FOUR of them are in our scrape (their live category counts
           130) — not enough to fill a desktop row or give the carousel anything
           to scroll. `new_arrivals()` puts those four first and TOPS THE RAIL UP
           so the component can be exercised at all (Ahmed, 2026-09-13: "just add
           more products to test the carousel").

           The fill is ordered by descending id, the same proxy
           `_listing.py`'s "وصل حديثاً" sort already uses, because no
           publish-date field exists anywhere in the client's data. So the first
           four are the client calling them new and the rest is our inference —
           a re-scrape of the full category replaces it. See DESIGN-NOTES §1. -->
      <section data-reveal class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("وصل حديثاً", "تسوق الكل", "shop.html")}
          {carousel("".join(product_card(x) for x in new_arrivals()))}
        </div>
      </section>

      <!-- ============================== REVIEWS ============================== -->
      <section data-reveal class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("أراء العملاء", "كل التعليقات", "#")}
          <!-- Dark cards. On mobile they scroll horizontally (narrower cards,
               a peek of the next, full-bleed to the screen edge) rather than
               stacking full-width and tall (Ahmed, 2026-08-02); from md they
               return to the 2×2 / row-of-four grid. -->
          <div class="flex md:grid gap-4 xl:gap-8 md:grid-cols-2 xl:grid-cols-4 -mx-4 px-4 md:mx-0 md:px-0 overflow-x-auto md:overflow-visible no-scrollbar snap-x">{"".join(review_card(*r) for r in REVIEWS)}
          </div>
        </div>
      </section>

      <!-- =============================== ABOUT =============================== -->
      <section data-reveal class="bg-primary text-white">
        <div class="items-center grid lg:grid-cols-2 mx-auto max-w-[1536px]">
          <!-- Two-line heading (Ahmed, 2026-10-07). The old xl:ps-[190px] left
               a 498px column at 1686 and the first half of the title alone
               measures 570px at 48px, so it broke into three. The start inset
               is now the page container's own 16px (the copy lines up with
               the header's edge) and the end gap 40px, which leaves 584px at
               1280 — the narrowest xl width — and more above it. text-balance
               evens the two lines. No <br>: the i18n walk is keyed on the
               whole string as one text node. -->
          <div class="flex flex-col gap-6 px-4 xl:ps-4 xl:pe-10 py-12 xl:py-20">
            <p class="font-semibold text-accent-yellow text-lg xl:text-xl">عن أبو عوف</p>
            <h2 class="font-bold text-3xl xl:text-5xl text-balance leading-tight">نحن نغير مفهوم الأكل الصحي في جميع أنحاء العالم</h2>
            <p class="text-white/80 text-base xl:text-lg leading-8">{e(ABOUT_COPY)}</p>
            {button("اعرف المزيد", "#", "accent", "lg", "mt-2 self-start")}
          </div>
          <div class="lg:order-first h-[320px] lg:h-full min-h-[420px]">
            <img src="images/abuauf/site/About-Homepage.webp" alt="فرع أبو عوف" class="w-full h-full object-cover" loading="lazy" />
          </div>
        </div>
      </section>

      <!-- =============================== BLOG =============================== -->
      <section data-reveal class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("آخر الأخبار", "كل المقالات", "blogs.html")}
          <div class="gap-6 xl:gap-8 grid md:grid-cols-2 lg:grid-cols-3">{"".join(blog_card(*b) for b in BLOG)}
          </div>
        </div>
      </section>

      <!-- ============================== RECIPES ============================== -->
      <section data-reveal class="bg-interaction-base py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("أشهي الوصفات من أبو عوف")}
          <div class="gap-6 xl:gap-8 grid lg:grid-cols-2">{"".join(recipe_card(*r) for r in RECIPES)}
          </div>
          <div class="flex justify-center mt-10">{button("كل الوصفات", "blogs.html")}</div>
        </div>
      </section>

      <!-- ========================== BRANCHES / EXPORT ========================== -->
      <section data-reveal class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="gap-6 xl:gap-12 grid lg:grid-cols-2">
{info_card("images/abuauf/site/pick-up.webp", "فروع أبو عوف",
           'يوجد أكثر من <span class="latin">150</span> فرع أبو عوف في مصر, أكتشف الأقرب اليك',
           "اكتشف الفروع", "#")}
{info_card("images/abuauf/site/Abu-Auf-flags.webp", "منتجات أبو عوف خارج مصر",
           "ما بين أسواق أوروبا، آسيا، أمريكا و الوطن العربي",
           "اعرف أكثر", "#", "w-[168px] h-[100px]")}
          </div>
        </div>
      </section>"""

    return page(
        "أبو عوف — قهوة ومكسرات وتمور وسناكس صحية",
        "تسوق أونلاين من أبو عوف: قهوة طازة، مكسرات، تمور وفواكه مجففة، سناكس صحية، "
        "بهارات وهدايا — بأفضل الأسعار وتوصيل لكل مصر.",
        body, "home", "/",
    )
