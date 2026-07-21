"""About — Figma 'About' (394:24746)."""
from components import page, page_header

SLUG = "about.html"

STATS = [("2010", "سنة التأسيس"), ("316", "فرع في مصر"), ("25", "محافظة"), ("1000+", "منتج")]

BODY = [
    ("قصتنا", "تأسست شركة أبو عوف في عام 2010 وأصبحت من أشهر الأسماء في الأسواق لتقديم "
              "منتجات القهوة الطبيعية عالية الجودة والمكسرات وزبد المكسرات والأطعمة الصحية "
              "والفاكهة المجففة.. وأكثر."),
    ("جودة في كل خطوة", "فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل "
                        "خطوة في عملية الإنتاج في أبو عوف تُدار بعناية لضمان إنتاج منتجات عالية "
                        "الجودة يتم توصيلها بحب وملئها بالمكونات المغذية من الطبيعة الأم."),
    ("نغذي العقل والروح", "نعطي الأولوية لابتكار المنتجات ونأخذ في الاعتبار اتجاهات السوق ورغبات "
                          "العملاء وتغيُّر الأذواق، كما نشجع دائمًا نمط الحياة الصحي؛ لأن هدفنا ليس "
                          "فقط تغذية الجسم، بل تغذية العقل والروح أيضًا."),
]


def build():
    stats = "".join(f"""
              <div class="flex flex-col items-center gap-1 bg-interaction-base px-4 py-6 rounded-2xl text-center">
                <span class="font-bold text-primary text-3xl latin">{v}</span>
                <span class="text-neutral-secondary text-sm">{label}</span>
              </div>""" for v, label in STATS)

    sections = "".join(f"""
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#062A1C] text-xl xl:text-2xl">{h}</h2>
              <p class="text-neutral-800 text-base xl:text-lg leading-9">{p}</p>
            </div>""" for h, p in BODY)

    body = f"""{page_header("قصتنا", [("الرئيسية", "index.html"), ("قصتنا", None)])}

      <section class="py-8">
        <div class="mx-auto px-4 xl:px-[190px] max-w-[1920px]">
          <div class="rounded-[20px] overflow-hidden">
            <img src="images/abuauf/site/About-Homepage.webp" alt="فرع أبو عوف" class="w-full h-[280px] xl:h-[460px] object-cover" />
          </div>
        </div>
      </section>

      <section class="pb-10">
        <div class="gap-4 grid grid-cols-2 lg:grid-cols-4 mx-auto px-4 xl:px-[190px] max-w-[1920px]">{stats}
        </div>
      </section>

      <section class="pb-16">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[190px] max-w-[1000px]">{sections}
        </div>
      </section>"""

    return page("قصتنا | أبو عوف",
                "تعرف على قصة أبو عوف منذ 2010 — قهوة ومكسرات وأطعمة صحية عالية الجودة.",
                body, "about", "/about")
