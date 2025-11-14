# ============================================================
# EFQM 2025 SMART AUTO NORMALIZER (v2)
# Author: Dr. A. Eghtedarian
# Description:
#   Automatically detects all company folders (Persian/English)
#   Standardizes names and creates full EFQM2025 structure.
# ============================================================

import os, json, re, shutil

print("🚀 Starting EFQM 2025 Smart Auto Normalizer v2 ...")

# مسیر پایه پروژه
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
companies_dir = os.path.join(base_dir, "data", "companies")
os.makedirs(companies_dir, exist_ok=True)

# تابع نرمال‌سازی نام (فارسی یا انگلیسی)
def normalize_name(name: str) -> str:
    name = name.strip().replace(" ", "_").replace("-", "_").replace("ـ", "_")
    name = re.sub(r"[^\w\u0600-\u06FF_]", "", name)
    name = re.sub(r"_+", "_", name)
    return name.lower()

# ساخت فایل JSON پایه اگر وجود ندارد
def ensure_json(folder, filename, content):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print(f"📝 Created: {filename} in {os.path.basename(folder)}")

# تابع ایجاد ساختار EFQM برای هر شرکت
def build_company_structure(src_path, name):
    norm = normalize_name(name)
    dest_dir = os.path.join(companies_dir, norm)
    if not os.path.exists(dest_dir):
        shutil.move(src_path, dest_dir)
        print(f"✅ Moved & normalized: {name} → {norm}")
    else:
        print(f"🔄 Folder {norm} already exists, merging...")

    # ایجاد فایل‌ها
    ensure_json(dest_dir, "company.json", {"organization": name})
    ensure_json(dest_dir, "assessment.json", {"criteria": []})
    ensure_json(dest_dir, "strengths.json", {"strengths": []})
    ensure_json(dest_dir, "opportunities.json", {"opportunities": []})

    # ایجاد پوشه attachments
    att = os.path.join(dest_dir, "attachments")
    os.makedirs(att, exist_ok=True)
    print(f"📁 Attachments folder ensured for {norm}")

# اسکن همه پوشه‌ها و فایل‌ها در companies
for item in os.listdir(companies_dir):
    path = os.path.join(companies_dir, item)
    if os.path.isdir(path):
        build_company_structure(path, item)
    elif os.path.isfile(path) and item.endswith(".json"):
        # اگر فایل تکی JSON باشد
        name = item.replace(".json", "")
        new_folder = os.path.join(companies_dir, normalize_name(name))
        os.makedirs(new_folder, exist_ok=True)
        shutil.move(path, os.path.join(new_folder, "company.json"))
        print(f"✅ Moved {item} → {new_folder}")
        build_company_structure(new_folder, name)

print("\n🎯 Smart normalization completed successfully!")
