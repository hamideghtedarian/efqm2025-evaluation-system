# ==============================================================
# EFQM Official Report Generator – Persian RTL + Embedded Font + Natural Signature
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
from datetime import datetime
import os, json, base64

print("🚀 Starting EFQM Official Report Generator (Final Embedded Version)...")

# --------------------------------------------------------------
# مسیرهای پایه پروژه
# --------------------------------------------------------------
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
companies_dir = os.path.join(base_dir, "data", "companies")
assets_dir = os.path.join(base_dir, "assets")
output_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------------
# فونت فارسی Base64 جاسازی‌شده (نسخه سبک‌شده Vazirmatn-Regular)
# --------------------------------------------------------------
embedded_font_path = os.path.join(base_dir, "fonts", "EmbeddedVazirmatn.ttf")
if not os.path.exists(embedded_font_path):
    # فونت base64 آماده
    vazirmatn_base64 = b"""
AAEAAAALAIAAAwAwT1MvMlg8sMcAAAC8AAAAYGNtYXAL8fcFAAAEAAAAFGdhc3AAHgAeAAADsAAAAAhnbHlmVtFvXAAAA8gAAABCaGVhZBgqMFEAAAToAAAANmhoZWEFHgNyAAAFIAAAACRobXR4RzqgqQAA...
    """
    with open(embedded_font_path, "wb") as f:
        f.write(base64.b64decode(vazirmatn_base64))
    print("✅ Embedded Vazirmatn font created.")

pdfmetrics.registerFont(TTFont("PersianFont", embedded_font_path))
print("✅ Persian font embedded successfully.")

# --------------------------------------------------------------
# تابع راست‌به‌چپ برای متن فارسی
# --------------------------------------------------------------
def rtl(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def draw_persian(canvas_obj, text, x, y, font_size=12, align="right"):
    txt = rtl(text)
    canvas_obj.setFont("PersianFont", font_size)
    text_width = canvas_obj.stringWidth(txt, "PersianFont", font_size)
    if align == "center":
        canvas_obj.drawCentredString(x, y, txt)
    elif align == "left":
        canvas_obj.drawString(x, y, txt)
    else:
        canvas_obj.drawRightString(x + text_width, y, txt)

# --------------------------------------------------------------
# بارگذاری داده شرکت
# --------------------------------------------------------------
company_file = os.path.join(companies_dir, "beta_petrochemical_co.json")
if not os.path.exists(company_file):
    raise FileNotFoundError("❌ فایل beta_petrochemical_co.json یافت نشد.")
with open(company_file, "r", encoding="utf-8") as f:
    data = json.load(f)

company_name = data.get("organization", "نام شرکت مشخص نیست")
evaluator = data.get("evaluator", "ارزیاب ناشناس")
score = data.get("score", "N/A")
date_str = datetime.now().strftime("%Y/%m/%d")

# --------------------------------------------------------------
# ایجاد PDF
# --------------------------------------------------------------
pdf_path = os.path.join(output_dir, "beta_petrochemical_co_official_feedback.pdf")
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# عنوان و اطلاعات کلی
draw_persian(c, "گزارش رسمی ارزیابی تعالی سازمانی", width/2, height - 3*cm, 16, "center")
draw_persian(c, f"نام شرکت: {company_name}", 3*cm, height - 4.5*cm)
draw_persian(c, f"ارزیاب: {evaluator}", 3*cm, height - 5.2*cm)
draw_persian(c, f"تاریخ گزارش: {date_str}", 3*cm, height - 5.9*cm)
c.line(2*cm, height - 6.5*cm, width - 2*cm, height - 6.5*cm)

# خلاصه گزارش
y = height - 7.5*cm
draw_persian(c, "خلاصه گزارش", 3*cm, y, 14)
y -= 0.8*cm
summary = "این گزارش بر اساس مدل EFQM 2025 تدوین شده و نقاط قوت و فرصت‌های بهبود سازمان را نشان می‌دهد."
draw_persian(c, summary, 3*cm, y)
y -= 1.5*cm

draw_persian(c, "نتایج کلیدی:", 3*cm, y, 14)
y -= 0.8*cm
results = [
    f"امتیاز کل: {score}",
    "سطح بلوغ: پیشرفته",
    "وضعیت: هم‌راستا با اهداف EFQM 2025",
    "گواهی پیشنهادی: EFQM 4-Star"
]
for r in results:
    draw_persian(c, f"• {r}", 4*cm, y)
    y -= 0.6*cm

# خط پایین
c.line(2*cm, 4*cm, width - 2*cm, 4*cm)
draw_persian(c, f"ارزیاب: {evaluator}", 2*cm, 3.4*cm, 10)
draw_persian(c, "ارزیاب ارشد مدل‌های تعالی سازمانی", 2*cm, 2.8*cm, 10)
draw_persian(c, f"تاریخ: {date_str}", 2*cm, 2.2*cm, 10)

# امضا
signature_file = os.path.join(assets_dir, "signature.png")
if os.path.exists(signature_file):
    c.drawImage(ImageReader(signature_file), width - 6*cm, 2.3*cm, 3.5*cm, 1.2*cm, mask='auto')
    print("✍️ Signature added (natural).")
else:
    draw_persian(c, "(محل امضا)", width - 3*cm, 2.3*cm, 10)

# ذخیره
c.showPage()
c.save()
print(f"✅ Report generated successfully!\n📄 {pdf_path}")
