
FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir \
    -r requirements.txt \
    "jaraco.context>=6.1.0" \
    "wheel>=0.46.2"

COPY app/ ./app/
COPY tests/ ./tests/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
