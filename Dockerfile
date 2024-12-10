FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools

RUN pip install --upgrade pip

COPY . .

RUN pip install pandas requests apache-airflow[postgres] psycopg2-binary

RUN pip install apache-airflow==2.6.1 jupyter

# Convert notebooks to scripts
RUN jupyter nbconvert --to script /app/notebooks/extract_data.ipynb --output /app/scripts/extract_data.py && \
    jupyter nbconvert --to script /app/notebooks/clean_data.ipynb --output /app/scripts/clean_data.py && \
    jupyter nbconvert --to script /app/notebooks/generate_insights.ipynb --output /app/scripts/generate_insights.py


