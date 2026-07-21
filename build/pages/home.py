"""Home page — Figma node 4842:55826."""
from catalog import e, home_categories, rail_products, category
from components import (
    ICON, blog_card, button, carousel, category_tile, info_card, page,
    product_card, recipe_card, review_card, section_heading,
)

SLUG = "index.html"

# 1440x440 desktop / 505x680 mobile pairs — the real Arabic storefront banners.
HERO = [
    ("coffee-web-A1.webp", "coffee.-A.webp", "قهوة تركي بالتوت — جديد من أبو عوف"),
    ("Madjool-web-AR.webp", "Madjool-mob-AR.webp", "تمور المجدول الفاخرة"),
    ("ps-web-A-600.webp", "ps-mobile-A-600.webp", "تشكيلة أبو عوف المميزة"),
    ("UAE-Abuauf-desktop-Ar.webp", "Dubai-hero-mobile-Ar.webp", "أبو عوف الآن في الإمارات"),
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
                  <picture>
                    <source media="(min-width: 768px)" srcset="images/abuauf/site/{d}" />
                    <img src="images/abuauf/site/{m}" alt="{e(alt)}"
                         class="w-full md:aspect-[1440/440] aspect-[505/680] object-cover"{' loading="lazy"' if i else ''} />
                  </picture>
                </a>
              </div>"""
        for i, (d, m, alt) in enumerate(HERO)
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
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="relative carousel hero-banners" data-autoplay style="--carousel-gap:16px">
            <div class="carousel-track">{hero_slides}
            </div>
            <button type="button" class="hidden md:grid top-1/2 start-6 absolute place-items-center bg-white/90 hover:bg-white shadow-custom3 -translate-y-1/2 rounded-full text-cta transition size-16 carousel-prev" aria-label="السابق">
              <span class="rtl:scale-flip">{ICON['arrow']}</span>
            </button>
            <button type="button" class="hidden md:grid top-1/2 end-6 absolute place-items-center bg-white/90 hover:bg-white shadow-custom3 -translate-y-1/2 rounded-full text-cta transition size-16 carousel-next" aria-label="التالي">
              <span class="ltr:scale-flip">{ICON['arrow']}</span>
            </button>
            <div class="flex justify-center gap-2 mt-4 carousel-dots"></div>
          </div>
        </div>
      </section>

      <!-- ========================= SHOP BY CATEGORY ========================= -->
      <section class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق منتجاتنا", centered=True)}
          <!-- The Figma mobile home (2595:60104) stacks these one per row; the
               tiles are 220px wide, so forcing two columns at 375px clipped
               30px off each. One column below sm, two from sm. -->
          <div class="gap-x-6 gap-y-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 justify-items-center">{tiles}
          </div>
        </div>
      </section>

      <!-- =========================== PRODUCT RAILS =========================== -->
      <section class="bg-white py-8 xl:py-12">
        <div class="mx-auto px-4 max-w-[1536px]" data-tabs>
          <div class="flex justify-center gap-8 xl:gap-12 mb-10 border-neutral-divider border-b">{tab_btns}</div>
{tab_panels}
        </div>
      </section>

      <!-- ============================ GIFTS BANNER ============================ -->
      <section class="py-8 xl:py-12">
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
      <section class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("أراء العملاء", "كل التعليقات", "faqs.html")}
          <div class="gap-x-24 gap-y-12 grid md:grid-cols-2">{"".join(review_card(*r) for r in REVIEWS)}
          </div>
        </div>
      </section>

      <!-- =============================== ABOUT =============================== -->
      <section class="bg-primary text-white">
        <div class="items-center grid lg:grid-cols-2 mx-auto max-w-[1536px]">
          <div class="flex flex-col gap-6 px-4 xl:ps-[190px] xl:pe-20 py-12 xl:py-20">
            <p class="font-semibold text-accent-yellow text-lg xl:text-xl">عن أبو عوف</p>
            <h2 class="font-bold text-3xl xl:text-5xl leading-tight">نحن نغير مفهوم الأكل الصحي في جميع أنحاء العالم</h2>
            <p class="text-white/80 text-base xl:text-lg leading-8">{e(ABOUT_COPY)}</p>
            {button("اعرف المزيد", "about.html", "accent", "lg", "mt-2 self-start")}
          </div>
          <div class="lg:order-first h-[320px] lg:h-full min-h-[420px]">
            <img src="images/abuauf/site/About-Homepage.webp" alt="فرع أبو عوف" class="w-full h-full object-cover" loading="lazy" />
          </div>
        </div>
      </section>

      <!-- =============================== BLOG =============================== -->
      <section class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("آخر الأخبار", "كل المقالات", "blogs.html")}
          <div class="gap-6 xl:gap-8 grid md:grid-cols-2 lg:grid-cols-3">{"".join(blog_card(*b) for b in BLOG)}
          </div>
        </div>
      </section>

      <!-- ============================== RECIPES ============================== -->
      <section class="bg-interaction-base py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("أشهي الوصفات من أبو عوف")}
          <div class="gap-6 xl:gap-8 grid lg:grid-cols-2">{"".join(recipe_card(*r) for r in RECIPES)}
          </div>
          <div class="flex justify-center mt-10">{button("كل الوصفات", "blogs.html")}</div>
        </div>
      </section>

      <!-- ========================== BRANCHES / EXPORT ========================== -->
      <section class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="gap-6 xl:gap-12 grid lg:grid-cols-2">
{info_card("images/abuauf/site/pick-up.webp", "فروع أبو عوف",
           'يوجد أكثر من <span class="latin">150</span> فرع أبو عوف في مصر, أكتشف الأقرب اليك',
           "اكتشف الفروع", "branches.html")}
{info_card("images/abuauf/site/Abu-Auf-flags.webp", "منتجات أبو عوف خارج مصر",
           "ما بين أسواق أوروبا، آسيا، أمريكا و الوطن العربي",
           "اعرف أكثر", "about.html", "w-[168px] h-[100px]")}
          </div>
        </div>
      </section>"""

    return page(
        "أبو عوف — قهوة ومكسرات وتمور وسناكس صحية",
        "تسوق أونلاين من أبو عوف: قهوة طازة، مكسرات، تمور وفواكه مجففة، سناكس صحية، "
        "بهارات وهدايا — بأفضل الأسعار وتوصيل لكل مصر.",
        body, "home", "/",
    )
