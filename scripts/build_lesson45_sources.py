"""Build short, page-bound Lesson 4/5 source extracts from local book texts.

For scanned works, only previously visually checked extracts are reused.
The exact slice markers fail loudly if a local database edition changes.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "Usul" / "Resources" / "books_data"
ASSETS = ROOT / "Usul" / "Resources" / "lesson_assets"

META = {
    "mujaz_subhani": ("الموجز في أصول الفقه", "الشيخ جعفر السبحاني", "الطبعة الرابعة عشرة، مؤسسة الإمام الصادق، 1429هـ", "1"),
    "usul_muzaffar_1": ("أصول الفقه", "الشيخ محمد رضا المظفر", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "ج 1"),
    "sadr_halaqat_1": ("دروس في علم الأصول", "الشهيد السيد محمد باقر الصدر", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "الحلقة الأولى/الثانية بحسب الموضع"),
    "murtada_dhariyah_1": ("الذريعة إلى أصول الشريعة", "السيد المرتضى", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "ج 1"),
    "tusi_uddah_1": ("العدة في أصول الفقه", "الشيخ الطوسي", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "ج 1"),
    "kifayah_akhund": ("كفاية الأصول", "الآخوند محمد كاظم الخراساني", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "1"),
    "khoei_muhadarat_1": ("محاضرات في أصول الفقه", "السيد أبو القاسم الخوئي", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "ج 1"),
    "sistani_rafid": ("الرافد في علم الأصول", "السيد علي الحسيني السيستاني، تقرير السيد منير الخباز", "نسخة قاعدة النص المحلية؛ بيانات الطبعة غير مثبتة", "1"),
}


def digital(sid: str, layer: str, book_id: str, pages: list[int], start: str, end: str, context: str, *, volume: str | None = None) -> dict:
    book, author, edition, default_volume = META[book_id]
    data = json.loads((BOOKS / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    body = "\n".join(data["pages"][str(page)]["body"] for page in pages)
    first = body.find(start)
    if first < 0:
        raise ValueError(f"{sid}: beginning not found")
    last = body.find(end, first)
    if last < 0:
        raise ValueError(f"{sid}: ending not found")
    excerpt = body[first:last + len(end)].strip()
    page_label = str(pages[0]) if len(pages) == 1 else f"{pages[0]}–{pages[-1]}"
    if book_id == "sadr_halaqat_1":
        edition = "نسخة قاعدة النص المحلية؛ ترقيم الحلقة الثانية مختلف عن PDF المصور" if pages[0] >= 140 else edition
        page_label = f"{page_label} في نسخة النص" if pages[0] >= 140 else page_label
    return {
        "source_id": sid, "layer": layer, "book": book, "author": author,
        "edition": edition, "volume": volume or default_volume,
        "printed_page": f"ص {page_label}", "scan_or_database_page": f"قاعدة النص: {page_label}",
        "content_kind": "verbatim", "verification": "exact_text_match", "context": context,
        "text": excerpt, "file": f"../Resources/books_data/{book_id}.json",
    }


def scan(sid: str, book: str, author: str, edition: str, printed: str, pdf_page: int, text: str, context: str) -> dict:
    filename = "مبادئ أصول الفقه - العلامة عبدالهادي الفضلي.pdf" if "الفضلي" in author else "الأصول - الشهيد الشيخ مرتضى مطهري.pdf"
    return {
        "source_id": sid, "layer": "core", "book": book, "author": author,
        "edition": edition, "volume": "1", "printed_page": printed,
        "scan_or_database_page": f"PDF ص {pdf_page}", "content_kind": "verbatim",
        "verification": "visually_verified_scan", "context": context, "text": text,
        "file": f"../{filename}", "pdf_page": pdf_page,
    }


FADHLI = ("مبادئ أصول الفقه", "العلامة عبد الهادي الفضلي", "مركز الغدير للدراسات والنشر والتوزيع؛ النسخة المصورة المحلية")
MUTAHHARI = ("الأصول", "الشهيد مرتضى مطهري", "ترجمة حسن علي الهاشمي، دار الولاء، الطبعة الأولى، 2009/1430")

SOURCES = {
    "04": [
        digital("l04_mujaz_famous", "core", "mujaz_subhani", [14], "الاستعمال الحقيقي :", "كإطلاق الأسد وإرادة الرجل الشجاع .", "تعريف الحقيقة والمجاز المشهور."),
        digital("l04_mujaz_claim", "core", "mujaz_subhani", [14], "إنّ اللّفظ - سواء", "المورد من مصاديق الموضوع له ،", "التحليل الادعائي الذي يختاره المتن للاستعارة."),
        digital("l04_mujaz_tabador", "core", "mujaz_subhani", [15], "هو انسباق المعنى", "فيثبت الثاني .", "التبادر من حاق اللفظ مع نفي القرينة."),
        digital("l04_mujaz_haml", "core", "mujaz_subhani", [16], "فاعلم أنّ المقصود", "هو القسم الأوّل ،", "الموجز يرجح الحمل الأولي في كشف وحدة المفهوم."),
        digital("l04_mujaz_itirad", "core", "mujaz_subhani", [16], "إذا اطّرد استعمال لفظ", "قد وضع اللّفظ بإزائه .", "التقرير الأولي لعلامة الاطراد."),
        scan("l04_fadhli_appearance", *FADHLI, "ص 44", 46, "والظاهر: هو اللفظ الذي يدل على أكثر من معنى واحد، إلا أن دلالته على أحد معانيه أقوى من دلالته على المعاني الآخر.", "تمييز الظاهر من النص بعد بحث الوضع."),
        scan("l04_mutahhari_hujjiyya", *MUTAHHARI, "ص 38", 38, "هل ظاهر القرآن - بقطع النظر عن تفسيره من خلال حديث - حجة ويمكن للفقيه أن يستند إليه أو لا؟", "فصل فهم الظاهر عن سؤال الاستناد إليه."),
        digital("l04_sadr_first", "core", "sadr_halaqat_1", [70], "والاستعمال المجازي هو", "المجازي .", "الشرح الأولي لعلاقة المجاز الثانوية.", volume="الحلقة الأولى"),
        digital("l04_sadr_second", "core", "sadr_halaqat_1", [190, 191], "والتحقيق أن الاعتراض بالدور", "فلا دور .", "تفسير التبادر بالقرن الأكيد بدل توقفه على العلم النظري.", volume="الحلقة الثانية"),
        digital("l04_muzaffar_itirad", "core", "usul_muzaffar_1", [72], "والصحيح : أن الاطراد", "حتى يكون علامة لها .", "نقد الاطراد المطلق علامة للحقيقة."),
        digital("l04_murtada_definition", "advanced", "murtada_dhariyah_1", [62], "فاللّفظ الموصوف بأنّه حقيقة", "ولا عرف ، ولا شرع .", "التعريف القديم للحقيقة والمجاز بحسب الوضع في لغة وعرف وشرع."),
        digital("l04_tusi_metaphor", "advanced", "tusi_uddah_1", [143], "والمجاز الثالث ،", "دليل على كونه مجازا .", "تقسيم قديم للمجاز وتقديم ظاهر الحقيقة."),
        digital("l04_akhund_itirad", "advanced", "kifayah_akhund", [20], "ثم إنه قد ذكر الاطراد", "وجه دائر ،", "المجاز يطرد مع حفظ العلاقة؛ قيد الحقيقة يجعل العلامة دورية."),
        digital("l04_khoei_refined", "advanced", "khoei_muhadarat_1", [139, 140], "والذي ينبغي أن يقال", "إلا أنه نادر جدا .", "تنقيح الاطراد بتعدد السياقات وإلغاء القرائن المحتملة."),
        digital("l04_sistani_three", "advanced", "sistani_rafid", [203, 204], "الأولى : ما هو منقول", "بحث الحقيقة والمجاز .", "تمييز صيغ الاتجاه النافي للمجاز في الكلمة."),
    ],
    "05": [
        digital("l05_mujaz_doubt", "core", "mujaz_subhani", [18], "إنّ الشكّ في الكلام", "ب . الشكّ في مراد المتكلّم بعد العلم بالمعنى الموضوع له .", "الفصل بين الشك في الوضع والشك في المراد."),
        digital("l05_mujaz_hakika", "core", "mujaz_subhani", [19], "إذا شكّ في إرادة المعنى الحقيقي", "وهذا ما يعبّر عنه بأصالة الحقيقة .", "مورد أصالة الحقيقة في المتن الضابط."),
        digital("l05_mujaz_unity", "core", "mujaz_subhani", [20], "ثمّ إنّ الأصول السابقة", "فهي حجّة .", "رد الأصول إلى الظهور وبناء العقلاء وعدم الردع."),
        scan("l05_fadhli_appearance", *FADHLI, "ص 44", 46, "والظاهر: هو اللفظ الذي يدل على أكثر من معنى واحد، إلا أن دلالته على أحد معانيه أقوى من دلالته على المعاني الآخر.", "تعريف الظهور الذي يسبق تطبيق أصالة الظهور."),
        scan("l05_mutahhari_hujjiyya", *MUTAHHARI, "ص 38", 38, "هل ظاهر القرآن - بقطع النظر عن تفسيره من خلال حديث - حجة ويمكن للفقيه أن يستند إليه أو لا؟", "الفصل بين فهم ظاهر القرآن وحجيته."),
        digital("l05_sadr_first", "core", "sadr_halaqat_1", [88], "وهنا نستعين بظهورين", "حجة .", "الظهور التصوري وظهور حال المتكلم في التطابق.", volume="الحلقة الأولى"),
        digital("l05_sadr_second", "core", "sadr_halaqat_1", [226], "ومرد ذلك في الحقيقة", "اسم أصالة الحقيقة .", "أصالة الحقيقة بوصفها ظهور التطابق في قصد التفهيم.", volume="الحلقة الثانية"),
        digital("l05_muzaffar_unity", "core", "usul_muzaffar_1", [76], "وفي الحقيقة أن جميع الأصول", "ولا تجري أصالة الحقيقة حينئذ .", "وحدة أصالة الظهور وتقديم الظهور المجازي عند قيامه."),
        digital("l05_murtada_apparent", "advanced", "murtada_dhariyah_1", [62], "ومن حكم الحقيقة وجوب حملها", "بدليل .", "الشاهد القديم في أولوية ظاهر الحقيقة بلا دليل صارف."),
        digital("l05_tusi_apparent", "advanced", "tusi_uddah_1", [143], "ويجب حمل الحقيقة على ظاهرها", "دليل على كونه مجازا .", "الشاهد الطوسي على تقديم الظاهر ودور الدليل الصارف."),
        digital("l05_akhund_intent", "advanced", "kifayah_akhund", [233], "وبالجملة : أصالة الظهور", "بالاجمال ،", "الفرق بين تعيين ما أريد وكيفية الاستعمال، وقيد انعقاد الظهور."),
        digital("l05_khoei_custom", "advanced", "khoei_muhadarat_1", [235], "وعلى ذلك فإن استعمل اللفظ", "كما لا يخفى ( 2 ) .", "عدم جعل الحقيقة التعبدية بديلاً عن الظهور العرفي."),
        digital("l05_sistani_scope", "advanced", "sistani_rafid", [124, 125], "كما ذكرنا في الامر السابق أنه لا نزاع كبروي", "ضمن علم الأصول .", "النزاع في شمول الظهور وعدم لغوية بحث الحجية."),
        digital("l05_sistani_no_taabbud", "advanced", "sistani_rafid", [209], "ولم\nيقم بناء من العقلاء", "للأصل العملي .", "لا تجري أصالة الحقيقة تعبداً حيث تخالف الظهور؛ يحتاج هذا المقطع إلى سياقه في المثال.")
    ],
}

LABELS = {
    "content_kind": {"verbatim": "نص حرفي", "summary": "تلخيص أمين", "analysis": "تحليل تحريري", "teacher_note": "تقرير الأستاذ"},
    "verification": {"exact_text_match": "مطابق للنص الرقمي", "visually_verified_scan": "مقابل بصرياً على النسخة المصورة", "pending": "بانتظار التحقيق"},
}

for number, records in SOURCES.items():
    order = [record["source_id"] for record in records]
    mapping = {record["source_id"]: record for record in records}
    payload = (
        "window.LESSON_LABELS = " + json.dumps(LABELS, ensure_ascii=False, indent=2) + ";\n"
        + "window.LESSON_SOURCE_ORDER = " + json.dumps(order, ensure_ascii=False, indent=2) + ";\n"
        + "window.LESSON_SOURCES = " + json.dumps(mapping, ensure_ascii=False, indent=2) + ";\n"
    )
    (ASSETS / f"lesson{number}_sources.js").write_text(payload, encoding="utf-8")
    print(f"Lesson {number}: {len(records)} extracts")
