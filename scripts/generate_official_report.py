# ==============================================================
# EFQM Official Report Generator – Persian RTL + Natural Signature
# Author: Dr. Abdulhamid Eghtedarian
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
# مسیرهای پایه پروژه
# --------------------------------------------------------------
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
companies_dir = os.path.join(base_dir, "data", "companies")
fonts_dir = os.path.join(base_dir, "fonts")
assets_dir = os.path.join(base_dir, "assets")
output_dir = os.path.join(base_dir, "reports", "company_reports")

os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------------
# ثبت فونت فارسی (Vazirmatn یا XB Zar)
# --------------------------------------------------------------
fonts_registered = False
try:
    font_path = os.path.join(fonts_dir, "XBZar.ttf")
    if not os.path.exists(font_path):
        font_path = os.path.join(fonts_dir, "Vazirmatn-Regular.ttf")
    pdfmetrics.registerFont(TTFont("PersianFont", font_path))
    fonts_registered = True
    print(f"✅ Persian font registered: {os.path.basename(font_path)}")
except Exception as e:
    print("⚠️ Font registration failed:", e)

# --------------------------------------------------------------
# توابع کمکی
# --------------------------------------------------------------
def rtl(text):
    """بازسازی و راست‌چین‌سازی متن فارسی"""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def draw_persian_text(canvas_obj, text, x, y, font_size=12, align="right"):
    """نوشتن متن فارسی با جهت راست‌به‌چپ و تنظیم چینش"""
    text_rtl = rtl(text)
    canvas_obj.setFont("PersianFont", font_size)
    text_width = canvas_obj.stringWidth(text_rtl, "PersianFont", font_size)
    if align == "center":
        canvas_obj.drawCentredString(x, y, text_rtl)
    elif align == "left":
        canvas_obj.drawString(x, y, text_rtl)
    else:  # align = right
        canvas_obj.drawRightString(x + text_width, y, text_rtl)

# --------------------------------------------------------------
# بارگذاری داده‌های شرکت (beta petrochemical co)
# --------------------------------------------------------------
company_file = os.path.join(companies_dir, "beta_petrochemical_co.json")
if not os.path.exists(company_file):
    raise FileNotFoundError("❌ فایل beta_petrochemical_co.json یافت نشد.")

with open(company_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", "نام شرکت مشخص نیست")
evaluator = company_data.get("evaluator", "ارزیاب ناشناس")
date_str = datetime.now().strftime("%Y/%m/%d")
score = company_data.get("score", "N/A")

# --------------------------------------------------------------
# مسیر خروجی PDF
# --------------------------------------------------------------
pdf_filename = "beta_petrochemical_co_official_feedback.pdf"
pdf_path = os.path.join(output_dir, pdf_filename)
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# --------------------------------------------------------------
# بخش عنوان و اطلاعات
# --------------------------------------------------------------
draw_persian_text(c, "گزارش رسمی ارزیابی تعالی سازمانی", width/2, height - 3*cm, 16, align="center")
draw_persian_text(c, f"نام شرکت: {company_name}", 3*cm, height - 4.5*cm, 12)
draw_persian_text(c, f"ارزیاب: {evaluator}", 3*cm, height - 5.2*cm, 12)
draw_persian_text(c, f"تاریخ گزارش: {date_str}", 3*cm, height - 5.9*cm, 12)
c.line(2*cm, height - 6.5*cm, width - 2*cm, height - 6.5*cm)

# --------------------------------------------------------------
# خلاصه گزارش و نتایج
# --------------------------------------------------------------
y_pos = height - 7.5*cm
draw_persian_text(c, "خلاصه گزارش", 3*cm, y_pos, 14)
y_pos -= 0.8*cm

summary = "این گزارش بر اساس مدل EFQM 2025 تهیه شده و شامل نقاط قوت، فرصت‌های بهبود و امتیاز نهایی سازمان است."
draw_persian_text(c, summary, 3*cm, y_pos, 12)
y_pos -= 1.5*cm

draw_persian_text(c, "نتایج کلیدی:", 3*cm, y_pos, 14)
y_pos -= 0.8*cm

results = [
    f"امتیاز کل: {score}",
    "سطح بلوغ: پیشرفته",
    "وضعیت: هم‌راستا با اهداف راهبردی EFQM 2025",
    "گواهی پیشنهادی: EFQM 4-Star"
]

for result in results:
    draw_persian_text(c, f"• {result}", 4*cm, y_pos, 12)
    y_pos -= 0.7*cm

# --------------------------------------------------------------
# بخش امضا و اطلاعات ارزیاب
# --------------------------------------------------------------
c.line(2*cm, 4*cm, width - 2*cm, 4*cm)
draw_persian_text(c, f"ارزیاب: {evaluator}", 2*cm, 3.5*cm, 10)
draw_persian_text(c, "ارزیاب ارشد مدل‌های تعالی سازمانی", 2*cm, 2.9*cm, 10)
draw_persian_text(c, f"تاریخ: {date_str}", 2*cm, 2.3*cm, 10)

# درج امضا با مقیاس طبیعی‌تر
signature_file = os.path.join(assets_dir, "signature.png")
if os.path.exists(signature_file):
    c.drawImage(ImageReader(signature_file), width - 6*cm, 2.3*cm, 3.5*cm, 1.2*cm, mask='auto')
    print("✍️ Signature added successfully.")
else:
    print("⚠️ Signature not found.")
    draw_persian_text(c, "(امضا)", width - 3*cm, 2.5*cm, 10)

# --------------------------------------------------------------
# پایان و ذخیره فایل
# --------------------------------------------------------------
c.showPage()
c.save()

print("✅ Report generated successfully!")
print(f"📁 File saved at: {pdf_path}")
