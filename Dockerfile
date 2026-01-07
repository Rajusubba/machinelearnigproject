FROM python:3.11-slim-bookworm

WORKDIR /app
COPY . /app

# If you REALLY need awscli inside the image:
RUN apt-get update && apt-get install -y --no-install-recommends awscli \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]