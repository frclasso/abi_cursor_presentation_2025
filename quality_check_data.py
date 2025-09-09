"""
Data Quality Validation for E-commerce Data

This module provides comprehensive data quality validation for e-commerce data
including business rule validation, data consistency checks, and data integrity
verification beyond basic schema validation.

Author: AI Assistant
Date: 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
import re
from decimal import Decimal
import warnings
warnings.filterwarnings('ignore')


class DataQualityValidator:
    """
    Comprehensive data quality validator for e-commerce data.
    
    This class provides methods to validate data quality beyond schema validation,
    including business rule validation, data consistency checks, and data integrity
    verification for users, products, sellers, sales, and payments.
    """
    
    def __init__(self):
        """Initialize the data quality validator."""
        self.validation_rules = {
            'users': self._get_user_validation_rules(),
            'products': self._get_product_validation_rules(),
            'sellers': self._get_seller_validation_rules(),
            'sales': self._get_sales_validation_rules(),
            'payments': self._get_payment_validation_rules()
        }
    
    def _get_user_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for user data."""
        return {
            'required_fields': ['user_id', 'first_name', 'last_name', 'email', 'phone'],
            'email_format': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone_format': r'^[\d\-\+\(\)\s]+$',
            'min_phone_digits': 10,
            'valid_genders': ['M', 'F', 'Other'],
            'age_range': (18, 100),
            'email_domains_blacklist': ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
        }
    
    def _get_product_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for product data."""
        return {
            'required_fields': ['product_id', 'name', 'price', 'category'],
            'price_range': (0.01, 100000.00),
            'rating_range': (1.0, 5.0),
            'stock_min': 0,
            'weight_min': 0.01,
            'valid_categories': [
                'Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports',
                'Beauty', 'Toys', 'Automotive', 'Health', 'Food & Beverages'
            ],
            'dimension_format': r'^\d+x\d+x\d+$'
        }
    
    def _get_seller_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for seller data."""
        return {
            'required_fields': ['seller_id', 'company_name', 'email', 'business_type'],
            'email_format': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone_format': r'^[\d\-\+\(\)\s]+$',
            'min_phone_digits': 10,
            'valid_business_types': ['Individual', 'Corporation', 'LLC', 'Partnership'],
            'tax_id_format': r'^\d{2}-\d{7}$',
            'rating_range': (1.0, 5.0),
            'commission_range': (0.0, 0.5)
        }
    
    def _get_sales_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for sales data."""
        return {
            'required_fields': ['sale_id', 'user_id', 'product_id', 'seller_id', 'total_amount'],
            'valid_statuses': ['completed', 'pending', 'cancelled', 'refunded'],
            'quantity_min': 1,
            'amount_min': 0.01,
            'discount_rate_max': 1.0,
            'tax_rate_max': 0.5,
            'date_range_days': 365
        }
    
    def _get_payment_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for payment data."""
        return {
            'required_fields': ['payment_id', 'sale_id', 'amount', 'payment_method'],
            'valid_methods': ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cryptocurrency'],
            'valid_statuses': ['completed', 'pending', 'failed'],
            'valid_gateways': ['stripe', 'paypal', 'square', 'adyen'],
            'valid_currencies': ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'CNY'],
            'amount_min': 0.01,
            'transaction_id_format': r'^TXN[A-Z0-9]+$'
        }
    
    def validate_data_quality(self, data_type: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate data quality for a specific data type.
        
        Args:
            data_type (str): Type of data ('users', 'products', 'sellers', 'sales', 'payments')
            df (pd.DataFrame): DataFrame to validate
            
        Returns:
            Dict[str, Any]: Validation results with quality metrics and issues
        """
        if data_type not in self.validation_rules:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        rules = self.validation_rules[data_type]
        results = {
            'data_type': data_type,
            'total_records': len(df),
            'quality_score': 0.0,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check for missing required fields
        missing_fields = self._check_missing_required_fields(df, rules['required_fields'])
        if missing_fields:
            results['issues'].extend(missing_fields)
        
        # Check for null values
        null_issues = self._check_null_values(df)
        if null_issues:
            results['issues'].extend(null_issues)
        
        # Check for duplicates
        duplicate_issues = self._check_duplicates(df, data_type)
        if duplicate_issues:
            results['issues'].extend(duplicate_issues)
        
        # Check data format and patterns
        format_issues = self._check_data_formats(df, data_type, rules)
        if format_issues:
            results['issues'].extend(format_issues)
        
        # Check business rules
        business_rule_issues = self._check_business_rules(df, data_type, rules)
        if business_rule_issues:
            results['issues'].extend(business_rule_issues)
        
        # Check data consistency
        consistency_issues = self._check_data_consistency(df, data_type)
        if consistency_issues:
            results['warnings'].extend(consistency_issues)
        
        # Calculate quality score
        results['quality_score'] = self._calculate_quality_score(results)
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _check_missing_required_fields(self, df: pd.DataFrame, required_fields: List[str]) -> List[Dict]:
        """Check for missing required fields."""
        issues = []
        
        for field in required_fields:
            if field not in df.columns:
                issues.append({
                    'type': 'missing_field',
                    'field': field,
                    'severity': 'error',
                    'message': f'Required field "{field}" is missing from the dataset'
                })
        
        return issues
    
    def _check_null_values(self, df: pd.DataFrame) -> List[Dict]:
        """Check for null values in critical fields."""
        issues = []
        
        for column in df.columns:
            null_count = df[column].isnull().sum()
            if null_count > 0:
                null_percentage = (null_count / len(df)) * 100
                
                severity = 'error' if null_percentage > 10 else 'warning'
                
                issues.append({
                    'type': 'null_values',
                    'field': column,
                    'severity': severity,
                    'count': int(null_count),
                    'percentage': round(null_percentage, 2),
                    'message': f'Field "{column}" has {null_count} null values ({null_percentage:.2f}%)'
                })
        
        return issues
    
    def _check_duplicates(self, df: pd.DataFrame, data_type: str) -> List[Dict]:
        """Check for duplicate records."""
        issues = []
        
        # Define primary key fields for each data type
        primary_keys = {
            'users': 'user_id',
            'products': 'product_id',
            'sellers': 'seller_id',
            'sales': 'sale_id',
            'payments': 'payment_id'
        }
        
        if data_type in primary_keys:
            pk_field = primary_keys[data_type]
            if pk_field in df.columns:
                duplicate_count = df[pk_field].duplicated().sum()
                if duplicate_count > 0:
                    issues.append({
                        'type': 'duplicates',
                        'field': pk_field,
                        'severity': 'error',
                        'count': int(duplicate_count),
                        'message': f'Found {duplicate_count} duplicate records based on {pk_field}'
                    })
        
        return issues
    
    def _check_data_formats(self, df: pd.DataFrame, data_type: str, rules: Dict) -> List[Dict]:
        """Check data format and patterns."""
        issues = []
        
        if data_type == 'users':
            # Check email format
            if 'email' in df.columns:
                email_pattern = rules['email_format']
                invalid_emails = df[df['email'].notna() & ~df['email'].str.match(email_pattern, na=False)]
                if len(invalid_emails) > 0:
                    issues.append({
                        'type': 'format_error',
                        'field': 'email',
                        'severity': 'error',
                        'count': len(invalid_emails),
                        'message': f'Found {len(invalid_emails)} invalid email formats'
                    })
            
            # Check phone format
            if 'phone' in df.columns:
                phone_pattern = rules['phone_format']
                invalid_phones = df[df['phone'].notna() & ~df['phone'].str.match(phone_pattern, na=False)]
                if len(invalid_phones) > 0:
                    issues.append({
                        'type': 'format_error',
                        'field': 'phone',
                        'severity': 'warning',
                        'count': len(invalid_phones),
                        'message': f'Found {len(invalid_phones)} invalid phone formats'
                    })
        
        elif data_type == 'products':
            # Check dimensions format
            if 'dimensions' in df.columns:
                dim_pattern = rules['dimension_format']
                invalid_dims = df[df['dimensions'].notna() & ~df['dimensions'].str.match(dim_pattern, na=False)]
                if len(invalid_dims) > 0:
                    issues.append({
                        'type': 'format_error',
                        'field': 'dimensions',
                        'severity': 'warning',
                        'count': len(invalid_dims),
                        'message': f'Found {len(invalid_dims)} invalid dimension formats'
                    })
        
        elif data_type == 'sellers':
            # Check tax ID format
            if 'tax_id' in df.columns:
                tax_pattern = rules['tax_id_format']
                invalid_tax_ids = df[df['tax_id'].notna() & ~df['tax_id'].str.match(tax_pattern, na=False)]
                if len(invalid_tax_ids) > 0:
                    issues.append({
                        'type': 'format_error',
                        'field': 'tax_id',
                        'severity': 'error',
                        'count': len(invalid_tax_ids),
                        'message': f'Found {len(invalid_tax_ids)} invalid tax ID formats'
                    })
        
        return issues
    
    def _check_business_rules(self, df: pd.DataFrame, data_type: str, rules: Dict) -> List[Dict]:
        """Check business rules and constraints."""
        issues = []
        
        if data_type == 'users':
            # Check age range
            if 'date_of_birth' in df.columns:
                current_year = datetime.now().year
                df['age'] = current_year - pd.to_datetime(df['date_of_birth']).dt.year
                invalid_ages = df[(df['age'] < rules['age_range'][0]) | (df['age'] > rules['age_range'][1])]
                if len(invalid_ages) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'date_of_birth',
                        'severity': 'error',
                        'count': len(invalid_ages),
                        'message': f'Found {len(invalid_ages)} users with age outside valid range ({rules["age_range"][0]}-{rules["age_range"][1]})'
                    })
            
            # Check gender values
            if 'gender' in df.columns:
                invalid_genders = df[df['gender'].notna() & ~df['gender'].isin(rules['valid_genders'])]
                if len(invalid_genders) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'gender',
                        'severity': 'warning',
                        'count': len(invalid_genders),
                        'message': f'Found {len(invalid_genders)} users with invalid gender values'
                    })
        
        elif data_type == 'products':
            # Check price range
            if 'price' in df.columns:
                invalid_prices = df[(df['price'] < rules['price_range'][0]) | (df['price'] > rules['price_range'][1])]
                if len(invalid_prices) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'price',
                        'severity': 'error',
                        'count': len(invalid_prices),
                        'message': f'Found {len(invalid_prices)} products with price outside valid range'
                    })
            
            # Check rating range
            if 'rating' in df.columns:
                invalid_ratings = df[(df['rating'] < rules['rating_range'][0]) | (df['rating'] > rules['rating_range'][1])]
                if len(invalid_ratings) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'rating',
                        'severity': 'warning',
                        'count': len(invalid_ratings),
                        'message': f'Found {len(invalid_ratings)} products with rating outside valid range'
                    })
            
            # Check categories
            if 'category' in df.columns:
                invalid_categories = df[df['category'].notna() & ~df['category'].isin(rules['valid_categories'])]
                if len(invalid_categories) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'category',
                        'severity': 'warning',
                        'count': len(invalid_categories),
                        'message': f'Found {len(invalid_categories)} products with invalid categories'
                    })
        
        elif data_type == 'sales':
            # Check quantity
            if 'quantity' in df.columns:
                invalid_quantities = df[df['quantity'] < rules['quantity_min']]
                if len(invalid_quantities) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'quantity',
                        'severity': 'error',
                        'count': len(invalid_quantities),
                        'message': f'Found {len(invalid_quantities)} sales with invalid quantities'
                    })
            
            # Check status values
            if 'status' in df.columns:
                invalid_statuses = df[df['status'].notna() & ~df['status'].isin(rules['valid_statuses'])]
                if len(invalid_statuses) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'status',
                        'severity': 'error',
                        'count': len(invalid_statuses),
                        'message': f'Found {len(invalid_statuses)} sales with invalid status values'
                    })
        
        elif data_type == 'payments':
            # Check payment methods
            if 'payment_method' in df.columns:
                invalid_methods = df[df['payment_method'].notna() & ~df['payment_method'].isin(rules['valid_methods'])]
                if len(invalid_methods) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'payment_method',
                        'severity': 'error',
                        'count': len(invalid_methods),
                        'message': f'Found {len(invalid_methods)} payments with invalid payment methods'
                    })
            
            # Check currencies
            if 'currency' in df.columns:
                invalid_currencies = df[df['currency'].notna() & ~df['currency'].isin(rules['valid_currencies'])]
                if len(invalid_currencies) > 0:
                    issues.append({
                        'type': 'business_rule',
                        'field': 'currency',
                        'severity': 'warning',
                        'count': len(invalid_currencies),
                        'message': f'Found {len(invalid_currencies)} payments with invalid currencies'
                    })
        
        return issues
    
    def _check_data_consistency(self, df: pd.DataFrame, data_type: str) -> List[Dict]:
        """Check data consistency and relationships."""
        warnings = []
        
        if data_type == 'sales':
            # Check if total_amount calculation is consistent
            if all(col in df.columns for col in ['subtotal', 'discount_amount', 'tax_amount', 'total_amount']):
                calculated_total = df['subtotal'] - df['discount_amount'] + df['tax_amount']
                inconsistent_totals = df[abs(df['total_amount'] - calculated_total) > 0.01]
                if len(inconsistent_totals) > 0:
                    warnings.append({
                        'type': 'consistency',
                        'field': 'total_amount',
                        'severity': 'warning',
                        'count': len(inconsistent_totals),
                        'message': f'Found {len(inconsistent_totals)} sales with inconsistent total amount calculations'
                    })
        
        return warnings
    
    def _calculate_quality_score(self, results: Dict) -> float:
        """Calculate overall data quality score."""
        total_issues = len(results['issues'])
        total_warnings = len(results['warnings'])
        total_records = results['total_records']
        
        if total_records == 0:
            return 0.0
        
        # Weight issues more heavily than warnings
        penalty = (total_issues * 2 + total_warnings) / total_records
        quality_score = max(0.0, 100.0 - (penalty * 100))
        
        return round(quality_score, 2)
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        # Check for high null value percentages
        null_issues = [issue for issue in results['issues'] if issue['type'] == 'null_values']
        for issue in null_issues:
            if issue['percentage'] > 20:
                recommendations.append(f"Consider data imputation for field '{issue['field']}' (missing {issue['percentage']:.1f}%)")
        
        # Check for format errors
        format_issues = [issue for issue in results['issues'] if issue['type'] == 'format_error']
        if format_issues:
            recommendations.append("Review and fix data format issues, especially for email and phone fields")
        
        # Check for duplicates
        duplicate_issues = [issue for issue in results['issues'] if issue['type'] == 'duplicates']
        if duplicate_issues:
            recommendations.append("Remove or merge duplicate records to improve data integrity")
        
        # Check for business rule violations
        business_rule_issues = [issue for issue in results['issues'] if issue['type'] == 'business_rule']
        if business_rule_issues:
            recommendations.append("Review business rule violations and update data accordingly")
        
        # General recommendations based on quality score
        if results['quality_score'] < 70:
            recommendations.append("Overall data quality is low. Consider comprehensive data cleaning and validation")
        elif results['quality_score'] < 90:
            recommendations.append("Data quality is acceptable but could be improved with minor cleanup")
        else:
            recommendations.append("Data quality is excellent. Maintain current data management practices")
        
        return recommendations
    
    def validate_cross_references(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Validate cross-references between different data types.
        
        Args:
            data_dict (Dict[str, pd.DataFrame]): Dictionary containing all data types
            
        Returns:
            Dict[str, Any]: Cross-reference validation results
        """
        results = {
            'cross_reference_issues': [],
            'orphaned_records': {},
            'recommendations': []
        }
        
        # Check sales -> users references
        if 'sales' in data_dict and 'users' in data_dict:
            sales_df = data_dict['sales']
            users_df = data_dict['users']
            
            if 'user_id' in sales_df.columns and 'user_id' in users_df.columns:
                orphaned_sales = sales_df[~sales_df['user_id'].isin(users_df['user_id'])]
                if len(orphaned_sales) > 0:
                    results['cross_reference_issues'].append({
                        'type': 'orphaned_sales',
                        'count': len(orphaned_sales),
                        'message': f'Found {len(orphaned_sales)} sales with invalid user_id references'
                    })
                    results['orphaned_records']['sales_users'] = orphaned_sales['user_id'].tolist()
        
        # Check sales -> products references
        if 'sales' in data_dict and 'products' in data_dict:
            sales_df = data_dict['sales']
            products_df = data_dict['products']
            
            if 'product_id' in sales_df.columns and 'product_id' in products_df.columns:
                orphaned_sales = sales_df[~sales_df['product_id'].isin(products_df['product_id'])]
                if len(orphaned_sales) > 0:
                    results['cross_reference_issues'].append({
                        'type': 'orphaned_sales',
                        'count': len(orphaned_sales),
                        'message': f'Found {len(orphaned_sales)} sales with invalid product_id references'
                    })
                    results['orphaned_records']['sales_products'] = orphaned_sales['product_id'].tolist()
        
        # Check payments -> sales references
        if 'payments' in data_dict and 'sales' in data_dict:
            payments_df = data_dict['payments']
            sales_df = data_dict['sales']
            
            if 'sale_id' in payments_df.columns and 'sale_id' in sales_df.columns:
                orphaned_payments = payments_df[~payments_df['sale_id'].isin(sales_df['sale_id'])]
                if len(orphaned_payments) > 0:
                    results['cross_reference_issues'].append({
                        'type': 'orphaned_payments',
                        'count': len(orphaned_payments),
                        'message': f'Found {len(orphaned_payments)} payments with invalid sale_id references'
                    })
                    results['orphaned_records']['payments_sales'] = orphaned_payments['sale_id'].tolist()
        
        # Generate recommendations
        if results['cross_reference_issues']:
            results['recommendations'].append("Fix orphaned records to maintain referential integrity")
            results['recommendations'].append("Implement foreign key constraints in your database")
        else:
            results['recommendations'].append("All cross-references are valid. Data integrity is maintained")
        
        return results


def main():
    """
    Main function to demonstrate data quality validation usage.
    """
    validator = DataQualityValidator()
    
    # Example usage
    print("Data Quality Validator Demo")
    print("=" * 50)
    
    # Create sample data with quality issues
    sample_data = pd.DataFrame({
        'user_id': ['U000001', 'U000002', 'U000003', 'U000001'],  # Duplicate
        'email': ['valid@example.com', 'invalid-email', 'test@domain.com', 'another@test.com'],
        'phone': ['123-456-7890', 'invalid-phone', '555-123-4567', '111-222-3333'],
        'age': [25, 150, 30, 18]  # Invalid age
    })
    
    # Validate data quality
    results = validator.validate_data_quality('users', sample_data)
    
    print(f"Data Quality Score: {results['quality_score']}%")
    print(f"Total Issues: {len(results['issues'])}")
    print(f"Total Warnings: {len(results['warnings'])}")
    
    print("\nIssues Found:")
    for issue in results['issues']:
        print(f"- {issue['message']}")
    
    print("\nRecommendations:")
    for rec in results['recommendations']:
        print(f"- {rec}")


if __name__ == "__main__":
    main()
