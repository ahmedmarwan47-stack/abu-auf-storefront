/*
 * tw-config.js — Tailwind Play CDN configuration.
 *
 * ABU AUF design system. Values are taken directly from the Abu Auf Figma
 * variables (file tQiydoANmIdYWq0IfmTsMz), not hand-picked, so the tokens here
 * are the same ones the designs are bound to.
 *
 * The site is Arabic-first / RTL. `Baloo Bhaijaan 2` is the Arabic typeface and
 * carries the full display/heading/text scale; `Inter` is the Latin companion
 * used for prices, SKUs and English fragments.
 *
 * Note on RTL: the original used the `tailwindcss-rtl` plugin. Modern Tailwind
 * ships logical-property utilities natively (ms-*, me-*, ps-*, pe-*, start-*,
 * end-*, text-start/end, rounded-s/e) plus the `rtl:`/`ltr:` variants, so no
 * plugin is required to keep those classes working.
 */
tailwind.config = {
  theme: {
    screens: {
      xs: "414px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
    },
    container: {
      screens: {
        sm: "100%",
        md: "100%",
        lg: "1024px",
        xl: "1280px",
      },
    },
    extend: {
      fontFamily: {
        // Arabic-first: the default sans IS the Arabic face.
        sans: ['"Baloo Bhaijaan 2"', "system-ui", "sans-serif"],
        arabic: ['"Baloo Bhaijaan 2"', "sans-serif"],
        latin: ["Inter", "system-ui", "sans-serif"],
        Inter: ["Inter", "system-ui", "sans-serif"],
        // Back-compat aliases so pages not yet rebuilt still render in-brand.
        DM_Sans: ['"Baloo Bhaijaan 2"', "sans-serif"],
        Caveat: ['"Baloo Bhaijaan 2"', "sans-serif"],
      },
      animation: {
        customBounce: "customBounce 3s ease-in-out infinite",
        "spin-slow": "spin 3s linear infinite",
        slideDown: "slideDown 0.35s ease-out forwards",
      },
      keyframes: {
        slideDown: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(0)" },
        },
        customBounce: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10%)" },
        },
      },
      colors: {
        /* ---- Abu Auf core brand ---------------------------------------- */
        // Primary/Green — masthead, brand surfaces, section bands
        primary: {
          DEFAULT: "#185039",
          light: "#EDEFEB",
          hover: "#163300",
          50: "#f1f6f3",
          100: "#dceae3",
          200: "#b9d5c7",
          300: "#8fbaa6",
          400: "#5f9a80",
          500: "#347a5d",
          600: "#185039",
          700: "#14432f",
          800: "#163300",
          900: "#0d2419",
        },
        // Interaction/Primary CTA — buttons. Hover resolves LIGHTER, per Figma.
        cta: { DEFAULT: "#163300", hover: "#185039", light: "#EDEFEB" },
        // Accent/Secondary Yellow — utility bar, badges, highlights
        accent: {
          DEFAULT: "#EDC843",
          yellow: "#EDC843",
          error: "#A8200D",
          green: "#346853",
          50: "#fdf9ec",
          100: "#fbf1d0",
          200: "#f7e3a1",
          300: "#f3d572",
          400: "#EDC843",
          500: "#d9b02c",
          600: "#b38f23",
          700: "#8c6f1b",
          800: "#664f13",
          900: "#3f300b",
        },
        // Primary/Beige — hero and soft section backgrounds
        beige: {
          DEFAULT: "#E8DFD0",
          50: "#fbf9f6",
          100: "#f6f2ea",
          200: "#E8DFD0",
          300: "#dbcdb6",
          400: "#cdba9c",
          500: "#bfa782",
          600: "#a98e66",
          700: "#8a7353",
          800: "#6b5940",
          900: "#4c3f2d",
        },

        /* ---- Shared system tokens (identical in both design systems) ---- */
        interaction: {
          primary: "#163300",
          hover: "#185039",
          tertiary: "#EDEFEB",
          "tertiary-hover": "#D5DAD1",
          base: "#EDEFEB",
          divider: "#D9D9D9",
          outline: "#868685",
          disabled: "#C6C6C6",
          "secondary-text": "#777777",
        },
        neutral: {
          black: "#000000",
          white: "#FFFFFF",
          beige: "#E8DFD0",
          cream: "#FEFBFA",
          divider: "#D9D9D9",
          outline: "#868685",
          disabled: "#C6C6C6",
          secondary: "#777777",
          50: "#f9f9f9",
          100: "#f3f3f3",
          200: "#e5e5e5",
          300: "#d7d7d7",
          400: "#c9c9c9",
          500: "#bbbbbb",
          600: "#868685",
          700: "#777777",
          800: "#5a5a5a",
          900: "#3d3d3d",
        },
        gray: {
          100: "#f3f3f3",
          200: "#e5e5e5",
          300: "#D6D7D9",
          400: "#c9c9c9",
          500: "#bbbbbb",
          550: "#6E727B",
          600: "#868685",
          700: "#787878",
        },
        green: {
          100: "#e6f4ea",
          200: "#c1e2cb",
          300: "#9cd1ac",
          400: "#77bf8d",
          500: "#52ad6e",
          600: "#346853",
          700: "#2c5444",
          800: "#185039",
          900: "#163300",
        },

        /* ---- Egypt flag (locale switcher) ------------------------------ */
        flag: {
          white: "#FFFFFF",
          green: "#005B13",
          black: "#000000",
          amber: "#CC9500",
          red: "#F0263C",
        },

        /* ---- Semantic / legacy aliases --------------------------------- */
        success: "#346853",
        border: { light: "#D6D7D9" },
        primaryDark: "#163300",
        primaryExtraDark: "#0d2419",
        primaryColor: "#185039",
        primaryLight: "#E8DFD0",
        offWhite: "#EDEFEB",
        cardbadgecolor: "#A8200D",
        bordercolor: "#868685",
        black900: "#00000090",
        textSecondary: "#2C3340",
        primaryText: "#969696",
        secondaryText: "#757575",
        blackText: "#2b2525",
        customGray: "#EAEBEC",
        customGrayMedium: "#979BA0",
        ctaBackground: "#EDEFEB",
        dividerText: "#C1C3C6",
        lightBlue: "#EDEFEB",
        backgroundLocationBar: "#EDEFEB",
      },
      boxShadow: {
        "cart-utility-box": "0px 0px 2px 1px #00000014",
        custom2: "0px 2px 3px rgba(22, 51, 0, 0.2)",
        custom3: "0px 0px 8px rgba(0, 0, 0, 0.16)",
        custom4: "0px 0px 6px rgba(0, 0, 0, 0.1)",
        "custom-5": "0px 2px 6px 0px #00000014",
        "cart-overview": "0px -2px 12px 0px #1850391f",
        "cart-btn": "0px 5px 10px 0px #1850394d",
        defaultSwitcher:
          "0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)",
        "location-btn": "0px 1px 2px rgba(0, 0, 0, 0.05)",
        "search-btn": "0px 1px 2px rgba(0, 0, 0, 0.05)",
      },
      scale: { flip: "-1" },
      borderRadius: {
        DEFAULT: "0.25rem",
        sm: "0.125rem",
        md: "0.375rem",
        lg: "0.5rem",
        xl: "0.75rem",
        "2xl": "22px",
        "3xl": "32px",
        full: "9999px",
        custom: "10px",
      },
      /*
       * Type scale mirrors the Figma Arabic ramp exactly (size / line-height).
       * Display = Bold 700, Heading = SemiBold 600, Text = Medium 500.
       */
      fontSize: {
        "2xs": ["10px", "16px"],
        xs: ["12px", "18px"],
        sm: ["14px", "20px"],
        base: ["16px", "22px"],
        lg: ["18px", "26px"],
        xl: ["20px", "28px"],
        "2xl": ["24px", "36px"],
        "3xl": ["32px", "42px"],
        "4xl": ["36px", "48px"],
        "5xl": ["48px", "64px"],
        "6xl": ["60px", "72px"],
        "7xl": ["96px", "112px"],
      },
    },
  },
};
