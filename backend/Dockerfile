FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x scripts/start.sh

EXPOSE 8000

# Wait for Postgres, run migrations, then start the API.
CMD ["scripts/start.sh"]
