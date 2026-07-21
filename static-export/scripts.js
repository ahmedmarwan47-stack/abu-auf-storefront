/* =====================================================================
   scripts.js — shared behaviour for the static Kouider build.

   Replaces the React runtime with vanilla JS:
     • Injects the shared header, footer and overlay chrome into every
       page (each page only ships a #site-header / #site-footer mount
       point, so markup stays DRY and works from the file:// protocol).
     • Re-implements the interactive pieces that were React components:
       mobile menu drawer, cart drawer, search modal, location bottom
       sheet, sticky-on-scroll navbar, mega-menu hover, language toggle.
     • Provides page-level helpers: carousels (replacing Swiper),
       accordions, tabs, quantity steppers, toasts and demo forms.

   Content that the CMS used to supply (menus, footer columns, socials)
   is baked in below as representative placeholder data.
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
    { name: "المشروبات", url: "/shop/coffee-beverage" },
    { name: "البهارات والزيوت", url: "/shop/spices-kitchen-baking" },
    { name: "الهدايا", url: "/shop/gifting-seasonal" },
  ];

  const FOOTER_COLUMNS = [
    {
      name: "تسوق",
      links: [
        { title: "مكسرات وحبوب ومقرمشات", url: "/shop/nuts-crackers" },
        { title: "قهوة ومشروبات", url: "/shop/coffee-beverage" },
        { title: "تمور وفواكه مجففة", url: "/shop/dates-dried-fruits" },
        { title: "سناكس صحية", url: "/shop/healthy-snacks" },
        { title: "الهدايا والمشاركة", url: "/shop/gifting-seasonal" },
      ],
    },
    {
      name: "أبو عوف",
      links: [
        { title: "قصتنا", url: "/about" },
        { title: "الفروع", url: "/branches" },
        { title: "المكافآت", url: "/rewards" },
        { title: "البلوج", url: "/blogs" },
        { title: "أتصل بنا", url: "/contact-us" },
      ],
    },
    {
      name: "المساعدة",
      links: [
        { title: "الأسئلة الشائعة", url: "/faqs" },
        { title: "سياسة الخصوصية", url: "/privacy-policy" },
        { title: "الشروط والأحكام", url: "/terms-conditions" },
        { title: "سياسة التوصيل والاسترجاع", url: "/return-policy" },
      ],
    },
  ];

  const SOCIALS = [
    {
      title: "Facebook",
      href: "#",
      svg: '<path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06C2 17.06 5.66 21.21 10.44 22v-7.03H7.9v-2.9h2.54V9.85c0-2.51 1.49-3.9 3.78-3.9 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.87h2.78l-.44 2.9h-2.34V22C18.34 21.21 22 17.06 22 12.06Z"/>',
    },
    {
      title: "Instagram",
      href: "#",
      svg: '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16Zm0 3.68A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84Zm0 10.16A4 4 0 1 1 16 12a4 4 0 0 1-4 4Zm6.4-10.4a1.44 1.44 0 1 0 1.44 1.44 1.44 1.44 0 0 0-1.44-1.44Z"/>',
    },
    {
      title: "TikTok",
      href: "#",
      svg: '<path d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 1 1-1.84-2.48V9.76a5.68 5.68 0 1 0 4.93 5.63V9.01a7.3 7.3 0 0 0 4.05 1.23V7.15a4.28 4.28 0 0 1-2.99-1.33Z"/>',
    },
    {
      title: "YouTube",
      href: "#",
      svg: '<path d="M23 12s0-3.2-.4-4.73a2.5 2.5 0 0 0-1.76-1.77C19.31 5.1 12 5.1 12 5.1s-7.31 0-8.84.4A2.5 2.5 0 0 0 1.4 7.27C1 8.8 1 12 1 12s0 3.2.4 4.73a2.5 2.5 0 0 0 1.76 1.77c1.53.4 8.84.4 8.84.4s7.31 0 8.84-.4a2.5 2.5 0 0 0 1.76-1.77C23 15.2 23 12 23 12Zm-13 3.5v-7l6 3.5Z"/>',
    },
  ];

  /* ---------------------------------------------------------------
     Route → static-file mapping
     --------------------------------------------------------------- */
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
    if (clean.startsWith("/shop/")) return "shop-category.html";
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
  function countryButton() {
    return `
      <button type="button" class="flex items-center gap-1.5 shrink-0 px-4 py-0.5 rounded-full hover:bg-black/5 transition-colors">
        <img src="images/abuauf/brand/flag-egypt.svg" alt="" class="rounded-full w-4 h-4 object-cover" />
        <span class="font-semibold text-[#163300] text-base leading-[26px] whitespace-nowrap">مصر (EGP)</span>
        <img src="images/abuauf/icons/icon-globe.svg" alt="" class="opacity-70 w-5 h-5" />
      </button>`;
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
          <span class="font-semibold text-white group-hover:text-white/80 text-xl leading-7 whitespace-nowrap transition-colors">${esc(item.name)}</span>
          ${trailing}
        </span>
        <span class="h-1 w-full bg-[#DCC498] rounded-full ${isActive ? "opacity-100" : "opacity-0 group-hover:opacity-60"} transition-opacity"></span>
      </a>`;

    if (!item.children || !item.children.length) {
      return `<li class="flex items-center gap-2.5 shrink-0">${label}${leading}</li>`;
    }

    const cols = item.children
      .map(
        (c) =>
          `<li><a href="${pageHref(c.url)}" class="block py-1.5 font-medium text-textSecondary hover:text-primary text-base transition-colors">${esc(c.name)}</a></li>`,
      )
      .join("");

    return `<li class="group/mega relative flex items-center gap-2.5 shrink-0">
      ${label}${leading}
      <div class="invisible group-hover/mega:visible top-full inset-inline-start-0 z-50 absolute opacity-0 group-hover/mega:opacity-100 pt-3 transition-all duration-200">
        <div class="flex gap-6 bg-white shadow-custom3 p-6 rounded-2xl w-max min-w-[420px]">
          <div class="flex-1">
            <div class="mb-3 font-semibold text-primary text-lg">${esc(item.name)}</div>
            <ul class="gap-x-8 grid grid-cols-2">${cols}</ul>
            <a href="${href}" class="inline-flex items-center gap-1 mt-4 font-semibold text-cta hover:text-primary text-base transition-colors">
              تسوق كل ${esc(item.name)}
              <span class="w-5 h-5 rtl:scale-flip">${ICON.arrowRight}</span>
            </a>
          </div>
          <div class="bg-interaction-base shrink-0 rounded-xl w-[180px] overflow-hidden">
            <img src="${item.image}" alt="${esc(item.name)}" class="w-full h-[160px] object-cover" loading="lazy" />
          </div>
        </div>
      </div>
    </li>`;
  }

  function headerHTML() {
    const checkout = isCheckout();

    /* --- support (utility) menu --- */
    const support = SUPPORT_MENU.map(
      (i) =>
        `<a href="${pageHref(i.url)}" class="font-medium text-white hover:text-white/70 text-sm leading-[140%] transition-colors">${esc(i.title)}</a>`,
    ).join("");

    /* --- desktop primary nav --- */
    const nav = MAIN_MENU.map(desktopNavItem).join("");

    const desktop = `
      <div class="hidden md:block">
        ${
          checkout
            ? ""
            : `<div class="relative z-40 bg-beige h-9">
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
          <div class="flex ${checkout ? "justify-center" : "justify-between"} items-center border-[#0F6140] border-b h-[100px]">
            <!-- RTL start (right edge): logo, products, delivery -->
            <div class="flex items-center gap-6 min-w-0">
              <a href="index.html" class="block shrink-0 w-[180px] h-[60px]">
                <img src="images/abuauf/brand/logo-abuauf-white.svg" alt="أبو عوف" class="w-full h-full object-contain" />
              </a>
              ${
                checkout
                  ? ""
                  : `<button type="button" data-open="menu" class="hidden lg:flex items-center gap-2.5 bg-cta hover:bg-cta-hover shrink-0 px-6 py-[18px] rounded-full transition-colors">
                       <img src="images/abuauf/icons/icon-grid.svg" alt="" class="w-6 h-6" />
                       <span class="font-semibold text-white text-xl leading-7 whitespace-nowrap">المنتجات</span>
                       <span class="w-6 h-6 text-white">${ICON.chevronDown}</span>
                     </button>
                     <button type="button" data-open="location" class="hidden xl:flex items-center gap-2.5 hover:bg-white/10 px-6 py-[18px] rounded-full min-w-0 transition-colors">
                       <span class="font-semibold text-white text-xl leading-7 truncate">التوصيل الى الشروق - القاهرة</span>
                       <span class="shrink-0 w-6 h-6 text-white">${ICON.chevronDown}</span>
                     </button>`
              }
            </div>

            <!-- RTL end (left edge): account, search, cart -->
            ${
              checkout
                ? ""
                : `<div class="flex items-center gap-6 shrink-0">
                     <a href="login.html" class="hidden lg:flex items-center gap-2.5 hover:bg-white/10 px-6 py-[18px] rounded-full transition-colors">
                       <img src="images/abuauf/icons/icon-user.svg" alt="" class="w-6 h-6" />
                       <span class="font-semibold text-white text-xl leading-7">الحساب</span>
                       <span class="w-6 h-6 text-white">${ICON.chevronDown}</span>
                     </a>
                     <button type="button" data-open="search" aria-label="بحث" class="place-items-center grid bg-cta hover:bg-cta-hover border-2 border-cta rounded-full transition-colors size-12">
                       <img src="images/abuauf/icons/icon-search.svg" alt="" class="w-5 h-5" />
                     </button>
                     <button type="button" data-open="cart" aria-label="السلة" class="relative place-items-center grid bg-accent-yellow hover:bg-accent-500 rounded-full transition-colors size-[60px]">
                       <img src="images/abuauf/icons/icon-cart.svg" alt="" class="w-9 h-9" />
                       <span class="-top-3 -end-3 absolute place-items-center grid bg-white shadow-custom4 px-2 rounded-full min-w-[28px] h-7 font-semibold text-black text-base" data-cart-count>2</span>
                     </button>
                   </div>`
            }
          </div>

          ${
            checkout
              ? ""
              : `<div data-navbar class="relative z-30 h-[54px]">
                   <nav class="h-full">
                     <ul class="flex items-start gap-9 h-full overflow-x-auto no-scrollbar">${nav}</ul>
                   </nav>
                 </div>`
          }
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
              : `<button type="button" data-open="menu" class="place-items-center grid w-8" aria-label="القائمة">${ICON.menu}</button>`
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
               <button type="button" data-open="location" class="flex justify-between items-center gap-1 bg-cta px-5 py-2.5 rounded-full w-full text-white">
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
  function footerHTML() {
    if (isCheckout()) {
      return `<footer class="bg-neutral-support-bg py-6">
        <div class="mx-auto max-w-[1392px] px-4 text-center text-bordercolor text-[10px]">© Abdel Rahim Koueider ${YEAR} — All copyrights reserved</div>
      </footer>`;
    }

    const columns = FOOTER_COLUMNS.map(
      (col) => `
      <div>
        <div class="mb-3.5 font-semibold text-white text-[18px] capitalize">${esc(col.name)}</div>
        <ul class="flex flex-col gap-y-2">
          ${col.links
            .map(
              (l) =>
                `<li><a href="${pageHref(l.url)}" class="text-base font-normal capitalize text-primaryLight hover:underline">${esc(l.title)}</a></li>`,
            )
            .join("")}
        </ul>
      </div>`,
    ).join("");

    const socials = SOCIALS.map(
      (s) =>
        `<li><a href="${s.href}" aria-label="Visit our ${s.title} page" class="grid place-items-center w-9 h-9 rounded-full bg-white/10 hover:bg-cta transition-colors text-white"><svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">${s.svg}</svg></a></li>`,
    ).join("");

    const subscription = `
      <div class="relative items-start gap-4 grid grid-cols-[auto,1fr] bg-primaryExtraDark xl:p-8 px-4 py-[32px] rounded-[20px] w-full xl:w-[582px] overflow-hidden">
        <div class="relative w-[74px] xl:w-[122px] h-[71px] xl:h-[117px]">
          <img src="images/subfooter.svg" alt="Newsletter envelope" class="w-full h-full object-contain" />
        </div>
        <div class="flex flex-col items-start gap-4 col-start-2">
          <p class="text-[18px] text-neutral-white leading-[140%]">Stay connected — get sweet news &amp; offers.</p>
        </div>
        <form data-newsletter class="col-span-2 xl:col-span-1 xl:col-start-2 flex items-center gap-4 bg-white pr-2 pl-4 border border-primary-light rounded-full w-full h-[52px]">
          <input type="email" required placeholder="Enter your email" class="flex-1 bg-transparent outline-none text-[14px] text-textSecondary" aria-label="Email address" />
          <button type="submit" class="flex justify-center items-center bg-neutral-support-bg px-6 rounded-full h-[36px] font-medium text-[14px] text-white">Subscribe</button>
        </form>
      </div>`;

    return `<footer class="bg-neutral-support-bg pt-[60px] pb-[24px]">
      <div class="flex flex-col gap-y-[60px] mx-auto px-4 2xl:px-0 max-w-[1392px]">
        <div class="flex flex-col gap-y-[60px] w-full">
          <div class="relative flex flex-col sm:flex-row gap-4 justify-between items-center pb-[60px] border-bordercolor border-b w-full">
            <div class="relative w-[242px] h-[42px]"><img src="images/logos/logo-light.png" alt="Kouider" class="w-full h-full object-contain" /></div>
            <div class="flex flex-col justify-end items-start">
              <a href="tel:19632" class="flex text-white text-sm dir-ltr">19632</a>
              <a href="mailto:info@koueider.com" class="flex text-white text-sm dir-ltr">info@koueider.com</a>
            </div>
          </div>
          <div class="flex flex-col-reverse xl:flex-row justify-between gap-10">
            <div class="flex flex-wrap gap-[60px] xl:gap-[80px]">${columns}</div>
            <div class="flex flex-col items-start xl:items-end gap-[32px]">
              ${subscription}
              <ul class="flex items-center gap-4">${socials}</ul>
            </div>
          </div>
          <div class="flex flex-wrap justify-between items-center gap-6">
            <span class="font-normal text-[10px] text-bordercolor dir-ltr">© Abdel Rahim Koueider ${YEAR} - All copyrights reserved</span>
            <img src="images/payments.png" alt="payment-methods" width="215" height="24" class="object-contain" />
            <span class="text-bordercolor text-[10px]"><a href="https://www.mitchdesigns.com" target="_blank" rel="noopener noreferrer" class="hover:underline">Web Design &amp; Development by MitchDesigns</a></span>
          </div>
        </div>
      </div>
    </footer>`;
  }

  const YEAR = 2025; // static build stamp (Date.now avoided for determinism)

  /* ---------------------------------------------------------------
     Overlays: backdrop, cart drawer, mobile menu, search, location
     --------------------------------------------------------------- */
  function overlaysHTML() {
    const menuLinks = MAIN_MENU.map(
      (i) => `
      <li class="border-b border-neutral-100">
        <a href="${pageHref(i.url)}" class="flex items-center justify-between py-3.5 text-textSecondary font-medium">${esc(i.name)}${i.children ? `<span class="w-4 h-4 text-neutral-500">${ICON.arrowRight}</span>` : ""}</a>
      </li>`,
    ).join("");
    const supportLinks = SUPPORT_MENU.map(
      (i) =>
        `<li><a href="${pageHref(i.url)}" class="block py-2 text-neutral-600 text-sm">${esc(i.title)}</a></li>`,
    ).join("");

    const demoCartItems = [
      { name: "Chocolate Fudge Cake", price: 650, qty: 1, img: "images/dummy-images/new-product.png" },
      { name: "Assorted Baklava Box", price: 420, qty: 1, img: "images/menudeafult.webp" },
    ];
    const cartRows = demoCartItems
      .map(
        (it) => `
      <div class="flex gap-3 py-4 border-b border-neutral-100">
        <img src="${it.img}" alt="${esc(it.name)}" class="w-[72px] h-[72px] rounded-lg object-cover bg-primary-light" />
        <div class="flex-1">
          <p class="font-medium text-textSecondary text-sm">${esc(it.name)}</p>
          <p class="mt-1 font-semibold text-primaryDark text-sm">EGP ${it.price}</p>
          <div class="inline-flex items-center gap-3 mt-2 border border-neutral-200 rounded-full px-2 py-1" data-stepper>
            <button type="button" data-step="-1" class="w-5 h-5 grid place-items-center text-primaryDark">−</button>
            <span data-qty class="text-sm w-4 text-center">${it.qty}</span>
            <button type="button" data-step="1" class="w-5 h-5 grid place-items-center text-primaryDark">+</button>
          </div>
        </div>
      </div>`,
      )
      .join("");

    return `
    <div data-backdrop class="overlay-backdrop"></div>

    <!-- Cart drawer -->
    <aside data-drawer="cart" class="side-drawer side-drawer--right" aria-label="Shopping cart">
      <div class="flex items-center justify-between px-5 py-4 border-b border-neutral-100">
        <h2 class="font-semibold text-textSecondary text-lg">Your Cart</h2>
        <button type="button" data-close class="grid place-items-center w-8 h-8 rounded-full hover:bg-neutral-100 text-textSecondary">${ICON.close}</button>
      </div>
      <div class="flex-1 overflow-y-auto px-5">${cartRows}</div>
      <div class="px-5 py-4 border-t border-neutral-100 shadow-cart-overview">
        <div class="flex justify-between mb-3"><span class="text-neutral-600 text-sm">Subtotal</span><span class="font-semibold text-primaryDark">EGP 1,070</span></div>
        <a href="checkout.html" class="block w-full text-center bg-cta hover:bg-cta-hover text-white font-semibold py-3 rounded-full transition-colors">Checkout</a>
        <a href="cart.html" class="block w-full text-center mt-2 text-primaryDark font-medium py-2 text-sm">View full cart</a>
      </div>
    </aside>

    <!-- Mobile menu drawer -->
    <aside data-drawer="menu" class="side-drawer side-drawer--left" aria-label="القائمة">
      <div class="flex justify-between items-center bg-primary px-5 py-4 border-neutral-100 border-b text-white">
        <img src="images/abuauf/brand/logo-abuauf-white.svg" alt="أبو عوف" class="w-[110px] h-9 object-contain" />
        <button type="button" data-close class="place-items-center grid w-8 h-8 text-white">${ICON.close}</button>
      </div>
      <div class="flex-1 px-5 py-4 overflow-y-auto">
        <ul>${menuLinks}</ul>
        <div class="mt-6">
          <p class="mb-1 text-neutral-500 text-xs">روابط أخرى</p>
          <ul>${supportLinks}</ul>
        </div>
        <div class="flex flex-col gap-3 mt-6">
          <a href="login.html" class="py-2.5 border border-cta rounded-full font-medium text-cta text-sm text-center">تسجيل الدخول</a>
          <div class="flex justify-center">${countryButton()}</div>
        </div>
      </div>
    </aside>

    <!-- Search modal -->
    <div data-modal="search" class="modal-shell">
      <div class="w-full max-w-[640px] bg-white rounded-2xl shadow-custom3 overflow-hidden" data-modal-box>
        <div class="flex items-center gap-3 px-5 py-4 border-b border-neutral-100">
          <span class="w-5 h-5 text-neutral-500">${ICON.search}</span>
          <input type="search" data-search-input placeholder="Search for cakes, sweets, gifts…" class="flex-1 outline-none text-textSecondary text-base" />
          <button type="button" data-close class="grid place-items-center w-8 h-8 rounded-full hover:bg-neutral-100 text-textSecondary">${ICON.close}</button>
        </div>
        <div class="px-5 py-6">
          <p class="text-neutral-500 text-xs uppercase tracking-wide mb-3">Popular searches</p>
          <div class="flex flex-wrap gap-2">
            ${["Birthday Cakes", "Baklava", "Chocolate Boxes", "Cheesecake", "Gift Boxes"]
              .map(
                (s) =>
                  `<a href="shop-category.html" class="px-3 py-1.5 rounded-full bg-primary-light text-textSecondary text-sm hover:bg-cta hover:text-white transition-colors">${s}</a>`,
              )
              .join("")}
          </div>
        </div>
      </div>
    </div>

    <!-- Location bottom sheet -->
    <div data-sheet="location" class="bottom-sheet">
      <div class="mx-auto w-10 h-1 rounded-full bg-neutral-200 mb-4"></div>
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-semibold text-textSecondary text-lg">Choose your location</h2>
        <button type="button" data-close class="grid place-items-center w-8 h-8 rounded-full hover:bg-neutral-100 text-textSecondary">${ICON.close}</button>
      </div>
      <form data-location-form class="flex flex-col gap-3">
        <label class="block">
          <span class="label">City</span>
          <select class="placeholder-select w-full border border-neutral-200 rounded-lg px-3 h-12 mt-1 text-textSecondary">
            <option>Cairo</option><option>Giza</option><option>Alexandria</option>
          </select>
        </label>
        <label class="block">
          <span class="label">Area</span>
          <select class="placeholder-select w-full border border-neutral-200 rounded-lg px-3 h-12 mt-1 text-textSecondary">
            <option>New Cairo</option><option>Nasr City</option><option>Maadi</option><option>Zamalek</option>
          </select>
        </label>
        <button type="submit" class="mt-2 bg-cta hover:bg-cta-hover text-white font-semibold py-3 rounded-full transition-colors">Confirm location</button>
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
        toast("Thanks for subscribing! 🎉");
      }),
    );
    scope.querySelectorAll("[data-location-form]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        closeOverlay();
        toast("Delivery location updated.");
      }),
    );
    scope.querySelectorAll("[data-demo-form]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        toast(f.getAttribute("data-demo-form") || "Submitted successfully.");
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
      if (should) {
        placeholder.style.height = nav.offsetHeight + "px";
        nav.classList.add(
          "fixed",
          "top-0",
          "left-0",
          "right-0",
          "z-[100]",
          "shadow-md",
          "animate-slideDown",
        );
      } else {
        placeholder.style.height = "0px";
        nav.classList.remove(
          "fixed",
          "top-0",
          "left-0",
          "right-0",
          "z-[100]",
          "shadow-md",
          "animate-slideDown",
        );
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
  window.kInit = function (scope) {
    scope = scope || document;
    scope.querySelectorAll(".carousel").forEach(initCarousel);
    initAccordions(scope);
    initTabs(scope);
    initSteppers(scope);
    initDemoForms(scope);
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
    window.kInit(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
