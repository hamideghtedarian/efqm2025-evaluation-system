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
# مسیر پایه پروژه (حتماً در اولین خط‌ها)
# --------------------------------------------------------------
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --------------------------------------------------------------
# مسیرها
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
# پیدا کردن فایل شرکت
# --------------------------------------------------------------
company_files = [f for f in os.listdir(companies_dir) if f.endswith(".json")]
if not company_files:
    raise FileNotFoundError("❌ هیچ فایل شرکتی در مسیر data/companies یافت نشد.")

data_file = os.path.join(companies_dir, company_files[0])
with open(data_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", "نام شرکت مشخص نیست")
evaluator = company_data.get("evaluator", "ارزیاب ناشناس")
date_str = datetime.now().strftime("%Y-%m-%d")

# --------------------------------------------------------------
# خروجی PDF
# --------------------------------------------------------------
pdf_filename = f"{company_name.replace(' ', '_')}_official_feedback.pdf"
pdf_path = os.path.join(output_dir, pdf_filename)

c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# --------------------------------------------------------------
# سرصفحه و اطلاعات اصلی
# --------------------------------------------------------------
c.setFont("Vazirmatn-Bold", 16)
c.drawCentredString(width/2, height - 3*cm, "گزارش رسمی ارزیابی تعالی سازمانی")

c.setFont("Vazirmatn", 12)
c.drawCentredString(width/2, height - 4*cm, f"نام شرکت: {company_name}")
c.drawCentredString(width/2, height - 4.8*cm, f"ارزیاب: {evaluator}")
c.drawCentredString(width/2, height - 5.6*cm, f"تاریخ گزارش: {date_str}")
c.line(2*cm, height - 6.2*cm, width - 2*cm, height - 6.2*cm)

# --------------------------------------------------------------
# درج امضا
# --------------------------------------------------------------
if os.path.exists(signature_file):
    c.drawImage(ImageReader(signature_file), width - 8*cm, 2*cm, 5*cm, 2*cm, mask='auto')
    print("✍️ Signature added.")
else:
    print("⚠️ Signature file not found.")

# --------------------------------------------------------------
# اطلاعات امضا
# --------------------------------------------------------------
c.setFont("Vazirmatn", 10)
c.drawString(2*cm, 3*cm, f"ارزیاب: {evaluator}")
c.drawString(2*cm, 2.4*cm, "ارزیاب ارشد مدل‌های تعالی سازمانی")
c.drawString(2*cm, 1.8*cm, f"تاریخ: {date_str}")

c.showPage()
c.save()

print("✅ Report generated successfully!")
print(f"📄 File saved at: {pdf_path}")
