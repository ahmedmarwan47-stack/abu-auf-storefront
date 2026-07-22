/* =====================================================================
   scripts.js — shared behaviour for the static Abu Auf build.

   Replaces the React runtime with vanilla JS:
     • Injects the shared header, footer and overlay chrome into every
       page (each page only ships a #site-header / #site-footer mount
       point, so markup stays DRY and works from the file:// protocol).
     • Re-implements the interactive pieces that were React components:
       mobile menu drawer, cart drawer, search modal, location bottom
       sheet, sticky-on-scroll navbar and mega-menu hover.
     • Provides page-level helpers: carousels (replacing Swiper),
       accordions, tabs, quantity steppers, toasts and demo forms.

   The document is Arabic-first and renders RTL. Anything that positions
   against a physical edge must use logical properties (ms/me, ps/pe,
   start/end) so it mirrors correctly.

   Menus, footer columns, socials and contact details below mirror the
   Abu Auf Figma; product data lives in data/catalog.json.
   ===================================================================== */
(function () {
  "use strict";

  /* ---------------------------------------------------------------
     Placeholder content (formerly fetched from the CMS)
     --------------------------------------------------------------- */
  /*
   * Category names and slugs are the real ones from the Abu Auf WooCommerce
   * catalog (see data/catalog.json). Arabic labels in the header nav follow
   * the Figma wording, which is occasionally shorter than the CMS category
   * name — e.g. "المكسرات" in the nav vs "مكسرات وحبوب ومقرمشات" in the grid.
   */
  const SUPPORT_MENU = [
    { title: "قصتنا", url: "/about" },
    { title: "المكافآت", url: "/rewards" },
    { title: "الفروع", url: "/branches" },
    { title: "منتجات أبو عوف خارج مصر", url: "/export" },
    { title: "البلوج", url: "/blogs" },
    { title: "سياسة التوصيل والاسترجاع", url: "/return-policy" },
    { title: "أتصل بنا", url: "/contact-us" },
  ];

  const MAIN_MENU = [
    {
      name: "العروض و الخصومات",
      url: "/shop/offers-promotions",
      icon: "images/abuauf/icons/icon-coupon.svg",
      image: "images/abuauf/categories/gifts.png",
    },
    {
      // The seasonal Christmas-tree badge that used to sit here was removed at
      // Ahmed's request. `desktopNavItem` no longer renders a badge at all.
      name: "المكسرات",
      url: "/shop/nuts-crackers",
      image: "images/abuauf/categories/Nuts.webp",
      children: [
        { name: "مكسرات نيئة", url: "/shop/raw-nuts" },
        { name: "مكسرات محمصة ومملحة", url: "/shop/roasted-salted-nuts" },
        { name: "مكسرات بنكهات", url: "/shop/flavored-nuts" },
        { name: "تشكيلة مكسرات", url: "/shop/mix-nuts" },
        { name: "حبوب ومقرمشات", url: "/shop/seeds-crackers" },
      ],
    },
    {
      name: "القهوة",
      url: "/shop/coffee-beverage",
      image: "images/abuauf/categories/Drinks-1.webp",
      children: [
        { name: "قهوة تركي", url: "/shop/turkish-coffee" },
        { name: "قهوة برازيلي", url: "/shop/brazilian-coffee" },
        { name: "قهوة مطحونة طازجة", url: "/shop/fresh-grounded-coffee" },
        { name: "إسبريسو", url: "/shop/espresso" },
        { name: "قهوة سريعة التحضير", url: "/shop/instant-coffee" },
        { name: "مشروبات ساخنة", url: "/shop/hot-drinks" },
      ],
    },
    {
      name: "التمور والفواكه المجففة",
      url: "/shop/dates-dried-fruits",
      image: "images/abuauf/categories/Dates.webp",
      children: [
        { name: "تمور", url: "/shop/dates" },
        { name: "فواكه مجففة", url: "/shop/dried-fruits" },
      ],
    },
    {
      name: "الوجبات صحية",
      url: "/shop/healthy-snacks",
      image: "images/abuauf/categories/Healthy_Snaks2.png",
      children: [
        { name: "ألواح صحية", url: "/shop/healthy-bars" },
        { name: "سناكس بروتين", url: "/shop/protein-snacks" },
        { name: "حبوب صحية", url: "/shop/healthy-grains" },
      ],
    },
    // Distinct from القهوة above: sharing a slug made both tabs read as the
    // active page at once.
    { name: "المشروبات", url: "/shop/hot-drinks" },
    { name: "البهارات والزيوت", url: "/shop/spices-kitchen-baking" },
    { name: "الهدايا", url: "/shop/gifting-seasonal" },
  ];

  /* Column order is RTL reading order: rightmost column first. */
  const FOOTER_COLUMNS = [
    {
      name: "أقسام المنتجات",
      links: [
        { title: "العروض و الخصومات", url: "/shop/offers-promotions" },
        { title: "المكسرات", url: "/shop/nuts-crackers" },
        { title: "القهوة", url: "/shop/coffee-beverage" },
        { title: "التمور والفواكه المجففة", url: "/shop/dates-dried-fruits" },
        { title: "الوجبات صحية", url: "/shop/healthy-snacks" },
        { title: "البهارات والزيوت", url: "/shop/spices-kitchen-baking" },
        { title: "الهدايا", url: "/shop/gifting-seasonal" },
      ],
    },
    {
      name: "عن الشركة",
      links: [
        { title: "قصتنا", url: "/about" },
        { title: "فروعنا", url: "/branches" },
        { title: "وصفاتنا", url: "/recipes" },
        { title: "التصدير", url: "/export" },
        { title: "الموزعين في مصر", url: "/distributors" },
        { title: "شركاء النجاح", url: "/partners" },
        { title: "فرص وظائف", url: "/careers" },
        { title: "إبداء الرأي", url: "/contact-us" },
      ],
    },
    {
      name: "المساعدة",
      links: [
        { title: "الاسئلة الشائعة", url: "/faqs" },
        { title: "تعليقات العملاء", url: "/reviews" },
        { title: "التوصيل أو الاستلام", url: "/return-policy" },
        { title: "تطبيق الجوال", url: "/app" },
        { title: "الشروط والاحكام", url: "/terms-conditions" },
        { title: "سياسة الخصوصية", url: "/privacy-policy" },
        { title: "سياسة الاسترجاع", url: "/return-policy" },
      ],
    },
  ];

  /* Contact details from the Figma footer. */
  const CONTACT = {
    hotline: "19969",
    address: "المنطقة الصناعية 31-33، التجمع الثالث، القاهرة الجديدة، مصر",
  };

  /* Real Abu Auf accounts; glyphs are the Figma social icon set. */
  const SOCIALS = [
    {
      title: "فيسبوك",
      href: "https://www.facebook.com/abuauf",
      icon: "images/abuauf/social/icon-facebook.svg",
    },
    {
      title: "انستجرام",
      href: "https://www.instagram.com/abuauf_egypt",
      icon: "images/abuauf/social/icon-instagram.svg",
    },
    {
      title: "لينكد إن",
      href: "https://www.linkedin.com/company/abu-auf",
      icon: "images/abuauf/social/icon-linkedin.svg",
    },
    {
      title: "يوتيوب",
      href: "https://www.youtube.com/@abuauf7602",
      icon: "images/abuauf/social/icon-youtube.svg",
    },
  ];

  /* ---------------------------------------------------------------
     Route → static-file mapping
     --------------------------------------------------------------- */
  /* The one category page that was actually built, by slug. */
  const CATEGORY_PAGE = { "coffee-beverage": "shop-category.html" };

  /* Sub-category slug → parent category slug, taken from the nav itself so the
     two cannot drift apart. */
  const CHILD_TO_PARENT = (function () {
    const m = {};
    MAIN_MENU.forEach(function (i) {
      const parent = (i.url || "").replace("/shop/", "");
      (i.children || []).forEach(function (c) {
        m[(c.url || "").replace("/shop/", "")] = parent;
      });
    });
    return m;
  })();

  function pageHref(url) {
    if (!url) return "#";
    if (/^https?:\/\//.test(url) || url.startsWith("#") || url.endsWith(".html"))
      return url;
    const clean = "/" + url.replace(/^\/+/, "").replace(/\/+$/, "");
    const map = {
      "/": "index.html",
      "/about": "about.html",
      "/branches": "branches.html",
      "/faqs": "faqs.html",
      "/contact-us": "contact-us.html",
      "/privacy-policy": "privacy-policy.html",
      "/terms-conditions": "terms-conditions.html",
      "/return-policy": "return-policy.html",
      "/blogs": "blogs.html",
      "/rewards": "rewards.html",
      "/export": "export.html",
      "/shop": "shop.html",
      "/cart": "cart.html",
      "/checkout": "checkout.html",
      "/thank-you": "thank-you.html",
      "/login": "login.html",
      "/register": "register.html",
      "/forget-password": "forget-password.html",
      "/reset-password": "reset-password.html",
      "/store-closed": "store-closed.html",
      "/my-account": "my-account.html",
    };
    if (map[clean]) return map[clean];
    /*
     * Category routes. Only one category page exists — shop-category.html, the
     * Figma Collection worked example for coffee — and every /shop/<slug> used
     * to resolve to it, so tapping "المكسرات" in the nav landed you on coffee.
     * Real category slugs now open the listing filtered to that category.
     * Sub-category slugs have no field in catalog.json, so they fall back to
     * their parent, which MAIN_MENU already records.
     */
    if (clean.startsWith("/shop/")) {
      let slug = clean.slice("/shop/".length);
      if (CHILD_TO_PARENT[slug]) slug = CHILD_TO_PARENT[slug];
      return CATEGORY_PAGE[slug] || "shop.html#" + slug;
    }
    if (clean.startsWith("/products/")) return "product.html";
    if (clean.startsWith("/blogs/")) return "blog.html";
    if (clean.startsWith("/my-account/"))
      return "my-account-" + clean.split("/")[2] + ".html";
    return "index.html";
  }

  const esc = (s) =>
    String(s == null ? "" : s).replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );

  /* ---------------------------------------------------------------
     SVG icons (ported from the React icon components)

     Every glyph is `w-full h-full` and paints in `currentColor`, so **the
     wrapper decides the size and the colour** — one rule, no surprises.

     They used to carry their own `w-4`/`w-5`/`w-6`, which silently fought the
     wrapper: the masthead chevrons sat in a `w-6 h-6` span but drew at 16px,
     and the breadcrumb arrows drew at 20px inside a 16px box and overflowed
     it. `menu` was worse — hardcoded `width="31" height="30"` and
     `stroke="white"`, so it ignored both.
     --------------------------------------------------------------- */
  const ICON = {
    account:
      '<svg viewBox="0 0 29 29" fill="none" class="w-full h-full"><path d="M4.47 22.96C7.43 21.29 10.85 20.33 14.5 20.33s7.07.96 10.03 2.63M18.88 11.58a4.38 4.38 0 1 1-8.75 0 4.38 4.38 0 0 1 8.75 0ZM27.63 14.5A13.13 13.13 0 1 1 1.38 14.5a13.13 13.13 0 0 1 26.25 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    search:
      '<svg viewBox="0 0 29 29" fill="none" class="w-full h-full"><path d="M27.63 27.63 18.88 18.88M21.79 11.58a10.21 10.21 0 1 1-20.42 0 10.21 10.21 0 0 1 20.42 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    location:
      '<svg viewBox="0 0 22 20" fill="none" class="w-full h-full"><path d="M16.75 11.75c-3 0-4 2-4 2h-3l-.14-.22c-.86-1.35-1.29-2.03-1.87-2.52-.51-.43-1.11-.76-1.75-.96-.72-.23-1.53-.23-3.13-.23H.75M16.75 11.75c3 0 4 2 4 2M16.75 11.75 15.23 3.38c-.17-.94-.26-1.4-.5-1.75a2 2 0 0 0-.84-.71c-.39-.17-.86-.17-1.81-.17h-.33M3.75 6.75h2M.75 3.75h4M15.75 5.75h1.42a1.5 1.5 0 0 0 .58-2.9c-.2-.09-.42-.1-.58-.1H15.25M6.75 15.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM18.75 16.75a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M20 7H7M20 12H4M16 17H4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    /* An actual globe. The asset named icon-globe.svg is a chevron-down (a
       misnamed Figma export) — using it as a globe put a dropdown arrow
       beside every language row in the locale popup. */
    globe:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M3 12h18M12 3c2.5 2.4 3.8 5.6 3.8 9S14.5 18.6 12 21c-2.5-2.4-3.8-5.6-3.8-9S9.5 5.4 12 3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
    /* Stepper glyphs — same SVGs as components.py's ICON. Text −/+ sit on a
       baseline and centre visibly low in their buttons; a viewBox-centred
       path cannot drift. */
    plus: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    minus: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    close:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    chevronDown:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    /* Shopping bag: solid body, stroked handle. Replaces the old basket,
       which was a Figma export carrying preserveAspectRatio="none" and a
       hardcoded fill, so it neither inherited colour nor scaled honestly.
       Solid reads better than an outline at 28px on the yellow disc. */
    cart:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">' +
      '<path d="M8.75 9.25V6.9a3.25 3.25 0 0 1 6.5 0v2.35" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>' +
      '<path d="M4.94 8.4h14.12c.63 0 1.12.54 1.06 1.17l-.88 9.09a3 3 0 0 1-2.99 2.71H7.75a3 3 0 0 1-2.99-2.71l-.88-9.09A1.07 1.07 0 0 1 4.94 8.4Z" fill="currentColor"/>' +
      "</svg>",
    arrowRight:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m9 6 6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    arrowLeft:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m15 6-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    phone:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  };

  const isCheckout = () => document.body.getAttribute("data-page") === "checkout";
  const currentPath = () => document.body.getAttribute("data-path") || "/";

  /* ---------------------------------------------------------------
     Country / currency selector.
     Egypt-only in this build; the markup carries the full control so the
     export drops straight into the real storefront.
     --------------------------------------------------------------- */
  /*
   * Country / language switcher. The live site opens a 288px panel headed
   * اللغة with English and العربية rows, a flag per row and a check on the
   * active one — replicated here, measured off abuauf.com rather than eyeballed.
   *
   * The toggle really does flip `dir` and `lang` on <html>, which is the point:
   * it makes the RTL↔LTR layout testable. It does NOT translate page copy —
   * see initLangSwitcher and DESIGN-NOTES.
   */
  /*
   * English chrome strings, keyed by the Arabic original so the existing data
   * literals do not have to be restructured. `t()` returns the Arabic unchanged
   * unless the document is in English mode.
   *
   * IMPORTANT: these English strings are written in-house — standard commerce
   * terminology, not the client's approved wording. They are placeholder and
   * flagged as such in DESIGN-NOTES. Page body copy is NOT translated: there is
   * no English source for it and machine-translating a storefront would be
   * inventing content. See the "Language" section in DESIGN-NOTES.
   */
  const EN = {
    // primary nav
    "العروض و الخصومات": "Offers & Discounts",
    "المكسرات": "Nuts",
    "القهوة": "Coffee",
    "التمور والفواكه المجففة": "Dates & Dried Fruits",
    "الوجبات صحية": "Healthy Snacks",
    "المشروبات": "Beverages",
    "البهارات والزيوت": "Spices & Oils",
    "الهدايا": "Gifting",
    // search
    "اقتراحات البحث": "Search suggestions",
    "ابحث عن قهوة، مكسرات، تمور…": "Search for coffee, nuts, dates…",
    "نتيجة": "results",
    "لا توجد نتائج لـ": "No results for",
    "تعذر تحميل نتائج البحث. حاول مرة أخرى.": "Could not load search results. Please try again.",
    "منتجات أُضيفت إلى السلة": "products added to cart",
    // masthead + utility
    "المنتجات": "Products",
    "الحساب": "Account",
    "تسجيل الدخول": "Sign in",
    "قصتنا": "Our Story",
    "المكافآت": "Rewards",
    "الفروع": "Branches",
    "منتجات أبو عوف خارج مصر": "Abu Auf Worldwide",
    "البلوج": "Blog",
    "سياسة التوصيل والاسترجاع": "Delivery & Returns",
    "أتصل بنا": "Contact Us",
    // footer columns
    "أقسام المنتجات": "Categories",
    "عن الشركة": "About",
    "المساعدة": "Help",
    "فروعنا": "Our Branches",
    "وصفاتنا": "Recipes",
    "التصدير": "Export",
    "الموزعين في مصر": "Distributors in Egypt",
    "شركاء النجاح": "Partners",
    "فرص وظائف": "Careers",
    "إبداء الرأي": "Feedback",
    "الاسئلة الشائعة": "FAQs",
    "تعليقات العملاء": "Reviews",
    "التوصيل أو الاستلام": "Delivery or Pickup",
    "تطبيق الجوال": "Mobile App",
    "الشروط والاحكام": "Terms & Conditions",
    "سياسة الخصوصية": "Privacy Policy",
    "سياسة الاسترجاع": "Return Policy",
    // cart / overlays
    "سلة التسوق": "Shopping Cart",
    "قد يعجبك أيضا": "You may also like",
    "مصاريف التوصيل": "Delivery fee",
    "الإجمالي": "Total",
    "خصم النقاط": "Points discount",
    "خصم المبلغ": "Apply discount",
    "إلغاء الخصم": "Remove discount",
    // locale popup + addresses
    "الدولة واللغة": "Country & language",
    "الدولة و العملة": "Country & currency",
    "تطبيق": "Apply",
    "اضف عنوان": "Add address",
    "تعديل العنوان": "Edit address",
    "اسم العنوان": "Address name",
    "العنوان": "Address",
    "المنطقة والمدينة": "Area & city",
    "اجعله العنوان الرئيسي": "Make it the main address",
    "حفظ العنوان": "Save address",
    "العنوان الرئيسي": "Main address",
    "تعديل": "Edit",
    "لا توجد عناوين محفوظة بعد.": "No saved addresses yet.",
    "تم النسخ ✓": "Copied ✓",
    "عرض السلة": "View cart",
    "اتمام الشراء": "Checkout",
    // Heading has no full stop; the older "سلتك فارغة." entry is kept because
    // translateDocument() may still meet that exact string in stored copy.
    "سلتك فارغة.": "Your cart is empty.",
    "سلتك فارغة": "Your cart is empty",
    "المنتجات اللي تضيفها هتظهر هنا.": "Products you add will appear here.",
    "حذف": "Remove",
    "اضف": "Add",
    "القائمة": "Menu",
    "روابط أخرى": "More links",
    "الاكثر مبيعا": "Best sellers",
    "اللغة": "Language",
    // build-time UI strings — these live in the generated HTML, and are picked
    // up by translateDocument()'s text-node pass rather than by t()
    "خصم 10% لما تستخدم برومو كود": "10% off with promo code",
    // Demo sign-in
    "تم تسجيل الدخول بنجاح": "Signed in successfully",
    "البريد الإلكتروني أو كلمة المرور غير صحيحة": "Incorrect email or password",
    "تم تسجيل الخروج": "Signed out",
    "تسجيل الخروج": "Sign out",
    "حساب تجريبي للاختبار": "Demo account for testing",
    "استخدم البيانات دي لتجربة تسجيل الدخول والمفضلة:": "Use these details to try signing in and favourites:",
    "املأ البيانات تلقائياً": "Fill automatically",
    // Listing filter-chip labels. These are the catalogue's OWN English
    // category names copied verbatim out of catalog.json — real client data,
    // not translations written here. The chips were the last visibly-Arabic
    // UI left on the shop pages in English mode.
    "العروض والخصومات": "Offers & Promotions",
    "مكسرات وحبوب ومقرمشات": "Nuts | Seeds & Crackers",
    "قهوة ومشروبات": "Coffee & Beverages",
    "تمور وفواكه مجففة": "Dates & Dried Fruits",
    "سناكس صحية": "Snacks",
    "اساسيات المطبخ": "Kitchen & Baking",
    "الهدايا والمشاركة": "Gifting & Sharing",
    "الحلويات": "Confectionary",
    "مخبوزات وبسكويت": "Baked Snacks & Biscuits",
    "اضف الى السلة": "Add to cart",
    "أضف إلى المفضلة": "Add to favourites",
    "إزالة من المفضلة": "Remove from favourites",
    "تمت الإضافة إلى المفضلة": "Added to favourites",
    "تمت الإزالة من المفضلة": "Removed from favourites",
    "لا توجد منتجات في المفضلة": "No saved products yet",
    "المنتجات اللي تحفظها هتظهر هنا.": "Products you save will appear here.",
    "تصفح المنتجات": "Browse products",
    "عرض المزيد": "Show more",
    "تسوق اكتر": "Shop more",
    "تسوق منتجاتنا": "Shop our products",
    "كل المنتجات": "All products",
    "الرئيسية": "Home",
    "المنتجات": "Products",
    "منتج": "products",
    "ترتيب حسب": "Sort by",
    "الأكثر مبيعاً": "Best selling",
    "وصل حديثاً": "New arrivals",
    "السعر: من الأقل": "Price: low to high",
    "السعر: من الأعلى": "Price: high to low",
    "سلة التسوق": "Shopping cart",
    "ملخص السلة": "Cart summary",
    "تعديل": "Edit",
    "الإجمالي": "Total",
    "مصاريف التوصيل": "Delivery fee",
    "أطلب الآن": "Order now",
    "اشتري الان": "Buy now",
    "هل لديك برومو كود؟": "Have a promo code?",
    "أضف ملاحظات على الطلب": "Add order notes",
    "لا توجد منتجات في هذا القسم حالياً.": "No products in this section yet.",
    "شكراً لك": "Thank you",
    "الاسئلة و الاجابات": "FAQs",
    "اشتراك": "Subscribe",
    "أشتراك": "Subscribe",
    "تسجيل الخروج": "Sign out",
    "تحتاج مساعدة؟": "Need help?",
    "الأسئلة المتداولة": "FAQs",
    "تواصل معنا": "Contact us",
    "مرحبا": "Welcome",
    "تأكيد": "Confirm",
    "إغلاق": "Close",
    "بحث": "Search",
    "الفروع": "Branches",
  };

  function currentLang() {
    return document.documentElement.getAttribute("lang") === "en" ? "en" : "ar";
  }

  /*
   * Build-time copy lives in the generated HTML, so t() cannot reach it. This
   * walks visible text nodes and swaps any whose exact trimmed text has a
   * dictionary entry, stashing the Arabic on the node so switching back is
   * lossless.
   *
   * Deliberately exact-match only: a string with no entry is left alone. That
   * is what keeps page prose — headings, FAQ answers, legal text, blog posts —
   * in Arabic rather than half-translated, and it means adding a translation is
   * just adding a dictionary key.
   */
  const I18N_STASH = new WeakMap();

  function translateDocument() {
    const en = currentLang() === "en";
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        const p = node.parentElement;
        if (!p) return NodeFilter.FILTER_REJECT;
        const tag = p.tagName;
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "TITLE") return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);

    nodes.forEach((node) => {
      const original = I18N_STASH.has(node) ? I18N_STASH.get(node) : node.nodeValue;
      const key = original.trim();
      if (!EN[key]) return;
      if (!I18N_STASH.has(node)) I18N_STASH.set(node, original);
      node.nodeValue = en ? original.replace(key, EN[key]) : original;
    });
  }
  function t(s) {
    return currentLang() === "en" && EN[s] ? EN[s] : s;
  }

  const LANGS = [
    { code: "en", label: "English", dir: "ltr" },
    { code: "ar", label: "العربية", dir: "rtl" },
  ];

  /*
   * Country + currency, mirroring the live site's switcher. Selecting a
   * country is DEMO state beyond the header label: every price in this build
   * is the client's real EGP figure and no AED price list exists to convert
   * to honestly — flagged in DESIGN-NOTES. `short` is what fits in the
   * masthead pill; `ar` is the full name the popup shows.
   */
  const COUNTRIES = [
    { code: "EG", currency: "EGP", ar: "مصر", short: "مصر", en: "Egypt", flag: "images/abuauf/brand/flag-egypt.svg" },
    { code: "AE", currency: "AED", ar: "الامارات العربية المتحدة", short: "الامارات", en: "UAE", flag: "images/abuauf/brand/flag-uae.svg" },
  ];
  const COUNTRY_KEY = "abuauf:country";
  function currentCountry() {
    let code = "EG";
    try {
      code = localStorage.getItem(COUNTRY_KEY) || "EG";
    } catch (e) {
      /* ignore */
    }
    return COUNTRIES.find((c) => c.code === code) || COUNTRIES[0];
  }

  /* The masthead pill. It used to own a dropdown of languages; both the
     country and the language now live in the locale POPUP (see overlaysHTML),
     because Ahmed wants to change the two together and apply once — the
     dropdown applied each row the moment it was clicked. */
  function countryButton() {
    const c = currentCountry();
    // Rendered FROM state, never hardcoded: repaintForLang rebuilds this
    // markup after applyLang has already run, so a literal here would
    // overwrite the freshly-applied label with a stale one.
    const label = currentLang() === "ar" ? c.short + " (العربية)" : c.en + " (English)";
    // No trailing chevron: despite its name, icon-globe.svg IS a
    // chevron-down (a misnamed Figma export), and a down-chevron promises a
    // dropdown. This opens a popup now, so the pill ends at its label
    // (Ahmed, 2026-07-22).
    return `
      <button type="button" data-open="locale" class="flex items-center gap-1.5 min-h-11 px-4 py-0.5 rounded-full hover:bg-black/5 transition-colors shrink-0">
        <img src="${c.flag}" alt="" data-country-flag class="rounded-full w-4 h-4 object-cover" />
        <span class="font-semibold text-[#163300] text-base leading-[26px] whitespace-nowrap" data-lang-label>${esc(label)}</span>
      </button>`;
  }

  /* ---------------------------------------------------------------
     Header
     --------------------------------------------------------------- */
  /*
   * A nav tab. The 4px underline is the Figma "Highlight" element — it sits in
   * the layout at all times and only changes transform, so tabs never shift
   * vertically on hover or when the active page changes.
   *
   * The current page and a hovered tab are drawn DIFFERENTLY on purpose; see
   * `.nav-underline` in styles.css. Ahmed reported the navbar as looking
   * permanently hovered three times, and the cause was that the two states
   * were pixel-identical: on a category page one tab carries a solid bar
   * forever, and with nothing to distinguish it from the hover bar it simply
   * reads as stuck. Same lesson as the mega-menu column.
   */
  function desktopNavItem(item) {
    const href = pageHref(item.url);
    const isActive = currentPath() === item.url;
    /* The discount glyph renders BEFORE the label in the DOM, which in RTL
       puts it on the right-hand side of the text — where Ahmed wants it. It
       used to come after, so it sat on the left. 24px to sit level with the
       16px label rather than towering over it. */
    const markIcon = item.icon
      ? `<img src="${item.icon}" alt="" class="shrink-0 w-6 h-6" />`
      : "";

    /* This column must sum to EXACTLY the bar's 48px: pt-3 (12) + label h-6
       (24) + gap-2 (8) + underline h-1 (4). It used to be pt-3.5 + gap-3 =
       54px, and because the ul's overflow-x-auto forces overflow-y to
       compute to auto as well, the last 6px were CLIPPED — the underline
       (hover and current-page alike) was being painted 2px below the visible
       bar on every page. Ahmed reported the hover states as simply not
       working; they worked, invisibly. If the bar height or any of these
       four numbers changes, re-do this sum. */
    const label = `
      <a href="${href}" class="flex flex-col gap-2 pt-3 shrink-0 group">
        <span class="flex items-center gap-1.5 h-6">
          ${markIcon}
          <span class="font-semibold text-white/90 group-hover:text-white text-base leading-6 whitespace-nowrap transition-colors duration-200">${esc(t(item.name))}</span>
        </span>
        <span class="nav-underline h-1 w-full rounded-full origin-center${isActive ? " is-current" : ""}"></span>
      </a>`;

    if (!item.children || !item.children.length) {
      return `<li class="flex items-center gap-2.5 shrink-0">${label}</li>`;
    }

    const cols = item.children
      .map(
        (c) =>
          `<li><a href="${pageHref(c.url)}" class="block py-1.5 font-medium text-textSecondary hover:text-primary text-base transition-colors">${esc(t(c.name))}</a></li>`,
      )
      .join("");

    return `<li class="group/mega relative flex items-center gap-2 shrink-0">
      ${label}
      <!-- start-0, not inset-inline-start-0 — same non-existent-class bug. -->
      <div class="invisible group-hover/mega:visible top-full start-0 z-50 absolute opacity-0 group-hover/mega:opacity-100 pt-3 transition-all duration-200">
        <div class="flex gap-6 bg-white shadow-custom3 p-6 rounded-2xl w-max min-w-[420px]">
          <div class="flex-1">
            <div class="mb-3 font-semibold text-primary text-lg">${esc(t(item.name))}</div>
            <ul class="gap-x-8 grid grid-cols-2">${cols}</ul>
            <a href="${href}" class="inline-flex items-center gap-1 mt-4 font-semibold text-cta hover:text-primary text-base transition-colors">
              تسوق كل ${esc(t(item.name))}
              <span class="w-5 h-5 rtl:scale-flip">${ICON.arrowRight}</span>
            </a>
          </div>
          <div class="bg-interaction-base shrink-0 rounded-xl w-[180px] overflow-hidden">
            <img src="${item.image}" alt="${esc(t(item.name))}" class="w-full h-[160px] object-cover" loading="lazy" />
          </div>
        </div>
      </div>
    </li>`;
  }

  /*
   * Products mega-panel — matches the live site, which opens a full-width
   * dropdown under المنتجات on desktop. This used to open the mobile side
   * drawer at every width, which is a phone pattern on a 1440px window.
   *
   * Three columns, RTL order: categories, the active category's
   * sub-categories, then a product rail. Phones are untouched — the drawer is
   * still the right control there.
   */
  /* `id` is each product's catalog.json id, so the tile can link to that
     product's own generated page instead of the bare product.html every
     product link on the site used to share. */
  const MEGA_FEATURED = [
    { id: 10576, name: "عرض سناكس بروتين بزبدة الفول السودانى 35 جم", price: 51, img: "images/abuauf/products/PR000085.webp" },
    { id: 46238, name: "بسكويت محشو تمر - 12 قطعة", price: 65, img: "images/abuauf/products/image-600x600-1.png" },
    { id: 10502, name: "بن أبو عوف تركي ساده فاتح 200 جم", price: 308, img: "images/abuauf/products/6223004765353-2-1.webp" },
    { id: 1571, name: "عرض معمول سادة وقرفة وشيكولاتة", price: 250, img: "images/abuauf/products/330-thumb.webp" },
  ];

  /* No onerror handler. This previously carried onerror="this.style.display
     ='none'", and the file it points at did not exist — so all 8 mega-panel
     category bullets failed silently on every page and nothing surfaced it.
     A missing asset should be visible, not swallowed. */
  const LEAF = `<img src="images/abuauf/icons/icon-leaf.svg" alt="" class="w-5 h-5 shrink-0" />`;

  function megaPanelHTML() {
    const cats = MAIN_MENU.map((item, i) => {
      const slug = (item.url || "").replace("/shop/", "");
      return `<li>
        <!-- Selected and hovered used to paint the identical #EDEFEB, so the
             chosen category was indistinguishable from one under the cursor —
             and because hovering also *activates* a category, the whole column
             read as permanently hovered. .mega-cat in styles.css gives the
             two states different treatments: hover is a faint wash, selected
             is a tinted surface with a brand bar on the leading edge. -->
        <button type="button" data-mega-cat="${i}" class="mega-cat flex items-center gap-3 px-4 rounded-xl w-full min-h-11 font-semibold text-[#062A1C] text-base text-start" data-active="${i === 0}">
          ${LEAF}
          <span class="flex-1 min-w-0 truncate">${esc(t(item.name))}</span>
          <span class="mega-cat__arrow w-4 h-4 text-neutral-secondary rtl:scale-flip shrink-0">${ICON.arrowRight}</span>
        </button>
      </li>`;
    }).join("");

    const subPanels = MAIN_MENU.map((item, i) => {
      const href = pageHref(item.url);
      const kids = (item.children || [])
        .map(
          (c) => `<li>
            <a href="${pageHref(c.url)}" class="flex items-center gap-3 px-4 rounded-xl min-h-11 text-[#062A1C] text-base transition-colors hover:bg-interaction-base">
              <span class="flex-1 min-w-0 truncate">${esc(t(c.name))}</span>
              <span class="w-4 h-4 text-neutral-secondary rtl:scale-flip shrink-0">${ICON.arrowRight}</span>
            </a>
          </li>`,
        )
        .join("");
      return `<ul data-mega-sub="${i}" ${i === 0 ? "" : "hidden"} class="flex flex-col gap-1">
        <li>
          <a href="${href}" class="flex items-center gap-3 px-4 rounded-xl min-h-11 font-semibold text-cta text-base transition-colors hover:bg-interaction-base">
            <span class="flex-1 min-w-0 truncate">جميع ${esc(t(item.name))}</span>
            <span class="w-4 h-4 rtl:scale-flip shrink-0">${ICON.arrowRight}</span>
          </a>
        </li>
        ${kids}
      </ul>`;
    }).join("");

    const featured = MEGA_FEATURED.map(
      (p) => `<a href="product-${p.id}.html" class="flex items-center gap-3 bg-white hover:shadow-custom4 p-3 rounded-2xl transition-shadow">
        <span class="flex-1 min-w-0">
          <span class="block font-medium text-[#062A1C] text-sm leading-5 line-clamp-2">${esc(p.name)}</span>
          <span class="inline-block bg-accent-yellow mt-1.5 px-2 py-0.5 rounded font-bold text-[#062A1C] text-xs latin">EGP ${p.price}.00</span>
        </span>
        <img src="${p.img}" alt="" class="bg-interaction-base p-1 rounded-lg w-14 h-14 object-contain shrink-0" loading="lazy" />
      </a>`,
    ).join("");

    return `
      <!-- start-0 end-0, NOT inset-inline-0: the latter is not a Tailwind
           class and never has been, so it compiled to nothing and the panel
           sat at its static position — 1126px inside a 1425px container,
           ~300px short of the full-width panel this is meant to be. It looked
           close enough in RTL to go unnoticed because the static position
           already pins it to the right edge. -->
      <div id="mega-panel" data-megamenu hidden class="hidden lg:block top-full start-0 end-0 z-40 absolute bg-white shadow-custom3 rounded-b-2xl">
        <!-- 1536 to match the nav above it. The panel is now full-bleed (its
             positioning parent lost its padding), so a 1600 cap would have
             left the panel 64px wider than the nav it hangs off. -->
        <div class="gap-6 grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1.15fr)] mx-auto p-6 max-w-[1536px]">
          <ul class="flex flex-col gap-1 pe-6 border-neutral-divider border-e">${cats}</ul>
          <div class="pe-6 border-neutral-divider border-e">${subPanels}</div>
          <div class="flex flex-col gap-3">
            <h3 class="font-bold text-[#062A1C] text-lg">${esc(t("الاكثر مبيعا"))}</h3>
            <div class="flex flex-col gap-2 bg-interaction-base p-3 rounded-2xl">${featured}</div>
          </div>
        </div>
      </div>`;
  }

  function headerHTML() {
    const checkout = isCheckout();

    /* --- support (utility) menu --- */
    const support = SUPPORT_MENU.map(
      (i) =>
        `<a href="${pageHref(i.url)}" class="font-semibold text-[#5F5035] hover:text-cta text-[13px] leading-[140%] transition-colors">${esc(t(i.title))}</a>`,
    ).join("");

    /* --- desktop primary nav --- */
    const nav = MAIN_MENU.map(desktopNavItem).join("");

    const desktop = `
      <div class="hidden md:block">
        ${
          checkout
            ? ""
            : `<div class="relative z-50 bg-beige h-[33px]">
                 <div class="flex justify-between items-center gap-6 mx-auto px-4 max-w-[1536px] h-full">
                   <div class="flex items-center gap-6 min-w-0">
                     ${countryButton()}
                     <nav class="hidden xl:flex items-center gap-6 min-w-0 overflow-hidden">${support}</nav>
                   </div>
                   <div class="hidden lg:flex items-center gap-2 shrink-0">
                     <span class="grid place-items-center bg-white border border-neutral-divider rounded w-[35px] h-6">
                       <img src="images/abuauf/payments/pay-mastercard.svg" alt="Mastercard" class="w-[22px] h-[14px]" />
                     </span>
                     <img src="images/abuauf/payments/pay-visa.svg" alt="Visa" class="w-[35px] h-6" />
                   </div>
                   <p class="hidden lg:block shrink-0 font-bold text-[#5F5035] text-base leading-[22px] whitespace-nowrap">
                     خصم 10% لما تستخدم برومو كود <span class="latin">DISCOUNT10</span>
                   </p>
                 </div>
               </div>`
        }
        <!-- Full-bleed background; the inline padding belongs to the inner
             container, not out here. With px-4 xl:px-20 on this element the
             80px was subtracted BEFORE max-w-[1536px] applied, so the cap
             never bound and the header sat 64px inside the page content edge
             on every page. On the live site the logo's outer edge lands
             exactly on the content container edge. -->
        <div class="relative z-40 bg-primary">
          <div class="flex justify-between items-center mx-auto px-4 border-[#0F6140] border-b h-[79px] max-w-[1536px]">
            <!-- RTL start (right edge): logo, products, delivery -->
            <div class="flex items-center gap-6 min-w-0">
              <!-- The client's own asset (abuauf.com/images/logo_white.webp,
                   524x134). The hand-derived SVG it replaced was five white
                   paths with the green leaf missing entirely, and was drawn at
                   180x60 (aspect 3.0) against the real mark's 3.91. Live
                   renders it 120x31. -->
              <a href="index.html" class="block shrink-0 w-[120px] h-[31px]">
                <img src="images/abuauf/brand/logo-abuauf-white.webp" alt="أبو عوف" class="w-full h-full object-contain" />
              </a>
              ${
                checkout
                  ? ""
                  : `<!-- No colour utilities here on purpose: the pill's fill is
                          state-driven and lives in styles.css (.mega-toggle).
                          Rest is unfilled, hover is a faint wash, and the solid
                          CTA fill now means exactly one thing - "the panel is
                          open". With bg-cta baked into the markup the button
                          sat permanently filled, which read as a stuck hover;
                          Ahmed reported it. -->
                     <button type="button" data-megamenu-toggle aria-expanded="false" aria-controls="mega-panel" class="mega-toggle hidden lg:flex items-center gap-3 shrink-0 px-4 py-2 rounded-full h-12">
                       <img src="images/abuauf/icons/icon-grid.svg" alt="" class="w-6 h-6" />
                       <span class="font-medium text-white text-[18px] leading-6 whitespace-nowrap">${esc(t("المنتجات"))}</span>
                       <span class="w-[18px] h-[18px] text-white shrink-0 chevron" data-megamenu-caret>${ICON.chevronDown}</span>
                     </button>
                     <button type="button" data-open="location" class="hidden xl:flex items-center gap-2 hover:text-white/80 py-3 h-12 min-w-0 transition-colors">
                       <span class="font-normal text-white text-[13px] leading-5 truncate">التوصيل الى الشروق - القاهرة</span>
                       <span class="shrink-0 w-[18px] h-[18px] text-white chevron">${ICON.chevronDown}</span>
                     </button>`
              }
            </div>

            <!-- RTL end (left edge): account, search, cart.
                 Checkout keeps account and cart but drops search, matching the
                 Figma checkout header — it is not a bare logo bar. -->
            <div class="flex items-center gap-6 shrink-0">
              <a href="login.html" data-account-link class="hidden lg:flex items-center gap-3 hover:text-white/80 py-2 h-12 transition-colors">
                <!-- Also the landing pad for the favourites flight, hence
                     data-fav-target on the icon rather than the whole link. -->
                <span class="relative shrink-0" data-fav-target>
                  <img src="images/abuauf/icons/icon-user.svg" alt="" class="w-6 h-6" />
                  <span data-fav-count hidden
                        class="-top-1.5 -end-2 absolute place-items-center grid bg-accent-yellow rounded-full min-w-[18px] h-[18px] px-1 font-bold text-[#062A1C] text-[10px] leading-none">0</span>
                </span>
                <span class="font-normal text-white text-[13px] leading-5" data-account-label>${esc(t("الحساب"))}</span>
                <span class="w-[18px] h-[18px] text-white shrink-0 chevron">${ICON.chevronDown}</span>
              </a>
              <!-- Search and cart ride along on scroll. Once the masthead has
                   left the viewport this group is pulled out of flow by
                   [data-sticky-actions][data-stuck] in styles.css and parked
                   under the sticky nav on an elevated pill. Driven by the same
                   scroll handler as the nav so the two can never disagree. -->
              <div data-sticky-actions class="flex items-center gap-6">
                ${
                  checkout
                    ? ""
                    : `<button type="button" data-open="search" aria-label="بحث" class="btn-elevate place-items-center grid bg-cta hover:bg-cta-hover border-2 border-cta rounded-full size-12">
                         <img src="images/abuauf/icons/icon-search.svg" alt="" class="w-5 h-5" />
                       </button>`
                }
                <button type="button" data-open="cart" aria-label="السلة" class="btn-elevate relative place-items-center grid bg-accent-yellow hover:bg-accent-500 rounded-full text-[#163300] size-12">
                  <span class="w-7 h-7" data-cart-glyph>${ICON.cart}</span>
                  <!-- Brand ink on a white ring rather than a bare white dot:
                       the ring separates it from the yellow button underneath,
                       and white-on-#163300 keeps AA with room to spare. -->
                  <span class="-top-2 -end-2 absolute place-items-center grid bg-cta ring-2 ring-white px-1.5 rounded-full min-w-[22px] h-[22px] font-bold text-white text-xs latin" data-cart-count>2</span>
                </button>
              </div>
            </div>
          </div>

          ${
            checkout
              ? ""
                 /* bg-primary is carried on the bar itself, not inherited from
                    the masthead, so it stays opaque once initStickyNav pulls
                    it out of flow with position:fixed. */
              : `<div data-navbar class="relative z-30 bg-primary h-[48px]">
                   <nav class="mx-auto px-4 max-w-[1536px] h-full">
                     <ul class="flex items-start gap-9 h-full overflow-x-auto no-scrollbar">${nav}</ul>
                   </nav>
                 </div>`
          }
          ${checkout ? "" : megaPanelHTML()}
        </div>
      </div>`;

    /* --- mobile header (refined against the Figma Mobile page later) --- */
    const mobile = `
      <div class="md:hidden block">
        ${
          checkout
            ? ""
            : `<div class="bg-beige px-3 py-1.5">
                 <p class="font-semibold text-[#5F5035] text-[11px] text-center">
                   خصم 10% لما تستخدم برومو كود <span class="latin">DISCOUNT10</span>
                 </p>
               </div>`
        }
        <!-- Both side groups are flex-1, so the logo sits dead-centre no
             matter how many controls each side holds — matching the live
             site's mx-auto logo without a transform, which keeps it RTL-safe.
             min-w-0 because a flex-1 child otherwise cannot shrink below its
             content (the most common bug class in this codebase).
             Live packs these at 36x36; ours stay 44x44 for WCAG 2.5.5, which
             is the project's standing accessibility deviation. -->
        <div class="relative flex items-center ${checkout ? "justify-center" : "justify-between"} gap-2 bg-primary px-4 py-2 text-white">
          ${
            checkout
              ? ""
              : `<div class="flex flex-1 items-center gap-1 min-w-0">
                   <button type="button" data-open="menu" class="place-items-center grid shrink-0 size-11 -ms-2" aria-label="Menu"><span class="w-6 h-6">${ICON.menu}</span></button>
                 </div>`
          }
          <a href="index.html" class="block shrink-0"><img src="images/abuauf/brand/logo-abuauf-white.webp" alt="أبو عوف" class="w-[120px] h-[31px] object-contain" /></a>
          ${
            checkout
              ? ""
              : `<div class="flex flex-1 justify-end items-center gap-1 min-w-0">
                   <button type="button" data-open="search" class="place-items-center grid shrink-0 size-11" aria-label="بحث">
                     <img src="images/abuauf/icons/icon-search.svg" alt="" class="w-5 h-5" />
                   </button>
                   <button type="button" data-open="cart" class="relative place-items-center grid bg-accent-yellow shrink-0 rounded-full text-[#163300] size-11" aria-label="السلة">
                     <span class="w-7 h-7" data-cart-glyph>${ICON.cart}</span>
                     <span class="-top-1 -end-1 absolute place-items-center grid bg-cta ring-2 ring-white rounded-full w-5 h-5 font-bold text-[10px] text-white latin" data-cart-count>2</span>
                   </button>
                 </div>`
          }
        </div>
      </div>
      ${
        checkout
          ? ""
          : `<div class="md:hidden block bg-interaction-base px-4 py-2">
               <button type="button" data-open="location" class="flex justify-between items-center gap-1 bg-cta px-5 py-2.5 rounded-full w-full min-h-11 text-white">
                 <span class="font-semibold text-xs truncate">التوصيل الى الشروق - القاهرة</span>
                 <span class="shrink-0 w-4 h-4 chevron">${ICON.chevronDown}</span>
               </button>
             </div>`
      }`;

    return `<header>${desktop}${mobile}</header>`;
  }

  /* ---------------------------------------------------------------
     Footer
     --------------------------------------------------------------- */
  /*
   * Payment marks, shared by the footer bar and the checkout summary.
   * Sizes are explicit px rather than percentages: these sit inside centred
   * flex/grid boxes where a percentage height resolves against the wrong
   * containing block and distorts the mark.
   */
  function paymentMarks(size) {
    const sm = size === "sm";
    const card = sm ? "w-[23px] h-4" : "w-[35px] h-6";
    const radius = sm ? "rounded-sm" : "rounded";
    const glyphW = sm ? 15 : 22;
    const glyphH = sm ? 9 : 14;
    const cod = sm ? "w-[41px] h-4" : "w-[61px] h-6";
    return `
      <div class="flex items-center gap-1 md:gap-2">
        <!-- Etisalat Cash ships as white artwork on its own opaque black
             plate, so it gets no white chip — it would read as a black box. -->
        <img src="images/abuauf/payments/pay-etisalat-cash.png" alt="اتصالات كاش" class="${card} ${radius} object-cover shrink-0" />
        <span class="inline-flex justify-center items-center bg-white border border-neutral-divider ${card} ${radius} shrink-0">
          <img src="images/abuauf/payments/pay-mastercard-alt.svg" alt="Mastercard" style="width:${glyphW}px;height:${glyphH}px" />
        </span>
        <img src="images/abuauf/payments/pay-visa.svg" alt="Visa" class="${card} ${radius} shrink-0" />
        <img src="images/abuauf/payments/pay-cod.png" alt="الدفع عند الاستلام" class="${cod} object-contain shrink-0" />
      </div>`;
  }

  function footerHTML() {
    const copyright = `جميع حقوق النشر تنتمي إلى ابو عوف, <span class="latin">${YEAR}</span>`;

    if (isCheckout()) {
      return `<footer class="bg-black py-6">
        <div class="mx-auto px-4 max-w-[1392px] text-onBlack text-xs text-center">${copyright}</div>
      </footer>`;
    }

    const columns = FOOTER_COLUMNS.map(
      (col) => `
      <div class="flex-1 min-w-[150px]">
        <h2 class="mb-5 font-bold text-onDarkGreen text-base leading-[22px]">${esc(t(col.name))}</h2>
        <ul class="flex flex-col gap-2">
          ${col.links
            .map(
              (l) =>
                `<li><a href="${pageHref(l.url)}" class="font-normal text-white hover:text-accent-yellow text-base leading-6 transition-colors">${esc(t(l.title))}</a></li>`,
            )
            .join("")}
        </ul>
      </div>`,
    ).join("");

    const socials = SOCIALS.map(
      (s) =>
        `<li><a href="${s.href}" target="_blank" rel="noopener noreferrer" aria-label="${esc(s.title)}" class="block opacity-90 hover:opacity-100 transition-opacity">
           <img src="${s.icon}" alt="" class="w-6 h-6" />
         </a></li>`,
    ).join("");

    /* --- pre-footer: newsletter + FAQ, split 50/50 on desktop --- */
    const preFooter = `
      <div class="bg-beige border-primary border-b">
        <div class="flex md:flex-row flex-col justify-center items-stretch gap-8 md:gap-12 mx-auto px-4 py-6 max-w-[1536px]">
          <div class="flex flex-col justify-center gap-6 py-6 md:py-[42px] flex-1">
            <div class="flex flex-col gap-2">
              <h2 class="font-bold text-[#062A1C] text-2xl md:text-3xl xl:text-4xl leading-tight xl:leading-[48px]">عندك اي اسئلة؟ كل حاجة هنا..</h2>
              <p class="font-semibold text-primary text-sm xl:text-xl leading-relaxed">لو عندك أي استفسار أو عايز تطرح أي سؤال ، هتلاقي كل حاجة هنا</p>
            </div>
            <a href="faqs.html" class="self-start bg-cta hover:bg-cta-hover px-8 xl:px-10 py-3 xl:py-[18px] rounded-full font-semibold text-white text-sm xl:text-xl transition-colors">الاسئلة و الاجابات</a>
          </div>

          <div class="flex flex-col justify-center gap-6 py-6 md:py-[42px] flex-1">
            <div class="flex flex-col gap-2">
              <h2 class="font-bold text-[#062A1C] text-2xl md:text-3xl xl:text-4xl leading-tight xl:leading-[48px]">اشترك لتعرف على أجدد العروض والخصومات</h2>
              <p class="font-semibold text-primary text-sm xl:text-xl leading-relaxed">كن أول من يعرف كل ما هو جديد في ابو عوف</p>
            </div>
            <form data-newsletter class="newsletter-row flex flex-row-reverse items-center gap-2 bg-transparent py-2 xl:py-[9px] pe-5 ps-2.5 border-2 border-neutral-outline rounded-2xl w-full">
              <span class="text-neutral-secondary shrink-0" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" class="w-6 h-6"><rect x="2.5" y="4.5" width="19" height="15" rx="2.5" stroke="currentColor" stroke-width="1.7"/><path d="m3 7 8.4 5.6a1 1 0 0 0 1.2 0L21 7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span>
              <input type="email" required aria-label="البريد الالكتروني"
                     placeholder="أدخل عنوان البريد الالكتروني"
                     class="flex-1 bg-transparent outline-none min-w-0 font-normal text-[#062A1C] placeholder:text-onBeigeMuted text-sm xl:text-base" />
              <button type="submit" class="bg-cta hover:bg-cta-hover px-5 py-2 xl:py-2.5 rounded-full font-bold text-white text-sm xl:text-base whitespace-nowrap transition-colors">اشتراك</button>
            </form>
          </div>
        </div>
      </div>`;

    return `<footer>
      ${preFooter}
      <div class="bg-[#062B1C]">
        <div class="flex xl:flex-row flex-col-reverse gap-10 xl:gap-6 mx-auto px-4 py-6 xl:py-12 max-w-[1536px]">
          <!-- RTL start (right): brand, hotline, address, socials -->
          <div class="flex flex-col gap-3 xl:flex-1 xl:order-first">
            <img src="images/abuauf/brand/logo-abuauf-white.webp" alt="أبو عوف" class="w-[180px] h-[46px] object-contain" />
            <a href="tel:${CONTACT.hotline}" class="mt-auto xl:mt-10 font-bold text-white text-2xl xl:text-4xl latin">${CONTACT.hotline}</a>
            <p class="max-w-[277px] font-semibold text-onDarkGreen text-sm xl:text-base leading-relaxed">${esc(CONTACT.address)}</p>
            <ul class="flex items-center gap-6 mt-1">${socials}</ul>
          </div>
          <!-- link columns -->
          <div class="flex flex-wrap gap-8 xl:gap-6 xl:flex-[3]">${columns}</div>
        </div>

        <div class="bg-black">
          <div class="flex md:flex-row flex-col-reverse justify-between items-center gap-4 mx-auto px-4 py-4 max-w-[1536px] min-h-[60px]">
            <a href="https://www.mitchdesigns.com" target="_blank" rel="noopener noreferrer"
               class="flex items-center gap-2 opacity-30 hover:opacity-60 p-1.5 transition-opacity shrink-0" dir="ltr">
              <img src="images/abuauf/brand/mitchdesigns-logomark.svg" alt="" class="w-[30px] h-[30px]" />
              <span class="flex flex-col gap-0.5 text-onBlack text-start latin">
                <span class="text-[10px] leading-[14px]">Web Design by</span>
                <span class="font-medium text-sm leading-4">MITCH DESIGNS</span>
              </span>
            </a>
            ${paymentMarks()}
            <p class="font-medium text-onBlack text-xs xl:text-base">${copyright}</p>
          </div>
        </div>
      </div>
    </footer>`;
  }

  const YEAR = 2026; // static build stamp (Date.now avoided for determinism)

  /* ---------------------------------------------------------------
     Overlays: backdrop, cart drawer, mobile menu, search, location
     --------------------------------------------------------------- */
  function overlaysHTML() {
    const menuLinks = MAIN_MENU.map(
      (i) => `
      <li class="border-b border-neutral-100">
        <a href="${pageHref(i.url)}" class="flex items-center justify-between min-h-11 py-3.5 text-textSecondary font-medium">${esc(t(i.name))}${i.children ? `<span class="w-4 h-4 text-neutral-secondary">${ICON.arrowRight}</span>` : ""}</a>
      </li>`,
    ).join("");
    const supportLinks = SUPPORT_MENU.map(
      (i) =>
        `<li><a href="${pageHref(i.url)}" class="flex items-center min-h-11 py-2 text-neutral-secondary text-sm">${esc(t(i.title))}</a></li>`,
    ).join("");

    /* Seed contents for a first-ever visit, so the drawer and cart page are
       not empty on a fresh browser. Real catalogue items. Once the shopper
       touches the cart this is never consulted again — Cart owns state. */
    /* (kept in CART_SEED at module scope) */

    /* "قد يعجبك أيضا" upsell — real catalogue items.
     *
     * Each row is a `[data-product]` host carrying the real catalogue id,
     * name, price and image, because `productFrom()` walks up to the nearest
     * `[data-product]` and bails when there isn't one. Without it the "اضف"
     * button had `data-add-to-cart` but no product behind it, so the handler
     * returned silently and the button did nothing at all.
     *
     * The first row used to be "مارشميلو بطيخ - 60 جرام" at EGP 30, which
     * matches NO product in catalog.json and was illustrated with the photo
     * of a different real product (قراصيا, id 1445). Replaced with a real
     * catalogue item at the same price so the layout is unchanged.
     */
    const upsell = [
      { id: "1631", name: "كرانبيري - 25 جم", price: 30, img: "images/abuauf/products/6223006314092.webp" },
      { id: "46238", name: "بسكويت محشو تمر - 12 قطعة", price: 65, img: "images/abuauf/products/image-600x600-1.png" },
    ]
      .map(
        (p) => `
        <div class="flex items-center gap-3 bg-white p-3 border border-neutral-divider rounded-2xl"
             data-product data-id="${esc(p.id)}" data-name="${esc(p.name)}"
             data-price="${p.price}" data-image="${esc(p.img)}">
          <img src="${p.img}" alt="" class="bg-interaction-base shrink-0 p-1 rounded-lg w-14 h-14 object-contain" loading="lazy" />
          <div class="flex-1 min-w-0">
            <p class="font-medium text-[#062A1C] text-sm line-clamp-2">${esc(p.name)}</p>
            <span class="inline-block bg-accent-yellow mt-1 px-2 py-0.5 rounded font-bold text-[#062A1C] text-xs latin">EGP ${p.price}.00</span>
          </div>
          <button type="button" data-add-to-cart class="flex items-center gap-1.5 bg-cta hover:bg-cta-hover shrink-0 px-4 rounded-full min-h-11 font-semibold text-white text-sm transition-colors">اضف</button>
        </div>`,
      )
      .join("");

    /* Static shell only — the numbers and disabled state are filled in by
       renderCart() on every cart:change. */
    const cartFooter = `
        <div class="flex justify-between text-sm">
          <span class="text-neutral-secondary">${esc(t("مصاريف التوصيل"))}</span>
          <span class="font-semibold text-[#062A1C] latin">${egp(DELIVERY_FEE)}</span>
        </div>
        <!-- Points discount, when applied on the cart or checkout page. The
             drawer must show WHY its total is lower than items + delivery,
             or the smaller number reads as a bug. -->
        <div class="flex justify-between items-center text-sm" data-cart-discount-row hidden>
          <span class="text-neutral-secondary">${esc(t("خصم النقاط"))}</span>
          <span class="bg-[#E9F3E6] px-2 py-0.5 rounded font-bold text-[#163300] latin" data-cart-discount></span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-neutral-secondary text-sm">${esc(t("الإجمالي"))}</span>
          <span class="font-bold text-[#062A1C] text-lg latin" data-cart-total>${egp(0)}</span>
        </div>
        <div class="gap-3 grid grid-cols-2 mt-1">
          <a href="cart.html" class="flex justify-center items-center border-cta hover:bg-interaction-base border rounded-full min-h-11 font-semibold text-cta text-sm transition-colors">${esc(t("عرض السلة"))}</a>
          <a href="checkout.html" data-cart-checkout class="flex justify-center items-center bg-cta hover:bg-cta-hover rounded-full min-h-11 font-semibold text-white text-sm text-center transition-colors">${esc(t("اتمام الشراء"))}</a>
        </div>
        <p data-cart-warning hidden class="flex items-start gap-2 mt-1 text-accent-error text-xs leading-5">
          <span aria-hidden="true">⚠</span>
          متبقي <span class="latin" data-cart-shortfall></span> لاستكمال الحد الأدنى للطلب
        </p>`;

    return `
    <div data-backdrop class="overlay-backdrop"></div>

    <!-- Cart drawer -->
    <aside data-drawer="cart" class="side-drawer side-drawer--right" aria-label="سلة التسوق">
      <div class="flex justify-between items-center px-5 py-4 border-neutral-divider border-b">
        <h2 class="font-bold text-[#062A1C] text-lg">${esc(t("سلة التسوق"))}</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-interaction-base rounded-full w-8 h-8 text-[#062A1C]" aria-label="إغلاق">${ICON.close}</button>
      </div>
      <div class="flex-1 px-5 overflow-y-auto">
        <div data-cart-lines></div>
        <div class="mt-4">
          <p class="mb-2 font-bold text-[#062A1C] text-sm">${esc(t("قد يعجبك أيضا"))}</p>
          <div class="flex flex-col gap-2">${upsell}</div>
        </div>
      </div>
      <div class="flex flex-col gap-2 shadow-cart-overview px-5 py-4 border-neutral-divider border-t">
        ${cartFooter}
      </div>
    </aside>

    <!-- Mobile menu drawer -->
    <aside data-drawer="menu" class="side-drawer side-drawer--left" aria-label="Menu">
      <div class="flex justify-between items-center bg-primary px-5 py-4 border-neutral-100 border-b text-white">
        <img src="images/abuauf/brand/logo-abuauf-white.webp" alt="أبو عوف" class="w-[110px] h-[28px] object-contain" />
        <button type="button" data-close class="place-items-center grid size-11 -me-2 text-white">${ICON.close}</button>
      </div>
      <div class="flex-1 px-5 py-4 overflow-y-auto">
        <ul>${menuLinks}</ul>
        <div class="mt-6">
          <p class="mb-1 text-neutral-secondary text-xs">${esc(t("روابط أخرى"))}</p>
          <ul>${supportLinks}</ul>
        </div>
        <div class="flex flex-col gap-3 mt-6">
          <a href="login.html" class="flex justify-center items-center min-h-11 py-2.5 border border-cta rounded-full font-medium text-cta text-sm text-center">تسجيل الدخول</a>
          <div class="flex justify-center">${countryButton()}</div>
        </div>
      </div>
    </aside>

    <!-- Search modal -->
    <div data-modal="search" class="modal-shell">
      <div class="bg-white shadow-custom3 rounded-2xl w-full max-w-[640px] overflow-hidden" data-modal-box>
        <div class="flex items-center gap-3 px-5 py-4 border-neutral-divider border-b search-row">
          <span class="w-5 h-5 text-neutral-secondary shrink-0">${ICON.search}</span>
          <label class="sr-only" for="site-search">${esc(t("ابحث عن قهوة، مكسرات، تمور…"))}</label>
          <input type="search" id="site-search" data-search-input autocomplete="off"
                 placeholder="ابحث عن قهوة، مكسرات، تمور…"
                 class="flex-1 bg-transparent outline-none min-w-0 text-[#062A1C] text-base" />
          <button type="button" data-close class="place-items-center grid hover:bg-interaction-base rounded-full w-11 h-11 text-[#062A1C] shrink-0" aria-label="إغلاق">${ICON.close}</button>
        </div>

        <!-- Idle state: the query is empty. These were five links that all
             pointed at the same category page; they now seed the box.

             The label is NOT "الأكثر بحثاً" any more and the terms are not
             the old invented ones. There is no search analytics behind this,
             so claiming these are the most-searched was inventing data — and
             the terms themselves were phrases like "قهوة تركي" that match
             nothing in the catalogue, so every chip was a guaranteed empty
             result. These five are counted off the real product names
             (5-7 products each), so a chip always lands on something. -->
        <div class="px-5 py-6" data-search-idle>
          <p class="mb-3 text-neutral-secondary text-xs">${esc(t("اقتراحات البحث"))}</p>
          <div class="flex flex-wrap gap-2">
            ${["قهوة", "مكسرات", "تمر", "معمول", "بروتين"]
              .map(
                (s) =>
                  `<button type="button" data-search-seed="${esc(s)}" class="bg-interaction-base hover:bg-cta px-3 py-2 rounded-full min-h-11 text-[#062A1C] hover:text-white text-sm transition-colors">${esc(s)}</button>`,
              )
              .join("")}
          </div>
        </div>

        <!-- Result count is a live region so a screen reader hears the list
             change; the list itself is plain anchors, which stay operable if
             the fetch or the JS ever fails. -->
        <p class="px-5 text-neutral-secondary text-xs" data-search-status role="status" aria-live="polite" hidden></p>
        <div class="max-h-[52vh] overflow-y-auto overscroll-contain" data-search-results hidden></div>
      </div>
    </div>

    <!-- Locale popup: country/currency + language, applied TOGETHER.
         A modal rather than the dropdown it replaced: the live site's
         dropdown applies each row the moment it is clicked, which repaints
         the page once per choice - Ahmed wants to pick both and pay the
         repaint once, so the rows here only set radios and nothing happens
         until تطبيق. -->
    <div data-modal="locale" class="modal-shell">
      <div class="bg-white shadow-custom3 rounded-2xl w-full max-w-[400px] overflow-hidden" data-modal-box>
        <div class="flex justify-between items-center px-5 py-4 border-neutral-divider border-b">
          <h2 class="font-bold text-[#062A1C] text-lg">${esc(t("الدولة واللغة"))}</h2>
          <button type="button" data-close class="place-items-center grid hover:bg-interaction-base rounded-full w-8 h-8 text-[#062A1C]" aria-label="إغلاق">${ICON.close}</button>
        </div>
        <div class="flex flex-col gap-5 p-5">
          <fieldset class="flex flex-col gap-2">
            <legend class="mb-2 font-bold text-[#062A1C] text-sm">${esc(t("الدولة و العملة"))}</legend>
            ${COUNTRIES.map(
              (c) => `
            <label class="cursor-pointer">
              <input type="radio" name="locale-country" value="${c.code}" class="peer sr-only"${c.code === currentCountry().code ? " checked" : ""} />
              <span class="flex items-center gap-3 px-4 py-2.5 border-2 border-neutral-divider peer-checked:border-cta rounded-xl min-h-11 transition-colors">
                <img src="${c.flag}" alt="" class="rounded-full w-6 h-6 object-cover shrink-0" />
                <span class="flex-1 min-w-0 text-[#062A1C] text-sm">${esc(c.ar)} <span class="latin">(${c.currency})</span></span>
                <span class="radio-dot shrink-0" aria-hidden="true"></span>
              </span>
            </label>`,
            ).join("")}
          </fieldset>
          <fieldset class="flex flex-col gap-2">
            <legend class="mb-2 font-bold text-[#062A1C] text-sm">${esc(t("اللغة"))}</legend>
            ${LANGS.map(
              (l) => `
            <label class="cursor-pointer">
              <input type="radio" name="locale-lang" value="${l.code}" class="peer sr-only"${l.code === currentLang() ? " checked" : ""} />
              <span class="flex items-center gap-3 px-4 py-2.5 border-2 border-neutral-divider peer-checked:border-cta rounded-xl min-h-11 transition-colors">
                <span class="w-5 h-5 text-neutral-secondary shrink-0" aria-hidden="true">${ICON.globe}</span>
                <span class="flex-1 min-w-0 text-[#062A1C] text-sm">${l.label}</span>
                <span class="radio-dot shrink-0" aria-hidden="true"></span>
              </span>
            </label>`,
            ).join("")}
          </fieldset>
          <button type="button" data-locale-apply class="bg-cta hover:bg-cta-hover py-3 rounded-full w-full font-semibold text-white text-sm transition-colors">${esc(t("تطبيق"))}</button>
        </div>
      </div>
    </div>

    <!-- Address form: add and edit share it; data-address-id says which. -->
    <div data-modal="address" class="modal-shell">
      <div class="bg-white shadow-custom3 rounded-2xl w-full max-w-[440px] overflow-hidden" data-modal-box>
        <div class="flex justify-between items-center px-5 py-4 border-neutral-divider border-b">
          <h2 class="font-bold text-[#062A1C] text-lg" data-address-form-title>${esc(t("اضف عنوان"))}</h2>
          <button type="button" data-close class="place-items-center grid hover:bg-interaction-base rounded-full w-8 h-8 text-[#062A1C]" aria-label="إغلاق">${ICON.close}</button>
        </div>
        <form data-address-form data-address-id="" class="flex flex-col gap-3 p-5">
          <label class="block">
            <span class="label">${esc(t("اسم العنوان"))}</span>
            <input type="text" name="label" required placeholder="المنزل، العمل…"
                   class="mt-1 px-3 border border-neutral-divider focus:border-cta rounded-lg outline-none w-full h-12 text-[#062A1C] text-sm transition-colors" />
          </label>
          <label class="block">
            <span class="label">${esc(t("العنوان"))}</span>
            <input type="text" name="line1" required placeholder="رقم الشقة والمبنى واسم الشارع"
                   class="mt-1 px-3 border border-neutral-divider focus:border-cta rounded-lg outline-none w-full h-12 text-[#062A1C] text-sm transition-colors" />
          </label>
          <label class="block">
            <span class="label">${esc(t("المنطقة والمدينة"))}</span>
            <input type="text" name="line2" required placeholder="المنطقة، المدينة"
                   class="mt-1 px-3 border border-neutral-divider focus:border-cta rounded-lg outline-none w-full h-12 text-[#062A1C] text-sm transition-colors" />
          </label>
          <label class="flex items-center gap-2 py-1 cursor-pointer">
            <input type="checkbox" name="main" class="accent-[#163300] size-4" />
            <span class="text-[#062A1C] text-sm">${esc(t("اجعله العنوان الرئيسي"))}</span>
          </label>
          <button type="submit" class="bg-cta hover:bg-cta-hover mt-1 py-3 rounded-full font-semibold text-white text-sm transition-colors">${esc(t("حفظ العنوان"))}</button>
        </form>
      </div>
    </div>

    <!-- Location bottom sheet -->
    <!-- Bottom sheet on phones, centred dialog from xl — the live site opens
         this as a popup on desktop, where a full-width sheet pinned to the
         bottom of a 1440px window reads as a mobile pattern out of place. -->
    <div data-sheet="location" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-label="أختار منطقة التوصيل">
      <!-- Drag affordance: meaningless once this is a centred dialog. -->
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-center mb-4">
        <h2 class="font-bold text-[#062A1C] text-lg">أختار منطقة التوصيل</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-interaction-base rounded-full w-8 h-8 text-[#062A1C]" aria-label="إغلاق">${ICON.close}</button>
      </div>
      <form data-location-form class="flex flex-col gap-3">
        <label class="block">
          <span class="label">المدينة</span>
          <select class="select-control mt-1 px-3 border border-neutral-divider rounded-lg w-full h-12 text-[#062A1C] placeholder-select">
            ${["القاهرة", "الجيزه", "الاسكندريه", "القليوبيه", "الشرقيه", "الدقهليه", "المنوفيه", "الغربيه"]
              .map((c) => `<option>${c}</option>`)
              .join("")}
          </select>
        </label>
        <label class="block">
          <span class="label">المنطقة</span>
          <select class="select-control mt-1 px-3 border border-neutral-divider rounded-lg w-full h-12 text-[#062A1C] placeholder-select">
            ${["التجمع الخامس", "مدينه نصر", "المعادي", "الزمالك", "هليوبوليس", "الشروق", "الرحاب", "المقطم"]
              .map((a) => `<option>${a}</option>`)
              .join("")}
          </select>
        </label>
        <button type="submit" class="bg-cta hover:bg-cta-hover mt-2 py-3 rounded-full font-semibold text-white transition-colors">تأكيد المنطقة</button>
      </form>
    </div>

    <div id="toast-container"></div>`;
  }

  /* ---------------------------------------------------------------
     Overlay open/close plumbing
     --------------------------------------------------------------- */
  const openMap = {
    cart: '[data-drawer="cart"]',
    menu: '[data-drawer="menu"]',
    search: '[data-modal="search"]',
    locale: '[data-modal="locale"]',
    address: '[data-modal="address"]',
    location: '[data-sheet="location"]',
    accountMenu: '[data-sheet="account-menu"]',
  };
  let openEl = null;

  function openOverlay(key) {
    const sel = openMap[key];
    if (!sel) return;
    const el = document.querySelector(sel);
    const backdrop = document.querySelector("[data-backdrop]");
    if (!el) return;
    openEl = el;
    el.classList.add("is-open");
    if (backdrop) backdrop.classList.add("is-open");
    document.body.classList.add("no-scroll");
    const input = el.querySelector("[data-search-input]");
    if (input) {
      // Warm the catalogue while the shopper is still reaching for the
      // keyboard, so the first keystroke renders instead of waiting on I/O.
      loadCatalog();
      setTimeout(() => input.focus(), 80);
    }
  }

  function closeOverlay() {
    document
      .querySelectorAll(".side-drawer.is-open, .modal-shell.is-open, .bottom-sheet.is-open")
      .forEach((el) => el.classList.remove("is-open"));
    const backdrop = document.querySelector("[data-backdrop]");
    if (backdrop) backdrop.classList.remove("is-open");
    document.body.classList.remove("no-scroll");
    openEl = null;
  }

  /* ---------------------------------------------------------------
     Site search

     The magnifier was in the masthead of all 130 pages and did nothing:
     the modal took focus and had no handler, no results and no empty
     state, so every query was a dead end.

     This is the one place scripts.js reads catalog.json at runtime.
     Everywhere else the catalogue is baked in at build time on purpose,
     but search cannot be — it has to reach products that are not on the
     current page. Fetched once, lazily, on first open, and cached; a
     failed fetch degrades to a message rather than a spinner that never
     resolves.
     --------------------------------------------------------------- */
  let catalogPromise = null;

  function loadCatalog() {
    if (!catalogPromise) {
      catalogPromise = fetch("data/catalog.json")
        .then((r) => {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then((d) => d.products || [])
        .catch(() => null);
    }
    return catalogPromise;
  }

  /*
   * Arabic needs folding before it can be matched the way a shopper types.
   * The catalogue writes قهوة with a ة and shoppers type ه; ى and ي, أ إ آ
   * and ا are used interchangeably; and the tashkeel that appears in a few
   * product names is never typed at all. Without this, searching "قهوه"
   * returns nothing while "قهوة" returns twelve products, which reads as a
   * broken search rather than a spelling difference.
   */
  function fold(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/[ً-ْـ]/g, "")
      .replace(/[أإآٱ]/g, "ا")
      .replace(/ى/g, "ي")
      .replace(/ة/g, "ه")
      .replace(/[ؤئ]/g, "ء")
      .replace(/\s+/g, " ")
      .trim();
  }

  function searchProducts(products, q) {
    const needle = fold(q);
    if (!needle) return [];
    const terms = needle.split(" ");
    const scored = [];
    products.forEach((p) => {
      const ar = fold(p.nameAr);
      const en = fold(p.name);
      // Every term must appear somewhere, so "قهوه تركي" narrows rather
      // than widening the way an OR match would.
      if (!terms.every((t2) => ar.includes(t2) || en.includes(t2))) return;
      // A prefix match is what the shopper is most likely reaching for, so
      // it outranks a match buried mid-name; popularityRank breaks ties
      // with the client's real sales order rather than catalogue order.
      const starts = ar.startsWith(terms[0]) || en.startsWith(terms[0]);
      scored.push({ p: p, score: (starts ? 0 : 1000) + (p.popularityRank || 999) });
    });
    scored.sort((a, b) => a.score - b.score);
    return scored.slice(0, 24).map((x) => x.p);
  }

  function searchResultHTML(p) {
    const name = currentLang() === "en" ? p.name || p.nameAr : p.nameAr || p.name;
    const img = (p.images && p.images[0]) || p.image || "";
    return `
      <a href="product-${esc(String(p.id))}.html"
         class="flex items-center gap-3 hover:bg-interaction-base px-5 py-3 border-neutral-divider border-b last:border-b-0 transition-colors">
        <img src="${esc(img)}" alt="" loading="lazy"
             class="bg-interaction-base shrink-0 p-1 rounded-lg w-12 h-12 object-contain" />
        <span class="flex-1 min-w-0 font-semibold text-[#062A1C] text-sm line-clamp-2">${esc(name)}</span>
        <span class="bg-accent-yellow shrink-0 px-2 py-0.5 rounded font-bold text-[#062A1C] text-xs latin">EGP ${esc(
          String(p.price),
        )}</span>
      </a>`;
  }

  function initSearch() {
    const modal = document.querySelector('[data-modal="search"]');
    if (!modal) return;
    const input = modal.querySelector("[data-search-input]");
    const results = modal.querySelector("[data-search-results]");
    const status = modal.querySelector("[data-search-status]");
    const idle = modal.querySelector("[data-search-idle]");
    if (!input || !results || !status || !idle) return;

    let timer = null;
    let token = 0;

    function render(q) {
      const mine = ++token;
      if (!fold(q)) {
        results.hidden = true;
        status.hidden = true;
        results.innerHTML = "";
        idle.hidden = false;
        return;
      }
      idle.hidden = true;
      loadCatalog().then((products) => {
        // A slow response for an abandoned query must not overwrite the
        // results of the one the shopper is actually looking at.
        if (mine !== token) return;
        status.hidden = false;
        if (!products) {
          results.hidden = true;
          results.innerHTML = "";
          status.textContent = t("تعذر تحميل نتائج البحث. حاول مرة أخرى.");
          return;
        }
        const hits = searchProducts(products, q);
        if (!hits.length) {
          results.hidden = true;
          results.innerHTML = "";
          status.textContent = t("لا توجد نتائج لـ") + ' "' + q.trim() + '"';
          return;
        }
        status.textContent = hits.length + " " + t("نتيجة");
        results.innerHTML = hits.map(searchResultHTML).join("");
        results.hidden = false;
        results.scrollTop = 0;
      });
    }

    input.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(() => render(input.value), 140);
    });

    // Enter with a single hit is unambiguous — go there rather than making
    // the shopper reach for the mouse to click the only row on screen.
    input.addEventListener("keydown", (e) => {
      if (e.key !== "Enter") return;
      const first = results.querySelector("a");
      if (first) {
        e.preventDefault();
        window.location.href = first.getAttribute("href");
      }
    });

    modal.addEventListener("click", (e) => {
      const seed = e.target.closest("[data-search-seed]");
      if (!seed) return;
      input.value = seed.dataset.searchSeed;
      input.focus();
      render(input.value);
    });
  }

  /* ---------------------------------------------------------------
     Toast
     --------------------------------------------------------------- */
  function toast(msg, type) {
    const c = document.getElementById("toast-container");
    if (!c) return;
    const el = document.createElement("div");
    el.className = "toast" + (type === "error" ? " toast--error" : "");
    el.textContent = msg;
    c.appendChild(el);
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transition = "opacity .3s";
      setTimeout(() => el.remove(), 300);
    }, 3000);
  }
  window.kToast = toast;

  /* ---------------------------------------------------------------
     Carousel (Swiper replacement)
     --------------------------------------------------------------- */
  /*
   * Browsers disagree on how scrollLeft is reported inside an RTL container.
   * Detect it once, then express every position as a *logical* offset where
   * 0 is the start of the track and `maxPos()` is the end — in both
   * directions. Everything below is written against that logical axis.
   */
  const rtlScrollType = (function detect() {
    const probe = document.createElement("div");
    probe.dir = "rtl";
    probe.style.cssText =
      "position:absolute;top:-9999px;width:100px;height:1px;overflow:scroll;visibility:hidden";
    probe.innerHTML = '<div style="width:200px;height:1px"></div>';
    document.body.appendChild(probe);
    let type = "negative"; // spec: 0 at the right edge, negative going left
    if (probe.scrollLeft > 0) {
      type = "positive"; // legacy WebKit: starts at max, counts down
    } else {
      probe.scrollLeft = 1;
      if (probe.scrollLeft !== 0) type = "positive";
    }
    probe.remove();
    return type;
  })();

  function initCarousel(root) {
    const track = root.querySelector(".carousel-track");
    if (!track) return;
    const prev = root.querySelector(".carousel-prev");
    const next = root.querySelector(".carousel-next");
    const dotsWrap = root.querySelector(".carousel-dots");

    const isRTL = () => getComputedStyle(track).direction === "rtl";
    const maxPos = () =>
      Math.max(0, track.scrollWidth - track.clientWidth - 1);

    // Physical scrollLeft -> logical offset (0 = start of track).
    function getPos() {
      const sl = track.scrollLeft;
      if (!isRTL()) return sl;
      return rtlScrollType === "negative" ? -sl : maxPos() - sl;
    }

    // Logical offset -> physical scrollLeft.
    function setPos(pos) {
      const p = Math.max(0, Math.min(maxPos(), pos));
      if (!isRTL()) track.scrollLeft = p;
      else if (rtlScrollType === "negative") track.scrollLeft = -p;
      else track.scrollLeft = maxPos() - p;
    }

    function slideStep() {
      const first = track.querySelector(".carousel-slide");
      if (!first) return track.clientWidth;
      const style = getComputedStyle(track);
      const gap = parseFloat(style.columnGap || style.gap || "16") || 16;
      return first.getBoundingClientRect().width + gap;
    }

    function update() {
      const pos = getPos();
      const max = maxPos();
      if (prev) prev.classList.toggle("is-disabled", pos <= 1);
      if (next) next.classList.toggle("is-disabled", pos >= max);
      if (dotsWrap) {
        const dots = dotsWrap.querySelectorAll(".carousel-dot");
        const idx = Math.round(pos / slideStep());
        dots.forEach((d, i) => d.classList.toggle("is-active", i === idx));
      }
    }

    if (prev)
      prev.addEventListener("click", () => setPos(getPos() - slideStep()));
    if (next)
      next.addEventListener("click", () => setPos(getPos() + slideStep()));

    if (dotsWrap) {
      const slides = track.querySelectorAll(".carousel-slide");
      const perView = Math.max(1, Math.round(track.clientWidth / slideStep()));
      const pages = Math.max(1, slides.length - perView + 1);
      dotsWrap.innerHTML = "";
      for (let i = 0; i < pages; i++) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "carousel-dot" + (i === 0 ? " is-active" : "");
        dot.addEventListener("click", () => setPos(i * slideStep()));
        dotsWrap.appendChild(dot);
      }
    }

    track.addEventListener("scroll", () => window.requestAnimationFrame(update));
    window.addEventListener("resize", update);
    update();

    if (root.hasAttribute("data-autoplay")) {
      setInterval(() => {
        if (getPos() >= maxPos()) setPos(0);
        else setPos(getPos() + slideStep());
      }, 4500);
    }
  }

  /* ---------------------------------------------------------------
     Accordion / tabs / steppers / forms
     --------------------------------------------------------------- */
  function initAccordions(scope) {
    scope.querySelectorAll("[data-accordion]").forEach((acc) => {
      acc.querySelectorAll(".accordion-item").forEach((item) => {
        const btn = item.querySelector(".accordion-trigger");
        if (!btn) return;
        btn.addEventListener("click", () => {
          const isOpen = item.classList.contains("is-open");
          if (!acc.hasAttribute("data-accordion-multi")) {
            acc
              .querySelectorAll(".accordion-item.is-open")
              .forEach((o) => o.classList.remove("is-open"));
          }
          item.classList.toggle("is-open", !isOpen);
        });
      });
    });
  }

  function initTabs(scope) {
    scope.querySelectorAll("[data-tabs]").forEach((tabs) => {
      const btns = tabs.querySelectorAll(".tab-btn");
      const panels = tabs.querySelectorAll(".tab-panel");
      btns.forEach((btn) => {
        btn.addEventListener("click", () => {
          const target = btn.getAttribute("data-tab");
          btns.forEach((b) =>
            b.classList.toggle("is-active", b === btn),
          );
          panels.forEach((p) =>
            p.toggleAttribute("hidden", p.getAttribute("data-panel") !== target),
          );
        });
      });
    });
  }

  /* ---------------------------------------------------------------
     Product gallery

     Thumbnails swap the main image. Selection is `aria-pressed` and nothing
     else — styles.css draws the ring off that selector — so the accessible
     state and the painted state are the same attribute and cannot drift. The
     same contract the favourites heart uses.

     The swap cross-fades: the main image is faded out, the src is changed
     while it is invisible, and it fades back in once the new file has
     decoded. Waiting on decode matters — swapping src on a visible <img>
     paints a blank frame while the next photo loads, and these are real
     900px photographs, not sprites.
     --------------------------------------------------------------- */
  function initGallery(scope) {
    scope.querySelectorAll("[data-gallery]").forEach((gallery) => {
      const main = gallery.querySelector("[data-gallery-main]");
      const thumbs = [...gallery.querySelectorAll("[data-gallery-thumb]")];
      if (!main || !thumbs.length) return;

      const plate = gallery.querySelector("[data-gallery-plate]");

      const show = (btn) => {
        const img = btn.querySelector("img");
        const src = img && img.getAttribute("src");
        if (!src || src === main.getAttribute("src")) return;

        thumbs.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        /* Carry the fill mode across with the image. The main shot is a
           background-isolated cut-out and has to sit inside the plate's
           padding; the gallery shots are photographs with their own
           backgrounds and fill the frame. Painting a photograph "contain"
           leaves it marooned in a border of plate colour. */
        if (plate) plate.dataset.fill = btn.dataset.fill || "contain";

        const swap = () => {
          main.setAttribute("src", src);
          // Only reveal once the bitmap is ready. decode() is unsupported on
          // older Safari, hence the fallback to the load event.
          const reveal = () => main.removeAttribute("data-swapping");
          if (main.decode) main.decode().then(reveal, reveal);
          else main.addEventListener("load", reveal, { once: true });
        };

        if (reduceMotion()) {
          swap();
          return;
        }
        main.dataset.swapping = "true";
        // One frame of fade-out before the src changes, so the old photo is
        // gone rather than cut. The timeout matches the CSS transition.
        setTimeout(swap, 180);
      };

      thumbs.forEach((btn) => btn.addEventListener("click", () => show(btn)));
    });
  }

  /* ---------------------------------------------------------------
     Size + quantity -> price

     The size chips are real SKUs (see build/fetch_sizes.py), each carrying its
     own live price and product id. Choosing one has to do three things, and
     missing any of them leaves the page lying to the shopper:

       1. repoint the displayed price at that size's price,
       2. repoint `data-price` AND `data-id` on the [data-product] host, so the
          cart adds the SKU that was actually chosen rather than whichever one
          the page happened to render with,
       3. survive the quantity multiplier without compounding.

     (3) is why the unit price lives in its own attribute. Multiplying the
     DISPLAYED number would square it on the second press.
     --------------------------------------------------------------- */
  function initSizeAndPrice(scope) {
    (scope || document).querySelectorAll("[data-product]").forEach((host) => {
      const display = host.querySelector("[data-price-display]");
      if (!display) return;
      const breakdown = host.querySelector("[data-price-breakdown]");
      const qtyEl = host.querySelector("[data-stepper] [data-qty]");
      const chips = [...host.querySelectorAll("[data-size-option]")];

      const paint = () => {
        const unit = Number(display.dataset.unitPrice) || 0;
        const qty = Math.max(1, parseInt(qtyEl && qtyEl.textContent, 10) || 1);
        display.textContent = egp(unit * qty);
        // The per-unit line only earns its space once it differs from the
        // total, i.e. from the second unit onward.
        if (breakdown) {
          breakdown.hidden = qty < 2;
          breakdown.textContent = qty < 2 ? "" : egp(unit) + " × " + qty;
        }
      };

      chips.forEach((chip) => {
        chip.addEventListener("change", () => {
          if (!chip.checked) return;
          const price = Number(chip.dataset.sizePrice) || 0;
          display.dataset.unitPrice = price;
          // Point the cart at the chosen SKU, not the rendered one.
          host.dataset.price = price;
          if (chip.dataset.sizeId) host.dataset.id = chip.dataset.sizeId;
          paint();
          if (!reduceMotion() && display.animate) {
            display.animate(
              [{ transform: "scale(1)" }, { transform: "scale(1.06)" }, { transform: "scale(1)" }],
              { duration: 240, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
            );
          }
        });
      });

      // The stepper owns the number; this just recomputes after it changes.
      // Listening on the host rather than the buttons keeps it working if the
      // stepper is ever re-rendered.
      host.addEventListener("click", (e) => {
        if (e.target.closest("[data-stepper] [data-step]")) setTimeout(paint, 0);
      });

      paint();
    });
  }

  function initSteppers(scope) {
    scope.querySelectorAll("[data-stepper]").forEach((st) => {
      const qtyEl = st.querySelector("[data-qty]");
      st.querySelectorAll("[data-step]").forEach((b) => {
        b.addEventListener("click", () => {
          const delta = parseInt(b.getAttribute("data-step"), 10);
          let v = parseInt(qtyEl.textContent, 10) || 1;
          const next = Math.max(1, v + delta);
          const changed = next !== v;
          qtyEl.textContent = next;
          /* The number slides in from the direction you pressed, so which way
             it moved is legible without reading the digit. At the floor of 1
             nothing changed, so nothing animates — the press is a no-op and
             animating it would imply otherwise. */
          if (changed && !reduceMotion() && qtyEl.animate) {
            qtyEl.animate(
              [
                { transform: "translateY(" + (delta > 0 ? 8 : -8) + "px)", opacity: 0 },
                { transform: "translateY(0)", opacity: 1 },
              ],
              { duration: 200, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
            );
          }
        });
      });
    });
  }

  /* ---------------------------------------------------------------
     Scroll reveal

     Sections fade and rise once, the first time they come into view. This is
     the bulk of what makes the page feel current, and it is cheap: one
     IntersectionObserver, unobserved after firing, and entirely skipped when
     the user asks for reduced motion.

     Anything already on screen at load is revealed immediately without
     animation, so the fold never appears to animate in after the fact.
     --------------------------------------------------------------- */
  function initReveal(scope) {
    const els = [...(scope || document).querySelectorAll("[data-reveal]")];
    if (!els.length) return;
    // Only now does the hidden state exist at all — see the .js-reveal gate in
    // styles.css. Set here rather than in markup so a JS failure degrades to
    // "no animation" instead of "no content".
    document.documentElement.classList.add("js-reveal");
    if (reduceMotion() || !("IntersectionObserver" in window)) {
      els.forEach((el) => el.setAttribute("data-reveal", "in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.setAttribute("data-reveal", "in");
          io.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.06 },
    );
    const pending = [];
    els.forEach((el) => {
      if (el.getBoundingClientRect().top < window.innerHeight) {
        el.setAttribute("data-reveal", "in"); // above the fold: no animation
      } else {
        pending.push(el);
        io.observe(el);
      }
    });

    /*
     * Failsafe. The reveal now applies to every <section> on all 130 pages,
     * so the cost of the observer not firing went from "one home page rail
     * stays faded" to "most of the site does" — and IntersectionObserver
     * does NOT fire in every context (it is inert in a hidden/background
     * document, which is exactly where this was being tested; a
     * default-config control observer did not fire either).
     *
     * The guiding rule for this system has always been that a failure
     * degrades to UNANIMATED, never to INVISIBLE. The .js-reveal gate gives
     * that when JS is off entirely; this gives it when JS runs but the
     * observer never reports. Worst case the shopper gets no animation on
     * content they had not reached yet — which they cannot tell apart from
     * having already scrolled past it.
     *
     * Deliberately not rAF- or scroll-driven: a backgrounded tab throttles
     * both, and this has to survive precisely the case where the observer
     * has already failed.
     */
    if (pending.length) {
      setTimeout(() => {
        pending.forEach((el) => {
          if (el.getAttribute("data-reveal") !== "in") {
            el.setAttribute("data-reveal", "in");
            io.unobserve(el);
          }
        });
      }, 2500);
    }
  }

  function initDemoForms(scope) {
    scope.querySelectorAll("[data-newsletter]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        f.reset();
        toast("تم الاشتراك بنجاح! 🎉");
      }),
    );
    scope.querySelectorAll("[data-location-form]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        closeOverlay();
        toast("تم تحديث منطقة التوصيل.");
      }),
    );
    scope.querySelectorAll("[data-demo-form]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        toast(f.getAttribute("data-demo-form") || "تم الإرسال بنجاح.");
        if (f.getAttribute("data-reset") !== "false") f.reset();
        // Optional: navigate to another page after the toast (mock success flow).
        const redirect = f.getAttribute("data-redirect");
        if (redirect) setTimeout(() => (window.location.href = redirect), 850);
      }),
    );
  }

  /* ---------------------------------------------------------------
     Sticky navbar on scroll (desktop) — mirrors useWindowScroll(150)
     --------------------------------------------------------------- */
  function initStickyNav() {
    const nav = document.querySelector("[data-navbar]");
    if (!nav) return;
    const placeholder = document.createElement("div");
    nav.parentNode.insertBefore(placeholder, nav.nextSibling);
    let stuck = false;
    function onScroll() {
      const should = window.scrollY > 150;
      if (should === stuck) return;
      stuck = should;
      /* Positioning is driven by data-stuck, not by Tailwind's `fixed`.
         The bar's base classes include `relative`, which ties `.fixed` on
         specificity and wins on source order, so the utility never took
         effect and this bar never actually stuck. styles.css carries the
         real rule. No inline padding either: the <nav> inside is already
         mx-auto px-4 max-w-[1536px], so it centres itself once fixed. */
      const stickyClasses = ["shadow-md", "animate-slideDown"];
      if (should) {
        placeholder.style.height = nav.offsetHeight + "px";
        nav.dataset.stuck = "true";
        nav.classList.add(...stickyClasses);
      } else {
        placeholder.style.height = "0px";
        delete nav.dataset.stuck;
        nav.classList.remove(...stickyClasses);
      }
      // Search + cart ride along, on the same threshold as the nav.
      document.querySelectorAll("[data-sticky-actions]").forEach((el) => {
        if (should) el.dataset.stuck = "true";
        else delete el.dataset.stuck;
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------------------
     Global click / key delegation
     --------------------------------------------------------------- */
  function initDelegation() {
    document.addEventListener("click", (e) => {
      const opener = e.target.closest("[data-open]");
      if (opener) {
        e.preventDefault();
        openOverlay(opener.getAttribute("data-open"));
        return;
      }
      if (e.target.closest("[data-close]")) {
        closeOverlay();
        return;
      }
      if (e.target.classList.contains("overlay-backdrop")) {
        closeOverlay();
      }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && openEl) closeOverlay();
    });
  }

  /* ---------------------------------------------------------------
     Public re-init hook for dynamically added markup
     --------------------------------------------------------------- */
  /* Password reveal toggles on the auth forms. */
  function initPasswordReveals(scope) {
    scope.querySelectorAll("[data-reveal]").forEach((btn) => {
      const input = scope.getElementById
        ? scope.getElementById(btn.getAttribute("data-reveal"))
        : document.getElementById(btn.getAttribute("data-reveal"));
      if (!input) return;
      btn.addEventListener("click", () => {
        const shown = input.type === "text";
        input.type = shown ? "password" : "text";
        btn.setAttribute(
          "aria-label",
          shown ? "إظهار كلمة السر" : "إخفاء كلمة السر",
        );
      });
    });
  }

  /* ---------------------------------------------------------------
     Listing filter + sort

     The export is static, so filtering happens over the cards already in the
     DOM — no fetch, still works from file://. Cards carry data-cat / data-price
     / data-id from catalog.json.

     Only chips rendered with a `data-filter` slug take part. Sub-category
     chips deliberately have none: the catalogue has no sub-category field, so
     filtering by them would empty the grid (see DESIGN-NOTES).
     --------------------------------------------------------------- */
  const CHIP_ON = ["bg-cta", "text-white", "border-cta"];
  const CHIP_OFF = ["chip-filter", "bg-white", "text-[#062A1C]",
                    "border-neutral-divider", "hover:border-cta"];

  /* ---------------------------------------------------------------
     Cart store

     Single source of truth for cart state, persisted to localStorage so it
     survives navigation between the standalone pages. No fetch — the store
     reads product details straight off `[data-product]` markup, so it works
     from file:// like the rest of the export.

     Every mutation dispatches a `cart:change` CustomEvent on `document`:

       document.addEventListener("cart:change", (e) => {
         e.detail.reason   // "add" | "qty" | "remove" | "clear" | "init"
         e.detail.product  // the item involved (absent for clear/init)
         e.detail.items    // full array after the change
         e.detail.count    // total units
         e.detail.subtotal // EGP
       });

     That event is the hook for micro-interactions — fly-to-cart, badge bounce,
     row collapse — none of which belong in here.
     --------------------------------------------------------------- */
  const CART_KEY = "abuauf:cart";

  /*
   * Seed for a first-ever visit only, so a fresh browser does not land on an
   * empty cart and lose the design. Real catalogue items. Written once, on the
   * first load where no cart key exists; after that the shopper owns the cart,
   * including deliberately emptying it.
   */
  /*
   * `id` MUST be the catalog.json product id — the same value product cards
   * carry in `data-id`. These were previously the barcodes lifted off the
   * image filenames ("6223006310759", "2000102000000"), which match no card,
   * so adding a seeded product from its own card created a SECOND line
   * instead of incrementing the first. Keep these in sync with the catalogue.
   */
  const CART_SEED = [
    { id: "1431", name: "تمر صحاري بالشيكولاته و اللوز - 300 جم", price: 220, image: "images/abuauf/products/6223006310759.webp", qty: 1 },
    { id: "1445", name: "قراصيا بدون نواه - 100 جم", price: 72.5, image: "images/abuauf/products/2000102000000.webp", qty: 1 },
  ];

  const Cart = (function () {
    let items = [];

    function load() {
      try {
        const raw = localStorage.getItem(CART_KEY);
        // No key at all = first ever visit, so seed. An empty array is a
        // shopper who emptied their cart on purpose — leave it alone.
        items = raw === null ? CART_SEED.slice() : JSON.parse(raw);
        if (!Array.isArray(items)) items = [];
      } catch (e) {
        items = [];
      }
    }

    function save() {
      try {
        localStorage.setItem(CART_KEY, JSON.stringify(items));
      } catch (e) {
        /* private mode — state still lives for this page view */
      }
    }

    function subtotal() {
      return items.reduce((s, it) => s + Number(it.price) * it.qty, 0);
    }
    function count() {
      return items.reduce((s, it) => s + it.qty, 0);
    }

    function emit(reason, product) {
      save();
      document.dispatchEvent(
        new CustomEvent("cart:change", {
          detail: { reason: reason, product: product || null, items: items.slice(), count: count(), subtotal: subtotal() },
        }),
      );
    }

    return {
      init: function () {
        load();
        emit("init");
      },
      items: function () {
        return items.slice();
      },
      count: count,
      subtotal: subtotal,
      find: function (id) {
        return items.find((it) => String(it.id) === String(id)) || null;
      },
      add: function (product, qty) {
        qty = Math.max(1, parseInt(qty, 10) || 1);
        const existing = items.find((it) => String(it.id) === String(product.id));
        if (existing) existing.qty += qty;
        else items.push({ id: product.id, name: product.name, price: Number(product.price), image: product.image, qty: qty });
        emit("add", product);
        return this;
      },
      setQty: function (id, qty) {
        const it = items.find((x) => String(x.id) === String(id));
        if (!it) return this;
        qty = parseInt(qty, 10) || 0;
        if (qty < 1) return this.remove(id);
        it.qty = qty;
        emit("qty", it);
        return this;
      },
      remove: function (id) {
        const i = items.findIndex((x) => String(x.id) === String(id));
        if (i === -1) return this;
        const [gone] = items.splice(i, 1);
        emit("remove", gone);
        return this;
      },
      clear: function () {
        items = [];
        emit("clear");
        return this;
      },
    };
  })();

  window.abuaufCart = Cart;

  /* ---------------------------------------------------------------
     Favourites store

     Deliberately the same shape as the cart store above: localStorage, no
     fetch, product details read straight off `[data-product]` markup so it
     works from file://. Items are {id, name, price, image} — no qty, a
     product is either saved or it isn't.

     Every mutation dispatches a `favs:change` CustomEvent on `document`:

       document.addEventListener("favs:change", (e) => {
         e.detail.reason   // "add" | "remove" | "clear" | "init"
         e.detail.product  // the item involved (absent for clear/init)
         e.detail.items    // full array after the change
         e.detail.count    // number saved
       });

     Before this the heart button on every product card was inert markup —
     184 of them across 7 pages, with no handler anywhere in this file.
     --------------------------------------------------------------- */
  const FAVS_KEY = "abuauf:favs";

  /*
   * Seeded on a first-ever visit only, exactly like CART_SEED and for the
   * same reason: my-account-favorites.html used to hard-code six products,
   * so a fresh browser would otherwise land on an empty favourites page and
   * lose the design. These are those same six, by real catalogue id. Once
   * the shopper touches a heart this is never consulted again.
   */
  const FAVS_SEED = [
    { id: "1320", name: "فول سوداني بالشيكولاتة - 100 جم", price: 35.5, image: "images/abuauf/products/2000208000000.webp" },
    { id: "1280", name: "عين جمل مقشر - 100 جم", price: 121, image: "images/abuauf/products/2000079000000.webp" },
    { id: "1287", name: "كاجو محمص ملح جامبو - 100 جم", price: 156, image: "images/abuauf/products/2000404000000.webp" },
    { id: "10573", name: "سودانى كرى كرى بطعم الجبنة -45 جم", price: 17, image: "images/abuauf/products/6223011434013-6.webp" },
    { id: "1288", name: "فستق امريكى ملح - 100 جم", price: 146.5, image: "images/abuauf/products/2000197000000.webp" },
    { id: "1319", name: "فول سودانى بطعم الجبنه - 100 جم", price: 33, image: "images/abuauf/products/Thumb-2000150000000.webp" },
  ];

  const Favs = (function () {
    let items = [];

    function load() {
      try {
        const raw = localStorage.getItem(FAVS_KEY);
        // No key = first ever visit, so seed. An empty array is a shopper who
        // cleared their favourites on purpose — leave it alone.
        items = raw === null ? FAVS_SEED.slice() : JSON.parse(raw);
        if (!Array.isArray(items)) items = [];
      } catch (e) {
        items = [];
      }
    }

    function save() {
      try {
        localStorage.setItem(FAVS_KEY, JSON.stringify(items));
      } catch (e) {
        /* private mode — state still lives for this page view */
      }
    }

    function emit(reason, product) {
      save();
      document.dispatchEvent(
        new CustomEvent("favs:change", {
          detail: { reason: reason, product: product || null, items: items.slice(), count: items.length },
        }),
      );
    }

    return {
      init: function () {
        load();
        emit("init");
      },
      items: function () {
        return items.slice();
      },
      count: function () {
        return items.length;
      },
      has: function (id) {
        return items.some((it) => String(it.id) === String(id));
      },
      add: function (product) {
        if (this.has(product.id)) return this;
        items.push({ id: product.id, name: product.name, price: Number(product.price), image: product.image });
        emit("add", product);
        return this;
      },
      remove: function (id) {
        const i = items.findIndex((x) => String(x.id) === String(id));
        if (i === -1) return this;
        const [gone] = items.splice(i, 1);
        emit("remove", gone);
        return this;
      },
      /* Returns the new state, so callers can react without re-querying. */
      toggle: function (product) {
        if (this.has(product.id)) {
          this.remove(product.id);
          return false;
        }
        this.add(product);
        return true;
      },
      clear: function () {
        items = [];
        emit("clear");
        return this;
      },
    };
  })();

  window.abuaufFavs = Favs;

  /* ---------------------------------------------------------------
     Demo auth

     A local stand-in for a real session so the account and favourites
     flows can actually be walked end to end. Same contract as the two
     stores above: localStorage, no fetch, an `auth:change` event.

     THIS IS NOT AUTHENTICATION. The credentials are hard-coded below and
     printed on the sign-in page; the check happens in client-side JS that
     anyone can read. It exists so the logged-in chrome and the favourites
     flow are demonstrable in a static export. **Rip this out and replace it
     with the real backend before launch** — see DESIGN-NOTES.
     --------------------------------------------------------------- */
  const AUTH_KEY = "abuauf:auth";
  const DEMO_USER = {
    email: "demo@abuauf.com",
    password: "AbuAuf2026",
    name: "محمد عادل",
    nameEn: "Mohamed Adel",
  };

  const Auth = (function () {
    let user = null;

    function emit(reason) {
      try {
        if (user) localStorage.setItem(AUTH_KEY, JSON.stringify(user));
        else localStorage.removeItem(AUTH_KEY);
      } catch (e) {
        /* private mode — the session still holds for this page view */
      }
      document.dispatchEvent(
        new CustomEvent("auth:change", { detail: { reason: reason, user: user } }),
      );
    }

    return {
      demo: DEMO_USER,
      init: function () {
        try {
          const raw = localStorage.getItem(AUTH_KEY);
          user = raw ? JSON.parse(raw) : null;
        } catch (e) {
          user = null;
        }
        emit("init");
      },
      user: function () {
        return user ? Object.assign({}, user) : null;
      },
      isAuthed: function () {
        return !!user;
      },
      /* Returns true on success, false on bad credentials. */
      login: function (email, password) {
        const ok =
          String(email || "").trim().toLowerCase() === DEMO_USER.email &&
          String(password || "") === DEMO_USER.password;
        if (!ok) return false;
        user = { email: DEMO_USER.email, name: DEMO_USER.name, nameEn: DEMO_USER.nameEn };
        emit("login");
        return true;
      },
      logout: function () {
        user = null;
        emit("logout");
        return this;
      },
    };
  })();

  window.abuaufAuth = Auth;

  /* Read a product off the nearest [data-product] element. */
  function productFrom(el) {
    const host = el.closest("[data-product]");
    if (!host) return null;
    const d = host.dataset;
    if (!d.id || !d.name) return null;
    return { id: d.id, name: d.name, price: Number(d.price) || 0, image: d.image || "" };
  }

  const egp = (n) => "EGP " + (Math.round(n * 100) / 100).toFixed(2);

  /* ---------------------------------------------------------------
     Language switcher

     Flips `dir` and `lang` on <html> so the RTL↔LTR layout can actually be
     exercised, and remembers the choice across pages via localStorage.

     It does NOT translate copy. Every string in this build is Arabic — there
     is no English content to switch to, and machine-translating the client's
     store into English would be inventing copy. So English mode is an
     honest direction/layout test: the writing direction, logical properties
     and mirrored components all flip, the words do not. Real bilingual
     support is a separate piece of work needing English copy (DESIGN-NOTES).
     --------------------------------------------------------------- */
  const LANG_KEY = "abuauf:lang";

  function applyLang(code) {
    const l = LANGS.find((x) => x.code === code) || LANGS[1];
    const c = currentCountry();
    document.documentElement.setAttribute("lang", l.code);
    document.documentElement.setAttribute("dir", l.dir);
    document.querySelectorAll("[data-lang-label]").forEach((el) => {
      el.textContent = l.code === "ar" ? c.short + " (العربية)" : c.en + " (English)";
    });
    document.querySelectorAll("[data-country-flag]").forEach((el) => {
      el.src = c.flag;
    });
    try {
      localStorage.setItem(LANG_KEY, l.code);
    } catch (e) {
      /* private mode — the toggle still works for this page view */
    }
  }

  /*
   * Re-render the JS-injected chrome in the new language and swap product
   * titles to the English names that already exist in catalog.json. Body copy
   * baked into the page stays Arabic — there is no English source for it.
   */
  /* Apply the current language to build-time page content: the catalogue's
     real English product names, then the exact-match dictionary pass.

     Split out of repaintForLang() so it can ALSO run on first paint. Without
     that, opening any page with English already stored left every build-time
     string in Arabic — the JS-injected chrome came out English because it is
     rendered through t() at render time, but translateDocument() only ever
     ran on a toggle click, never on load. So the language appeared to change
     on the page you clicked and then half-revert on every page you navigated
     to. */
  function applyLangToContent() {
    // data-name is Arabic, data-name-en is the catalogue's real English
    // name. Nothing invented here.
    const en = currentLang() === "en";
    document.querySelectorAll("[data-product][data-name-en]").forEach((card) => {
      const target = card.querySelector("[data-product-title]");
      if (!target) return;
      target.textContent = en ? card.dataset.nameEn : card.dataset.name;
    });
    translateDocument();
  }

  function repaintForLang() {
    const header = document.getElementById("site-header");
    const footer = document.getElementById("site-footer");
    const overlays = document.getElementById("site-overlays");
    if (header) header.innerHTML = headerHTML();
    if (footer) footer.innerHTML = footerHTML();
    if (overlays) overlays.innerHTML = overlaysHTML();

    applyLangToContent();

    initMegaMenu();
    initLangSwitcher(true);
    window.kInit(document);
    renderCart();
    document.dispatchEvent(new CustomEvent("auth:change", { detail: { reason: "lang", user: Auth.user() } }));
    // Heart aria-labels come from t(), so they have to be re-derived here —
    // repaint replaces the chrome but the cards are build-time markup.
    syncFavButtons();
  }

  function initLangSwitcher(skipApply) {
    if (!skipApply) {
      let stored = "ar";
      try {
        stored = localStorage.getItem(LANG_KEY) || "ar";
      } catch (e) {
        /* ignore */
      }
      applyLang(stored);
    }

    /* The choices live in the locale modal now and commit on تطبيق alone —
       one repaint however much changed. Delegated on document (bound once,
       via the guard below) so it survives the chrome re-render that apply
       itself triggers. */
    if (initLangSwitcher._bound) return;
    initLangSwitcher._bound = true;
    document.addEventListener("click", (e) => {
      const apply = e.target.closest("[data-locale-apply]");
      if (!apply) return;
      const modal = apply.closest('[data-modal="locale"]');
      const country = modal.querySelector('input[name="locale-country"]:checked');
      const lang = modal.querySelector('input[name="locale-lang"]:checked');
      const langChanged = lang && lang.value !== currentLang();
      const countryChanged = country && country.value !== currentCountry().code;
      if (country) {
        try {
          localStorage.setItem(COUNTRY_KEY, country.value);
        } catch (err) {
          /* ignore */
        }
      }
      closeOverlay();
      if (!langChanged && !countryChanged) return;
      // One repaint covers both: applyLang re-reads the country for the
      // masthead label, and repaintForLang rebuilds the chrome (including
      // this modal, whose checked states are written at render time).
      applyLang(lang ? lang.value : currentLang());
      repaintForLang();
      toast("تم تطبيق التفضيلات");
    });
  }

  /* ---------------------------------------------------------------
     Cart rendering — drawer body, badge, cart page

     Everything here is a pure function of Cart state and re-runs on
     `cart:change`. Nothing mutates state; the handlers below do that.
     --------------------------------------------------------------- */
  const DELIVERY_FEE = 30;
  const MIN_ORDER = 150;

  /* ---------------------------------------------------------------
     Fly-to-target

     Clones a bit of the page, arcs it to a destination, and resolves when it
     lands. Used for add-to-cart (the product image flies to the cart) and for
     favouriting (a heart flies to the account button).

     Deliberately a ghost clone on `position: fixed` rather than moving the
     real node: the real card must stay put and keep working, and a fixed
     ghost is immune to whatever scroll container it started in.
     --------------------------------------------------------------- */
  const reduceMotion = () =>
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let badgeHold = 0;

  /*
   * Directional roll for a counter. The new value slides in from below on an
   * increment and from above on a decrement, so the motion itself says which
   * way the number went — a swap-and-pulse only says "something changed".
   * The write happens unconditionally; only the motion is optional, so
   * reduced-motion users get the same truth without the ride.
   */
  function rollTo(el, value, dir) {
    const next = String(value);
    if (el.textContent === next) return;
    el.textContent = next;
    if (reduceMotion() || !el.animate) return;
    el.animate(
      [
        { transform: "translateY(" + (dir < 0 ? "-0.55em" : "0.55em") + ")", opacity: 0 },
        { transform: "translateY(0)", opacity: 1 },
      ],
      { duration: 240, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
    );
  }

  function syncCartBadges() {
    const n = Cart.count();
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      const old = parseInt(el.textContent, 10) || 0;
      // Only a badge the shopper can currently see earns the roll — animating
      // inside a hidden badge, or on first paint, is motion with no witness.
      if (el.hidden || !el.offsetParent || old === n) el.textContent = n;
      else rollTo(el, n, n > old ? 1 : -1);
      el.hidden = n === 0;
    });
  }

  /* The catch: the destination dips under the landing's weight and springs
     back. Deliberately smaller travel than pulse() — it plays on the whole
     48px cart button, where a 1.28 spike reads as a glitch, not a catch. */
  function squash(el) {
    if (!el || reduceMotion() || !el.animate) return;
    el.animate(
      [
        { transform: "scale(1)" },
        { transform: "scale(0.9)", offset: 0.3 },
        { transform: "scale(1.06)", offset: 0.65 },
        { transform: "scale(1)" },
      ],
      { duration: 360, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
    );
  }

  /* A short scale pulse on the destination, so the landing is felt. */
  function pulse(el) {
    if (!el || reduceMotion() || !el.animate) return;
    el.animate(
      [
        { transform: "scale(1)" },
        { transform: "scale(1.28)", offset: 0.4 },
        { transform: "scale(0.94)", offset: 0.72 },
        { transform: "scale(1)" },
      ],
      { duration: 420, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
    );
  }

  /*
   * `ghostHTML` overrides what flies; by default the source element is cloned.
   * Resolves as soon as the ghost lands (or immediately when motion is
   * reduced / the geometry is unusable), so callers can chain the landing
   * beat without caring which happened.
   *
   * The flight is two staged movements, not one:
   *
   *   1. PICK UP — the ghost stays exactly where the source is and condenses
   *      into a small rounded, shadowed white tile. The product visibly
   *      gathers into something pocket-sized before anything is thrown.
   *   2. THROW — the tile arcs to the target and shrinks the rest of the way
   *      into the cart, carrying its gathered scale the whole distance.
   *
   * Splitting them is the whole reason this reads as smooth. One keyframe
   * list that both gathers and travels has to compromise its easing across the
   * two, and the throw ends up starting before the eye has found the thing
   * being thrown — which is exactly what the single-stage version did.
   *
   * opts.card   — draw the tile chrome. Hearts fly bare (opts omitted).
   * opts.quick  — tighter and faster, for repeat taps on a card stepper.
   * opts.tag    — small text chip riding along with the tile, e.g. "+1".
   */
  function flyTo(sourceEl, targetEl, ghostHTML, opts) {
    opts = opts || {};
    if (!sourceEl || !targetEl || reduceMotion() || !document.body.animate) {
      return Promise.resolve(false);
    }
    const s = sourceEl.getBoundingClientRect();
    const t = targetEl.getBoundingClientRect();
    if (!s.width || !s.height || !t.width) return Promise.resolve(false);

    const ghost = document.createElement("div");
    ghost.className = "fly-ghost" + (opts.card ? " fly-ghost--card" : "");
    ghost.style.cssText =
      "position:fixed;z-index:200;pointer-events:none;left:" +
      s.left + "px;top:" + s.top + "px;width:" + s.width + "px;height:" + s.height + "px;";

    /* The plate is a separate node from the ghost so the two stages never
       fight over one transform: the plate owns the pick-up scale (a CSS
       transition), the ghost owns the travel (a WAAPI animation). */
    const plate = document.createElement("div");
    plate.className = "fly-ghost__plate";
    if (ghostHTML) plate.innerHTML = ghostHTML;
    else {
      const clone = sourceEl.cloneNode(true);
      clone.removeAttribute("id");
      clone.style.width = "100%";
      clone.style.height = "100%";
      plate.appendChild(clone);
    }
    ghost.appendChild(plate);
    if (opts.tag) {
      const tag = document.createElement("span");
      tag.className = "fly-ghost__tag latin";
      tag.textContent = opts.tag;
      ghost.appendChild(tag);
    }
    document.body.appendChild(ghost);

    /*
     * Clamp the destination into the viewport.
     *
     * Normally the cart button is on screen wherever you are on the page:
     * [data-sticky-actions] goes position:fixed once you scroll and parks it
     * at top 68. But that only happens on a scroll *handler*, so there is a
     * window — a click landing in the same tick as a programmatic scroll, or
     * any page without that bar — where the only cart button is the masthead
     * one, sitting a thousand-odd pixels above the viewport. Measured at -1514
     * from the home page's first rail. Unclamped, the item is thrown off the
     * top of the screen and the shopper sees nothing but the badge tick.
     * Clamping keeps the heading and stops the item at the edge instead; when
     * the target is already visible this is inert.
     */
    const edge = 24;
    const tx = t.left + t.width / 2;
    const ty = Math.min(Math.max(t.top + t.height / 2, edge), window.innerHeight - edge);

    const dx = tx - (s.left + s.width / 2);
    const dy = ty - (s.top + s.height / 2);
    // Arc height scales with distance but is capped, so a short hop does not
    // loop absurdly and a long one still reads as a throw rather than a slide.
    const lift = Math.min(160, Math.hypot(dx, dy) * 0.32) + 40;

    const pickupMs = opts.card ? (opts.quick ? 150 : 230) : 0;
    const flightMs = opts.quick ? 560 : 700;

    /* Force a style flush so the transition has a resolved start value to
       move away from. Deliberately NOT requestAnimationFrame: rAF does not
       fire in a backgrounded tab, so the pick-up would be skipped there and
       could then land *after* the throw had already removed the class. */
    if (pickupMs) {
      void ghost.offsetWidth;
      ghost.classList.add("is-picked");
    }

    return new Promise((resolve) => {
      let done = false;
      const finish = () => {
        if (done) return;
        done = true;
        ghost.remove();
        resolve(true);
      };

      const throwIt = () => {
        // `is-picked` deliberately STAYS on for the whole flight. It is what
        // holds the plate at its gathered-up scale, and dropping it here would
        // ease the tile back to full size just as it starts travelling — the
        // ghost would visibly swell in mid-air. The ghost's own scale keyframes
        // multiply with the plate's, so the tile keeps shrinking all the way
        // into the cart.
        //
        // The path is SAMPLED, not three-point. WAAPI interpolates keyframes
        // linearly in transform space, so with only start/apex/end the "arc"
        // was two straight lines with a corner at the apex — visible on every
        // long throw. Sixteen samples along a real parabola cost nothing and
        // the corner disappears. Time-easing rides on the sample spacing
        // (easeInOut on p), so the overall easing stays: gathers speed,
        // crests, decelerates into the cart.
        const N = 16;
        const frames = [];
        for (let i = 0; i <= N; i++) {
          const t = i / N;
          const p = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
          const x = dx * p;
          // sin(pi*p) peaks at exactly `lift` mid-flight and lands at 0 — the
          // same arc height the old apex keyframe had, without its corner.
          const y = dy * p - lift * Math.sin(Math.PI * p);
          const scale = 1 - 0.84 * p;
          // A held tilt against the direction of travel, righting itself on
          // approach — reads as carried momentum rather than a spin.
          const rot = -7 * Math.sin(Math.PI * p) + 4 * p;
          frames.push({
            transform:
              "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px) " +
              "scale(" + scale.toFixed(3) + ") rotate(" + rot.toFixed(2) + "deg)",
            // Stay fully present for most of the flight; only melt into the
            // cart over the last fifth so the landing is crisp, not a fade-out
            // that starts mid-air.
            opacity: p < 0.8 ? 1 : 1 - ((p - 0.8) / 0.2) * 0.85,
            offset: t,
          });
        }
        const anim = ghost.animate(frames, {
          duration: flightMs, easing: "linear", fill: "forwards",
        });
        anim.onfinish = finish;
      };

      setTimeout(throwIt, pickupMs);
      // Belt and braces: if the tab is backgrounded the animation may never
      // fire onfinish, and a stranded ghost would sit over the page forever.
      setTimeout(finish, pickupMs + flightMs + 700);
    });
  }

  /* The visible cart button for the current breakpoint. Both exist in the
     DOM at all times; only one is laid out. */
  function visibleCartButton() {
    return (
      [...document.querySelectorAll('[data-open="cart"]')].find(
        (b) => b.getBoundingClientRect().width > 0,
      ) || null
    );
  }

  function visibleAccountTarget() {
    return (
      [...document.querySelectorAll("[data-fav-target], [data-account-link]")].find(
        (b) => b.getBoundingClientRect().width > 0,
      ) || null
    );
  }

  /*
   * Empty cart.
   *
   * Was a bare centred <p> reading "سلتك فارغة." — a dead end with nothing to
   * look at and nowhere to go, in a container otherwise sized for a list.
   * Built to the SAME shape as the favourites empty state (glyph, heading,
   * one supporting line, one CTA) and reusing its exact CTA label, so the two
   * empty states in this build read as one idea rather than two designs.
   *
   * It renders in three places — the drawer, the cart page and (since the
   * checkout summary started reading the store) the checkout aside — so it is
   * built to survive a ~340px column: nothing here has a fixed width.
   */
  function cartEmptyHTML() {
    return (
      '<div class="cart-empty flex flex-col items-center gap-2 px-4 py-12 text-center">' +
      '<span class="cart-empty__badge place-items-center grid bg-interaction-base mb-1 rounded-full text-cta size-16">' +
      '<span class="w-8 h-8">' + ICON.cart + "</span>" +
      "</span>" +
      '<p class="font-bold text-[#062A1C] text-lg">' + esc(t("سلتك فارغة")) + "</p>" +
      '<p class="max-w-[30ch] text-neutral-secondary text-sm leading-6">' +
      esc(t("المنتجات اللي تضيفها هتظهر هنا.")) + "</p>" +
      '<a href="shop.html" class="btn-elevate flex justify-center items-center bg-cta hover:bg-cta-hover mt-3 px-6 rounded-full min-h-11 font-semibold text-white text-sm transition-colors">' +
      esc(t("تصفح المنتجات")) + "</a>" +
      "</div>"
    );
  }

  function cartLineHTML(it) {
    return `
      <div class="flex gap-3 py-4 border-neutral-divider border-b" data-cart-line data-id="${esc(String(it.id))}">
        <img src="${esc(it.image)}" alt="${esc(it.name)}" class="bg-interaction-base shrink-0 p-1.5 rounded-lg w-[72px] h-[72px] object-contain" />
        <div class="flex-1 min-w-0">
          <div class="flex justify-between items-start gap-2">
            <p class="flex-1 min-w-0 font-semibold text-[#062A1C] text-sm line-clamp-2">${esc(it.name)}</p>
            <span data-line-total class="bg-accent-yellow shrink-0 px-2 py-0.5 rounded font-bold text-[#062A1C] text-xs latin">${egp(it.price * it.qty)}</span>
          </div>
          <p class="mt-1 text-neutral-secondary text-xs">العدد: <span class="latin" data-line-qty>${it.qty}</span></p>
          <!-- gap-1 until sm: at 320 the stepper (122) + حذف (24) + gap (8)
               came to 154 inside a 141px column, overflowing the row by 13px.
               The tighter gap brings it to 138. The baseline sweep missed
               this because it happened to run against an emptied cart, so no
               line ever rendered. -->
          <div class="flex justify-between items-center gap-2 mt-2">
            <!-- p-1, matching the product page counter's uniform 4px inset
                 between container and buttons - the px-2 py-1 it had gave
                 8px sides against 4px verticals and read as a different
                 control. Also 2px narrower, which the 320px budget likes. -->
            <div class="inline-flex items-center gap-1 sm:gap-3 p-1 border border-neutral-divider rounded-full">
              <button type="button" data-cart-step="-1" class="place-items-center grid shrink-0 w-8 h-8 text-[#062A1C]" aria-label="إنقاص"><span class="w-3.5 h-3.5">${ICON.minus}</span></button>
              <span class="w-4 text-sm text-center latin" data-line-qty-num>${it.qty}</span>
              <button type="button" data-cart-step="1" class="place-items-center grid shrink-0 bg-cta hover:bg-cta-hover rounded-full w-8 h-8 text-white transition-colors" aria-label="زيادة"><span class="w-3.5 h-3.5">${ICON.plus}</span></button>
            </div>
            <button type="button" data-cart-remove class="shrink-0 min-h-11 text-accent-error text-xs underline">حذف</button>
          </div>
        </div>
      </div>`;
  }

  /* ---------------------------------------------------------------
     Per-card quantity stepper

     Once a product is in the cart, its card swaps the add button for a
     −/n/+ control, so the second unit is one tap away instead of a re-add
     that gives no feedback. State comes from the same place as everything
     else — the card's `data-id` against the store — so every card for the
     same product on the page (rail + grid + upsell) stays in step, and the
     control survives a reload with no extra persistence.

     Driven off `cart:change`, so a change made in the drawer repaints the
     cards and vice versa.
     --------------------------------------------------------------- */
  function syncCardSteppers(scope) {
    (scope || document).querySelectorAll("[data-card-stepper]").forEach((stepper) => {
      const card = stepper.closest("[data-product]");
      if (!card) return;
      // Sibling lookup, not a card-wide query: on the product page the
      // outer [data-product] host also contains the related-products rail,
      // whose cards have add buttons of their own.
      const addBtn = stepper.parentElement.querySelector("[data-add-to-cart]");
      const it = Cart.find(card.dataset.id);
      stepper.hidden = !it;
      if (addBtn) addBtn.hidden = !!it;
      const num = stepper.querySelector("[data-card-qty]");
      if (it && num && num.textContent !== String(it.qty)) {
        // Rolls in the direction the quantity moved — see rollTo above.
        rollTo(num, it.qty, it.qty > (parseInt(num.textContent, 10) || 0) ? 1 : -1);
      }
    });
  }

  /* ---------------------------------------------------------------
     Points discount (the "خصم المبلغ" banner on cart and checkout)

     Stored, not held in a variable: the shopper applies it on the cart page
     and expects checkout to remember. The amount comes off the banner's own
     data attribute at click time; nothing here knows what a point is worth.
     Demo state like the points balance itself — see DESIGN-NOTES.
     --------------------------------------------------------------- */
  const POINTS_KEY = "abuauf:pointsDiscount";
  const pointsDiscount = () => Number(localStorage.getItem(POINTS_KEY)) || 0;

  function syncPointsUI() {
    const d = pointsDiscount();
    document.querySelectorAll("[data-points-apply]").forEach((b) => {
      b.textContent = d ? t("إلغاء الخصم") : t("خصم المبلغ");
      b.setAttribute("aria-pressed", d ? "true" : "false");
    });
    // The banner's message follows the state: spent points must not keep
    // being offered as available.
    document.querySelectorAll("[data-points-idle]").forEach((el) => (el.hidden = !!d));
    document.querySelectorAll("[data-points-used]").forEach((el) => (el.hidden = !d));
    /* Deliberately no totals work here. The checkout summary used to be
       static build-time markup with its own data-base-total, so this function
       carried a second, parallel set of totals hooks. It now carries the cart
       page's hooks instead: renderCart owns every figure on both pages, and
       every caller of this function already calls it. One renderer to keep
       correct rather than two to keep agreeing. */
  }

  function renderCart() {
    const items = Cart.items();
    const sub = Cart.subtotal();
    const shortfall = Math.max(0, MIN_ORDER - sub);
    const belowMin = shortfall > 0;
    const empty = items.length === 0;
    // Capped at the order's own worth — a 100 EGP wallet against a 60 EGP
    // basket discounts 60, it does not owe the shopper money.
    const discount = empty ? 0 : Math.min(pointsDiscount(), sub + DELIVERY_FEE);

    /* Badge — every cart button on the page.
       While a ghost is mid-flight the badge is held at its old value, so the
       number ticks up at the moment the item lands rather than before it has
       left. State is still the truth; only the display waits. */
    if (!badgeHold) syncCartBadges();

    // The card stepper is the thing being pressed, so it is NOT held back
    // with the badge — its number has to answer the tap immediately.
    syncCardSteppers();

    /*
     * Keyed reconcile rather than innerHTML replacement. Blowing the list away
     * on every change would destroy nodes mid-transition and drop focus, which
     * makes row-level micro-interactions impossible to build on top. Rows that
     * survive a change keep their DOM node; only genuinely new or gone rows are
     * created or detached.
     */
    document.querySelectorAll("[data-cart-lines]").forEach((host) => {
      // Drop the server-rendered rows the first time the store paints.
      host.querySelectorAll("[data-cart-static]").forEach((el) => el.remove());
      let emptyMsg = host.querySelector("[data-cart-empty]");
      if (empty && !emptyMsg) {
        emptyMsg = document.createElement("div");
        emptyMsg.setAttribute("data-cart-empty", "");
        emptyMsg.innerHTML = cartEmptyHTML();
        host.appendChild(emptyMsg);
      } else if (!empty && emptyMsg) {
        emptyMsg.remove();
      }

      const seen = {};
      items.forEach((it, i) => {
        seen[it.id] = true;
        let row = host.querySelector('[data-cart-line][data-id="' + CSS.escape(String(it.id)) + '"]');
        if (!row) {
          const tmp = document.createElement("div");
          tmp.innerHTML = cartLineHTML(it);
          row = tmp.firstElementChild;
          host.appendChild(row);
        } else {
          // Update in place so the node — and anything animating it — survives.
          const price = row.querySelector("[data-line-total]");
          const qtyTxt = row.querySelector("[data-line-qty]");
          const qtyNum = row.querySelector("[data-line-qty-num]");
          if (price) price.textContent = egp(it.price * it.qty);
          if (qtyTxt) qtyTxt.textContent = it.qty;
          if (qtyNum) {
            rollTo(qtyNum, it.qty, it.qty > (parseInt(qtyNum.textContent, 10) || 0) ? 1 : -1);
          }
        }
        // Keep DOM order in step with state order.
        if (host.children[i] !== row) host.insertBefore(row, host.children[i] || null);
      });

      host.querySelectorAll("[data-cart-line]").forEach((row) => {
        if (!seen[row.dataset.id]) row.remove();
      });
    });

    /* Totals + checkout gating, drawer and cart page alike. */
    document.querySelectorAll("[data-cart-subtotal]").forEach((el) => (el.textContent = egp(sub)));
    document.querySelectorAll("[data-cart-total]").forEach((el) => (el.textContent = egp(empty ? 0 : sub + DELIVERY_FEE - discount)));
    document.querySelectorAll("[data-cart-discount-row]").forEach((el) => (el.hidden = !discount));
    document.querySelectorAll("[data-cart-discount]").forEach((el) => (el.textContent = "− " + egp(discount)));
    document.querySelectorAll("[data-cart-shortfall]").forEach((el) => (el.textContent = egp(shortfall)));
    document.querySelectorAll("[data-cart-warning]").forEach((el) => (el.hidden = !belowMin || empty));
    document.querySelectorAll("[data-cart-checkout]").forEach((el) => {
      const blocked = belowMin || empty;
      el.classList.toggle("pointer-events-none", blocked);
      el.classList.toggle("opacity-50", blocked);
      el.setAttribute("aria-disabled", blocked ? "true" : "false");
    });
  }

  /*
   * Throw a product's image into the cart button and tick the badge when it
   * lands. Returns whether a flight actually started, because the caller has
   * to know: the badge is held from BEFORE the mutation until the landing, so
   * a hold with no flight to release it would freeze the number forever.
   */
  function throwToCart(sourceEl, opts) {
    const target = visibleCartButton();
    if (!sourceEl || !target || reduceMotion()) return false;
    badgeHold++;
    flyTo(sourceEl, target, null, opts).then(() => {
      badgeHold = Math.max(0, badgeHold - 1);
      if (badgeHold) return;
      // syncCartBadges rolls the badge to its new number, so the badge is not
      // ALSO pulsed — a pulse started a frame later would take over the
      // transform and cut the roll off mid-slide. The button itself takes the
      // catch instead: a small squash, plus the glyph's pulse.
      syncCartBadges();
      squash(target);
      const glyph = target.querySelector("[data-cart-glyph]");
      if (glyph) pulse(glyph);
    });
    return true;
  }

  /* The bundle total has to answer the checkboxes. It was baked at build
     time, so unticking a companion left the figure claiming a price for
     something you had just declined to buy. */
  function syncBundleTotal() {
    document.querySelectorAll("[data-bundle]").forEach((box) => {
      const out = box.querySelector("[data-bundle-total]");
      if (!out) return;
      let sum = Number(box.dataset.bundleBase) || 0;
      box.querySelectorAll("[data-bundle-item]").forEach((row) => {
        const check = row.querySelector("[data-bundle-check]");
        if (check && !check.checked) return;
        sum += Number(row.dataset.price) || 0;
      });
      out.textContent = egp(sum);
    });
  }

  function initCartUI() {
    Cart.init();
    document.addEventListener("cart:change", renderCart);
    renderCart();
    syncBundleTotal();
    document.addEventListener("change", (e) => {
      if (e.target.closest("[data-bundle-check]")) syncBundleTotal();
    });
    // A discount applied on a previous page (cart -> checkout) must paint on
    // arrival, not wait for the first click.
    syncPointsUI();

    document.addEventListener("click", (e) => {
      /* خصم المبلغ — apply the wallet-points discount, or press again to
         take it back. The mutation is a stored number plus a repaint; the
         same handler serves the cart page and checkout. */
      const applyPoints = e.target.closest("[data-points-apply]");
      if (applyPoints) {
        const banner = applyPoints.closest("[data-points-banner]");
        const amount = Number(banner && banner.dataset.pointsDiscount) || 0;
        if (pointsDiscount()) {
          localStorage.removeItem(POINTS_KEY);
          toast("تم إلغاء خصم النقاط");
        } else if (amount > 0) {
          localStorage.setItem(POINTS_KEY, String(amount));
          toast("تم خصم " + egp(amount) + " من الإجمالي");
        }
        syncPointsUI();
        renderCart();
        pulse(applyPoints);
        return;
      }

      const add = e.target.closest("[data-add-to-cart]");
      if (add) {
        const product = productFrom(add);
        if (!product) return;
        // Respect a quantity stepper sitting next to the button (product page).
        const scope = add.closest("[data-product]") || document;
        const qtyEl = scope.querySelector("[data-stepper] [data-qty]");

        /* Send the product image to the cart, and hold the badge at its old
           number until it lands. The mutation itself is not delayed — the
           store updates now, only the badge waits, so nothing can desync.
           The hold has to start BEFORE the mutation, or Cart.add's
           `cart:change` repaints the badge on the way past. */
        const img = scope.querySelector && scope.querySelector("img");
        const qty = qtyEl ? parseInt(qtyEl.textContent, 10) : 1;
        throwToCart(img, { card: true, tag: "+" + qty });

        Cart.add(product, qty);
        toast("تمت الإضافة إلى السلة");
        return;
      }

      /* "أضف الجميع الى السلة" — the frequently-bought-together block.
         Adds this product plus every companion still ticked, in one go and
         with one flight, rather than three separate ghosts racing each
         other. Nothing ticked still adds the product being viewed, which is
         what the total says it will do. */
      const bundleAdd = e.target.closest("[data-bundle-add]");
      if (bundleAdd) {
        const box = bundleAdd.closest("[data-bundle]");
        if (!box) return;
        const picks = [];
        const base = productFrom(box);
        if (base) picks.push(base);
        box.querySelectorAll("[data-bundle-item]").forEach((row) => {
          const check = row.querySelector("[data-bundle-check]");
          if (check && !check.checked) return;
          const prod = productFrom(row);
          if (prod) picks.push(prod);
        });
        if (!picks.length) return;
        const img = box.querySelector("[data-bundle-item] img") || box.querySelector("img");
        throwToCart(img, { card: true, tag: "+" + picks.length });
        picks.forEach((prod) => Cart.add(prod, 1));
        toast(picks.length + " " + t("منتجات أُضيفت إلى السلة"));
        return;
      }

      /* Card stepper. Every increment throws another one across the page —
         the reward for pressing + is the same little flight, not a number
         that quietly changes. Stepping below 1 drops the line, which puts
         the add button back. */
      const cardStep = e.target.closest("[data-card-step]");
      if (cardStep) {
        const product = productFrom(cardStep);
        if (!product) return;
        const card = cardStep.closest("[data-product]");
        const delta = parseInt(cardStep.dataset.cardStep, 10);
        const it = Cart.find(product.id);
        const next = (it ? it.qty : 0) + delta;

        if (next < 1) {
          Cart.remove(product.id);
          toast("تمت الإزالة من السلة");
          return;
        }
        if (delta > 0) throwToCart(card && card.querySelector("img"), { card: true, quick: true, tag: "+1" });
        if (it) Cart.setQty(product.id, next);
        else Cart.add(product, 1);

        pulse(cardStep);
        // The quantity itself is NOT pulsed here any more: syncCardSteppers
        // rolls it directionally on the same tick, and a pulse started after
        // the roll would win the transform and cancel it mid-slide.
        return;
      }

      const step = e.target.closest("[data-cart-step]");
      if (step) {
        const line = step.closest("[data-cart-line]");
        const it = Cart.find(line.dataset.id);
        if (it) Cart.setQty(it.id, it.qty + parseInt(step.dataset.cartStep, 10));
        return;
      }
      const rm = e.target.closest("[data-cart-remove]");
      if (rm) {
        const line = rm.closest("[data-cart-line]");
        Cart.remove(line.dataset.id);
      }
    });
  }

  /* ---------------------------------------------------------------
     Favourites UI

     Two jobs: reflect saved state onto every heart button on the page, and
     drive the favourites account page.

     The heart's filled/outline state is expressed purely through
     `aria-pressed` — the accessible state and the visual state are the same
     attribute, so they cannot drift. styles.css does the icon swap off that
     selector. Note it does NOT use the `hidden` attribute: `[hidden]` is
     already forced with `!important` in styles.css, which would make the
     state impossible to override back on. See CLAUDE.md.
     --------------------------------------------------------------- */
  function syncFavButtons(scope) {
    (scope || document).querySelectorAll("[data-fav-toggle]").forEach((btn) => {
      const product = productFrom(btn);
      if (!product) return;
      const on = Favs.has(product.id);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.setAttribute("aria-label", t(on ? "إزالة من المفضلة" : "أضف إلى المفضلة"));
    });
  }

  /*
   * The favourites page ships every catalogue card in the DOM, hidden, and
   * this reveals the saved ones — the same "filter what is already rendered"
   * approach the listing chips use, so the card markup still comes from
   * components.py alone rather than being duplicated in JS, and it works
   * from file:// with no fetch.
   */
  function renderFavsPage() {
    const grid = document.querySelector("[data-favs-grid]");
    if (!grid) return;
    let shown = 0;
    grid.querySelectorAll("[data-product]").forEach((card) => {
      const on = Favs.has(card.dataset.id);
      card.hidden = !on;
      if (on) shown++;
    });
    const empty = document.querySelector("[data-favs-empty]");
    if (empty) empty.hidden = shown > 0;
    grid.hidden = shown === 0;
    const countEl = document.querySelector("[data-favs-count]");
    if (countEl) countEl.textContent = String(shown);
  }

  /* ---------------------------------------------------------------
     Demo auth UI — the sign-in form, and the chrome that reflects it.
     --------------------------------------------------------------- */
  function initAuthUI() {
    Auth.init();

    const paintAccountLinks = () => {
      const authed = Auth.isAuthed();
      const u = Auth.user();
      document.querySelectorAll("[data-account-link]").forEach((el) => {
        el.setAttribute("href", pageHref(authed ? "/my-account" : "/login"));
        const label = el.querySelector("[data-account-label]");
        if (label) {
          label.textContent = authed
            ? currentLang() === "en"
              ? u.nameEn
              : u.name
            : t("الحساب");
        }
      });
      document.querySelectorAll("[data-authed-only]").forEach((el) => {
        el.hidden = !authed;
      });
      document.querySelectorAll("[data-anon-only]").forEach((el) => {
        el.hidden = authed;
      });
    };

    document.addEventListener("auth:change", paintAccountLinks);
    paintAccountLinks();

    // Sign-in form. Beats initDemoForms to the submit because the login form
    // is not tagged [data-demo-form] — it has a real (demo) credential check.
    document.querySelectorAll("[data-login-form]").forEach((form) => {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = (form.querySelector('[name="email"]') || {}).value;
        const password = (form.querySelector('[name="password"]') || {}).value;
        if (Auth.login(email, password)) {
          toast(t("تم تسجيل الدخول بنجاح"));
          setTimeout(() => (window.location.href = pageHref("/my-account")), 700);
        } else {
          toast(t("البريد الإلكتروني أو كلمة المرور غير صحيحة"), "error");
        }
      });
    });

    // One-tap fill, so the demo credentials do not have to be retyped.
    document.querySelectorAll("[data-demo-fill]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const form = document.querySelector("[data-login-form]");
        if (!form) return;
        const email = form.querySelector('[name="email"]');
        const password = form.querySelector('[name="password"]');
        if (email) email.value = Auth.demo.email;
        if (password) password.value = Auth.demo.password;
        if (email) email.focus();
      });
    });

    document.querySelectorAll("[data-logout]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        Auth.logout();
        toast(t("تم تسجيل الخروج"));
        setTimeout(() => (window.location.href = pageHref("/")), 600);
      });
    });
  }

  function initFavsUI() {
    Favs.init();

    const refresh = () => {
      syncFavButtons();
      renderFavsPage();
      syncFavCount();
    };
    document.addEventListener("favs:change", refresh);
    refresh();

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-fav-toggle]");
      if (!btn) return;
      const product = productFrom(btn);
      if (!product) return;

      const wasOn = Favs.has(product.id);
      const on = Favs.toggle(product);
      toast(on ? "تمت الإضافة إلى المفضلة" : "تمت الإزالة من المفضلة");

      // The heart itself always reacts, so the control feels alive even where
      // there is nowhere to fly to (the phone masthead has no account icon).
      pulse(btn);
      if (!on || wasOn) return;

      const target = visibleAccountTarget();
      if (!target) return;
      // A filled heart in the brand red-pink, not a clone of the button — the
      // button is an outline at rest, and an outline reads as nothing at 16px.
      const heartGhost =
        '<span style="display:grid;place-items:center;width:100%;height:100%;color:#e0245e">' +
        '<svg viewBox="0 0 24 24" fill="currentColor" style="width:100%;height:100%">' +
        '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z"/>' +
        "</svg></span>";
      flyTo(btn, target, heartGhost).then(() => {
        syncFavCount();
        pulse(target.querySelector("[data-fav-count]") || target);
      });
    });
  }

  /* Favourites badge on the account button. */
  function syncFavCount() {
    const n = Favs.count();
    document.querySelectorAll("[data-fav-count]").forEach((el) => {
      el.textContent = n;
      el.hidden = n === 0;
    });
  }

  /* ---------------------------------------------------------------
     Products mega-panel (desktop)
     --------------------------------------------------------------- */
  function initMegaMenu() {
    const toggle = document.querySelector("[data-megamenu-toggle]");
    const panel = document.getElementById("mega-panel");
    if (!toggle || !panel) return;
    const caret = toggle.querySelector("[data-megamenu-caret]");

    /* The caret flip is a class, not an inline transform. As an inline style
       it fought the `transition-transform` utility and snapped rather than
       eased; `.chevron` in styles.css owns both the transition and the
       rotation now, and every chevron on the site shares it. */
    const setOpen = (open) => {
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (caret) caret.classList.toggle("chevron--open", open);
    };

    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      setOpen(panel.hidden);
    });

    // Switching category is hover on the live site; keep click too so the
    // panel is reachable without a pointer.
    const activate = (idx) => {
      panel.querySelectorAll("[data-mega-cat]").forEach((b) => {
        b.dataset.active = b.dataset.megaCat === String(idx);
      });
      panel.querySelectorAll("[data-mega-sub]").forEach((u) => {
        u.hidden = u.dataset.megaSub !== String(idx);
      });
    };
    panel.querySelectorAll("[data-mega-cat]").forEach((b) => {
      const idx = b.dataset.megaCat;
      b.addEventListener("mouseenter", () => activate(idx));
      b.addEventListener("focus", () => activate(idx));
      b.addEventListener("click", () => activate(idx));
    });

    document.addEventListener("click", (e) => {
      if (!panel.hidden && !panel.contains(e.target) && !toggle.contains(e.target))
        setOpen(false);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !panel.hidden) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  function initListing(scope) {
    const grid = scope.querySelector("[data-product-grid]");
    const chips = [...scope.querySelectorAll("[data-filter]")];
    if (!grid || !chips.length) return;

    const cards = [...grid.children];
    cards.forEach((c, i) => (c.dataset.order = i)); // "الأكثر مبيعاً" = as published
    const countEl = scope.querySelector("[data-result-count]");
    const emptyEl = scope.querySelector("[data-empty-state]");
    const select = scope.querySelector("[data-listing] select, select");

    const setChip = (el, on) => {
      el.classList.remove(...(on ? CHIP_OFF : CHIP_ON));
      el.classList.add(...(on ? CHIP_ON : CHIP_OFF));
      el.setAttribute("aria-current", on ? "true" : "false");
    };

    function apply(slug, sort) {
      const visible = cards.filter((c) => {
        const show = slug === "all" || c.dataset.cat === slug;
        c.hidden = !show;
        return show;
      });
      if (sort && sort !== "popular") {
        const dir = sort === "price-desc" ? -1 : 1;
        const key = sort === "newest" ? "id" : "price";
        visible.sort((a, b) =>
          sort === "newest"
            ? Number(b.dataset.id) - Number(a.dataset.id)
            : dir * (Number(a.dataset.price) - Number(b.dataset.price))
        );
      } else {
        visible.sort((a, b) => Number(a.dataset.order) - Number(b.dataset.order));
      }
      visible.forEach((c) => grid.appendChild(c));
      if (countEl) countEl.textContent = visible.length;
      if (emptyEl) emptyEl.hidden = visible.length > 0;
      chips.forEach((c) => setChip(c, c.dataset.filter === slug));
    }

    let current = "all";
    chips.forEach((c) =>
      c.addEventListener("click", (ev) => {
        ev.preventDefault();
        current = c.dataset.filter;
        apply(current, select ? select.value : "popular");
        history.replaceState(null, "", "#" + current);
      })
    );
    if (select) {
      select.addEventListener("change", () => apply(current, select.value));
    }

    const readHash = () => {
      const h = (location.hash || "").replace("#", "");
      return h && chips.some((c) => c.dataset.filter === h) ? h : null;
    };

    // Arriving from the nav at shop.html#<slug> while already on shop.html is
    // a hash change, not a load — without this the page would sit unfiltered.
    window.addEventListener("hashchange", () => {
      const h = readHash();
      if (!h) return;
      current = h;
      apply(current, select ? select.value : "popular");
    });

    current = readHash() || "all";
    apply(current, select ? select.value : "popular");
  }

  /* ---------------------------------------------------------------
     Order notes, referral copy, addresses

     Three controls that shipped as dead markup and now do what they say
     (Ahmed pressed all three, 2026-07-22). Same store discipline as the
     cart: localStorage state, render as a pure function of it.
     --------------------------------------------------------------- */
  const NOTE_KEY = "abuauf:orderNote";

  function initOrderNotes() {
    document.querySelectorAll("[data-order-note]").forEach((ta) => {
      try {
        ta.value = localStorage.getItem(NOTE_KEY) || "";
      } catch (e) {
        /* ignore */
      }
    });
    document.addEventListener("click", (e) => {
      const save = e.target.closest("[data-order-note-save]");
      if (!save) return;
      const ta = (save.closest("div") || document).querySelector("[data-order-note]");
      if (!ta) return;
      const note = ta.value.trim();
      try {
        if (note) localStorage.setItem(NOTE_KEY, note);
        else localStorage.removeItem(NOTE_KEY);
      } catch (err) {
        /* ignore */
      }
      toast(note ? "تمت إضافة ملاحظتك على الطلب" : "تمت إزالة الملاحظات");
      pulse(save);
    });
  }

  function initReferralCopy() {
    /* navigator.clipboard.writeText rejects in more places than you would
       think (unfocused document, older WebViews), so a hidden-textarea
       execCommand copy backs it up — and the copied state must only ever
       paint when one of the two actually took. */
    function copyText(text) {
      const legacy = () => {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.cssText = "position:fixed;top:-9999px;opacity:0";
        document.body.appendChild(ta);
        ta.select();
        let ok = false;
        try {
          ok = document.execCommand("copy");
        } catch (err) {
          ok = false;
        }
        ta.remove();
        return ok;
      };
      /* writeText does not merely reject in awkward contexts — with a
         pending permission decision it can simply never settle, which left
         the button frozen on neither branch. So it races a short timer:
         whoever finishes first wins, and the timer path still sits inside
         the click's transient user activation, which execCommand needs. */
      return new Promise((resolve, reject) => {
        let settled = false;
        const win = () => {
          if (!settled) {
            settled = true;
            resolve();
          }
        };
        const viaLegacy = () => {
          if (settled) return;
          if (legacy()) win();
          else {
            settled = true;
            reject(new Error("copy failed"));
          }
        };
        if (navigator.clipboard) {
          navigator.clipboard.writeText(text).then(win, viaLegacy);
          setTimeout(viaLegacy, 350);
        } else {
          viaLegacy();
        }
      });
    }

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-copy-ref]");
      if (!btn || btn.dataset.copied) return;
      const link = (btn.closest("div") || document).querySelector("[data-ref-link]");
      const text = link ? link.textContent.trim() : "";
      if (!text) return;
      copyText(text).then(
        () => {
          /* The copied state lives on the button itself — a toast alone is
             off in the corner, and the question being answered is "did THIS
             button work". Reverts after a beat so it can be used again. */
          btn.dataset.copied = "true";
          const old = btn.textContent;
          btn.textContent = t("تم النسخ ✓");
          btn.classList.add("pointer-events-none");
          setTimeout(() => {
            btn.textContent = old;
            btn.classList.remove("pointer-events-none");
            delete btn.dataset.copied;
          }, 2600);
        },
        () => toast("تعذر النسخ — انسخ الرابط يدوياً", "error"),
      );
    });
  }

  /*
   * Addresses — the same contract as the cart and favourites stores: seeded
   * from the page's two demo addresses, persisted under abuauf:addresses,
   * and the grid re-rendered from state on every change. Exactly one address
   * is main at all times: setting a new main clears the old one, deleting
   * the main promotes the first survivor.
   */
  const ADDR_KEY = "abuauf:addresses";
  const ADDR_SEED = [
    { id: "a-home", label: "المنزل", line1: "شقة 3 - 220 شارع الحرية - الدور الأول", line2: "مصر الجديدة، القاهرة", main: true },
    { id: "a-work", label: "العمل", line1: "مبنى 12 - شارع التسعين الشمالي", line2: "التجمع الخامس، القاهرة", main: false },
  ];

  function addrAll() {
    try {
      const v = JSON.parse(localStorage.getItem(ADDR_KEY));
      if (Array.isArray(v)) return v;
    } catch (e) {
      /* fall through to seed */
    }
    return ADDR_SEED.map((a) => Object.assign({}, a));
  }

  function addrWrite(list) {
    if (list.length && !list.some((a) => a.main)) list[0].main = true;
    try {
      localStorage.setItem(ADDR_KEY, JSON.stringify(list));
    } catch (e) {
      /* ignore */
    }
    renderAddresses();
  }

  function addressCardHTML(a) {
    return `
      <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]" data-address-card data-id="${esc(a.id)}">
        <div class="flex justify-between items-center gap-3">
          <h3 class="font-bold text-[#062A1C] text-base">${esc(a.label)}</h3>
        </div>
        <div class="flex flex-col gap-1 text-neutral-secondary text-sm">
          <span>${esc(a.line1)}</span><span>${esc(a.line2)}</span>
        </div>
        ${a.main ? `<span class="bg-interaction-base px-3 py-1 rounded-full font-semibold text-primary text-xs self-start">${esc(t("العنوان الرئيسي"))}</span>` : ""}
        <div class="flex gap-2">
          <button type="button" data-address-edit class="hover:bg-interaction-base px-4 py-1.5 border border-neutral-divider rounded-full font-semibold text-[#062A1C] text-xs transition-colors">${esc(t("تعديل"))}</button>
          <button type="button" data-address-remove class="px-4 py-1.5 font-semibold text-accent-error text-xs">${esc(t("حذف"))}</button>
        </div>
      </div>`;
  }

  function renderAddresses() {
    const grid = document.querySelector("[data-addresses-grid]");
    if (!grid) return;
    const list = addrAll();
    grid.innerHTML = list.length
      ? list.map(addressCardHTML).join("")
      : `<p class="col-span-full py-8 text-neutral-secondary text-sm">${esc(t("لا توجد عناوين محفوظة بعد."))}</p>`;
  }

  function openAddressForm(addr) {
    const form = document.querySelector("[data-address-form]");
    if (!form) return;
    form.dataset.addressId = addr ? addr.id : "";
    form.elements.label.value = addr ? addr.label : "";
    form.elements.line1.value = addr ? addr.line1 : "";
    form.elements.line2.value = addr ? addr.line2 : "";
    form.elements.main.checked = addr ? !!addr.main : false;
    // The main address cannot demote itself — there would be no main left.
    form.elements.main.disabled = !!(addr && addr.main);
    const title = document.querySelector("[data-address-form-title]");
    if (title) title.textContent = addr ? t("تعديل العنوان") : t("اضف عنوان");
    openOverlay("address");
    setTimeout(() => form.elements.label.focus(), 80);
  }

  function initAddresses() {
    if (!document.querySelector("[data-addresses-grid]")) return;
    renderAddresses();

    document.addEventListener("click", (e) => {
      if (e.target.closest("[data-address-add]")) {
        openAddressForm(null);
        return;
      }
      const card = e.target.closest("[data-address-card]");
      if (!card) return;
      const list = addrAll();
      const addr = list.find((a) => a.id === card.dataset.id);
      if (!addr) return;
      if (e.target.closest("[data-address-edit]")) {
        openAddressForm(addr);
      } else if (e.target.closest("[data-address-remove]")) {
        addrWrite(list.filter((a) => a.id !== addr.id));
        toast("تم حذف العنوان");
      }
    });

    document.addEventListener("submit", (e) => {
      const form = e.target.closest("[data-address-form]");
      if (!form) return;
      e.preventDefault();
      const list = addrAll();
      const id = form.dataset.addressId;
      const entry = {
        id: id || "a-" + Date.now(),
        label: form.elements.label.value.trim(),
        line1: form.elements.line1.value.trim(),
        line2: form.elements.line2.value.trim(),
        main: form.elements.main.checked,
      };
      if (!entry.label || !entry.line1 || !entry.line2) return;
      if (entry.main) list.forEach((a) => (a.main = false));
      const at = list.findIndex((a) => a.id === id);
      if (at >= 0) list[at] = Object.assign({}, list[at], entry);
      else list.push(entry);
      addrWrite(list);
      closeOverlay();
      toast(id ? "تم تعديل العنوان" : "تمت إضافة العنوان");
    });
  }

  window.kInit = function (scope) {
    scope = scope || document;
    scope.querySelectorAll(".carousel").forEach(initCarousel);
    initAccordions(scope);
    initTabs(scope);
    initGallery(scope);
    initSteppers(scope);
    initSizeAndPrice(scope);
    initDemoForms(scope);
    initPasswordReveals(scope);
    initListing(scope);
    initReveal(scope);
  };

  /* ---------------------------------------------------------------
     Boot
     --------------------------------------------------------------- */
  function boot() {
    const header = document.getElementById("site-header");
    const footer = document.getElementById("site-footer");
    if (header) header.innerHTML = headerHTML();
    if (footer) footer.innerHTML = footerHTML();

    const overlays = document.createElement("div");
    overlays.id = "site-overlays";
    overlays.innerHTML = overlaysHTML();
    document.body.appendChild(overlays);

    initDelegation();
    initStickyNav();
    initMegaMenu();
    initSearch();
    initLangSwitcher();
    initCartUI();
    initAuthUI();
    initFavsUI();
    initOrderNotes();
    initReferralCopy();
    initAddresses();
    // Must run after the chrome is in the DOM and after initFavsUI, so the
    // dictionary pass sees every string on the page. Without this call a
    // stored English preference only styled the chrome.
    applyLangToContent();
    window.kInit(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
