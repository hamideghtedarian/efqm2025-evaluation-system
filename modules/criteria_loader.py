import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CRITERIA_FILE = os.path.join(BASE_DIR, "data", "criteria", "efqm2025_full_model.json")

def load_criteria():
    if not os.path.exists(CRITERIA_FILE):
        raise FileNotFoundError(f"EFQM criteria file missing: {CRITERIA_FILE}")

    with open(CRITERIA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_criteria_list():
    data = load_criteria()
    return data.get("criteria", [])

def get_criterion(code: str):
    """مثلاً C1 یا C4-3"""
    criteria = get_criteria_list()
    parts = code.split("-")

    # Criterion only (like C1)
    if len(parts) == 1:
        for c in criteria:
            if c["code"] == code:
                return c
        return None

    # Subcriterion (like C4-3)
    for c in criteria:
        if c["code"] == parts[0]:
            for sub in c["subcriteria"]:
                if sub["code"] == code:
                    return sub
    return None
