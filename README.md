# Data Engineering Screening Challenge

This assessment is designed to evaluate your ability to design, implement, and document a complete ETL pipeline using real-world data. The task mimics challenges faced in a data engineering environment, involving data ingestion, cleaning, transformation, and analysis using modern cloud tools.

## Objective

Build a pipeline that processes claims and user data by:

1. Extracting data from multiple APIs.
2. Cleaning and normalizing the data.
3. Joining datasets to generate insights.
4. Automating the pipeline and documenting your work.

We encourage you to use Apache Airflow, Docker, and Python, but you may use normal Python scripts if preferred. Follow software engineering best practices, including modular code, clear documentation, and adherence to coding standards.

## Project Details

### Tech Stack

- **Primary Tools**: Python, Docker, Apache Airflow, Google BigQuery.
- **Free BigQuery Tier**: Google Cloud Free Tier provides 50 GB of free storage and 1 TB of free queries per month. Create a free Google Cloud account to access BigQuery and Google Cloud Storage (GCS). Optionally, if you are unable to get a Google Cloud Account, you can save the data in your repository as CSV files, but BigQuery is encouraged.

### Tasks

1. **Extract Data from APIs**: 
   - Use the following public APIs to retrieve data. Save the raw JSON data in Google Cloud Storage (GCS):
     - Users Data
     - Products Data
     - Carts Data
   - Example: Use `requests` or any HTTP library in Python to fetch data.

2. **Clean and Normalize Data**: 
   - Prepare the following cleaned datasets:
     - **Users Table**:
       - Fields: `user_id`, `first_name`, `last_name`, `gender`, `age`, `street`, `city`, `postal_code`.
       - Tasks: Extract and flatten the address field into `street`, `city`, and `postal_code`.
     - **Products Table**:
       - Fields: `product_id`, `name`, `category`, `brand`, `price`.
       - Tasks: Exclude products with `price <= 50`.
     - **Carts Table**:
       - Fields: `cart_id`, `user_id`, `product_id`, `quantity`, `price`, `total_cart_value`.
       - Tasks: Flatten the products array into one row per product. Add `total_cart_value` for each cart.

3. **Load Data into BigQuery**: 
   - Store the cleaned datasets in separate BigQuery tables:
     - `users_table`
     - `products_table`
     - `carts_table`

4. **Join and Enrich Data**: 
   - Perform the following joins in BigQuery:
     - **Users and Carts**: Combine demographic data with transaction details.
     - **Carts and Products**: Enrich transaction data with product details.
   - Generate the following datasets:
     - **User Summary**:
       - Fields: `user_id`, `first_name`, `total_spent`, `total_items`, `age`, `city`.
       - Insights: Total spending and number of purchases per user.
     - **Category Summary**:
       - Fields: `category`, `total_sales`, `total_items_sold`.
       - Insights: Aggregate sales by product category.
     - **Cart Details**:
       - Fields: `cart_id`, `user_id`, `product_id`, `quantity`, `price`, `total_cart_value`.
       - Insights: Transaction-level details enriched with user and product data.

5. **Automate with Orchestration**: 
   - Automate the pipeline using Apache Airflow. The tasks should run in the following order:
     - Extract data from APIs.
     - Save raw JSON locally.
     - Clean and load data into BigQuery.
     - Run transformations and generate outputs.

6. **Document Your Work**: 
   - Provide clear documentation:
     - **Pipeline Design**: Include DAG structure and task dependencies.
     - **Codebase Overview**: Explain your scripts and modules.
     - **BigQuery Queries**: Share and explain your SQL logic.
     - **Assumptions and Trade-offs**: Highlight decisions made during implementation.

## Setup Instructions

1. **Clone the Repository**:

```bash
git clone git@github.com:foscraft/savannah_engineering.git
cd savannah_engineering
```
Run the bash script

```bash
bash run.sh
```

How the file looks like

```bash
#!/bin/bash
set -e

mkdir -p scripts

jupyter nbconvert --to script ./notebooks/extract_data.ipynb --output ../scripts/extract_data
jupyter nbconvert --to script ./notebooks/clean_data.ipynb --output ../scripts/clean_data
jupyter nbconvert --to script ./notebooks/generate_insights.ipynb --output ../scripts/generate_insights

docker compose build
docker compose up -d
```

Running this creates the `scripts` directory, later the `data` directory is created and subdirectories `jsons`, `cleaned`, `insights`. The relevant files are created and populated into the directories specified. All these happens when the pipeline is started.

The pipeline runs `hourly`

![](./media/2.png)

![](./media/1.png)

Incase you're having trouble logging in to airflow; reset password.

```bash
docker exec -it savannah_engineering-airflow-webserver-1  bash
```

Then run the following command to create user `savannah` and password `admin`.

```bash
airflow users create --username savannah --firstname savannah --lastname savannah --role Admin --email admin@example.com --password admin
```
Generate the secret key for for airflow (I have created one secret and passed it on `docker-compose.yml`)

```bash
openssl rand -base64 32
```