import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
COMPANIES_DIR = os.path.join(BASE_DIR, "data", "companies")

def save_assessment(company_name, assessment_data):
    """Save assessment JSON for a company"""
    company_path = os.path.join(COMPANIES_DIR, company_name)

    if not os.path.exists(company_path):
        os.makedirs(company_path, exist_ok=True)

    file_path = os.path.join(company_path, "assessment.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(assessment_data, f, ensure_ascii=False, indent=2)

    return file_path
