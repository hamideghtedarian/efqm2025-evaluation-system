from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANIES_DIR = os.path.join(BASE_DIR, "data", "companies")
CRITERIA_FILE = os.path.join(BASE_DIR, "data", "criteria", "efqm2025_full_model.json")

# ========================
#   Serve Front-End Pages
# ========================

@app.route("/")
def home():
    return send_from_directory("templates", "assessment_form.html")


@app.route("/templates/<path:filename>")
def serve_templates(filename):
    return send_from_directory("templates", filename)


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


@app.route("/data/<path:filename>")
def serve_data
