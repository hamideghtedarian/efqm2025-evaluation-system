from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm

# 🔹 ثبت فونت فارسی برای پشتیبانی کامل متون
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# 📄 مسیر خروجی فایل PDF
output_path = "help/EFQM2025_HelpCenter_Official.pdf"

# 📘 ایجاد سند
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=2*cm, leftMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)

# ✨ استایل‌ها
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleFa', fontName='HeiseiMin-W3', alignment=TA_CENTER, fontSize=16, leading=22))
styles.add(ParagraphStyle(name='BodyFa', fontName='HeiseiMin-W3', alignment=TA_RIGHT, fontSize=12, leading=18))
styles.add(ParagraphStyle(name='BodyEn', alignment=TA_LEFT, fontSize=11, leading=16))

story = []

# 🏛 جلد رسمی
story.append(Image("help/banner.png", width=16*cm, height=3*cm))
story.append(Spacer(1, 20))
story.append(Paragraph("سامانه ارزیابی EFQM 2025", styles['TitleFa']))
story.append(Paragraph("EFQM 2025 Evaluation System – Help & Guidance", styles['BodyEn']))
story.append(Spacer(1, 12))
story.append(Paragraph("عبدالحمید اقتداریان – ارزیاب ارشد و مشاور مدل تعالی EFQM", styles['BodyFa']))
story.append(Paragraph("October 2025", styles['BodyEn']))
story.append(PageBreak())

# 📘 چکیده مدیریتی
story.append(Paragraph("چکیده مدیریتی", styles['TitleFa']))
story.append(Paragraph(
    "هدف این سند، ارائه‌ی راهنمای جامع برای ارزیابان و مدیران سازمان‌ها بر اساس مدل تعالی EFQM 2025 است.",
    styles['BodyFa']))
story.append(Paragraph(
    "This document provides comprehensive guidance for assessors and managers based on the EFQM 2025 Excellence Model.",
    styles['BodyEn']))
story.append(PageBreak())

# 📙 فصل ۱
story.append(Paragraph("فصل ۱: مدل EFQM 2025 و منطق RADAR", styles['TitleFa']))
story.append(Paragraph(
    "مدل EFQM 2025 شامل سه بُعد اصلی است: جهت‌گیری (Direction)، اجرا (Execution) و نتایج (Results).",
    styles['BodyFa']))
story.append(Paragraph(
    "The EFQM 2025 Model includes three main dimensions: Direction, Execution, and Results.",
    styles['BodyEn']))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "منطق RADAR چهار محور اصلی دارد: Results, Approach, Deployment, Assessment & Refinement.",
    styles['BodyFa']))
story.append(PageBreak())

# 📗 فصل ۲
story.append(Paragraph("فصل ۲: راهنمای استفاده از سامانه ارزیابی", styles['TitleFa']))
story.append(Paragraph(
    "این سامانه شامل پنج ماژول است: ارزیابی، هم‌راستایی، اولویت پروژه‌ها، داشبورد و داشبورد مدیریتی.",
    styles['BodyFa']))
story.append(Paragraph(
    "This system consists of five modules: Criteria, Alignment, Priority, Dashboard, and Dashboard Master.",
    styles['BodyEn']))
story.append(PageBreak())

# 📕 فصل ۳
story.append(Paragraph("فصل ۳: توصیه‌های تخصصی برای ارزیابان", styles['TitleFa']))
story.append(Paragraph(
    "ارزیابان باید ضمن تحلیل شواهد و نتایج، نقاط قوت و فرصت‌های بهبود را با منطق RADAR ثبت کنند.",
    styles['BodyFa']))
story.append(Paragraph(
    "Assessors should record strengths and opportunities for improvement following the RADAR logic.",
    styles['BodyEn']))
story.append(PageBreak())

# ✍️ صفحه امضا
story.append(Spacer(1, 40))
story.append(Image("help/signature-template.png", width=14*cm, height=4*cm))
story.append(Spacer(1, 20))
story.append(Paragraph("For official EFQM 2025 evaluation documentation", styles['BodyEn']))
story.append(Paragraph("Inspired by the EFQM Model 2025", styles['BodyEn']))

# ✅ ساخت فایل نهایی
doc.build(story)
print("✅ فایل رسمی EFQM2025_HelpCenter_Official.pdf با موفقیت ایجاد شد.")
