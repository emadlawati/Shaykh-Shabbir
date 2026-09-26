# -*- coding: utf-8 -*-
"""
Build Book Database for Authentic Hawzawi Book Reader & Lessons
Extracts structured pages, headers, and footnotes from Markdown files
in AhlulBayt Library and outputs offline JS/JSON bundles.
Now includes both Mutaqaddimin (Mufid, Murtada, Tusi) and Muta'akhkhirin/Mu'asirin.
"""

import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_LIB = r"C:\Imad Works\OpenCode\Urwa Extraction\output\AhlulBayt Library\أصول الفقه عند الشيعة"
OUT_DIR = r"C:\Imad Works\OpenCode\Shaykh Shabbir\Usul\Resources\books_data"

os.makedirs(OUT_DIR, exist_ok=True)

BOOK_CONFIGS = [
    # --- تأسيسات المتقدمين (المدرسة البغدادية - القرن الرابع والخامس الهجري) ---
    {
        "id": "mufid_tadhkirah",
        "title": "التذكرة بأصول الفقه",
        "author": "الشيخ المفيد (ت 413 هـ)",
        "school": "المدرسة البغدادية التأسيسية",
        "era": "المتقدمون (القرن الخامس)",
        "file": "التذكرة بأصول الفقه - الشيخ المفيد - دار المفيد للطباعة والنشر والتوزيع.md",
        "vol": 1
    },
    {
        "id": "murtada_dhariyah_1",
        "title": "الذريعة إلى أصول الشريعة (ج 1)",
        "author": "السيد المرتضى علم الهدى (ت 436 هـ)",
        "school": "المدرسة العقلانية القطعية (رفض الآحاد والتمسك بالإجماع والقطع)",
        "era": "المتقدمون (القرن الخامس)",
        "file": "الذريعة إلى أصول الشريعة - الشريف المرتضى - دانشگاه تهران ، مؤسسه انتشارات و چا - ج 01 - 1.md",
        "vol": 1
    },
    {
        "id": "tusi_uddah_1",
        "title": "العدة في أصول الفقه (ج 1)",
        "author": "شيخ الطائفة أبو جعفر الطوسي (ت 460 هـ)",
        "school": "مدرسة جامع الأصول (تأسيس حجية خبر الثقة والجمع المنهجي)",
        "era": "المتقدمون (القرن الخامس)",
        "file": "العدة في أصول الفقه ( عدة الأصول ) ( ط . ق ) - الشيخ الطوسي - مؤسسة آل البيت ( ع ) للطباعة والنشر - ج 01 - 1.md",
        "vol": 1
    },
    # --- تحقيقات المتأخرين والمعاصرين (مدرسة النجف وقم) ---
    {
        "id": "mujaz_subhani",
        "title": "الموجز في أصول الفقه",
        "author": "الشيخ جعفر السبحاني",
        "school": "المدرسة التبسيطية التعليمية المعاصرة",
        "era": "المعاصرون",
        "file": "الموجز في أصول الفقه - الشيخ جعفر السبحاني - موسسه الامام الصادق ( ع ) - قم - ج 01 - 1.md",
        "vol": 1
    },
    {
        "id": "usul_muzaffar_1",
        "title": "أصول الفقه (ج 1)",
        "author": "الشيخ محمد رضا المظفر",
        "school": "مدرسة النجف المنهجية (مدرسة المحقق الأصفهاني)",
        "era": "القرن الرابع عشر الهجري",
        "file": "أصول الفقه - الشيخ محمد رضا المظفر - مؤسسة النشر الإسلامي التابعة لجماعة - ج 01 - 1.md",
        "vol": 1
    },
    {
        "id": "usul_muzaffar_2",
        "title": "أصول الفقه (ج 2)",
        "author": "الشيخ محمد رضا المظفر",
        "school": "مدرسة النجف المنهجية",
        "era": "القرن الرابع عشر الهجري",
        "file": "أصول الفقه - الشيخ محمد رضا المظفر - مؤسسة النشر الإسلامي التابعة لجماعة - ج 02 - 2.md",
        "vol": 2
    },
    {
        "id": "kifayah_akhund",
        "title": "كفاية الأصول",
        "author": "المحقق الآخوند الخراساني",
        "school": "أم المدارس الأصولية الحديثة (مدرسة الآخوند)",
        "era": "مجدد علم الأصول الحديث",
        "file": "كفاية الأصول - الآخوند الخراساني - مؤسسة آل البيت ( ع ) لإحياء التراث.md",
        "vol": 1
    },
    {
        "id": "khoei_muhadarat_1",
        "title": "محاضرات في أصول الفقه (ج 1)",
        "author": "السيد أبو القاسم الخوئي (تقرير الفياض)",
        "school": "مدرسة التحقيق والتدقيق النجفية (المدرسة الخوئية)",
        "era": "زعيم الحوزة العلمية",
        "file": "محاضرات في أصول الفقه تقرير أبحاث السيد أبو القاسم الخوئي - الشيخ محمد إسحاق الفياض - مؤسسة النشر الإسلامي التابعة لجماعة - ج 01 - 1.md",
        "vol": 1
    },
    {
        "id": "sadr_halaqat_1",
        "title": "دروس في علم الأصول (الحلقة الأولى)",
        "author": "الشهيد السيد محمد باقر الصدر",
        "school": "المدرسة الأصولية التجديدية (مدرسة الشهيد الصدر)",
        "era": "فيلسوف ومجدد الأصول",
        "file": "دروس في علم الأصول - السيد محمد باقر الصدر - دار الكتاب اللبناني - بيروت - لبنان - ج 01 - 1.md",
        "vol": 1
    },
    {
        "id": "sistani_rafid",
        "title": "الرافد في علم الأصول",
        "author": "السيد علي السيستاني (تقرير القطيفي)",
        "school": "المدرسة التاريخية التحليلية المقارنة",
        "era": "المرجعية المعاصرة",
        "file": "الرافد في علم الأصول ، محاضرات آية الله العظمى السيد علي الحسيني - السيد منير السيد عدنان القطيفي - مكتب آية الله العظمى السيد السيستان.md",
        "vol": 1
    }
]

