"""
Pytest configuration and shared fixtures for the e-commerce testing suite.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {
        'users_df': pd.DataFrame({
            'user_id': ['U000001', 'U000002', 'U000003'],
            'first_name': ['John', 'Jane', 'Bob'],
            'last_name': ['Doe', 'Smith', 'Johnson'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
            'phone': ['123-456-7890', '098-765-4321', '555-123-4567'],
            'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'city': ['New York', 'Los Angeles', 'Chicago'],
            'state': ['NY', 'CA', 'IL'],
            'zip_code': ['10001', '90210', '60601'],
            'country': ['USA', 'USA', 'USA'],
            'date_joined': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'is_active': [True, True, False],
            'age': [25, 30, 35],
            'gender': ['M', 'F', 'M']
        }),
        'products_df': pd.DataFrame({
            'product_id': ['P000001', 'P000002', 'P000003'],
            'name': ['Product A', 'Product B', 'Product C'],
            'description': ['Description A', 'Description B', 'Description C'],
            'category': ['Electronics', 'Clothing', 'Books'],
            'price': [100.00, 50.00, 25.00],
            'cost': [60.00, 30.00, 15.00],
            'stock_quantity': [100, 200, 150],
            'sku': ['SKU-001', 'SKU-002', 'SKU-003'],
            'brand': ['Brand A', 'Brand B', 'Brand C'],
            'weight': [1.5, 0.8, 0.3],
            'dimensions': ['10x10x5', '8x6x2', '6x4x1'],
            'is_active': [True, True, False],
            'created_at': ['2024-01-01', '2024-01-02', '2024-01-03']
        }),
        'sales_df': pd.DataFrame({
            'sale_id': ['SALE000001', 'SALE000002', 'SALE000003'],
            'user_id': ['U000001', 'U000002', 'U000003'],
            'product_id': ['P000001', 'P000002', 'P000003'],
            'seller_id': ['S0001', 'S0002', 'S0003'],
            'quantity': [2, 1, 3],
            'unit_price': [100.00, 50.00, 25.00],
            'total_amount': [200.00, 50.00, 75.00],
            'discount': [0.1, 0.0, 0.05],
            'final_amount': [180.00, 50.00, 71.25],
            'sale_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
            'status': ['completed', 'pending', 'completed'],
            'shipping_address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'shipping_city': ['New York', 'Los Angeles', 'Chicago'],
            'shipping_state': ['NY', 'CA', 'IL'],
            'shipping_zip': ['10001', '90210', '60601']
        }),
        'payments_df': pd.DataFrame({
            'payment_id': ['PAY000001_1', 'PAY000002_1', 'PAY000003_1'],
            'sale_id': ['SALE000001', 'SALE000002', 'SALE000003'],
            'amount': [180.00, 50.00, 71.25],
            'payment_method': ['credit_card', 'paypal', 'debit_card'],
            'payment_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
            'status': ['completed', 'pending', 'completed'],
            'transaction_id': ['TXN-001', 'TXN-002', 'TXN-003'],
            'card_last_four': ['1234', '5678', '9012']
        }),
        'sellers_df': pd.DataFrame({
            'seller_id': ['S0001', 'S0002', 'S0003'],
            'company_name': ['Company A', 'Company B', 'Company C'],
            'contact_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'email': ['company1@example.com', 'company2@example.com', 'company3@example.com'],
            'phone': ['123-456-7890', '098-765-4321', '555-123-4567'],
            'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'city': ['New York', 'Los Angeles', 'Chicago'],
            'state': ['NY', 'CA', 'IL'],
            'zip_code': ['10001', '90210', '60601'],
            'country': ['USA', 'USA', 'USA'],
            'tax_id': ['12-3456789', '23-4567890', '34-5678901'],
            'rating': [4.5, 4.2, 4.8],
            'total_sales': [100000, 150000, 200000],
            'is_verified': [True, True, False],
            'joined_date': ['2024-01-01', '2024-01-02', '2024-01-03']
        })
    }

@pytest.fixture
def sample_bad_users_data():
    """Sample bad users data for testing validation."""
    return pd.DataFrame({
        'user_id': ['U000001', 'U000002', 'U000003'],
        'first_name': ['John', '', 'Bob<script>alert("xss")</script>'],
        'last_name': ['Doe', 'Smith', ''],
        'email': ['invalid-email', 'jane@example.com', 'notanemail'],
        'phone': ['123', 'invalid-phone', '098-765-4321'],
        'address': ['123 Main St', '', '789 Pine Rd'],
        'city': ['New York', 'Los Angeles', ''],
        'state': ['NY', 'CA', 'IL'],
        'zip_code': ['123', '90210', 'invalid-zip'],
        'country': ['USA', 'USA', ''],
        'date_joined': ['2024-01-01', None, '2024-01-03'],
        'is_active': [True, 'yes', False],
        'age': [25, -5, 35],
        'gender': ['M', 'invalid', 'M']
    })

@pytest.fixture
def sample_bad_products_data():
    """Sample bad products data for testing validation."""
    return pd.DataFrame({
        'product_id': ['P000001', 'P000002', 'P000003'],
        'name': ['', 'Product B', 'Product<script>alert("xss")</script>'],
        'description': ['Description A', '', 'Description C'],
        'category': ['InvalidCategory', 'Clothing', ''],
        'price': [-100.00, 'expensive', 25.00],
        'cost': [-60.00, 'unknown', 15.00],
        'stock_quantity': [-50, 'many', 150],
        'sku': ['', 'SKU-002', 'SKU with spaces'],
        'brand': ['Brand A', '', 'Brand<script>alert("xss")</script>'],
        'weight': [-1.5, 'heavy', 0.3],
        'dimensions': ['', '8x6x2', 'large x medium'],
        'is_active': [True, 'N', False],
        'created_at': [None, '2024-01-02', '2024-01-03']
    })

@pytest.fixture
def sample_metrics_data():
    """Sample metrics data for testing."""
    return {
        'city_dist': pd.DataFrame({
            'city': ['New York', 'Los Angeles', 'Chicago'],
            'user_count': [100, 80, 60],
            'percentage': [41.7, 33.3, 25.0]
        }),
        'sales_status': pd.DataFrame({
            'status': ['completed', 'pending', 'cancelled'],
            'count': [85, 10, 5],
            'percentage': [85.0, 10.0, 5.0]
        }),
        'gender_dist': pd.DataFrame({
            'gender': ['M', 'F', 'Other'],
            'user_count': [120, 110, 70],
            'percentage': [40.0, 36.7, 23.3]
        }),
        'payment_dist': pd.DataFrame({
            'payment_method': ['credit_card', 'paypal', 'debit_card'],
            'transaction_count': [100, 80, 70],
            'percentage': [40.0, 32.0, 28.0]
        })
    }

@pytest.fixture
def mock_validation_results():
    """Mock validation results for testing."""
    return {
        'valid': {
            'users': {
                'total_records': 1000,
                'total_columns': 14,
                'issues': ['Missing values: {\'phone\': 5}'],
                'issue_count': 1
            },
            'products': {
                'total_records': 500,
                'total_columns': 13,
                'issues': [],
                'issue_count': 0
            },
            'sales': {
                'total_records': 2000,
                'total_columns': 12,
                'issues': [],
                'issue_count': 0
            },
            'payments': {
                'total_records': 1800,
                'total_columns': 8,
                'issues': [],
                'issue_count': 0
            }
        },
        'bad': {
            'users': {
                'total_records': 200,
                'total_columns': 14,
                'issues': ['Missing values: {\'email\': 20}', 'Invalid email formats: 15', 'XSS attempts in first_name: 3'],
                'issue_count': 3
            },
            'products': {
                'total_records': 100,
                'total_columns': 13,
                'issues': ['Negative values in price: 25', 'Empty strings: {\'name\': 10}'],
                'issue_count': 2
            },
            'sales': {
                'total_records': 500,
                'total_columns': 12,
                'issues': ['Missing values: {\'user_id\': 10}', 'Invalid amounts: 15'],
                'issue_count': 2
            },
            'payments': {
                'total_records': 400,
                'total_columns': 8,
                'issues': ['Invalid payment methods: 5', 'Negative amounts: 8'],
                'issue_count': 2
            }
        }
    }

@pytest.fixture
def temp_directories(tmp_path):
    """Create temporary directories for testing."""
    data_dir = tmp_path / "data_sources"
    metrics_dir = tmp_path / "metrics"
    images_dir = tmp_path / "images"
    
    data_dir.mkdir()
    metrics_dir.mkdir()
    images_dir.mkdir()
    
    return {
        'data_dir': data_dir,
        'metrics_dir': metrics_dir,
        'images_dir': images_dir
    }

# Fixtures for the refactored metrics generator
@pytest.fixture
def mock_data_loader(sample_data):
    """Mock data loader for testing."""
    def loader():
        return (
            sample_data['users_df'],
            sample_data['products_df'],
            sample_data['sales_df'],
            sample_data['payments_df'],
            sample_data['sellers_df']
        )
    return loader

@pytest.fixture
def metrics_generator(mock_data_loader, tmp_path):
    """Create a metrics generator with mock data and temporary output directory."""
    from generate_metrics_dataframes_refactored import MetricsDataFrameGenerator
    return MetricsDataFrameGenerator(
        data_loader=mock_data_loader,
        output_dir=str(tmp_path / "metrics")
    )
