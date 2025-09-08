"""
Unit tests for generate_bad_records.py using pytest mocking.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock, call
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from generate_bad_records import (
    generate_bad_users, generate_bad_products, generate_bad_sales, 
    generate_bad_payments, main, create_directories
)
from tests.fixtures.test_data import (
    sample_users_data, sample_products_data, sample_sales_data, 
    sample_payments_data, sample_bad_users_data, sample_bad_products_data,
    temp_directories
)

class TestGenerateBadRecords:
    """Test cases for generate_bad_records.py functions."""
    
    @patch('os.makedirs')
    def test_create_directories(self, mock_makedirs):
        """Test directory creation."""
        create_directories()
        mock_makedirs.assert_any_call('tests/data_sources', exist_ok=True)
        mock_makedirs.assert_any_call('images', exist_ok=True)
    
    def test_generate_bad_users(self):
        """Test bad users data generation."""
        bad_users_df = generate_bad_users(10)
        
        assert len(bad_users_df) == 10
        assert 'user_id' in bad_users_df.columns
        assert 'first_name' in bad_users_df.columns
        assert 'last_name' in bad_users_df.columns
        assert 'email' in bad_users_df.columns
        assert 'phone' in bad_users_df.columns
        assert 'address' in bad_users_df.columns
        assert 'city' in bad_users_df.columns
        assert 'state' in bad_users_df.columns
        assert 'zip_code' in bad_users_df.columns
        assert 'country' in bad_users_df.columns
        assert 'date_joined' in bad_users_df.columns
        assert 'is_active' in bad_users_df.columns
        assert 'age' in bad_users_df.columns
        assert 'gender' in bad_users_df.columns
        
        # Check that some data quality issues are present
        has_empty_strings = (bad_users_df == '').any().any()
        has_invalid_emails = bad_users_df['email'].str.contains('@', na=False).sum() < len(bad_users_df)
        has_negative_ages = (bad_users_df['age'] < 0).any()
        
        # At least one of these issues should be present
        assert has_empty_strings or has_invalid_emails or has_negative_ages
    
    def test_generate_bad_products(self):
        """Test bad products data generation."""
        bad_products_df = generate_bad_products(10)
        
        assert len(bad_products_df) == 10
        assert 'product_id' in bad_products_df.columns
        assert 'name' in bad_products_df.columns
        assert 'description' in bad_products_df.columns
        assert 'category' in bad_products_df.columns
        assert 'price' in bad_products_df.columns
        assert 'cost' in bad_products_df.columns
        assert 'stock_quantity' in bad_products_df.columns
        assert 'sku' in bad_products_df.columns
        assert 'brand' in bad_products_df.columns
        assert 'weight' in bad_products_df.columns
        assert 'dimensions' in bad_products_df.columns
        assert 'is_active' in bad_products_df.columns
        assert 'created_at' in bad_products_df.columns
        
        # Check that some data quality issues are present
        has_empty_strings = (bad_products_df == '').any().any()
        has_negative_prices = (bad_products_df['price'] < 0).any()
        has_negative_stock = (bad_products_df['stock_quantity'] < 0).any()
        has_xss_attempts = bad_products_df['name'].str.contains('<script>', na=False).any()
        
        # At least one of these issues should be present
        assert has_empty_strings or has_negative_prices or has_negative_stock or has_xss_attempts
    
    def test_generate_bad_sales(self, sample_bad_users_data, sample_bad_products_data):
        """Test bad sales data generation."""
        bad_users_df = sample_bad_users_data
        bad_products_df = sample_bad_products_data
        bad_sellers_df = pd.DataFrame({
            'seller_id': ['S0001', 'S0002', 'S0003'],
            'company_name': ['Company A', 'Company B', 'Company C']
        })
        
        bad_sales_df = generate_bad_sales(10, bad_users_df, bad_products_df, bad_sellers_df)
        
        assert len(bad_sales_df) == 10
        assert 'sale_id' in bad_sales_df.columns
        assert 'user_id' in bad_sales_df.columns
        assert 'product_id' in bad_sales_df.columns
        assert 'seller_id' in bad_sales_df.columns
        assert 'quantity' in bad_sales_df.columns
        assert 'unit_price' in bad_sales_df.columns
        assert 'total_amount' in bad_sales_df.columns
        assert 'discount' in bad_sales_df.columns
        assert 'final_amount' in bad_sales_df.columns
        assert 'sale_date' in bad_sales_df.columns
        assert 'status' in bad_sales_df.columns
        assert 'shipping_address' in bad_sales_df.columns
        assert 'shipping_city' in bad_sales_df.columns
        assert 'shipping_state' in bad_sales_df.columns
        assert 'shipping_zip' in bad_sales_df.columns
        
        # Check that some data quality issues are present
        has_null_values = bad_sales_df.isnull().any().any()
        has_negative_quantities = (bad_sales_df['quantity'] < 0).any()
        has_invalid_amounts = (bad_sales_df['total_amount'] < 0).any()
        has_invalid_status = ~bad_sales_df['status'].isin(['completed', 'pending', 'cancelled']).any()
        
        # At least one of these issues should be present
        assert has_null_values or has_negative_quantities or has_invalid_amounts or has_invalid_status
    
    def test_generate_bad_sales_with_invalid_inputs(self, sample_products_data):
        """Test bad sales generation with invalid inputs."""
        with pytest.raises(ValueError, match="Users and products DataFrames must be provided"):
            generate_bad_sales(5, None, sample_products_data)
        
        with pytest.raises(ValueError, match="Users and products DataFrames must be provided"):
            generate_bad_sales(5, sample_users_data, None)
    
    def test_generate_bad_payments(self):
        """Test bad payments data generation."""
        bad_sales_df = pd.DataFrame({
            'sale_id': ['SALE000001', 'SALE000002', 'SALE000003'],
            'status': ['completed', 'pending', 'completed'],
            'final_amount': [100.0, 50.0, 75.0],
            'sale_date': ['2024-01-15', '2024-01-16', '2024-01-17']
        })
        
        bad_payments_df = generate_bad_payments(bad_sales_df)
        
        assert len(bad_payments_df) > 0
        assert 'payment_id' in bad_payments_df.columns
        assert 'sale_id' in bad_payments_df.columns
        assert 'amount' in bad_payments_df.columns
        assert 'payment_method' in bad_payments_df.columns
        assert 'payment_date' in bad_payments_df.columns
        assert 'status' in bad_payments_df.columns
        assert 'transaction_id' in bad_payments_df.columns
        assert 'card_last_four' in bad_payments_df.columns
        
        # Check that some data quality issues are present
        has_null_values = bad_payments_df.isnull().any().any()
        has_negative_amounts = (bad_payments_df['amount'] < 0).any()
        has_invalid_methods = ~bad_payments_df['payment_method'].isin(['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash']).any()
        has_invalid_status = ~bad_payments_df['status'].isin(['completed', 'pending', 'failed']).any()
        
        # At least one of these issues should be present
        assert has_null_values or has_negative_amounts or has_invalid_methods or has_invalid_status
    
    def test_generate_bad_payments_with_invalid_input(self):
        """Test bad payments generation with invalid input."""
        with pytest.raises(ValueError, match="Sales DataFrame must be provided"):
            generate_bad_payments(None)
    
    @patch('pandas.DataFrame.to_csv')
    @patch('os.makedirs')
    @patch('generate_bad_records.generate_bad_payments')
    @patch('generate_bad_records.generate_bad_sales')
    @patch('generate_bad_records.generate_bad_products')
    @patch('generate_bad_records.generate_bad_users')
    def test_main_function(self, mock_generate_users, mock_generate_products, 
                          mock_generate_sales, mock_generate_payments, 
                          mock_makedirs, mock_to_csv, 
                          sample_bad_users_data, sample_bad_products_data):
        """Test main function execution."""
        # Mock return values
        mock_generate_users.return_value = sample_bad_users_data
        mock_generate_products.return_value = sample_bad_products_data
        mock_generate_sales.return_value = pd.DataFrame({'sale_id': ['SALE000001']})
        mock_generate_payments.return_value = pd.DataFrame({'payment_id': ['PAY000001']})
        
        # Run main function
        main()
        
        # Verify functions were called
        mock_makedirs.assert_called()
        mock_generate_users.assert_called_once_with(200)
        mock_generate_products.assert_called_once_with(100)
        mock_generate_sales.assert_called_once()
        mock_generate_payments.assert_called_once()
        
        # Verify CSV files were saved
        assert mock_to_csv.call_count == 4  # bad_users, bad_products, bad_sales, bad_payments
    
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
    
    def test_bad_data_quality_issues(self):
        """Test that bad data contains various quality issues."""
        bad_users_df = generate_bad_users(100)
        
        # Check for different types of issues
        issues_found = []
        
        # Check for missing values
        if bad_users_df.isnull().any().any():
            issues_found.append("missing_values")
        
        # Check for empty strings
        if (bad_users_df == '').any().any():
            issues_found.append("empty_strings")
        
        # Check for negative ages
        if (bad_users_df['age'] < 0).any():
            issues_found.append("negative_ages")
        
        # Check for invalid email formats
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = ~bad_users_df['email'].astype(str).str.match(email_pattern, na=False)
        if invalid_emails.any():
            issues_found.append("invalid_emails")
        
        # Check for XSS attempts
        if bad_users_df['first_name'].astype(str).str.contains('<script>', na=False).any():
            issues_found.append("xss_attempts")
        
        # Should have found at least some issues
        assert len(issues_found) > 0, f"No data quality issues found in bad users data. Issues checked: {issues_found}"
    
    def test_bad_products_quality_issues(self):
        """Test that bad products data contains various quality issues."""
        bad_products_df = generate_bad_products(100)
        
        # Check for different types of issues
        issues_found = []
        
        # Check for missing values
        if bad_products_df.isnull().any().any():
            issues_found.append("missing_values")
        
        # Check for empty strings
        if (bad_products_df == '').any().any():
            issues_found.append("empty_strings")
        
        # Check for negative prices
        if (bad_products_df['price'] < 0).any():
            issues_found.append("negative_prices")
        
        # Check for negative stock
        if (bad_products_df['stock_quantity'] < 0).any():
            issues_found.append("negative_stock")
        
        # Check for XSS attempts
        if bad_products_df['name'].astype(str).str.contains('<script>', na=False).any():
            issues_found.append("xss_attempts")
        
        # Should have found at least some issues
        assert len(issues_found) > 0, f"No data quality issues found in bad products data. Issues checked: {issues_found}"
    
    def test_data_consistency_in_bad_data(self):
        """Test that bad data maintains some consistency for testing purposes."""
        bad_users_df = generate_bad_users(50)
        bad_products_df = generate_bad_products(25)
        bad_sellers_df = pd.DataFrame({
            'seller_id': ['S0001', 'S0002', 'S0003'],
            'company_name': ['Company A', 'Company B', 'Company C']
        })
        bad_sales_df = generate_bad_sales(100, bad_users_df, bad_products_df, bad_sellers_df)
        
        # Check that user_ids in sales exist in users (some may be None due to bad data)
        sales_user_ids = set(bad_sales_df['user_id'].dropna().unique())
        users_user_ids = set(bad_users_df['user_id'].unique())
        if sales_user_ids:  # Only check if there are valid user_ids
            assert sales_user_ids.issubset(users_user_ids)
        
        # Check that product_ids in sales exist in products (some may be None due to bad data)
        sales_product_ids = set(bad_sales_df['product_id'].dropna().unique())
        products_product_ids = set(bad_products_df['product_id'].unique())
        if sales_product_ids:  # Only check if there are valid product_ids
            assert sales_product_ids.issubset(products_product_ids)
    
    def test_bad_data_vs_good_data_comparison(self, sample_users_data):
        """Test that bad data has more issues than good data."""
        good_users = sample_users_data
        bad_users = generate_bad_users(10)
        
        # Count issues in good data
        good_issues = 0
        if good_users.isnull().any().any():
            good_issues += 1
        if (good_users == '').any().any():
            good_issues += 1
        if (good_users['age'] < 0).any():
            good_issues += 1
        
        # Count issues in bad data
        bad_issues = 0
        if bad_users.isnull().any().any():
            bad_issues += 1
        if (bad_users == '').any().any():
            bad_issues += 1
        if (bad_users['age'] < 0).any():
            bad_issues += 1
        
        # Bad data should have more issues
        assert bad_issues >= good_issues, f"Bad data ({bad_issues} issues) should have at least as many issues as good data ({good_issues} issues)"
    
    @patch('generate_bad_records.fake')
    def test_faker_integration(self, mock_fake):
        """Test that Faker is properly integrated."""
        # Mock Faker methods
        mock_fake.first_name.return_value = "Test"
        mock_fake.last_name.return_value = "User"
        mock_fake.email.return_value = "test@example.com"
        mock_fake.phone_number.return_value = "123-456-7890"
        mock_fake.street_address.return_value = "123 Test St"
        mock_fake.city.return_value = "Test City"
        mock_fake.state.return_value = "TS"
        mock_fake.zipcode.return_value = "12345"
        mock_fake.country.return_value = "Test Country"
        mock_fake.date_between.return_value = "2024-01-01"
        
        bad_users_df = generate_bad_users(5)
        
        # Verify Faker was called
        assert mock_fake.first_name.called
        assert mock_fake.last_name.called
        assert mock_fake.email.called
