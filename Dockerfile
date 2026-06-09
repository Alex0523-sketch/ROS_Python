FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SECRET_KEY=build-secret-key-placeholder
ENV DEBUG=false
ENV POSTGRES_HOST=localhost
ENV POSTGRES_DB=placeholder
ENV POSTGRES_USER=placeholder
ENV POSTGRES_PASSWORD=placeholder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/media

RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000
