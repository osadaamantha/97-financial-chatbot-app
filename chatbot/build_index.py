import os
import csv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.docstore.document import Document

# File paths
CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "financial_metrics.csv")
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

print("🧠 Checking vector store existence...")

if os.path.exists(CHROMA_DB_DIR):
    print("✅ Vector store already exists at 'chroma_db/'. Skipping embedding creation.")
else:
    print("📄 Loading CSV and generating embeddings...")

    # Load raw data from CSV
    documents = []
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row.get("CompanyName") or not row.get("Revenue"):
                continue  # Skip incomplete rows

            sentence = (
                f"In {row.get('Year')}, {row.get('CompanyName')} reported "
                f"a revenue of {row.get('Revenue')} and a gross profit of {row.get('GrossProfit')}. "
                f"The net income was {row.get('NetIncome')}, with other operating income of {row.get('OtherOperatingIncome')}. "
                f"This data covers the period {row.get('PeriodStartEnd')}."
            )

            documents.append(Document(page_content=sentence, metadata=row))

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Create Chroma vector store
    vectordb = Chroma.from_documents(documents, embeddings, persist_directory=CHROMA_DB_DIR)
    vectordb.persist()

    print("✅ Vector store created and persisted at 'chroma_db/'")
