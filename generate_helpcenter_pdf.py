from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from bidi.algorithm import get_display
import arabic_reshaper
import os

# مسیر پایه پروژه
base_dir = os.path.dirname(os.path.abspath(__file__))

# مسیر فونت فارسی
font_path = os.path.join(base_dir, "fonts", "Vazirmatn.ttf")

# ثبت فونت فارسی
pdfmetrics.registerFont(TTFont("Vazirmatn", font_path))
farsi_font = "Vazirmatn"

# مسیر فایل‌ها
output_path = os.path.join(base_dir, "help", "EFQM2025_HelpCenter_Official.pdf")
banner_path = os.path.join(base_dir, "help", "banner.png")
logo_path = os.path.join(base_dir, "help", "logo_gray.png")
signature_path = os.path.join(base_dir, "help", "signature-template.png")

# تنظیم سند
doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=50, leftMargin=50,
                        topMargin=60, bottomMargin=60)

# استایل‌ها
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MyTitle', fontName=farsi_font, fontSize=18, alignment=2, spaceAfter=20, rightIndent=0))
styles.add(ParagraphStyle(name='MySubTitle', fontName=farsi_font, fontSize=13, alignment=2, textColor=colors.gray))
styles.add(ParagraphStyle(name='MyPersian', fontName=farsi_font, fontSize=12, alignment=2, leading=20))
styles.add(ParagraphStyle(name='MyEnglish', fontName='Helvetica', fontSize=10, leading=14, alignment=0, textColor=colors.darkgray))

# تابع
