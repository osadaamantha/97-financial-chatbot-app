from pathlib import Path

readme_content = """
# 📊 97-Financial-Chatbot-App

A full-stack AI-powered dashboard application that provides **financial insights** and **natural language Q&A** for Sri Lankan companies using **React**, **Flask**, **FastAPI**, **LangChain**, and **Docker**.

---

## 🚀 Features

- 📈 **Interactive Financial Dashboard**
  - Revenue, COGS, Gross Profit, and Net Income visualizations.
  - Filter by company, year, year range, and quarter range.

- 💬 **AI Chatbot (LangChain + OpenAI)**
  - Ask natural language questions about financial performance.
  - Answers generated based on CSV vector embeddings.

- 📄 **PDF Financial Report Scraper**
  - Scrapes and processes quarterly reports from the CSE website.

- 🐳 **Dockerized for Easy Deployment**
  - Single image for backend (FastAPI + Flask) and frontend (React).

---

## 🛠️ Technologies Used

- **Frontend**: React, Recharts, CSS
- **Backend**: Flask, FastAPI, LangChain, OpenAI
- **Vector Store**: ChromaDB
- **Scraping**: BeautifulSoup, Requests
- **Containerization**: Docker

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/osadaamantha/97-financial-chatbot-app.git
cd 97-financial-chatbot-app
```
### 2. Run with Docker

```bash
docker build -t financial-dashboard .
docker run -p 8080:5000 -p 8800:8000 financial-dashboard
```

### Note by any chance if the docker run fails due to port already occupied, then stop the relevant container id using following command and re run the docker run.
```bash
docker stop <container_id_which_runs_the_port>
```

🌐 Access Dashboard & Chatbot API: http://localhost:8080

### 3. Run Locally (without Docker)

```bash
cd financial_backend
python chatbot/build_index.py  # Builds vector DB (run once)
uvicorn chatbot.app:app --reload --port 8000  # Start FastAPI
python api/app.py  # Start Flask
```
### Frontend:

```bash
cd client
npm install
npm start
```

### 📁 Project Structure

<pre> financial_backend/ ├── api/ # Flask REST API │ └── app.py ├── chatbot/ # FastAPI + LangChain chatbot │ ├── app.py │ └── build_index.py ├── client/ # React frontend │ └── src/ ├── scraper/ # PDF scraping utilities │ └── ... ├── chroma_db/ # Vector store directory (auto-generated) ├── Dockerfile # Full-stack build config ├── financial_metrics.csv # Source data ├── main.py # Scraper runner ├── requirements.txt └── .gitignore </pre>

### 📝 Example Questions for Chatbot

"What is the gross profit for 2022 for DIPPED PRODUCTS PLC?"

"Compare revenue between 2023 and 2024 for REXP."


### Local setup (without Docker)

```bash

# Python virtual environment
python -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Flask API
cd api
python app.py

# FastAPI Chatbot
cd ../chatbot
uvicorn app:app --port 8000

# React frontend
cd ../client
npm install
npm start
```



Authour
Amantha
osadaamantha@gmail.com