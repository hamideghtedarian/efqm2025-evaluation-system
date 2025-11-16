import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
COMPANIES_DIR = os.path.join(BASE_DIR, "data", "companies")

def load_assessment(company):
    """Load assessment file for a company"""
    path = os.path.join(COMPANIES_DIR, company, "assessment.json")
    if not os.path.exists(path):
        return {"company": company, "criteria": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_assessment(company, data):
    """Save full assessment JSON"""
    folder = os.path.join(COMPANIES_DIR, company)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "assessment.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def update_subcriterion(company, criterion_code, subcriterion_code, strengths, opportunities, radar):
    """Update one subcriterion entry inside assessment.json"""

    data = load_assessment(company)

    if criterion_code not in data["criteria"]:
        data["criteria"][criterion_code] = {}

    data["criteria"][criterion_code][subcriterion_code] = {
        "strengths": strengths,
        "opportunities": opportunities,
        "radar": radar
    }

    save_assessment(company, data)
    return True
