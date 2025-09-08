"""
Unit tests for generate_fake_data.py using pytest mocking.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock, call
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from generate_fake_data import (
    generate_users, generate_products, generate_sellers, 
    generate_sales, generate_payments, main, create_directories
)
from tests.fixtures.test_data import (
    sample_users_data, sample_products_data, sample_sales_data, 
    sample_payments_data, temp_directories
)

class TestGenerateFakeData:
    """Test cases for generate_fake_data.py functions."""
    
    @patch('os.makedirs')
    def test_create_directories(self, mock_makedirs):
        """Test directory creation."""
        create_directories()
        mock_makedirs.assert_any_call('tests/data_sources', exist_ok=True)
        mock_makedirs.assert_any_call('images', exist_ok=True)
    
    @patch('generate_fake_data.fake')
    def test_generate_users(self, mock_fake):
        """Test users data generation with mocked Faker."""
        # Mock Faker methods
        mock_fake.first_name.side_effect = ['John', 'Jane', 'Bob']
        mock_fake.last_name.side_effect = ['Doe', 'Smith', 'Johnson']
        mock_fake.email.side_effect = ['john@example.com', 'jane@example.com', 'bob@example.com']
        mock_fake.phone_number.side_effect = ['123-456-7890', '098-765-4321', '555-123-4567']
        mock_fake.street_address.side_effect = ['123 Main St', '456 Oak Ave', '789 Pine Rd']
        mock_fake.city.side_effect = ['New York', 'Los Angeles', 'Chicago']
        mock_fake.state.side_effect = ['NY', 'CA', 'IL']
        mock_fake.zipcode.side_effect = ['10001', '90210', '60601']
        mock_fake.country.side_effect = ['USA', 'USA', 'USA']
        mock_fake.date_between.side_effect = ['2024-01-01', '2024-01-02', '2024-01-03']
        
        users_df = generate_users(3)
        
        assert len(users_df) == 3
        assert 'user_id' in users_df.columns
        assert 'first_name' in users_df.columns
        assert 'last_name' in users_df.columns
        assert 'email' in users_df.columns
        assert 'phone' in users_df.columns
        assert 'address' in users_df.columns
        assert 'city' in users_df.columns
        assert 'state' in users_df.columns
        assert 'zip_code' in users_df.columns
        assert 'country' in users_df.columns
        assert 'date_joined' in users_df.columns
        assert 'is_active' in users_df.columns
        assert 'age' in users_df.columns
        assert 'gender' in users_df.columns
        
        # Check user_id format
        assert all(users_df['user_id'].str.startswith('U'))
        assert all(users_df['user_id'].str.len() == 7)  # U + 6 digits
        
        # Verify Faker was called
        assert mock_fake.first_name.call_count == 3
        assert mock_fake.last_name.call_count == 3
        assert mock_fake.email.call_count == 3
    
    @patch('generate_fake_data.fake')
    def test_generate_products(self, mock_fake):
        """Test products data generation with mocked Faker."""
        # Mock Faker methods
        mock_fake.catch_phrase.side_effect = ['Product A', 'Product B', 'Product C']
        mock_fake.text.side_effect = ['Description A', 'Description B', 'Description C']
        mock_fake.bothify.side_effect = ['SKU-001', 'SKU-002', 'SKU-003']
        mock_fake.company.side_effect = ['Brand A', 'Brand B', 'Brand C']
        mock_fake.date_between.side_effect = ['2024-01-01', '2024-01-02', '2024-01-03']
        
        products_df = generate_products(3)
        
        assert len(products_df) == 3
        assert 'product_id' in products_df.columns
        assert 'name' in products_df.columns
        assert 'description' in products_df.columns
        assert 'category' in products_df.columns
        assert 'price' in products_df.columns
        assert 'cost' in products_df.columns
        assert 'stock_quantity' in products_df.columns
        assert 'sku' in products_df.columns
        assert 'brand' in products_df.columns
        assert 'weight' in products_df.columns
        assert 'dimensions' in products_df.columns
        assert 'is_active' in products_df.columns
        assert 'created_at' in products_df.columns
        
        # Check product_id format
        assert all(products_df['product_id'].str.startswith('P'))
        assert all(products_df['product_id'].str.len() == 7)  # P + 6 digits
        
        # Check price and cost are positive
        assert all(products_df['price'] > 0)
        assert all(products_df['cost'] > 0)
        
        # Verify Faker was called
        assert mock_fake.catch_phrase.call_count == 3
        assert mock_fake.text.call_count == 3
        assert mock_fake.bothify.call_count == 3
    
    @patch('generate_fake_data.fake')
    def test_generate_sellers(self, mock_fake):
        """Test sellers data generation with mocked Faker."""
        # Mock Faker methods
        mock_fake.company.side_effect = ['Company A', 'Company B', 'Company C']
        mock_fake.name.side_effect = ['John Doe', 'Jane Smith', 'Bob Johnson']
        mock_fake.email.side_effect = ['company1@example.com', 'company2@example.com', 'company3@example.com']
        mock_fake.phone_number.side_effect = ['123-456-7890', '098-765-4321', '555-123-4567']
        mock_fake.street_address.side_effect = ['123 Main St', '456 Oak Ave', '789 Pine Rd']
        mock_fake.city.side_effect = ['New York', 'Los Angeles', 'Chicago']
        mock_fake.state.side_effect = ['NY', 'CA', 'IL']
        mock_fake.zipcode.side_effect = ['10001', '90210', '60601']
        mock_fake.country.side_effect = ['USA', 'USA', 'USA']
        mock_fake.bothify.side_effect = ['12-3456789', '23-4567890', '34-5678901']
        mock_fake.date_between.side_effect = ['2024-01-01', '2024-01-02', '2024-01-03']
        
        sellers_df = generate_sellers(3)
        
        assert len(sellers_df) == 3
        assert 'seller_id' in sellers_df.columns
        assert 'company_name' in sellers_df.columns
        assert 'contact_name' in sellers_df.columns
        assert 'email' in sellers_df.columns
        assert 'phone' in sellers_df.columns
        assert 'address' in sellers_df.columns
        assert 'city' in sellers_df.columns
        assert 'state' in sellers_df.columns
        assert 'zip_code' in sellers_df.columns
        assert 'country' in sellers_df.columns
        assert 'tax_id' in sellers_df.columns
        assert 'rating' in sellers_df.columns
        assert 'total_sales' in sellers_df.columns
        assert 'is_verified' in sellers_df.columns
        assert 'joined_date' in sellers_df.columns
        
        # Check seller_id format
        assert all(sellers_df['seller_id'].str.startswith('S'))
        assert all(sellers_df['seller_id'].str.len() == 5)  # S + 4 digits
        
        # Check rating range
        assert all(sellers_df['rating'] >= 3.0)
        assert all(sellers_df['rating'] <= 5.0)
        
        # Verify Faker was called
        assert mock_fake.company.call_count == 3
        assert mock_fake.name.call_count == 3
        assert mock_fake.email.call_count == 3
    
    def test_generate_sales(self):
        """Test sales data generation."""
        users_df = sample_users_data
        products_df = sample_products_data
        sellers_df = pd.DataFrame({
            'seller_id': ['S0001', 'S0002', 'S0003'],
            'company_name': ['Company A', 'Company B', 'Company C']
        })
        
        sales_df = generate_sales(5, users_df, products_df, sellers_df)
        
        assert len(sales_df) == 5
        assert 'sale_id' in sales_df.columns
        assert 'user_id' in sales_df.columns
        assert 'product_id' in sales_df.columns
        assert 'seller_id' in sales_df.columns
        assert 'quantity' in sales_df.columns
        assert 'unit_price' in sales_df.columns
        assert 'total_amount' in sales_df.columns
        assert 'discount' in sales_df.columns
        assert 'final_amount' in sales_df.columns
        assert 'sale_date' in sales_df.columns
        assert 'status' in sales_df.columns
        assert 'shipping_address' in sales_df.columns
        assert 'shipping_city' in sales_df.columns
        assert 'shipping_state' in sales_df.columns
        assert 'shipping_zip' in sales_df.columns
        
        # Check sale_id format
        assert all(sales_df['sale_id'].str.startswith('SALE'))
        assert all(sales_df['sale_id'].str.len() == 12)  # SALE + 8 digits
        
        # Check quantity is positive
        assert all(sales_df['quantity'] > 0)
        
        # Check amounts are positive
        assert all(sales_df['unit_price'] > 0)
        assert all(sales_df['total_amount'] > 0)
        assert all(sales_df['final_amount'] > 0)
        
        # Check discount range
        assert all(sales_df['discount'] >= 0)
        assert all(sales_df['discount'] <= 1)
        
        # Check status values
        assert all(sales_df['status'].isin(['completed', 'pending', 'cancelled']))
    
    def test_generate_sales_with_invalid_inputs(self):
        """Test sales generation with invalid inputs."""
        with pytest.raises(ValueError, match="Users, products, and sellers DataFrames must be provided"):
            generate_sales(5, None, sample_products_data, pd.DataFrame())
        
        with pytest.raises(ValueError, match="Users, products, and sellers DataFrames must be provided"):
            generate_sales(5, sample_users_data, None, pd.DataFrame())
        
        with pytest.raises(ValueError, match="Users, products, and sellers DataFrames must be provided"):
            generate_sales(5, sample_users_data, sample_products_data, None)
    
    def test_generate_payments(self):
        """Test payments data generation."""
        sales_df = sample_sales_data
        payments_df = generate_payments(sales_df)
        
        assert len(payments_df) > 0
        assert 'payment_id' in payments_df.columns
        assert 'sale_id' in payments_df.columns
        assert 'amount' in payments_df.columns
        assert 'payment_method' in payments_df.columns
        assert 'payment_date' in payments_df.columns
        assert 'status' in payments_df.columns
        assert 'transaction_id' in payments_df.columns
        assert 'card_last_four' in payments_df.columns
        
        # Check payment_id format
        assert all(payments_df['payment_id'].str.startswith('PAY'))
        
        # Check amount is positive
        assert all(payments_df['amount'] > 0)
        
        # Check payment method values
        valid_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash']
        assert all(payments_df['payment_method'].isin(valid_methods))
        
        # Check status values
        assert all(payments_df['status'].isin(['completed', 'pending', 'failed']))
    
    def test_generate_payments_with_invalid_input(self):
        """Test payments generation with invalid input."""
        with pytest.raises(ValueError, match="Sales DataFrame must be provided"):
            generate_payments(None)
    
    @patch('pandas.DataFrame.to_csv')
    @patch('os.makedirs')
    @patch('generate_fake_data.generate_payments')
    @patch('generate_fake_data.generate_sales')
    @patch('generate_fake_data.generate_sellers')
    @patch('generate_fake_data.generate_products')
    @patch('generate_fake_data.generate_users')
    def test_main_function(self, mock_generate_users, mock_generate_products, 
                          mock_generate_sellers, mock_generate_sales, 
                          mock_generate_payments, mock_makedirs, mock_to_csv):
        """Test main function execution."""
        # Mock return values
        mock_generate_users.return_value = sample_users_data
        mock_generate_products.return_value = sample_products_data
        mock_generate_sellers.return_value = pd.DataFrame({'seller_id': ['S0001']})
        mock_generate_sales.return_value = sample_sales_data
        mock_generate_payments.return_value = sample_payments_data
        
        # Run main function
        main()
        
        # Verify functions were called
        mock_makedirs.assert_called()
        mock_generate_users.assert_called_once_with(1000)
        mock_generate_products.assert_called_once_with(500)
        mock_generate_sellers.assert_called_once_with(50)
        mock_generate_sales.assert_called_once()
        mock_generate_payments.assert_called_once()
        
        # Verify CSV files were saved
        assert mock_to_csv.call_count == 5  # users, products, sellers, sales, payments
    
    @patch('pandas.DataFrame.to_csv')
    @patch('os.makedirs')
    def test_main_function_with_error(self, mock_makedirs, mock_to_csv):
        """Test main function with error handling."""
        # Make to_csv raise an exception
        mock_to_csv.side_effect = Exception("CSV write error")
        
        # This should not raise an exception, but handle it gracefully
        try:
            main()
        except Exception as e:
            pytest.fail(f"Main function should handle errors gracefully, but raised: {e}")
    
    def test_data_consistency(self):
        """Test data consistency across generated datasets."""
        users_df = generate_users(100)
        products_df = generate_products(50)
        sellers_df = generate_sellers(10)
        sales_df = generate_sales(200, users_df, products_df, sellers_df)
        payments_df = generate_payments(sales_df)
        
        # Check that all user_ids in sales exist in users
        sales_user_ids = set(sales_df['user_id'].unique())
        users_user_ids = set(users_df['user_id'].unique())
        assert sales_user_ids.issubset(users_user_ids)
        
        # Check that all product_ids in sales exist in products
        sales_product_ids = set(sales_df['product_id'].unique())
        products_product_ids = set(products_df['product_id'].unique())
        assert sales_product_ids.issubset(products_product_ids)
        
        # Check that all sale_ids in payments exist in sales
        payments_sale_ids = set(payments_df['sale_id'].unique())
        sales_sale_ids = set(sales_df['sale_id'].unique())
        assert payments_sale_ids.issubset(sales_sale_ids)
    
    def test_data_types(self):
        """Test that generated data has correct types."""
        users_df = generate_users(10)
        products_df = generate_products(10)
        
        # Check numeric columns
        assert users_df['age'].dtype in ['int64', 'int32']
        assert products_df['price'].dtype in ['float64', 'float32']
        assert products_df['cost'].dtype in ['float64', 'float32']
        assert products_df['stock_quantity'].dtype in ['int64', 'int32']
        
        # Check string columns
        assert users_df['first_name'].dtype == 'object'
        assert users_df['email'].dtype == 'object'
        assert products_df['name'].dtype == 'object'
        assert products_df['category'].dtype == 'object'
        
        # Check boolean columns
        assert users_df['is_active'].dtype == 'bool'
        assert products_df['is_active'].dtype == 'bool'
    
    def test_data_ranges(self):
        """Test that generated data is within expected ranges."""
        users_df = generate_users(1000)
        products_df = generate_products(100)
        
        # Age should be between 18 and 80
        assert users_df['age'].min() >= 18
        assert users_df['age'].max() <= 80
        
        # Price should be positive
        assert products_df['price'].min() > 0
        assert products_df['price'].max() <= 1000  # Based on the generation logic
        
        # Cost should be positive and less than price
        assert products_df['cost'].min() > 0
        assert all(products_df['cost'] <= products_df['price'])
        
        # Stock quantity should be non-negative
        assert products_df['stock_quantity'].min() >= 0
        assert products_df['stock_quantity'].max() <= 1000  # Based on the generation logic
    
    @patch('generate_fake_data.random')
    def test_random_choices(self, mock_random):
        """Test that random choices are properly used."""
        # Mock random choices
        mock_random.choice.side_effect = ['M', 'F', 'Other']
        mock_random.randint.side_effect = [25, 30, 35]
        mock_random.choices.side_effect = [['completed'], ['pending'], ['cancelled']]
        
        users_df = generate_users(3)
        
        # Verify random was called
        assert mock_random.choice.called
        assert mock_random.randint.called
        assert mock_random.choices.called
    
    def test_discount_calculation(self):
        """Test that discount calculation works correctly."""
        users_df = sample_users_data
        products_df = sample_products_data
        sellers_df = pd.DataFrame({
            'seller_id': ['S0001'],
            'company_name': ['Company A']
        })
        
        sales_df = generate_sales(10, users_df, products_df, sellers_df)
        
        # Check that final_amount is calculated correctly
        for _, row in sales_df.iterrows():
            expected_final = row['total_amount'] * (1 - row['discount'])
            assert abs(row['final_amount'] - expected_final) < 0.01  # Allow for floating point precision
    
    def test_payment_generation_logic(self):
        """Test that payment generation follows the expected logic."""
        sales_df = pd.DataFrame({
            'sale_id': ['SALE000001', 'SALE000002', 'SALE000003'],
            'status': ['completed', 'cancelled', 'completed'],
            'final_amount': [100.0, 50.0, 75.0],
            'sale_date': ['2024-01-15', '2024-01-16', '2024-01-17']
        })
        
        payments_df = generate_payments(sales_df)
        
        # Check that cancelled sales don't have payments
        cancelled_sale_ids = sales_df[sales_df['status'] == 'cancelled']['sale_id'].tolist()
        cancelled_payments = payments_df[payments_df['sale_id'].isin(cancelled_sale_ids)]
        assert len(cancelled_payments) == 0
        
        # Check that completed sales have payments
        completed_sale_ids = sales_df[sales_df['status'] == 'completed']['sale_id'].tolist()
        completed_payments = payments_df[payments_df['sale_id'].isin(completed_sale_ids)]
        assert len(completed_payments) > 0
