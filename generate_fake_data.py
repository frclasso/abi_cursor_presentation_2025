#!/usr/bin/env python3
"""
Generate fake valid data for e-commerce application.
Creates CSV files with users, products, sellers, sales, and payments data.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Initialize Faker
fake = Faker()

def create_directories():
            """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
    os.makedirs('tests/data_sources', exist_ok=True)
    os.makedirs('images', exist_ok=True)

def generate_users(num_users=1000):
    """
    Generate fake users data for e-commerce application.
    
    Creates a DataFrame with realistic user data including personal information,
    contact details, and account status. Uses Faker library for realistic data
    generation with proper formatting and constraints.
    
    Args:
        num_users (int): Number of users to generate (default: 1000)
        
    Returns:
        pd.DataFrame: DataFrame containing user data with columns:
            user_id, first_name, last_name, email, phone, address, city,
            state, zip_code, country, date_joined, is_active, age, gender
    """
    users = []
    
    for i in range(num_users):
        user = {
            'user_id': f'U{i+1:06d}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'country': fake.country(),
            'date_joined': fake.date_between(start_date='-2y', end_date='today'),
            'is_active': random.choice([True, True, True, False]),  # 75% active
            'age': random.randint(18, 80),
            'gender': random.choice(['M', 'F', 'Other'])
        }
        users.append(user)
    
    return pd.DataFrame(users)

def generate_products(num_products=500):
    """
    Generate fake products data for e-commerce application.
    
    Creates a DataFrame with realistic product data including product information,
    pricing, inventory, and categorization. Uses Faker library for realistic
    product names, descriptions, and other attributes.
    
    Args:
        num_products (int): Number of products to generate (default: 500)
        
    Returns:
        pd.DataFrame: DataFrame containing product data with columns:
            product_id, name, description, category, price, cost, stock_quantity,
            sku, brand, weight, dimensions, is_active, created_at
    """
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 
                  'Beauty', 'Toys', 'Automotive', 'Health', 'Food']
    
    products = []
    
    for i in range(num_products):
        category = random.choice(categories)
        product = {
            'product_id': f'P{i+1:06d}',
            'name': fake.catch_phrase(),
            'description': fake.text(max_nb_chars=200),
            'category': category,
            'price': round(random.uniform(10, 1000), 2),
            'cost': round(random.uniform(5, 500), 2),
            'stock_quantity': random.randint(0, 1000),
            'sku': fake.bothify(text='SKU-####-????'),
            'brand': fake.company(),
            'weight': round(random.uniform(0.1, 50), 2),
            'dimensions': f"{random.randint(1, 50)}x{random.randint(1, 50)}x{random.randint(1, 50)}",
            'is_active': random.choice([True, True, False]),  # 67% active
            'created_at': fake.date_between(start_date='-1y', end_date='today')
        }
        products.append(product)
    
    return pd.DataFrame(products)

def generate_sellers(num_sellers=50):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    sellers = []
    
    for i in range(num_sellers):
        seller = {
            'seller_id': f'S{i+1:04d}',
            'company_name': fake.company(),
            'contact_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'country': fake.country(),
            'tax_id': fake.bothify(text='##-#######'),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'total_sales': random.randint(0, 1000000),
            'is_verified': random.choice([True, True, False]),  # 67% verified
            'joined_date': fake.date_between(start_date='-2y', end_date='today')
        }
        sellers.append(seller)
    
    return pd.DataFrame(sellers)

def generate_sales(num_sales=5000, users_df=None, products_df=None, sellers_df=None):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if users_df is None or products_df is None or sellers_df is None:
        raise ValueError("Users, products, and sellers DataFrames must be provided")
    
    sales = []
    
    for i in range(num_sales):
        user = users_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        seller = sellers_df.sample(1).iloc[0]
        
        quantity = random.randint(1, 10)
        unit_price = product['price']
        total_amount = quantity * unit_price
        
        # Add some discount occasionally
        discount = 0
        if random.random() < 0.3:  # 30% chance of discount
            discount = round(random.uniform(0.05, 0.25), 2)
        
        final_amount = total_amount * (1 - discount)
        
        sale = {
            'sale_id': f'SALE{i+1:08d}',
            'user_id': user['user_id'],
            'product_id': product['product_id'],
            'seller_id': seller['seller_id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': round(total_amount, 2),
            'discount': discount,
            'final_amount': round(final_amount, 2),
            'sale_date': fake.date_between(start_date='-1y', end_date='today'),
            'status': random.choices(['completed', 'pending', 'cancelled'], weights=[85, 10, 5])[0],
            'shipping_address': fake.street_address(),
            'shipping_city': fake.city(),
            'shipping_state': fake.state(),
            'shipping_zip': fake.zipcode()
        }
        sales.append(sale)
    
    return pd.DataFrame(sales)

def generate_payments(sales_df=None):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if sales_df is None:
        raise ValueError("Sales DataFrame must be provided")
    
    payments = []
    payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash']
    
    for i, sale in sales_df.iterrows():
        if sale['status'] == 'cancelled':
            continue  # Skip cancelled sales
            
        # Generate 1-3 payments per sale (some sales might have partial payments)
        num_payments = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
        remaining_amount = sale['final_amount']
        
        for j in range(num_payments):
            if remaining_amount <= 0:
                break
                
            payment_amount = remaining_amount if j == num_payments - 1 else round(random.uniform(0.1, remaining_amount), 2)
            remaining_amount -= payment_amount
            
            payment = {
                'payment_id': f'PAY{i+1:08d}_{j+1}',
                'sale_id': sale['sale_id'],
                'amount': round(payment_amount, 2),
                'payment_method': random.choice(payment_methods),
                'payment_date': sale['sale_date'] + timedelta(days=random.randint(0, 7)),
                'status': random.choices(['completed', 'pending', 'failed'], weights=[90, 7, 3])[0],
                'transaction_id': fake.bothify(text='TXN-########'),
                'card_last_four': fake.bothify(text='####') if random.choice(payment_methods) in ['credit_card', 'debit_card'] else None
            }
            payments.append(payment)
    
    return pd.DataFrame(payments)

def main():
            """
        Main.
        
        Performs the main operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("Creating directories...")
    create_directories()
    
    print("Generating users data...")
    users_df = generate_users(1000)
    
    print("Generating products data...")
    products_df = generate_products(500)
    
    print("Generating sellers data...")
    sellers_df = generate_sellers(50)
    
    print("Generating sales data...")
    sales_df = generate_sales(5000, users_df, products_df, sellers_df)
    
    print("Generating payments data...")
    payments_df = generate_payments(sales_df)
    
    # Save to CSV files
    print("Saving data to CSV files...")
    users_df.to_csv('tests/data_sources/users.csv', index=False)
    products_df.to_csv('tests/data_sources/products.csv', index=False)
    sellers_df.to_csv('tests/data_sources/sellers.csv', index=False)
    sales_df.to_csv('tests/data_sources/sales.csv', index=False)
    payments_df.to_csv('tests/data_sources/payments.csv', index=False)
    
    print("Data generation completed!")
    print(f"Generated {len(users_df)} users")
    print(f"Generated {len(products_df)} products")
    print(f"Generated {len(sellers_df)} sellers")
    print(f"Generated {len(sales_df)} sales")
    print(f"Generated {len(payments_df)} payments")
    
    # Display sample data
    print("\nSample users data:")
    print(users_df.head())
    
    print("\nSample products data:")
    print(products_df.head())
    
    print("\nSample sales data:")
    print(sales_df.head())
    
    print("\nSample payments data:")
    print(payments_df.head())

if __name__ == "__main__":
    main()
