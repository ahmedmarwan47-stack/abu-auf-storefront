"""English dictionary for the language switch — generated into i18n-en.js.

WHY THIS FILE EXISTS
--------------------
`scripts.js` used to carry the whole dictionary as one inline literal, and it
covered the chrome only: 1,457 of the 1,524 distinct Arabic strings on the
built site had no entry, so switching to English left roughly 70% of every
page in Arabic. Ahmed asked for the switch to reach everything
(2026-07-22).

Three of those surfaces could not be fixed by adding keys to that literal at
all, and are handled by the engine in `translateDocument()` instead — see the
comment there. What is left is the dictionary itself, and it belongs here
rather than in `scripts.js` for two reasons:

  * It is the only place that can read `catalog.json`, so all 99 product names
    resolve to the client's OWN English `name` field. Retyping them into a JS
    literal would be inventing data that we already have (CLAUDE.md, "real
    data over invented data").
  * Whole families of strings are formulaic — gallery labels, governorate
    rows — and are better looped than listed. `GALLERY` alone would be 40
    hand-written entries.

STATUS OF THE ENGLISH IN HERE
-----------------------------
Split deliberately into two dicts, because they do not carry the same
authority and must not be signed off as if they did:

  UI    — our own interface copy. Standard commerce terminology, written
          in-house. Placeholder pending client sign-off, same as the chrome
          strings always were.
  COPY  — the CLIENT'S OWN marketing and product prose, translated in-house.
          There is no English source for any of it: the Store API returns
          English names but never English descriptions. This is the one place
          in the project where we write English for text the client wrote in
          Arabic, and it is flagged in DESIGN-NOTES §1 as needing their
          approval before launch. Nothing here is machine-translated and
          nothing invents a claim the Arabic does not make, but it is still
          our words for their product.

Branch street addresses are deliberately NOT translated (310 of them). A
postal address is not copy — transliterating "برج نفرتيتى - تقاطع جمال عبد
الناصر" would produce something a courier cannot use. Governorate NAMES are
translated because they are also section headings.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(os.path.dirname(HERE), "static-export")

# --------------------------------------------------------------------------
# UI — our own interface copy
# --------------------------------------------------------------------------
UI = {
    # --- global chrome / actions
    "اضف الى السلة": "Add to cart",
    "عرض المزيد": "Show more",
    "شاهد الوصفة": "View recipe",
    "الوصفات": "Recipes",
    "الرئيسية": "Home",
    "تخطي إلى المحتوى": "Skip to content",
    "الإجمالي": "Total",
    "اشتري الان": "Buy now",
    "تغيير المنطقة": "Change area",
    "القائمة": "Menu",
    "تأكيد": "Confirm",
    "حذف": "Remove",
    "تعديل": "Edit",
    "عرض": "View",
    "اختر": "Select",
    "نسخ": "Copy",
    "أرسال": "Send",
    "اعرف المزيد": "Learn more",
    "اعرف أكثر": "Learn more",
    "المنتجات": "Products",
    "الفروع": "Branches",
    "المكافآت": "Rewards",
    "قصتنا": "Our Story",
    "البلوج": "Blog",
    "تواصل معنا": "Contact us",
    "أتصل بنا": "Contact Us",
    "الأسئلة الشائعة": "FAQs",
    "الأسئلة المتداولة": "FAQs",
    "تحتاج مساعدة؟": "Need help?",
    "الشروط والأحكام": "Terms & Conditions",
    "سياسة الخصوصية": "Privacy Policy",
    "سياسة الاسترجاع": "Return Policy",
    "سياسة التوصيل والاسترجاع": "Delivery & Returns",
    "تسوق منتجاتنا": "Shop our products",
    "تسوق اكتر": "Shop more",
    "تسوق اكتر من أبو عوف": "More from Abu Auf",
    "كل المنتجات": "All products",
    "تصفح المنتجات": "Browse products",
    "قائمة المنتجات": "Product list",
    "المنتجات المحفوظة": "Saved products",
    "المفضلة": "Favourites",

    # --- product page
    "عادة ما يتم شراؤه معاً: أضف هذه العناصر": "Frequently bought together: add these items",
    "أضف الجميع الى السلة": "Add all to cart",
    "وصفات بالمنتج": "Recipes with this product",
    "منتجات مشابهة": "Similar products",
    "اختر الحجم": "Choose a size",
    "الفوائد": "Benefits",
    "الفوائد:": "Benefits:",
    "الوصف:": "Description:",
    "المحتويات": "Contents",
    "طريقة الحفظ": "How to store",
    "الوزن الصافي:": "Net weight:",
    "معلومات إضافية:": "Additional information:",
    "معلومات إضافية عن المنتج:": "More about this product:",
    "مقاس البوكس:": "Box size:",
    "نسبة الخصم:": "Discount:",
    "تفاصيل العرض:": "Offer details:",
    "طرق الاستمتاع:": "Ways to enjoy:",
    "طرق الأستمتاع:": "Ways to enjoy:",
    "كيفية الاستمتاع:": "How to enjoy:",
    "كيفية الاستخدام:": "How to use:",
    "طريقة التحضير:": "How to prepare:",
    "الرائحة والطعم:": "Aroma and taste:",
    "نوع القهوة:": "Coffee type:",
    "النكهة": "Flavour",
    "نصائح": "Tips",
    "مخبوزة": "Baked",
    "نوع مقرمشات بافس:": "Puffs type:",
    "نكهة المقرمشات:": "Puffs flavour:",
    "حجم المقرمشات:": "Puffs size:",
    "حجم المنتج:": "Product size:",
    "النكهة: رائحة البيتزا الغنية مع القرمشة في كل قضمة":
        "Flavour: rich pizza aroma with a crunch in every bite",
    "النكهة: جبنة": "Flavour: cheese",

    # --- weights (units, kept as their own strings)
    "35 جم": "35 g",
    "40 جرام": "40 g",
    "50 جم": "50 g",
    "75 جم": "75 g",
    "90 جم": "90 g",
    "100 جم": "100 g",
    "100 جرام": "100 g",
    "200 جم": "200 g",
    "225 جم": "225 g",
    "250 جم": "250 g",

    # --- best-seller headings
    "الأكثر مبيعاً": "Best selling",
    "وصل حديثاً": "New arrivals",
    "الأكثر مبيعاً في مخبوزات وبسكويت": "Best selling in Baked Snacks & Biscuits",
    "الأكثر مبيعاً في البهارات والزيوت": "Best selling in Spices & Oils",
    "الأكثر مبيعاً في الهدايا والمشاركة": "Best selling in Gifting & Sharing",
    "الأكثر مبيعاً في اساسيات المطبخ": "Best selling in Kitchen & Baking",
    "الأكثر مبيعاً في مكسرات وحبوب ومقرمشات": "Best selling in Nuts, Seeds & Crackers",
    "الأكثر مبيعاً في قهوة ومشروبات": "Best selling in Coffee & Beverages",

    # --- promises strip
    "توصيل خلال ساعتين": "Delivery within two hours",
    "في القاهرة الكبرى": "across Greater Cairo",
    "استرجاع خلال 14 يوم": "Returns within 14 days",
    "من تاريخ الاستلام": "from the delivery date",
    "+316 فرعاً في مصر": "316+ branches in Egypt",
    "في 25 محافظة": "across 25 governorates",

    # --- categories
    "العروض والخصومات": "Offers & Promotions",
    "قهوة ومشروبات": "Coffee & Beverages",
    "اساسيات المطبخ": "Kitchen & Baking",
    "تمور وفواكه مجففة": "Dates & Dried Fruits",
    "الهدايا والمشاركة": "Gifting & Sharing",
    "البهارات والزيوت": "Spices & Oils",
    "مكسرات وحبوب ومقرمشات": "Nuts, Seeds & Crackers",
    "مخبوزات وبسكويت": "Baked Snacks & Biscuits",
    "سناكس صحية": "Healthy Snacks",
    "الحلويات": "Confectionery",
    "التمور والفواكه المجففة": "Dates & Dried Fruits",
    "الوجبات صحية": "Healthy Snacks",
    "الهدايا": "Gifting",
    "القهوة": "Coffee",
    "المكسرات": "Nuts",
    "قهوة": "Coffee",
    "تغذية": "Nutrition",
    "سلة هدايا": "Gift basket",

    # --- account
    "حسابي": "My account",
    "الحساب": "Account",
    "طلباتي": "My orders",
    "محفظتي": "My wallet",
    "نقاطي": "My points",
    "بيانات الحساب": "Account details",
    "عناويني": "My addresses",
    "بياناتي": "My details",
    "عضوية ذهبية": "Gold membership",
    "مرحبا محمد": "Welcome, Mohamed",
    "تسجيل الدخول": "Sign in",
    "تسجيل الخروج": "Sign out",
    "إنشاء حساب": "Create account",
    "إنشاء حساب جديد": "Create a new account",
    "كلمة السر": "Password",
    "كلمة المرور": "Password",
    "كلمة السر الجديدة": "New password",
    "تأكيد كلمة السر": "Confirm password",
    "نسيت كلمة المرور": "Forgot password",
    "نسيت كلمة المرور الخاصة بي": "I forgot my password",
    "إعادة تعيين كلمة المرور": "Reset password",
    "تغيير كلمة المرور": "Change password",
    "حفظ كلمة المرور": "Save password",
    "العودة لتسجيل الدخول": "Back to sign in",
    "سجل بأستخدام جوجل": "Sign in with Google",
    "سجل بأستخدام فيسبوك": "Sign in with Facebook",
    "المعلومات الشخصية": "Personal information",
    "حفظ التعديلات": "Save changes",
    "اختر كلمة مرور جديدة لحسابك.": "Choose a new password for your account.",
    "أدخل البريد الالكتروني المسجل وهنبعتلك رابط لإعادة تعيين كلمة المرور.":
        "Enter your registered email and we will send you a link to reset your password.",
    "لتغيير كلمة المرور، أدخل كلمة المرور الحالية ثم الجديدة.":
        "To change your password, enter your current password and then the new one.",
    "عند إنشاء حساب، هتكسب نقاط خصم في محفظتك ويمكنك الدفع بشكل أسرع والاحتفاظ بأكثر من عنوان وتتبع الطلبات والمزيد.":
        "Create an account to earn points in your wallet, check out faster, save more than one address, track your orders and more.",
    "حساب تجريبي للاختبار": "Demo account for testing",
    "استخدم البيانات دي لتجربة تسجيل الدخول والمفضلة:":
        "Use these details to try signing in and favourites:",
    "املأ البيانات تلقائياً": "Fill automatically",
    "صفحة حسابي الرئيسية": "My account home",
    "يمكنك إدارة الطلبات والمحفظة ومعلومات الحساب الخاصة بك هنا.":
        "Manage your orders, wallet and account details here.",
    "شكرا لتسجيلك حساب معنا !": "Thank you for creating an account with us!",
    "شارك الموقع مع الأصحاب والعائلة": "Share the site with friends and family",
    "أنسخ الرابط أدناه وشاركه مع عائلتك وأصدقائك واحصل على خصومات حصرية":
        "Copy the link below, share it with family and friends, and get exclusive discounts",
    "لا توجد منتجات في المفضلة": "No saved products yet",
    "المنتجات اللي تحفظها هتظهر هنا.": "Products you save will appear here.",

    # --- orders
    "طلباتي الحالية": "My current orders",
    "كل الطلبات": "All orders",
    "تفاصيل الطلب": "Order details",
    "حالة الطلب": "Order status",
    "متابعة التسوق": "Continue shopping",
    "رقم الطلب": "Order number",
    "التاريخ": "Date",
    "المجموع": "Subtotal",
    "تم الطلب": "Order placed",
    "تحت التحضير": "In preparation",
    "جاري التحضير": "Being prepared",
    "جاري تجهيز الطلب": "Order being prepared",
    "في الطريق إليك": "On its way to you",
    "تم التسليم": "Delivered",
    "مكتمل": "Completed",
    "ملغي": "Cancelled",
    "الميعاد المتوقع للتوصيل": "Estimated delivery",
    "بيانات التوصيل": "Delivery details",
    "عنوان التوصيل": "Delivery address",

    # --- wallet / points
    "رصيد محفظتي": "My wallet balance",
    "رصيد النقاط": "Points balance",
    "استبدال النقاط": "Redeem points",
    "إزاي تكسب نقاط؟": "How do you earn points?",
    "اكسب نقطة على كل جنيه تشتريه من الموقع":
        "Earn a point for every pound you spend on the site",
    "نقاط إضافية عند تقييم المنتجات اللي اشتريتها":
        "Extra points for reviewing products you have bought",
    "مكافأة ترحيبية عند إنشاء حساب جديد": "A welcome bonus when you create an account",
    "سجل المعاملات": "Transaction history",
    "استرداد من طلب #30941": "Refund from order #30941",
    "خصم على طلب #30942": "Discount on order #30942",
    "مكافأة تسجيل": "Sign-up bonus",
    "خصم المحفظة": "Wallet discount",
    "خصم كود الخصم": "Promo code discount",
    "خصم المبلغ": "Apply discount",
    "إلغاء الخصم": "Remove discount",
    "الدفع من المحفظة": "Pay from wallet",
    "هل لديك برومو كود؟": "Have a promo code?",
    "اكتب الكود": "Enter code",
    "تطبيق": "Apply",
    "تم تطبيق الكود": "Code applied",
    "كود غير صالح": "Invalid code",
    "اختر الفرع": "Choose a branch",
    "تأكيد الفرع": "Confirm branch",
    "المحافظة": "Governorate",
    "لا توجد فروع في هذه المحافظة": "No branches in this governorate",
    "حدد اليوم والوقت": "Pick a day & time",
    "تأكيد الموعد": "Confirm time",
    "اليوم": "Today",
    "تم الخصم من رصيدك": "Deducted from your balance",
    "كل ما تشتري أكثر من أبوعوف هتكسب نقط و فلوس":
        "The more you buy from Abu Auf, the more points and cash you earn",
    "اجمع نقاطك مع كل طلب من أبو عوف، وتابع رصيدك ومستوى عضويتك من صفحة النقاط في حسابك.":
        "Collect points with every Abu Auf order, and track your balance and membership tier from the points page in your account.",

    # --- cart / checkout
    "سلة التسوق": "Shopping cart",
    "ملخص السلة": "Cart summary",
    "مصاريف التوصيل": "Delivery fee",
    "هل لديك برومو كود؟": "Have a promo code?",
    "أضف ملاحظات على الطلب": "Add order notes",
    "أطلب الآن": "Order now",
    "أكمل إلى الدفع": "Continue to payment",
    "إتمام عملية الشراء بأمان": "Secure checkout",
    "تأكيد عملية الشراء": "Confirm purchase",
    "طريقة الدفع": "Payment method",
    "بيانات العميل": "Customer details",
    "نوع الطلب": "Order type",
    "طلب عادي": "Standard order",
    "إهداء الطلب": "Send as a gift",
    "أرسل الطلب كهدية لشخص تحبه": "Send this order as a gift to someone you love",
    "وقت التوصيل": "Delivery time",
    "في غضون 60 دقيقة": "Within 60 minutes",
    "أختار تاريخ": "Choose a date",
    "حدد اليوم والوقت المناسب": "Pick the day and time that suits you",
    "طريقة التوصيل": "Delivery method",
    "توصيل": "Delivery",
    "بإضافة مصاريف اضافية": "An extra fee applies",
    "الاستلام من المتجر": "Pick up in store",
    "الاستلام من الفرع": "Pick up from a branch",
    "مواعيد التوصيل": "Delivery times",
    "خطوات الشراء": "Checkout steps",

    # --- forms
    "الاسم الأول": "First name",
    "اسم العائلة": "Last name",
    "الاسم الاخير": "Last name",
    "الاسم": "Name",
    "رقم الهاتف": "Phone number",
    "البريد الالكتروني": "Email",
    "الموضوع": "Subject",
    "الرسالة": "Message",
    "المدينة": "City",
    "الحي": "District",
    "المنطقة": "Area",
    "رقم العقار و الشارع": "Building number and street",
    "نوع العقار": "Property type",
    "رقم الشقة": "Apartment number",
    "الشقة": "Apartment",
    "شقة": "Apartment",
    "فيلا": "Villa",
    "الطابق": "Floor",
    "قبول الشروط": "Accept the terms",
    "اضف عنوان": "Add address",
    "العنوان الرئيسي": "Main address",
    "عنواني الرئيسي": "My main address",

    # --- demo record values
    "محمد": "Mohamed",
    "عادل": "Adel",
    "محمد عادل": "Mohamed Adel",
    "شقة 3 - 220 شارع الحرية - الدور الأول": "Apt 3 - 220 El Horreya Street - First floor",
    "مبنى 12 - شارع التسعين الشمالي": "Building 12 - North Ninety Street",
    "التجمع الخامس، القاهرة": "Fifth Settlement, Cairo",
    "مصر الجديدة، القاهرة": "Heliopolis, Cairo",
    "مصر الجديدة": "Heliopolis",
    "القاهرة، مصر": "Cairo, Egypt",
    "القاهرة الجديدة": "New Cairo",
    "شارع 5 عقار رقم 4": "Street 5, building 4",
    "23 مارس 2026": "23 March 2026",
    "28 مارس 2026": "28 March 2026",
    "21 مارس 2026": "21 March 2026",
    "14 مارس 2026": "14 March 2026",

    # --- listing
    "ترتيب حسب": "Sort by",
    "السعر: من الأقل": "Price: low to high",
    "السعر: من الأعلى": "Price: high to low",
    "لا توجد منتجات في هذا القسم حالياً.": "No products in this section yet.",

    # --- home
    "أبو عوف — قهوة ومكسرات وتمور وسناكس صحية":
        "Abu Auf — coffee, nuts, dates and healthy snacks",
    "20٪": "20%",
    "اعثر على الهدية المثالية لكل شخص وكل مناسبة":
        "Find the perfect gift for every person and every occasion",
    "تسوق الهدايا": "Shop gifts",
    "أراء العملاء": "Customer reviews",
    "كل التعليقات": "All reviews",
    "آخر الأخبار": "Latest news",
    "أشهي الوصفات من أبو عوف": "The tastiest recipes from Abu Auf",
    "كل الوصفات": "All recipes",
    "اكتشف الفروع": "Discover our branches",
    "منتجات أبو عوف خارج مصر": "Abu Auf Worldwide",
    "عن أبو عوف": "About Abu Auf",
    "أقرب فرع": "Nearest branch",
    "المتجر مغلق حالياً": "The store is currently closed",

    # --- store copy (ours)
    "نحن نغير مفهوم الأكل الصحي في جميع أنحاء العالم":
        "We are changing what healthy eating means, all over the world",
    "سنة التأسيس": "Founded",
    "فرع في مصر": "branches in Egypt",
    "محافظة": "governorates",
    "جودة في كل خطوة": "Quality at every step",
    "نغذي العقل والروح": "Nourishing mind and spirit",
    "أكثر من 30 نكهة قهوة لذيذة تنعش الحواس — من التركي والبرازيلي للإسبريسو والقهوة المطحونة طازة، محمصة على أصولها ومعبأة تحافظ على الريحة لآخر فنجان.":
        "More than 30 delicious coffee flavours to wake up the senses — from Turkish and Brazilian to espresso and freshly ground coffee, properly roasted and packed to hold the aroma to the last cup.",
    "قهوة برازيلي": "Brazilian coffee",
    "قهوة مطحونة طازجة": "Freshly ground coffee",
    "إسبريسو": "Espresso",
    "قهوة سريعة التحضير": "Instant coffee",
    "مشروبات ساخنة": "Hot drinks",
    # Real coffee sub-category labels off the live abuauf.com filter bar.
    "قهوة تركي معبأة": "Packed Turkish coffee",
    "قهوة برازيلي معبأة": "Packed Brazilian coffee",
    "قهوة مطحونة فريش": "Freshly ground coffee",
    "قهوة بالنكهات": "Flavoured coffee",
    "قهوة فرنسية": "French coffee",
    "مشروبات ساخنه": "Hot drinks",
    "قهوة خضراء": "Green coffee",
    "قهوة عربي": "Arabic coffee",
    "عصائر": "Juices",

    # --- reviews (in-house placeholder personas)
    "التمور والمكسرات دايماً طازة وجودتها ثابتة، وبيوصلوا بسرعة. أبو عوف بقى جزء أساسي من تسوق البيت عندنا.":
        "The dates and nuts are always fresh and consistently good, and they arrive quickly. Abu Auf has become a fixture of our household shop.",
    "منى عبد الله — القاهرة": "Mona Abdallah — Cairo",
    "القهوة التركي بتاعتهم أحلى حاجة جربتها، والطحن بيكون مظبوط على حسب طلبك. التغليف كمان بيحافظ على الريحة.":
        "Their Turkish coffee is the best I have tried, and the grind is exactly as you ask for it. The packaging holds the aroma too.",
    "أحمد فؤاد — الجيزة": "Ahmed Fouad — Giza",
    "طلبت هدايا لمناسبة عائلية والتغليف كان شيك جداً. الأسعار كويسة مقارنة بالجودة اللي بتاخدها.":
        "I ordered gifts for a family occasion and the packaging was very smart. The prices are good for the quality you get.",
    "سارة محمود — الإسكندرية": "Sara Mahmoud — Alexandria",
    "بحب قسم السناكس الصحية، فيه اختيارات كتير للأطفال واللانش بوكس. الخدمة سريعة والفروع منتشرة.":
        "I love the healthy snacks section — plenty of choices for children and lunch boxes. The service is fast and the branches are everywhere.",
    "كريم سمير — المنصورة": "Karim Samir — Mansoura",

    # --- blog
    "كل المقالات": "All articles",
    "أحدث المقالات": "Latest articles",
    "مقالات ذات صلة": "Related articles",
    "قراءة ٥ دقائق": "5 min read",
    "نصائح سريعة": "Quick tips",
    "نصائح ووصفات ومعلومات عن القهوة والمكسرات والتمور والأكل الصحي — من فريق أبو عوف.":
        "Tips, recipes and know-how on coffee, nuts, dates and healthy eating — from the Abu Auf team.",
    "فوائد المكسرات النيئة لصحة القلب": "The heart benefits of raw nuts",
    "المكسرات مصدر غني بالدهون الصحية والألياف، وإضافتها لنظامك اليومي أسهل مما تتخيل.":
        "Nuts are a rich source of healthy fats and fibre, and working them into your day is easier than you think.",
    "دليلك لاختيار درجة تحميص القهوة": "Your guide to choosing a coffee roast",
    "من التحميص الفاتح للغامق، كل درجة ليها طابع مختلف. تعرف على الفرق واختار اللي يناسب ذوقك.":
        "From light to dark, every roast has its own character. Learn the difference and pick the one that suits your taste.",
    "التمور: طاقة طبيعية في كل قطعة": "Dates: natural energy in every piece",
    "التمور مش بس حلوة المذاق، ده كمان مصدر سريع للطاقة وغنية بالبوتاسيوم والألياف.":
        "Dates are not just sweet — they are a fast source of energy and rich in potassium and fibre.",
    "أفكار لانش بوكس صحي للأطفال": "Healthy lunch box ideas for children",
    "تشكيلة سناكس تجمع بين الطعم اللذيذ والقيمة الغذائية، سهلة التحضير وبتفضل طازة.":
        "A range of snacks that combine good taste with real nutrition — easy to prepare and they stay fresh.",
    "دليل البهارات: إزاي تختار وتحفظ": "A spice guide: how to choose and store",
    "البهارات الطازة بتفرق في أي طبق. اعرف إزاي تختارها وتحفظها عشان تحافظ على نكهتها.":
        "Fresh spices change any dish. Learn how to choose and store them so they keep their flavour.",
    "جرانولا بيتي بالمكسرات والعسل": "Homemade granola with nuts and honey",
    "وصفة بسيطة تعملها في البيت وتفضل معاك أسبوع كامل، مثالية للفطار السريع.":
        "A simple recipe you can make at home that keeps for a week — ideal for a quick breakfast.",
    "المكسرات من أقدم الأطعمة اللي عرفها الإنسان، ولحد النهارده فضلت واحدة من أغنى المصادر الطبيعية للدهون الصحية والبروتين والألياف. الدراسات بتشير إن تناول حفنة صغيرة يومياً بيرتبط بتحسن في صحة القلب ومستويات الكوليسترول.":
        "Nuts are among the oldest foods people have eaten, and they remain one of the richest natural sources of healthy fats, protein and fibre. Studies link a small handful a day with better heart health and cholesterol levels.",
    "الفرق بين المكسرات النيئة والمحمصة مش بس في الطعم. التحميص على درجات حرارة عالية ممكن يقلل نسبة بعض الفيتامينات الحساسة للحرارة، وعشان كده بنحمص على دفعات صغيرة وبدرجات محسوبة تحافظ على القيمة الغذائية والنكهة في نفس الوقت.":
        "The difference between raw and roasted nuts is not only taste. Roasting at high temperatures can reduce some heat-sensitive vitamins, which is why we roast in small batches at measured temperatures that protect the nutrition and the flavour at once.",
    "أحسن طريقة تدخل بيها المكسرات في يومك إنك تخليها في متناول إيدك — علبة صغيرة على المكتب أو في شنطة الشغل. جربها كمان فوق الزبادي أو السلطة، أو اطحنها وحطها في العجين للمخبوزات.":
        "The best way to work nuts into your day is to keep them within reach — a small tub on your desk or in your work bag. Try them over yoghurt or salad too, or grind them into dough for baking.",
    "ابدأ بكمية صغيرة — حفنة يومياً كفاية": "Start small — a handful a day is enough",
    "نوّع بين اللوز والكاجو وعين الجمل عشان تنوع العناصر":
        "Mix almonds, cashews and walnuts so you vary the nutrients",
    "احفظها في برطمان محكم بعيد عن الحرارة والضوء":
        "Keep them in an airtight jar away from heat and light",
    "جرانولا بار بالتمر والمكسرات": "Date and nut granola bars",
    "مخبوزات الطازة هي أحلى أختيار لنقنقة سريعة او لافكار لذيذة في اللانش بوكس، اختار النوع اللي تحبه.":
        "Fresh bakes are the best choice for a quick nibble or a tasty lunch box idea — pick the one you like.",
    "قهوة مثلجة بزبدة الفول السوداني": "Iced coffee with peanut butter",
    "وصفة سريعة تجمع بين القهوة المطحونة الطازة وزبدة الفول السوداني لمشروب غني ومنعش.":
        "A quick recipe pairing freshly ground coffee with peanut butter for a rich, refreshing drink.",
    "كيكة التمر بالقرفة والشيكولاتة البيضاء": "Date cake with cinnamon and white chocolate",
    "وصفة سهلة تجمع بين حلاوة التمر ودفء القرفة، جاهزة في أقل من ساعة.":
        "An easy recipe pairing the sweetness of dates with the warmth of cinnamon, ready in under an hour.",
    "فتوتشيني ألفريدو دجاج مع الكاجو": "Chicken alfredo fettuccine with cashews",
    "طبق كريمي غني بالمكسرات، مناسب لعشاء سريع في نص ساعة.":
        "A creamy dish rich with nuts, right for a quick dinner in half an hour.",

    # --- about / export
    "تأسست شركة أبو عوف في عام 2010 وأصبحت من أشهر الأسماء في الأسواق لتقديم منتجات القهوة الطبيعية عالية الجودة والمكسرات وزبد المكسرات والأطعمة الصحية والفاكهة المجففة.. وأكثر.":
        "Abu Auf was founded in 2010 and has become one of the best-known names in the market for high-quality natural coffee, nuts, nut butters, healthy foods, dried fruit and more.",
    "فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل خطوة في عملية الإنتاج في أبو عوف تُدار بعناية لضمان إنتاج منتجات عالية الجودة يتم توصيلها بحب وملئها بالمكونات المغذية من الطبيعة الأم.":
        "Every product has its own story, and because we pay constant attention to detail, every step of production at Abu Auf is handled carefully to ensure high-quality products, delivered with care and filled with nourishing ingredients from mother nature.",
    "نعطي الأولوية لابتكار المنتجات ونأخذ في الاعتبار اتجاهات السوق ورغبات العملاء وتغيُّر الأذواق، كما نشجع دائمًا نمط الحياة الصحي؛ لأن هدفنا ليس فقط تغذية الجسم، بل تغذية العقل والروح أيضًا.":
        "We put product innovation first, taking account of market trends, customer wishes and changing tastes, and we always encourage a healthy lifestyle — because our aim is not only to nourish the body, but the mind and spirit too.",
    # The home page runs the two about paragraphs together in one node, so the
    # joined form needs its own key — exact-match matching cannot compose it
    # from the two entries above.
    "تأسست شركة أبو عوف في عام 2010 وأصبحت من أشهر الأسماء في الأسواق لتقديم منتجات القهوة الطبيعية عالية الجودة والمكسرات وزبد المكسرات والأطعمة الصحية والفاكهة المجففة.. وأكثر. فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل خطوة في عملية الإنتاج في أبو عوف تُدار بعناية لضمان إنتاج منتجات عالية الجودة يتم توصيلها بحب وملئها بالمكونات المغذية من الطبيعة الأم.":
        "Abu Auf was founded in 2010 and has become one of the best-known names in the market for high-quality natural coffee, nuts, nut butters, healthy foods, dried fruit and more. Every product has its own story, and because we pay constant attention to detail, every step of production at Abu Auf is handled carefully to ensure high-quality products, delivered with care and filled with nourishing ingredients from mother nature.",
    "خدمات التصدير": "Export services",
    "ما بين أسواق أوروبا، آسيا، أمريكا و الوطن العربي":
        "Across the markets of Europe, Asia, the Americas and the Arab world",
    "رصيد ثقة كافي نتيجة نجاحنا مع شركائنا":
        "A record of trust built on our success with our partners",
    "نصّدر الأصناف الأكثر طلباً في الأسواق العالمية":
        "We export the lines most in demand in world markets",
    "التمور المصرية": "Egyptian dates",
    "المشاركة بالمعارض الدولية": "Taking part in international trade fairs",
    "اتجهت شركة \"أبوعوف\" للتصدير إلى الأسواق العالمية، ما بين الأسواق الأوروبية والأسيوية والأمريكية بالإضافة إلى الأسواق العربية. اهتمت الشركة بمراعاة متطلبات كل سوق على حدة و تلبية احتياجات العملاء، و ذلك بالتواصل المستمر مع الأسواق الخارجية والتواجد بالمعارض العالمية. تمكنت شركة \"أبوعوف\" من الانتشار في الأسواق الخارجية والتي تضم مختلف الدول. وتسعى شركة \"أبوعوف\" للتوسع في باقي الأسواق.":
        "Abu Auf has turned to exporting into world markets — European, Asian and American as well as Arab. The company has been careful to observe the requirements of each market separately and to meet customers' needs, through continuous contact with markets abroad and a presence at international trade fairs. Abu Auf has established itself across foreign markets spanning a range of countries, and continues to seek expansion into the rest.",
    "يسر شركة أبو عوف أن تعلن عن مشاركتها في أبرز المعارض الدولية، تشمل هذه المشاركة معرض جلفود في الفترة من عام 2020 حتى عام 2023، ومعرض انوجا في الفترة من عام 2017 حتى عام 2019، ومعرض سيال في عام 2018، بالإضافة إلى معرض الصين الدولي للاستيراد اكسبو في عام 2019. نحن نسعى لزيادة تواجدنا في المعارض القادمة لنكون أقرب إلى عملاء جدد ولنستمر في تحقيق أهدافنا وتقديم منتجاتنا المتميزة.":
        "Abu Auf is pleased to announce its participation in the leading international trade fairs: Gulfood from 2020 to 2023, Anuga from 2017 to 2019, SIAL in 2018, and the China International Import Expo in 2019. We aim to increase our presence at future fairs, to be closer to new customers and to keep meeting our goals and presenting our products.",

    # --- contact
    "لو عندك أي استفسار أو اقتراح، إحنا هنا. اختار الطريقة اللي تناسبك أو ابعتلنا رسالة وهنرد عليك في أقرب وقت.":
        "If you have a question or a suggestion, we are here. Choose whichever way suits you, or send us a message and we will reply as soon as we can.",
    "الخط الساخن": "Hotline",
    "واتساب": "WhatsApp",
    "المقر الرئيسي": "Head office",
    "المنطقة الصناعية 31-33، التجمع الثالث، القاهرة الجديدة، مصر":
        "Industrial Zone 31-33, Third Settlement, New Cairo, Egypt",
    "ابعتلنا رسالة": "Send us a message",
    "فريق خدمة العملاء جاهز يساعدك": "Our customer service team is ready to help",
    "لسه عندك سؤال؟": "Still have a question?",

    # --- FAQ
    "الطلب والتوصيل": "Ordering and delivery",
    "إزاي أطلب من الموقع؟": "How do I order from the site?",
    "اختار المنتجات اللي تحبها وضيفها للسلة، بعدين اضغط على «أطلب الآن» واملأ بيانات التوصيل. هتوصلك رسالة تأكيد على البريد الالكتروني ورقم الهاتف.":
        "Choose the products you like and add them to the cart, then press “Order now” and fill in your delivery details. You will get a confirmation by email and text message.",
    "الطلب بيوصل في قد إيه؟": "How long does delivery take?",
    "داخل القاهرة الكبرى التوصيل خلال ساعتين. باقي المحافظات من يوم لثلاثة أيام عمل حسب المنطقة.":
        "Within Greater Cairo, delivery takes two hours. Other governorates take one to three working days depending on the area.",
    "كام الحد الأدنى للطلب؟": "What is the minimum order?",
    "الحد الأدنى للطلب 150 جنيه، ومصاريف التوصيل بتحسب حسب المنطقة وبتظهر قبل تأكيد الطلب.":
        "The minimum order is EGP 150. Delivery is charged by area and is shown before you confirm the order.",
    "أقدر أستلم من الفرع؟": "Can I pick up from a branch?",
    "أيوه — اختار «الاستلام من المتجر» في صفحة إتمام الشراء وحدد الفرع الأقرب ليك.":
        "Yes — choose “Pick up in store” at checkout and select the branch nearest to you.",
    "الدفع": "Payment",
    "طرق الدفع المتاحة إيه؟": "Which payment methods can I use?",
    "بنقبل الدفع عند الاستلام، بطاقات الائتمان (فيزا وماستركارد)، اتصالات كاش، وفاليو، بالإضافة لرصيد المحفظة.":
        "We accept cash on delivery, credit cards (Visa and Mastercard), Etisalat Cash, ValU, and your wallet balance.",
    "الدفع أونلاين آمن؟": "Is paying online secure?",
    "أيوه، كل عمليات الدفع بتتم من خلال بوابة دفع مؤمنة، وإحنا مابنحتفظش ببيانات بطاقتك.":
        "Yes. All payments go through a secured payment gateway, and we do not store your card details.",
    "المنتجات والاسترجاع": "Products and returns",
    "المنتجات طازة إزاي؟": "How are the products kept fresh?",
    "بنحمص ونعبّي على دفعات صغيرة، والتغليف بيحافظ على النكهة والريحة لحد ما يوصلك.":
        "We roast and pack in small batches, and the packaging holds the flavour and aroma until it reaches you.",
    "أقدر أرجّع منتج؟": "Can I return a product?",
    "تقدر تطلب استرجاع خلال 14 يوم من الاستلام طالما المنتج في حالته الأصلية وغير مفتوح. راجع سياسة الاسترجاع للتفاصيل.":
        "You can request a return within 14 days of delivery as long as the product is unopened and in its original condition. See the return policy for details.",
    "إزاي أكسب نقاط؟": "How do I earn points?",
    "بتكسب نقاط على كل جنيه بتشتريه، وتقدر تستبدلها كخصم على طلبك القادم من صفحة نقاطي.":
        "You earn points on every pound you spend, and you can redeem them as a discount on your next order from the My points page.",

    # --- legal (already in-house placeholder; see DESIGN-NOTES)
    "البيانات اللي بنجمعها": "The data we collect",
    "إزاي بنستخدم بياناتك": "How we use your data",
    "مشاركة البيانات": "Sharing data",
    "حقوقك": "Your rights",
    "بنجمع البيانات اللي بتدخلها بنفسك عند إنشاء حساب أو إتمام طلب: الاسم، البريد الالكتروني، رقم الهاتف، وعناوين التوصيل.":
        "We collect the data you enter yourself when creating an account or completing an order: name, email, phone number and delivery addresses.",
    "بنجمع كمان بيانات تقنية عن استخدامك للموقع زي نوع المتصفح والصفحات اللي بتزورها، وده بيساعدنا نحسّن التجربة.":
        "We also collect technical data about your use of the site, such as browser type and the pages you visit, which helps us improve the experience.",
    "بنستخدم بياناتك عشان نجهز طلباتك ونوصّلها، ونتواصل معاك بخصوص حالة الطلب، ونبعتلك عروض لو اخترت تشترك في النشرة البريدية.":
        "We use your data to prepare and deliver your orders, to contact you about order status, and to send you offers if you have chosen to subscribe to the newsletter.",
    "مابنبيعش بياناتك لأي طرف ثالث. بنشاركها بس مع شركات الشحن وبوابات الدفع بالقدر اللازم لإتمام طلبك.":
        "We do not sell your data to any third party. We share it only with couriers and payment gateways, and only as far as is needed to complete your order.",
    "تقدر تطلب الاطلاع على بياناتك أو تعديلها أو حذفها في أي وقت من خلال التواصل معنا على info@abuauf.com.":
        "You can ask to see, correct or delete your data at any time by contacting us at info@abuauf.com.",
    "الأسعار والمنتجات": "Prices and products",
    "الطلبات والإلغاء": "Orders and cancellation",
    "باستخدامك لموقع أبو عوف أو بإتمام طلب من خلاله، فإنك توافق على الشروط والأحكام الموضحة في هذه الصفحة.":
        "By using the Abu Auf site or placing an order through it, you agree to the terms and conditions set out on this page.",
    "أنت مسؤول عن الحفاظ على سرية بيانات الدخول الخاصة بحسابك، وعن كل النشاط اللي بيتم من خلاله.":
        "You are responsible for keeping your account login details confidential, and for all activity that takes place through it.",
    "كل الأسعار بالجنيه المصري وشاملة الضرائب المطبقة. بنحتفظ بحقنا في تعديل الأسعار أو إيقاف أي منتج في أي وقت.":
        "All prices are in Egyptian pounds and include applicable taxes. We reserve the right to change prices or discontinue any product at any time.",
    "بنبذل مجهود إن صور ووصف المنتجات تكون دقيقة، لكن ممكن يحصل اختلاف بسيط في اللون أو الشكل عن الصورة المعروضة.":
        "We make every effort to keep product images and descriptions accurate, but slight differences in colour or shape from the image shown are possible.",
    "بنحتفظ بحقنا في رفض أو إلغاء أي طلب في حالة عدم توفر المنتج أو وجود خطأ في السعر. في الحالة دي هيتم رد المبلغ بالكامل.":
        "We reserve the right to refuse or cancel any order where the product is unavailable or the price is wrong. In that case the amount is refunded in full.",
    "داخل القاهرة الكبرى: التوصيل خلال ساعتين من تأكيد الطلب.":
        "Within Greater Cairo: delivery within two hours of order confirmation.",
    "باقي المحافظات: من يوم إلى ثلاثة أيام عمل حسب المنطقة.":
        "Other governorates: one to three working days depending on the area.",
    "مصاريف التوصيل بتتحدد حسب المنطقة وبتظهر واضحة في صفحة إتمام الشراء قبل تأكيد الطلب.":
        "Delivery charges are set by area and are shown clearly at checkout before you confirm the order.",
    "تقدر تختار «الاستلام من المتجر» وتستلم طلبك من أقرب فرع ليك بدون مصاريف توصيل.":
        "You can choose “Pick up in store” and collect your order from your nearest branch with no delivery charge.",
    "تقدر تطلب استرجاع أي منتج خلال 14 يوم من تاريخ الاستلام، بشرط إن المنتج يكون في حالته الأصلية وغير مفتوح.":
        "You can request a return on any product within 14 days of delivery, provided it is unopened and in its original condition.",
    "المنتجات الغذائية المفتوحة لا يمكن استرجاعها لأسباب تتعلق بالسلامة الغذائية.":
        "Opened food products cannot be returned, for food safety reasons.",
    "بيتم رد المبلغ بنفس طريقة الدفع خلال 7 أيام عمل من استلام المنتج المرتجع.":
        "Refunds are issued to the original payment method within 7 working days of us receiving the returned product.",

    # --- thank you
    "شكراً لك": "Thank you",
    "تم تقديم طلبك بنجاح": "Your order was placed successfully",
    "بأنتظار تأكيد متجر": "Awaiting store confirmation",
    "سيتم تجهيز الطلب قريباً": "Your order will be prepared shortly",
    "طلبك في الطريق إليك": "Your order is on its way",
    "تم تسليم الطلب": "Order delivered",
    "سعدنا بخدمتك ونود أن تراك مرة أخرى":
        "It was a pleasure serving you — we hope to see you again",

    # --- branches page
    "فروع أبو عوف": "Abu Auf branches",

    # --- hero product copy (ours, translated from the client's English)
    "استمتع بالنكهات الخفيفة والمشرقة من بن أبو عوف البرازيلي فاتح التحميص. مذاق ناعم ومنعش، مثالي لمن يفضلون التحميص الفاتح في فنجانهم اليومي.":
        "Enjoy the light, bright flavours of Abu Auf light-roast Brazilian coffee. Smooth and refreshing, ideal for anyone who prefers a light roast in their daily cup.",
    "تحميص فاتح": "Light roast",
    "نكهة خفيفة ومشرقة": "Light, bright flavour",
    "حبوب مختارة بعناية": "Carefully selected beans",
    "مذاق ناعم": "Smooth taste",
    "مناسب للتحضير اليومي": "Right for everyday brewing",
    "نكهات خفيفة ومشرقة من التحميص الفاتح": "Light, bright flavours from a light roast",
    "حبوب برازيلية مختارة بعناية": "Carefully selected Brazilian beans",
    "مذاق ناعم ومنعش مناسب للتحضير اليومي":
        "A smooth, refreshing taste suited to everyday brewing",
    "يحفظ في عبوة محكمة الغلق بعيداً عن الرطوبة":
        "Keep in an airtight container away from moisture",
    "بعيداً عن أشعة الشمس المباشرة ومصادر الحرارة":
        "Away from direct sunlight and sources of heat",
    "يفضل الطحن قبل التحضير مباشرة للحفاظ على النكهة":
        "Best ground just before brewing to preserve the flavour",

    # --- misc product names that are not catalogue entries
    "لب سورى مقشر": "Peeled Syrian seeds",
    "بريتزل جبنة - 200 جم": "Cheese pretzels - 200 g",
    "بريتزل كاتشب - 200 جم": "Ketchup pretzels - 200 g",
    "بريتزل باربكيو - 200 جم": "Barbecue pretzels - 200 g",
    "لوز مملح فاخر": "Premium salted almonds",
    "ملح الهيمالايا الصخري ناعم": "Fine Himalayan rock salt",
}

# --------------------------------------------------------------------------
# Templates — keyed on the element's content with element children as slots
# --------------------------------------------------------------------------
TPL = {
    "({0} تقييم)": "({0} reviews)",
    "{0} التوصيل خلال ساعتين في القاهرة الكبرى":
        "{0} Delivery within two hours across Greater Cairo",
    "ضمن أفضل {0} مبيعاً في أبو عوف": "Among the top {0} best sellers at Abu Auf",
    "ضمن أفضل {0} مبيعاً في مخبوزات وبسكويت":
        "Among the top {0} best sellers in Baked Snacks & Biscuits",
    "ضمن أفضل {0} مبيعاً في البهارات والزيوت":
        "Among the top {0} best sellers in Spices & Oils",
    "ضمن أفضل {0} مبيعاً في الهدايا والمشاركة":
        "Among the top {0} best sellers in Gifting & Sharing",
    "ضمن أفضل {0} مبيعاً في اساسيات المطبخ":
        "Among the top {0} best sellers in Kitchen & Baking",
    "ضمن أفضل {0} مبيعاً في مكسرات وحبوب ومقرمشات":
        "Among the top {0} best sellers in Nuts, Seeds & Crackers",
    "ضمن أفضل {0} مبيعاً في قهوة ومشروبات":
        "Among the top {0} best sellers in Coffee & Beverages",
    "{0}الرئيسية": "{0}Home",
    "{0}طلباتي": "{0}My orders",
    "{0}المفضلة": "{0}Favourites",
    "{0}عناويني": "{0}My addresses",
    "{0}محفظتي": "{0}My wallet",
    "{0}نقاطي": "{0}My points",
    "{0}بيانات الحساب": "{0}Account details",
    "{0} تسجيل الخروج": "{0} Sign out",
    "البريد الالكتروني{0}": "Email{0}",
    "رقم الهاتف{0}": "Phone number{0}",
    "الاسم الأول{0}": "First name{0}",
    "الاسم الاخير{0}": "Last name{0}",
    "الاسم{0}": "Name{0}",
    "الرسالة{0}": "Message{0}",
    "المدينة{0}": "City{0}",
    "الحي{0}": "District{0}",
    "المنطقة{0}": "Area{0}",
    "رقم العقار و الشارع{0}": "Building number and street{0}",
    "نوع العقار{0}": "Property type{0}",
    "رقم الشقة{0}": "Apartment number{0}",
    "تشكيلة متنوعة تبدا من {0} جنية": "A varied range starting from EGP {0}",
    "الوزن الصافي: {0}": "Net weight: {0}",
    "رصيدك {0}": "Your balance {0}",
    "طلب رقم {0}": "Order number {0}",
    "250 جم · عدد {0}": "250 g · qty {0}",
    "{0} منتج": "{0} products",
    "({0} منتج)": "({0} products)",
    "عدد {0}": "Qty {0}",
    "يوجد أكثر من {0} فرع لأبو عوف في {1} محافظة في مصر — اختر محافظتك لتجد أقرب فرع إليك.":
        "There are more than {0} Abu Auf branches across {1} governorates in Egypt — choose your governorate to find the one nearest you.",
    "يوجد أكثر من {0} فرع أبو عوف في مصر, أكتشف الأقرب اليك":
        "There are more than {0} Abu Auf branches in Egypt — find the one nearest you",
    "{0}متبقي {1} لاستكمال الحد الأدنى للطلب":
        "{0}{1} to go to reach the minimum order",
    "هل لديك حساب بالفعل؟ {0}": "Already have an account? {0}",
    "لديك حساب بالفعل؟ {0}": "Already have an account? {0}",
    "أوافق على {0}": "I agree to the {0}",
    "خصم يصل إلى {0} على قسم": "Up to {0} off in",
    "يمكنك خصم {0} من طلبك القادم": "You can take {0} off your next order",
    "{0} في حالة عمل طلب من قبل كضيف (بدون حساب)، الرجاء عمل حساب الآن بنفس الإيميل المستخدم في الطلب لمتابعة حالة الشحن.":
        "{0} If you have ordered before as a guest (without an account), please create an account now with the same email used on the order so you can track its status.",
    "{0} إذا كان لديك حساب على موقعنا السابق، فبرجاء إنشاء اسم مستخدم وكلمة مرور جديدين على هذا الموقع الجديد.":
        "{0} If you had an account on our previous site, please create a new username and password on this new one.",
    "مواعيد العمل من {0} صباحاً حتى {1} مساءً يومياً. تقدر تتصفح المنتجات دلوقتي وتكمل طلبك في المواعيد.":
        "Opening hours are {0}am to {1}pm daily. You can browse the products now and complete your order during those hours.",
    "إذا كانت لديك أسئلة حول طلبك، يمكنك مراسلتنا عبر البريد الإلكتروني على {0} أو الاتصال بنا على {1}":
        "If you have questions about your order, email us at {0} or call us on {1}",
    "ثقة عملاء شركة \"أبو عوف\" وتجاربهم المتميزة دفعتها إلى تلبية احتياجات السوق المتزايدة، لذلك لديهم الآن قسم خاص بتوريد الطلبات بكميات كبيرة للشركات وبتواجدها بأكبر عدد ممكن من الأماكن. لدى الشركة رصيد ثقة كافي نتيجة نجاحها مع شركاء متميزين في السوق المصري من فنادق، مطاعم، كافيهات، وشركات. لذا، لا تتردد في التواصل مع الشركة. لدى الشركة أيضا فريق متخصص في التعامل المهني {0} من حيث الالتزام بالمواعيد والحفاظ على جودة المنتجات والتغليف وطريقة العرض.":
        "The trust of Abu Auf's customers and their excellent experiences have driven the company to meet growing market demand, and it now has a dedicated division supplying bulk orders to businesses across as many locations as possible. The company has built a record of trust through its success with distinguished partners in the Egyptian market — hotels, restaurants, cafes and corporates. Do not hesitate to get in touch. The company also has a team specialising in professional service {0} in punctuality, product quality, packaging and presentation.",
}

# --------------------------------------------------------------------------
# COPY — the client's own product prose. In-house English, needs sign-off.
# --------------------------------------------------------------------------
COPY = {
    # coffee
    "نكهة غنية وقوية لتجربة قهوة مميزة.": "A rich, strong flavour for a distinctive coffee experience.",
    "يزيد من الطاقة ويعزز التركيز.": "Lifts your energy and sharpens focus.",
    "غني بمضادات الأكسدة لبداية صحية.": "Rich in antioxidants for a healthy start.",
    "فوائد القهوة:": "Coffee benefits:",
    "يمنحك تجربة قهوة عربية غنية وأصيلة -": "Gives you a rich, authentic Arabic coffee experience -",
    "يعزز اليقظة والتركيز": "Boosts alertness and concentration",
    "يوفر طقوس قهوة مريحة وعطرية": "Makes for a comforting, aromatic coffee ritual",
    "استكشف لذة القهوة الفاتحة بنكهتها الرائعة.":
        "Discover the pleasure of light-roast coffee and its wonderful flavour.",
    "تتميز بنكهة خفيفة مع لمحات ناعمة من الزهور والحمضيات مما يخلق تجربة طعم منعشة ورائعة.":
        "It has a light flavour with soft floral and citrus notes, making for a refreshing and delightful taste.",
    "مصنوعة من حبوب بن أرابيكا الفاخرة، المعروفة بتنوع ونكهتها الرائعة.":
        "Made from premium Arabica beans, known for their range and excellent flavour.",
    "قهوة محمصة متوسطة بدون إضافات.": "Medium-roast coffee with no additives.",
    "تتميز بنكهة متوازنة، مع لمحات خفيفة من الجوز، وتركيبة ناعمة تُسعد الحواس.":
        "It has a balanced flavour with light walnut notes and a smooth body that delights the senses.",
    "حبوب القهوة: مصنوعة من حبوب البن العربيكا عالية الجودة، المشهورة بنكهتها المتوازنة والمعقدة.":
        "Coffee beans: made from high-quality Arabica beans, renowned for their balanced and complex flavour.",
    "بن أبو عوف محوج فاتح، يقدم تجربة قهوة خفيفة ولذيذة.":
        "Abu Auf lightly spiced coffee offers a light and delicious coffee experience.",
    "إنها مثالية في الصباح لبدأ يومك بنشاط وحيوية.":
        "It is ideal in the morning to start your day with energy.",
    "وصديقة رائعة أثناء استراحات العمل، لاستكمال يومك المزدحم بمزاج مظبوط.":
        "And great company on a work break, to carry you through a busy day in the right mood.",
    "بن أبو عوف محوج وسط - 100 جم.": "Abu Auf medium-spiced coffee - 100 g.",
    "استمتع بالتوازن بين نكهة بن أبو عوف المميزة مع مذاق التحويجة المتوسطة.":
        "Enjoy the balance between Abu Auf's distinctive coffee and a medium spice blend.",
    "سواء كانت لحظة صباحية روتينية أو لشحن طاقتك في منتصف اليوم، هذه القهوة مثالية لجميع اللحظات.":
        "Whether it is a morning routine or a midday recharge, this coffee suits every moment.",
    "مأخوذ بعناية من أفضل المزارع في فيتنام والبرازيل وكينيا. له طعم طبيعي لذيذ.":
        "Carefully sourced from the best farms in Vietnam, Brazil and Kenya. A delicious natural taste.",

    # generic benefit bullets
    "وجبة متعددة الاستخدامات: مناسبة للكبار والأطفال في أي وقت وفي أي مكان.":
        "A versatile snack: right for adults and children, any time and anywhere.",
    "جودة عالية: مصنوعة من مكونات عالية الجودة لطعم لذيذ.":
        "High quality: made with high-quality ingredients for a delicious taste.",
    "نكهة غنية: مزيج لذيذ من الشوكولاتة والبندق.":
        "Rich flavour: a delicious blend of chocolate and hazelnut.",
    "كريمي ومقرمش: شوكولاتة ناعمة مع بندق مقرمش.":
        "Creamy and crunchy: smooth chocolate with crisp hazelnuts.",
    "وجبة خفيفة مريحة: بحجم مناسب للتناول السريع.":
        "A convenient snack: sized for eating on the go.",
    "قرمشة لذيذة: يجمع بين قرمشة البريتزل وغنى اللوز.":
        "Delicious crunch: pretzel crispness meets the richness of almonds.",
    "مالح وحلو: نكهة متوازنة مع لمسة من الملوحة وحلاوة المكسرات.":
        "Salty and sweet: a balanced flavour with a touch of salt and nutty sweetness.",
    "وجبة خفيفة مريحة: بحجم مناسب للاستمتاع أثناء التنقل.":
        "A convenient snack: sized to enjoy while you are out and about.",
    "خفيف ومقرمش: منتفخ بشكل مثالي ليمنحك قرمشة ممتعة.":
        "Light and crisp: perfectly puffed for a satisfying crunch.",
    "وجبة خفيفة متعددة الاستخدامات: استمتع به سادة أو مع إضافاتك المفضلة.":
        "A versatile snack: enjoy it plain or with your favourite toppings.",
    "خيار قليل السعرات: بديل صحي للعديد من الوجبات الخفيفة.":
        "A lower-calorie option: a healthy alternative to many snacks.",
    "غني بالعناصر الغذائية: مليء بالبروتين والدهون الصحية والفيتامينات الأساسية.":
        "Nutrient rich: packed with protein, healthy fats and essential vitamins.",
    "غني بمضادات الأكسدة: يدعم الصحة العامة ويساعد في مكافحة الجذور الحرة.":
        "Rich in antioxidants: supports general health and helps fight free radicals.",
    "يعزز صحة القلب: يحتوي على دهون صحية تعزز صحة القلب والأوعية الدموية.":
        "Supports heart health: contains healthy fats that benefit the heart and blood vessels.",
    "نكهة قوية: يضيف لمسة حارة وجريئة للأطباق بفضل ناعميته":
        "Strong flavour: its fine grind adds a warm, bold touch to dishes",
    "استخدامات متعددة: مثالي لتحسين طعم اللحوم، الخضروات، الشوربات، والصلصات":
        "Many uses: ideal for lifting the taste of meat, vegetables, soups and sauces",
    "تعبئة مريحة: بحجم مثالي للاستخدام اليومي وسهل التخزين":
        "Convenient packaging: sized for everyday use and easy to store",
    "نكهة منعشة: يضيف طعماً حمضياً وحلواً خفيفاً للأطباق":
        "Refreshing flavour: adds a light citrus sweetness to dishes",
    "غني بالعناصر الغذائية: يحتوي على الفيتامينات والمعادن الأساسية":
        "Nutrient rich: contains essential vitamins and minerals",
    "يساعد على الهضم: يدعم الهضم الصحي ويقلل الانتفاخ":
        "Aids digestion: supports healthy digestion and reduces bloating",
    "وجبة خفيفة مغذية: غنية بالفيتامينات والدهون الصحية.":
        "A nourishing snack: rich in vitamins and healthy fats.",
    "تحميص مثالي: استمتع بالنكهة الغنية والمكسرات لبذور عباد الشمس المحمصة.":
        "Perfectly roasted: enjoy the rich, nutty flavour of roasted sunflower seeds.",
    "استخدام متعدد: رائعة بمفردها أو كإضافة للسلطات، الزبادي، والأطباق.":
        "Versatile: great on their own or added to salads, yoghurt and dishes.",
    "طعمه لذيذ، نكهته مميزة وقوامة مقرمش.":
        "Delicious taste, distinctive flavour and a crunchy texture.",
    "الذ اختيار لعشاء خفيف صحي او فطور سريع حيث أنه مليء بالعناصر الغذائية مثل: مصدر مميز للبروتين، غني بالألياف والفيتامينات.":
        "The tastiest choice for a light healthy dinner or a quick breakfast, packed with nutrients: an excellent source of protein, rich in fibre and vitamins.",
    "يمكن استخدامه في مختلف وصفات الحلوة والحادقة بما فيهم المشروبات.":
        "It can be used in all kinds of sweet and savoury recipes, drinks included.",
    "يعتبر اختيار مثالي كوجبة خفيفة صحية وسريعة لجميع الأعمار.":
        "An ideal choice as a quick, healthy snack for all ages.",
    "يحتوي على الدهون الصحية والبروتين ومناسب لجميع النظم الغذائية (الدايت).":
        "It contains healthy fats and protein and suits every kind of diet.",
    "- مصدر أمريكي موثوق: الفستق المحمص لدى أبو عوف يأتي مباشرة من أمريكا، لضمان للجودة والمذاق الرائع.":
        "- A trusted American source: Abu Auf's roasted pistachios come straight from the United States, for guaranteed quality and great taste.",
    "- تجربة مقرمشة فريدة: مع كل حبة مقرمشة من الفستق، ستدرك أنه الأفضل بلا منازع عن باقي انواع المكسرات الاخرى.":
        "- A uniquely crunchy experience: with every crisp pistachio you will find it is unbeatable among nuts.",
    "جودة عالية وطازجة.": "High quality and fresh.",
    "مقرمش لا يقاوم ولذيذ.": "Irresistibly crunchy and delicious.",
    "طبقة جبن لنكهة إضافية غنية.": "A cheese coating for extra rich flavour.",
    "طازج، مقرمش ومختار بعناية.": "Fresh, crunchy and carefully selected.",
    "مغطاة بالشوكولاتة اللذيذة لمزيد من النكهات الشهية.":
        "Coated in delicious chocolate for even more flavour.",
    "تسالي خفيفة مغذية وسهلة التناول في أي مكان وأي وقت.":
        "A light, nourishing snack that is easy to eat anywhere, any time.",
    "مذاق محمص، مقرمش وطازج وعالي الجودة.":
        "A roasted taste — crunchy, fresh and high quality.",
    "مغذي ولذيذ وغني بالعناصر الغذائية المفيدة للجميع.":
        "Nourishing, delicious and rich in nutrients that are good for everyone.",
    "مثالي للتسالي الخفيفة والوجبات السريعة الصحية.":
        "Ideal for light snacking and quick healthy meals.",
    "جربه فوق أنواع السلطات المفضلة لديك، لقرمشة صحية وخفيفة.":
        "Try it over your favourite salads for a light, healthy crunch.",
    "اخلطه مع الشوكولاتة والفواكه المجففة لمذاق يجمع بين الحادق والحلو.":
        "Mix it with chocolate and dried fruit for a taste that is both savoury and sweet.",
    "طازج وعالي الجودة: يتمتع لوزنا المملح بالطازجة الدائمة والجودة العالية.":
        "Fresh and high quality: our salted almonds are consistently fresh and of high quality.",
    "-مناسب لتناولة والاستمتع بمزيج النكهات تلك الالذيذة اثناء ايام العمل في وقت الراحة لتجدد طاقتك بنكهتة الشهية":
        "- Right for enjoying this delicious mix of flavours during a break on a working day, to restore your energy with its appetising taste",
    "-حلي مشاهدات المبارايات مع مذاق مقرمشة ونكهة الكراميل اللذيذة":
        "- Sweeten match nights with a crunchy texture and delicious caramel flavour",
    "-اختيار لذيذ لسهرات الاصدقاء و الاهل":
        "- A delicious choice for evenings with friends and family",
    "مثالي لتسالي السفر بسبب حجمه الصغير وخفته.":
        "Ideal as a travel snack thanks to its small size and light weight.",
    "غني بالكراميل والملح (كراميل مملح).": "Rich with caramel and salt (salted caramel).",
    "جاهز للأكل مباشرة ومناسب لجميع الأعمار.":
        "Ready to eat straight away and suitable for all ages.",
    "مزيج لذيذ من مقرمشات صينية فاخرة، تحتوي على نكهات مميزة.":
        "A delicious mix of premium Chinese crackers with distinctive flavours.",
    "قرمشة لا تقاوم في كل قضمة.": "An irresistible crunch in every bite.",
    "تنوع في تناولها: استمتع بها بمفردك، أو أضفها إلى السلطات، أو امزجها مع مجموعتنا الفاخرة من المكسرات.":
        "Enjoy them however you like: on their own, added to salads, or mixed with our premium range of nuts.",
    "يمكن استخدام ملح الهيمالايا للطهي أو على السلطات، تماما مثل الملح العادي.":
        "Himalayan salt can be used for cooking or on salads, exactly like ordinary salt.",
    "عزز نكهة أطباقك عن طريق إضافته إلى الصلصات والمرقات، أو يمكن استخدامة مع المخبوزات الحادقة والحلوة بشكل طبيعي مثل الملح":
        "Lift your dishes by adding it to sauces and stocks, or use it in savoury and sweet baking just as you would ordinary salt",
    "استمتع بمزيج مثالي من الكاكاو مع القهوة والشوكولاتة في بروتين بار صحي ولذيذ من أبو عوف.":
        "Enjoy a perfect blend of cocoa, coffee and chocolate in a healthy, delicious Abu Auf protein bar.",
    "وجبة خفيفة تجدد طاقتك وتساعدك على استكمال يومك بنشاط متجدد.":
        "A snack that restores your energy and helps you carry on through the day.",
    "خالي من السكر والجلوتين: مثالي للذين يهتمون بتقليل استهلاك السكر والجلوتين.":
        "Sugar free and gluten free: ideal for anyone cutting down on sugar and gluten.",
    "بروتين بار بنكهة البندق من أبو عوف يجمع بين حلاوة الشوكولاتة الداكنة ونكهة البندق المحمصة لتصبح نكهة لذيذة ومميزة.":
        "Abu Auf's hazelnut protein bar brings together the sweetness of dark chocolate and the flavour of roasted hazelnuts for a delicious, distinctive taste.",
    "غني بالألياف": "Rich in fibre",
    "مصدر عالي البروتين (22 جم بروتين في كل بار)":
        "A high-protein source (22 g of protein per bar)",
    "تحضير وجبة فطور شهية من حبوب الشوفان مع الاضافات المفضلة لديك مثل الفواكهة":
        "Make an appetising breakfast of oats with your favourite additions, such as fruit",
    "تحضير الكوكيز كبديل صحي للدقيق او ممكن في المخبوزات ايضا":
        "Make cookies with it as a healthy alternative to flour, or use it in baking generally",
    "الأفراد الذين يسعون لزيادة استهلاكهم اليومي من الألياف.":
        "People looking to increase their daily fibre intake.",
    "الأشخاص الذين يهتمون بصحتهم": "People who care about their health",
    "النباتيين والنباتيين الصارمين": "Vegetarians and vegans",
    "الأشخاص الباحثين عن تحسين صحة القلب والهضم":
        "People looking to improve heart health and digestion",
    "بذور الشيا من أبو عوف هي مصدر غني بالألياف وأحماض أوميغا-3 والبروتين.":
        "Abu Auf chia seeds are a rich source of fibre, omega-3 and protein.",
    "تمنحك هذه البذور الصغيرة الطاقة والشعور بالشبع لفترة طويلة.":
        "These small seeds give you energy and keep you feeling full for longer.",
    "مناسبة للنباتيين والمتبعين لنظام غذائي خالٍ من الجلوتين.":
        "Suitable for vegetarians and anyone on a gluten-free diet.",
    "نكهة لذيذة: يتميز لب القرع المقشر من أبو عوف بنكهة لذيذة وغنية بالعناصر الغذائية.":
        "Delicious flavour: Abu Auf's peeled pumpkin seeds have a delicious taste and are rich in nutrients.",
    "غني بالعناصر: يحتوي هذا المنتج على تركيز عالي من العناصر الغذائية الأساسية، مما يجعله خيارًا صحيًا.":
        "Nutrient dense: this product contains a high concentration of essential nutrients, making it a healthy choice.",
    "خالٍ من الجلوتين: مناسب للأشخاص الذين يعانون من حساسية الجلوتين.":
        "Gluten free: suitable for people with a gluten intolerance.",
    "زبدة الفول السوداني الكريمية والغنية.": "Creamy, rich peanut butter.",
    "طعم استثنائي وجودة عالية.": "Exceptional taste and high quality.",
    "مكونات طبيعية بالكامل.": "Entirely natural ingredients.",
    "انتشرها على الخبز، البسكويت، أو الفواكه.": "Spread it on bread, biscuits or fruit.",
    "استخدمها في السندويشات، العصائر، أو أثناء الخبز.":
        "Use it in sandwiches, smoothies or baking.",
    "كن إبداعيًا في الوصفات والوجبات الخفيفة.": "Be creative with recipes and snacks.",
    "بلح عضوي محشى باللوز يقدم مذاقًا فريدًا ولذيذًا يناسب أي وقت من اليوم.":
        "Organic dates stuffed with almonds, for a unique and delicious taste at any time of day.",
    "مثالي لتناوله صباحًا مع فنجان قهوة دافئة من أبو عوف، يمنحك الطاقة لبداية نهار مليء بالحيوية.":
        "Ideal in the morning with a warm cup of Abu Auf coffee, giving you the energy to start a lively day.",
    "وجبة خفيفة صحية: تناولها بديلًا صحيًا للوجبات الغنية بالسعرات الحرارية.":
        "A healthy snack: eat them as a healthy alternative to calorie-heavy foods.",
    "مزيج متناغم من الحلاوة الطبيعية من التمور ونكهة اللوز المقرمش ونعومة الشوكولاتة.":
        "A harmonious blend of natural date sweetness, crunchy almonds and smooth chocolate.",
    "تعمل كمحسن للمزاج، تعزز من الشعور بالسعادة والاسترخاء.":
        "They lift the mood, encouraging a sense of happiness and calm.",
    "تحتوي على مضادات الأكسدة، مما يساعد في تقليل التوتر الأكسدي في الجسم.":
        "They contain antioxidants, which help reduce oxidative stress in the body.",
    "تناولها كوجبة خفيفة سريعة ومنبهة للطاقة.":
        "Eat them as a quick, energising snack.",
    "حلوى طبيعية ولذيذة تناسب أي وقت من اليوم.":
        "A natural, delicious sweet for any time of day.",
    "شهيرة بطعمها الغني وملمسها الرائع.":
        "Known for their rich taste and wonderful texture.",
    "تمور عضوية مغطاة بطبقة رقيقة من الشوكولاته.":
        "Organic dates covered in a thin layer of chocolate.",
    "زبيب صغير ولا يحتوي على بذور.": "Small, seedless raisins.",
    "طعم حلو وفاكهي، ملمس مطاطي ولذيذ.":
        "A sweet, fruity taste with a chewy, delicious texture.",
    "مثالي للتناول الخفيف، أو الخبز، أو التطبيقات الطهي.":
        "Ideal for snacking, baking or cooking.",
    "تين اسباني فاخر: تين اسباني مجفف أصيل من اسبانيا، ضمان للجودة والنكهة الاستثنائية.":
        "Premium Spanish figs: authentic dried figs from Spain, for guaranteed quality and exceptional flavour.",
    "نكهة فريدة: طعم غني ولذيذ مع رائحة مميزة، مما يجعله الخيار المفضل لعشاق التين.":
        "A unique flavour: a rich, delicious taste with a distinctive aroma, making it the favourite for fig lovers.",
    "مصدر مباشر: مستورد مباشرة من اسبانيا، مما يحافظ على النكهة والطازج.":
        "Sourced directly: imported straight from Spain, which preserves the flavour and freshness.",
    "كوجبة خفيفة: استمتع بحفنة كوجبة خفيفة ومشبعة.":
        "As a snack: enjoy a handful as a filling snack.",
    "استمتع بأجود أنواع الزبيب من أبو عوف.": "Enjoy the finest raisins from Abu Auf.",
    "تمتع بها كوجبة خفيفة منفردة أو أضفها إلى أطباقك المفضلة.":
        "Enjoy them on their own as a snack or add them to your favourite dishes.",
    "استمتع بطعمها الحلو الطبيعي من أفضل أنواع الزبيب في مصر.":
        "Enjoy their natural sweetness — the finest raisins in Egypt.",
    "استمتع بعلبة معمول بعجوة المجدول المغطاة بالشيكولاتة، تجربة لذيذة تجمع بين تميز التمر ونعومة الشيكولاتة.":
        "Enjoy a box of maamoul with Medjool date paste covered in chocolate — a delicious experience combining fine dates with smooth chocolate.",
    "كل لقمة تقدم سيمفونية من النكهات الفريدة والملمس الهش، مثالية لمرافقة قهوتك اليومية أو كوجبة خفيفة صحية خلال يوم عمل طويل.":
        "Every bite offers a symphony of unique flavours and a crumbly texture — perfect alongside your daily coffee or as a healthy snack through a long working day.",
    "غمر نفسك في طعم الشوكولاتة الفاخرة المغطاة بالمعمول، لحظات سعادة في كل قطعة لذيذة.":
        "Immerse yourself in the taste of fine chocolate over maamoul — moments of happiness in every delicious piece.",
    "مزيج مثالي من التوابل الفاخرة": "A perfect blend of premium spices",
    "يعزز النكهة الطبيعية للدجاج": "Brings out the natural flavour of chicken",
    "سهل الاستخدام ومتعدد الاستخدامات": "Easy to use and versatile",
    "استمتع بحفنة كوجبة خفيفة ومشبعة.": "Enjoy a handful as a filling snack.",
    "استخدمها في الخبز والحلويات أو الأطباق المالحة لإضافة الحلاوة.":
        "Use them in baking and desserts, or in savoury dishes to add sweetness.",
    "مثالية للأيام المزدحمة أو كوجبة خفيفة في حقيبة الغداء للأطفال.":
        "Ideal for busy days or as a snack in children's lunch boxes.",
    "منخفضة الدهون والصوديوم، وغنية بالنكهة.": "Low in fat and sodium, and full of flavour.",
    "مناسبة للكبار والأطفال في أي وقت وفي أي مكان.":
        "Right for adults and children, any time and anywhere.",
    "مصنوعة من مكونات عالية الجودة لطعم لذيذ.":
        "Made with high-quality ingredients for a delicious taste.",
    "تزيد من الطاقة، وتساعد في الهضم، وتدعم الصحة العامة.":
        "They lift your energy, aid digestion and support general health.",
    "يعزز أطباق السلطات والشوفان والعديد من الأطباق الأخرى.":
        "It lifts salads, oats and many other dishes.",
    "يمكن استخدامه في تحضير المخبوزات لإضافة نكهة مميزة.":
        "It can be used in baking to add a distinctive flavour.",
    "يُعتبر خيارًا مثاليًا لتناول سناك خفيف وصحي وملئ بالطاقة.":
        "An ideal choice for a light, healthy and energising snack.",
    "مثالي لتقديمه في السهرات والتجمعات كسناك خفيف.":
        "Ideal to serve at evenings and gatherings as a light snack.",
    "يعد سناكس خفيفًا ومقرمشًا يعزز تجربة مشاهدة الأفلام والمسرحيات.":
        "A light, crunchy snack that improves any film or theatre night.",
}


# --------------------------------------------------------------------------
# CHROME — Arabic literals that live in scripts.js template literals
#
# These never appear in the generated HTML, so the HTML scan cannot see them:
# the mega-menu subcategory lists, the toasts, the drawers, the country and
# address data. They reach the page through the injected chrome and are picked
# up by translateDocument()'s walk of <body>, so they only need dictionary
# entries — no code change at the call sites.
# --------------------------------------------------------------------------
CHROME = {
    "أبو عوف": "Abu Auf",
    "السلة": "Cart",
    "بحث": "Search",
    "إغلاق": "Close",
    "إنقاص": "Decrease",
    "زيادة": "Increase",
    "السابق": "Previous",
    "التالي": "Next",
    "مسار التنقل": "Breadcrumb",
    "4.8 من 5": "4.8 out of 5",
    "اقرأ المزيد": "Read more",
    "إظهار كلمة السر": "Show password",
    "إخفاء كلمة السر": "Hide password",
    "أضف ملاحظة": "Add a note",
    "ملاحظات على الطلب": "Order notes",
    "فرع أبو عوف": "Abu Auf branch",
    "جميع حقوق النشر تنتمي إلى ابو عوف,": "All rights reserved, Abu Auf,",
    # Size-variant SKU names that are not a catalogue `nameAr`, so
    # _catalog_names() cannot reach them; they survive only in card alt text.
    "بن برازيلى فاتح محوج - 100 جم": "Light Spiced Brazilian Coffee - 100 g",
    "بهارات فراخ - 75 جم": "Chicken Spices - 75 g",
    "العدد:": "Qty:",
    "أضف": "Add",
    # mega-menu subcategories
    "مكسرات": "Nuts",
    "مكسرات نيئة": "Raw nuts",
    "مكسرات محمصة ومملحة": "Roasted and salted nuts",
    "مكسرات بنكهات": "Flavoured nuts",
    "تشكيلة مكسرات": "Nut selections",
    "حبوب ومقرمشات": "Seeds and crackers",
    "قهوة تركي": "Turkish coffee",
    "قهوه تركي": "Turkish coffee",
    "قهوه": "Coffee",
    "تمر": "Dates",
    "تمور": "Dates",
    "فواكه مجففة": "Dried fruit",
    "ألواح صحية": "Healthy bars",
    "سناكس بروتين": "Protein snacks",
    "حبوب صحية": "Healthy grains",
    "بروتين": "Protein",
    "مخبوزات": "Baked goods",
    "مشروبات": "Drinks",
    "مطبخ": "Kitchen",
    "وصفات": "Recipes",
    "اليوم": "Today",
    "الشوكولاتة": "Chocolate",
    "التجمع": "The Settlement",
    # locale / country
    "العربية": "Arabic",
    "مصر": "Egypt",
    "الامارات": "UAE",
    "الامارات العربية المتحدة": "United Arab Emirates",
    # location sheet
    "أختار منطقة التوصيل": "Choose a delivery area",
    "تأكيد المنطقة": "Confirm area",
    "التوصيل الى الشروق - القاهرة": "Delivery to El Shorouk - Cairo",
    "تم تحديث منطقة التوصيل.": "Delivery area updated.",
    # addresses
    "المنزل": "Home",
    "العمل": "Work",
    "المنزل، العمل…": "Home, Work…",
    "المنطقة، المدينة": "Area, city",
    "رقم الشقة والمبنى واسم الشارع": "Apartment, building and street name",
    "تمت إضافة العنوان": "Address added",
    "تم تعديل العنوان": "Address updated",
    "تم حذف العنوان": "Address deleted",
    # search
    "الأكثر بحثاً": "Most searched",
    "أدخل عنوان البريد الالكتروني": "Enter your email address",
    # newsletter / footer
    "اشترك لتعرف على أجدد العروض والخصومات":
        "Subscribe to hear about the newest offers and discounts",
    "كن أول من يعرف كل ما هو جديد في ابو عوف":
        "Be the first to know what is new at Abu Auf",
    "تم الاشتراك بنجاح! 🎉": "Subscribed successfully! 🎉",
    "تم الإرسال بنجاح.": "Sent successfully.",
    "انستجرام": "Instagram",
    "فيسبوك": "Facebook",
    "يوتيوب": "YouTube",
    "لينكد إن": "LinkedIn",
    # payment methods
    "الدفع عند الاستلام": "Cash on delivery",
    "اتصالات كاش": "Etisalat Cash",
    # toasts
    "تمت الإضافة إلى السلة": "Added to cart",
    "تمت الإزالة من السلة": "Removed from cart",
    "تمت إضافة ملاحظتك على الطلب": "Your order note was added",
    "تمت إزالة الملاحظات": "Notes removed",
    "تم تطبيق التفضيلات": "Preferences applied",
    "تم إلغاء خصم المحفظة": "Wallet discount removed",
    "تم خصم": "Discounted",
    "من الإجمالي": "from the total",
    "متبقي": "remaining",
    "لاستكمال الحد الأدنى للطلب": "to reach the minimum order",
    "تعذر النسخ — انسخ الرابط يدوياً": "Could not copy — copy the link manually",
    # FAQ / contact intros
    "عندك اي اسئلة؟ كل حاجة هنا..": "Got questions? Everything is here…",
    "لو عندك أي استفسار أو عايز تطرح أي سؤال ، هتلاقي كل حاجة هنا":
        "If you have a query or want to ask a question, you will find everything here",
    # banner alt text
    "قهوة تركي بالتوت — جديد من أبو عوف":
        "Berry Turkish coffee — new from Abu Auf",
    "تمور المجدول الفاخرة": "Premium Medjool dates",
    "تشكيلة أبو عوف المميزة": "The Abu Auf signature selection",
    "أبو عوف الآن في الإمارات": "Abu Auf is now in the UAE",
    "البريتزل": "Pretzels",
    "معمول": "Maamoul",
    # offer names
    "عرض سناكس بروتين بزبدة الفول السودانى 35 جم":
        "Peanut butter protein snack offer 35 g",
    "عرض معمول سادة وقرفة وشيكولاتة":
        "Plain, cinnamon and chocolate maamoul offer",
    "مارشميلو بطيخ - 60 جرام": "Watermelon marshmallow - 60 g",
}

# --------------------------------------------------------------------------
# COPY2 — the remaining client product prose (see COPY above; same status).
# --------------------------------------------------------------------------
COPY2 = {
    # spices
    "يعزز النكهة دون عناء وسهل الاستخدام": "Lifts flavour effortlessly and is easy to use",
    "توابل للحم والخضروات والسلطات.": "A seasoning for meat, vegetables and salads.",
    "دمجه في التتبيلات والصلصات.": "Blend it into marinades and sauces.",
    "إضافته إلى الخبز المحلي أو زبدة الثوم.": "Add it to homemade bread or garlic butter.",
    "جمبري بزبدة الثوم:": "Garlic butter prawns:",
    "في التتبيل": "In marinades",
    "مع وصفات الفراخ او اللحم مثل الوصفات الهندية الشعبية":
        "With chicken or meat recipes, such as popular Indian dishes",
    "مع الشورب أو بأي طريقة تفضلها": "With soup, or however you prefer",
    "فركها على اللحوم قبل الشواء أو الخبز.":
        "Rub it into meat before grilling or roasting.",
    "مناسبة للتبديل أو التتبيل.": "Good as a rub or a marinade.",
    "رش على الحلويات، الشوفان، والمشروبات الساخنة.":
        "Sprinkle over desserts, oats and hot drinks.",
    "امزجه في الكاري والأطباق المطبوخة للحصول على نكهة دافئة.":
        "Stir it into curries and cooked dishes for a warm flavour.",
    "مثالي للبتي فور، الكعك، والفطائر.": "Ideal for petit fours, cakes and pastries.",
    "يرش على الدجاج المتبل قبل الطهي": "Sprinkle over marinated chicken before cooking",
    "المثالية للشواء أو التحميص أو القلي": "Ideal for grilling, roasting or frying",
    "يرفع من نكهة الحساء واليخنات والصلصات": "Lifts soups, stews and sauces",
    "دجاج بالثوم والبارميزان": "Garlic and parmesan chicken",
    "مكونات:": "Ingredients:",
    "المكونات:": "Ingredients:",
    "المكونات": "Ingredients",
    "أفخاذ دجاج": "Chicken thighs",
    "بهارات الدجاج": "Chicken seasoning",
    "مسحوق الثوم": "Garlic powder",
    "جبنة البارميزان": "Parmesan cheese",
    "زيت الزيتون": "Olive oil",
    "اخلطي بهارات الدجاج، وبودرة الثوم، والبارميزان المبشور.":
        "Mix the chicken seasoning, garlic powder and grated parmesan.",
    "يُغطى الدجاج بالخليط ويُرش بزيت الزيتون.":
        "Coat the chicken in the mixture and drizzle with olive oil.",
    "اخبزيها حتى يصبح الدجاج ذهبي اللون ويصل إلى درجة حرارة داخلية آمنة.":
        "Bake until the chicken is golden and has reached a safe internal temperature.",
    "استخدام متعدد الاستخدامات: مثالي لأطباق مختلفة مثل الدجاج واللحوم المتبلة أو فوق وصفات المعكرونة أو السلطة":
        "Versatile: ideal for a range of dishes such as chicken and marinated meats, or over pasta and salad",
    "مثالي لأطباق مختلفة مثل الدجاج واللحوم المتبلة أو فوق وصفات المعكرونة أو السلطة":
        "Ideal for a range of dishes such as chicken and marinated meats, or over pasta and salad",
    "أفكار الاستخدام:": "Serving ideas:",
    "السعرات الحرارية:": "Calories:",
    "تتغير حسب المكونات": "Varies with the ingredients",
    "مناسب للأفراد الذين يحبون نكهة الثوم.": "Right for anyone who loves garlic.",
    "طريقة الاستخدام:": "How to use:",
    "قلي الجمبري في زبدة الثوم، عصير الليمون، اتركه حتى يصبح لون الجمبري وردي..":
        "Fry the prawns in garlic butter and lemon juice until they turn pink.",
    # snacks / biscuits
    "استمتع برائحة الشوكولاتة الرائعة والقرمشة المُرضية للحبوب المقرمشة الممزوجة بشكل مثالي لتخلق علاجًا لذيذًا.":
        "Enjoy a wonderful chocolate aroma and the satisfying crunch of crisped grains, perfectly blended into a delicious treat.",
    "استمتع بها مباشرة من العبوة لتناول وجبة خفيفة سريعة ولذيذة.":
        "Enjoy them straight from the pack for a quick, tasty snack.",
    "تقدم هذه الوجبات الخفيفة البروتينية نكهة لذيذة ،عبارة عن مزيج مثالي من الطماطم المنعشة والنكهات الترابية للريحان.":
        "These protein snacks deliver a delicious flavour — a perfect blend of fresh tomato and earthy basil.",
    "يمكن أضافتة إلي السهرات والتجمعات": "Good for evenings and gatherings",
    "مناسب لتسالي سريعة وسط اليوم": "Right for a quick midday snack",
    "يتميز بسكويت أبو عوف بنكهة الجبن برائحة البسكويت الطازج مع لمسة الجبن اللذيذة. الطعم هو التوازن المثالي بين الطعم المقرمش والجبني.":
        "Abu Auf cheese biscuits carry the aroma of freshly baked biscuits with a delicious touch of cheese — a perfect balance of crunchy and cheesy.",
    "أنها تحتوي على العناصر الغذائية الأساسية، مما يضيف قيمة إلى وقت تناول الوجبات الخفيفة لطفلك.":
        "They contain essential nutrients, adding value to your child's snack time.",
    "يعد هذا البسكويت على شكل سمكة متعة عند تناوله وإضافة إبداعية إلى صناديق الغداء للأطفال.":
        "These fish-shaped biscuits are fun to eat and a creative addition to children's lunch boxes.",
    "تتميز مقرمشات أبو عوف المملحة على شكل سمكة برائحة رقيقة من المقرمشات المخبوزة الطازجة والتوازن المثالي للملح، مما يوفر قرمشة مرضية مع كل قضمة.":
        "Abu Auf salted fish-shaped crackers have the delicate aroma of freshly baked crackers and a perfect balance of salt, giving a satisfying crunch in every bite.",
    "يمكن الاستمتاع بهذه المقرمشات اللذيذة على شكل سمكة لمفردها، مما يجعلها وجبة خفيفة مريحة ولذيذة للمدرسة أو النزهات أو ليالي مشاهدة الأفلام.":
        "These delicious fish-shaped crackers can be enjoyed on their own, making a convenient, tasty snack for school, picnics or film nights.",
    "أو يمكن الأستمتاع بها مع صوص الجبن او اي نكهة من الصوصات المفضلة،لتصبح تسالي لذيذة مقرمشة .":
        "Or enjoy them with cheese sauce or any dip you like, for a delicious crunchy snack.",
    "مثالية بجانب الأطباق الجبن المشكلة": "Ideal alongside a cheese board",
    "نوع المنتج:": "Product type:",
    "نوع المنتج: بسكويت مخبوز على شكل سمكة":
        "Product type: baked fish-shaped biscuits",
    "نوع المنتج: بريتزلز": "Product type: pretzels",
    "أين أستمتع بها:": "Where to enjoy them:",
    "أين أستمتع بها: كوجبة خفيفة مثالية للأطفال، مثالية للانش بوكس الأطفال في المدرسة، مثالي وقت السفر او الأجازات":
        "Where to enjoy them: an ideal snack for children, perfect for school lunch boxes, and great for travel and holidays",
    "وصفات/طرق للاستمتاع:": "Recipes and ways to enjoy:",
    "طرق الاستمتاع بها:": "Ways to enjoy them:",
    "مثالية في بوكس المدرسة للأطفال": "Ideal in children's school lunch boxes",
    "يكسر ويرش فوق السلطات لنكهة قرمشة":
        "Break them up and scatter over salads for a crunchy note",
    "لذيذة كوجبة خفيفة سريعة أثناء السفر أو في أيام العمل":
        "Delicious as a quick snack while travelling or on a working day",
    # dates / dried fruit
    "تمر مجدول محشو عين جمل": "Medjool dates stuffed with walnuts",
    "تمر مجدول محشو لوز": "Medjool dates stuffed with almonds",
    "تمر مجدول محشو فستق": "Medjool dates stuffed with pistachios",
    "تمر مجدول محشو كاجو بخار": "Medjool dates stuffed with steamed cashews",
    "تمر مجدول محشو مشمشية \"": "Medjool dates stuffed with apricot paste",
    ":يحتوي بوكس تمور جولد علي": "The Gold dates box contains:",
    "غني بالعناصر الغذائية الأساسية.": "Rich in essential nutrients.",
    "يزيد من الطاقة ويدعم الصحة العامة.": "Lifts energy and supports general health.",
    "كوجبة خفيفة: تناول المشمش مباشرة كوجبة خفيفة صحية.":
        "As a snack: eat the apricots straight, as a healthy snack.",
    "خبر سار لمحبي الكاجو، متعة أكبر مع توفير أكثر لنكهة الكاجو المحمص المفضل لديكم من ابو عوف، استمتعوا ب20% خصم على 275 جم من الكاجو المحمص المملح، فهو يعد إختيار مثالي للتسالي مع مشاهدة أفلامك المفضلة.":
        "Good news for cashew lovers: more pleasure and more savings on your favourite Abu Auf roasted cashews. Enjoy 20% off 275 g of roasted salted cashews — an ideal snack while watching your favourite films.",
    "نكهة البلح:": "Date flavour:",
    "الخيار المثالي صباحًا:": "The ideal morning choice:",
    "كيفية الاستفادة منه:": "How to make the most of it:",
    "تناولها قبل التمرين: مصدر رائع للطاقة قبل ممارسة الرياضة.":
        "Before a workout: a great source of energy before exercise.",
    "تناولها في الوجبات الخفيفة: مثالية لتحسين الوجبات الخفيفة الصحية، ويمكن استخدامها في الحلويات الخفيفة.":
        "As a snack: ideal for improving healthy snacking, and usable in light desserts.",
    "تمور الصحراء بالشوكولاتة واللوز:": "Sahara dates with chocolate and almonds:",
    "فوائد تناول الشوكولاتة:": "The benefits of chocolate:",
    "توفر دفعة سريعة من الطاقة، مما يجعلها خيارًا مثاليًا خلال فترات الانخفاض في النشاط.":
        "They give a quick energy lift, making them ideal during a dip in the day.",
    "كيفية الاستمتاع بتمور الصحراء بالشوكولاتة واللوز:":
        "How to enjoy Sahara dates with chocolate and almonds:",
    "إضافتها إلى حبوب الإفطار أو الزبادي في الصباح لمزيد من اللذة.":
        "Add them to breakfast cereal or yoghurt in the morning for extra pleasure.",
    "تضمينها في وصفات الحلوى للحصول على لمسة فاخرة.":
        "Include them in dessert recipes for a luxurious touch.",
    "تناولها مع فنجان دافئ من الشاي أو القهوة لتجربة لذيذة ومريحة.":
        "Enjoy them with a warm cup of tea or coffee for a delicious, comforting experience.",
    "المميزات:": "Features:",
    "طرق الأستمتاع بالمنتج:": "Ways to enjoy this product:",
    "مثالية مع فنجان من قهوة أبو عوف الدافئة.":
        "Ideal with a warm cup of Abu Auf coffee.",
    "كيفية الاستمتاع بصحارى ديليتس شوكولاته:":
        "How to enjoy Sahara Delights chocolate:",
    "قدمها مع فنجان من قهوة أبو عوف الساخنة للحصول على وجبة لذيذة.":
        "Serve them with a hot cup of Abu Auf coffee for a delicious treat.",
    "أضفها إلى الحلويات للحصول على لمسة إضافية من الحلاوة.":
        "Add them to desserts for extra sweetness.",
    "شاركها مع الأصدقاء والعائلة لجلسة ممتعة.":
        "Share them with friends and family for an enjoyable evening.",
    "تفاصيل المنتج:": "Product details:",
    "أضفه إلى الزبادي أو الفطائر الصباحية لوجبة إفطار غنية بالعناصر الغذائية.":
        "Add it to yoghurt or morning pancakes for a nutrient-rich breakfast.",
    "قم بمزجه مع مجموعة من المكسرات والفواكه المجففة لوجبة خفيفة صحية.":
        "Mix it with a range of nuts and dried fruit for a healthy snack.",
    "استخدمه في الخبز لإضافة الحلاوة الطبيعية والملمس.":
        "Use it in baking to add natural sweetness and texture.",
    "معلومات عن المنتج:": "About this product:",
    "معلومات عن المنتج::": "About this product:",
    "كوجبة خفيفة: استمتع بحفنة من التين المجفف بمفردك لتجربة حلوة ومرضية.":
        "As a snack: enjoy a handful of dried figs on their own for a sweet, satisfying treat.",
    "في الحلويات: اقطع التين وأضفه إلى الكعك، البسكويت، أو الحلويات الكريمية للحلاوة الطبيعية.":
        "In desserts: chop the figs into cakes, biscuits or creamy puddings for natural sweetness.",
    "مزيج فاخر: قدم التين مع الجبن والمكسرات لتجربة مثيرة على الطبق كمقبلات أو حلوى.":
        "A luxurious pairing: serve figs with cheese and nuts for an exciting plate as a starter or dessert.",
    "في الطهي: استخدمها في الخبز والحلويات أو الأطباق المالحة لإضافة الحلاوة.":
        "In cooking: use them in baking, desserts or savoury dishes to add sweetness.",
    "أثناء التنقل: مثالية للأيام المزدحمة أو كوجبة خفيفة في حقيبة الغداء للأطفال":
        "On the go: ideal for busy days or as a snack in children's lunch boxes",
    "لذيذة وصحية: منخفضة الدهون والصوديوم، وغنية بالنكهة.":
        "Delicious and healthy: low in fat and sodium, and full of flavour.",
    "القراصيا بالنواة وجامبو (100 جرام):": "Jumbo prunes with stones (100 g):",
    "لذيذة وصحية:": "Delicious and healthy:",
    "وجبة متعددة الاستخدامات:": "A versatile snack:",
    "جودة عالية:": "High quality:",
    "فوائد صحية:": "Health benefits:",
    "كوجبة خفيفة:": "As a snack:",
    "في الطهي:": "In cooking:",
    "أثناء التنقل:": "On the go:",
    "يتم اختيار كل حبة زبيب بعناية لضمان أقصى درجات النكهة والنضارة.":
        "Every raisin is carefully selected to ensure maximum flavour and freshness.",
    "تجربة فاخرة:": "A premium experience:",
    "وجبة خفيفة في أي مكان:": "A snack for anywhere:",
    "مثالية لجعل وقت الوجبات الخفيفة أكثر رونقًا، سواء في العمل، أو خلال نزهات النهار، أو كإضافة لذيذة إلى علبة الغداء الخاصة بك.":
        "Ideal for making snack time feel special — at work, on a day out, or as a delicious addition to your lunch box.",
    "جودة مضمونة:": "Guaranteed quality:",
    "صُنعت بعناية وخبرة، مضمونة لتقديم أعلى مستويات الجودة والرضا.":
        "Made with care and expertise, guaranteed to deliver the highest quality and satisfaction.",
    "في الطهي: استخدمه في السلطات، الحلويات، أو العصائر الطازجة.":
        "In cooking: use it in salads, desserts or fresh juices.",
    "للخبز: زين الحلويات المخبوزة بحلاوته الطبيعية.":
        "For baking: finish baked desserts with its natural sweetness.",
    # maamoul
    "لمسة عربية أصيلة، قدم المعمول مع فنجان القهوة.":
        "An authentic Arabic touch: serve maamoul with a cup of coffee.",
    "يمكن تقديمة مع البسكويت والكحك والغريبة مثل أجواء الاعياد":
        "It can be served with biscuits, kahk and ghorayeba, just like the holidays.",
    "ضع كمية مناسبة من الآيس كريم بين قطعتين من المعمول لتحصل على مزيج من النكهات الفريدة.":
        "Put a scoop of ice cream between two pieces of maamoul for a uniquely flavoured combination.",
    "2 معمول سادة + 1 معمول قرفة + 1 معمول شوكولاتة":
        "2 plain maamoul + 1 cinnamon maamoul + 1 chocolate maamoul",
    "سادة": "Plain",
    "قرفة": "Cinnamon",
    "مثالي لتقديمه خلال المناسبات الاحتفالية.":
        "Ideal to serve during festive occasions.",
    "استمتع به مع فنجان من الشاي أو القهوة.":
        "Enjoy it with a cup of tea or coffee.",
    "مناسب ل:": "Right for:",
    "عشاق الشوكولاتة والمعمول.": "Lovers of chocolate and maamoul.",
    "الباحثين عن خيار حلوى فريدة.": "Anyone looking for a distinctive sweet.",
    "كيف تستمتع:": "How to enjoy it:",
    "كيف الأستمتاع:": "How to enjoy it:",
    "عرض المعمول يحتوي علي:": "The maamoul offer contains:",
    "قم بمزج قطع المعمول مع كريمة الخفق والفواكه الطازجة للحصول على بار لذيذ للطاقة .":
        "Blend pieces of maamoul with whipped cream and fresh fruit for a delicious energy bar.",
    "شوكولاتة داكنة": "Dark chocolate",
    "مثالي مع كوب دافئ من القهوة أو الشاي":
        "Ideal with a warm cup of coffee or tea",
    "لذيذ كسناكس مغذية شهية في لانش بوكس المدرسة":
        "Delicious as an appetising, nourishing snack in a school lunch box",
    "شهي لتناوله بمفردة": "Appetising on its own",
    "مثالية للتجمعات المنزلية أو النزهات أو كهدية للمناسبات الخاصة":
        "Ideal for gatherings at home, picnics, or as a gift for special occasions",
    "رشها فوق الآيس كريم أو الزبادي لإضافة نكهة لذيذة إلى الحلويات الخاصة بك.":
        "Sprinkle over ice cream or yoghurt to add a delicious note to your desserts.",
    "أستمتع بها بجانب لبن دافئ وأي نوع أخر من المشروبات":
        "Enjoy them alongside warm milk or any other drink",
    "طريقة الأستمتاع :": "How to enjoy:",
    "طرق الأستمتاع": "Ways to enjoy",
    "طرق للأستمتاع:": "Ways to enjoy:",
    "مناسب للانش بوكس المدارس": "Right for school lunch boxes",
    "مناسب لتسالي السفر": "Right as a travel snack",
    # pretzels / offers
    "الباربكيو": "Barbecue",
    "كاتشب": "Ketchup",
    "الجبنة": "Cheese",
    "الشطة الحارة والليمون المنعش": "Hot chilli and fresh lemon",
    "واحد فقط": "One only",
    "3+1 مجانا": "3+1 free",
    "نكهات المتاحة في العرض:": "Flavours available in this offer:",
    "بريتزل ملح البحري - 200 جم": "Sea salt pretzels - 200 g",
    "بوكس صغير": "Small box",
    "بوكس وسط": "Medium box",
    "كلاسيك": "Classic",
    # nuts
    "لوز الأمريكي الخام:": "Raw American almonds:",
    "وجبة خفيفة صحية:": "A healthy snack:",
    "متعدد الاستخدامات:": "Versatile:",
    "المعلومات الإضافية:": "Additional information:",
    "الكاجو الخام المميز:": "Premium raw cashews:",
    "وجبة خفيفة ومغذية:": "A nourishing snack:",
    "مصدر غني بالعناصر الغذائية:": "A rich source of nutrients:",
    "مفيد للحفاظ على الوزن:": "Helpful for weight management:",
    "يمكن استخدامه كجزء من نظام غذائي للحفاظ على الوزن.":
        "It can be used as part of a weight-management diet.",
    "فستق مغطى بالجبن اللذيذ:": "Pistachios in a delicious cheese coating:",
    "وجبة خفيفة صحية ومريحة.": "A healthy, convenient snack.",
    "متوفر في مجموعة متنوعة من أنواع المكسرات.":
        "Available across a wide range of nuts.",
    "الوصفات: أضف هذه الفول السوداني المغطى بالجبن لتعزيز إبداعاتك الطهو بنكهة إضافية.":
        "Recipes: add these cheese-coated peanuts to lift your cooking with extra flavour.",
    "جربه في السلطات، الورقيات، أو كطبق تغطية فريد.":
        "Try them in salads, over greens, or as a distinctive topping.",
    "السهرات: أضف لمسة من الفخامة إلى تجمعاتك الاجتماعية مع وعاء من هذه الفول السوداني المغطى بالجبن اللذيذ كوجبة خفيفة تُسعد الجميع.":
        "Evenings: add a touch of luxury to your gatherings with a bowl of these delicious cheese-coated peanuts — a snack everyone enjoys.",
    "ليالي الأفلام: اجعل ليالي مشاهدة الأفلام ممتعة باستمتاعك بالفول السوداني هذا لتجربة لذيذة ومرضية.":
        "Film nights: make them more enjoyable with these peanuts, for a delicious and satisfying experience.",
    "غني بالعناصر الغذائية، بما في ذلك البروتين والفيتامينات والمعادن والمركبات النباتية.":
        "Rich in nutrients, including protein, vitamins, minerals and plant compounds.",
    "مثالي للاستمتاع بطعم يجمع ما بين نكهة الشوكولاتة الحلوة وقوام السوداني المقرمش.":
        "Ideal for a taste that brings together sweet chocolate and crunchy peanuts.",
    "مثالي لإضافة نكهة مميزة مع الكيك والتورت.":
        "Ideal for adding a distinctive note to cakes and tortes.",
    "مثالي لوضعه في لانش بوكس الأولاد لإضافة نكهة لذيذة ومذاق صحي.":
        "Ideal in children's lunch boxes, for a delicious and healthy taste.",
    "مثالي للاستمتاع به أثناء مشاهدة أفلامك وسهراتك مع من تحب.":
        "Ideal to enjoy while watching films and spending evenings with the people you love.",
    "الكاجو المحمص الفاخر:": "Premium roasted cashews:",
    "غني بالمغذيات وصديق للنظام الغذائي:": "Nutrient rich and diet friendly:",
    "غني بالعناصر الغذائية مثل الدهون الصحية والبروتين.":
        "Rich in nutrients such as healthy fats and protein.",
    "مثالي للأنظمة الغذائية النباتية.": "Ideal for plant-based diets.",
    "اختيار ذكي للتحكم في الوزن.": "A smart choice for weight control.",
    "طرق للاستمتاع بالكاجو المحمص:": "Ways to enjoy roasted cashews:",
    "بمفرده كنوع من التسالي اللذيذة الصحية الخفيفة.":
        "On their own, as a delicious, light and healthy snack.",
    "على أنواع السلطات: أضف قرمشة صحية خفيفة مع أنواع السلطات.":
        "On salads: add a light, healthy crunch to any salad.",
    "متعة الحفلات: يقدم كوجبة خفيفة لذيذة للحفلات، ومثالي لليالي مشاهدة الأفلام.":
        "Party pleasure: serve as a delicious party snack, ideal for film nights.",
    "متعدد الاستخدامات في وصفات لذيذة:": "Versatile in delicious recipes:",
    "أساسي في التشيز بلاتر.": "A staple on a cheese board.",
    "مثالي لجميع المناسبات:": "Ideal for every occasion:",
    "مثالي لجميع السهرات مع الأهل والأصدقاء.":
        "Ideal for every evening with family and friends.",
    "مثالي لتسالي خفيفة وصحية أمام أفلامك المفضلة.":
        "Ideal as a light, healthy snack in front of your favourite films.",
    "نكهة طبيعية لذيذة: ليس فقط لذيذًا بل غنيًا أيضًا بنكهة طبيعية مذهلة.":
        "Delicious natural flavour: not only tasty but rich in a remarkable natural flavour.",
    "تجربة تسالي متميزة: لمسة واحدة مقرمشة وستدرك أن هذه هي فعلاً أفضل تسالي في متناول يدك.":
        "A superior snacking experience: one crunchy bite and you will know this really is the best snack within reach.",
    "مجموعة متنوعة من الخيارات: تقدم مجموعتنا من المكسرات تشكيلة واسعة تناسب جميع الأذواق الرفيعة.":
        "A wide choice: our range of nuts offers a broad selection to suit every refined taste.",
    "سموذي لذيذ باللوز: امزج لوزنا المملح الفاخر مع زبادي يوناني وعسل وموز للحصول على سموذي لذيذ ومغذي.":
        "A delicious almond smoothie: blend our premium salted almonds with Greek yoghurt, honey and banana for a delicious, nourishing smoothie.",
    "قرمشة لوزية في السلطة: أضف قرمشة اللوز المملح إلى سلطتك لإضافة نكهة وملمس إضافيين.":
        "Almond crunch in a salad: add salted almonds to your salad for extra flavour and texture.",
    "تسالي ليلة الأفلام: خذ حفنة من هذه اللوز لتستمتع بها أثناء مشاهدة أفلامك المفضلة أو برامجك التلفزيونية.":
        "Film-night snacking: take a handful of these almonds to enjoy while watching your favourite films or shows.",
    "جذابة في الحفلات: قدمها في التجمعات والحفلات كوجبة خفيفة صحية ولذيذة سيستمتع بها الجمي":
        "A hit at parties: serve them at gatherings as a healthy, delicious snack everyone will enjoy",
    "مع المأكولات المتعددة: يعزز أطباق السلطات والشوفان والعديد من الأطباق الأخرى.":
        "With many foods: it lifts salads, oats and many other dishes.",
    "مثالي مع المخبوزات: يمكن استخدامه في تحضير المخبوزات لإضافة نكهة مميزة.":
        "Ideal in baking: it can be used in baking to add a distinctive flavour.",
    "كيفية الاستمتاع بعين الجمل أكثر:": "How to enjoy walnuts even more:",
    "مع المأكولات المتعددة:": "With many foods:",
    "مثالي مع المخبوزات:": "Ideal in baking:",
    "مثالي لسناكس وسط اليوم:": "Ideal as a midday snack:",
    "مناسب للسهرات وتجمعات الأهل والأصحاب:":
        "Right for evenings and gatherings with family and friends:",
    "يحلى مشاهدة الأفلام والمسرحيات:":
        "It sweetens film and theatre nights:",
    "قم بإقرانها بالفواكه الطازجة أو الخضار للحصول على وجبة خفيفة كاملة ومتوازنة.":
        "Pair them with fresh fruit or vegetables for a complete, balanced snack.",
    # popcorn
    "استمتعوا بفشار ابو عوف بالكراميل الجاهز للأكل مباشرة في اي مكان وفي اي وقت:":
        "Enjoy Abu Auf caramel popcorn, ready to eat straight away, anywhere and any time:",
    "وجبة خفيفة للسهرة:": "An evening snack:",
    "حلوى للحفلات:": "A party sweet:",
    "فكرة هدية:": "A gift idea:",
    "لعشاق الفشار": "For popcorn lovers",
    "عوف:": "Auf:",
    "اختيار لذيذ لسهرات الأصدقاء وتجمعات الأهل.":
        "A delicious choice for evenings with friends and family gatherings.",
    "حلوى لذيذة خلال مشاهدة المباريات أو الأفلام، فشار غني بنكهة الكراميل مع الشوكولاتة اللذيذة.":
        "A delicious treat while watching matches or films — popcorn rich with caramel and delicious chocolate.",
    "كيفية الاستمتاع بها:": "How to enjoy it:",
    "مثالية مع مشاهدة الأفلام والمسرحيات أو المباريات لتسالي خفيفة وصحية.":
        "Ideal with films, theatre or matches, as a light and healthy snack.",
    "لذيذة كوجبة خفيفة في أيام العمل المزدحمة.":
        "Delicious as a snack on busy working days.",
    # coffee
    "معلومات عن النكهة:": "About the flavour:",
    "تفاصيل عن النكهة:": "Flavour details:",
    "نوع حبوب البن:": "Bean type:",
    "طريقة الاستمتاع بالقهوة:": "How to enjoy this coffee:",
    "استمتع بالقهوة في صباح هادئ في المنزل أو خلال العمل إذا كان يومك طويل ومزدحم.":
        "Enjoy it on a quiet morning at home, or at work if your day is long and busy.",
    "فوائد لفقدان الوزن:": "Weight-loss benefits:",
    "يمكن أن تدعم القهوة الفاتحة عملية إدارة الوزن من خلال توفير زيادة خفيفة في الكافيين دون مرارة القهوة الغامقة.":
        "Light-roast coffee can support weight management by giving a mild caffeine lift without the bitterness of a dark roast.",
    "يمكن أن تساعدك في البقاء مستيقظًا ومشبعًا دون الحاجة إلى سعرات حرارية إضافية.":
        "It can help you stay alert and satisfied without extra calories.",
    "تمتع بتناول القهوة هذه في الصباح أثناء قراءة الصحف.":
        "Enjoy this coffee in the morning while reading the papers.",
    "استمتع بتناولها خلال الأيام المشغولة والعملية.":
        "Enjoy it through busy working days.",
    "تمتع بشرب القهوة وأنت تجتمع مع العائلة أو الأصدقاء.":
        "Enjoy it while catching up with family or friends.",
    "استمتع في أي وقت:": "Enjoy it any time:",
    "تجربة قهوة تركية أصلية.": "An authentic Turkish coffee experience.",
    "مثالي للتجمعات التقليدية ولحظات الاسترخاء":
        "Ideal for traditional gatherings and moments of calm",
    "تركية": "Turkish",
    "بن برازيلي": "Brazilian coffee",
    "بن برازيلي محوج وسط": "Medium-spiced Brazilian coffee",
    "المشروبات: يتم الاستمتاع بها كمشروب ساخن أو بارد، مع إضافة الحليب أو السكر أو المنكهات علي حسب الرغبة":
        "Drinks: enjoy it hot or cold, with milk, sugar or flavourings to taste",
    "طعم القهوة:": "Coffee taste:",
    "استخدام القهوة:": "Coffee use:",
    "الطبخ": "Cooking",
    # salt / protein bars / seeds
    "نوع الملح:": "Salt type:",
    "يعتبر بديل صحيا للملح العادي لمتبعي الدايت او محبي المأكولات الصحية":
        "A healthy alternative to ordinary salt for dieters and anyone who loves healthy food",
    "غني بالمواد المغذية: يحتوي على العناصر الغذائية الأساسية للرياضيين ومتبعي الحميات.":
        "Nutrient rich: contains the essential nutrients athletes and dieters need.",
    "قوة البروتين: يوفر جرعة صحية من البروتين لزيادة الطاقة.":
        "Protein power: delivers a healthy dose of protein for more energy.",
    "وجبة خفيفة مثالية: مناسبة للأشخاص الذين يعيشون حياة مزدحمة.":
        "The ideal snack: right for people with busy lives.",
    "توازن في النكهة: يحقق توازنًا مثاليًا بين نكهة القهوة والشوكولاتة.":
        "Balanced flavour: strikes a perfect balance between coffee and chocolate.",
    "مناسب لمن هذا البار:": "Who this bar is for:",
    "الرياضيين وعشاق اللياقة البدنية.": "Athletes and fitness enthusiasts.",
    "أي شخص يتبع حمية غذائية محددة.": "Anyone following a specific diet.",
    "الأفراد الذين يبحثون عن وجبة خفيفة غنية بالعناصر الغذائية.":
        "People looking for a nutrient-rich snack.",
    "وصف المنتج:": "Product description:",
    "فوائد بروتين بار البندق:": "The benefits of the hazelnut protein bar:",
    "غني بأحماض أوميغا 3 الدهنية التي تفيد صحة القلب":
        "Rich in omega-3 fatty acids, which benefit heart health",
    "من يمكنه الاستمتاع بهذا البار:": "Who can enjoy this bar:",
    "ينصح به للأشخاص الذين يتبعون نمط حياة نشطًا يمارسون الرياضة بانتظام.":
        "Recommended for people with an active lifestyle who exercise regularly.",
    "مناسب لأولئك الذين يبحثون عن بديل صحي للوجبات الخفيفة التقليدية.":
        "Right for anyone looking for a healthy alternative to conventional snacks.",
    "كيفية الاستفادة من حبوب الشوفان:": "How to make the most of oats:",
    "مناسب لمن:": "Right for:",
    "الباحثين عن وجبة فطور صحية تدعم صحة القلب.":
        "Anyone looking for a healthy breakfast that supports heart health.",
    "متبعي الدايت ونظم غذائية محددة": "Dieters and people on specific eating plans",
    "مناسب للأفراد التالية لهم:": "Right for the following people:",
    "كيفية تناول حبوب بذر الكتان:": "How to eat flaxseed:",
    "رشها فوق السلطات أو الزبادي": "Sprinkle over salads or yoghurt",
    "امزجها مع دقيق الشوفان أو الحبوب": "Mix with oatmeal or cereal",
    "استخدمها في وصفات الخبز لإضافة نكهة وقيمة غذائية.":
        "Use it in baking recipes to add flavour and nutrition.",
    "طرق الاستخدام:": "Ways to use it:",
    "يمكن إضافة بذور الشيا إلى العصائر الصباحية لزيادة القيمة الغذائية.":
        "Chia seeds can be added to morning smoothies to boost their nutrition.",
    "يمكن رشها فوق السلطات لإضافة نكهة وقوام مميز.":
        "They can be sprinkled over salads to add flavour and a distinctive texture.",
    "يمكن استخدامها في وصفات الخبز والمعجنات لإضافة قوام وفوائد غذائية.":
        "They can be used in bread and pastry recipes to add texture and nutrition.",
    "يمكن إعداد بودنج الشيا عن طريق مزجها مع حليب ومكملات غذائية وتناولها كوجبة صحية ولذيذة.":
        "Chia pudding can be made by mixing them with milk and supplements, for a healthy, delicious meal.",
    "غني بالمواد الغذائية: يحتوي لب القرع المقشر على مجموعة غنية من الفيتامينات والمعادن والدهون الصحية.":
        "Nutrient rich: peeled pumpkin seeds contain a rich range of vitamins, minerals and healthy fats.",
    "داعم لصحة القلب: نظرًا لاحتوائه على نسبة عالية من المغنيسيوم، قد يكون داعمًا لصحة القلب.":
        "Supports heart health: with its high magnesium content, it may support the heart.",
    "دعم للجهاز المناعي: يحتوي على مضادات الأكسدة التي قد تدعم الجهاز المناعي.":
        "Immune support: contains antioxidants that may support the immune system.",
    "مناسب للجلوتين: يمكن تناوله بسهولة من قبل الأشخاص الذين يعانون من حساسية الجلوتين.":
        "Gluten friendly: easily eaten by people with a gluten intolerance.",
    "الأماكن المناسبة لتناوله:": "Where to enjoy it:",
    "كوجبة خفيفة صحية: استمتع به في أي وقت وفي أي مكان كوجبة خفيفة شهية مثل اثناء سهرات الاصحاب والاهل، اثناء السفر أو بين العمل كسناكس صحية لذيذة":
        "As a healthy snack: enjoy it any time and anywhere as an appetising snack — during evenings with friends and family, while travelling, or between tasks at work",
    "وزن المنتج:": "Product weight:",
    "ما يميز هذا المنتج:": "What sets this product apart:",
    "كيفية استخدام هذا المنتج:": "How to use this product:",
    "افرده على الخبز أو السندويشات..": "Spread it on bread or sandwiches.",
    "استخدمه في تحضير صلصات السلطات أو الصلصات.":
        "Use it to make salad dressings or sauces.",
    "ضيفة في الحلويات او المخبوزات الحلوة .":
        "Add it to desserts or sweet baking.",
    "كيفية الاستمتاع بتناولها:": "How to enjoy them:",
    "3 عبوات من زبدة الفول السوداني النقية.": "3 jars of pure peanut butter.",
    "يدعم إدارة الوزن: منخفض السعرات الحرارية وغني بالألياف، مما يساعد على الشعور بالشبع لفترة أطول.":
        "Supports weight management: low in calories and rich in fibre, helping you feel full for longer.",
    "مثالي للتسالي: خيار لذيذ ومشبع للتسالي.":
        "Ideal for snacking: a delicious, filling choice.",
    "طبيعي ونقي: يوفر طعماً فلفلياً أصلياً دون إضافات":
        "Natural and pure: delivers an authentic peppery taste with no additives",
    "فوائد صحية: غني بمضادات الأكسدة التي تساهم في الصحة العامة":
        "Health benefits: rich in antioxidants that contribute to general health",
    "قوة مضادة للأكسدة: يساعد في حماية الجسم من الإجهاد التأكسدي":
        "Antioxidant power: helps protect the body from oxidative stress",
    "مثالي للطهي: مثالي للكاري والحساء والتتبيلات":
        "Ideal for cooking: perfect for curries, soups and marinades",
    "اختيار صحي: مثالية كوجبة خفيفة مقرمشة دون الشعور بالذنب.":
        "A healthy choice: ideal as a crunchy snack with no guilt.",
    "مكونات عالية الجودة: مصنوع من شوكولاتة وبندق ممتاز.":
        "High-quality ingredients: made with excellent chocolate and hazelnuts.",
    "إشباع لذيذ: مثالي لاستراحة حلوة ومليئة بالمكسرات.":
        "Deliciously filling: ideal for a sweet, nutty break.",
    "مكونات عالية الجودة: مصنوع من بريتزل ولوز ممتاز.":
        "High-quality ingredients: made with excellent pretzels and almonds.",
    "تعزيز الطاقة: مثالي كوجبة خفيفة سريعة ومشبعة":
        "An energy lift: ideal as a quick, filling snack",
    "سهل التحضير: سهل وسريع التحضير في المنزل.":
        "Easy to prepare: quick and simple to make at home.",
    "مثالي لأي مناسبة: مناسب لأمسيات الأفلام، الحفلات، أو كوجبة خفيفة سريعة.":
        "Ideal for any occasion: right for film nights, parties, or a quick snack.",
    # weights
    "الوزن": "Weight",
    "الوزن :": "Weight:",
    "الوزن: 90 جرام": "Weight: 90 g",
    "25 جم": "25 g",
    "40 جم": "40 g",
    "45 جرام": "45 g",
    "50جرام": "50 g",
    "60 جرام": "60 g",
    "65 جرام": "65 g",
    "65جرام": "65 g",
    "80 جرام": "80 g",
    "85 جرام": "85 g",
    "100 جرام.": "100 g.",
    "200 جرام": "200 g",
    "330 جرام": "330 g",
    "400 جم": "400 g",
}

# --------------------------------------------------------------------------
# TPL2 — the remaining templates (mostly client benefit lists).
# --------------------------------------------------------------------------
TPL2 = {
    "{0}{1} د": "{0}{1} d",
    "{0} 3 بريتزل بسعر اقل {1} {2}": "{0} 3 pretzels for less {1} {2}",
    "نسبة العرض: {0} {1} {2} {3} {4} {5}": "Offer: {0} {1} {2} {3} {4} {5}",
    "{0} يعزز أطباق السلطات والشوفان والعديد من الأطباق الأخرى.":
        "{0} It lifts salads, oats and many other dishes.",
    "{0} يمكن استخدامه في تحضير المخبوزات لإضافة نكهة مميزة.":
        "{0} It can be used in baking to add a distinctive flavour.",
    "{0} يُعتبر خيارًا مثاليًا لتناول سناك خفيف وصحي وملئ بالطاقة.":
        "{0} An ideal choice for a light, healthy and energising snack.",
    "{0} مثالي لتقديمه في السهرات والتجمعات كسناك خفيف.":
        "{0} Ideal to serve at evenings and gatherings as a light snack.",
    "{0} يعد سناكس خفيفًا ومقرمشًا يعزز تجربة مشاهدة الأفلام والمسرحيات.":
        "{0} A light, crunchy snack that improves any film or theatre night.",
    "{0} منخفضة الدهون والصوديوم، وغنية بالنكهة.":
        "{0} Low in fat and sodium, and full of flavour.",
    "{0} مناسبة للكبار والأطفال في أي وقت وفي أي مكان.":
        "{0} Right for adults and children, any time and anywhere.",
    "{0} مصنوعة من مكونات عالية الجودة لطعم لذيذ.":
        "{0} Made with high-quality ingredients for a delicious taste.",
    "{0} تزيد من الطاقة، وتساعد في الهضم، وتدعم الصحة العامة.":
        "{0} They lift your energy, aid digestion and support general health.",
    "{0} استمتع بحفنة كوجبة خفيفة ومشبعة.":
        "{0} Enjoy a handful as a filling snack.",
    "{0} استخدمها في الخبز والحلويات أو الأطباق المالحة لإضافة الحلاوة.":
        "{0} Use them in baking and desserts, or in savoury dishes to add sweetness.",
    "{0} مثالية للأيام المزدحمة أو كوجبة خفيفة في حقيبة الغداء للأطفال.":
        "{0} Ideal for busy days or as a snack in children's lunch boxes.",
    "إيه مميزات الزبيب المصري الفاخر: {0}":
        "What makes premium Egyptian raisins special: {0}",
    "لذة فائقة: {0} نكهات رفيعة: {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}":
        "Exceptional taste: {0} Refined flavours: {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}",
    "مميزات المنتج: {0} {1} {2} {3} {4} {5} {6} {7}":
        "Product features: {0} {1} {2} {3} {4} {5} {6} {7}",
    "مميزات المنتج: {0} {1} {2} {3} {4} جمبري، مسحوق الثوم، زبدة، ليمون. {5} قلي الجمبري في زبدة الثوم، عصير الليمون، اتركه حتى يصبح لون الجمبري وردي. {6} {7} {8}":
        "Product features: {0} {1} {2} {3} {4} Prawns, garlic powder, butter, lemon. {5} Fry the prawns in garlic butter and lemon juice until they turn pink. {6} {7} {8}",
    "استخدام متعدد الاستخدامات: {0}": "Versatile use: {0}",
    "جمبري، مسحوق الثوم، زبدة، ليمون. {0}":
        "Prawns, garlic powder, butter, lemon. {0}",
    "كيفية الاستخدام: {0}": "How to use: {0}",
    "طرق الأستمتاع بمعمول أبوعوف: {0} وصفات: ساندويتش الآيس كريم بالمعمول: {1} بارالمعمول: {2}":
        "Ways to enjoy Abu Auf maamoul: {0} Recipes: maamoul ice-cream sandwich: {1} Maamoul bar: {2}",
    "العرض: {0} النكهات المتاحة في العرض: {1} طرق الأستمتاع: {2}":
        "The offer: {0} Flavours available: {1} Ways to enjoy: {2}",
    "مقرمشات بنكهة: {0} يكفي كم شخص: {1}":
        "Crackers flavoured with: {0} Serves: {1}",
    "{0} ١ سادة ١ قرفة ١ شوكولاتة ١ فراولة":
        "{0} 1 plain, 1 cinnamon, 1 chocolate, 1 strawberry",
    "{0}: يستخدم في وصفات الحلويات مثل التيراميسو، الكيك وغيرهم من المخبوزات الحلوة":
        "{0}: used in dessert recipes such as tiramisu, cake and other sweet bakes",
    "{0} بسكويت مخبوز على شكل سمكة": "{0} baked fish-shaped biscuits",
    "{0}: رائحة البيتزا الغنية مع القرمشة في كل قضمة":
        "{0}: a rich pizza aroma with a crunch in every bite",
    "{0} كوجبة خفيفة مثالية للأطفال، مثالية للانش بوكس الأطفال في المدرسة، مثالي وقت السفر او الأجازات":
        "{0} an ideal snack for children, perfect for school lunch boxes, and great for travel and holidays",
    "{0} رائعة كوجبة خفيفة مستقلة أو مع الجبن و المكسرات في التيشز بلاتر، او مكسر فوق السلطات":
        "{0} great on their own, with cheese and nuts on a cheese board, or crushed over salads",
    "{0} بريتزلز": "{0} pretzels",
    "{0}: جبنة": "{0}: cheese",
    "حجم البرطمان : {0} نكهة القهوة: {1}": "Jar size: {0} Coffee flavour: {1}",
    "حجم المنتج: {0}": "Product size: {0}",
    "صحي ومفيد للطاقة: {0} كيفية الاستمتاع: {1}":
        "Healthy and energising: {0} How to enjoy: {1}",
    "طرق الاستمتاع بفشار أبو {0} {1}": "Ways to enjoy Abu {0} popcorn {1}",
    "نوع القهوة: {0} الوزن: {1} النكهة: {2} أماكن الاستمتاع المثالية: {3}":
        "Coffee type: {0} Weight: {1} Flavour: {2} Best enjoyed: {3}",
    "{0} 100 جم {1} {2} {3} مثالي للاستمتاع به خلال أثناء مشاهدة الأفلام {4} قدمي كراميل الفشار كحلوى لذيذة في الاحتفالات والتجمعات. {5} ضعي كراميل الفشار في أكياس جميلة كهدية حلوة ومُفكرة.\" {6} حيث تجربه الفشار بالكراميل تعد من التجارب اللذيذة الغير تقليدية التي تجمع بين حلاوة الكراميل وقرمشة الفشار جميع الأعمار لانه مغذي":
        "{0} 100 g {1} {2} {3} Ideal to enjoy while watching films {4} Serve caramel popcorn as a delicious treat at celebrations and gatherings. {5} Put caramel popcorn in pretty bags as a sweet, thoughtful gift. {6} Caramel popcorn is one of those deliciously unconventional treats, bringing together the sweetness of caramel and the crunch of popcorn, for all ages, because it is nourishing",
}


def _catalog_names():
    """Product names, from the client's own English `name` field.

    Covers the card titles, the product page h1, cart and drawer lines, the
    bundle rows, and every `alt` that repeats the name — which is why this is
    worth more than its 99 entries suggest.
    """
    path = os.path.join(EXPORT, "data", "catalog.json")
    with open(path, encoding="utf-8") as f:
        cat = json.load(f)
    out = {}
    for p in cat["products"]:
        ar, en = (p.get("nameAr") or "").strip(), (p.get("name") or "").strip()
        if ar and en:
            out[ar] = en
        for s in p.get("sizes") or []:
            sar, sen = (s.get("nameAr") or "").strip(), (s.get("name") or "").strip()
            if sar and sen:
                out[sar] = sen
    return out


def _generated():
    """Formulaic families — looped rather than listed.

    GALLERY is 40 entries on its own (every thumbnail on every gallery length),
    and the governorate rows are a name plus a count. Writing these by hand
    would be forty chances to typo a number.
    """
    out = {}
    # gallery thumbnail labels: "عرض الصورة 3 من 7"
    for total in range(1, 13):
        for i in range(1, total + 1):
            out["عرض الصورة %d من %d" % (i, total)] = "View image %d of %d" % (i, total)

    # The mega-menu and footer build these by CONCATENATION in scripts.js
    # ("تسوق كل " + name), so the string that reaches the DOM is not a literal
    # anywhere and cannot be keyed by hand without guessing. Generated from
    # the same category list the nav uses, so adding a category cannot leave a
    # link stranded in Arabic — the exact failure mode the concatenation trap
    # in CLAUDE.md describes for Tailwind classes, in a different register.
    for ar, en in NAV_CATEGORIES.items():
        out["تسوق كل " + ar] = "Shop all " + en
        out["جميع " + ar] = "All " + en
    return out


NAV_CATEGORIES = {
    "العروض و الخصومات": "Offers & Discounts",
    "المكسرات": "Nuts",
    "القهوة": "Coffee",
    "التمور والفواكه المجففة": "Dates & Dried Fruits",
    "الوجبات صحية": "Healthy Snacks",
    "المشروبات": "Beverages",
    "البهارات والزيوت": "Spices & Oils",
    "الهدايا": "Gifting",
}


GOVERNORATES = {
    "القاهرة": "Cairo", "الجيزة": "Giza", "الجيزه": "Giza",
    "الإسكندرية": "Alexandria", "الاسكندريه": "Alexandria",
    "البحر الأحمر": "Red Sea", "البحر الاحمر": "Red Sea",
    "القليوبية": "Qalyubia", "القليوبيه": "Qalyubia",
    "الدقهلية": "Dakahlia", "الدقهليه": "Dakahlia",
    "الغربية": "Gharbia", "الغربيه": "Gharbia",
    "الشرقية": "Sharqia", "الشرقيه": "Sharqia",
    "المنوفية": "Monufia", "المنوفيه": "Monufia",
    "البحيرة": "Beheira", "البحيره": "Beheira",
    "بورسعيد": "Port Said", "السويس": "Suez", "دمياط": "Damietta",
    "المنيا": "Minya", "أسيوط": "Asyut", "اسيوط": "Asyut",
    "أسوان": "Aswan", "اسوان": "Aswan",
    "جنوب سيناء": "South Sinai", "شمال سيناء": "North Sinai",
    "الفيوم": "Fayoum", "كفر الشيخ": "Kafr El Sheikh",
    "الغردقة": "Hurghada", "طنطا": "Tanta",
    "الأقصر": "Luxor", "الاقصر": "Luxor",
    "الاسماعليه": "Ismailia", "بني سويف": "Beni Suef",
    "سوهاج": "Sohag", "قنا": "Qena",
    "الوادي الجديد": "New Valley", "مرسي مطروح": "Marsa Matrouh",
    "دبي": "Dubai", "الشارقة": "Sharjah", "ديرا": "Deira",
}

# Cairo districts used by the delivery-area sheet and the branches list.
DISTRICTS = {
    "15 من مايو": "15th of May City", "العباسيه": "Abbassia",
    "عين شمس الشرقيه": "East Ain Shams", "عين شمس الغربيه": "West Ain Shams",
    "الظاهر": "El Zaher", "المطريه": "Matareya", "الرحاب": "Al Rehab",
    "الحلميه الجديده": "New Helmeya", "وسط البلد": "Downtown",
    "الشروق": "El Shorouk", "النزهه الجديده": "New Nozha",
    "جاردن سيتي": "Garden City", "حدائق القبه": "Hadayek El Kobba",
    "هليوبوليس": "Heliopolis", "حلوان": "Helwan", "القطاميه": "Katameya",
    "المعادي": "Maadi", "المعادي الجديده": "New Maadi", "مدينتي": "Madinaty",
    "المنيل": "Manial", "المقطم": "Mokattam", "مدينه نصر": "Nasr City",
    "شيراتون": "Sheraton", "شبرا": "Shubra",
    "التجمع الاول": "First Settlement", "التجمع الثالث": "Third Settlement",
    "التجمع الخامس": "Fifth Settlement",
    "زهراء المعادي": "Zahraa El Maadi", "زهراء مدينه نصر": "Zahraa Nasr City",
    "الزمالك": "Zamalek", "الزيتون": "Zeitoun",
}


def build_dictionary():
    text = {}
    text.update(_generated())
    text.update(GOVERNORATES)
    text.update(DISTRICTS)
    text.update(_catalog_names())
    text.update(COPY)
    text.update(COPY2)
    text.update(CHROME)
    text.update(UI)  # our own UI wins any collision with scraped copy

    tpl = dict(TPL)
    tpl.update(TPL2)
    # "<governorate> {0}" rows on the branches page
    for ar, en in GOVERNORATES.items():
        tpl.setdefault(ar + " {0}", en + " {0}")
    return text, tpl


def write(dest=None):
    text, tpl = build_dictionary()
    dest = dest or os.path.join(EXPORT, "i18n-en.js")
    payload = json.dumps({"text": text, "tpl": tpl}, ensure_ascii=False,
                         sort_keys=True, separators=(",", ":"))
    banner = (
        "/* GENERATED by build/i18n.py - do not edit.\n"
        "   %d text entries, %d templates.\n"
        "   English is in-house and awaits client sign-off (DESIGN-NOTES). */\n"
    ) % (len(text), len(tpl))
    with open(dest, "w", encoding="utf-8") as f:
        f.write(banner + "window.ABUAUF_I18N=" + payload + ";\n")
    return len(text), len(tpl), os.path.getsize(dest)


if __name__ == "__main__":
    n, m, size = write()
    print("i18n-en.js: %d text, %d templates, %s bytes" % (n, m, format(size, ",")))
