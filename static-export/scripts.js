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
      name: "المكسرات",
      url: "/shop/nuts-crackers",
      badge: "images/abuauf/icons/nav-nuts-badge.png",
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
     --------------------------------------------------------------- */
  const ICON = {
    account:
      '<svg viewBox="0 0 29 29" fill="none" class="w-6 h-6"><path d="M4.47 22.96C7.43 21.29 10.85 20.33 14.5 20.33s7.07.96 10.03 2.63M18.88 11.58a4.38 4.38 0 1 1-8.75 0 4.38 4.38 0 0 1 8.75 0ZM27.63 14.5A13.13 13.13 0 1 1 1.38 14.5a13.13 13.13 0 0 1 26.25 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    search:
      '<svg viewBox="0 0 29 29" fill="none" class="w-6 h-6"><path d="M27.63 27.63 18.88 18.88M21.79 11.58a10.21 10.21 0 1 1-20.42 0 10.21 10.21 0 0 1 20.42 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    location:
      '<svg viewBox="0 0 22 20" fill="none" class="w-[22px] h-5"><path d="M16.75 11.75c-3 0-4 2-4 2h-3l-.14-.22c-.86-1.35-1.29-2.03-1.87-2.52-.51-.43-1.11-.76-1.75-.96-.72-.23-1.53-.23-3.13-.23H.75M16.75 11.75c3 0 4 2 4 2M16.75 11.75 15.23 3.38c-.17-.94-.26-1.4-.5-1.75a2 2 0 0 0-.84-.71c-.39-.17-.86-.17-1.81-.17h-.33M3.75 6.75h2M.75 3.75h4M15.75 5.75h1.42a1.5 1.5 0 0 0 .58-2.9c-.2-.09-.42-.1-.58-.1H15.25M6.75 15.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM18.75 16.75a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    menu: '<svg width="31" height="30" viewBox="0 0 31 30" fill="none"><path d="M21 6 9 6M21 12 3 12M15 18H3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    close:
      '<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    chevronDown:
      '<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    cart: '<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6"><path d="M2.5 3h1.6c.5 0 .93.35 1.03.84l.34 1.66m0 0 1.4 6.86c.16.8.87 1.37 1.68 1.37h7.9c.79 0 1.48-.54 1.66-1.31l1.3-5.4a.85.85 0 0 0-.83-1.05H5.47M9 20a1 1 0 1 1-2 0 1 1 0 0 1 2 0Zm9 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    arrowRight:
      '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><path d="m9 6 6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    arrowLeft:
      '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><path d="m15 6-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    phone:
      '<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
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
    "عرض السلة": "View cart",
    "اتمام الشراء": "Checkout",
    "سلتك فارغة.": "Your cart is empty.",
    "حذف": "Remove",
    "اضف": "Add",
    "القائمة": "Menu",
    "روابط أخرى": "More links",
    "الاكثر مبيعا": "Best sellers",
    "اللغة": "Language",
    // build-time UI strings — these live in the generated HTML, and are picked
    // up by translateDocument()'s text-node pass rather than by t()
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
    { code: "en", label: "English", dir: "ltr", flag: "images/abuauf/brand/flag-egypt.svg" },
    { code: "ar", label: "العربية", dir: "rtl", flag: "images/abuauf/brand/flag-egypt.svg" },
  ];

  const CHECK_ICON =
    '<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="m5 13 4 4L19 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function countryButton() {
    const rows = LANGS.map(
      (l) => `
        <button type="button" data-lang="${l.code}" class="flex items-center gap-3 hover:bg-interaction-base px-4 rounded-lg w-full min-h-11 text-start transition-colors">
          <img src="${l.flag}" alt="" class="rounded-full w-6 h-6 object-cover shrink-0" />
          <span class="flex-1 min-w-0 text-[#062A1C] text-base">${l.label}</span>
          <span class="text-cta shrink-0" data-lang-check="${l.code}" hidden>${CHECK_ICON}</span>
        </button>`,
    ).join("");

    return `
      <div class="relative shrink-0" data-lang-switcher>
        <button type="button" data-lang-toggle aria-expanded="false" class="flex items-center gap-1.5 min-h-11 px-4 py-0.5 rounded-full hover:bg-black/5 transition-colors">
          <img src="images/abuauf/brand/flag-egypt.svg" alt="" class="rounded-full w-4 h-4 object-cover" />
          <span class="font-semibold text-[#163300] text-base leading-[26px] whitespace-nowrap" data-lang-label>مصر (العربية)</span>
          <img src="images/abuauf/icons/icon-globe.svg" alt="" class="opacity-70 w-5 h-5" />
        </button>
        <div data-lang-panel hidden class="top-full inset-inline-start-0 z-50 absolute bg-white shadow-custom3 mt-2 p-2 rounded-2xl w-[288px]">
          <h4 class="mb-1 px-4 py-3 border-neutral-divider border-b font-bold text-[#062A1C] text-base">${esc(t("اللغة"))}</h4>
          ${rows}
        </div>
      </div>`;
  }

  /* ---------------------------------------------------------------
     Header
     --------------------------------------------------------------- */
  /*
   * A nav tab. The 4px underline is the Figma "Highlight" element — it sits in
   * the layout at all times and only changes opacity, so tabs never shift
   * vertically on hover or when the active page changes.
   */
  function desktopNavItem(item) {
    const href = pageHref(item.url);
    const isActive = currentPath() === item.url;
    const leading = item.badge
      ? `<img src="${item.badge}" alt="" class="shrink-0 w-[38px] h-[38px] object-contain" />`
      : "";
    const trailing = item.icon
      ? `<img src="${item.icon}" alt="" class="shrink-0 w-7 h-7" />`
      : "";

    const label = `
      <a href="${href}" class="flex flex-col gap-3 pt-3.5 shrink-0 group">
        <span class="flex items-center gap-1 h-6">
          <span class="font-semibold text-white text-base leading-6 whitespace-nowrap">${esc(t(item.name))}</span>
          ${trailing}
        </span>
        <span class="h-1 w-full bg-[#DCC498] rounded-full origin-center ${isActive ? "scale-x-100" : "scale-x-0 group-hover:scale-x-100"} transition-transform duration-[250ms] ease-[cubic-bezier(0.42,0,0.58,1)]"></span>
      </a>`;

    if (!item.children || !item.children.length) {
      return `<li class="flex items-center gap-2.5 shrink-0">${label}${leading}</li>`;
    }

    const cols = item.children
      .map(
        (c) =>
          `<li><a href="${pageHref(c.url)}" class="block py-1.5 font-medium text-textSecondary hover:text-primary text-base transition-colors">${esc(t(c.name))}</a></li>`,
      )
      .join("");

    return `<li class="group/mega relative flex items-center gap-2 shrink-0">
      ${label}${leading}
      <div class="invisible group-hover/mega:visible top-full inset-inline-start-0 z-50 absolute opacity-0 group-hover/mega:opacity-100 pt-3 transition-all duration-200">
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
  const MEGA_FEATURED = [
    { name: "عرض سناكس بروتين بزبدة الفول السودانى 35 جم", price: 51, img: "images/abuauf/products/PR000085.webp" },
    { name: "بسكويت محشو تمر - 12 قطعة", price: 65, img: "images/abuauf/products/image-600x600-1.png" },
    { name: "بن أبو عوف تركي ساده فاتح 200 جم", price: 308, img: "images/abuauf/products/6223004765353-2-1.webp" },
    { name: "عرض معمول سادة وقرفة وشيكولاتة", price: 250, img: "images/abuauf/products/330-thumb.webp" },
  ];

  const LEAF = `<img src="images/abuauf/icons/icon-leaf.svg" alt="" class="w-5 h-5 shrink-0" onerror="this.style.display='none'" />`;

  function megaPanelHTML() {
    const cats = MAIN_MENU.map((item, i) => {
      const slug = (item.url || "").replace("/shop/", "");
      return `<li>
        <button type="button" data-mega-cat="${i}" class="flex items-center gap-3 px-4 rounded-xl w-full min-h-11 font-semibold text-[#062A1C] text-base text-start transition-colors hover:bg-interaction-base data-[active=true]:bg-interaction-base" data-active="${i === 0}">
          ${LEAF}
          <span class="flex-1 min-w-0 truncate">${esc(t(item.name))}</span>
          <span class="w-4 h-4 text-neutral-secondary rtl:scale-flip shrink-0">${ICON.arrowRight}</span>
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
      (p) => `<a href="product.html" class="flex items-center gap-3 bg-white hover:shadow-custom4 p-3 rounded-2xl transition-shadow">
        <span class="flex-1 min-w-0">
          <span class="block font-medium text-[#062A1C] text-sm leading-5 line-clamp-2">${esc(p.name)}</span>
          <span class="inline-block bg-accent-yellow mt-1.5 px-2 py-0.5 rounded font-bold text-[#062A1C] text-xs latin">EGP ${p.price}.00</span>
        </span>
        <img src="${p.img}" alt="" class="bg-interaction-base p-1 rounded-lg w-14 h-14 object-contain shrink-0" loading="lazy" />
      </a>`,
    ).join("");

    return `
      <div id="mega-panel" data-megamenu hidden class="hidden lg:block top-full inset-inline-0 z-40 absolute bg-white shadow-custom3 rounded-b-2xl">
        <div class="gap-6 grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1.15fr)] mx-auto p-6 max-w-[1600px]">
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
                 <div class="flex justify-between items-center gap-6 px-4 xl:px-20 h-full">
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
        <div class="relative z-40 bg-primary px-4 xl:px-20">
          <div class="flex justify-between items-center mx-auto border-[#0F6140] border-b h-[79px] max-w-[1536px]">
            <!-- RTL start (right edge): logo, products, delivery -->
            <div class="flex items-center gap-6 min-w-0">
              <a href="index.html" class="block shrink-0 w-[180px] h-[60px]">
                <img src="images/abuauf/brand/logo-abuauf-white.svg" alt="أبو عوف" class="w-full h-full object-contain" />
              </a>
              ${
                checkout
                  ? ""
                  : `<button type="button" data-megamenu-toggle aria-expanded="false" aria-controls="mega-panel" class="hidden lg:flex items-center gap-3 bg-cta hover:bg-cta-hover shrink-0 px-4 py-2 rounded-full h-12 transition-colors">
                       <img src="images/abuauf/icons/icon-grid.svg" alt="" class="w-6 h-6" />
                       <span class="font-medium text-white text-[18px] leading-6 whitespace-nowrap">${esc(t("المنتجات"))}</span>
                       <span class="w-6 h-6 text-white transition-transform" data-megamenu-caret>${ICON.chevronDown}</span>
                     </button>
                     <button type="button" data-open="location" class="hidden xl:flex items-center gap-2 hover:text-white/80 py-3 h-12 min-w-0 transition-colors">
                       <span class="font-normal text-white text-[13px] leading-5 truncate">التوصيل الى الشروق - القاهرة</span>
                       <span class="shrink-0 w-6 h-6 text-white">${ICON.chevronDown}</span>
                     </button>`
              }
            </div>

            <!-- RTL end (left edge): account, search, cart.
                 Checkout keeps account and cart but drops search, matching the
                 Figma checkout header — it is not a bare logo bar. -->
            <div class="flex items-center gap-6 shrink-0">
              <a href="login.html" class="hidden lg:flex items-center gap-3 hover:text-white/80 py-2 h-12 transition-colors">
                <img src="images/abuauf/icons/icon-user.svg" alt="" class="w-6 h-6" />
                <span class="font-normal text-white text-[13px] leading-5">${esc(t("الحساب"))}</span>
                <span class="w-6 h-6 text-white">${ICON.chevronDown}</span>
              </a>
              ${
                checkout
                  ? ""
                  : `<button type="button" data-open="search" aria-label="بحث" class="place-items-center grid bg-cta hover:bg-cta-hover border-2 border-cta rounded-full transition-colors size-12">
                       <img src="images/abuauf/icons/icon-search.svg" alt="" class="w-5 h-5" />
                     </button>`
              }
              <button type="button" data-open="cart" aria-label="السلة" class="relative place-items-center grid bg-accent-yellow hover:bg-accent-500 rounded-full transition-colors size-12">
                <img src="images/abuauf/icons/icon-cart.svg" alt="" class="w-7 h-7" />
                <span class="-top-2 -end-2 absolute place-items-center grid bg-white shadow-custom4 px-1.5 rounded-full min-w-[22px] h-[22px] font-semibold text-black text-xs" data-cart-count>2</span>
              </button>
            </div>
          </div>

          ${
            checkout
              ? ""
                 /* bg-primary is carried on the bar itself, not inherited from
                    the masthead, so it stays opaque once initStickyNav pulls
                    it out of flow with position:fixed. */
              : `<div data-navbar class="relative z-30 bg-primary h-[48px]">
                   <nav class="mx-auto max-w-[1536px] h-full">
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
        <div class="relative flex items-center ${checkout ? "justify-center" : "justify-between"} bg-primary px-4 py-4 text-white">
          ${
            checkout
              ? ""
              : `<button type="button" data-open="menu" class="place-items-center grid size-11 -me-2" aria-label="Menu">${ICON.menu}</button>`
          }
          <a href="index.html" class="block"><img src="images/abuauf/brand/logo-abuauf-white.svg" alt="أبو عوف" class="w-[132px] h-[44px] object-contain" /></a>
          ${
            checkout
              ? ""
              : `<button type="button" data-open="cart" class="relative place-items-center grid bg-accent-yellow rounded-full size-11" aria-label="السلة">
                   <img src="images/abuauf/icons/icon-cart.svg" alt="" class="w-7 h-7" />
                   <span class="-top-1 -end-1 absolute place-items-center grid bg-white rounded-full w-5 h-5 font-bold text-[10px] text-black" data-cart-count>2</span>
                 </button>`
          }
        </div>
      </div>
      ${
        checkout
          ? ""
          : `<div class="md:hidden block bg-interaction-base px-4 py-2">
               <button type="button" data-open="location" class="flex justify-between items-center gap-1 bg-cta px-5 py-2.5 rounded-full w-full min-h-11 text-white">
                 <span class="font-semibold text-xs truncate">التوصيل الى الشروق - القاهرة</span>
                 <span class="shrink-0 w-3.5 h-3.5">${ICON.chevronDown}</span>
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
            <form data-newsletter class="flex flex-row-reverse items-center gap-2 bg-transparent py-2 xl:py-[9px] pe-5 ps-2.5 border-2 border-neutral-outline rounded-2xl w-full">
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
            <img src="images/abuauf/brand/logo-abuauf-white.svg" alt="أبو عوف" class="w-[180px] h-[46px] object-contain" />
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
        <img src="images/abuauf/brand/logo-abuauf-white.svg" alt="أبو عوف" class="w-[110px] h-9 object-contain" />
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
        <div class="flex items-center gap-3 px-5 py-4 border-neutral-divider border-b">
          <span class="w-5 h-5 text-neutral-secondary">${ICON.search}</span>
          <input type="search" data-search-input placeholder="ابحث عن قهوة، مكسرات، تمور…" class="flex-1 outline-none text-[#062A1C] text-base" />
          <button type="button" data-close class="place-items-center grid hover:bg-interaction-base rounded-full w-8 h-8 text-[#062A1C]" aria-label="إغلاق">${ICON.close}</button>
        </div>
        <div class="px-5 py-6">
          <p class="mb-3 text-neutral-secondary text-xs">الأكثر بحثاً</p>
          <div class="flex flex-wrap gap-2">
            ${["قهوة تركي", "مكسرات مشكلة", "تمر مجدول", "زبدة فول سوداني", "بوكس هدايا"]
              .map(
                (s) =>
                  `<a href="shop-category.html" class="bg-interaction-base hover:bg-cta px-3 py-1.5 rounded-full text-[#062A1C] hover:text-white text-sm transition-colors">${s}</a>`,
              )
              .join("")}
          </div>
        </div>
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
          <select class="mt-1 px-3 border border-neutral-divider rounded-lg w-full h-12 text-[#062A1C] placeholder-select">
            ${["القاهرة", "الجيزه", "الاسكندريه", "القليوبيه", "الشرقيه", "الدقهليه", "المنوفيه", "الغربيه"]
              .map((c) => `<option>${c}</option>`)
              .join("")}
          </select>
        </label>
        <label class="block">
          <span class="label">المنطقة</span>
          <select class="mt-1 px-3 border border-neutral-divider rounded-lg w-full h-12 text-[#062A1C] placeholder-select">
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
    if (input) setTimeout(() => input.focus(), 80);
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

  function initSteppers(scope) {
    scope.querySelectorAll("[data-stepper]").forEach((st) => {
      const qtyEl = st.querySelector("[data-qty]");
      st.querySelectorAll("[data-step]").forEach((b) => {
        b.addEventListener("click", () => {
          const delta = parseInt(b.getAttribute("data-step"), 10);
          let v = parseInt(qtyEl.textContent, 10) || 1;
          v = Math.max(1, v + delta);
          qtyEl.textContent = v;
        });
      });
    });
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
      // Padding is added only while stuck: in flow the bar inherits the
      // masthead's padding, but fixed positioning takes it out of that box.
      const stickyClasses = [
        "fixed",
        "top-0",
        "left-0",
        "right-0",
        "z-[100]",
        "shadow-md",
        "animate-slideDown",
        "px-4",
        "xl:px-20",
      ];
      if (should) {
        placeholder.style.height = nav.offsetHeight + "px";
        nav.classList.add(...stickyClasses);
      } else {
        placeholder.style.height = "0px";
        nav.classList.remove(...stickyClasses);
      }
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
    document.documentElement.setAttribute("lang", l.code);
    document.documentElement.setAttribute("dir", l.dir);
    document.querySelectorAll("[data-lang-label]").forEach((el) => {
      el.textContent = l.code === "ar" ? "مصر (العربية)" : "Egypt (English)";
    });
    document.querySelectorAll("[data-lang-check]").forEach((el) => {
      el.hidden = el.dataset.langCheck !== l.code;
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
  function repaintForLang() {
    const header = document.getElementById("site-header");
    const footer = document.getElementById("site-footer");
    const overlays = document.getElementById("site-overlays");
    if (header) header.innerHTML = headerHTML();
    if (footer) footer.innerHTML = footerHTML();
    if (overlays) overlays.innerHTML = overlaysHTML();

    // Product titles: data-name is Arabic, data-name-en is the catalogue's
    // real English name. Nothing invented here.
    const en = currentLang() === "en";
    document.querySelectorAll("[data-product][data-name-en]").forEach((card) => {
      const target = card.querySelector("[data-product-title]");
      if (!target) return;
      target.textContent = en ? card.dataset.nameEn : card.dataset.name;
    });

    translateDocument();

    initMegaMenu();
    initLangSwitcher(true);
    window.kInit(document);
    renderCart();
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

    document.querySelectorAll("[data-lang-switcher]").forEach((wrap) => {
      const toggle = wrap.querySelector("[data-lang-toggle]");
      const panel = wrap.querySelector("[data-lang-panel]");
      if (!toggle || !panel) return;
      toggle.addEventListener("click", (e) => {
        e.stopPropagation();
        const open = panel.hidden;
        panel.hidden = !open;
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
      panel.querySelectorAll("[data-lang]").forEach((btn) => {
        btn.addEventListener("click", () => {
          const changed = btn.dataset.lang !== currentLang();
          applyLang(btn.dataset.lang);
          panel.hidden = true;
          toggle.setAttribute("aria-expanded", "false");
          if (changed) repaintForLang();
        });
      });
      document.addEventListener("click", (e) => {
        if (!panel.hidden && !wrap.contains(e.target)) {
          panel.hidden = true;
          toggle.setAttribute("aria-expanded", "false");
        }
      });
    });
  }

  /* ---------------------------------------------------------------
     Cart rendering — drawer body, badge, cart page

     Everything here is a pure function of Cart state and re-runs on
     `cart:change`. Nothing mutates state; the handlers below do that.
     --------------------------------------------------------------- */
  const DELIVERY_FEE = 30;
  const MIN_ORDER = 150;

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
          <div class="flex justify-between items-center gap-2 mt-2">
            <div class="inline-flex items-center gap-3 px-2 py-1 border border-neutral-divider rounded-full">
              <button type="button" data-cart-step="-1" class="place-items-center grid w-8 h-8 text-[#062A1C]" aria-label="إنقاص">−</button>
              <span class="w-4 text-sm text-center latin" data-line-qty-num>${it.qty}</span>
              <button type="button" data-cart-step="1" class="place-items-center grid w-8 h-8 text-[#062A1C]" aria-label="زيادة">+</button>
            </div>
            <button type="button" data-cart-remove class="min-h-11 text-accent-error text-xs underline">حذف</button>
          </div>
        </div>
      </div>`;
  }

  function renderCart() {
    const items = Cart.items();
    const sub = Cart.subtotal();
    const shortfall = Math.max(0, MIN_ORDER - sub);
    const belowMin = shortfall > 0;
    const empty = items.length === 0;

    /* Badge — every cart button on the page. */
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      el.textContent = Cart.count();
      el.hidden = Cart.count() === 0;
    });

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
        emptyMsg = document.createElement("p");
        emptyMsg.setAttribute("data-cart-empty", "");
        emptyMsg.className = "py-10 text-neutral-secondary text-sm text-center";
        emptyMsg.textContent = "سلتك فارغة.";
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
          if (qtyNum) qtyNum.textContent = it.qty;
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
    document.querySelectorAll("[data-cart-total]").forEach((el) => (el.textContent = egp(empty ? 0 : sub + DELIVERY_FEE)));
    document.querySelectorAll("[data-cart-shortfall]").forEach((el) => (el.textContent = egp(shortfall)));
    document.querySelectorAll("[data-cart-warning]").forEach((el) => (el.hidden = !belowMin || empty));
    document.querySelectorAll("[data-cart-checkout]").forEach((el) => {
      const blocked = belowMin || empty;
      el.classList.toggle("pointer-events-none", blocked);
      el.classList.toggle("opacity-50", blocked);
      el.setAttribute("aria-disabled", blocked ? "true" : "false");
    });
  }

  function initCartUI() {
    Cart.init();
    document.addEventListener("cart:change", renderCart);
    renderCart();

    document.addEventListener("click", (e) => {
      const add = e.target.closest("[data-add-to-cart]");
      if (add) {
        const product = productFrom(add);
        if (!product) return;
        // Respect a quantity stepper sitting next to the button (product page).
        const scope = add.closest("[data-product]") || document;
        const qtyEl = scope.querySelector("[data-stepper] [data-qty]");
        Cart.add(product, qtyEl ? parseInt(qtyEl.textContent, 10) : 1);
        toast("تمت الإضافة إلى السلة");
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

  function initFavsUI() {
    Favs.init();

    const refresh = () => {
      syncFavButtons();
      renderFavsPage();
    };
    document.addEventListener("favs:change", refresh);
    refresh();

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-fav-toggle]");
      if (!btn) return;
      const product = productFrom(btn);
      if (!product) return;
      const on = Favs.toggle(product);
      toast(on ? "تمت الإضافة إلى المفضلة" : "تمت الإزالة من المفضلة");
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

    const setOpen = (open) => {
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (caret) caret.style.transform = open ? "rotate(180deg)" : "";
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

  window.kInit = function (scope) {
    scope = scope || document;
    scope.querySelectorAll(".carousel").forEach(initCarousel);
    initAccordions(scope);
    initTabs(scope);
    initSteppers(scope);
    initDemoForms(scope);
    initPasswordReveals(scope);
    initListing(scope);
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
    initLangSwitcher();
    initCartUI();
    initFavsUI();
    window.kInit(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
