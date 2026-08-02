"""Home page — Figma node 4842:55826."""
from catalog import e, home_categories, rail_products, category
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
HERO = [
    ("hero-coffee.webp", "قهوة طازجة تُطحن لك"),
    ("hero-pistachio.webp", "فستق أمريكي محمص ومملح"),
    ("hero-dates.webp", "تمور صحراوية فاخرة وطبيعية"),
    ("hero-nuts-mix.webp", "مكسرات مشكلة فاخرة وطبيعية"),
]

CATEGORY_ORDER = [
    ("Dates & Dried Fruits", "التمور والفواكه المجففة"),
    ("Nuts | Seeds & Crackers", "المكسرات"),
    ("Coffee & Beverages", "القهوة"),
    ("Spices", "البهارات والزيوت"),
    ("Snacks", "الوجبات صحية"),
    ("Gifting & Sharing", "الهدايا"),
]

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
                <a href="shop.html" class="block relative rounded-[20px] w-full overflow-hidden">
                  <img src="images/abuauf/site/{img}" alt="{e(alt)}"
                       class="w-full aspect-[3/1] object-cover"{' loading="lazy"' if i else ''} />
                </a>
              </div>"""
        for i, (img, alt) in enumerate(HERO)
    )

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
      <section class="bg-white pt-4 md:pt-6 w-full">
        <!-- The hero is banner artwork, so the home page had no h1 at all and
             its outline started at h2. Screen readers and search engines both
             read the h1 as the page's name, so it is given here rather than
             painted — the visible identity is the masthead logo. -->
        <h1 class="sr-only">أبو عوف — قهوة ومكسرات وتمور وسناكس صحية</h1>
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="relative carousel hero-banners" data-autoplay data-carousel-seamless style="--carousel-gap:16px">
            <div class="carousel-track">{hero_slides}
            </div>
            <!-- Offset is set in styles.css, scoped to .hero-banners: the 64px
                 circle is pulled out by half its width so its centre lands ON the
                 banner's side border (Ahmed, 2026-07-29 — "in the middle of the
                 border"). A start/end utility here would tie on specificity with
                 the global .carousel-prev -10px and lose on source order. -->
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

      <!-- ============================ GIFTS BANNER ============================ -->
      <section data-reveal class="py-8 xl:py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="items-center gap-8 grid lg:grid-cols-2 bg-beige px-6 xl:px-12 py-10 xl:py-0 rounded-[20px] overflow-hidden">
            <div class="flex flex-col gap-4 py-0 xl:py-16">
              <p class="font-semibold text-primary text-lg xl:text-xl">خصم يصل إلى <span class="latin">20٪</span> على قسم</p>
              <h2 class="font-bold text-[#062A1C] text-4xl xl:text-6xl leading-tight">الهدايا</h2>
              <p class="text-neutral-800 text-base xl:text-xl leading-8">اعثر على الهدية المثالية لكل شخص وكل مناسبة</p>
              {button("تسوق الهدايا", "shop-category.html", "primary", "lg", "mt-2 self-start")}
            </div>
            <div class="gap-3 grid grid-cols-2 self-stretch py-8">
              <img src="images/abuauf/site/1-2.webp" alt="" class="rounded-xl w-full h-full object-cover" loading="lazy" />
              <img src="images/abuauf/site/2-1.webp" alt="" class="rounded-xl w-full h-full object-cover" loading="lazy" />
              <img src="images/abuauf/site/3-1.webp" alt="" class="rounded-xl w-full h-full object-cover" loading="lazy" />
              <img src="images/abuauf/site/4-1-1.webp" alt="" class="rounded-xl w-full h-full object-cover" loading="lazy" />
            </div>
          </div>
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
          <div class="flex flex-col gap-6 px-4 xl:ps-[190px] xl:pe-20 py-12 xl:py-20">
            <p class="font-semibold text-accent-yellow text-lg xl:text-xl">عن أبو عوف</p>
            <h2 class="font-bold text-3xl xl:text-5xl leading-tight">نحن نغير مفهوم الأكل الصحي في جميع أنحاء العالم</h2>
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
