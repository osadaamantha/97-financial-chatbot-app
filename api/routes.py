from flask import Blueprint, jsonify
import csv
import os

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/api/financial-data", methods=["GET"])
def get_financial_data():
    data = []
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "financial_metrics.csv")
    
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return jsonify(data)
