#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة المساعد الأصولي الذكي (Usul Study Assistant CLI)
للبحث والمطالعة واستخراج النصوص ومقارنة المسائل بين الموجز والمظفر والشهيد الصدر
وربطها بالحديث والفقه من مكتبات نور وأهل البيت.
"""

import os
import sys
import re
import argparse
from pathlib import Path

# ضبط مخرجات الطرفية لدعم اللغة العربية والترميز العالمي
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# مسارات المكتبات المحلية المعتمدة
BASE_DIR = Path(__file__).resolve().parent.parent
NOOR_USUL_DIR = Path(r"C:\Imad Works\OpenCode\Scraping\out_es\jamiusoul3\ar")
NOOR_HADITH_DIR = Path(r"C:\Imad Works\OpenCode\Scraping\out_es\jamiahadith4")
NOOR_FIQH_DIR = Path(r"C:\Imad Works\OpenCode\Scraping\out_es\jamifeqh3")
AHLULBAYT_DIR = Path(r"C:\Imad Works\OpenCode\Urwa Extraction\output\AhlulBayt Library")
DICT_DIR = AHLULBAYT_DIR / "مصطلحات ومفردات فقهية"
MASTER_DICT_FILE = BASE_DIR / "Master_Dictionary.md"

# ملف النص الكامل المعتمد لكتاب الموجز من مكتبة أهل البيت
MUJAZ_FULL_FILE = AHLULBAYT_DIR / "أصول الفقه عند الشيعة" / "الموجز في أصول الفقه - الشيخ جعفر السبحاني - موسسه الامام الصادق ( ع ) - قم - ج 01 - 1.md"
TEMPLATE_FILE = BASE_DIR / "Templates" / "درس_أصولي_نموذجي.md"

def normalize_arabic(text: str) -> str:
    """توحيد الحروف العربية لتسهيل المطابقة والبحث التقريبي"""
    if not text:
        return ""
    text = re.sub(r'[\u064B-\u0652\u0640]', '', text)  # إزالة التشكيل وحركات الإعراب والتطويل
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'[يى]', 'ي', text)
    text = re.sub(r'[\u06A9]', 'ك', text)
    text = re.sub(r'[\u06CC]', 'ي', text)
    return text.strip()

def cmd_info(args):
    """عرض إحصائيات الموارد والمكتبات المحلية المتصلة"""
    print("=" * 65)
    print("        بيئة البحث الأصولي والمكتبات الحوزوية المتصلة")
    print("=" * 65)
    print(f"• المجلد الرئيسي لمشروع الدراسة : {BASE_DIR}")
    print(f"• المعجم الأصولي والفقهي الشامل : {'متوفر ومربوط' if MASTER_DICT_FILE.exists() else 'قيد التجهيز'}")
    print(f"• معاجم المصطلحات التخصصية     : {'متوفرة [29 معجماً كاملاً]' if DICT_DIR.exists() else 'غير موجودة'}")
    print(f"• النص الكامل لكتاب الموجز     : {'متوفر ومربوط [278 ألف حرف]' if MUJAZ_FULL_FILE.exists() else 'غير موجود'}")
    print(f"• مكتبة نور (جامع الأصول)      : {'متوفرة ومربوطة' if NOOR_USUL_DIR.exists() else 'غير موجودة'}")
    print(f"• مكتبة نور (جامع الحديث)      : {'متوفرة ومربوطة' if NOOR_HADITH_DIR.exists() else 'غير موجودة'}")
    print(f"• مكتبة نور (جامع الفقه)       : {'متوفرة ومربوطة' if NOOR_FIQH_DIR.exists() else 'غير موجودة'}")
    print(f"• مكتبة أهل البيت (أصول الفقه) : {'متوفرة [978 كتاباً كاملاً]' if (AHLULBAYT_DIR / 'أصول الفقه عند الشيعة').exists() else 'غير موجودة'}")
    print("=" * 65)

def cmd_extract_mujaz(args):
    """استخراج نص المسألة الكامل من كتاب الموجز للشيخ السبحاني بالبحث عن العنوان"""
    target_file = MUJAZ_FULL_FILE if MUJAZ_FULL_FILE.exists() else (NOOR_USUL_DIR / "سبحانی تبریزی، جعفر" / "الموجز في أصول الفقه" / "reading.md")
    if not target_file.exists():
        print(f"خطأ: لم يتم العثور على ملف الموجز في: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    # تقسيم النص بناءً على العناوين والصفحات
    query_norm = normalize_arabic(args.query)
    
    # تقسيم الكتاب إلى أقسام عند كل عنوان يبدأ بـ ### أو ##
    sections = re.split(r'\n(?=###?\s+)', text)
    matches = []

    for sec in sections:
        header = sec.split('\n', 1)[0]
        if query_norm in normalize_arabic(header):
            matches.append(sec)

    if not matches:
        # بحث في أول 300 حرف من القسم إن لم يطابق العنوان المباشر
        for sec in sections:
            if query_norm in normalize_arabic(sec[:300]):
                matches.append(sec)

    if not matches:
        print(f"لم يتم العثور على عنوان يطابق: '{args.query}' في كتاب الموجز.")
        print("أمثلة صالحة للبحث: 'الامر الاول', 'الوضع', 'الدلالة', 'المشتق', 'مادة الامر'.")
        return

    for i, match in enumerate(matches[:args.max]):
        print(f"\n[النتيجة {i+1}]")
        print("=" * 60)
        # إظهار المقطع
        lines = match.strip().split('\n')
        print("\n".join(lines[:args.lines]))
        if len(lines) > args.lines:
            print(f"\n... [تتمة المقطع تحتوي على {len(lines) - args.lines} سطراً إضافياً]")
        print("=" * 60)

def search_files(directory: Path, query: str, file_filter: str = None, max_results: int = 5):
    """دالة بحث سريعة في ملفات الماركداون مع إبراز رقم الصفحة والنص المطابق"""
    if not directory.exists():
        print(f"المسار غير موجود: {directory}")
        return

    query_norm = normalize_arabic(query)
    matched = 0

    files = list(directory.glob("*.md")) if directory.is_dir() else [directory]
    for file_path in files:
        if file_filter and normalize_arabic(file_filter) not in normalize_arabic(file_path.name):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        if query_norm not in normalize_arabic(content):
            continue

        # تقسيم إلى فقرات أو أسطر للعثور على موضع المطابقة
        lines = content.split('\n')
        current_page = "غير محدد"
        for idx, line in enumerate(lines):
            p_match = re.search(r'---\s*\[ج?\s*(\d+)?\s*ص\s*(\d+)\]\s*---|<!--\s*Page:\s*(\d+)\s*-->', line)
            if p_match:
                current_page = p_match.group(2) or p_match.group(3) or "صفحة"
                continue

            if query_norm in normalize_arabic(line):
                matched += 1
                start = max(0, idx - 2)
                end = min(len(lines), idx + 4)
                snippet = "\n".join(lines[start:end]).strip()

                print(f"\n[النتيجة {matched}]")
                print(f"الكتاب: {file_path.name[:65]}... | الصفحة: {current_page}")
                print("-" * 55)
                print(snippet)
                print("=" * 55)

                if matched >= max_results:
                    return

    if matched == 0:
        print(f"لم يتم العثور على نتائج مطابقة لـ: '{query}'.")

def cmd_search(args):
    """البحث في كتب أصول الفقه عند الشيعة"""
    target_dir = AHLULBAYT_DIR / "أصول الفقه عند الشيعة"
    print(f"جاري البحث عن: '{args.query}' في مكتبة أصول الفقه الشيعية...")
    search_files(target_dir, args.query, file_filter=args.author or args.book, max_results=args.max)

def cmd_fiqh_search(args):
    """البحث في كتب الفقه الشيعي وتفاريع الفروع"""
    target_dir = AHLULBAYT_DIR / "فقه الشيعة من القرن الثامن"
    if not target_dir.exists():
        target_dir = AHLULBAYT_DIR / "فقه الشيعة - فتاوى المراجع"
    print(f"جاري البحث عن: '{args.query}' في كتب الفقه الشيعي...")
    search_files(target_dir, args.query, file_filter=args.book, max_results=args.max)

def cmd_hadith_search(args):
    """البحث في كتب الحديث الشريف وقسم الفقه (وسائل الشيعة وغيرها)"""
    target_dir = AHLULBAYT_DIR / "مصادر الحديث الشيعية ـ قسم الفقه"
    print(f"جاري البحث عن: '{args.query}' في مصادر الحديث الشريف...")
    search_files(target_dir, args.query, file_filter=args.book, max_results=args.max)

def cmd_dict_search(args):
    """البحث في كتب ومعاجم المصطلحات الفقهية والأصولية (29 معجماً محلياً)"""
    if not DICT_DIR.exists():
        print(f"خطأ: مسار المعاجم غير موجود: {DICT_DIR}")
        return
    print(f"جاري البحث عن: '{args.query}' في معاجم المصطلحات الفقهية والأصولية...")
    search_files(DICT_DIR, args.query, file_filter=args.book, max_results=args.max)

def cmd_define(args):
    """استعراض تعريف مفصل لمصطلح أصولي أو فقهي من المعجم الشامل أو أمهات المعاجم"""
    term_raw = args.term.strip()
    term_norm = normalize_arabic(term_raw)

    found_in_master = False
    if MASTER_DICT_FILE.exists():
        with open(MASTER_DICT_FILE, 'r', encoding='utf-8', errors='replace') as f:
            m_text = f.read()

        entries = re.split(r'\n(?=###?\s+)', m_text)
        for entry in entries:
            header = entry.split('\n', 1)[0]
            if term_norm in normalize_arabic(header):
                print("=" * 65)
                print(f"         نتيجة من: المعجم الأصولي والفقهي الشامل ({term_raw})")
                print("=" * 65)
                print(entry.strip())
                print("=" * 65)
                found_in_master = True
                break

    if not found_in_master or args.deep:
        if not found_in_master:
            print(f"لم يُعثر على '{term_raw}' في المعجم الشامل، جاري البحث في أمهات المعاجم الحوزوية...")
        else:
            print("\n" + "=" * 65)
            print("[مطابقات إضافية من أمهات المعاجم التخصصية الـ 29]")
            print("=" * 65)
        search_files(DICT_DIR, term_raw, file_filter=args.book, max_results=args.max)

def cmd_create_dossier(args):
    """توليد ملف درس جديد مسبق التجهيز بالقالب الخماسي واقتباس نص الموجز تلقائياً"""
    target_path = BASE_DIR / args.file_path
    if target_path.exists() and not args.force:
        print(f"تنبيه: الملف موجود بالفعل في: {target_path}")
        print("إذا كنت ترغب في استبداله، أعد تشغيل الأمر مع إضافة --force")
        return

    if not TEMPLATE_FILE.exists():
        print(f"خطأ: لم يتم العثور على القالب في: {TEMPLATE_FILE}")
        return

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    title = args.title or target_path.stem.replace('_', ' ')
    content = content.replace("[عنوان الدرس الأصولي]: [اسم المسألة الدقيق]", title)

    # استخراج نص الموجز تلقائياً إن وُجد
    if args.query and MUJAZ_FULL_FILE.exists():
        with open(MUJAZ_FULL_FILE, 'r', encoding='utf-8', errors='replace') as f:
            mujaz_text = f.read()
        query_norm = normalize_arabic(args.query)
        sections = re.split(r'\n(?=###? الامر|###? المقصد|###? الفصل|###? المبحث)', mujaz_text)
        for sec in sections:
            first_lines = "\n".join(sec.split('\n')[:3])
            if query_norm in normalize_arabic(first_lines):
                cleaned = sec.strip()
                content = content.replace("«...»", f"«\n{cleaned}\n»", 1)
                break

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"تم إنشاء ملف الدرس بنجاح في:\n{target_path}")

def main():
    parser = argparse.ArgumentParser(description="أداة المساعد الأصولي الذكي لمكتبات الحوزة")
    subparsers = parser.add_subparsers(dest="command", help="الأوامر المتاحة")

    # info
    subparsers.add_parser("info", help="عرض بيانات المكتبات المتصلة")

    # extract-mujaz
    p_extract = subparsers.add_parser("extract-mujaz", help="استخراج نص من كتاب الموجز للسبحاني")
    p_extract.add_argument("query", help="عنوان المسألة أو الأمر (مثال: 'الامر الاول')")
    p_extract.add_argument("--lines", type=int, default=35, help="عدد الأسطر المعروضة")
    p_extract.add_argument("--max", type=int, default=2, help="عدد النتائج")

    # search
    p_search = subparsers.add_parser("search", help="البحث في كتب أصول الفقه")
    p_search.add_argument("query", help="عبارة البحث")
    p_search.add_argument("--author", help="تصفية باسم المؤلف (مظفر، صدر، سبحاني، خوئي)")
    p_search.add_argument("--book", help="تصفية باسم الكتاب")
    p_search.add_argument("--max", type=int, default=4, help="أقصى عدد للنتائج")

    # hadith-search
    p_hadith = subparsers.add_parser("hadith-search", help="البحث في مصادر الحديث الشريف")
    p_hadith.add_argument("query", help="عبارة البحث في الحديث")
    p_hadith.add_argument("--book", help="اسم الكتاب (وسائل، كافي)")
    p_hadith.add_argument("--max", type=int, default=3, help="أقصى عدد للنتائج")

    # fiqh-search
    p_fiqh = subparsers.add_parser("fiqh-search", help="البحث في كتب الفقه والتفاريع")
    p_fiqh.add_argument("query", help="عبارة البحث في الفقه")
    p_fiqh.add_argument("--book", help="اسم الكتاب (عروة، منهاج)")
    p_fiqh.add_argument("--max", type=int, default=3, help="أقصى عدد للنتائج")

    # dict-search
    p_dict = subparsers.add_parser("dict-search", help="البحث في معاجم المصطلحات الفقهية والأصولية الـ 29")
    p_dict.add_argument("query", help="المصطلح أو العبارة المراد البحث عنها")
    p_dict.add_argument("--book", help="تصفية باسم معجم معين (مشكيني، فتح الله، عجم، عاملي...)")
    p_dict.add_argument("--max", type=int, default=4, help="أقصى عدد للنتائج")

    # define
    p_def = subparsers.add_parser("define", help="استعراض تعريف مصطلح بدقة من المعجم الشامل مع شواهده وتطبيقاته")
    p_def.add_argument("term", help="اسم المصطلح (مثال: الاستنباط، الكر، العوارض الذاتية...)")
    p_def.add_argument("--deep", action="store_true", help="إضافة نتائج موسعة من المعاجم الـ 29")
    p_def.add_argument("--book", help="تصفية البحث الإضافي باسم معجم محدد")
    p_def.add_argument("--max", type=int, default=3, help="أقصى عدد للنتائج الإضافية")

    # create-dossier
    p_create = subparsers.add_parser("create-dossier", help="توليد ملف درس جديد بالقالب خماسي المراحل")
    p_create.add_argument("file_path", help="المسار النسبي (مثال: 00_المقدمة_والمبادئ/02_الوضع.md)")
    p_create.add_argument("--title", help="عنوان المسألة")
    p_create.add_argument("--query", help="عنوان المسألة في الموجز لاقتباسه تلقائياً")
    p_create.add_argument("--force", action="store_true", help="استبدال الملف إن كان موجوداً")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    if args.command == "info":
        cmd_info(args)
    elif args.command == "extract-mujaz":
        cmd_extract_mujaz(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "hadith-search":
        cmd_hadith_search(args)
    elif args.command == "fiqh-search":
        cmd_fiqh_search(args)
    elif args.command == "dict-search":
        cmd_dict_search(args)
    elif args.command == "define":
        cmd_define(args)
    elif args.command == "create-dossier":
        cmd_create_dossier(args)

if __name__ == "__main__":
    main()
