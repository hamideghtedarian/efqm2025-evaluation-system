# ============================================================
# EFQM 2025 Auto Normalizer for Company Data Structures
# Author: A. Eghtedarian & GPT-5
# Description:
#   Scans all folders and files in data/companies
#   Automatically standardizes their names, creates missing
#   JSON files (company, assessment, strengths, opportunities),
#   and builds attachments folders for all.
# ============================================================

import os
import json
import re

print("🚀 Starting EFQM 2025 Auto Normalizer...")

# --- مسیر پایه
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
companies_dir = os.path.join(base_dir, "data", "companies")
os.makedirs(companies_dir, exist_ok=True)

# --- تابع نرمال‌سازی نام‌ها
def normalize_name(name: str) -> str:
    name = name.strip().replace(" ", "_").replace("-", "_")
    name = re.sub(r"[^\w_]", "", name)  # حذف حروف خاص
    return name.lower()

# --- ساخت فایل JSON پایه
def create_json_if_missing(folder, filename, content):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print(f"📝 Created: {filename}")

# --- ساختار استاندارد هر شرکت
def ensure_company_structure(company_name):
    norm_name =
