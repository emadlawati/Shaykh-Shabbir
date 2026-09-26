window.LESSON_LABELS = {
  content_kind: { verbatim: "نص حرفي", summary: "تلخيص أمين", analysis: "تحليل تحريري", teacher_note: "تقرير الأستاذ" },
  verification: { exact_text_match: "مطابق للنص الرقمي", visually_verified_scan: "مقابل بصرياً على النسخة المصورة", pending: "بانتظار التحقيق" }
};
window.LESSON_SOURCE_ORDER = [
  "l03_mujaz_meanings", "l03_fadhli_appearance", "l03_mutahhari_hujjiyya",
  "l03_sadr_first", "l03_sadr_second", "l03_muzaffar_strict",
  "l03_murtada_address", "l03_akhund_will", "l03_khoei_strict",
  "l03_sistani_three"
];
window.LESSON_SOURCES = {
  l03_mujaz_meanings: {
    source_id: "l03_mujaz_meanings", layer: "core", book: "الموجز في أصول الفقه", author: "الشيخ جعفر السبحاني",
    edition: "الطبعة الرابعة عشرة، مؤسسة الإمام الصادق، 1429هـ", volume: "1", printed_page: "ص 13",
    scan_or_database_page: "قاعدة النص: 13", content_kind: "verbatim", verification: "exact_text_match",
    context: "التقسيم الثنائي وشروط التصديقية في المتن الضابط.",
    text: "فالدلالة التصوّرية : هي عبارة عن انتقال الذهن إلى معنى اللّفظ بمجرّد سماعه وإن لم يقصده اللّافظ ، كما إذا سمعه من الساهي أو النائم .\nوأمّا الدلالة التصديقيّة : فهي دلالة اللّفظ على أنّ المعنى مراد للمتكلّم ومقصود له .\nفالدلالة الأولى تحصل بالعلم باللغة ، وأمّا الثانية فتتوقف على أمور :\nأ . أن يكون المتكلم عالما باللغة .\nب . أن يكون في مقام البيان والإفادة .\nج . أن يكون جادّا لا هازلا .\nد . أن لا ينصب قرينة على خلاف المعنى الحقيقي .",
    file: "../Resources/books_data/mujaz_subhani.json"
  },
  l03_fadhli_appearance: {
    source_id: "l03_fadhli_appearance", layer: "core", book: "مبادئ أصول الفقه", author: "العلامة عبد الهادي الفضلي",
    edition: "مركز الغدير للدراسات والنشر والتوزيع؛ النسخة المصورة المحلية", volume: "1", printed_page: "ص 44",
    scan_or_database_page: "PDF ص 46", content_kind: "verbatim", verification: "visually_verified_scan",
    context: "النص والظاهر من جهة احتمال المعنى؛ لا يعرض تقسيم التصورية والتصديقية.",
    text: "وتتنوع دراسة دلالة المتن إلى نوعين هما: دراسة النص ودراسة الظاهر، وذلك لأن الألفاظ -بطبيعتها- قد تكون نصّاً في معانيها، وقد تكون ظاهرة فيها.",
    file: "../مبادئ أصول الفقه - العلامة عبدالهادي الفضلي.pdf", pdf_page: 46
  },
  l03_mutahhari_hujjiyya: {
    source_id: "l03_mutahhari_hujjiyya", layer: "core", book: "الأصول", author: "الشهيد مرتضى مطهري",
    edition: "ترجمة حسن علي الهاشمي، دار الولاء، الطبعة الأولى، 2009/1430", volume: "1", printed_page: "ص 38",
    scan_or_database_page: "PDF ص 38", content_kind: "verbatim", verification: "visually_verified_scan",
    context: "فصل فهم ظاهر القرآن عن سؤال جواز الاستناد إليه.",
    text: "هل ظاهر القرآن - بقطع النظر عن تفسيره من خلال حديث - حجة ويمكن للفقيه أن يستند إليه أو لا؟",
    file: "../الأصول - الشهيد الشيخ مرتضى مطهري.pdf", pdf_page: 38
  },
  l03_sadr_first: {
    source_id: "l03_sadr_first", layer: "core", book: "دروس في علم الأصول، الحلقة الأولى", author: "الشهيد السيد محمد باقر الصدر",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "الحلقة الأولى", printed_page: "ص 75–76",
    scan_or_database_page: "قاعدة النص: 75–76", content_kind: "verbatim", verification: "exact_text_match",
    context: "الدلالة التصورية وما يضاف إليها من مدلولين تصديقيين.",
    text: "ولا تنفك هذه الدلالة عن اللفظ مهما سمعناه ومن أي مصدر كان",
    file: "../Resources/books_data/sadr_halaqat_1.json"
  },
  l03_sadr_second: {
    source_id: "l03_sadr_second", layer: "core", book: "دروس في علم الأصول، الحلقة الثانية", author: "الشهيد السيد محمد باقر الصدر",
    edition: "نسخة قاعدة النص المحلية؛ ترقيمها مختلف عن PDF المصور", volume: "الحلقة الثانية", printed_page: "ص 184–186 في نسخة النص",
    scan_or_database_page: "قاعدة النص: 184–186", content_kind: "verbatim", verification: "exact_text_match",
    context: "الجد والهزل ومصدر كل مرتبة دلالية.",
    text: "وأما الهازل حين يقول الماء بارد ، فلكلامه دلالة تصورية ودلالة تصديقية أولى دون الدلالة التصديقية الثانية ، لأنه ليس جادا ولا يريد الاخبار حقيقية ، وأما الآلة حين تردد الجملة ذاتها فليس لها إلا دلالة تصورية فقط .",
    file: "../Resources/books_data/sadr_halaqat_1.json"
  },
  l03_muzaffar_strict: {
    source_id: "l03_muzaffar_strict", layer: "core", book: "أصول الفقه", author: "الشيخ محمد رضا المظفر",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "ج 1", printed_page: "ص 65",
    scan_or_database_page: "قاعدة النص: 65", content_kind: "verbatim", verification: "exact_text_match",
    context: "يذكر التقسيم الشائع ثم يضيق الدلالة الحقيقية إلى الكشف عن الإرادة.",
    text: "والحق أن الدلالة تابعة للإرادة",
    file: "../Resources/books_data/usul_muzaffar_1.json"
  },
  l03_murtada_address: {
    source_id: "l03_murtada_address", layer: "advanced", book: "الذريعة إلى أصول الشريعة", author: "السيد المرتضى",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "ج 1", printed_page: "ص 60",
    scan_or_database_page: "قاعدة النص: 60", content_kind: "verbatim", verification: "exact_text_match",
    context: "الكلام من النائم قد يفهم لغوياً ولا يكون خطاباً مقصوداً.",
    text: "ولهذا جاز أن يتكلّم النّائم ، ولم يجز أن يخاطب ، كما لم يجز أن يأمر وينهى .",
    file: "../Resources/books_data/murtada_dhariyah_1.json"
  },
  l03_akhund_will: {
    source_id: "l03_akhund_will", layer: "advanced", book: "كفاية الأصول", author: "الآخوند محمد كاظم الخراساني",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "1", printed_page: "ص 16",
    scan_or_database_page: "قاعدة النص: 16", content_kind: "verbatim", verification: "exact_text_match",
    context: "الإرادة ليست جزءاً من الموضوع له، وإن كان القصد جزءاً من الاستعمال.",
    text: "لا ريب في كون الألفاظ موضوعة بإزاء معانيها من حيث هي ، لا من حيث هي مرادة للافظها",
    file: "../Resources/books_data/kifayah_akhund.json"
  },
  l03_khoei_strict: {
    source_id: "l03_khoei_strict", layer: "advanced", book: "محاضرات في أصول الفقه", author: "السيد أبو القاسم الخوئي",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "ج 1", printed_page: "ص 118",
    scan_or_database_page: "قاعدة النص: 118", content_kind: "verbatim", verification: "exact_text_match",
    context: "حصر الدلالة الوضعية بالتصديقية بناء على مسلك التعهد.",
    text: "وأما الدلالة التصورية - وهي : الانتقال إلى المعنى من سماع اللفظ - فهي غير مستندة إلى الوضع ، بل هي من جهة الانس الحاصل من كثرة الاستعمال",
    file: "../Resources/books_data/khoei_muhadarat_1.json"
  },
  l03_sistani_three: {
    source_id: "l03_sistani_three", layer: "advanced", book: "الرافد في علم الأصول", author: "السيد علي الحسيني السيستاني، تقرير السيد منير الخباز",
    edition: "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", volume: "1", printed_page: "ص 145",
    scan_or_database_page: "قاعدة النص: 145", content_kind: "verbatim", verification: "exact_text_match",
    context: "يسمي المراتب الأنسية والتفهيمية والتصديقية؛ الأخيرة موضع الإلزام العقلائي.",
    text: "الدلالة التفهيمية : وهي التي تتقوم بقصد المتكلم اخطار المعنى في ذهن السامع",
    file: "../Resources/books_data/sistani_rafid.json"
  }
};
