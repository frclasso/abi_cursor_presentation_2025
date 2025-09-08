"""
Demonstration script for Data Quality Validator

This script demonstrates how to use the DataQualityValidator class
with the actual e-commerce data files to perform comprehensive data quality checks.
"""

import pandas as pd
from datetime import datetime
import os
from data_quality_validator import DataQualityValidator


def load_data_files(data_dir="tests/data_sources"):
    """
    Load all e-commerce data files from the specified directory.
    
    Loads users, sellers, products, sales, and payments data from CSV files
    in the specified directory. Performs necessary data type conversions
    for date columns and handles missing files gracefully.
    
    Args:
        data_dir (str): Directory path containing the data files
        
    Returns:
        dict: Dictionary with data type as key and DataFrame as value
    """
    data_files = {
        'users': 'users.csv',
        'sellers': 'sellers.csv', 
        'products': 'products.csv',
        'sales': 'sales.csv',
        'payments': 'payments.csv'
    }
    
    data_dict = {}
    
    for data_type, filename in data_files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            print(f"Loading {data_type} data from {filepath}")
            df = pd.read_csv(filepath)
            
            # Convert date columns
            if data_type == 'users':
                df['date_joined'] = pd.to_datetime(df['date_joined']).dt.date
            elif data_type == 'sellers':
                df['joined_date'] = pd.to_datetime(df['joined_date']).dt.date
            elif data_type == 'products':
                df['created_at'] = pd.to_datetime(df['created_at']).dt.date
            elif data_type == 'sales':
                df['sale_date'] = pd.to_datetime(df['sale_date']).dt.date
            elif data_type == 'payments':
                df['payment_date'] = pd.to_datetime(df['payment_date']).dt.date
            
            data_dict[data_type] = df
            print(f"  Loaded {len(df)} records")
        else:
            print(f"Warning: {filepath} not found")
    
    return data_dict


