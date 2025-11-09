import os, json
from datetime import datetime

# مسیرهای پایه
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
companies_dir = os.path.join(base_dir, "data", "companies")
assets_dir = os.path.join(base_dir, "assets")
output_dir = os.path.join(base_dir, "reports", "company_reports")
os.makedirs(output_dir, exist_ok=True)

# فایل داده شرکت (بتا)
company_file = os.path.join(companies_dir, "beta_petrochemical_co.json")
if not os.path.exists(company_file):
    raise FileNotFoundError("beta_petrochemical_co.json در data/companies پیدا نشد.")

with open(company_file, "r", encoding="utf-8") as f:
    data = json.load(f)

company_name = data.get("organization", "نام شرکت مشخص نیست")
evaluator = data.get("evaluator", "ارزیاب ناشناس")
score = data.get("score", "N/A")
evaluation_date = data.get("evaluation_date", "")
today = datetime.now().strftime("%Y/%m/%d")

# مسیر امضا (نسبی برای HTML)
signature_rel = "../assets/signature.png"

html_path = os.path.join(output_dir, "beta_petrochemical_co_official_feedback.html")

html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <title>گزارش رسمی ارزیابی تعالی سازمانی - {company_name}</title>
  <style>
    @font-face {{
      font-family: 'Vazirmatn';
      src: local('Vazirmatn'), url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;600&display=swap');
    }}
    body {{
      font-family: 'Vazirmatn', sans-serif;
      direction: rtl;
      text-align: right;
      margin: 40px;
      background: #f7f7f7;
    }}
    .report-container {{
      background: #ffffff;
      padding: 30px 40px;
      border-radius: 12px;
      box-shadow: 0 0 10px rgba(0,0,0,0.06);
      max-width: 900px;
      margin: 0 auto;
    }}
    h1, h2, h3 {{
      margin: 0 0 12px 0;
    }}
    h1 {{
      font-size: 22px;
      text-align: center;
      margin-bottom: 24px;
    }}
    .meta {{
      font-size: 14px;
      margin-bottom: 16px;
      line-height: 1.8;
    }}
    .section-title {{
      font-size: 16px;
      margin-top: 24px;
      margin-bottom: 8px;
      font-weight: 600;
      border-right: 4px solid #444;
      padding-right: 8px;
    }}
    .bullet {{
      margin-right: 16px;
      font-size: 14px;
      line-height: 1.8;
    }}
    .divider {{
      border-top: 1px solid #ccc;
      margin: 24px 0;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-top: 32px;
    }}
    .footer-info {{
      font-size: 13px;
      line-height: 1.7;
    }}
    .signature-box {{
      text-align: left;
    }}
    .signature-box img {{
      width: 140px;
      height: auto;
      display: block;
      margin-bottom: 4px;
    }}
    .signature-label {{
      font-size: 12px;
      color: #555;
    }}
  </style>
</head>
<body>
  <div class="report-container">
    <h1>گزارش رسمی ارزیابی تعالی سازمانی</h1>

    <div class="meta">
      <div><strong>نام شرکت:</strong> {company_name}</div>
      <div><strong>ارزیاب:</strong> {evaluator}</div>
      <div><strong>تاریخ گزارش:</strong> {today}</div>
      {"<div><strong>تاریخ ارزیابی:</strong> " + evaluation_date + "</div>" if evaluation_date else ""}
      <div><strong>امتیاز کل:</strong> {score}</div>
    </div>

    <div class="divider"></div>

    <div class="section-title">خلاصه گزارش</div>
    <p class="bullet">
      این گزارش بر اساس مدل EFQM 2025 تهیه شده و تصویری کل‌نگر از نقاط قوت و فرصت‌های بهبود
      سازمان فراهم می‌آورد. تحلیل‌ها بر پایه منطق RADAR و تیم ارزیابی خبره انجام شده است.
    </p>

    <div class="section-title">نتایج کلیدی</div>
    <p class="bullet">• امتیاز کل سازمان: {score}</p>
    <p class="bullet">• سطح بلوغ: پیشرفته</p>
    <p class="bullet">• وضعیت: هم‌راستا با اهداف راهبردی و ذی‌نفعان کلیدی</p>
    <p class="bullet">• پیشنهاد: حرکت به سمت اخذ تقدیرنامه سطح بالاتر EFQM در چرخه بعدی</p>

    <div class="section-title">جمع‌بندی</div>
    <p class="bullet">
      با توجه به نتایج حاصل‌شده، سازمان از پایه‌های محکمی در حوزه‌های رهبری،
      جهت‌گیری استراتژیک و نتایج کلیدی برخوردار است. توصیه می‌شود تمرکز ویژه‌ای
      بر توسعه نوآوری سیستماتیک، دیجیتال‌سازی فرآیندها و مشارکت فعال‌تر ذی‌نفعان
      در طراحی آینده سازمان صورت گیرد.
    </p>

    <div class="divider"></div>

    <div class="footer">
      <div class="footer-info">
        <div><strong>ارزیاب:</strong> {evaluator}</div>
        <div>ارزیاب ارشد مدل‌های تعالی سازمانی</div>
        <div>تاریخ: {today}</div>
      </div>
      <div class="signature-box">
        <img src="{signature_rel}" alt="امضا" />
        <div class="signature-label">امضا و تأیید ارزیاب</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTML report generated successfully:")
print("📄", html_path)
