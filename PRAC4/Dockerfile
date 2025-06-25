FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ansible openssh-client && \
    pip install Flask

COPY . .

RUN chmod 600 /app/keys/id_rsa || true

CMD ["python", "app/app.py"]
