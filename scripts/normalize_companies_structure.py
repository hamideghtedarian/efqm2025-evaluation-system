# ==============================================================
# EFQM Data Normalizer for Company Structure
# Author: Dr. Abdulhamid Eghtedarian
# Date: 2025-11-12
# ==============================================================

import os
import json
import re
import shutil

print("🚀 Starting EFQM Company Structure Normalizer...")

# مسیر پایه مخزن
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
companies_dir = os.path.join(base_dir, "data", "companies")

# اطمینان از وجود مسیر
if not os.path.exists(companies_dir):
    print("❌ پوشه data/companies وجود ندارد.")
    exit(1)

# تابع ساخت شناسه استاندارد شرکت (slug)
def normalize_slug(name):
    if not name:
        return "unknown_company"
    # حروف فارسی و انگلیسی و عدد را نگه می‌داریم
    name = re.sub(r"[^\w\s\u0600-\u06FF]", "", name)
    name = name.strip().replace(" ", "_").replace("ـ", "_")
    return name.lower()

# ساختار استاندارد EFQM برای هر شرکت
def build_structure(company_slug, source_file):
    company_dir = os.path.join(companies_dir, company_slug)
    os.makedirs(company_dir, exist_ok=True)

    # مسیرهای استاندارد
    company_json = os.path.join(company_dir, "company.json")
    assessment_json = os.path.join(company_dir, "assessment.json")
    strengths_json = os.path.join(company_dir, "strengths.json")
    opportunities_json = os.path.join(company_dir, "opportunities.json")
    attachments_dir = os.path.join(company_dir, "attachments")

    os.makedirs(attachments_dir, exist_ok=True)

    # انتقال یا کپی فایل اصلی
    if os.path.isfile(source_file):
        shutil.copy2(source_file, company_json)

    # ایجاد فایل‌های پایه اگر وجود ندارند
    if not os.path.exists(assessment_json):
        with open(assessment_json, "w", encoding="utf-8") as f:
            json.dump({"criteria": []}, f, ensure_ascii=False, indent=2)

    if not os.path.exists(strengths_json):
        with open(strengths_json, "w", encoding="utf-8") as f:
            json.dump({"strengths": []}, f, ensure_ascii=False, indent=2)

    if not os.path.exists(opportunities_json):
        with open(opportunities_json, "w", encoding="utf-8") as f:
            json.dump({"opportunities": []}, f, ensure_ascii=False, indent=2)

    print(f"✅ ساختار استاندارد برای شرکت '{company_slug}' ایجاد شد.")
    return company_dir

# پردازش تمام فایل‌ها و پوشه‌ها در companies
for item in os.listdir(companies_dir):
    path = os.path.join(companies_dir, item)

    # اگر فایل JSON است
    if os.path.isfile(path) and item.endswith(".json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            company_name = data.get("organization", item.replace(".json", ""))
            slug = normalize_slug(company_name)
            new_dir = build_structure(slug, path)
            print(f"➡ انتقال {item} به {new_dir}")
        except Exception as e:
            print(f"⚠️ خطا در پردازش {item}: {e}")

    # اگر پوشه است و نیاز به استانداردسازی دارد
    elif os.path.isdir(path):
        slug = normalize_slug(item)
        if slug != item:
            new_path = os.path.join(companies_dir, slug)
            shutil.move(path, new_path)
            print(f"🔄 تغییر نام پوشه: {item} → {slug}")

print("\n🎯 عملیات نرمال‌سازی ساختار شرکت‌ها با موفقیت پایان یافت.")
