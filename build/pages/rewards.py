"""
Rewards — the nav has always linked to /rewards, but before this page existed
the route fell through to index.html, so tapping "المكافآت" silently returned
you to the homepage.

IMPORTANT, and the reason this page is thin: **the live abuauf.com/rewards is
itself unfinished.** Its H1 is real; its body copy is Arabic lorem ipsum
("لوريم سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت..."). So there is no real
copy to scrape, unlike export.py.

What is real here: the H1 and the hero image, both taken from the live page.
Everything else is deliberately minimal — the page routes honestly and links to
the account points area that already exists, rather than inventing a rewards
programme the client has not described. See DESIGN-NOTES §2.
"""
from components import button, page, page_header

SLUG = "rewards.html"

# Real, from the live page.
HEADING = "كل ما تشتري أكثر من أبوعوف هتكسب نقط و فلوس"


def build():
    body = f"""{page_header("المكافآت", [("الرئيسية", "index.html"), ("المكافآت", None)])}

      <section class="py-8">
        <div class="flex flex-col gap-8 mx-auto px-4 max-w-[1536px]">
          <img src="images/abuauf/rewards-hero.webp" alt="{HEADING}"
               class="rounded-[20px] w-full max-h-[420px] object-cover" />

          <div class="flex flex-col gap-4 max-w-[820px]">
            <h2 class="font-bold text-[#062A1C] text-2xl xl:text-3xl leading-tight">{HEADING}</h2>
            <p class="text-neutral-800 text-base xl:text-lg leading-9">
              اجمع نقاطك مع كل طلب من أبو عوف، وتابع رصيدك ومستوى عضويتك من صفحة النقاط
              في حسابك.
            </p>
          </div>

          <div class="flex flex-wrap gap-3">
            {button("نقاطي", "my-account-point.html", "primary", "md")}
            {button("محفظتي", "my-account-wallet.html", "secondary", "md")}
          </div>
        </div>
      </section>"""

    return page("المكافآت | أبو عوف",
                "اجمع نقاط مع كل طلب من أبو عوف وتابع رصيدك ومستوى عضويتك.",
                body, "rewards", "/rewards")
