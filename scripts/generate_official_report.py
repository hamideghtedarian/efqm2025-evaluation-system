# ==============================================================
# EFQM Official Report Generator – Persian RTL + Signature
# ==============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import arabic_reshaper
from bidi.algorithm import get_display

import os, json
from datetime import datetime

print("🚀 Starting EFQM Official Report Generator (Persian RTL)...")

# --------------------------------------------------------------
# مسیر پایه پروژه
# --------------------------------------------------------------
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

companies_dir = os.path.join(base_dir, "data", "companies")
fonts_dir = os.path.join(base_dir, "fonts")
signature_file = os.path.join(base_dir, "assets", "signature.png")
output_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------------
# ثبت فونت فارسی (Vazirmatn)
# --------------------------------------------------------------
try:
    pdfmetrics.registerFont(TTFont("Vazirmatn", os.path.join(fonts_dir, "Vazirmatn-Regular.ttf")))
    # اگر Bold ندارید، این خط را می‌توانید کامنت کنید
    pdfmetrics.registerFont(TTFont("Vazirmatn-Bold", os.path.join(fonts_dir, "Vazirmatn-Bold.ttf")))
    print("✅ Persian font Vazirmatn registered.")
except Exception as e:
    print("⚠️ Font registration failed:", e)

# --------------------------------------------------------------
# تابع کمکی برای اصلاح و راست‌به‌چپ کردن متن فارسی
# --------------------------------------------------------------
def rtl(text: str) -> str:
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

# --------------------------------------------------------------
# بارگذاری داده‌های شرکت بتا
# --------------------------------------------------------------
company_file = os.path.join(companies_dir, "beta_petrochemical_co.json")
if not os.path.exists(company_file):
    raise FileNotFoundError("❌ فایل beta_petrochemical_co.json در data/companies پیدا نشد.")

with open(company_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", "نام شرکت مشخص نیست")
evaluator = company_data.get("evaluator", "ارزیاب ناشناس")
date_str = datetime.now().strftime("%Y-%m-%d")

# --------------------------------------------------------------
# مسیر خروجی PDF
# --------------------------------------------------------------
pdf_filename = "beta_petrochemical_co_official_feedback.pdf"
pdf_path = os.path.join(output_dir, pdf_filename)
print(f"📄 Generating PDF: {pdf_path}")

c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# --------------------------------------------------------------
# عنوان و اطلاعات کلی (همه با rtl)
# --------------------------------------------------------------
# عنوان
try:
    c.setFont("Vazirmatn-Bold", 16)
except:
    c.setFont("Vazirmatn", 16)

c.drawCentredString(width / 2, height - 3 * cm, rtl("گزارش رسمی ارزیابی تعالی سازمانی"))

# اطلاعات شرکت
c.setFont("Vazirmatn", 12)
c.drawCentredString(width / 2, height - 4 * cm, rtl(f"نام شرکت: {company_name}"))
c.drawCentredString(width / 2, height - 4.8 * cm, rtl(f"ارزیاب: {evaluator}"))
c.drawCentredString(width / 2, height - 5.6 * cm, rtl(f"تاریخ گزارش: {date_str}"))

c.line(2 * cm, height - 6.2 * cm, width - 2 * cm, height - 6.2 * cm)

# --------------------------------------------------------------
# درج امضا با اندازه طبیعی‌تر
# --------------------------------------------------------------
signature_width = 4 * cm   # عرض حدود ۴ سانتی‌متر
signature_height = 1.5 * cm   # ارتفاع متناسب

if os.path.exists(signature_file):
    c.drawImage(
        ImageReader(signature_file),
        width - (signature_width + 3 * cm),  # کمی فاصله از راست
        2 * cm,                              # فاصله از پایین
        signature_width,
        signature_height,
        mask='auto'
    )
    print("✍️ Signature added at natural scale.")
else:
    print("⚠️ Signature file not found at:", signature_file)

# --------------------------------------------------------------
# اطلاعات ارزیاب در کنار امضا (همه با rtl)
# --------------------------------------------------------------
c.setFont("Vazirmatn", 10)
c.drawString(2 * cm, 3 * cm, rtl(f"ارزیاب: {evaluator}"))
c.drawString(2 * cm, 2.4 * cm, rtl("ارزیاب ارشد مدل‌های تعالی سازمانی"))
c.drawString(2 * cm, 1.8 * cm, rtl(f"تاریخ: {date_str}"))

# --------------------------------------------------------------
# پایان و ذخیره
# --------------------------------------------------------------
c.showPage()
c.save()

print("✅ Report generated successfully!")
print(f"📁 Saved at: {pdf_path}")
