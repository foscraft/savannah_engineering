#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import requests # type: ignore
import json


# In[4]:


url_user = "https://dummyjson.com/user"
url_products = "https://dummyjson.com/products"
url_carts = "https://dummyjson.com/carts"


# In[ ]:


# Set the base directory to the mapped data directory in the Docker container
DATA_DIR = '/opt/airflow/data/jsons'  # Adjusted to point to the correct directory
os.makedirs(DATA_DIR, exist_ok=True)  # Create the directory if it doesn't exis


# In[7]:


def fetch_and_save_data(url, filename):
    try:
        folder = DATA_DIR
        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, filename)

        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")


# In[8]:


fetch_and_save_data(url_user, "users.json")
fetch_and_save_data(url_products, "products.json")
fetch_and_save_data(url_carts, "carts.json")

