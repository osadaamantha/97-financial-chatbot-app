# 🧾 Final Report — Financial Dashboard & Chatbot

## 🚀 Overview

This project delivers a **full-stack solution** combining:

- 📊 A financial dashboard with quarterly/yearly filters
- 🧠 An AI-powered chatbot using **RAG (Retrieval-Augmented Generation)**
- 🐳 Fully containerized setup using Docker
- 🧾 Data sourced from scraped quarterly reports and CSVs

Built with modern, scalable technologies like **React, Flask, FastAPI, LangChain, OpenAI API, and Docker**.

---

## 🧱 Architecture
``` bash 
financial_backend/
│
├── client/ # React dashboard + chatbot UI
├── api/ # Flask backend serving financial metrics API
├── chatbot/ # FastAPI + LangChain RAG chatbot
├── scraper/ # PDF scraping, LLM extraction logic
├── chroma_db/ # Vector store (ignored in git)
├── financial_metrics.csv
├── Dockerfile
├── requirements.txt
└── README.md

```


---

## ✅ Approach & Assumptions

### 📊 Dashboard

- Built in **React**, consumes data via Flask API.
- Dynamic filters: company, year, year-range, quarter-range.
- Summarized KPIs (Revenue, Net Income, etc.) with visualizations.
- Assumes clean and structured data from `financial_metrics.csv`.

### 🧠 Chatbot

- Based on **LangChain RAG pipeline** using OpenAI’s GPT-4-turbo.
- Uses `Chroma` vector store built from `financial_metrics.csv`.
- FastAPI handles question input, routes through ConversationalRetrievalChain.

### 📦 Docker

- Multi-stage Docker build for React frontend and Python backend.
- Exposes both Flask (5000) and FastAPI (8000) from a single container.
- React build hosted statically within the same container.

---

## ⚠️ Limitations & Data Handling

| Area | Handling |
|------|----------|
| 🧾 PDF Parsing | Relies on `pdfplumber` + GPT prompt for clean table parsing |
| 📅 Inconsistent periods | Only the latest **3-month period** is extracted |
| 🧠 Chatbot Data | Answers limited to content pre-loaded in the CSV via vector index |
| 🧼 Data Quality | Cleans text, tolerates bracketed negatives, excludes incomplete rows |
| 🌍 Company Scope | Only supports `DIPD.N0000` and `REXP.N0000` at present |
| 📤 GPT Output | Strict JSON enforced, fallback to cleaning markdown formatting |

---

## 📈 Final Outcome

| Feature | Status |
|--------|--------|
| 📊 Filterable Dashboard | ✅ Completed |
| 💬 RAG-based Chatbot | ✅ Completed |
| 🔍 GPT Extraction from PDFs | ✅ Completed |
| 🐳 Dockerization | ✅ Multi-stage container |
| 🔁 GitHub Deployment | ✅ Public repo created |
| 📘 Documentation | ✅ README + Final Report |

---

## 🔮 Potential Enhancements

- Live PDF ingestion in chatbot
- Automated CI/CD pipeline (GitHub Actions)
- User authentication for access control
- Extend to more companies dynamically

---

## 👥 Author

**Amantha Madanayake**  
🔗 GitHub: [github.com/osadaamantha](https://github.com/osadaamantha)

---
