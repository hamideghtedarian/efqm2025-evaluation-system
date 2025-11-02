#!/usr/bin/env python3
"""
Generate PDF feedback reports for all companies in data/companies/
and pack them into a ZIP file under reports/.

Requirements (install once in Codespaces / local):
pip install reportlab arabic_reshaper python-bidi

Place:
- fonts/Vazirmatn.ttf
- help/banner.png (or ./help/banner.png)
- help/logo_gray.png
- help/signature-template.png

Run:
python scripts/generate_company_reports.py
"""
import os
import json
import zipfile
from datetime import datetime
from pathlib import Path
import re

# PDF libs
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# RTL libs
import arabic_reshaper
from bidi.algorithm import get_display

# ------------------ Configuration ------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # repo root
COMPANIES_DIR = BASE_DIR / "data" / "companies"
CRITERIA_FILE = BASE_DIR / "data" / "criteria" / "efqm2025.json"  # optional usage if needed
REPORTS_DIR = BASE_DIR / "reports" / "company_reports"
ZIP_DIR = BASE_DIR / "reports"
FONTS_DIR = BASE_DIR / "fonts"
VAZIR_FONT = FONTS_DIR / "Vazirmatn.ttf"

BANNER_PATH = BASE_DIR / "help" / "banner.png"
LOGO_PATH = BASE_DIR / "help" / "logo_gray.png"
SIGN_PATH = BASE_DIR / "help" / "signature-template.png"

# Ensure output dirs
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
ZIP_DIR.mkdir(parents=True, exist_ok=True)

# ------------------ Helpers ------------------
def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s-]+", "_", s)
    return s

def fix_rtl(text: str) -> str:
    if not isinstance(text, str):
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def register_font():
    if VAZIR_FONT.exists():
        try:
            pdfmetrics.registerFont(TTFont("Vazirmatn", str(VAZIR_FONT)))
            print("✅ Vazirmatn font registered.")
            return "Vazirmatn"
        except Exception as e:
            print("⚠️ Warning: failed to register Vazirmatn:", e)
    print("⚠️ Vazirmatn not found; falling back to Helvetica (may not render Persian correctly).")
    return "Helvetica"

