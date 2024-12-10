#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import pandas as pd # type: ignore


# In[ ]:


# Set the base directory to the mapped data directory in the Docker container
BASEDIR = '/opt/airflow/data'  # Adjusted to point to the correct directory


# In[9]:


users_df = pd.read_csv(os.path.join(BASEDIR, 'cleaned', 'cleaned_users.csv'))
products_df = pd.read_csv(os.path.join(BASEDIR, 'cleaned', 'cleaned_products.csv'))
carts_df = pd.read_csv(os.path.join(BASEDIR, 'cleaned', 'cleaned_carts.csv'))


# In[10]:


INSIGHTS_DIR = os.path.join(BASEDIR, 'insights')
os.makedirs(INSIGHTS_DIR, exist_ok=True)


# In[11]:


# 1. User Summary: Total spending and number of purchases per user
user_summary = carts_df.groupby('user_id').agg(
    total_spent=('total_cart_value', 'sum'),
    total_items=('cart_id', 'count')
).reset_index()

user_summary = user_summary.merge(users_df[['user_id', 'first_name', 'age', 'city']], on='user_id', how='left')


# In[12]:


# 2. Category Summary: Aggregate sales by product category
category_summary = carts_df.merge(products_df[['product_id', 'category']], on='product_id', how='left')
category_summary = category_summary.groupby('category').agg(
    total_sales=('total_cart_value', 'sum'),
    total_items_sold=('cart_id', 'count')
).reset_index()


# In[13]:


# 3. Cart Details: Transaction-level details enriched with user and product data
cart_details = carts_df.merge(users_df[['user_id', 'first_name', 'age', 'city']], on='user_id', how='left')
cart_details = cart_details.merge(products_df[['product_id', 'name', 'category']], on='product_id', how='left')


# In[14]:


cart_details_path = os.path.join(INSIGHTS_DIR, 'cart_details.csv')
category_summary_path = os.path.join(INSIGHTS_DIR, 'category_summary.csv')
user_summary_path = os.path.join(INSIGHTS_DIR, 'user_summary.csv')


# In[15]:


# Write to CSV
user_summary.to_csv(user_summary_path, index=False)
category_summary.to_csv(category_summary_path, index=False)
cart_details.to_csv(cart_details_path, index=False)

print("Insights generated and saved to CSV.")

