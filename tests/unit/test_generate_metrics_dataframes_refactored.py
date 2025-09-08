"""
Unit tests for the refactored generate_metrics_dataframes.py using pytest fixtures.
This demonstrates how to test the refactored code with proper dependency injection.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from generate_metrics_dataframes_refactored import MetricsDataFrameGenerator

class TestMetricsDataFrameGenerator:
    """Test cases for the refactored MetricsDataFrameGenerator class."""
    
    def test_init_default(self):
        """Test initialization with default parameters."""
        generator = MetricsDataFrameGenerator()
        assert generator.data_loader is not None
        assert generator.output_dir == 'tests/metrics/'
        assert generator.data == {}
    
    def test_init_custom(self, mock_data_loader, tmp_path):
        """Test initialization with custom parameters."""
        generator = MetricsDataFrameGenerator(
            data_loader=mock_data_loader,
            output_dir=str(tmp_path / "custom_metrics")
        )
        assert generator.data_loader == mock_data_loader
        assert generator.output_dir == str(tmp_path / "custom_metrics")
    
    def test_load_data_with_mock(self, mock_data_loader):
        """Test data loading with mock data loader."""
        generator = MetricsDataFrameGenerator(data_loader=mock_data_loader)
        users_df, products_df, sales_df, payments_df, sellers_df = generator.load_data()
        
        assert users_df is not None
        assert products_df is not None
        assert sales_df is not None
        assert payments_df is not None
        assert sellers_df is not None
        
        # Verify data structure
        assert 'user_id' in users_df.columns
        assert 'product_id' in products_df.columns
        assert 'sale_id' in sales_df.columns
        assert 'payment_id' in payments_df.columns
    
    def test_users_distribution_by_address(self, metrics_generator, sample_data):
        """Test users distribution by address generation."""
        users_df = sample_data['users_df']
        result = metrics_generator.users_distribution_by_address(users_df)
        
        assert 'city_distribution' in result
        assert 'state_distribution' in result
        assert 'country_distribution' in result
        
        # Check city distribution
        city_df = result['city_distribution']
        assert 'city' in city_df.columns
        assert 'user_count' in city_df.columns
        assert 'percentage' in city_df.columns
        assert len(city_df) <= 10  # Should be top 10
        
        # Check state distribution
        state_df = result['state_distribution']
        assert 'state' in state_df.columns
        assert 'user_count' in state_df.columns
        assert 'percentage' in state_df.columns
        
        # Check country distribution
        country_df = result['country_distribution']
        assert 'country' in country_df.columns
        assert 'user_count' in country_df.columns
        assert 'percentage' in country_df.columns
    
    def test_total_sales_metrics(self, metrics_generator, sample_data):
        """Test total sales metrics calculation."""
        sales_df = sample_data['sales_df']
        payments_df = sample_data['payments_df']
        result = metrics_generator.total_sales_metrics(sales_df, payments_df)
        
        assert 'total_sales_amount' in result
        assert 'total_sales_count' in result
        assert 'average_sale_amount' in result
        assert 'total_payments_amount' in result
        assert 'total_payments_count' in result
        assert 'sales_by_status' in result
        assert 'monthly_sales' in result
        
        # Check data types
        assert isinstance(result['total_sales_amount'], (int, float))
        assert isinstance(result['total_sales_count'], int)
        assert isinstance(result['average_sale_amount'], (int, float))
        
        # Check sales by status DataFrame
        status_df = result['sales_by_status']
        assert 'status' in status_df.columns
        assert 'count' in status_df.columns
        assert 'percentage' in status_df.columns
    
    def test_top_10_products(self, metrics_generator, sample_data):
        """Test top 10 products analysis."""
        sales_df = sample_data['sales_df']
        products_df = sample_data['products_df']
        result = metrics_generator.top_10_products(sales_df, products_df)
        
        assert 'top_products_quantity' in result
        assert 'top_products_revenue' in result
        
        # Check quantity-based products
        qty_df = result['top_products_quantity']
        assert 'product_name' in qty_df.columns
        assert 'total_quantity_sold' in qty_df.columns
        assert 'total_revenue' in qty_df.columns
        assert 'total_transactions' in qty_df.columns
        
        # Check revenue-based products
        rev_df = result['top_products_revenue']
        assert 'product_name' in rev_df.columns
        assert 'total_revenue' in rev_df.columns
        assert 'total_quantity_sold' in rev_df.columns
    
    def test_top_10_buyers(self, metrics_generator, sample_data):
        """Test top 10 buyers analysis."""
        sales_df = sample_data['sales_df']
        users_df = sample_data['users_df']
        result = metrics_generator.top_10_buyers(sales_df, users_df)
        
        assert 'top_buyers_amount' in result
        assert 'top_buyers_frequency' in result
        
        # Check amount-based buyers
        amount_df = result['top_buyers_amount']
        assert 'first_name' in amount_df.columns
        assert 'last_name' in amount_df.columns
        assert 'total_spent' in amount_df.columns
        assert 'total_purchases' in amount_df.columns
        
        # Check frequency-based buyers
        freq_df = result['top_buyers_frequency']
        assert 'first_name' in freq_df.columns
        assert 'total_purchases' in freq_df.columns
        assert 'total_spent' in freq_df.columns
    
    def test_payment_method_analysis(self, metrics_generator, sample_data):
        """Test payment method analysis."""
        payments_df = sample_data['payments_df']
        result = metrics_generator.payment_method_analysis(payments_df)
        
        assert 'payment_distribution' in result
        assert 'payment_amounts' in result
        assert 'payment_success_rates' in result
        assert 'most_used_method' in result
        
        # Check payment distribution
        dist_df = result['payment_distribution']
        assert 'payment_method' in dist_df.columns
        assert 'transaction_count' in dist_df.columns
        assert 'percentage' in dist_df.columns
        
        # Check payment amounts
        amounts_df = result['payment_amounts']
        assert 'payment_method' in amounts_df.columns
        assert 'total_amount' in amounts_df.columns
        assert 'average_amount' in amounts_df.columns
    
    def test_gender_purchase_analysis(self, metrics_generator, sample_data):
        """Test gender purchase analysis."""
        sales_df = sample_data['sales_df']
        users_df = sample_data['users_df']
        result = metrics_generator.gender_purchase_analysis(sales_df, users_df)
        
        assert 'gender_distribution' in result
        assert 'gender_purchases' in result
        
        # Check gender distribution
        dist_df = result['gender_distribution']
        assert 'gender' in dist_df.columns
        assert 'user_count' in dist_df.columns
        assert 'percentage' in dist_df.columns
        
        # Check gender purchases
        purchases_df = result['gender_purchases']
        assert 'gender' in purchases_df.columns
        assert 'total_spent' in purchases_df.columns
        assert 'average_purchase' in purchases_df.columns
        assert 'transactions_per_buyer' in purchases_df.columns
    
    @patch('os.makedirs')
    def test_save_metrics_to_csv(self, mock_makedirs, metrics_generator, tmp_path):
        """Test saving metrics to CSV files."""
        # Create sample metrics data
        metrics_data = {
            'address': {
                'city_distribution': pd.DataFrame({'city': ['NYC'], 'user_count': [100]}),
                'state_distribution': pd.DataFrame({'state': ['NY'], 'user_count': [100]})
            },
            'sales': pd.DataFrame({'status': ['completed'], 'count': [50]})
        }
        
        # Mock the CSV writing
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            metrics_generator.save_metrics_to_csv(metrics_data)
            
            # Verify directory creation
            mock_makedirs.assert_called_once_with(metrics_generator.output_dir, exist_ok=True)
            
            # Verify CSV files were saved
            assert mock_to_csv.call_count >= 3  # At least 3 CSV files should be created
    
    def test_generate_all_metrics(self, metrics_generator):
        """Test generating all metrics."""
        result = metrics_generator.generate_all_metrics()
        
        # Check that all expected metrics are generated
        assert 'address' in result
        assert 'sales' in result
        assert 'products' in result
        assert 'buyers' in result
        assert 'payments' in result
        assert 'gender' in result
        
        # Check address metrics
        assert 'city_distribution' in result['address']
        assert 'state_distribution' in result['address']
        assert 'country_distribution' in result['address']
        
        # Check sales metrics
        assert 'total_sales_amount' in result['sales']
        assert 'sales_by_status' in result['sales']
        assert 'monthly_sales' in result['sales']
    
    def test_data_consistency(self, metrics_generator, sample_data):
        """Test data consistency across different analyses."""
        users_df = sample_data['users_df']
        products_df = sample_data['products_df']
        sales_df = sample_data['sales_df']
        payments_df = sample_data['payments_df']
        
        # Generate all metrics
        address_metrics = metrics_generator.users_distribution_by_address(users_df)
        sales_metrics = metrics_generator.total_sales_metrics(sales_df, payments_df)
        product_metrics = metrics_generator.top_10_products(sales_df, products_df)
        buyer_metrics = metrics_generator.top_10_buyers(sales_df, users_df)
        
        # Check that user counts are consistent
        total_users = len(users_df)
        city_total = address_metrics['city_distribution']['user_count'].sum()
        state_total = address_metrics['state_distribution']['user_count'].sum()
        country_total = address_metrics['country_distribution']['user_count'].sum()
        
        assert city_total == total_users
        assert state_total == total_users
        assert country_total == total_users
        
        # Check that sales counts are consistent
        total_sales = len(sales_df)
        assert sales_metrics['total_sales_count'] == total_sales
    
    def test_error_handling_with_none_data(self):
        """Test error handling when data loader returns None."""
        def failing_loader():
            return None, None, None, None, None
        
        generator = MetricsDataFrameGenerator(data_loader=failing_loader)
        result = generator.generate_all_metrics()
        
        # Should return empty dict when data loading fails
        assert result == {}
    
    def test_custom_output_directory(self, mock_data_loader, tmp_path):
        """Test using custom output directory."""
        custom_dir = str(tmp_path / "custom_output")
        generator = MetricsDataFrameGenerator(
            data_loader=mock_data_loader,
            output_dir=custom_dir
        )
        
        metrics_data = {
            'test_metric': pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        }
        
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            generator.save_metrics_to_csv(metrics_data)
            
            # Check that the file was saved to the custom directory
            call_args = mock_to_csv.call_args[0][0]
            assert custom_dir in call_args


class TestBackwardCompatibility:
    """Test backward compatibility with original function interface."""
    
    def test_load_data_function(self, mock_data_loader):
        """Test the original load_data function still works."""
        from generate_metrics_dataframes_refactored import load_data
        
        # This will use the default data loader (file-based)
        # We can't easily test this without mocking file operations
        pass
    
    def test_individual_functions(self, sample_data):
        """Test that individual functions still work with the original interface."""
        from generate_metrics_dataframes_refactored import (
            users_distribution_by_address,
            total_sales_metrics,
            top_10_products,
            top_10_buyers,
            payment_method_analysis,
            gender_purchase_analysis
        )
        
        users_df = sample_data['users_df']
        products_df = sample_data['products_df']
        sales_df = sample_data['sales_df']
        payments_df = sample_data['payments_df']
        
        # Test each function
        address_result = users_distribution_by_address(users_df)
        assert 'city_distribution' in address_result
        
        sales_result = total_sales_metrics(sales_df, payments_df)
        assert 'total_sales_amount' in sales_result
        
        products_result = top_10_products(sales_df, products_df)
        assert 'top_products_quantity' in products_result
        
        buyers_result = top_10_buyers(sales_df, users_df)
        assert 'top_buyers_amount' in buyers_result
        
        payments_result = payment_method_analysis(payments_df)
        assert 'payment_distribution' in payments_result
        
        gender_result = gender_purchase_analysis(sales_df, users_df)
        assert 'gender_distribution' in gender_result


# Integration tests
class TestIntegration:
    """Integration tests for the refactored system."""
    
    def test_full_workflow(self, metrics_generator):
        """Test the complete workflow from data loading to CSV output."""
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            result = metrics_generator.generate_all_metrics()
            
            # Verify all metrics were generated
            assert len(result) == 6  # address, sales, products, buyers, payments, gender
            
            # Verify CSV files were created
            assert mock_to_csv.call_count > 0
            
            # Verify the structure of the result
            for metric_type, metric_data in result.items():
                assert isinstance(metric_data, dict)
                for sub_metric, df in metric_data.items():
                    assert isinstance(df, pd.DataFrame)
    
    def test_performance_with_large_dataset(self, tmp_path):
        """Test performance with a larger dataset."""
        # Create a larger dataset
        large_users = pd.DataFrame({
            'user_id': [f'U{i:06d}' for i in range(1000)],
            'first_name': [f'User{i}' for i in range(1000)],
            'last_name': [f'Last{i}' for i in range(1000)],
            'email': [f'user{i}@example.com' for i in range(1000)],
            'city': [f'City{i%10}' for i in range(1000)],
            'state': [f'ST{i%5}' for i in range(1000)],
            'country': ['USA'] * 1000,
            'gender': ['M' if i % 2 == 0 else 'F' for i in range(1000)]
        })
        
        large_products = pd.DataFrame({
            'product_id': [f'P{i:06d}' for i in range(100)],
            'name': [f'Product{i}' for i in range(100)],
            'category': [f'Category{i%10}' for i in range(100)],
            'price': [10.0 + i for i in range(100)]
        })
        
        large_sales = pd.DataFrame({
            'sale_id': [f'SALE{i:08d}' for i in range(5000)],
            'user_id': [f'U{np.random.randint(0, 1000):06d}' for _ in range(5000)],
            'product_id': [f'P{np.random.randint(0, 100):06d}' for _ in range(5000)],
            'quantity': np.random.randint(1, 10, 5000),
            'final_amount': np.random.uniform(10, 1000, 5000),
            'sale_date': pd.date_range('2024-01-01', periods=5000, freq='H'),
            'status': np.random.choice(['completed', 'pending', 'cancelled'], 5000)
        })
        
        large_payments = pd.DataFrame({
            'payment_id': [f'PAY{i:08d}' for i in range(4500)],
            'sale_id': [f'SALE{i:08d}' for i in range(4500)],
            'amount': np.random.uniform(10, 1000, 4500),
            'payment_method': np.random.choice(['credit_card', 'paypal', 'debit_card'], 4500),
            'status': np.random.choice(['completed', 'pending', 'failed'], 4500)
        })
        
        def large_data_loader():
            return large_users, large_products, large_sales, large_payments, pd.DataFrame({'seller_id': ['S0001']})
        
        generator = MetricsDataFrameGenerator(
            data_loader=large_data_loader,
            output_dir=str(tmp_path / "large_metrics")
        )
        
        # This should complete without errors
        result = generator.generate_all_metrics()
        assert len(result) == 6
