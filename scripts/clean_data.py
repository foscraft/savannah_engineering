#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
import pandas as pd # type: ignore


# In[ ]:


# Set the base directory to the mapped data directory in the Docker container
BASEDIR = '/opt/airflow/data'


# In[ ]:


with open(os.path.join(BASEDIR, 'jsons', 'users.json'), 'r') as file:
    users_data = json.load(file)

with open(os.path.join(BASEDIR, 'jsons', 'products.json'), 'r') as file:
    products_data = json.load(file)

with open(os.path.join(BASEDIR, 'jsons', 'carts.json'), 'r') as file:
    carts_data = json.load(file)


# In[8]:


CLEANED_DIR = os.path.join(BASEDIR, 'cleaned')

os.makedirs(CLEANED_DIR, exist_ok=True)

users_df = pd.DataFrame(users_data)

address_data = [
    {
        'street': address.get('address', '') if isinstance(address, dict) else '',
        'city': address.get('city', '') if isinstance(address, dict) else '',
        'postal_code': address.get('postalCode', '') if isinstance(address, dict) else ''
    } for address in users_df.get('address', [])
]


# In[9]:


address_df = pd.DataFrame(address_data)

# Combine and rename columns
users_df = pd.concat([users_df, address_df], axis=1)
users_df = users_df[['id', 'firstName', 'lastName', 'gender', 'age', 'street', 'city', 'postal_code']]
users_df.columns = ['user_id', 'first_name', 'last_name', 'gender', 'age', 'street', 'city', 'postal_code']


# In[10]:


# Clean and normalize products data
products_df = pd.DataFrame(products_data)

# Use boolean indexing for filtering
products_df = products_df[products_df['price'] > 50]
products_df = products_df[['id', 'title', 'category', 'brand', 'price']]
products_df.columns = ['product_id', 'name', 'category', 'brand', 'price']


# In[ ]:


# Clean and normalize carts data
carts_df = pd.DataFrame(carts_data)

carts_df = carts_df.explode('products', ignore_index=True)
cat_product_data = [
        {
            'product_id': product.get('id', None),
            'quantity': product.get('quantity', 0),
            'price': product.get('price', 0)
        } if isinstance(product, dict) else {'cart_id': carts_df.loc[i, 'id'], 'product_id': None, 'quantity': 0, 'price': 0}
        for i, product in enumerate(carts_df['products'])
    ]
cat_product_df = pd.DataFrame(cat_product_data)


# In[ ]:


# Combine and calculate additional fields
carts_df = pd.concat([carts_df, cat_product_df], axis=1)
carts_df['total_cart_value'] = carts_df['quantity'] * carts_df['price']
carts_df = carts_df[['id', 'userId', 'product_id', 'quantity', 'price', 'total_cart_value']]
carts_df.columns = ['cart_id', 'user_id', 'product_id', 'quantity', 'price', 'total_cart_value']


# In[15]:


users_csv_path = os.path.join(CLEANED_DIR, 'cleaned_users.csv')
products_csv_path = os.path.join(CLEANED_DIR, 'cleaned_products.csv')
carts_csv_path = os.path.join(CLEANED_DIR, 'cleaned_carts.csv')


# In[16]:


users_df.to_csv(users_csv_path, index=False)
products_df.to_csv(products_csv_path, index=False)
carts_df.to_csv(carts_csv_path, index=False)

print(f"Data cleaned and saved to CSV in: {CLEANED_DIR}")

