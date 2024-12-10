#!/bin/bash
set -e

mkdir -p scripts

jupyter nbconvert --to script ./notebooks/extract_data.ipynb --output ../scripts/extract_data
jupyter nbconvert --to script ./notebooks/clean_data.ipynb --output ../scripts/clean_data
jupyter nbconvert --to script ./notebooks/generate_insights.ipynb --output ../scripts/generate_insights

docker compose build
docker compose up -d
