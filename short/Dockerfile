FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV SHORT_DB_URL=sqlite://./DB/shorturl.db
CMD ["uvicorn", "main:app_short", "--host", "0.0.0.0", "--port", "80"]
