import json
import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import arabic_reshaper
from bidi.algorithm import get_display

# اضافه کردن مسیر اصلی پروژه برای import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from persian_pdf import PersianPDF

def load_company_data(company_name):
    """بارگذاری داده‌های شرکت"""
    company_path = f"data/companies/{company_name}.json"
    if os.path.exists(company_path):
        with open(company_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def create_feedback_pdf(company_data, output_path):
    """ایجاد PDF بازخورد"""
    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        
        # ایجاد نمونه PersianPDF
        persian_pdf = PersianPDF()
        
        # هدر
        c.setFillColorRGB(0.2, 0.4, 0.6)
        c.rect(0, height-100, width, 100, fill=1)
        
        c.setFillColorRGB(1, 1, 1)
        
        # استفاده از PersianPDF برای متن فارسی
        company_name_fa = company_data.get('name_fa', 'شرکت')
        persian_pdf.draw_persian_text(c, f"گزارش ارزیابی {company_name_fa}", 50, height-50, 16)
        persian_pdf.draw_persian_text(c, "چارچوب EFQM 2025", 50, height-70, 12)
        
        # محتوای اصلی
        c.setFillColorRGB(0, 0, 0)
        y_position = height - 150
        
        # بخش‌های مختلف
        sections = [
            ("نقاط قوت", company_data.get('strengths', [])),
            ("فرصت‌های بهبود", company_data.get('improvements', [])),
            ("پیشنهادات", company_data.get('recommendations', []))
        ]
        
        for section_title, items in sections:
            if items:
                persian_pdf.draw_persian_text(c, section_title, 50, y_position, 14)
                y_position -= 30
                
                for item in items:
                    if y_position < 100:
                        c.showPage()
                        y_position = height - 100
                        persian_pdf = PersianPDF()  # ایجاد مجدد برای صفحه جدید
                    
                    persian_pdf.draw_persian_text(c, f"• {item}", 70, y_position, 10)
                    y_position -= 20
        
        c.save()
        print(f"✅ PDF ایجاد شد: {output_path}")
        
    except Exception as e:
        print(f"❌ خطا در ایجاد PDF: {e}")

def main():
    """تابع اصلی"""
    companies = [
        "alfa petrochemical co",
        "beta petrochmical co", 
        "شرکت پتروشیمی الفا",
        "شرکت پتروشیمی بتا"
    ]
    
    # ایجاد پوشه خروجی
    os.makedirs("reports/company_reports", exist_ok=True)
    
    for company in companies:
        print(f"📊 در حال پردازش: {company}")
        company_data = load_company_data(company)
        
        if company_data:
            # نام فایل خروجی
            if any('\u0600' <= char <= '\u06FF' for char in company):
                output_name = f"{company}_feedback.pdf"
            else:
                output_name = f"{company}_feedback.pdf"
            
            output_path = f"reports/company_reports/{output_name}"
            create_feedback_pdf(company_data, output_path)
        else:
            print(f"⚠️ داده‌ای برای {company} یافت نشد")

if __name__ == "__main__":
    main()
