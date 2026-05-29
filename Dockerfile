FROM python:3.12-slim-bookworm

WORKDIR /sentinel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# we only have app/ & alembic/ so we copy both


CMD ["uvicorn", "main.app:app", "--host", "0.0.0.0", "--port", "8000"]