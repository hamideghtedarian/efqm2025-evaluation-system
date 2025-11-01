from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os

# مسیر پایه پروژه
base_dir = os.path.dirname(os.path.abspath(__file__))

# مسیر فونت فارسی
font_path = os.path.join(base_dir, "fonts", "Vazirmatn.ttf")

# ثبت فونت با جاسازی کامل در PDF
try:
    pdfmetrics.registerFont(TTFont("Vazirmatn", font_path, subfontIndex=0))
    farsi_font = "Vazirmatn"
    print("✅ فونت فارسی Vazirmatn با موفقیت ثبت و جاسازی شد.")
except Exception as e:
    print("⚠️ خطا در ثبت فونت فارسی:", e)
    farsi_font = "Helvetica"

# مسیر فایل‌ها
output_path = os.path.join(base_dir, "help", "EFQM2025_HelpCenter_Official.pdf")
banner_path = os.path.join(base_dir, "help", "banner.png")
logo_path = os.path.join(base_dir, "help", "logo_gray.png")
signature_path = os.path.join(base_dir, "help", "signature-template.png")

# تنظیم سند
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=50, leftMargin=50,
                        topMargin=60, bottomMargin=60)

# تعریف استایل‌ها
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MyTitle', fontName=farsi_font, fontSize=18, alignment=1, spaceAfter=20))
styles.add(ParagraphStyle(name='MySubTitle', fontName=farsi_font, fontSize=13, alignment=1, textColor=colors.gray))
styles.add(ParagraphStyle(name='MyPersian', fontName=farsi_font, fontSize=12, alignment=2, leading=20))
styles.add(ParagraphStyle(name='MyEnglish', fontName='Helvetica', fontSize=10, leading=14, alignment=1, textColor=colors.darkgray))

content = []

# بنر بالا
if os.path.exists(banner_path):
    content.append(Image(ImageReader(banner_path), width=480, height=120))
content.append(Spacer(1, 20))

# عنوان
content.append(Paragraph("راهنمای رسمی سامانه ارزیابی EFQM 2025", styles['MyTitle']))
content.append(Paragraph("تهیه و تنظیم: عبدالحمید اقتداریان – ارزیاب ارشد مدل تعالی EFQM", styles['MySubTitle']))
content.append(Spacer(1, 20))

# متن فارسی
text_fa = """
این سند جهت راهنمایی ارزیابان و مدیران طراحی شده تا ارزیابی‌های مبتنی بر مدل تعالی EFQM 2025 را 
به صورت ساخت‌یافته و منطبق با منطق RADAR انجام دهند. کلیه معیارها، زیرمعیارها و شواهد در سامانه قابل ثبت و پیگیری است.
"""
content.append(Paragraph(text_fa, styles['MyPersian']))
content.append(Spacer(1, 20))

# متن انگلیسی
text_en = """
This document provides structured guidance for assessors and managers performing EFQM 2025 evaluations, 
aligned with the RADAR logic. All criteria, sub-criteria, and evidence are managed within the system.
"""
content.append(Paragraph(text_en, styles['MyEnglish']))
content.append(Spacer(1, 30))

# لوگو و امضا
if os.path.exists(logo_path):
    content.append(Image(ImageReader(logo_path), width=120, height=40))
content.append(Spacer(1, 30))

content.append(Paragraph("عبدالحمید اقتداریان", styles['MyPersian']))
if os.path.exists(signature_path):
    content.append(Image(ImageReader(signature_path), width=180, height=60))
content.append(Spacer(1, 10))

content.append(Paragraph("© 2025 hamideghtedarian | EFQM2025 Evaluation System", styles['MyEnglish']))

# ساخت PDF
doc.build(content)
print("✅ فایل PDF نهایی با پشتیبانی کامل از فارسی ساخته شد:", output_path)
