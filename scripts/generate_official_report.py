# ==============================================================
# EFQM Official Report Generator (Persian + English)
# Author: Dr. Abdulhamid Eghtedarian
# ==============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, json
from datetime import datetime

print("🚀 Starting EFQM Official Report Generator...")

# --------------------------------------------------------------
# مسیر پایه پروژه (تعریف قبل از هر چیز)
# --------------------------------------------------------------
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --------------------------------------------------------------
# مسیرهای مهم
# --------------------------------------------------------------
companies_dir = os.path.join(base_dir, "data", "companies")
fonts_dir = os.path.join(base_dir, "fonts")
signature_file = os.path.join(base_dir, "assets", "signature.png")
output_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------------
# ثبت فونت فارسی Vazirmatn
# --------------------------------------------------------------
try:
    pdfmetrics.registerFont(TTFont("Vazirmatn", os.path.join(fonts_dir, "Vazirmatn-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Vazirmatn-Bold", os.path.join(fonts_dir, "Vazirmatn-Bold.ttf")))
    print("✅ Persian fonts registered successfully.")
except Exception as e:
    print("⚠️ Font registration failed:", e)

# --------------------------------------------------------------
# یافتن فایل شرکت
# --------------------------------------------------------------
company_files = [f for f in os.listdir(companies_dir) if f.endswith(".json")]
if not company_files:
    raise FileNotFoundError("❌ هیچ فایل شرکتی در مسیر data/companies یافت نشد.")

first_company = company_files[0]
data_file = os.path.join(companies_dir, first_company)
print(f"🧾 Using company file: {data_file}")

# --------------------------------------------------------------
# بارگذاری داده شرکت
# --------------------------------------------------------------
with open(data_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", os.path.splitext(first_company)[0])
evaluator = company_data.get("evaluator", "ارزیاب ناشناس")
date_str = datetime.now().strftime("%Y-%m-%d")

# --------------------------------------------------------------
# مسیر خروجی PDF
# --------------------------------------------------------------
pdf_filename = f"{company_name.replace(' ', '_')}_feedback_official.pdf"
pdf_path = os.path.join(output_dir, pdf_filename)
print(f"📄 Generating PDF: {pdf_path}")

# --------------------------------------------------------------
# ایجاد فایل PDF
# --------------------------------------------------------------
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# --------------------------------------------------------------
# سرصفحه گزارش
# --------------------------------------------------------------
c.setFont("Vazirmatn-Bold", 16)
c.drawCentredString(width / 2, height - 3 * cm, "گزارش رسمی ارزیابی تعالی سازمانی")

c.setFont("Vazirmatn", 12)
c.drawCentredString(width / 2, height - 4 * cm, f"نام شرکت: {company_name}")
c.drawCentredString(width / 2, height - 4.8 * cm, f"ارزیاب: {evaluator}")
c.drawCentredString(width / 2, height - 5.6 * cm, f"تاریخ گزارش: {date_str}")

c.line(2 * cm, height - 6.2 * cm, width - 2 * cm, height - 6.2 * cm)

# --------------------------------------------------------------
# درج امضا در پایین صفحه
# --------------------------------------------------------------
signature_width = 5 * cm
signature_height = 2 * cm
print(f"🔍
