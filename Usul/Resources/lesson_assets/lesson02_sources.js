window.LESSON_LABELS = {
  content_kind: { verbatim: "نص حرفي", summary: "تلخيص أمين", analysis: "تحليل تحريري", teacher_note: "تقرير الأستاذ" },
  verification: { exact_text_match: "مطابق للنص الرقمي", visually_verified_scan: "مقابل بصرياً على النسخة المصورة", pending: "بانتظار التحقيق" }
};
window.LESSON_SOURCE_ORDER = [
  "l02_mujaz_division", "l02_mujaz_wad", "l02_mujaz_four",
  "l02_fadhli_text", "l02_mutahhari_types", "l02_sadr_first",
  "l02_sadr_second", "l02_muzaffar_four", "l02_murtada_use",
  "l02_akhund_wad", "l02_khoei_commitment", "l02_sistani_stages"
];
window.LESSON_SOURCES = {
  l02_mujaz_division: {
    source_id: "l02_mujaz_division", layer: "core", book: "الموجز في أصول الفقه", author: "الشيخ جعفر السبحاني",
    edition: "الطبعة الرابعة عشرة، مؤسسة الإمام الصادق، 1429هـ", volume: "1", printed_page: "ص 10",
    scan_or_database_page: "قاعدة النص: 10", content_kind: "verbatim", verification: "exact_text_match",
    context: "الأقسام الأربعة بحسب وظيفة البحث الأصولي.",
    text: "تنقسم المباحث الأصولية إلى أربعة أنواع :\nالأوّل : المباحث اللفظية ويقع البحث فيها عن مداليل الألفاظ وظواهرها التي تقع في طريق الاستنباط نظير ظهور صيغة الأمر في الوجوب .\nالثاني : المباحث العقلية ويقع البحث فيها عن الأحكام العقلية الكلية التي تقع في طريق الاستنباط نظير البحث عن وجود الملازمة بين وجوب الشيء ووجوب مقدمته .\nالثالث : مباحث الحجج والأمارات كالبحث عن حجّية خبر الواحد .\nالرابع : مباحث الأصول العملية ، وهي تبحث عن مرجع المجتهد عند فقد الدليل على الحكم الشرعي .",
    file: "../Resources/books_data/mujaz_subhani.json"
  },
  l02_mujaz_wad: {
    source_id: "l02_mujaz_wad", layer: "core", book: "الموجز في أصول الفقه", author: "الشيخ جعفر السبحاني",
    edition: "الطبعة الرابعة عشرة، مؤسسة الإمام الصادق، 1429هـ", volume: "1", printed_page: "ص 10–11",
    scan_or_database_page: "قاعدة النص: 10–11", content_kind: "verbatim", verification: "exact_text_match",
    context: "التعريف الأول للوضع والثاني الأوسع منه.",
    text: "جعل اللفظ في مقابل المعنى وتعيينه للدلالة عليه .\nوربما يعرّف : انّه نحو اختصاص للّفظ بالمعنى وارتباط خاص بينهما ناشئ من تخصيصه به تارة ، ويسمّى بالوضع التعييني ، وكثرة استعماله فيه أخرى ويسمّى بالوضع التعيّني .",
    file: "../Resources/books_data/mujaz_subhani.json"
  },
  l02_mujaz_four: {
    source_id: "l02_mujaz_four", layer: "core", book: "الموجز في أصول الفقه", author: "الشيخ جعفر السبحاني",
    edition: "الطبعة الرابعة عشرة، مؤسسة الإمام الصادق، 1429هـ", volume: "1", printed_page: "ص 11–12",
    scan_or_database_page: "قاعدة النص: 11–12", content_kind: "verbatim", verification: "exact_text_match",
    context: "ميزان العموم والخصوص وحجة امتناع القسم الرابع.",
    text: "ثمّ إنّ الميزان في كون الوضع خاصّا أو عامّا هو كون المعنى الملحوظ حين الوضع جزئيا أو كلّيا .",
    file: "../Resources/books_data/mujaz_subhani.json"
  },
  l02_fadhli_text: {
    source_id: "l02_fadhli_text", layer: "core", book: "مبادئ أصول الفقه", author: "العلامة عبد الهادي الفضلي",
    edition: "مركز الغدير للدراسات والنشر والتوزيع؛ النسخة المصورة المحلية", volume: "1", printed_page: "ص 40",
    scan_or_database_page: "PDF ص 42", content_kind: "verbatim", verification: "visually_verified_scan",
    context: "التمييز بين ثبوت متن الدليل وفهم دلالته؛ تأطير للبحث اللغوي.",
    text: "دراسة المتن تتنوع في علوم التشريع الإسلامي إلى نوعين -أيضاً- هما: تحقيق المتن، ودلالة المتن.",
    file: "../مبادئ أصول الفقه - العلامة عبدالهادي الفضلي.pdf", pdf_page: 42
  },
  l02_mutahhari_types: {
    source_id: "l02_mutahhari_types", layer: "core", book: "الأصول", author: "الشهيد مرتضى مطهري",
    edition: "ترجمة حسن علي الهاشمي، دار الولاء، الطبعة الأولى، 2009/1430", volume: "1", printed_page: "ص 37–38",
    scan_or_database_page: "PDF ص 37–38", content_kind: "verbatim", verification: "visually_verified_scan",
    context: "التمييز بين قواعد الاستنباط والقواعد المستخدمة عند العجز عنه.",
    text: "الأول: قواعد الاستنباط الصحيح للأحكام الشرعية الواقعية من مصادرها.\nالثاني: قواعد الاستخدام الصحيح لمجموعة من القواعد العلمية في صورة العجز عن الاستنباط.",
    file: "../الأصول - الشهيد الشيخ مرتضى مطهري.pdf", pdf_page: 37
  },
  l02_sadr_first: {
    source_id: "l02_sadr_first", layer: "core", book: "دروس في علم الأصول، الحلقة الأولى", author: "الشهيد السيد محمد باقر الصدر",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "الحلقة الأولى", printed_page: "ص 68",
    scan_or_database_page: "قاعدة النص: 68", content_kind: "verbatim", verification: "exact_text_match",
    context: "الوضع بوصفه تقريناً بين تصور اللفظ وتصور المعنى.",
    text: "فالوضع هو عملية تقرن بها لفظا بمعنى نتيجتها أن يقفز الذهن إلى المعنى عند تصور اللفظ دائما .",
    file: "../Resources/books_data/sadr_halaqat_1.json"
  },
  l02_sadr_second: {
    source_id: "l02_sadr_second", layer: "core", book: "دروس في علم الأصول، الحلقة الثانية", author: "الشهيد السيد محمد باقر الصدر",
    edition: "نسخة قاعدة النص المحلية؛ ترقيمها مختلف عن PDF المصور", volume: "الحلقة الثانية", printed_page: "ص 186 في نسخة النص",
    scan_or_database_page: "قاعدة النص: 186", content_kind: "verbatim", verification: "exact_text_match",
    context: "القرن الأكيد وصلته بالدلالة التصورية والتعيّن بكثرة الاستعمال.",
    text: "ومن هنا نعرف أن الوضع ليس سببا إلا للدلالة التصورية ، وأما الدلالتان التصديقيتان الأولى والثانية ، فمنشأهما الظهور الحالي والسياقي للكلام لا الوضع .",
    file: "../Resources/books_data/sadr_halaqat_1.json"
  },
  l02_muzaffar_four: {
    source_id: "l02_muzaffar_four", layer: "core", book: "أصول الفقه", author: "الشيخ محمد رضا المظفر",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "ج 1", printed_page: "ص 56",
    scan_or_database_page: "قاعدة النص: 56", content_kind: "verbatim", verification: "exact_text_match",
    context: "التمييز بين إمكان الأقسام ووقوع الثالث في الحروف على رأيه.",
    text: "لا نزاع في إمكان الأقسام الثلاثة الأولى ، كما لا نزاع في وقوع القسمين الأولين .",
    file: "../Resources/books_data/usul_muzaffar_1.json"
  },
  l02_murtada_use: {
    source_id: "l02_murtada_use", layer: "advanced", book: "الذريعة إلى أصول الشريعة", author: "السيد المرتضى",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "ج 1", printed_page: "ص 60–61",
    scan_or_database_page: "قاعدة النص: 60–61", content_kind: "verbatim", verification: "exact_text_match",
    context: "التفريق المبكر بين الكلام والخطاب والمستعمل والمهمل.",
    text: "ولهذا جاز أن يتكلّم النّائم ، ولم يجز أن يخاطب ، كما لم يجز أن يأمر وينهى .",
    file: "../Resources/books_data/murtada_dhariyah_1.json"
  },
  l02_akhund_wad: {
    source_id: "l02_akhund_wad", layer: "advanced", book: "كفاية الأصول", author: "الآخوند محمد كاظم الخراساني",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "1", printed_page: "ص 9–10",
    scan_or_database_page: "قاعدة النص: 9–10", content_kind: "verbatim", verification: "exact_text_match",
    context: "الاختصاص وأصل تقسيم الوضع؛ وقوعه في الحروف عنده محل اعتراض.",
    text: "الوضع هو نحو اختصاص للفظ بالمعنى ، وارتباط خاص بينهما ، ناش من تخصيصه به تارة ، ومن كثرة استعماله فيه أخرى ، وبهذا المعنى صح تقسيمه إلى التعييني والتعيني ، كما لا يخفى .",
    file: "../Resources/books_data/kifayah_akhund.json"
  },
  l02_khoei_commitment: {
    source_id: "l02_khoei_commitment", layer: "advanced", book: "محاضرات في أصول الفقه", author: "السيد أبو القاسم الخوئي",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "ج 1", printed_page: "ص 52",
    scan_or_database_page: "قاعدة النص: 52", content_kind: "verbatim", verification: "exact_text_match",
    context: "صياغة مسلك التعهد ووظيفته التخاطبية.",
    text: "قد تبين أن حقيقة الوضع : عبارة عن التعهد بإبراز المعنى الذي تعلق قصد المتكلم بتفهيمه بلفظ مخصوص ،",
    file: "../Resources/books_data/khoei_muhadarat_1.json"
  },
  l02_sistani_stages: {
    source_id: "l02_sistani_stages", layer: "advanced", book: "الرافد في علم الأصول", author: "السيد علي الحسيني السيستاني، تقرير السيد منير الخباز",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "1", printed_page: "ص 163",
    scan_or_database_page: "قاعدة النص: 163", content_kind: "verbatim", verification: "exact_text_match",
    context: "أربع مراحل لتحليل العلاقة، مع تمييز الاختيار من النتيجة الذهنية.",
    text: "1 - مرحلة الانتخاب : وهي المسماة عندهم بالوضع .\n2 - مرحلة الإشارة : وهي الإشارة باللفظ للمعنى لعوامل كمية أو كيفية تساعد على ذلك .\n3 - مرحلة التلازم والسببية الذهنية : وهي كون صورة اللفظ سببا لتصور المعنى .\n4 - مرحلة الهوهوية : وهي اندماج تصور المعنى في تصور اللفظ .",
    file: "../Resources/books_data/sistani_rafid.json"
  }
};
