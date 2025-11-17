from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import json

app = Flask(__name__)

# ==============================
# مسیرهای اصلی پروژه
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
COMPANIES_DIR = os.path.join(DATA_DIR, "companies")
CRITERIA_FILE = os.path.join(DATA_DIR, "criteria", "efqm2025.json")

os.makedirs(COMPANIES_DIR, exist_ok=True)


# ==============================
# صفحه مدیریت شرکت‌ها
# ==============================
@app.route("/")
def index():
    return render_template("company_manager.html")


# ==============================
# صفحه ارزیابی یک شرکت
# ==============================
@app.route("/assessment")
def assessment_page():
    return render_template("assessment_form.html")


# ==============================
# API: بارگذاری معیارها (EFQM2025)
# ==============================
@app.get("/api/criteria")
def api_criteria():
    if not os.path.exists(CRITERIA_FILE):
        return jsonify({"error": "criteria file not found"}), 404
    with open(CRITERIA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


# ==============================
# API: لیست شرکت‌ها
# ==============================
@app.get("/api/list-companies")
def list_companies():
    companies = []
    for name in os.listdir(COMPANIES_DIR):
        path = os.path.join(COMPANIES_DIR, name)
        if os.path.isdir(path):
            has_assessment = os.path.exists(os.path.join(path, "assessment.json"))
            companies.append({
                "name": name,
                "hasAssessment": has_assessment
            })
    return jsonify(companies)


# ==============================
# API: ساخت شرکت جدید
# ==============================
@app.post("/api/create-company")
def api_create_company():
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "No name"}), 400

    safe_name = name.replace(" ", "_")
    company_path = os.path.join(COMPANIES_DIR, safe_name)
    os.makedirs(company_path, exist_ok=True)

    return jsonify({"message": f"شرکت «{name}» با موفقیت ایجاد شد."})


# ==============================
# کمک‌کننده: بارگذاری ارزیابی شرکت
# ==============================
def load_assessment(company):
    path = os.path.join(COMPANIES_DIR, company, "assessment.json")
    if not os.path.exists(path):
        return {"company": company, "criteria": {}}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================
# کمک‌کننده: ذخیره ارزیابی شرکت
# ==============================
def save_assessment(company, data):
    folder = os.path.join(COMPANIES_DIR, company)
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, "assessment.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


# ==============================
# API: ذخیره‌سازی زیرمعیار EFQM
# ==============================
@app.post("/api/save-subcriterion")
def api_save_subcriterion():
    data = request.json

    company = data.get("company")
    criterion = data.get("criterion")
    subcriterion = data.get("subcriterion")

    strengths = data.get("strengths", [])
    opportunities = data.get("opportunities", [])
    radar = data.get("radar", {})

    if not all([company, criterion, subcriterion]):
        return jsonify({"error": "Missing required fields"}), 400

    assessment = load_assessment(company)

    # ایجاد ساختار مناسب EFQM
    if criterion not in assessment["criteria"]:
        assessment["criteria"][criterion] = {}

    assessment["criteria"][criterion][subcriterion] = {
        "strengths": strengths,
        "opportunities": opportunities,
        "radar": radar
    }

    save_assessment(company, assessment)

    return jsonify({"message": "Subcriterion saved"})


# ==============================
# API: دسترسی فایل‌های ذخیره‌شده شرکت
# ==============================
@app.route("/data/companies/<company>/<filename>")
def serve_company_file(company, filename):
    return send_from_directory(os.path.join(COMPANIES_DIR, company), filename)


# ==============================
# اجرای برنامه
# ==============================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
