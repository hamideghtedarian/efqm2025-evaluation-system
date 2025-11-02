import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from zipfile import ZipFile

# مسیر اصلی پروژه
base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(base_dir)  # رفتن به ریشه پروژه

# مسیر داده‌ها (پوشه‌های فارسی)
companies_dir = os.path.join(base_dir, "data", "کمپانی")
criteria_file = os.path.join(base_dir, "data", "معیارها", "efqm2025.json")

# مسیر خروجی
reports_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(reports_dir, exist_ok=True)

# ثبت فونت فارسی (برای جلوگیری از حروف جدا)
fonts_dir = os.path.join(base_dir, "fonts")
font_path = os.path.join(fonts_dir, "Vazirmatn.ttf")

if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("Vazirmatn", font_path))
    font_name = "Vazirmatn"
else:
    font_name = "Helvetica"

# بارگذاری معیارها
with open(criteria_file, "r", encoding="utf-8") as f:
    criteria_data = json.load(f)

# ساخت گزارش برای هر شرکت
for filename in os.listdir(companies_dir):
    if filename.endswith(".json"):
        company_path = os.path.join(companies_dir, filename)
        with open(company_path, "r", encoding="utf-8") as f:
            company_data = json.load(f)

        org_name = company_data.get("organization", "نامشخص")
        evaluator = company_data.get("evaluator", "ارزیاب نامشخص")
        date = company_data.get("date", datetime.now().strftime("%Y-%m-%d"))

        # مسیر PDF خروجی
        pdf_filename = f"{org_name}_feedback.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)

        # ایجاد PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        c.setFont(font_name, 14)
        c.drawString(100, height - 80, f"گزارش بازخورد مدل EFQM 2025")
        c.setFont(font_name, 12)
        c.drawString(100, height - 110, f"نام سازمان: {org_name}")
        c.drawString(100, height - 130, f"ارزیاب: {evaluator}")
        c.drawString(100, height - 150, f"تاریخ ارزیابی: {date}")
        c.line(100, height - 160, 480, height - 160)

        y = height - 190
        c.setFont(font_name, 11)

        # چاپ معیارها و زیرمعیارها
        for criterion in criteria_data.get("criteria", []):
            c.drawString(80, y, f"معیار {criterion['id']}: {criterion['title']}")
            y -= 20

            for sub in criterion.get("subcriteria", []):
                text = f"   زیرمعیار {sub['id']}: {sub['title']}"
                c.drawString(100, y, text)
                y -= 15
                if y < 100:
                    c.showPage()
                    c.setFont(font_name, 11)
                    y = height - 80

        c.showPage()
        c.setFont(font_name, 10)
        c.drawString(100, height - 100, "© گزارش تولیدشده به‌صورت خودکار توسط سیستم ارزیابی EFQM2025")
        c.save()

        print(f"✅ گزارش برای {org_name} ایجاد شد: {pdf_filename}")

# ایجاد فایل ZIP نهایی
zip_name = f"EFQM2025_Assessment_Pack_{datetime.now().strftime('%Y%m%d')}.zip"
zip_path = os.path.join(base_dir, "reports", zip_name)

with ZipFile(zip_path, "w") as zipf:
    for file in os.listdir(reports_dir):
        if file.endswith(".pdf"):
            zipf.write(os.path.join(reports_dir, file),
                       arcname=f"company_reports/{file}")

print(f"\n📦 بسته نهایی ایجاد شد: {zip_path}")
print("🎉 عملیات با موفقیت پایان یافت.")
