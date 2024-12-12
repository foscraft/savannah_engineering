#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests # type: ignore
import json
import os


# In[ ]:


DATA_DIR = '/opt/airflow/data/jsons'
os.makedirs(DATA_DIR, exist_ok=True)


# In[ ]:


def fetch_and_save_data():
    """
    Fetch data from /carts, /products, and /users endpoints, handle pagination,
    and save results to JSON files in the specified directory. Raise errors for failed API calls.
    """
    endpoints = {
        "carts": "https://dummyjson.com/carts",
        "products": "https://dummyjson.com/products",
        "users": "https://dummyjson.com/users",
    }
    output_files = {
        "carts": os.path.join(DATA_DIR, "carts.json"),
        "products": os.path.join(DATA_DIR, "products.json"),
        "users": os.path.join(DATA_DIR, "users.json"),
    }
    limit = 10  

    for key, url in endpoints.items():
        try:
            skip = 0
            all_data = []

            while True:
                response = requests.get(url, params={"limit": limit, "skip": skip})
                response.raise_for_status()  
                data = response.json()
                results = data.get(key, [])  
                if not results:
                    break

                all_data.extend(results)
                skip += limit

            with open(output_files[key], "w") as json_file:
                json.dump(all_data, json_file, indent=4)

            print(f"Data for '{key}' successfully saved to {output_files[key]} with {len(all_data)} entries.")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch data from {url}: {e}")

try:
    fetch_and_save_data()
except RuntimeError as e:
    print(f"Error: {e}")

