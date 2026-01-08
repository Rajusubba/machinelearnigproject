FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Gunicorn serves Flask via WSGI
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]