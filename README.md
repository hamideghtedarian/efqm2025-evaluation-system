# EFQM 2025 Assessment Repository

این مخزن برای مدیریت داده‌های ارزیابی سازمان‌ها بر اساس مدل **EFQM 2025** طراحی شده است.  
ساختار داده‌ها بر پایه منطق **RADAR** شامل چهار مؤلفه Approach، Deployment، Assessment و Refinement می‌باشد.  

## 📁 ساختار پوشه‌ها
efqm2025-assessment/
├── README.md
├── schema/
│   └── efqm2025-schema.json
├── data/
│   ├── criteria/
│   │   └── efqm2025.json
│   └── companies/
│       └── example-company.json
├── forms/
│   └── radar-form.html
└── scripts/
    └── evaluate.py


## ⚙️ نحوه استفاده
1. فایل‌های `criteria` را تغییر ندهید مگر برای بروزرسانی رسمی مدل EFQM.
2. برای هر شرکت جدید، یک فایل JSON در مسیر `data/companies/` با ساختار نمونه ایجاد کنید.
3. ارزیاب‌ها داده‌ها را در فرم HTML یا به‌صورت مستقیم در JSON وارد می‌کنند.
4. برای تجمیع و محاسبه امتیازات، از اسکریپت `scripts/evaluate.py` استفاده کنید.

## 📜 مجوز
MIT License — استفاده و توسعه آزاد است با ذکر منبع.

