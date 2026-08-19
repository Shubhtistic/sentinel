FROM python:3.12-slim-bookworm

WORKDIR /sentinel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["uvicorn", "sentinel.main:app", "--host", "0.0.0.0", "--port", "8000"]