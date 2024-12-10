FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools

RUN pip install pandas requests \
    apache-airflow[postgres] \
    apache-airflow==2.6.1 \
    psycopg2-binary jupyter

COPY . /app
