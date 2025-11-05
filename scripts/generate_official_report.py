from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os, json
from datetime import datetime

# مسیرهای پایه
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
companies_dir = os.path.join(base_dir, "data", "companies")
signature_file = os.path.join(base_dir, "assets", "signature.png")
output_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(output_dir, exist_ok=True)

# جستجوی خودکار اولین فایل شرکت
company_files = [f for f in os.listdir(companies_dir) if f.endswith(".json")]
if not company_files:
    raise FileNotFoundError("❌ هیچ فایل شرکتی در مسیر data/companies یافت نشد.")

first_company = company_files[0]
data_file = os.path.join(companies_dir, first_company)

# بارگذاری داده شرکت
with open(data_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", os.path.splitext(first_company)[0])
evaluator = company_data.get("evaluator", "Unknown Evaluator")
date_str = datetime.now().strftime("%Y-%m-%d")

# ایجاد فایل PDF خروجی
pdf_filename = f"{company_name.replace(' ', '_')}_feedback_official.pdf"
pdf_path = os.path.join
