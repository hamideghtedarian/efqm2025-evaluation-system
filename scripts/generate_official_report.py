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
print(f"🔍 Using company file: {data_file}")

# بارگذاری داده شرکت
with open(data_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", os.path.splitext(first_company)[0])
evaluator = company_data.get("evaluator", "Unknown Evaluator")
date_str = datetime.now().strftime("%Y-%m-%d")

# ایجاد فایل PDF خروجی
pdf_filename = f"{company_name.replace(' ', '_')}_feedback_official.pdf"
pdf_path = os.path.join(output_dir, pdf_filename)
print(f"📄 Generating PDF: {pdf_path}")

c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# عنوان گزارش
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2, height - 3 * cm, "Organizational Excellence Assessment Report")

c.setFont("Helvetica", 12)
c.drawCentredString(width / 2, height - 4 * cm, f"Company: {company_name}")
c.drawCentredString(width / 2, height - 4.7 * cm, f"Evaluator: {evaluator}")
c.drawCentredString(width / 2, height - 5.4 * cm, f"Date: {date_str}")
c.line(2 * cm, height - 6 * cm, width - 2 * cm, height - 6 * cm)

# درج امضا در گوشه پایین راست
signature_width = 5 * cm  # ۵ سانتی‌متر
signature_height = 2.2 * cm
print(f"🔍 Searching for signature at: {signature_file}")

try:
    signature_img = ImageReader(signature_file)
    c.drawImage(
        signature_img,
        width - (signature_width + 3 * cm),
        2 * cm,
        signature_width,
        signature_height,
        mask='auto'
    )
    print("✅ Signature loaded successfully.")
except Exception as e:
    print("⚠️ Error while loading signature:", e)

# اطلاعات ارزیاب کنار امضا
c.setFont("Helvetica", 10)
c.drawString(2 * cm, 3 * cm, f"Evaluated by: {evaluator}")
c.drawString(2 * cm, 2.4 * cm, "Senior Assessor – Organizational Excellence Models")
c.drawString(2 * cm, 1.8 * cm, f"Date: {date_str}")

# فوتر خاکستری
c.setFont("Helvetica-Oblique", 8)
c.setFillGray(0.4)
c.drawCentredString(width / 2, 1 * cm, "© Hamid Eghtedarian Brand | All Rights Reserved")

c.showPage()
c.save()

print(f"✅ PDF generated successfully: {pdf_path}")
