from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os, json
from datetime import datetime

# مسیرهای پایه
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(base_dir, "data", "companies", "beta_petrochemical_co.json")
signature_file = os.path.join(base_dir, "assets", "signature.png")
output_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(output_dir, exist_ok=True)

# بارگذاری داده شرکت
with open(data_file, "r", encoding="utf-8") as f:
    company_data = json.load(f)

company_name = company_data.get("organization", "Unknown Company")
evaluator = company_data.get("evaluator", "Unknown Evaluator")
date_str = datetime.now().strftime("%Y-%m-%d")

# ایجاد PDF
pdf_path = os.path.join(output_dir, f"{company_name.replace(' ', '_')}_feedback_official.pdf")
c = canvas.Canvas(pdf_path, pagesize=A4)

# اندازه صفحه
width, height = A4

# عنوان گزارش
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2, height - 3 * cm, "Organizational Excellence Assessment Report")

c.setFont("Helvetica", 12)
c.drawCentredString(width / 2, height - 4 * cm, f"Company: {company_name}")
c.drawCentredString(width / 2, height - 4.7 * cm, f"Evaluator: {evaluator}")
c.drawCentredString(width / 2, height - 5.4 * cm, f"Date: {date_str}")

# خط افقی
c.line(2 * cm, height - 6 * cm, width - 2 * cm, height - 6 * cm)

# بخش امضا و اطلاعات ارزیاب در پایین صفحه
signature_width = 5 * cm  # ۵ سانتی‌متر عرض امضا
signature_height = 2.2 * cm

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
except Exception as e:
    print("⚠️ Signature not found or unreadable:", e)

# اطلاعات ارزیاب کنار امضا
c.setFont("Helvetica", 10)
c.drawString(2 * cm, 3 * cm, f"Evaluated by: {evaluator}")
c.drawString(2 * cm, 2.4 * cm, "Senior Assessor – Organizational Excellence Models")
c.drawString(2 * cm, 1.8 * cm, f"Date: {date_str}")

# امضا و فوتر
c.setFont("Helvetica-Oblique", 8)
c.setFillGray(0.4)
c.drawCentredString(width / 2, 1 * cm, "© Hamid Eghtedarian Brand | All Rights Reserved")

c.showPage()
c.save()

print(f"✅ Official report generated successfully: {pdf_path}")
