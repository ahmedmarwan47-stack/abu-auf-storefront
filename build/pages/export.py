"""
Export services — content scraped verbatim from the live abuauf.com/export.

The nav has always linked to /export; before this page existed the route fell
through to index.html, so tapping "منتجات أبو عوف خارج مصر" silently returned
you to the homepage.

Every string and image here is the client's own, taken from the live page —
nothing on this page is written in-house. Contrast with rewards.py, whose live
counterpart is still lorem ipsum.
"""
from components import page, page_header

SLUG = "export.html"

INTRO_HEADING = "ما بين أسواق أوروبا، آسيا، أمريكا و الوطن العربي"
INTRO_BODY = (
    "اتجهت شركة \"أبوعوف\" للتصدير إلى الأسواق العالمية، ما بين الأسواق الأوروبية "
    "والأسيوية والأمريكية بالإضافة إلى الأسواق العربية. اهتمت الشركة بمراعاة متطلبات "
    "كل سوق على حدة و تلبية احتياجات العملاء، و ذلك بالتواصل المستمر مع الأسواق "
    "الخارجية والتواجد بالمعارض العالمية. تمكنت شركة \"أبوعوف\" من الانتشار في الأسواق "
    "الخارجية والتي تضم مختلف الدول. وتسعى شركة \"أبوعوف\" للتوسع في باقي الأسواق."
)

B2B_HEADING = "رصيد ثقة كافي نتيجة نجاحنا مع شركائنا"
B2B_BODY = (
    "ثقة عملاء شركة \"أبو عوف\" وتجاربهم المتميزة دفعتها إلى تلبية احتياجات السوق "
    "المتزايدة، لذلك لديهم الآن قسم خاص بتوريد الطلبات بكميات كبيرة للشركات وبتواجدها "
    "بأكبر عدد ممكن من الأماكن. لدى الشركة رصيد ثقة كافي نتيجة نجاحها مع شركاء "
    "متميزين في السوق المصري من فنادق، مطاعم، كافيهات، وشركات. لذا، لا تتردد في "
    "التواصل مع الشركة. لدى الشركة أيضا فريق متخصص في التعامل المهني "
    "<span class=\"latin\">Business to Business</span> من حيث الالتزام بالمواعيد "
    "والحفاظ على جودة المنتجات والتغليف وطريقة العرض."
)

PRODUCTS_HEADING = "نصّدر الأصناف الأكثر طلباً في الأسواق العالمية"
PRODUCTS = [
    ("images/abuauf/export/export-dates.webp", "التمور المصرية"),
    ("images/abuauf/export/export-coffee.webp", "القهوة"),
    ("images/abuauf/export/export-pretzel.webp", "البريتزل"),
    ("images/abuauf/export/export-maamoul.jpg", "معمول"),
]

EXPO_HEADING = "المشاركة بالمعارض الدولية"
EXPO_BODY = (
    "يسر شركة أبو عوف أن تعلن عن مشاركتها في أبرز المعارض الدولية، تشمل هذه المشاركة "
    "معرض جلفود في الفترة من عام 2020 حتى عام 2023، ومعرض انوجا في الفترة من عام 2017 "
    "حتى عام 2019، ومعرض سيال في عام 2018، بالإضافة إلى معرض الصين الدولي للاستيراد "
    "اكسبو في عام 2019. نحن نسعى لزيادة تواجدنا في المعارض القادمة لنكون أقرب إلى "
    "عملاء جدد ولنستمر في تحقيق أهدافنا وتقديم منتجاتنا المتميزة."
)


def build():
    cards = "".join(f"""
              <figure class="flex flex-col gap-3 min-w-0">
                <img src="{src}" alt="{label}"
                     class="bg-interaction-base rounded-2xl w-full h-[220px] xl:h-[260px] object-cover"
                     loading="lazy" />
                <figcaption class="font-semibold text-[#062A1C] text-base text-center">{label}</figcaption>
              </figure>""" for src, label in PRODUCTS)

    body = f"""{page_header("خدمات التصدير", [("الرئيسية", "index.html"), ("خدمات التصدير", None)])}

      <!-- ============================ GLOBAL MARKETS ============================ -->
      <section class="py-8">
        <div class="flex flex-col gap-8 mx-auto px-4 max-w-[1536px]">
          <img src="images/abuauf/export/export-map.webp" alt="{INTRO_HEADING}"
               class="rounded-[20px] w-full object-cover" />
          <div class="flex flex-col gap-4 max-w-[900px]">
            <h2 class="font-bold text-[#062A1C] text-2xl xl:text-3xl leading-tight">{INTRO_HEADING}</h2>
            <p class="text-neutral-800 text-base xl:text-lg leading-9">{INTRO_BODY}</p>
          </div>
        </div>
      </section>

      <!-- ================================ B2B ================================ -->
      <section class="py-8">
        <div class="items-center gap-8 xl:gap-12 grid grid-cols-1 lg:grid-cols-2 mx-auto px-4 max-w-[1536px]">
          <div class="flex flex-col gap-4 min-w-0">
            <h2 class="font-bold text-[#062A1C] text-2xl xl:text-3xl leading-tight">{B2B_HEADING}</h2>
            <p class="text-neutral-800 text-base xl:text-lg leading-9">{B2B_BODY}</p>
          </div>
          <img src="images/abuauf/export/export-b2b.webp" alt="{B2B_HEADING}"
               class="order-first lg:order-none rounded-[20px] w-full object-cover" loading="lazy" />
        </div>
      </section>

      <!-- ============================== PRODUCTS ============================== -->
      <section class="py-8">
        <div class="flex flex-col gap-8 mx-auto px-4 max-w-[1536px]">
          <h2 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">{PRODUCTS_HEADING}</h2>
          <div class="gap-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">{cards}
          </div>
        </div>
      </section>

      <!-- ================================ EXPOS ================================ -->
      <section class="py-8 pb-16">
        <div class="flex flex-col gap-6 mx-auto px-4 max-w-[1536px]">
          <div class="flex flex-col gap-4 bg-interaction-base p-6 xl:p-10 rounded-[20px]">
            <div class="flex items-center gap-4">
              <img src="images/abuauf/export/export-expo.webp" alt=""
                   class="shrink-0 w-12 h-12 object-contain" loading="lazy" />
              <h2 class="font-bold text-[#062A1C] text-2xl xl:text-3xl">{EXPO_HEADING}</h2>
            </div>
            <p class="text-neutral-800 text-base xl:text-lg leading-9">{EXPO_BODY}</p>
          </div>
        </div>
      </section>"""

    return page("تصدير منتجات أبو عوف | جودة عالية وتشكيلة متنوعة",
                "أبو عوف تصدّر التمور والقهوة والبريتزل والمعمول لأسواق أوروبا وآسيا "
                "وأمريكا والوطن العربي.",
                body, "export", "/export")
