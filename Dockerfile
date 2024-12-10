FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools

RUN pip install --upgrade pip

RUN pip install pandas requests apache-airflow[postgres] psycopg2-binary

RUN pip install apache-airflow==2.6.1 jupyter

#RUN airflow users reset-password --username admin


