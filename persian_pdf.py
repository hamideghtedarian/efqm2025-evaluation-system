cd /workspace/your-project
cat > persian_pdf.py << 'EOF'
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

class PersianPDF:
    def __init__(self):
        self.setup_fonts()
    
    def setup_fonts(self):
        """تنظیم فونت‌های فارسی"""
        font_paths = [
            '/usr/share/fonts/truetype/vazir/Vazir.ttf',
            '/usr/share/fonts/truetype/Vazir.ttf',
            './fonts/Vazir.ttf',
            'Vazir.ttf',
            '/workspace/fonts/Vazir.ttf'
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('Vazir', font_path))
                    self.font_name = 'Vazir'
                    print(f"✅ فونت فارسی بارگذاری شد: {font_path}")
                    return
                except Exception as e:
                    print(f"❌ خطا در بارگذاری فونت {font_path}: {e}")
                    continue
        
        self.font_name = 'Helvetica'
        print("⚠️ فونت فارسی یافت نشد، از Helvetica استفاده می‌شود")
    
    def format_persian_text(self, text):
        """فرمت کردن متن فارسی"""
        if text and any('\u0600' <= char <= '\u06FF' for char in str(text)):
            try:
                reshaped_text = arabic_reshaper.reshape(str(text))
                bidi_text = get_display(reshaped_text)
                return bidi_text
            except Exception as e:
                print(f"خطا در فرمت متن فارسی: {e}")
                return str(text)
        return str(text)
    
    def draw_persian_text(self, canvas, text, x, y, font_size=12):
        """رسم متن فارسی در PDF"""
        formatted_text = self.format_persian_text(text)
        canvas.setFont(self.font_name, font_size)
        canvas.drawString(x, y, formatted_text)

# تست
if __name__ == "__main__":
    pdf = PersianPDF()
    test_text = "سلام این یک تست فارسی است"
    print(f"فونت فعال: {pdf.font_name}")
    print(f"تست متن: {pdf.format_persian_text(test_text)}")
EOF
