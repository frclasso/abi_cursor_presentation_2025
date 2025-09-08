#!/usr/bin/env python3
"""
Generate bad/invalid records for e-commerce application testing.
Creates CSV files with intentionally corrupted data to test data validation.
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

def generate_bad_users(num_users=200):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    users = []
    
    for i in range(num_users):
        # Introduce different types of bad data
        bad_data_type = random.choice([
            'missing_required', 'invalid_email', 'invalid_phone', 'negative_age',
            'invalid_zip', 'empty_strings', 'special_chars', 'duplicate_email'
        ])
        
        user = {
            'user_id': f'U{i+1:06d}',
            'first_name': fake.first_name() if bad_data_type != 'empty_strings' else '',
            'last_name': fake.last_name() if bad_data_type != 'empty_strings' else '',
            'email': generate_bad_email(bad_data_type),
            'phone': generate_bad_phone(bad_data_type),
            'address': fake.street_address() if bad_data_type != 'empty_strings' else '',
            'city': fake.city() if bad_data_type != 'empty_strings' else '',
            'state': fake.state() if bad_data_type != 'empty_strings' else '',
            'zip_code': generate_bad_zip(bad_data_type),
            'country': fake.country() if bad_data_type != 'empty_strings' else '',
            'date_joined': generate_bad_date(bad_data_type),
            'is_active': generate_bad_boolean(bad_data_type),
            'age': generate_bad_age(bad_data_type),
            'gender': generate_bad_gender(bad_data_type)
        }
        
        # Add missing required fields
        if bad_data_type == 'missing_required':
            required_fields = ['first_name', 'last_name', 'email']
            field_to_remove = random.choice(required_fields)
            user[field_to_remove] = None
        
        users.append(user)
    
    return pd.DataFrame(users)

def generate_bad_email(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_email':
        invalid_emails = [
            'notanemail',
            'missing@domain',
            '@missinglocal.com',
            'spaces in@email.com',
            'double@@domain.com',
            'missingdot@domaincom',
            'toolong' + 'a' * 100 + '@domain.com'
        ]
        return random.choice(invalid_emails)
    elif bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'user@domain.com<script>alert("xss")</script>'
    else:
        return fake.email()

def generate_bad_phone(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_phone':
        invalid_phones = [
            '123',  # Too short
            '12345678901234567890',  # Too long
            'abc-def-ghij',  # Letters
            '123-456-789-012-345',  # Too many parts
            '+1-800-INVALID',  # Letters in number
            '123.456.789.012'  # Wrong format
        ]
        return random.choice(invalid_phones)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return fake.phone_number()

def generate_bad_zip(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_zip':
        invalid_zips = [
            '123',  # Too short
            '1234567890',  # Too long
            'abcde',  # Letters
            '1234-567',  # Wrong format
            '00000'  # Invalid zip
        ]
        return random.choice(invalid_zips)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return fake.zipcode()

def generate_bad_date(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'missing_required':
        return None
    elif bad_type == 'empty_strings':
        return ''
    else:
        return fake.date_between(start_date='-2y', end_date='today')

def generate_bad_boolean(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'special_chars':
        invalid_bools = ['yes', 'no', '1', '0', 'true', 'false', 'Y', 'N']
        return random.choice(invalid_bools)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.choice([True, False])

def generate_bad_age(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_age':
        return random.randint(-100, -1)
    elif bad_type == 'special_chars':
        return random.choice(['adult', 'young', 'old', 'teen'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.randint(18, 80)

def generate_bad_gender(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'special_chars':
        invalid_genders = ['MALE', 'FEMALE', '1', '2', 'X', 'Other', 'Prefer not to say']
        return random.choice(invalid_genders)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.choice(['M', 'F', 'Other'])

def generate_bad_products(num_products=100):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
    products = []
    
    for i in range(num_products):
        bad_data_type = random.choice([
            'missing_required', 'negative_price', 'invalid_price', 'empty_strings',
            'special_chars', 'invalid_category', 'negative_stock'
        ])
        
        product = {
            'product_id': f'P{i+1:06d}',
            'name': generate_bad_product_name(bad_data_type),
            'description': generate_bad_description(bad_data_type),
            'category': generate_bad_category(bad_data_type, categories),
            'price': generate_bad_price(bad_data_type),
            'cost': generate_bad_cost(bad_data_type),
            'stock_quantity': generate_bad_stock(bad_data_type),
            'sku': generate_bad_sku(bad_data_type),
            'brand': generate_bad_brand(bad_data_type),
            'weight': generate_bad_weight(bad_data_type),
            'dimensions': generate_bad_dimensions(bad_data_type),
            'is_active': generate_bad_boolean(bad_data_type),
            'created_at': generate_bad_date(bad_data_type)
        }
        
        # Add missing required fields
        if bad_data_type == 'missing_required':
            required_fields = ['name', 'price', 'category']
            field_to_remove = random.choice(required_fields)
            product[field_to_remove] = None
        
        products.append(product)
    
    return pd.DataFrame(products)

def generate_bad_product_name(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'Product<script>alert("xss")</script>'
    else:
        return fake.catch_phrase()

def generate_bad_description(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'Description with <script>alert("xss")</script> and other issues'
    else:
        return fake.text(max_nb_chars=200)

def generate_bad_category(bad_type, valid_categories):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_category':
        invalid_categories = ['InvalidCategory', '123', 'Category with spaces', '']
        return random.choice(invalid_categories)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.choice(valid_categories)

def generate_bad_price(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_price':
        return round(random.uniform(-100, -1), 2)
    elif bad_type == 'invalid_price':
        return random.choice(['free', 'expensive', 'cheap', 'not available'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return round(random.uniform(10, 1000), 2)

def generate_bad_cost(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_price':
        return round(random.uniform(-50, -1), 2)
    elif bad_type == 'invalid_price':
        return random.choice(['unknown', 'variable', 'not set'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return round(random.uniform(5, 500), 2)

def generate_bad_stock(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_stock':
        return random.randint(-100, -1)
    elif bad_type == 'special_chars':
        return random.choice(['many', 'few', 'out of stock', 'available'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.randint(0, 1000)

def generate_bad_sku(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'SKU with spaces and special chars!@#'
    else:
        return fake.bothify(text='SKU-####-????')

def generate_bad_brand(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'Brand<script>alert("xss")</script>'
    else:
        return fake.company()

def generate_bad_weight(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_price':
        return round(random.uniform(-10, -0.1), 2)
    elif bad_type == 'special_chars':
        return random.choice(['heavy', 'light', 'medium'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return round(random.uniform(0.1, 50), 2)

def generate_bad_dimensions(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'large x medium x small'
    else:
        return f"{random.randint(1, 50)}x{random.randint(1, 50)}x{random.randint(1, 50)}"

def generate_bad_sales(num_sales=1000, users_df=None, products_df=None):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if users_df is None or products_df is None:
        raise ValueError("Users and products DataFrames must be provided")
    
    sales = []
    
    for i in range(num_sales):
        bad_data_type = random.choice([
            'missing_required', 'invalid_amounts', 'future_date', 'empty_strings',
            'special_chars', 'invalid_status', 'negative_quantity'
        ])
        
        user = users_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        
        quantity = generate_bad_quantity(bad_data_type)
        unit_price = generate_bad_price(bad_data_type)
        total_amount = quantity * unit_price if isinstance(quantity, (int, float)) and isinstance(unit_price, (int, float)) else 0
        
        discount = generate_bad_discount(bad_data_type)
        discount_value = discount if isinstance(discount, (int, float)) else 0
        
        sale = {
            'sale_id': f'SALE{i+1:08d}',
            'user_id': user['user_id'] if bad_data_type != 'missing_required' else None,
            'product_id': product['product_id'] if bad_data_type != 'missing_required' else None,
            'seller_id': f'S{random.randint(1, 50):04d}',
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': round(total_amount, 2) if isinstance(total_amount, (int, float)) else 0,
            'discount': discount,
            'final_amount': round(total_amount * (1 - discount_value), 2) if isinstance(total_amount, (int, float)) else 0,
            'sale_date': generate_bad_sale_date(bad_data_type),
            'status': generate_bad_status(bad_data_type),
            'shipping_address': generate_bad_address(bad_data_type),
            'shipping_city': generate_bad_city(bad_data_type),
            'shipping_state': generate_bad_state(bad_data_type),
            'shipping_zip': generate_bad_zip(bad_data_type)
        }
        
        sales.append(sale)
    
    return pd.DataFrame(sales)

def generate_bad_quantity(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_quantity':
        return random.randint(-10, -1)
    elif bad_type == 'special_chars':
        return random.choice(['many', 'few', 'some'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.randint(1, 10)

def generate_bad_discount(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_amounts':
        return random.choice([1.5, -0.1, '10%', 'free'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return round(random.uniform(0, 0.25), 2)

def generate_bad_sale_date(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'future_date':
        return fake.date_between(start_date='today', end_date='+1y')
    elif bad_type == 'empty_strings':
        return ''
    else:
        return fake.date_between(start_date='-1y', end_date='today')

def generate_bad_status(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_status':
        invalid_statuses = ['shipped', 'delivered', 'processing', '1', '0', 'yes', 'no']
        return random.choice(invalid_statuses)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.choices(['completed', 'pending', 'cancelled'], weights=[85, 10, 5])[0]

def generate_bad_address(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'Address<script>alert("xss")</script>'
    else:
        return fake.street_address()

def generate_bad_city(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'City<script>alert("xss")</script>'
    else:
        return fake.city()

def generate_bad_state(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'State<script>alert("xss")</script>'
    else:
        return fake.state()

def generate_bad_payments(sales_df=None):
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
        if sale['status'] == 'cancelled' or pd.isna(sale['status']):
            continue
            
        bad_data_type = random.choice([
            'missing_required', 'invalid_amounts', 'future_date', 'empty_strings',
            'special_chars', 'invalid_method', 'negative_amount'
        ])
        
        num_payments = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
        remaining_amount = sale['final_amount'] if isinstance(sale['final_amount'], (int, float)) else 100
        
        for j in range(num_payments):
            if remaining_amount <= 0:
                break
                
            payment_amount = generate_bad_payment_amount(bad_data_type, remaining_amount)
            remaining_amount -= payment_amount if isinstance(payment_amount, (int, float)) else 0
            
            payment = {
                'payment_id': f'PAY{i+1:08d}_{j+1}',
                'sale_id': sale['sale_id'] if bad_data_type != 'missing_required' else None,
                'amount': payment_amount,
                'payment_method': generate_bad_payment_method(bad_data_type, payment_methods),
                'payment_date': generate_bad_payment_date(bad_data_type, sale.get('sale_date')),
                'status': generate_bad_payment_status(bad_data_type),
                'transaction_id': generate_bad_transaction_id(bad_data_type),
                'card_last_four': generate_bad_card_last_four(bad_data_type)
            }
            payments.append(payment)
    
    return pd.DataFrame(payments)

def generate_bad_payment_amount(bad_type, remaining_amount):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'negative_amount':
        return round(random.uniform(-100, -1), 2)
    elif bad_type == 'invalid_amounts':
        return random.choice(['free', 'expensive', 'not set'])
    elif bad_type == 'empty_strings':
        return ''
    else:
        return round(random.uniform(0.1, remaining_amount), 2)

def generate_bad_payment_method(bad_type, valid_methods):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'invalid_method':
        invalid_methods = ['bitcoin', 'check', 'money_order', 'invalid']
        return random.choice(invalid_methods)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.choice(valid_methods)

def generate_bad_payment_date(bad_type, sale_date):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'future_date':
        return fake.date_between(start_date='today', end_date='+1y')
    elif bad_type == 'empty_strings':
        return ''
    else:
        if sale_date and not pd.isna(sale_date):
            return sale_date + timedelta(days=random.randint(0, 7))
        else:
            return fake.date_between(start_date='-1y', end_date='today')

def generate_bad_payment_status(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'special_chars':
        invalid_statuses = ['paid', 'unpaid', '1', '0', 'yes', 'no']
        return random.choice(invalid_statuses)
    elif bad_type == 'empty_strings':
        return ''
    else:
        return random.choices(['completed', 'pending', 'failed'], weights=[90, 7, 3])[0]

def generate_bad_transaction_id(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'TXN<script>alert("xss")</script>'
    else:
        return fake.bothify(text='TXN-########')

def generate_bad_card_last_four(bad_type):
            """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
    if bad_type == 'empty_strings':
        return ''
    elif bad_type == 'special_chars':
        return 'abcd'
    else:
        return fake.bothify(text='####')

