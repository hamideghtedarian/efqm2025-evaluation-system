from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__)

# -----------------------------------
# مسیرهای اصلی سیستم
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
COMPANIES_DIR = os.path.join(DATA_DIR, "companies")
CRITERIA_FILE = os.path.join(DATA_DIR, "criteria", "efqm2025_full_model.json")

# --------------------------------------------------------
# 1) صفحه اصلی (فرم ارزیابی)
# --------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory("templates", "assessment_form.html")

# سرویس‌دهی فایل‌های static
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# سرویس‌دهی فایل‌های templates
@app.route("/templates/<path:filename>")
def templates_files(filename):
    return send_from_directory("templates", filename)

# سرویس‌دهی فایل‌های JSON مدل EFQM
@app.route("/data/<path:filename>")
def data_files(filename):
    return send_from_directory("data", filename)

# --------------------------------------------------------
# 2) API: خواندن مدل EFQM 2025
# --------------------------------------------------------

@app.route("/api/criteria")
def get_criteria():
    if not os.path.exists(CRITERIA_FILE):
        return jsonify({"error": "EFQM model file not found"}), 404

    with open(CRITERIA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

# --------------------------------------------------------
# 3) API: ذخیره ارزیابی شرکت
# --------------------------------------------------------

@app.route("/api/save-assessment", methods=["POST"])
def save_assessment():
    try:
        data = request.json
        company_name = data.get("company")
        assessment_data = data.get("assessment")

        if not company_name or not assessment_data:
            return jsonify({"error": "Missing company or assessment"}), 400

        # مسیر شرکت
        company_folder = os.path.join(COMPANIES_DIR, company_name)
        os.makedirs(company_folder, exist_ok=True)

        # مسیر ذخیره فایل
        assessment_file = os.path.join(company_folder, "assessment.json")

        # ذخیره‌سازی JSON
        with open(assessment_file, "w", encoding="utf-8") as f:
            json.dump(assessment_data, f, ensure_ascii=False, indent=2)

        return
