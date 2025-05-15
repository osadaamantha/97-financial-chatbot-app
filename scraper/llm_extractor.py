import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_financial_data(data: str) -> str:
    data = data.replace(",", "")
    if "(" in data and ")" in data:
        return str(float(data.replace("(", "").replace(")", "")))  # Treat as positive
    return str(float(data))

def extract_financial_metrics(text: str, company_name: str) -> dict:
    prompt = f"""
You are a Financial Data Extraction Assistant. Your task is to review the text of a quarterly financial report (provided below) and extract specific financial metrics only from the most recent 3-month reporting period, following the detailed instructions below.

---

1. **Statement Priority (Strict Rule)**  
- Use “Statement of Profit or Loss” if available — prioritize the **Group** column, and extract data only for the **03 months to** with the latest 3-month column (e.g., “3 months ended 30 June 2023”).  
- If unavailable, use “Consolidated Income Statement” with the latest 3-month column extracting only for the **3 months ended** starting naming convention column.  
- If neither exists, fall back to “Company Income Statement” or “Standalone”.  
- ⚠️ Ignore any older or duplicate versions if Group/Consolidated exists.

---

2. **Ignore These Sections**  
- Statement of Comprehensive Income or “Other Comprehensive Income”  
- Statement of Financial Position  
- Statement of Changes in Equity  
- Cash Flow Statement  
- Notes to the financials  
- Segment-level information  
- Duplicate income statements not clearly marked as official

---

3. **Only Extract the Latest 3-Month Period**  
- Look for formats like “3 months ended [Date]” and convert to: "YYYY-MM-DD - YYYY-MM-DD"  
  Example: “3 months ended 30 June 2023” → "2023-04-01 - 2023-06-30"  
- If multiple periods exist, pick the most recent.  
- ⚠️ Exclude 6, 9, 12-month or annual data.

---

4. **Important Notes on Table Layouts**  
- If column headers are split across multiple lines (e.g., dates and periods), merge them logically.  
- Always extract from the **Group** or **Consolidated** column. Avoid **Company** or **Standalone** unless no alternatives exist.  
- Assume the data is arranged vertically even if grid lines are missing.

---

5. **Extract These Fields**  
Return only values for the latest 3-month period:

- `CompanyName` → from document header (e.g., “ABC PLC”). Set this value to `{company_name}`.
- `Revenue` → from “Revenue”, “Sales”, or “Turnover”
- `COGS` → from “Cost of Sales” or “Cost of Revenue”
- `GrossProfit` → use if present, else calculate: Revenue - COGS
- `OtherOperatingIncome` → from “Other Operating Income” or “Other Income”
- `DistributionCosts` → from “Distribution Costs”
- `OtherOperatingExpense` → If "Other Operating Expense" or "Other Expense" is not listed, use "Administrative Expenses" as a substitute. Do not return both.
- `NetIncome` → from “Profit for the period” (after taxes)

⚠️ Do not return negative numbers. All values must be treated as positive, even if enclosed in brackets or preceded by a minus sign.

---

6. **Strict JSON Output Only**  
Return your answer in this format, and nothing else:

```json
{{
  "CompanyName": "{company_name}",
  "Revenue": "...",
  "COGS": "...",
  "GrossProfit": "...",
  "OtherOperatingIncome": "...",
  "DistributionCosts": "...",
  "OtherOperatingExpense": "...",
  "NetIncome": "...",
  "PeriodStartEnd": "YYYY-MM-DD - YYYY-MM-DD"
}}
```

    - All values must be strings (e.g., "578,300")
    - No currency symbols or extra text
    - Empty fields must return ""

    ---

    7. **Final Validations**
    - Ensure all values come from the selected **Group or Consolidated** 3-month column
    - when extracting the columns 
    - Validate that the extracted date range matches the **latest** 3-month period
    - Output only clean JSON — no markdown, no notes

    Below is the extracted financial report text:
    {text[:12000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-4 model earlier but changed it to 3.5 due to cost
            messages=[
                {"role": "system", "content": "You extract financial metrics from quarterly financial reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        result = response.choices[0].message.content.strip()

        # Clean up GPT output if wrapped in markdown
        if result.startswith("```") or not result.startswith("{"):
            result = result.replace("```json", "").replace("```", "").strip()

        # Parse all the numerical data properly (including handling negative values in parentheses)
        metrics = json.loads(result)
        for key in ["Revenue", "COGS", "GrossProfit", "OtherOperatingIncome", "DistributionCosts", "OtherOperatingExpense", "NetIncome"]:
            if metrics.get(key):
                metrics[key] = parse_financial_data(metrics[key])

        print("🧠 GPT result:")
        print(metrics)

        return metrics

    except Exception as e:
        print(f"❌ Error during OpenAI extraction: {e}")
        return {}