def load_bad_data_files(data_dir="tests/data_sources"):
            """
        Load data from configured source.
        
        Loads data from the configured data source with proper error
        handling and validation. Supports various data formats and
        provides detailed loading status information.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
    bad_data_files = {
        'users': 'bad_users.csv',
        'sellers': 'bad_sellers.csv', 
        'products': 'bad_products.csv',
        'sales': 'bad_sales.csv',
        'payments': 'bad_payments.csv'
    }
    
    data_dict = {}
    
    for data_type, filename in bad_data_files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            print(f"Loading bad {data_type} data from {filepath}")
            df = pd.read_csv(filepath)
            
            # Convert date columns
            if data_type == 'users':
                df['date_joined'] = pd.to_datetime(df['date_joined'], errors='coerce').dt.date
            elif data_type == 'sellers':
                df['joined_date'] = pd.to_datetime(df['joined_date'], errors='coerce').dt.date
            elif data_type == 'products':
                df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.date
            elif data_type == 'sales':
                df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce').dt.date
            elif data_type == 'payments':
                df['payment_date'] = pd.to_datetime(df['payment_date'], errors='coerce').dt.date
            
            data_dict[data_type] = df
            print(f"  Loaded {len(df)} records")
        else:
            print(f"Warning: {filepath} not found")
    
    return data_dict


def demonstrate_validation():
    """
    Demonstrate comprehensive data quality validation process.
    
    Loads both good and bad e-commerce data, performs validation using
    the DataQualityValidator class, and displays detailed results including
    quality scores, error counts, and sample validation errors. Exports
    a comprehensive validation report to JSON.
    
    Returns:
        DataQualityValidator: The validator instance used for demonstration
    """
    print("=" * 80)
    print("DATA QUALITY VALIDATION DEMONSTRATION")
    print("=" * 80)
    
    # Initialize validator
    validator = DataQualityValidator()
    
    # Load good data
    print("\n1. LOADING GOOD DATA")
    print("-" * 40)
    good_data = load_data_files()
    
    if good_data:
        print("\n2. VALIDATING GOOD DATA")
        print("-" * 40)
        good_results = validator.validate_all_data(good_data)
        
        for data_type, results in good_results.items():
            print(f"\n{data_type.upper()} Data Quality:")
            print(f"  Total records: {results['total_records']:,}")
            print(f"  Valid records: {results['valid_records']:,}")
            print(f"  Invalid records: {results['invalid_records']:,}")
            print(f"  Quality score: {results['data_quality_score']:.2%}")
            
            if results['validation_errors']:
                print(f"  Sample errors:")
                for error in results['validation_errors'][:3]:  # Show first 3 errors
                    print(f"    Row {error['row_index']}: {error['error_message']}")
    
    # Load bad data for comparison
    print("\n3. LOADING BAD DATA FOR COMPARISON")
    print("-" * 40)
    bad_data = load_bad_data_files()
    
    if bad_data:
        print("\n4. VALIDATING BAD DATA")
        print("-" * 40)
        bad_results = validator.validate_all_data(bad_data)
        
        for data_type, results in bad_results.items():
            print(f"\n{data_type.upper()} Data Quality (Bad Data):")
            print(f"  Total records: {results['total_records']:,}")
            print(f"  Valid records: {results['valid_records']:,}")
            print(f"  Invalid records: {results['invalid_records']:,}")
            print(f"  Quality score: {results['data_quality_score']:.2%}")
            
            if results['validation_errors']:
                print(f"  Sample errors:")
                for error in results['validation_errors'][:5]:  # Show first 5 errors
                    print(f"    Row {error['row_index']}: {error['error_message']}")
    
    # Generate summary
    print("\n5. VALIDATION SUMMARY")
    print("-" * 40)
    summary = validator.get_validation_summary()
    
    print(f"Total data types validated: {summary['total_data_types']}")
    print(f"Overall quality score: {summary['overall_quality_score']:.2%}")
    print(f"Total records processed: {summary['total_records']:,}")
    print(f"Total valid records: {summary['total_valid_records']:,}")
    print(f"Total invalid records: {summary['total_invalid_records']:,}")
    
    print("\nData type quality scores:")
    for data_type, score in summary['data_type_scores'].items():
        print(f"  {data_type}: {score:.2%}")
    
    # Export validation report
    print("\n6. EXPORTING VALIDATION REPORT")
    print("-" * 40)
    report_filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    validator.export_validation_report(report_filename)
    print(f"Validation report exported to: {report_filename}")
    
    return validator


def demonstrate_specific_validations():
            """
        Demonstrate Specific Validations.
        
        Performs the demonstrate specific validations operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n" + "=" * 80)
    print("SPECIFIC VALIDATION FEATURES DEMONSTRATION")
    print("=" * 80)
    
    validator = DataQualityValidator()
    
    # Test with a small sample of each data type
    print("\n1. TESTING INDIVIDUAL VALIDATION RULES")
    print("-" * 50)
    
    # Test user validation
    print("\nUser Validation Tests:")
    test_users = pd.DataFrame({
        'user_id': ['U000001', 'INVALID_ID', 'U000003'],
        'first_name': ['John', 'Jane', '<script>alert("xss")</script>'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'email': ['john@example.com', 'invalid-email', 'bob@example.com'],
        'phone': ['123-456-7890', '987-654-3210', '555-123-4567'],
        'address': ['123 Main St', '456 Oak Ave', '789 Pine St'],
        'city': ['Anytown', 'Somewhere', 'Elsewhere'],
        'state': ['CA', 'NY', 'TX'],
        'zip_code': ['12345', '67890', '54321'],
        'country': ['USA', 'USA', 'USA'],
        'date_joined': [pd.Timestamp('2024-01-01').date(), pd.Timestamp('2024-01-02').date(), pd.Timestamp('2024-01-03').date()],
        'is_active': [True, False, True],
        'age': [30, 25, 150],  # One invalid age
        'gender': ['M', 'F', 'M']
    })
    
    user_results = validator.validate_dataframe(test_users, 'users')
    print(f"  Valid records: {user_results['valid_records']}")
    print(f"  Invalid records: {user_results['invalid_records']}")
    print(f"  Quality score: {user_results['data_quality_score']:.2%}")
    
    for error in user_results['validation_errors']:
        print(f"    Error in row {error['row_index']}: {error['error_message']}")
    
    # Test product validation
    print("\nProduct Validation Tests:")
    test_products = pd.DataFrame({
        'product_id': ['P000001', 'P000002', 'P000003'],
        'name': ['Valid Product', 'Another Product', '<script>alert("xss")</script>'],
        'description': ['A valid product description that is long enough', 'Another valid description', 'Valid description'],
        'category': ['Electronics', 'Clothing', 'Books'],
        'price': [100.0, 50.0, 25.0],
        'cost': [50.0, 60.0, 30.0],  # One where cost > price
        'stock_quantity': [10, 5, 0],
        'sku': ['SKU-12345', 'SKU-67890', 'SKU-11111'],
        'brand': ['Brand A', 'Brand B', 'Brand C'],
        'weight': [1.5, 2.0, 'heavy'],  # One invalid weight
        'dimensions': ['10x20x30', '5x10x15', 'invalid-format'],  # One invalid format
        'is_active': [True, False, True],
        'created_at': [pd.Timestamp('2024-01-01').date(), pd.Timestamp('2024-01-02').date(), pd.Timestamp('2024-01-03').date()]
    })
    
    product_results = validator.validate_dataframe(test_products, 'products')
    print(f"  Valid records: {product_results['valid_records']}")
    print(f"  Invalid records: {product_results['invalid_records']}")
    print(f"  Quality score: {product_results['data_quality_score']:.2%}")
    
    for error in product_results['validation_errors']:
        print(f"    Error in row {error['row_index']}: {error['error_message']}")


if __name__ == "__main__":
    # Run the demonstration
    validator = demonstrate_validation()
    demonstrate_specific_validations()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nThe DataQualityValidator provides comprehensive data quality validation")
    print("for e-commerce data using Pydantic models with strict validation rules.")
    print("\nKey features demonstrated:")
    print("- Schema validation for all data types (users, sellers, products, sales, payments)")
    print("- Data type validation (emails, phone numbers, dates, etc.)")
    print("- Business rule validation (price > cost, amount calculations)")
    print("- Security validation (XSS detection)")
    print("- Comprehensive error reporting and quality scoring")
    print("- Export capabilities for validation reports")
