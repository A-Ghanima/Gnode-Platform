FROM python:3.11-alpine

RUN apk add --no-cache \
    mysql-client \
    postgresql-client \
    sqlite \
    gzip \
    dcron

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backup.sh upload.py entrypoint.sh ./
RUN chmod +x backup.sh entrypoint.sh

CMD ["/app/entrypoint.sh"]
