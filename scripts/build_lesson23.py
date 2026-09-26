"""Build the offline interactive views of Lessons 2–5 from Markdown renders.

First render the Markdown with PowerShell's ConvertFrom-Markdown to
tmp/lesson23/lesson0N_rendered.html, then run this script. The Markdown is
the canonical lesson text; this builder adds navigation and study controls.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "Usul" / "00_المقدمة_والمبادئ"
TMP = ROOT / "tmp" / "lesson23"

CONFIG = {
    "02": {
        "stem": "02_تقسيم_المباحث_وحقيقة_الوضع_وأقسامه",
        "title": "تقسيم المباحث الأصولية، حقيقة الوضع وأقسامه",
        "subtitle": "ابدأ بتقسيم الموجز، ثم فرّق بين التعيين والتعيّن وأقسام العام والخاص، وبعدها افحص اختلاف المدارس في حقيقة الوضع.",
        "source_count": 12,
        "source_js": "lesson02_sources.js",
        "tasks": [
            "قرأت عبارة الموجز ص 10–13 في تقسيم المباحث والوضع وأقسامه.",
            "أعدت برهان امتناع الخاص/العام مع تحديد فرضه.",
            "دوّنت نكات الشيخ شبير وإجاباته في دفتر التقرير.",
            "قارنت المظفر والصدر والخوئي والآخوند والسيستاني من نصوصهم.",
            "أجريت الاستظهار النشط قبل فتح الأجوبة.",
        ],
        "source_buttons": {
            "core": [
                ("l02_mujaz_division", "تقسيم الموجز"),
                ("l02_mujaz_wad", "تعريف الوضع"),
                ("l02_mujaz_four", "ميزان الأقسام"),
                ("l02_fadhli_text", "الفضلي"),
                ("l02_mutahhari_types", "مطهري"),
                ("l02_sadr_first", "الحلقة الأولى"),
                ("l02_sadr_second", "الحلقة الثانية"),
                ("l02_muzaffar_four", "المظفر"),
            ],
            "advanced": [
                ("l02_murtada_use", "المرتضى"),
                ("l02_akhund_wad", "الآخوند"),
                ("l02_khoei_commitment", "الخوئي"),
                ("l02_sistani_stages", "السيستاني"),
            ],
        },
        "cards": [
            ("ما الأنواع الأربعة للمباحث في الموجز؟", "اللفظية، العقلية، الحجج والأمارات، والأصول العملية."),
            ("ما الفرق بين سؤال الدلالة وسؤال الحجية؟", "الأول يسأل عما يفهم من اللفظ؛ الثاني عن صلاحية ذلك الفهم للاحتجاج."),
            ("أي تعريف للوضع يشمل التعيّني؟", "الاختصاص والارتباط الناشئ من تخصيص أو كثرة استعمال؛ تعريف الجعل الأول يختص بالتعييني."),
            ("كيف تنفي ذاتية دلالة اللفظ؟", "لو كانت من ذات الصوت لفهمه غير المتعلم للغة؛ المشاهدة خلاف ذلك."),
            ("ماذا يعني «الوضع عام»؟", "المعنى الذي لحظه الواضع عند التعيين معنى كلي."),
            ("أعط مثالاً للخاص/الخاص والعام/العام.", "اسم علم لشخص بعينه؛ واسم جنس لمعنى كلي كإنسان."),
            ("هل إمكان العام/الخاص يثبت وقوعه في الحروف؟", "لا؛ وقوعه يحتاج إلى دليل مستقل، والآخوند ينازع فيه."),
            ("لماذا يمتنع الخاص/العام في فرضه؟", "الفرد الخاص لا يحكي عن الجامع الذي لم يتصوره الواضع ولو بوجه."),
            ("ما محورا الشخصي/النوعي والتعييني/التعيّني؟", "الأول كيفية تصور اللفظ الموضوع؛ الثاني طريقة نشوء العلاقة."),
            ("ماذا يضيف الصدر والخوئي إلى التخصيص؟", "الصدر يفسر الانتقال بالقرن الأكيد؛ الخوئي يفسر الوضع بالتعهد عند قصد التفهيم."),
        ],
    },
    "03": {
        "stem": "03_الدلالة_التصورية_والدلالة_التصديقية",
        "title": "الدلالة التصورية والدلالة التصديقية",
        "subtitle": "افصل خطور المعنى عن قصد تفهيمه والمراد الجدي، ثم اسأل متى يصير الظهور حجة في الاستنباط.",
        "source_count": 10,
        "source_js": "lesson03_sources.js",
        "tasks": [
            "قرأت الموجز ص 13 وضبطت التصورية والتصديقية وشروطهما.",
            "فرّقت في الأمثلة بين الإرادة الاستعمالية والجدية.",
            "قارنت اعتراضات الصدر والمظفر والخوئي دون خلط مصطلحاتهم.",
            "دوّنت نكات الشيخ شبير وتطبيقات القرائن في دفتر التقرير.",
            "أجريت الاستظهار النشط قبل فتح الأجوبة.",
        ],
        "source_buttons": {
            "core": [
                ("l03_mujaz_meanings", "الموجز"),
                ("l03_fadhli_appearance", "الفضلي"),
                ("l03_mutahhari_hujjiyya", "مطهري"),
                ("l03_sadr_first", "الحلقة الأولى"),
                ("l03_sadr_second", "الحلقة الثانية"),
                ("l03_muzaffar_strict", "المظفر"),
            ],
            "advanced": [
                ("l03_murtada_address", "المرتضى"),
                ("l03_akhund_will", "الآخوند"),
                ("l03_khoei_strict", "الخوئي"),
                ("l03_sistani_three", "السيستاني"),
            ],
        },
        "cards": [
            ("ما التصورية في الموجز؟", "انتقال الذهن إلى معنى اللفظ بمجرد سماعه ولو لم يقصده اللافظ."),
            ("ما شروط التصديقية في الموجز؟", "علم المتكلم باللغة، مقام البيان، الجد، وعدم نصب قرينة على خلاف المعنى الحقيقي."),
            ("ماذا يضيف الصدر؟", "يفصل قصد التفهيم الاستعمالي عن الغرض الجدي."),
            ("ما الذي يثبت من صوت النائم؟", "قد يخطر المعنى للسّامع؛ لا يثبت قصد تفهيم أو جد."),
            ("ما الذي يثبت من كلام الهازل؟", "الخاطر وقصد استعمال الكلام غالباً؛ لا تبني مضمونه جدّاً."),
            ("كيف تؤثر القرينة المنفصلة؟", "تحد نطاق المراد الجدي أو الحجية ولا يلزم أن تمحو أصل الظهور الاستعمالي."),
            ("ما تحقيق المظفر في لفظ الدلالة؟", "يقصر حقيقتها على كشف قصد المتكلم، ويعد الخاطر المجرد تداعياً."),
            ("لماذا يحصر الخوئي الوضعية في التصديقية؟", "لأنه يفسر الوضع بالتعهد الاختياري بإبراز المعنى عند قصد التفهيم."),
            ("ما أسماء المراتب عند السيستاني؟", "أُنسية، تفهيمية، وتصديقية بمعنى الإلزام العقلائي بالظاهر."),
            ("ما الفرق بين الفهم والحجية؟", "الفهم يحدد الظهور؛ العمل يحتاج إلى إثبات الصدور والحجية والفحص عن القرائن والمعارض."),
        ],
    },
    "04": {
        "stem": "04_الحقيقة_والمجاز_وعلامات_الحقيقة",
        "title": "الحقيقة والمجاز وعلامات الحقيقة",
        "subtitle": "ابدأ بتحليل المجاز في الموجز، ثم اختبر التبادر والحمل والاطراد، وقارن ما تثبته كل علامة بالفعل.",
        "source_count": 15,
        "source_js": "lesson04_sources.js",
        "tasks": [
            "قرأت الموجز ص 14–18 في الحقيقة والمجاز وعلاماتهما.",
            "أعدت دفع دور التبادر وميزت الحمل الأولي من الشائع.",
            "دوّنت نكات الشيخ شبير وإجاباته في دفتر التقرير.",
            "قارنت نقد المظفر والآخوند بتنقيح الخوئي لعلامة الاطراد.",
            "أجريت الاستظهار النشط قبل فتح الأجوبة.",
        ],
        "source_buttons": {
            "core": [
                ("l04_mujaz_famous", "المشهور"), ("l04_mujaz_claim", "ادعاء الموجز"),
                ("l04_mujaz_tabador", "التبادر"), ("l04_mujaz_haml", "الحمل"),
                ("l04_mujaz_itirad", "الاطراد"), ("l04_fadhli_appearance", "الفضلي"),
                ("l04_mutahhari_hujjiyya", "مطهري"), ("l04_sadr_first", "الحلقة الأولى"),
                ("l04_sadr_second", "الحلقة الثانية"), ("l04_muzaffar_itirad", "المظفر"),
            ],
            "advanced": [
                ("l04_murtada_definition", "المرتضى"), ("l04_tusi_metaphor", "الطوسي"),
                ("l04_akhund_itirad", "الآخوند"), ("l04_khoei_refined", "الخوئي"),
                ("l04_sistani_three", "السيستاني"),
            ],
        },
        "cards": [
            ("ما المجاز على التعريف المشهور؟", "استعمال اللفظ في غير ما وضع له لعلاقة مع قرينة."),
            ("أين يضع الموجز التجوز في استعارة أسد؟", "في ادعاء فردية الشجاع لمفهوم الأسد، مع استعمال اللفظ في معناه الأصلي."),
            ("ما شرط التبادر المعتبر؟", "أن يكون من حاق اللفظ بلا معونة قرينة."),
            ("كيف يدفع الدور في التبادر؟", "المرتكز الإجمالي غير العلم التفصيلي؛ أو تبادر أهل اللغة علامة للجاهل بها."),
            ("ما الفرق بين الحمل الأولي والشائع؟", "الأول اتحاد مفهومي، والثاني صدق عنوان على مصداق في الخارج."),
            ("ما اعتراض الصدر على الحمل علامة للوضع؟", "صحة حمل معنى لا تثبت أن لفظ المحمول موضوع له من دون ضبط معناه."),
            ("ما دعوى الموجز في الاطراد؟", "استمرار الاستعمال في أفراد جامع واحد يكشف عنده عن وضع اللفظ للجامع."),
            ("لماذا يعترض المظفر والآخوند؟", "المجاز يطرد كذلك مع حفظ علاقة استعماله."),
            ("ما تنقيح الخوئي؟", "تنوع المحامل والسياقات مع طرح القرائن المحتملة قد يكشف المعنى الحقيقي."),
            ("هل تبادر اليوم يكفي لنص قديم؟", "لا؛ يلزم بحث تغير اللغة وقرائن زمن صدور النص."),
        ],
    },
    "05": {
        "stem": "05_الأصول_اللفظية_العقلائية",
        "title": "الأصول اللفظية العقلائية وأصالة الظهور",
        "subtitle": "افصل الشك في الوضع عن الشك في المراد، ثم اتبع ظهور الكلام بقرائنه وافحص حدود حجيته.",
        "source_count": 14,
        "source_js": "lesson05_sources.js",
        "tasks": [
            "قرأت الموجز ص 18–20 وحددت نوعي الشك والأصول الخمسة.",
            "أعدت الاستدلال من الظهور إلى المراد والحجية.",
            "دوّنت نكات الشيخ شبير وإجاباته في دفتر التقرير.",
            "قارنت المظفر والصدر والآخوند والخوئي والسيستاني من مقاطعهم.",
            "أجريت الاستظهار النشط قبل فتح الأجوبة.",
        ],
        "source_buttons": {
            "core": [
                ("l05_mujaz_doubt", "نوعا الشك"), ("l05_mujaz_hakika", "أصالة الحقيقة"),
                ("l05_mujaz_unity", "أصالة الظهور"), ("l05_fadhli_appearance", "الفضلي"),
                ("l05_mutahhari_hujjiyya", "مطهري"), ("l05_sadr_first", "الحلقة الأولى"),
                ("l05_sadr_second", "الحلقة الثانية"), ("l05_muzaffar_unity", "المظفر"),
            ],
            "advanced": [
                ("l05_murtada_apparent", "المرتضى"), ("l05_tusi_apparent", "الطوسي"),
                ("l05_akhund_intent", "الآخوند"), ("l05_khoei_custom", "الخوئي"),
                ("l05_sistani_scope", "حدود الحجية"), ("l05_sistani_no_taabbud", "السيستاني"),
            ],
        },
        "cards": [
            ("ما نوعا الشك في الموجز؟", "الشك في الموضوع له، والشك في مراد المتكلم بعد العلم بالوضع."),
            ("لماذا لا تثبت أصالة الحقيقة وضع الصعيد؟", "لأنها تعالج المراد عند ظهور معروف، لا أصل المعنى المعجمي."),
            ("ما مورد أصالة الحقيقة؟", "احتمال إرادة المجاز مع ظهور الكلام في المعنى الحقيقي وعدم قرينة صارفة."),
            ("ما مورد أصالة العموم؟", "الشك في تخصيص عام انعقد ظهوره في العموم."),
            ("ماذا تفحص قبل أصالة الإطلاق؟", "مقام البيان والقرائن وشروط انعقاد الإطلاق."),
            ("متى يسقط أصل عدم التقدير؟", "إذا قامت قرينة على محذوف أو صار الكلام بسياقه ظاهراً فيه."),
            ("إذا ظهر المجاز بقرينة فماذا يقدم؟", "الظهور النهائي للكلام؛ لا تعمل الحقيقة تعبداً ضده."),
            ("كيف يستدل على حجية الظهور؟", "السيرة العقلائية في المحاورة مع إمضاء الشارع وعدم الردع."),
            ("ما الفرق بين احتمال القرينة وقرينية الموجود؟", "الأول احتمال غير مثبت، والثاني عنصر حاضر قد يمنع انعقاد ظهور واضح."),
            ("ما خطوات الاستناد الفقهي؟", "ضبط النص والمعنى والسياق والمراد، ثم الصدور والحجية والفحص عن المعارض."),
        ],
    },
}

TABS = [
    ("orientation", "1. التوجيه"),
    ("core", "2. الطبقة الأساسية"),
    ("reconstruction", "3. إعادة التركيب"),
    ("advanced", "4. التحقيق المتقدم"),
    ("applications", "5. التطبيقات"),
    ("mastery", "6. الإتقان"),
    ("sources", "7. المصادر"),
]


def split_sections(rendered: str) -> list[str]:
    starts = list(re.finditer(r'<h2 id="section-\d+">', rendered))
    if len(starts) != 7:
        raise ValueError(f"Expected 7 lesson sections; found {len(starts)}")
    parts = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(rendered)
        part = rendered[match.start():end]
        part = re.sub(r"\s*<hr\s*/>\s*$", "", part)
        parts.append(part)
    return parts


def source_buttons(buttons: list[tuple[str, str]]) -> str:
    items = " ".join(
        f'<button class="source-button" type="button" data-source="{sid}">{html.escape(label)}</button>'
        for sid, label in buttons
    )
    return f'<div class="card source-shortcuts"><strong>اقرأ النصوص المباشرة:</strong> {items}</div>'


def task_list(tasks: list[str]) -> str:
    return "\n".join(
        f'<li><label><input class="task-check" id="task-{i}" type="checkbox"><span>{html.escape(task)}</span></label></li>'
        for i, task in enumerate(tasks, 1)
    )


def flashcards(cards: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'<button class="flashcard" type="button" aria-expanded="false">'
        f'<span class="front">{i}. {html.escape(question)}</span>'
        f'<span class="back" hidden>{html.escape(answer)}</span></button>'
        for i, (question, answer) in enumerate(cards, 1)
    )


def build(number: str) -> None:
    config = CONFIG[number]
    sections = split_sections((TMP / f"lesson{number}_rendered.html").read_text(encoding="utf-8-sig"))
    nav = "\n".join(
        f'<button class="tab" role="tab" aria-selected="false" data-tab="{sid}">{html.escape(label)}</button>'
        for sid, label in TABS
    )
    panels = []
    for (sid, _), content in zip(TABS, sections):
        additions = ""
        if sid == "orientation":
            additions = f'''
<div class="grid two lesson-controls">
  <article class="card"><h3>خطة الإنجاز</h3><ul class="task-list" id="tasks-list">{task_list(config["tasks"])}</ul></article>
  <article class="card"><h3>دفتر تقرير الدرس</h3><p class="muted">الملاحظات محفوظة تلقائياً على هذا الجهاز.</p>
    <div class="toolbar"><span id="save-status" class="muted"></span><span id="notes-unified-count" class="muted">0 حرف</span><button class="btn small" id="copy-notes" type="button">نسخ</button></div>
    <textarea class="notes" id="notes-unified" aria-label="دفتر تقرير الدرس" placeholder="نكات الأستاذ، الإشكالات، الأجوبة، وما يحتاج إلى مراجعة"></textarea>
  </article>
</div>'''
        elif sid in ("core", "advanced"):
            additions = source_buttons(config["source_buttons"][sid])
        elif sid == "mastery":
            additions = f'''
<article class="card lesson-controls"><h3>بطاقات الاستظهار: أجب أولاً ثم اضغط البطاقة</h3><div class="flash-grid">{flashcards(config["cards"])}</div></article>
<div class="grid two lesson-controls">
  <article class="card"><h3>سجل الأخطاء</h3><span id="error-log-count" class="muted">0 حرف</span>
    <textarea class="error-log" id="error-log" aria-label="سجل الأخطاء" placeholder="السؤال ← جوابي الأول ← موضع الخطأ ← التصحيح ← مثال جديد"></textarea>
  </article>
  <article class="card"><h3>المراجعات المتباعدة</h3><ul class="task-list">
    <li><label><input class="task-check" id="task-6" type="checkbox"><span>بعد يوم: أعدت الأساس من الذاكرة.</span></label><input id="review-1" data-review-date type="date" aria-label="تاريخ مراجعة اليوم الأول"></li>
    <li><label><input class="task-check" id="task-7" type="checkbox"><span>بعد 7 أيام: حللت تطبيقاً جديداً.</span></label><input id="review-7" data-review-date type="date" aria-label="تاريخ مراجعة الأسبوع"></li>
    <li><label><input class="task-check" id="task-8" type="checkbox"><span>بعد 21 يوماً: أجريت مباحثة شفهية.</span></label><input id="review-21" data-review-date type="date" aria-label="تاريخ مراجعة اليوم الحادي والعشرين"></li>
  </ul></article>
</div>'''
        elif sid == "sources":
            additions = '''<div class="toolbar lesson-controls"><strong>المقتطفات الموثقة</strong><div>
<button class="btn small primary" type="button" data-source-filter="all">الكل</button>
<button class="btn small" type="button" data-source-filter="core">الأساسي</button>
<button class="btn small" type="button" data-source-filter="advanced">المتقدم</button></div></div>
<div class="source-grid" id="source-list"></div>'''
        panels.append(f'<section class="panel" id="panel-{sid}" tabindex="-1" hidden><article class="card lesson-prose">{content}</article>{additions}</section>')
    result = f'''<!doctype html>
<html lang="ar" dir="rtl" data-theme="light">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="درس أصولي محقق في {html.escape(config["title"])} بطبقتين أساسية ومتقدمة.">
  <title>الدرس {number} — {html.escape(config["title"])}</title>
  <script>try{{const t=localStorage.getItem('shabbir_usul_theme');if(t==='dark'||t==='light')document.documentElement.dataset.theme=t}}catch(e){{}}</script>
  <link rel="stylesheet" href="../Resources/lesson_assets/lesson.css">
</head>
<body data-lesson="{number}">
  <header class="site-header"><div class="shell header-grid">
    <div class="header-copy"><p class="eyebrow">الموجز في أصول الفقه • الدرس {number} • النسخة المعيارية</p>
      <h1>{html.escape(config["title"])}</h1><p class="subtitle">{html.escape(config["subtitle"])}</p>
      <div class="meta-row"><span class="pill core">الطبقة الأساسية كاملة</span><span class="pill advanced">التحقيق المتقدم</span>
      <span class="pill verified">{config["source_count"]} مقتطفاً موثقاً</span><span class="pill">4 س 15 د</span></div></div>
    <div class="header-actions"><button class="btn" id="theme-toggle" type="button"><span id="theme-label">النمط الداكن</span></button>
      <button class="btn" id="print-lesson" type="button">طباعة الدرس</button>
      <a class="btn" href="{config["stem"]}.md">نسخة Markdown</a></div>
  </div><div class="shell progress-panel" aria-label="تقدم الدرس"><div class="progress-row"><span>تقدم التحضير والمراجعة</span>
  <span id="progress-text">0 من 8 • 0٪</span></div><div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div></div></header>
  <nav class="tabs-wrap" aria-label="أقسام الدرس"><div class="shell tabs" role="tablist">{nav}</div></nav>
  <main class="shell">{"".join(panels)}</main>
  <footer class="footer">معيار الدرس {number} • الموجز هو المتن الضابط • آخر مقابلة للمصادر المصورة: 23 سبتمبر 2026</footer>
  <div class="drawer-overlay" id="source-overlay"></div>
  <aside class="drawer" id="source-drawer" aria-hidden="true" aria-label="المصدر">
    <div class="drawer-head"><div><p class="eyebrow">المصدر</p><h2 id="source-title"></h2><p id="source-author" class="muted"></p></div>
      <button class="btn small" id="source-close" type="button">إغلاق</button></div>
    <div class="drawer-body"><div class="meta-row"><span class="pill" id="source-kind"></span><span class="pill verified" id="source-verification"></span></div>
      <dl class="provenance" id="source-provenance"></dl><p id="source-context"></p><blockquote class="source-text" id="source-text"></blockquote>
      <div class="toolbar"><button class="btn small" id="source-copy" type="button">نسخ النص</button>
      <a class="btn small" id="source-link" href="#">فتح المصدر المحلي</a></div></div>
  </aside>
  <script src="../Resources/lesson_assets/{config["source_js"]}"></script>
  <script src="../Resources/lesson_assets/lesson.js"></script>
</body></html>
'''
    (LESSON_DIR / f'{config["stem"]}.html').write_text(result, encoding="utf-8")


if __name__ == "__main__":
    for lesson_number in CONFIG:
        build(lesson_number)
    print("Built Lessons 2–5 interactive HTML.")
