import requests
import pdfplumber
import io

def get_pdf_text_from_url(pdf_url: str, symbol: str) -> str:
    """
    Downloads a PDF, extracts text from only the relevant pages:
    - For DIPD.N0000 → Group-level "Statement of Profit or Loss"
    - For REXP.N0000 → "Consolidated Income Statement"
    """
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise error for bad status

        relevant_text = ""

        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                lowered = text.lower()

                if symbol == "DIPD.N0000":
                    if "statement of profit or loss" in lowered and "group" in lowered:
                        relevant_text += f"\n\nPage {i+1}\n{text}"

                elif symbol == "REXP.N0000":
                    if "consolidated income statement" in lowered:
                        relevant_text += f"\n\nPage {i+1}\n{text}"

        if not relevant_text.strip():
            print("⚠️ No relevant P&L section found.")
        return relevant_text.strip()

    except Exception as e:
        print(f"❌ Error processing PDF from {pdf_url}: {e}")
        return ""
