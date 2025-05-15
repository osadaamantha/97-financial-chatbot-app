from dotenv import load_dotenv
from scraper.pdf_downloader import get_all_quarterly_pdf_links
from scraper.utils import process_pdf_url
import os

load_dotenv()

company_symbols = ["DIPD.N0000", "REXP.N0000"]
success_count = 0

for symbol in company_symbols:
    print(f"\n🔍 Scraping: {symbol}")
    company_url = f"https://www.cse.lk/pages/company-profile/company-profile.component.html?symbol={symbol}"

    pdf_links = get_all_quarterly_pdf_links(company_url, symbol)
    print(f"📄 Found {len(pdf_links)} quarterly PDFs for {symbol}")

    if not pdf_links:
        print(f"⚠️ No PDFs found for {symbol}. Skipping.")
        continue

    for link in pdf_links:
        if process_pdf_url(link, symbol):
            success_count += 1

print(f"\n✅ Successfully processed {success_count} quarterly reports.")