# ------------------ PDF generation per company ------------------
def build_company_pdf(company_data: dict, out_path: Path, farsi_font_name: str):
    """
    company_data expected structure (example):
    {
      "organization": "شرکت پتروشیمی بتا",
      "evaluator": "نام ارزیاب",
      "date": "2025-10-23",
      "criteria": [ ... ]  # optional, custom structure
      // any other fields used in the report
    }
    """
    # Document
    doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                            rightMargin=50, leftMargin=50, topMargin=60, bottomMargin=60)

    styles = getSampleStyleSheet()
    # custom unique style names
    styles.add(ParagraphStyle(name='MyTitle', fontName=farsi_font_name, fontSize=16, leading=20, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name='MySub', fontName=farsi_font_name, fontSize=12, leading=16, alignment=1, textColor=colors.gray))
    styles.add(ParagraphStyle(name='MyBody', fontName=farsi_font_name, fontSize=11, leading=16, alignment=2))
    styles.add(ParagraphStyle(name='MyEn', fontName='Helvetica', fontSize=10, leading=14, alignment=0))

    story = []

    # Header banner
    try:
        if BANNER_PATH.exists():
            story.append(Image(ImageReader(str(BANNER_PATH)), width=480, height=120))
    except Exception as e:
        print("⚠️ banner load error:", e)
    story.append(Spacer(1,12))

    # Title block
    org = company_data.get("organization", "نام شرکت")
    evaluator = company_data.get("evaluator", "")
    date = company_data.get("date", datetime.utcnow().strftime("%Y-%m-%d"))

    story.append(Paragraph(fix_rtl(org), styles['MyTitle']))
    sub_line = f"{fix_rtl('گزارش بازخورد ارزیابی')} — {fix_rtl('تاریخ:')} {fix_rtl(str(date))}"
    story.append(Paragraph(sub_line, styles['MySub']))
    if evaluator:
        story.append(Paragraph(fix_rtl("ارزیاب: ") + " " + fix_rtl(evaluator), styles['MySub']))
    story.append(Spacer(1,12))

    # Short executive summary (from available fields or placeholder)
    summary = company_data.get("summary", "")
    if not summary:
        summary = "خلاصه: گزارش بازخورد شامل نتایج ارزیابی مطابق EFQM 2025 و فرصت‌های بهبود پیشنهادی است."
    story.append(Paragraph(fix_rtl(summary), styles['MyBody']))
    story.append(Spacer(1,12))

    # If criteria exist, show a compact table of top-level criteria scores (robust)
    criteria = company_data.get("criteria") or []
    if isinstance(criteria, list) and len(criteria) > 0:
        # build small table: Criterion | Score
        table_data = [[fix_rtl("معیار"), fix_rtl("امتیاز")]]
        for c in criteria:
            title = c.get("title") or c.get("name") or str(c.get("id",""))
            score = c.get("score","")
            table_data.append([fix_rtl(str(title)), fix_rtl(str(score))])
        # Use a simple Table
        t = Table(table_data, colWidths=[350, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(1,0), colors.HexColor("#E5E7EB")),
            ('ALIGN',(0,0),(-1,-1),'RIGHT'),
            ('FONTNAME', (0,0), (-1,-1), farsi_font_name),
            ('GRID',(0,0),(-1,-1), 0.3, colors.gray),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1,12))

    # Strengths & Opportunities if present
    strengths = company_data.get("strengths", [])
    opportunities = company_data.get("opportunities", [])
    if strengths:
        story.append(Paragraph(fix_rtl("نقاط قوت:"), styles['MyBody']))
        for s in strengths:
            story.append(Paragraph("• " + fix_rtl(str(s)), styles['MyBody']))
        story.append(Spacer(1,8))
    if opportunities:
        story.append(Paragraph(fix_rtl("فرصت‌های بهبود:"), styles['MyBody']))
        for o in opportunities:
            story.append(Paragraph("• " + fix_rtl(str(o)), styles['MyBody']))
        story.append(Spacer(1,8))

    # RADAR example block (if exists)
    # We'll attempt to print for each criteria->subcriteria->radar
    for c in criteria:
        sub = c.get("subcriteria") or []
        if sub:
            for sc in sub:
                sc_title = sc.get("title") or sc.get("name","")
                story.append(Paragraph(fix_rtl(str(sc_title)), styles['MySub']))
                radar = sc.get("radar") or {}
                # show Results / Approach / Deployment / Refinement if present
                if radar:
                    parts = []
                    for k in ("results","approach","deployment","refinement"):
                        if radar.get(k):
                            parts.append(f"{k.capitalize()}: {radar.get(k)}")
                    if parts:
                        story.append(Paragraph(fix_rtl("؛ ".join(parts)), styles['MyBody']))
                story.append(Spacer(1,6))

    # Footer with logo and signature if available
    story.append(Spacer(1,20))
    try:
        if LOGO_PATH.exists():
            story.append(Image(ImageReader(str(LOGO_PATH)), width=120, height=40))
    except Exception as e:
        print("⚠️ logo load error:", e)
    story.append(Spacer(1,12))
    story.append(Paragraph(fix_rtl(evaluator or ""), styles['MyBody']))
    try:
        if SIGN_PATH.exists():
            story.append(Image(ImageReader(str(SIGN_PATH)), width=180, height=60))
    except Exception as e:
        print("⚠️ signature load error:", e))
    story.append(Spacer(1,8))
    story.append(Paragraph("© EFQM2025 Assessment Pack", styles['MyEn'] if 'MyEn' in styles else styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        print(f"✅ PDF created: {out_path}")
    except Exception as e:
        print("❌ Error building PDF for", company_data.get("organization"), e)

# ------------------ Main driver ------------------
def main():
    farsi_font = register_and_get_font()
    # read company files
    files = sorted([p for p in COMPANIES_DIR.glob("*.json")])
    if not files:
        print("⚠️ No company JSON files found in", COMPANIES_DIR)
        return

    created_files = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            print("⚠️ Failed to read", f, e)
            continue

        org = data.get("organization") or data.get("name") or f.stem
        slug = slugify(org)
        out_name = f"{slug}_feedback.pdf"
        out_path = REPORTS_DIR / out_name

        # build pdf
        build_company_pdf(data, out_path, farsi_font)
        created_files.append(out_path)

    # create zip
    if created_files:
        today = datetime.utcnow().strftime("%Y%m%d")
        zip_name = ZIP_DIR / f"EFQM2025_Assessment_Pack_{today}.zip"
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
            for p in created_files:
                z.write(p, arcname=p.name)
        print("✅ ZIP package created:", zip_name)
    else:
        print("⚠️ No PDFs were created.")

# ------------------ small helper to register font ------------------
def register_and_get_font():
    if VAZIR_FONT.exists():
        try:
            pdfmetrics.registerFont(TTFont("Vazirmatn", str(VAZIR_FONT)))
            print("✅ Registered Vazirmatn")
            return "Vazirmatn"
        except Exception as e:
            print("⚠️ Could not register Vazirmatn:", e)
    return "Helvetica"

if __name__ == "__main__":
    main()
