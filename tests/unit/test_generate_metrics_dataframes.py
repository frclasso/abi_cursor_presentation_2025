"""
Unit tests for generate_metrics_dataframes.py using pytest fixtures.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from generate_metrics_dataframes import (
    generate_users, generate_products, generate_sellers, 
    generate_sales, generate_payments, main
)
from tests.fixtures.test_data import (
    sample_users_data, sample_products_data, sample_sales_data, 
    sample_payments_data, temp_directories
)

class TestGenerateMetricsDataframes:
    """Test cases for generate_metrics_dataframes.py functions."""
    
    def test_generate_users(self):
        """Test users data generation."""
        users_df = generate_users(10)
        
        assert len(users_df) == 10
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
        
        # Check age range
        assert all(users_df['age'] >= 18)
        assert all(users_df['age'] <= 80)
        
        # Check gender values
        assert all(users_df['gender'].isin(['M', 'F', 'Other']))
    
    def test_generate_products(self):
        """Test products data generation."""
        products_df = generate_products(10)
        
        assert len(products_df) == 10
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
        
        # Check stock quantity is non-negative
        assert all(products_df['stock_quantity'] >= 0)
        
        # Check weight is positive
        assert all(products_df['weight'] > 0)
    
    def test_generate_sellers(self):
        """Test sellers data generation."""
        sellers_df = generate_sellers(5)
        
        assert len(sellers_df) == 5
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
        
        # Check total_sales is non-negative
        assert all(sellers_df['total_sales'] >= 0)
    
    def test_generate_sales(self, sample_users_data, sample_products_data):
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
    
    def test_generate_sales_with_invalid_inputs(self, sample_users_data, sample_products_data):
        """Test sales generation with invalid inputs."""
        with pytest.raises(ValueError, match="Users, products, and sellers DataFrames must be provided"):
            generate_sales(5, None, sample_products_data, pd.DataFrame())
        
        with pytest.raises(ValueError, match="Users, products, and sellers DataFrames must be provided"):
            generate_sales(5, sample_users_data, None, pd.DataFrame())
        
        with pytest.raises(ValueError, match="Users, products, and sellers DataFrames must be provided"):
            generate_sales(5, sample_users_data, sample_products_data, None)
    
    def test_generate_payments(self, sample_sales_data):
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
    @patch('generate_metrics_dataframes.generate_payments')
    @patch('generate_metrics_dataframes.generate_sales')
    @patch('generate_metrics_dataframes.generate_sellers')
    @patch('generate_metrics_dataframes.generate_products')
    @patch('generate_metrics_dataframes.generate_users')
    def test_main_function(self, mock_generate_users, mock_generate_products, 
                          mock_generate_sellers, mock_generate_sales, 
                          mock_generate_payments, mock_makedirs, mock_to_csv, 
                          sample_users_data, sample_products_data, sample_sales_data, sample_payments_data):
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
