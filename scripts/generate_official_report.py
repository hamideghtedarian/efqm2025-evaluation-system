import os, json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# ثبت فونت‌های فارسی
fonts_dir = os.path.join(base_dir, "fonts")
pdfmetrics.registerFont(TTFont("Vazirmatn", os.path.join(fonts_dir, "Vazirmatn-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Vazirmatn-Bold", os.path.join(fonts_dir, "Vazirmatn-Bold.ttf")))

print("🚀 Script started...")

try:
    # مسیر پایه پروژه
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("📂 Base directory:", base_dir)

    companies_dir = os.path.join(base_dir, "data", "companies")
    signature_file = os.path.join(base_dir, "assets", "signature.png")
    output_dir = os.path.join(base_dir, "reports", "company_reports")
    os.makedirs(output_dir, exist_ok=True)
    print("📁 Folders checked/created.")

    # جستجوی فایل شرکت
    company_files = [f for f in os.listdir(companies_dir) if f.endswith(".json")]
    if not company_files:
        raise FileNotFoundError("❌ هیچ فایل JSON در data/companies پیدا نشد.")

    first_company = company_files[0]
    data_file = os.path.join(companies_dir, first_company)
    print("🧾 Company file found:", data_file)

    # بارگذاری داده
    with open(data_file, "r", encoding="utf-8") as f:
        company_data = json.load(f)

    company_name = company_data.get("organization", os.path.splitext(first_company)[0])
    evaluator = company_data.get("evaluator", "Unknown Evaluator")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # مسیر خروجی PDF
    pdf_filename = f"{company_name.replace(' ', '_')}_feedback_official.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    print("📄 Output file:", pdf_path)

    # ایجاد گزارش PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Vazirmatn-Bold", 16)
    c.drawCentredString(width / 2, height - 3 * cm, "Organizational Excellence Assessment Report")

    c.setFont("Vazirmatn", 12)
    c.drawCentredString(width / 2, height - 4 * cm, f"Company: {company_name}")
    c.drawCentredString(width / 2, height - 4.7 * cm, f"Evaluator: {evaluator}")
    c.drawCentredString(width / 2, height - 5.4 * cm, f"Date: {date_str}")

    c.line(2 * cm, height - 6 * cm, width - 2 * cm, height - 6 * cm)
    print("🖋 Header drawn.")

    # درج امضا
    print("🔍 Searching for signature:", signature_file)
    if os.path.exists(signature_file):
        c.drawImage(ImageReader(signature_file), width - 8 * cm, 2 * cm, 5 * cm, 2.2 * cm, mask='auto')
        print("✅ Signature added.")
    else:
        print("⚠️ Signature not found!")

    # اطلاعات ارزیاب
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, 3 * cm, f"Evaluated by: {evaluator}")
    c.drawString(2 * cm, 2.4 * cm, "Senior Assessor – Organizational Excellence Models")
    c.drawString(2 * cm, 1.8 * cm, f"Date: {date_str}")

    c.showPage()
    c.save()
    print(f"✅ PDF successfully generated at: {pdf_path}")

except Exception as e:
    print("💥 Error occurred:", e)
