from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# 🧠 تنظیم فونت فارسی (HeiseiMin برای ژاپنی/فارسی مناسب است)
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# مسیر فایل خروجی
output_path = "help/EFQM2025_HelpCenter_Official.pdf"

# مسیر تصاویر
banner_path = "help/banner.png"
logo_path = "help/logo_gray.png"
signature_path = "help/signature-template.png"

# تنظیم صفحه
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=50, leftMargin=50, topMargin=60, bottomMargin=60)

# سبک‌ها
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Persian', fontName='HeiseiMin-W3', fontSize=12, leading=20, rightIndent=0, alignment=4))
styles.add(ParagraphStyle(name='Title', fontName='HeiseiMin-W3', fontSize=18, leading=24, alignment=1, spaceAfter=20))
styles.add(ParagraphStyle(name='SubTitle', fontName='HeiseiMin-W3', fontSize=14, leading=20, alignment=1, textColor=colors.gray))
styles.add(ParagraphStyle(name='English', fontName='HeiseiMin-W3', fontSize=10, leading=14, alignment=1, textColor=colors.darkgray))

content = []

# بنر بالا
content.append(Image(banner_path, width=480, height=120))
content.append(Spacer(1, 20))

# عنوان فارسی
content.append(Paragraph("راهنمای رسمی سامانه ارزیابی EFQM 2025", styles['Title']))
content.append(Paragraph("تهیه و تنظیم: عبدالحمید اقتداریان – ارزیاب ارشد مدل تعالی EFQM", styles['SubTitle']))
content.append(Spacer(1, 20))

# توضیح فارسی
text_fa = """
این سند برای راهنمایی ارزیابان و مدیران تدوین شده است تا فرآیند ارزیابی بر اساس مدل تعالی EFQM 2025 را به‌صورت ساخت‌یافته، 
مستند و هم‌راستا با منطق RADAR انجام دهند. تمامی بخش‌ها شامل معیارها، زیرمعیارها، شواهد و تحلیل‌های RADAR در سامانه طراحی شده‌اند.
"""
content.append(Paragraph(text_fa, styles['Persian']))
content.append(Spacer(1, 20))

# English section
text_en = """
This document is prepared to guide assessors and managers in performing evaluations based on the EFQM 2025 Model 
using a structured approach aligned with the RADAR logic. All components including criteria, sub-criteria, evidence, 
and improvement actions are embedded within the system.
"""
content.append(Paragraph(text_en, styles['English']))
content.append(Spacer(1, 30))

# بنر پایین
content.append(Image(logo_path, width=120, height=40))
content.append(Spacer(1, 40))

# امضا
content.append(Paragraph("عبدالحمید اقتداریان", styles['Persian']))
content.append(Image(signature_path, width=180, height=60))
content.append(Spacer(1, 10))
content.append(Paragraph("© 2025 hamideghtedarian | EFQM2025 Evaluation System", styles['English']))

# ساخت PDF
doc.build(content)
print("✅ فایل PDF رسمی با موفقیت تولید شد:", output_path)
