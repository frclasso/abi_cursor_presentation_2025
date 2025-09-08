"""
Unit tests for ecommerce_analyzer.py using pytest fixtures.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import os
import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ecommerce_analyzer import EcommerceAnalyzer
from tests.fixtures.test_data import (
    sample_users_data, sample_products_data, sample_sales_data, 
    sample_payments_data, sample_bad_users_data, sample_bad_products_data,
    sample_metrics_data, mock_validation_results, temp_directories
)

class TestEcommerceAnalyzer:
    """Test cases for EcommerceAnalyzer class."""
    
    def test_init(self, temp_directories):
                """
        Test Init.
        
        Performs the test init operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        assert analyzer.metrics_path == str(temp_directories['metrics_dir'])
        assert analyzer.data_path == str(temp_directories['data_dir'])
        assert analyzer.output_path == str(temp_directories['images_dir'])
        assert analyzer.data == {}
        assert analyzer.raw_data == {}
        assert analyzer.validation_results == {}
    
    @patch('pandas.read_csv')
    def test_load_metrics_data_success(self, mock_read_csv, temp_directories, sample_metrics_data):
                """
        Load data from configured source.
        
        Loads data from the configured data source with proper error
        handling and validation. Supports various data formats and
        provides detailed loading status information.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        # Mock the CSV files
        mock_dataframes = {
            'address_city_distribution.csv': sample_metrics_data['city_dist'],
            'address_state_distribution.csv': pd.DataFrame({'state': ['NY', 'CA'], 'user_count': [50, 40]}),
            'address_country_distribution.csv': pd.DataFrame({'country': ['USA'], 'user_count': [90]}),
            'sales_sales_by_status.csv': sample_metrics_data['sales_status'],
            'sales_monthly_sales.csv': pd.DataFrame({'month': ['2024-01'], 'total_amount': [1000]}),
            'products_top_products_quantity.csv': pd.DataFrame({'product_name': ['Product A'], 'total_quantity_sold': [10]}),
            'products_top_products_revenue.csv': pd.DataFrame({'product_name': ['Product A'], 'total_revenue': [1000]}),
            'buyers_top_buyers_amount.csv': pd.DataFrame({'first_name': ['John'], 'total_spent': [500]}),
            'buyers_top_buyers_frequency.csv': pd.DataFrame({'first_name': ['John'], 'total_purchases': [5]}),
            'payments_payment_distribution.csv': sample_metrics_data['payment_dist'],
            'payments_payment_amounts.csv': pd.DataFrame({'payment_method': ['credit_card'], 'total_amount': [1000]}),
            'gender_gender_distribution.csv': sample_metrics_data['gender_dist'],
            'gender_gender_purchases.csv': pd.DataFrame({'gender': ['M'], 'total_spent': [500]})
        }
        
        def mock_read_csv_side_effect(filepath):
            filename = os.path.basename(filepath)
            return mock_dataframes.get(filename, pd.DataFrame())
        
        mock_read_csv.side_effect = mock_read_csv_side_effect
        
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        result = analyzer.load_metrics_data()
        
        assert result is True
        assert 'city_dist' in analyzer.data
        assert 'sales_status' in analyzer.data
        assert 'gender_dist' in analyzer.data
        assert len(analyzer.data) == 13
    
    @patch('pandas.read_csv')
    def test_load_metrics_data_failure(self, mock_read_csv, temp_directories):
                """
        Load data from configured source.
        
        Loads data from the configured data source with proper error
        handling and validation. Supports various data formats and
        provides detailed loading status information.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        result = analyzer.load_metrics_data()
        
        assert result is False
    
    @patch('pandas.read_csv')
    def test_load_raw_data_success(self, mock_read_csv, temp_directories, sample_users_data, sample_products_data, sample_sales_data, sample_payments_data, sample_bad_users_data, sample_bad_products_data):
                """
        Load data from configured source.
        
        Loads data from the configured data source with proper error
        handling and validation. Supports various data formats and
        provides detailed loading status information.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        mock_dataframes = {
            'users.csv': sample_users_data,
            'products.csv': sample_products_data,
            'sales.csv': sample_sales_data,
            'payments.csv': sample_payments_data,
            'sellers.csv': pd.DataFrame({'seller_id': ['S0001'], 'company_name': ['Company A']}),
            'bad_users.csv': sample_bad_users_data,
            'bad_products.csv': sample_bad_products_data,
            'bad_sales.csv': pd.DataFrame({'sale_id': ['SALE000001'], 'user_id': ['U000001']}),
            'bad_payments.csv': pd.DataFrame({'payment_id': ['PAY000001'], 'sale_id': ['SALE000001']})
        }
        
        def mock_read_csv_side_effect(filepath):
            filename = os.path.basename(filepath)
            return mock_dataframes.get(filename, pd.DataFrame())
        
        mock_read_csv.side_effect = mock_read_csv_side_effect
        
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        result = analyzer.load_raw_data()
        
        assert result is True
        assert 'valid' in analyzer.raw_data
        assert 'bad' in analyzer.raw_data
        assert 'users' in analyzer.raw_data['valid']
        assert 'users' in analyzer.raw_data['bad']
    
    def test_validate_data_quality(self, temp_directories, sample_users_data, sample_products_data, sample_bad_users_data, sample_bad_products_data):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up raw data
        analyzer.raw_data = {
            'valid': {
                'users': sample_users_data,
                'products': sample_products_data
            },
            'bad': {
                'users': sample_bad_users_data,
                'products': sample_bad_products_data
            }
        }
        
        result = analyzer.validate_data_quality()
        
        assert 'valid' in result
        assert 'bad' in result
        assert 'users' in result['valid']
        assert 'products' in result['valid']
        
        # Check that bad data has more issues
        valid_issues = sum([table['issue_count'] for table in result['valid'].values()])
        bad_issues = sum([table['issue_count'] for table in result['bad'].values()])
        
        assert bad_issues > valid_issues
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_sales_overview_chart(self, mock_close, mock_savefig, temp_directories, sample_metrics_data):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up data
        analyzer.data = {
            'sales_status': sample_metrics_data['sales_status'],
            'monthly_sales': pd.DataFrame({'total_amount': [1000, 1200, 1100]}),
            'top_products_qty': pd.DataFrame({'product_name': ['Product A'], 'total_quantity_sold': [10]}),
            'gender_dist': sample_metrics_data['gender_dist']
        }
        
        analyzer.create_sales_overview_chart()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_data_quality_dashboard(self, mock_close, mock_savefig, temp_directories, mock_validation_results):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up validation results
        analyzer.validation_results = mock_validation_results
        
        analyzer.create_data_quality_dashboard()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_validation_comparison_chart(self, mock_close, mock_savefig, temp_directories, mock_validation_results):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up validation results
        analyzer.validation_results = mock_validation_results
        
        analyzer.create_validation_comparison_chart()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_geographic_analysis(self, mock_close, mock_savefig, temp_directories):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up data
        analyzer.data = {
            'state_dist': pd.DataFrame({'state': ['NY', 'CA'], 'user_count': [50, 40]}),
            'country_dist': pd.DataFrame({'country': ['USA'], 'user_count': [90]})
        }
        
        analyzer.create_geographic_analysis()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_payment_analysis(self, mock_close, mock_savefig, temp_directories, sample_metrics_data):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up data
        analyzer.data = {
            'payment_dist': sample_metrics_data['payment_dist'],
            'payment_amounts': pd.DataFrame({'payment_method': ['credit_card'], 'total_amount': [1000]})
        }
        
        analyzer.create_payment_analysis()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_customer_analysis(self, mock_close, mock_savefig, temp_directories):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up data
        analyzer.data = {
            'top_buyers_amount': pd.DataFrame({'first_name': ['John'], 'last_name': ['Doe'], 'total_spent': [500]}),
            'gender_purchases': pd.DataFrame({'gender': ['M'], 'total_spent': [500], 'average_purchase': [100], 'transactions_per_buyer': [5]})
        }
        
        analyzer.create_customer_analysis()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_product_analysis(self, mock_close, mock_savefig, temp_directories):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up data
        analyzer.data = {
            'top_products_rev': pd.DataFrame({'product_name': ['Product A'], 'total_revenue': [1000]}),
            'top_products_qty': pd.DataFrame({'category': ['Electronics', 'Clothing']})
        }
        
        analyzer.create_product_analysis()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_comprehensive_dashboard(self, mock_close, mock_savefig, temp_directories, sample_metrics_data):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up data
        analyzer.data = {
            'sales_status': sample_metrics_data['sales_status'],
            'monthly_sales': pd.DataFrame({'total_amount': [1000, 1200, 1100]}),
            'top_products_qty': pd.DataFrame({'product_name': ['Product A'], 'total_quantity_sold': [10]}),
            'gender_dist': sample_metrics_data['gender_dist'],
            'payment_dist': sample_metrics_data['payment_dist'],
            'top_buyers_amount': pd.DataFrame({'first_name': ['John'], 'last_name': ['Doe'], 'total_spent': [500]}),
            'gender_purchases': pd.DataFrame({'gender': ['M'], 'total_spent': [500], 'average_purchase': [100], 'transactions_per_buyer': [5]}),
            'state_dist': pd.DataFrame({'state': ['NY', 'CA', 'TX'], 'user_count': [50, 40, 30]})
        }
        
        analyzer.create_comprehensive_dashboard()
        
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('os.listdir')
    @patch.object(EcommerceAnalyzer, 'create_validation_comparison_chart')
    @patch.object(EcommerceAnalyzer, 'create_data_quality_dashboard')
    @patch.object(EcommerceAnalyzer, 'create_comprehensive_dashboard')
    @patch.object(EcommerceAnalyzer, 'create_product_analysis')
    @patch.object(EcommerceAnalyzer, 'create_customer_analysis')
    @patch.object(EcommerceAnalyzer, 'create_payment_analysis')
    @patch.object(EcommerceAnalyzer, 'create_geographic_analysis')
    @patch.object(EcommerceAnalyzer, 'create_sales_overview_chart')
    @patch.object(EcommerceAnalyzer, 'validate_data_quality')
    @patch.object(EcommerceAnalyzer, 'load_raw_data')
    @patch.object(EcommerceAnalyzer, 'load_metrics_data')
    def test_generate_all_visualizations_success(self, mock_load_metrics, mock_load_raw, 
                                                mock_validate, mock_sales, mock_geo, 
                                                mock_payment, mock_customer, mock_product,
                                                mock_comprehensive, mock_quality, mock_comparison,
                                                mock_listdir, temp_directories, mock_validation_results):
                """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
        # Mock return values
        mock_load_metrics.return_value = True
        mock_load_raw.return_value = True
        mock_validate.return_value = mock_validation_results
        mock_listdir.return_value = ['image1.png', 'image2.png']
        
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        # Set up the analyzer with mock data to avoid KeyError
        analyzer.data = {
            'sales_status': pd.DataFrame({'status': ['completed'], 'count': [100]}),
            'monthly_sales': pd.DataFrame({'total_amount': [1000]}),
            'top_products_qty': pd.DataFrame({'product_name': ['Product A'], 'total_quantity_sold': [10]}),
            'gender_dist': pd.DataFrame({'gender': ['M'], 'user_count': [50]}),
            'payment_dist': pd.DataFrame({'payment_method': ['credit_card'], 'transaction_count': [50]}),
            'top_buyers_amount': pd.DataFrame({'first_name': ['John'], 'last_name': ['Doe'], 'total_spent': [500]}),
            'gender_purchases': pd.DataFrame({'gender': ['M'], 'total_spent': [500], 'average_purchase': [100], 'transactions_per_buyer': [5]}),
            'state_dist': pd.DataFrame({'state': ['NY'], 'user_count': [30]})
        }
        analyzer.validation_results = mock_validation_results
        
        result = analyzer.generate_all_visualizations()
        
        assert result is True
        mock_load_metrics.assert_called_once()
        mock_load_raw.assert_called_once()
        mock_validate.assert_called_once()
        mock_sales.assert_called_once()
        mock_geo.assert_called_once()
        mock_payment.assert_called_once()
        mock_customer.assert_called_once()
        mock_product.assert_called_once()
        mock_comprehensive.assert_called_once()
        mock_quality.assert_called_once()
        mock_comparison.assert_called_once()
    
    def test_print_validation_summary(self, temp_directories, capsys, mock_validation_results):
                """
        Test Print Validation Summary.
        
        Performs the test print validation summary operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        analyzer = EcommerceAnalyzer(
            metrics_path=str(temp_directories['metrics_dir']),
            data_path=str(temp_directories['data_dir']),
            output_path=str(temp_directories['images_dir'])
        )
        
        analyzer.validation_results = mock_validation_results
        analyzer.print_validation_summary()
        
        captured = capsys.readouterr()
        assert "DATA VALIDATION SUMMARY" in captured.out
        assert "VALID DATA:" in captured.out
        assert "BAD DATA:" in captured.out
        assert "QUALITY SCORE:" in captured.out
