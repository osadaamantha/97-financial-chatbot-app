import os
import requests
import fitz  # PyMuPDF
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def extract_year_from_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open("temp.pdf", "wb") as f:
                f.write(response.content)
            
            doc = fitz.open("temp.pdf")
            first_page_text = doc[0].get_text().lower()
            doc.close()
            os.remove("temp.pdf")

            # Check for any of the target years
            for year in ["2022", "2023", "2024"]:
                if year in first_page_text:
                    return year
        return None
    except Exception as e:
        print(f"Error checking PDF {pdf_url}: {e}")
        return None

def get_all_quarterly_pdf_links(company_url: str, company_symbol: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(company_url)
        time.sleep(10)
        print(f"Navigating to {company_url}")

        # Click Financials
        financials_tab = driver.find_element(By.XPATH, '//a[contains(text(), "Financials")]')
        financials_tab.click()
        time.sleep(5)

        # Click Quarterly Reports
        quarterly_reports_tab = driver.find_element(By.XPATH, '//a[contains(text(), "Quarterly Reports")]')
        quarterly_reports_tab.click()
        time.sleep(5)

        pdf_links = []

        # Locate rows in active tab
        rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'tab-pane') and contains(@class, 'active')]//tr")

        for row in rows:
            try:
                report_text = row.find_element(By.XPATH, ".//td[2]").text
                pdf_link_elem = row.find_element(By.XPATH, ".//a[contains(@href, '.pdf')]")
                pdf_url = pdf_link_elem.get_attribute('href')
                report_text_lower = report_text.lower()

                if company_symbol == "DIPD.N0000":
                    if (
                        "quarterly financial report" in report_text_lower or
                        "interim financial statements" in report_text_lower
                    ):
                        year = extract_year_from_pdf(pdf_url)
                        if year:
                            pdf_links.append(pdf_url)

                elif company_symbol == "REXP.N0000":
                    if (
                        "interim financial statement" in report_text_lower or
                        "interim financial statements" in report_text_lower or
                        "financial statements" in report_text_lower or
                        "quater" in report_text_lower or  # typo tolerance
                        "interim" in report_text_lower     # broad fallback
                    ):
                        year = extract_year_from_pdf(pdf_url)
                        if year:
                            pdf_links.append(pdf_url)

            except Exception:
                continue

        print(f"📄 Found {len(pdf_links)} quarterly PDF links for 2022–2024.")
        return pdf_links

    except Exception as e:
        print(f"❌ Failed to extract PDF links: {e}")
        return []
    finally:
        driver.quit()