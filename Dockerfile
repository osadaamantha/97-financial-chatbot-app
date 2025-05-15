# Stage 1 - Build the React app
FROM node:20 AS frontend

WORKDIR /app
COPY client/ /app/
RUN npm install && npm run build

# Stage 2 - Backend and Static Frontend Hosting
FROM python:3.10

WORKDIR /app

# Copy backend and chatbot
COPY api /app/api
COPY chatbot /app/chatbot
COPY financial_metrics.csv /app/
COPY requirements.txt /app/

# Copy built React files from frontend stage
COPY --from=frontend /app/build /app/client/build

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Add PYTHONPATH
ENV PYTHONPATH=/app

# Expose ports
EXPOSE 5000
EXPOSE 8000

# Start both backend servers
CMD ["bash", "-c", "uvicorn chatbot.app:app --host 0.0.0.0 --port 8000 & python api/app.py"]
