"""
Data Quality Validator using Pydantic for E-commerce Data Validation

This module provides comprehensive data quality validation for sales, sellers, users, 
products, and payments data using Pydantic models with strict validation rules.
"""

import re
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any, Union
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
import pandas as pd


class GenderEnum(str, Enum):
    """
    Enumeration for valid gender values in user data.
    
    This enum defines the allowed gender values that can be used in the UserModel
    validation. It ensures data consistency and prevents invalid gender entries.
    
    Attributes:
        M (str): Male gender identifier
        F (str): Female gender identifier  
        OTHER (str): Other/Non-binary gender identifier
    """
    M = "M"
    F = "F"
    OTHER = "Other"


class PaymentMethodEnum(str, Enum):
    """
    Enumeration for valid payment methods in payment data.
    
    This enum defines the allowed payment methods that can be used in the PaymentModel
    validation. It ensures only valid payment types are accepted.
    
    Attributes:
        CREDIT_CARD (str): Credit card payment method
        DEBIT_CARD (str): Debit card payment method
        PAYPAL (str): PayPal payment method
        CASH (str): Cash payment method
        CHECK (str): Check payment method
    """
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    CASH = "cash"
    CHECK = "check"


class PaymentStatusEnum(str, Enum):
    """
    Enumeration for valid payment statuses in payment data.
    
    This enum defines the allowed payment statuses that can be used in the PaymentModel
    validation. It ensures only valid payment states are accepted.
    
    Attributes:
        COMPLETED (str): Payment successfully completed
        PENDING (str): Payment is pending processing
        FAILED (str): Payment processing failed
        REFUNDED (str): Payment has been refunded
        UNPAID (str): Payment is unpaid
    """
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"
    REFUNDED = "refunded"
    UNPAID = "unpaid"


class SaleStatusEnum(str, Enum):
    """
    Enumeration for valid sale statuses in sales data.
    
    This enum defines the allowed sale statuses that can be used in the SaleModel
    validation. It ensures only valid sale states are accepted.
    
    Attributes:
        COMPLETED (str): Sale has been completed successfully
        PENDING (str): Sale is pending processing
        PROCESSING (str): Sale is currently being processed
        CANCELLED (str): Sale has been cancelled
        REFUNDED (str): Sale has been refunded
    """
    COMPLETED = "completed"
    PENDING = "pending"
    PROCESSING = "processing"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class UserModel(BaseModel):
    """
    Pydantic model for comprehensive user data validation.
    
    This model validates user data with strict rules for data quality, security,
    and business logic compliance. It ensures all user information meets the
    required standards for e-commerce applications.
    
    Attributes:
        user_id (str): Unique user identifier in format U000000
        first_name (str): User's first name (1-100 characters)
        last_name (str): User's last name (1-100 characters)
        email (EmailStr): Valid email address
        phone (str): Phone number (10-20 characters, valid format)
        address (str): User's address (5-200 characters)
        city (str): User's city (2-100 characters)
        state (str): User's state (2-50 characters)
        zip_code (str): ZIP code in format 12345 or 12345-6789
        country (str): User's country (2-100 characters)
        date_joined (date): Date when user joined
        is_active (bool): Whether user account is active
        age (int): User's age (0-120 years)
        gender (GenderEnum): User's gender (M, F, or Other)
    
    Raises:
        ValidationError: If any field fails validation rules
        ValueError: If XSS attempts are detected in text fields
    """
    user_id: str = Field(..., pattern=r'^U\d{6}$', description="User ID must be in format U000000")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name is required")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name is required")
    email: EmailStr = Field(..., description="Valid email address required")
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number required")
    address: str = Field(..., min_length=5, max_length=200, description="Address required")
    city: str = Field(..., min_length=2, max_length=100, description="City required")
    state: str = Field(..., min_length=2, max_length=50, description="State required")
    zip_code: str = Field(..., min_length=5, max_length=10, description="ZIP code required")
    country: str = Field(..., min_length=2, max_length=100, description="Country required")
    date_joined: date = Field(..., description="Date joined required")
    is_active: bool = Field(..., description="Active status required")
    age: int = Field(..., ge=0, le=120, description="Age must be between 0 and 120")
    gender: GenderEnum = Field(..., description="Gender must be M, F, or Other")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """
        Validate phone number format and characters.
        
        Ensures the phone number contains only valid characters including digits,
        hyphens, plus signs, parentheses, periods, spaces, and 'x' for extensions.
        
        Args:
            v (str): Phone number to validate
            
        Returns:
            str: Validated phone number
            
        Raises:
            ValueError: If phone number contains invalid characters
        """
        if not re.match(r'^[\d\-\+\(\)\.\sx]+$', v):
            raise ValueError('Phone number contains invalid characters')
        return v

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v):
        """Validate ZIP code format"""
        if not re.match(r'^\d{5}(-\d{4})?$', v):
            raise ValueError('ZIP code must be in format 12345 or 12345-6789')
        return v

    @field_validator('first_name', 'last_name', 'city', 'state', 'country')
    @classmethod
    def validate_no_xss(cls, v):
        """Validate no XSS attempts in text fields"""
        if '<script>' in v.lower() or 'javascript:' in v.lower():
            raise ValueError('XSS attempt detected in text field')
        return v


