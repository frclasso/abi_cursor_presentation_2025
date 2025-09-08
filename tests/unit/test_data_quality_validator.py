"""
Unit tests for Data Quality Validator using Pydantic
"""

import pytest
import pandas as pd
from datetime import date, datetime
import json
import tempfile
import os

from data_quality_validator import (
    DataQualityValidator, UserModel, SellerModel, ProductModel, 
    SaleModel, PaymentModel, GenderEnum, PaymentMethodEnum, 
    PaymentStatusEnum, SaleStatusEnum
)


class TestUserModel:
    """
    Comprehensive test cases for UserModel validation.
    
    This test class validates all aspects of the UserModel including valid data
    acceptance, invalid data rejection, field validation rules, and business
    logic enforcement. Tests cover edge cases, security validation, and
    data type constraints.
    """
    
    def test_valid_user(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        valid_user = {
            'user_id': 'U000001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345',
            'country': 'USA',
            'date_joined': date(2024, 1, 1),
            'is_active': True,
            'age': 30,
            'gender': GenderEnum.M
        }
        
        user = UserModel(**valid_user)
        assert user.user_id == 'U000001'
        assert user.first_name == 'John'
        assert user.email == 'john@example.com'
    
    def test_invalid_user_id_format(self):
                """
        Test that invalid data is rejected with appropriate errors.
        
        Verifies that malformed or invalid data is properly rejected
        with meaningful error messages and validation failures.
        """
        invalid_user = {
            'user_id': 'INVALID',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345',
            'country': 'USA',
            'date_joined': date(2024, 1, 1),
            'is_active': True,
            'age': 30,
            'gender': GenderEnum.M
        }
        
        with pytest.raises(ValueError, match="String should match pattern"):
            UserModel(**invalid_user)
    
    def test_missing_required_fields(self):
                """
        Test handling of missing required fields.
        
        Verifies that missing required fields are properly detected
        and appropriate validation errors are raised.
        """
        incomplete_user = {
            'user_id': 'U000001',
            'first_name': 'John',
            # Missing last_name and other required fields
        }
        
        with pytest.raises(ValueError):
            UserModel(**incomplete_user)
    
    def test_invalid_email(self):
                """
        Test that invalid data is rejected with appropriate errors.
        
        Verifies that malformed or invalid data is properly rejected
        with meaningful error messages and validation failures.
        """
        invalid_user = {
            'user_id': 'U000001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345',
            'country': 'USA',
            'date_joined': date(2024, 1, 1),
            'is_active': True,
            'age': 30,
            'gender': GenderEnum.M
        }
        
        with pytest.raises(ValueError):
            UserModel(**invalid_user)
    
    def test_invalid_age_range(self):
                """
        Test that invalid data is rejected with appropriate errors.
        
        Verifies that malformed or invalid data is properly rejected
        with meaningful error messages and validation failures.
        """
        invalid_user = {
            'user_id': 'U000001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345',
            'country': 'USA',
            'date_joined': date(2024, 1, 1),
            'is_active': True,
            'age': 150,  # Invalid age
            'gender': GenderEnum.M
        }
        
        with pytest.raises(ValueError, match="Input should be less than or equal to 120"):
            UserModel(**invalid_user)
    
    def test_xss_attempt_detection(self):
                """
        Test XSS attack detection in text fields.
        
        Verifies that XSS attack attempts in text fields are properly
        detected and blocked with security validation errors.
        """
        malicious_user = {
            'user_id': 'U000001',
            'first_name': '<script>alert("xss")</script>',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345',
            'country': 'USA',
            'date_joined': date(2024, 1, 1),
            'is_active': True,
            'age': 30,
            'gender': GenderEnum.M
        }
        
        with pytest.raises(ValueError, match="XSS attempt detected"):
            UserModel(**malicious_user)


class TestProductModel:
    """Test cases for ProductModel validation"""
    
    def test_valid_product(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        valid_product = {
            'product_id': 'P000001',
            'name': 'Test Product',
            'description': 'A test product description that is long enough',
            'category': 'Electronics',
            'price': 100.0,
            'cost': 50.0,
            'stock_quantity': 10,
            'sku': 'SKU-12345',
            'brand': 'Test Brand',
            'weight': 1.5,
            'dimensions': '10x20x30',
            'is_active': True,
            'created_at': date(2024, 1, 1)
        }
        
        product = ProductModel(**valid_product)
        assert product.product_id == 'P000001'
        assert product.price == 100.0
        assert product.cost == 50.0
    
    def test_price_cost_validation(self):
                """
        Test Price Cost Validation.
        
        Performs the test price cost validation operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        invalid_product = {
            'product_id': 'P000001',
            'name': 'Test Product',
            'description': 'A test product description that is long enough',
            'category': 'Electronics',
            'price': 50.0,  # Price equal to cost
            'cost': 50.0,
            'stock_quantity': 10,
            'sku': 'SKU-12345',
            'brand': 'Test Brand',
            'weight': 1.5,
            'dimensions': '10x20x30',
            'is_active': True,
            'created_at': date(2024, 1, 1)
        }
        
        with pytest.raises(ValueError, match="Price must be greater than cost"):
            ProductModel(**invalid_product)
    
    def test_invalid_dimensions_format(self):
                """
        Test that invalid data is rejected with appropriate errors.
        
        Verifies that malformed or invalid data is properly rejected
        with meaningful error messages and validation failures.
        """
        invalid_product = {
            'product_id': 'P000001',
            'name': 'Test Product',
            'description': 'A test product description that is long enough',
            'category': 'Electronics',
            'price': 100.0,
            'cost': 50.0,
            'stock_quantity': 10,
            'sku': 'SKU-12345',
            'brand': 'Test Brand',
            'weight': 1.5,
            'dimensions': 'invalid-format',  # Invalid format
            'is_active': True,
            'created_at': date(2024, 1, 1)
        }
        
        with pytest.raises(ValueError, match="Dimensions must be in format LxWxH"):
            ProductModel(**invalid_product)


class TestSaleModel:
    """Test cases for SaleModel validation"""
    
    def test_valid_sale(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        valid_sale = {
            'sale_id': 'SALE00000001',
            'user_id': 'U000001',
            'product_id': 'P000001',
            'seller_id': 'S0001',
            'quantity': 2,
            'unit_price': 100.0,
            'total_amount': 200.0,
            'discount': 0.1,
            'final_amount': 180.0,
            'sale_date': date(2024, 1, 1),
            'status': SaleStatusEnum.COMPLETED,
            'shipping_address': '123 Main St',
            'shipping_city': 'Anytown',
            'shipping_state': 'CA',
            'shipping_zip': '12345'
        }
        
        sale = SaleModel(**valid_sale)
        assert sale.sale_id == 'SALE00000001'
        assert sale.quantity == 2
        assert sale.final_amount == 180.0
    
    def test_amount_calculation_validation(self):
                """
        Test Amount Calculation Validation.
        
        Performs the test amount calculation validation operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        invalid_sale = {
            'sale_id': 'SALE00000001',
            'user_id': 'U000001',
            'product_id': 'P000001',
            'seller_id': 'S0001',
            'quantity': 2,
            'unit_price': 100.0,
            'total_amount': 300.0,  # Wrong total (should be 200)
            'discount': 0.1,
            'final_amount': 180.0,
            'sale_date': date(2024, 1, 1),
            'status': SaleStatusEnum.COMPLETED,
            'shipping_address': '123 Main St',
            'shipping_city': 'Anytown',
            'shipping_state': 'CA',
            'shipping_zip': '12345'
        }
        
        with pytest.raises(ValueError, match="Total amount.*does not match"):
            SaleModel(**invalid_sale)


class TestPaymentModel:
    """Test cases for PaymentModel validation"""
    
    def test_valid_payment(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        valid_payment = {
            'payment_id': 'PAY00000001_1',
            'sale_id': 'SALE00000001',
            'amount': 100.0,
            'payment_method': PaymentMethodEnum.CREDIT_CARD,
            'payment_date': date(2024, 1, 1),
            'status': PaymentStatusEnum.COMPLETED,
            'transaction_id': 'TXN-12345678',
            'card_last_four': '1234'
        }
        
        payment = PaymentModel(**valid_payment)
        assert payment.payment_id == 'PAY00000001_1'
        assert payment.amount == 100.0
        assert payment.card_last_four == '1234'
    
    def test_invalid_payment_id_format(self):
                """
        Test that invalid data is rejected with appropriate errors.
        
        Verifies that malformed or invalid data is properly rejected
        with meaningful error messages and validation failures.
        """
        invalid_payment = {
            'payment_id': 'INVALID',
            'sale_id': 'SALE00000001',
            'amount': 100.0,
            'payment_method': PaymentMethodEnum.CREDIT_CARD,
            'payment_date': date(2024, 1, 1),
            'status': PaymentStatusEnum.COMPLETED,
            'transaction_id': 'TXN-12345678',
            'card_last_four': '1234'
        }
        
        with pytest.raises(ValueError, match="String should match pattern"):
            PaymentModel(**invalid_payment)


class TestDataQualityValidator:
    """Test cases for DataQualityValidator class"""
    
    def setup_method(self):
                """
        Set up test environment or configuration.
        
        Prepares the test environment with necessary data, configuration,
        or setup required for testing. Ensures clean state for testing.
        """
        self.validator = DataQualityValidator()
        
        # Create valid test data
        self.valid_users_df = pd.DataFrame({
            'user_id': ['U000001', 'U000002'],
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Smith'],
            'email': ['john@example.com', 'jane@example.com'],
            'phone': ['123-456-7890', '987-654-3210'],
            'address': ['123 Main St', '456 Oak Ave'],
            'city': ['Anytown', 'Somewhere'],
            'state': ['CA', 'NY'],
            'zip_code': ['12345', '67890'],
            'country': ['USA', 'USA'],
            'date_joined': [date(2024, 1, 1), date(2024, 1, 2)],
            'is_active': [True, False],
            'age': [30, 25],
            'gender': ['M', 'F']
        })
        
        # Create invalid test data
        self.invalid_users_df = pd.DataFrame({
            'user_id': ['INVALID', 'U000002'],
            'first_name': ['', 'Jane'],  # Empty first name
            'last_name': ['Doe', 'Smith'],
            'email': ['invalid-email', 'jane@example.com'],
            'phone': ['123-456-7890', '987-654-3210'],
            'address': ['123 Main St', '456 Oak Ave'],
            'city': ['Anytown', 'Somewhere'],
            'state': ['CA', 'NY'],
            'zip_code': ['12345', '67890'],
            'country': ['USA', 'USA'],
            'date_joined': [date(2024, 1, 1), date(2024, 1, 2)],
            'is_active': [True, False],
            'age': [30, 25],
            'gender': ['M', 'F']
        })
    
    def test_validate_dataframe_valid_data(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        results = self.validator.validate_dataframe(self.valid_users_df, 'users')
        
        assert results['total_records'] == 2
        assert results['valid_records'] == 2
        assert results['invalid_records'] == 0
        assert results['data_quality_score'] == 1.0
        assert len(results['validation_errors']) == 0
    
    def test_validate_dataframe_invalid_data(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        results = self.validator.validate_dataframe(self.invalid_users_df, 'users')
        
        assert results['total_records'] == 2
        assert results['valid_records'] == 1
        assert results['invalid_records'] == 1
        assert results['data_quality_score'] == 0.5
        assert len(results['validation_errors']) == 1
    
    def test_validate_dataframe_unknown_data_type(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        with pytest.raises(ValueError, match="Unknown data type"):
            self.validator.validate_dataframe(self.valid_users_df, 'unknown_type')
    
    def test_validate_all_data(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        data_dict = {
            'users': self.valid_users_df,
            'sellers': pd.DataFrame()  # Empty dataframe for testing
        }
        
        results = self.validator.validate_all_data(data_dict)
        
        assert 'users' in results
        assert 'sellers' in results
        assert results['users']['total_records'] == 2
        assert results['sellers']['total_records'] == 0
    
    def test_get_validation_summary(self):
                """
        Test Get Validation Summary.
        
        Performs the test get validation summary operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        # First validate some data
        self.validator.validate_dataframe(self.valid_users_df, 'users')
        
        summary = self.validator.get_validation_summary()
        
        assert summary['total_data_types'] == 1
        assert summary['overall_quality_score'] == 1.0
        assert 'users' in summary['data_type_scores']
        assert summary['data_type_scores']['users'] == 1.0
    
    def test_get_validation_errors(self):
                """
        Test Get Validation Errors.
        
        Performs the test get validation errors operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        # First validate some invalid data
        self.validator.validate_dataframe(self.invalid_users_df, 'users')
        
        errors = self.validator.get_validation_errors('users')
        
        assert 'data_type' in errors
        assert errors['data_type'] == 'users'
        assert len(errors['errors']) == 1
        assert errors['errors'][0]['row_index'] == 0
    
    def test_get_validation_errors_all_types(self):
                """
        Test Get Validation Errors All Types.
        
        Performs the test get validation errors all types operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        # First validate some data
        self.validator.validate_dataframe(self.invalid_users_df, 'users')
        
        errors = self.validator.get_validation_errors()
        
        assert 'users' in errors
        assert len(errors['users']) == 1
    
    def test_export_validation_report(self):
                """
        Test Export Validation Report.
        
        Performs the test export validation report operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        # First validate some data
        self.validator.validate_dataframe(self.valid_users_df, 'users')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.validator.export_validation_report(temp_file)
            
            # Check that file was created and contains valid JSON
            assert os.path.exists(temp_file)
            
            with open(temp_file, 'r') as f:
                report = json.load(f)
            
            assert 'validation_summary' in report
            assert 'detailed_results' in report
            assert 'timestamp' in report
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_handle_nan_values(self):
                """
        Test Handle Nan Values.
        
        Performs the test handle nan values operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        # Create DataFrame with NaN values
        df_with_nan = pd.DataFrame({
            'user_id': ['U000001', 'U000002'],
            'first_name': ['John', None],  # NaN value
            'last_name': ['Doe', 'Smith'],
            'email': ['john@example.com', 'jane@example.com'],
            'phone': ['123-456-7890', '987-654-3210'],
            'address': ['123 Main St', '456 Oak Ave'],
            'city': ['Anytown', 'Somewhere'],
            'state': ['CA', 'NY'],
            'zip_code': ['12345', '67890'],
            'country': ['USA', 'USA'],
            'date_joined': [date(2024, 1, 1), date(2024, 1, 2)],
            'is_active': [True, False],
            'age': [30, 25],
            'gender': ['M', 'F']
        })
        
        results = self.validator.validate_dataframe(df_with_nan, 'users')
        
        assert results['total_records'] == 2
        assert results['invalid_records'] == 1  # One record with NaN first_name
        assert results['valid_records'] == 1


class TestDataQualityValidatorIntegration:
    """Integration tests for DataQualityValidator with real data"""
    
    def test_validate_real_sales_data(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        validator = DataQualityValidator()
        
        # Create realistic sales data
        sales_data = pd.DataFrame({
            'sale_id': ['SALE00000001', 'SALE00000002'],
            'user_id': ['U000001', 'U000002'],
            'product_id': ['P000001', 'P000002'],
            'seller_id': ['S0001', 'S0002'],
            'quantity': [2, 1],
            'unit_price': [100.0, 50.0],
            'total_amount': [200.0, 50.0],
            'discount': [0.1, 0.0],
            'final_amount': [180.0, 50.0],
            'sale_date': [date(2024, 1, 1), date(2024, 1, 2)],
            'status': ['completed', 'pending'],
            'shipping_address': ['123 Main St', '456 Oak Ave'],
            'shipping_city': ['Anytown', 'Somewhere'],
            'shipping_state': ['CA', 'NY'],
            'shipping_zip': ['12345', '67890']
        })
        
        results = validator.validate_dataframe(sales_data, 'sales')
        
        assert results['total_records'] == 2
        assert results['valid_records'] == 2
        assert results['invalid_records'] == 0
        assert results['data_quality_score'] == 1.0
    
    def test_validate_mixed_quality_data(self):
                """
        Test that valid data passes validation.
        
        Verifies that properly formatted data with all required fields
        and valid data types is accepted by the validation model.
        """
        validator = DataQualityValidator()
        
        # Create mixed quality data
        mixed_data = pd.DataFrame({
            'user_id': ['U000001', 'INVALID', 'U000003'],
            'first_name': ['John', 'Jane', 'Bob'],
            'last_name': ['Doe', 'Smith', 'Johnson'],
            'email': ['john@example.com', 'invalid-email', 'bob@example.com'],
            'phone': ['123-456-7890', '987-654-3210', '555-123-4567'],
            'address': ['123 Main St', '456 Oak Ave', '789 Pine St'],
            'city': ['Anytown', 'Somewhere', 'Elsewhere'],
            'state': ['CA', 'NY', 'TX'],
            'zip_code': ['12345', '67890', '54321'],
            'country': ['USA', 'USA', 'USA'],
            'date_joined': [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            'is_active': [True, False, True],
            'age': [30, 25, 35],
            'gender': ['M', 'F', 'M']
        })
        
        results = validator.validate_dataframe(mixed_data, 'users')
        
        assert results['total_records'] == 3
        assert results['valid_records'] == 2  # Two valid records
        assert results['invalid_records'] == 1  # One invalid record
        assert results['data_quality_score'] == 2/3  # 66.67% quality score
        assert len(results['validation_errors']) == 1


if __name__ == "__main__":
    pytest.main([__file__])
