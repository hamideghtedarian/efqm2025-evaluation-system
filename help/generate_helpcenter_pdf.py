from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os

# تنظیم مسیر اجرای کد
os.chdir(os.path.dirname(__file__))

# مسیر خروجی
output_path = "help/EFQM2025_HelpCenter_Official.pdf"

# مسیر تصاویر محلی
banner_path = "help/banner.png"
logo_path = "help/logo_gray.png"
signature_path = "help/signature-template.png"

# ساخت سند PDF
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=50, leftMargin=50,
                        topMargin=60, bottomMargin=60)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Persian', fontName='Helvetica', fontSize=12, leading=20, alignment=4))
styles.add(ParagraphStyle(name='MyTitle', fontName='Helvetica-Bold', fontSize=18, leading=24, alignment=1, spaceAfter=20))
styles.add(ParagraphStyle(name='SubTitle', fontName='Helvetica', fontSize=13, leading=18, alignment=1, textColor=colors.gray))
styles.add(ParagraphStyle(name='English', fontName='Helvetica', fontSize=10, leading=14, alignment=1, textColor=colors.darkgray))

content = []

# بنر بالا
try:
    content.append(Image(ImageReader(banner_path), width=480, height=120))
except Exception as e:
    print("⚠️ بنر بارگذاری نشد:", e)
content.append(Spacer(1, 20))

# عنوان اصلی
content.append(Paragraph("راهنمای رسمی سامانه ارزیابی EFQM 2025", styles['MyTitle']))
content.append(Paragraph("تهیه و تنظیم: عبدالحمید اقتداریان – ارزیاب ارشد مدل تعالی EFQM", styles['SubTitle']))
content.append(Spacer(1, 20))

# متن فارسی
text_fa = """
این سند برای راهنمایی ارزیابان و مدیران تدوین شده است تا فرآیند ارزیابی بر اساس مدل تعالی EFQM 2025 را 
به‌صورت ساخت‌یافته، مستند و هم‌راستا با منطق RADAR انجام دهند. تمامی بخش‌ها شامل معیارها، زیرمعیارها، 
شواهد و تحلیل‌های RADAR در سامانه طراحی شده‌اند.
"""
content.append(Paragraph(text_fa, styles['Persian']))
content.append(Spacer(1, 20))

# متن انگلیسی
text_en = """
This document is prepared to guide assessors and managers in performing evaluations based on the EFQM 2025 Model 
using a structured approach aligned with the RADAR logic. All components including criteria, sub-criteria, evidence, 
and improvement actions are embedded within the system.
"""
content.append(Paragraph(text_en, styles['English']))
content.append(Spacer(1, 30))

# لوگو پایین صفحه
try:
    content.append(Image(ImageReader(logo_path), width=120, height=40))
except Exception as e:
    print("⚠️ لوگو بارگذاری نشد:", e)
content.append(Spacer(1, 40))

# امضا
content.append(Paragraph("عبدالحمید اقتداریان", styles['Persian']))
try:
    content.append(Image(ImageReader(signature_path), width=180, height=60))
except Exception as e:
    print("⚠️ امضا بارگذاری نشد:", e)
content.append(Spacer(1, 10))
content.append(Paragraph("© 2025 hamideghtedarian | EFQM2025 Evaluation System", styles['English']))

try:
    doc.build(content)
    print("✅ فایل PDF رسمی با موفقیت ساخته شد:", output_path)
except Exception as e:
    print("❌ خطا در ساخت PDF:", e)