class SellerModel(BaseModel):
    """Pydantic model for seller data validation"""
    seller_id: str = Field(..., pattern=r'^S\d{4}$', description="Seller ID must be in format S0000")
    company_name: str = Field(..., min_length=1, max_length=200, description="Company name required")
    contact_name: str = Field(..., min_length=1, max_length=100, description="Contact name required")
    email: EmailStr = Field(..., description="Valid email address required")
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number required")
    address: str = Field(..., min_length=5, max_length=200, description="Address required")
    city: str = Field(..., min_length=2, max_length=100, description="City required")
    state: str = Field(..., min_length=2, max_length=50, description="State required")
    zip_code: str = Field(..., min_length=5, max_length=10, description="ZIP code required")
    country: str = Field(..., min_length=2, max_length=100, description="Country required")
    tax_id: str = Field(..., min_length=5, max_length=20, description="Tax ID required")
    rating: float = Field(..., ge=0.0, le=5.0, description="Rating must be between 0.0 and 5.0")
    total_sales: int = Field(..., ge=0, description="Total sales must be non-negative")
    is_verified: bool = Field(..., description="Verification status required")
    joined_date: date = Field(..., description="Joined date required")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format"""
        if not re.match(r'^[\d\-\+\(\)\.\sx]+$', v):
            raise ValueError('Phone number contains invalid characters')
        return v

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v):
        """Validate ZIP code format"""
        if not re.match(r'^\d{5}(-\d{4})?$', v):
            raise ValueError('ZIP code must be in format 12345 or 12345-6789')
        return v

    @field_validator('company_name', 'contact_name', 'city', 'state', 'country')
    @classmethod
    def validate_no_xss(cls, v):
        """Validate no XSS attempts in text fields"""
        if '<script>' in v.lower() or 'javascript:' in v.lower():
            raise ValueError('XSS attempt detected in text field')
        return v


class ProductModel(BaseModel):
    """Pydantic model for product data validation"""
    product_id: str = Field(..., pattern=r'^P\d{6}$', description="Product ID must be in format P000000")
    name: str = Field(..., min_length=1, max_length=200, description="Product name required")
    description: str = Field(..., min_length=10, max_length=1000, description="Product description required")
    category: str = Field(..., min_length=2, max_length=50, description="Category required")
    price: float = Field(..., gt=0, description="Price must be positive")
    cost: float = Field(..., ge=0, description="Cost must be non-negative")
    stock_quantity: int = Field(..., ge=0, description="Stock quantity must be non-negative")
    sku: str = Field(..., min_length=5, max_length=50, description="SKU required")
    brand: str = Field(..., min_length=1, max_length=100, description="Brand required")
    weight: Union[float, str] = Field(..., description="Weight required")
    dimensions: str = Field(..., min_length=3, max_length=50, description="Dimensions required")
    is_active: bool = Field(..., description="Active status required")
    created_at: date = Field(..., description="Created date required")

    @field_validator('weight')
    @classmethod
    def validate_weight(cls, v):
        """Validate weight is numeric if string"""
        if isinstance(v, str):
            try:
                float(v)
            except ValueError:
                raise ValueError('Weight must be numeric')
        return v

    @field_validator('dimensions')
    @classmethod
    def validate_dimensions(cls, v):
        """Validate dimensions format"""
        if not re.match(r'^\d+x\d+x\d+$', v):
            raise ValueError('Dimensions must be in format LxWxH (e.g., 10x20x30)')
        return v

    @field_validator('name', 'description', 'category', 'brand')
    @classmethod
    def validate_no_xss(cls, v):
        """Validate no XSS attempts in text fields"""
        if '<script>' in v.lower() or 'javascript:' in v.lower():
            raise ValueError('XSS attempt detected in text field')
        return v

    @model_validator(mode='after')
    def validate_price_cost_relationship(self):
        """Validate that price is greater than cost"""
        if self.price <= self.cost:
            raise ValueError('Price must be greater than cost for profitability')
        return self


class SaleModel(BaseModel):
    """Pydantic model for sale data validation"""
    sale_id: str = Field(..., pattern=r'^SALE\d{8}$', description="Sale ID must be in format SALE00000000")
    user_id: str = Field(..., pattern=r'^U\d{6}$', description="User ID must be in format U000000")
    product_id: str = Field(..., pattern=r'^P\d{6}$', description="Product ID must be in format P000000")
    seller_id: str = Field(..., pattern=r'^S\d{4}$', description="Seller ID must be in format S0000")
    quantity: int = Field(..., gt=0, description="Quantity must be positive")
    unit_price: float = Field(..., gt=0, description="Unit price must be positive")
    total_amount: float = Field(..., ge=0, description="Total amount must be non-negative")
    discount: float = Field(..., ge=0.0, le=1.0, description="Discount must be between 0.0 and 1.0")
    final_amount: float = Field(..., ge=0, description="Final amount must be non-negative")
    sale_date: date = Field(..., description="Sale date required")
    status: SaleStatusEnum = Field(..., description="Valid sale status required")
    shipping_address: str = Field(..., min_length=5, max_length=200, description="Shipping address required")
    shipping_city: str = Field(..., min_length=2, max_length=100, description="Shipping city required")
    shipping_state: str = Field(..., min_length=2, max_length=50, description="Shipping state required")
    shipping_zip: str = Field(..., min_length=5, max_length=10, description="Shipping ZIP required")

    @field_validator('shipping_zip')
    @classmethod
    def validate_shipping_zip(cls, v):
        """Validate shipping ZIP code format"""
        if not re.match(r'^\d{5}(-\d{4})?$', v):
            raise ValueError('Shipping ZIP code must be in format 12345 or 12345-6789')
        return v

    @field_validator('shipping_address', 'shipping_city', 'shipping_state')
    @classmethod
    def validate_no_xss(cls, v):
        """Validate no XSS attempts in shipping fields"""
        if '<script>' in v.lower() or 'javascript:' in v.lower():
            raise ValueError('XSS attempt detected in shipping field')
        return v

    @model_validator(mode='after')
    def validate_amounts(self):
        """Validate amount calculations"""
        expected_total = self.quantity * self.unit_price
        expected_final = self.total_amount * (1 - self.discount)
        
        if abs(self.total_amount - expected_total) > 0.01:
            raise ValueError(f'Total amount {self.total_amount} does not match quantity * unit_price {expected_total}')
        
        if abs(self.final_amount - expected_final) > 0.01:
            raise ValueError(f'Final amount {self.final_amount} does not match total_amount * (1 - discount) {expected_final}')
        
        return self


class PaymentModel(BaseModel):
    """Pydantic model for payment data validation"""
    payment_id: str = Field(..., pattern=r'^PAY\d{8}_\d+$', description="Payment ID must be in format PAY00000000_1")
    sale_id: str = Field(..., pattern=r'^SALE\d{8}$', description="Sale ID must be in format SALE00000000")
    amount: float = Field(..., gt=0, description="Payment amount must be positive")
    payment_method: PaymentMethodEnum = Field(..., description="Valid payment method required")
    payment_date: date = Field(..., description="Payment date required")
    status: PaymentStatusEnum = Field(..., description="Valid payment status required")
    transaction_id: str = Field(..., min_length=5, max_length=50, description="Transaction ID required")
    card_last_four: Optional[str] = Field(None, pattern=r'^\d{4}$', description="Card last four digits must be 4 digits")

    @field_validator('transaction_id')
    @classmethod
    def validate_no_xss(cls, v):
        """Validate no XSS attempts in transaction ID"""
        if '<script>' in v.lower() or 'javascript:' in v.lower():
            raise ValueError('XSS attempt detected in transaction ID')
        return v


class DataQualityValidator:
    """
    Comprehensive data quality validator using Pydantic models
    """
    
    def __init__(self):
        self.models = {
            'users': UserModel,
            'sellers': SellerModel,
            'products': ProductModel,
            'sales': SaleModel,
            'payments': PaymentModel
        }
        self.validation_results = {}
    
    def validate_dataframe(self, df: pd.DataFrame, data_type: str) -> Dict[str, Any]:
        """
        Validate a pandas DataFrame against the appropriate Pydantic model
        
        Args:
            df: Pandas DataFrame to validate
            data_type: Type of data ('users', 'sellers', 'products', 'sales', 'payments')
            
        Returns:
            Dictionary containing validation results
        """
        if data_type not in self.models:
            raise ValueError(f"Unknown data type: {data_type}. Must be one of {list(self.models.keys())}")
        
        model = self.models[data_type]
        results = {
            'total_records': len(df),
            'valid_records': 0,
            'invalid_records': 0,
            'validation_errors': [],
            'data_quality_score': 0.0
        }
        
        for index, row in df.iterrows():
            try:
                # Convert pandas row to dictionary and handle NaN values
                row_dict = row.to_dict()
                
                # Replace NaN values with None for Pydantic validation
                for key, value in row_dict.items():
                    if pd.isna(value):
                        row_dict[key] = None
                
                # Validate the record
                model(**row_dict)
                results['valid_records'] += 1
                
            except Exception as e:
                results['invalid_records'] += 1
                results['validation_errors'].append({
                    'row_index': index,
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'record_data': row_dict
                })
        
        # Calculate data quality score
        if results['total_records'] > 0:
            results['data_quality_score'] = results['valid_records'] / results['total_records']
        
        self.validation_results[data_type] = results
        return results
    
    def validate_all_data(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Validate all data types in the provided dictionary
        
        Args:
            data_dict: Dictionary with data type as key and DataFrame as value
            
        Returns:
            Dictionary containing validation results for all data types
        """
        all_results = {}
        
        for data_type, df in data_dict.items():
            all_results[data_type] = self.validate_dataframe(df, data_type)
        
        return all_results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all validation results
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.validation_results:
            return {"message": "No validation results available"}
        
        summary = {
            'total_data_types': len(self.validation_results),
            'overall_quality_score': 0.0,
            'data_type_scores': {},
            'total_records': 0,
            'total_valid_records': 0,
            'total_invalid_records': 0
        }
        
        total_records = 0
        total_valid = 0
        
        for data_type, results in self.validation_results.items():
            summary['data_type_scores'][data_type] = results['data_quality_score']
            summary['total_records'] += results['total_records']
            summary['total_valid_records'] += results['valid_records']
            summary['total_invalid_records'] += results['invalid_records']
            total_records += results['total_records']
            total_valid += results['valid_records']
        
        if total_records > 0:
            summary['overall_quality_score'] = total_valid / total_records
        
        return summary
    
    def get_validation_errors(self, data_type: str = None) -> Dict[str, Any]:
        """
        Get validation errors for a specific data type or all data types
        
        Args:
            data_type: Specific data type to get errors for, or None for all
            
        Returns:
            Dictionary containing validation errors
        """
        if data_type:
            if data_type not in self.validation_results:
                return {"error": f"No validation results for data type: {data_type}"}
            return {
                'data_type': data_type,
                'errors': self.validation_results[data_type]['validation_errors']
            }
        
        return {
            data_type: results['validation_errors'] 
            for data_type, results in self.validation_results.items()
        }
    
    def export_validation_report(self, output_file: str = "validation_report.json") -> None:
        """
        Export validation results to a JSON file
        
        Args:
            output_file: Path to output file
        """
        import json
        
        report = {
            'validation_summary': self.get_validation_summary(),
            'detailed_results': self.validation_results,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Validation report exported to {output_file}")


# Example usage and testing functions
def validate_sample_data():
    """Example function to demonstrate validation usage"""
    import pandas as pd
    
    # Create sample data
    sample_users = pd.DataFrame({
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
        'date_joined': ['2024-01-01', '2024-01-02'],
        'is_active': [True, False],
        'age': [30, 25],
        'gender': ['M', 'F']
    })
    
    # Initialize validator
    validator = DataQualityValidator()
    
    # Validate data
    results = validator.validate_dataframe(sample_users, 'users')
    
    print("Validation Results:")
    print(f"Total records: {results['total_records']}")
    print(f"Valid records: {results['valid_records']}")
    print(f"Invalid records: {results['invalid_records']}")
    print(f"Data quality score: {results['data_quality_score']:.2%}")
    
    if results['validation_errors']:
        print("\nValidation Errors:")
        for error in results['validation_errors']:
            print(f"Row {error['row_index']}: {error['error_message']}")


if __name__ == "__main__":
    validate_sample_data()