def main():
            """
        Main.
        
        Performs the main operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("Creating directories...")
    create_directories()
    
    print("Generating bad users data...")
    bad_users_df = generate_bad_users(200)
    
    print("Generating bad products data...")
    bad_products_df = generate_bad_products(100)
    
    print("Generating bad sales data...")
    bad_sales_df = generate_bad_sales(1000, bad_users_df, bad_products_df)
    
    print("Generating bad payments data...")
    bad_payments_df = generate_bad_payments(bad_sales_df)
    
    # Save to CSV files with 'bad_' prefix
    print("Saving bad data to CSV files...")
    bad_users_df.to_csv('tests/data_sources/bad_users.csv', index=False)
    bad_products_df.to_csv('tests/data_sources/bad_products.csv', index=False)
    bad_sales_df.to_csv('tests/data_sources/bad_sales.csv', index=False)
    bad_payments_df.to_csv('tests/data_sources/bad_payments.csv', index=False)
    
    print("Bad data generation completed!")
    print(f"Generated {len(bad_users_df)} bad users")
    print(f"Generated {len(bad_products_df)} bad products")
    print(f"Generated {len(bad_sales_df)} bad sales")
    print(f"Generated {len(bad_payments_df)} bad payments")
    
    # Display sample bad data
    print("\nSample bad users data:")
    print(bad_users_df.head())
    
    print("\nSample bad products data:")
    print(bad_products_df.head())
    
    print("\nSample bad sales data:")
    print(bad_sales_df.head())
    
    print("\nSample bad payments data:")
    print(bad_payments_df.head())

if __name__ == "__main__":
    main()
