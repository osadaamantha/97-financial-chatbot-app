import os
import csv
import re
from scraper.pdf_parser import get_pdf_text_from_url
from scraper.llm_extractor import extract_financial_metrics
from scraper.constants import company_name_map


def clean_text(text: str) -> str:
    text = ''.join(char if char.isprintable() else ' ' for char in text)
    return re.sub(r'\s+', ' ', text).strip()

def is_valid(metrics: dict) -> bool:
    required = ["CompanyName", "Revenue", "COGS", "GrossProfit", "OtherOperatingIncome", "DistributionCosts", "OtherOperatingExpense", "NetIncome", "PeriodStartEnd"]
    return all(metrics.get(field) not in [None, "", "null"] for field in required)

def save_metrics_to_csv(metrics: dict):
    fieldnames = ["CompanyName", "Revenue", "COGS", "GrossProfit", "OtherOperatingIncome", "DistributionCosts", "OtherOperatingExpense", "NetIncome", "PeriodStartEnd"]
    file_exists = os.path.isfile("financial_metrics.csv")

    with open("financial_metrics.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics)

def process_pdf_url(pdf_url: str, symbol: str) -> bool:
    print(f"📥 Processing PDF: {pdf_url}")
    raw_text = get_pdf_text_from_url(pdf_url, symbol)
    cleaned_text = clean_text(raw_text)

    company_name = company_name_map.get(symbol, "Unknown Company")
    metrics = extract_financial_metrics(cleaned_text, company_name)

    if not is_valid(metrics):
        print("⏩ Skipped — incomplete data")
        return False

    save_metrics_to_csv(metrics)
    print(f"✅ Saved metrics for {company_name}")
    return True