def parse_markdown_book(config):
    filepath = os.path.join(BASE_LIB, config["file"])
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return None
        
    print(f"Parsing: {config['title']} ...")
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Extract frontmatter metadata
    meta = {}
    m_meta = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if m_meta:
        for line in m_meta.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip(' "\'')

    # Extract Table of Contents from text if present
    toc = []
    toc_match = re.search(r"##\s*فهرس الموضوعات\s*\n(.*?)(?=\n##|\n---|\Z)", text, re.DOTALL)
    if toc_match:
        toc_text = toc_match.group(1)
        for t_line in toc_text.splitlines():
            m_item = re.search(r"[-*•]?\s*(.*?)\s*\(\s*ص\s*(\d+)\s*\)", t_line)
            if m_item:
                t_title = m_item.group(1).strip()
                t_page = int(m_item.group(2))
                if t_title and not t_title.startswith("وفيها"):
                    toc.append({"title": t_title, "page": t_page})

    # Find all page markers: [ج 1 ص 49] or [ص 49]
    page_matches = list(re.finditer(r"\[\s*(?:ج\s*(\d+)\s*)?ص\s*(\d+)\s*\]", text))
    pages = {}
    current_header = ""

    for i in range(len(page_matches)):
        m = page_matches[i]
        p_num = int(m.group(2))
        start_idx = m.end()
        end_idx = page_matches[i+1].start() if i+1 < len(page_matches) else len(text)
        raw_content = text[start_idx:end_idx].strip()
        
        # Clean leading/trailing boundary lines
        raw_content = re.sub(r"^-+\s*", "", raw_content).strip()
        raw_content = re.sub(r"\s*-+$", "", raw_content).strip()
        
        lines = raw_content.splitlines()
        body_lines = []
        fn_lines = []
        in_fn = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("### "):
                current_header = stripped.replace("### ", "").strip()
                continue
            elif stripped.startswith("## "):
                current_header = stripped.replace("## ", "").strip()
                continue
                
            if re.match(r"^\(\s*\d+\s*\)", stripped) or re.match(r"^\[\s*\d+\s*\]", stripped):
                in_fn = True
                
            if in_fn:
                fn_lines.append(stripped)
            else:
                body_lines.append(line)
                
        body = "\n".join(body_lines).strip()
        footnotes = "\n".join(fn_lines).strip()
        
        pages[str(p_num)] = {
            "page": p_num,
            "header": current_header,
            "body": body,
            "footnotes": footnotes
        }

    # If TOC was empty, build it from recorded headers
    if not toc:
        seen_headers = set()
        for p_str, p_data in sorted(pages.items(), key=lambda x: int(x[0])):
            h = p_data["header"]
            if h and h not in seen_headers and len(h) < 60:
                toc.append({"title": h, "page": int(p_str)})
                seen_headers.add(h)

    result = {
        "id": config["id"],
        "title": config["title"],
        "author": config["author"],
        "school": config["school"],
        "era": config["era"],
        "volume": config["vol"],
        "totalPages": len(pages),
        "minPage": min(int(k) for k in pages.keys()) if pages else 0,
        "maxPage": max(int(k) for k in pages.keys()) if pages else 0,
        "toc": toc[:50],
        "pages": pages
    }
    return result

def main():
    all_books = {}
    catalog = []
    
    for config in BOOK_CONFIGS:
        b_data = parse_markdown_book(config)
        if b_data:
            all_books[b_data["id"]] = b_data
            catalog.append({
                "id": b_data["id"],
                "title": b_data["title"],
                "author": b_data["author"],
                "school": b_data["school"],
                "era": b_data["era"],
                "volume": b_data["volume"],
                "totalPages": b_data["totalPages"],
                "minPage": b_data["minPage"],
                "maxPage": b_data["maxPage"],
                "toc": b_data["toc"]
            })
            
            out_single = os.path.join(OUT_DIR, f"{b_data['id']}.json")
            with open(out_single, "w", encoding="utf-8") as f:
                json.dump(b_data, f, ensure_ascii=False, indent=2)
            print(f"  -> Saved {out_single} ({b_data['totalPages']} pages)")

    catalog_path = os.path.join(OUT_DIR, "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"\nSaved catalog to {catalog_path}")

    js_bundle_path = os.path.join(OUT_DIR, "books_db.js")
    with open(js_bundle_path, "w", encoding="utf-8") as f:
        f.write("/* Offline Hawzawi Book Database - Auto-Generated */\n")
        f.write("window.HAWZA_CATALOG = " + json.dumps(catalog, ensure_ascii=False) + ";\n")
        f.write("window.HAWZA_BOOKS = " + json.dumps(all_books, ensure_ascii=False) + ";\n")
    print(f"Saved complete offline JS bundle to {js_bundle_path} ({os.path.getsize(js_bundle_path) / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    main()
