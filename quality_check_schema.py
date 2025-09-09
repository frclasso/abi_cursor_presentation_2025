"""
Schema Validation for E-commerce Data Quality

This module provides Pydantic-based schema validation for e-commerce data
including users, products, sellers, sales, and payments. It ensures that
data structures conform to expected schemas and field types.

Author: AI Assistant
Date: 2025
"""

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, Union, Literal, Annotated
from datetime import datetime, date
from decimal import Decimal
import re


class UserSchema(BaseModel):
    """
    Pydantic schema for user data validation.
    
    This schema defines the expected structure and validation rules
    for user records in the e-commerce system.
    """
    
    user_id: Annotated[str, Field(pattern=r'^U\d{6}$', min_length=7, max_length=7)] = Field(
        ..., description="User ID in format U######"
    )
    first_name: Annotated[str, Field(min_length=1, max_length=50)] = Field(
        ..., description="User's first name"
    )
    last_name: Annotated[str, Field(min_length=1, max_length=50)] = Field(
        ..., description="User's last name"
    )
    email: EmailStr = Field(
        ..., description="Valid email address"
    )
    phone: Annotated[str, Field(pattern=r'^[\d\-\+\(\)\s]+$', min_length=10, max_length=20)] = Field(
        ..., description="Phone number with valid format"
    )
    address: Annotated[str, Field(min_length=1, max_length=200)] = Field(
        ..., description="Street address"
    )
    city: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="City name"
    )
    state: Annotated[str, Field(min_length=1, max_length=50)] = Field(
        ..., description="State or province"
    )
    country: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Country name"
    )
    postal_code: Annotated[str, Field(pattern=r'^[\w\s\-]+$', min_length=3, max_length=20)] = Field(
        ..., description="Postal or ZIP code"
    )
    date_of_birth: date = Field(
        ..., description="Date of birth"
    )
    gender: Literal['M', 'F', 'Other'] = Field(
        ..., description="Gender (M, F, or Other)"
    )
    registration_date: datetime = Field(
        ..., description="User registration timestamp"
    )
    is_active: bool = Field(
        ..., description="Whether user account is active"
    )
    total_orders: int = Field(
        ge=0, description="Total number of orders (non-negative)"
    )
    total_spent: Decimal = Field(
        ge=0, decimal_places=2, description="Total amount spent (non-negative)"
    )
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v):
        """Validate that date of birth is reasonable."""
        if v.year < 1900 or v.year > 2010:
            raise ValueError('Date of birth must be between 1900 and 2010')
        return v
    
    @field_validator('registration_date')
    @classmethod
    def validate_registration_date(cls, v):
        """Validate that registration date is not in the future."""
        if v > datetime.now():
            raise ValueError('Registration date cannot be in the future')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        """Validate phone number format."""
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', v)
        if len(digits_only) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v


class ProductSchema(BaseModel):
    """
    Pydantic schema for product data validation.
    
    This schema defines the expected structure and validation rules
    for product records in the e-commerce system.
    """
    
    product_id: Annotated[str, Field(pattern=r'^P\d{6}$', min_length=7, max_length=7)] = Field(
        ..., description="Product ID in format P######"
    )
    name: Annotated[str, Field(min_length=1, max_length=200)] = Field(
        ..., description="Product name"
    )
    description: Annotated[str, Field(min_length=1, max_length=1000)] = Field(
        ..., description="Product description"
    )
    category: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Product category"
    )
    brand: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Product brand"
    )
    price: Decimal = Field(
        gt=0, decimal_places=2, description="Product price (positive)"
    )
    cost: Decimal = Field(
        ge=0, decimal_places=2, description="Product cost (non-negative)"
    )
    stock_quantity: int = Field(
        ge=0, description="Stock quantity (non-negative)"
    )
    weight: Decimal = Field(
        gt=0, decimal_places=2, description="Product weight in kg (positive)"
    )
    dimensions: Annotated[str, Field(pattern=r'^\d+x\d+x\d+$')] = Field(
        ..., description="Product dimensions in format WxHxD"
    )
    is_active: bool = Field(
        ..., description="Whether product is active"
    )
    created_date: datetime = Field(
        ..., description="Product creation timestamp"
    )
    rating: Decimal = Field(
        ge=1.0, le=5.0, decimal_places=1, description="Product rating (1.0-5.0)"
    )
    review_count: int = Field(
        ge=0, description="Number of reviews (non-negative)"
    )
    
    @field_validator('price')
    @classmethod
    def validate_price_vs_cost(cls, v, info):
        """Validate that price is greater than cost."""
        if hasattr(info, 'data') and 'cost' in info.data and v <= info.data['cost']:
            raise ValueError('Price must be greater than cost')
        return v
    
    @field_validator('created_date')
    @classmethod
    def validate_created_date(cls, v):
        """Validate that created date is not in the future."""
        if v > datetime.now():
            raise ValueError('Created date cannot be in the future')
        return v
    
    @field_validator('dimensions')
    @classmethod
    def validate_dimensions_format(cls, v):
        """Validate dimensions format and values."""
        parts = v.split('x')
        if len(parts) != 3:
            raise ValueError('Dimensions must be in format WxHxD')
        
        for part in parts:
            try:
                dim = float(part)
                if dim <= 0:
                    raise ValueError('All dimensions must be positive')
            except ValueError:
                raise ValueError('All dimensions must be numeric')
        
        return v


class SellerSchema(BaseModel):
    """
    Pydantic schema for seller data validation.
    
    This schema defines the expected structure and validation rules
    for seller records in the e-commerce system.
    """
    
    seller_id: Annotated[str, Field(pattern=r'^S\d{6}$', min_length=7, max_length=7)] = Field(
        ..., description="Seller ID in format S######"
    )
    company_name: Annotated[str, Field(min_length=1, max_length=200)] = Field(
        ..., description="Company or business name"
    )
    contact_name: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Contact person name"
    )
    email: EmailStr = Field(
        ..., description="Valid email address"
    )
    phone: Annotated[str, Field(pattern=r'^[\d\-\+\(\)\s]+$', min_length=10, max_length=20)] = Field(
        ..., description="Phone number with valid format"
    )
    address: Annotated[str, Field(min_length=1, max_length=200)] = Field(
        ..., description="Business address"
    )
    city: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="City name"
    )
    state: Annotated[str, Field(min_length=1, max_length=50)] = Field(
        ..., description="State or province"
    )
    country: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Country name"
    )
    postal_code: Annotated[str, Field(pattern=r'^[\w\s\-]+$', min_length=3, max_length=20)] = Field(
        ..., description="Postal or ZIP code"
    )
    business_type: Literal['Individual', 'Corporation', 'LLC', 'Partnership'] = Field(
        ..., description="Type of business entity"
    )
    tax_id: Annotated[str, Field(pattern=r'^\d{2}-\d{7}$')] = Field(
        ..., description="Tax ID in format ##-#######"
    )
    registration_date: datetime = Field(
        ..., description="Seller registration timestamp"
    )
    is_verified: bool = Field(
        ..., description="Whether seller is verified"
    )
    rating: Decimal = Field(
        ge=1.0, le=5.0, decimal_places=1, description="Seller rating (1.0-5.0)"
    )
    total_sales: Decimal = Field(
        ge=0, decimal_places=2, description="Total sales amount (non-negative)"
    )
    commission_rate: Decimal = Field(
        ge=0.0, le=1.0, decimal_places=3, description="Commission rate (0.0-1.0)"
    )
    
    @field_validator('registration_date')
    @classmethod
    def validate_registration_date(cls, v):
        """Validate that registration date is not in the future."""
        if v > datetime.now():
            raise ValueError('Registration date cannot be in the future')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        """Validate phone number format."""
        digits_only = re.sub(r'\D', '', v)
        if len(digits_only) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v


class SaleSchema(BaseModel):
    """
    Pydantic schema for sales data validation.
    
    This schema defines the expected structure and validation rules
    for sales records in the e-commerce system.
    """
    
    sale_id: Annotated[str, Field(pattern=r'^SA\d{8}$', min_length=10, max_length=10)] = Field(
        ..., description="Sale ID in format SA########"
    )
    user_id: Annotated[str, Field(pattern=r'^U\d{6}$', min_length=7, max_length=7)] = Field(
        ..., description="User ID in format U######"
    )
    product_id: Annotated[str, Field(pattern=r'^P\d{6}$', min_length=7, max_length=7)] = Field(
        ..., description="Product ID in format P######"
    )
    seller_id: Annotated[str, Field(pattern=r'^S\d{6}$', min_length=7, max_length=7)] = Field(
        ..., description="Seller ID in format S######"
    )
    quantity: int = Field(
        gt=0, description="Quantity purchased (positive)"
    )
    unit_price: Decimal = Field(
        gt=0, decimal_places=2, description="Unit price (positive)"
    )
    subtotal: Decimal = Field(
        gt=0, decimal_places=2, description="Subtotal amount (positive)"
    )
    discount_amount: Decimal = Field(
        ge=0, decimal_places=2, description="Discount amount (non-negative)"
    )
    discount_rate: Decimal = Field(
        ge=0.0, le=1.0, decimal_places=3, description="Discount rate (0.0-1.0)"
    )
    tax_amount: Decimal = Field(
        ge=0, decimal_places=2, description="Tax amount (non-negative)"
    )
    tax_rate: Decimal = Field(
        ge=0.0, le=1.0, decimal_places=3, description="Tax rate (0.0-1.0)"
    )
    total_amount: Decimal = Field(
        gt=0, decimal_places=2, description="Total amount (positive)"
    )
    sale_date: datetime = Field(
        ..., description="Sale timestamp"
    )
    status: Literal['completed', 'pending', 'cancelled', 'refunded'] = Field(
        ..., description="Sale status"
    )
    shipping_address: Annotated[str, Field(min_length=1, max_length=200)] = Field(
        ..., description="Shipping address"
    )
    shipping_city: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Shipping city"
    )
    shipping_state: Annotated[str, Field(min_length=1, max_length=50)] = Field(
        ..., description="Shipping state"
    )
    shipping_country: Annotated[str, Field(min_length=1, max_length=100)] = Field(
        ..., description="Shipping country"
    )
    shipping_postal_code: Annotated[str, Field(pattern=r'^[\w\s\-]+$', min_length=3, max_length=20)] = Field(
        ..., description="Shipping postal code"
    )
    
    @field_validator('subtotal')
    @classmethod
    def validate_subtotal_calculation(cls, v, info):
        """Validate that subtotal equals quantity * unit_price."""
        if hasattr(info, 'data') and 'quantity' in info.data and 'unit_price' in info.data:
            expected = info.data['quantity'] * info.data['unit_price']
            if abs(v - expected) > Decimal('0.01'):
                raise ValueError('Subtotal must equal quantity * unit_price')
        return v
    
    @field_validator('total_amount')
    @classmethod
    def validate_total_calculation(cls, v, info):
        """Validate that total_amount is calculated correctly."""
        if hasattr(info, 'data') and all(key in info.data for key in ['subtotal', 'discount_amount', 'tax_amount']):
            expected = info.data['subtotal'] - info.data['discount_amount'] + info.data['tax_amount']
            if abs(v - expected) > Decimal('0.01'):
                raise ValueError('Total amount calculation is incorrect')
        return v
    
    @field_validator('sale_date')
    @classmethod
    def validate_sale_date(cls, v):
        """Validate that sale date is not in the future."""
        if v > datetime.now():
            raise ValueError('Sale date cannot be in the future')
        return v


class PaymentSchema(BaseModel):
    """
    Pydantic schema for payment data validation.
    
    This schema defines the expected structure and validation rules
    for payment records in the e-commerce system.
    """
    
    payment_id: Annotated[str, Field(pattern=r'^PAY[A-Z0-9_]+$', min_length=10)] = Field(
        ..., description="Payment ID with valid format"
    )
    sale_id: Annotated[str, Field(pattern=r'^SA\d{8}$', min_length=10, max_length=10)] = Field(
        ..., description="Sale ID in format SA########"
    )
    payment_method: Literal['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cryptocurrency'] = Field(
        ..., description="Payment method used"
    )
    amount: Decimal = Field(
        gt=0, decimal_places=2, description="Payment amount (positive)"
    )
    payment_date: datetime = Field(
        ..., description="Payment timestamp"
    )
    status: Literal['completed', 'pending', 'failed'] = Field(
        ..., description="Payment status"
    )
    transaction_id: Annotated[str, Field(pattern=r'^TXN[A-Z0-9]+$', min_length=10)] = Field(
        ..., description="Transaction ID with valid format"
    )
    gateway: Literal['stripe', 'paypal', 'square', 'adyen'] = Field(
        ..., description="Payment gateway used"
    )
    currency: Annotated[str, Field(pattern=r'^[A-Z]{3}$', min_length=3, max_length=3)] = Field(
        ..., description="Currency code (3 letters)"
    )
    
    @field_validator('payment_date')
    @classmethod
    def validate_payment_date(cls, v):
        """Validate that payment date is not in the future."""
        if v > datetime.now():
            raise ValueError('Payment date cannot be in the future')
        return v
    
    @field_validator('currency')
    @classmethod
    def validate_currency_code(cls, v):
        """Validate that currency code is valid."""
        valid_currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'CNY']
        if v not in valid_currencies:
            raise ValueError(f'Currency must be one of: {", ".join(valid_currencies)}')
        return v


class SchemaValidator:
    """
    Main class for validating e-commerce data schemas.
    
    This class provides methods to validate data against the defined
    Pydantic schemas for users, products, sellers, sales, and payments.
    """
    
    def __init__(self):
        """Initialize the schema validator."""
        self.schemas = {
            'users': UserSchema,
            'products': ProductSchema,
            'sellers': SellerSchema,
            'sales': SaleSchema,
            'payments': PaymentSchema
        }
    
    def validate_record(self, data_type: str, record: dict) -> dict:
        """
        Validate a single record against its schema.
        
        Args:
            data_type (str): Type of data ('users', 'products', 'sellers', 'sales', 'payments')
            record (dict): Record data to validate
            
        Returns:
            dict: Validation result with success status and details
            
        Raises:
            ValueError: If data_type is not supported
        """
        if data_type not in self.schemas:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        try:
            schema_class = self.schemas[data_type]
            validated_record = schema_class(**record)
            
            return {
                'success': True,
                'validated_data': validated_record.dict(),
                'errors': []
            }
            
        except Exception as e:
            return {
                'success': False,
                'validated_data': None,
                'errors': [str(e)]
            }
    
    def validate_batch(self, data_type: str, records: list) -> dict:
        """
        Validate a batch of records against their schema.
        
        Args:
            data_type (str): Type of data ('users', 'products', 'sellers', 'sales', 'payments')
            records (list): List of records to validate
            
        Returns:
            dict: Batch validation result with success counts and error details
        """
        if data_type not in self.schemas:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        results = {
            'total_records': len(records),
            'valid_records': 0,
            'invalid_records': 0,
            'valid_records_data': [],
            'errors': []
        }
        
        for i, record in enumerate(records):
            validation_result = self.validate_record(data_type, record)
            
            if validation_result['success']:
                results['valid_records'] += 1
                results['valid_records_data'].append(validation_result['validated_data'])
            else:
                results['invalid_records'] += 1
                results['errors'].append({
                    'record_index': i,
                    'record_id': record.get('user_id', record.get('product_id', record.get('sale_id', record.get('payment_id', f'Record_{i}')))),
                    'errors': validation_result['errors']
                })
        
        return results
    
    def get_schema_fields(self, data_type: str) -> list:
        """
        Get the field names for a specific data type schema.
        
        Args:
            data_type (str): Type of data ('users', 'products', 'sellers', 'sales', 'payments')
            
        Returns:
            list: List of field names in the schema
            
        Raises:
            ValueError: If data_type is not supported
        """
        if data_type not in self.schemas:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        schema_class = self.schemas[data_type]
        return list(schema_class.model_fields.keys())
    
    def get_schema_info(self, data_type: str) -> dict:
        """
        Get detailed information about a specific data type schema.
        
        Args:
            data_type (str): Type of data ('users', 'products', 'sellers', 'sales', 'payments')
            
        Returns:
            dict: Schema information including fields and their types
            
        Raises:
            ValueError: If data_type is not supported
        """
        if data_type not in self.schemas:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        schema_class = self.schemas[data_type]
        fields_info = {}
        
        for field_name, field_info in schema_class.model_fields.items():
            fields_info[field_name] = {
                'type': str(field_info.annotation),
                'required': field_info.is_required(),
                'description': field_info.description or '',
                'constraints': {}
            }
            
            # Add constraints if they exist
            if hasattr(field_info, 'constraints'):
                for constraint_name, constraint_value in field_info.constraints.items():
                    fields_info[field_name]['constraints'][constraint_name] = constraint_value
        
        return {
            'data_type': data_type,
            'fields': fields_info,
            'total_fields': len(fields_info)
        }


def main():
    """
    Main function to demonstrate schema validation usage.
    """
    validator = SchemaValidator()
    
    # Example usage
    print("Schema Validator Demo")
    print("=" * 50)
    
    # Get schema information
    for data_type in ['users', 'products', 'sellers', 'sales', 'payments']:
        schema_info = validator.get_schema_info(data_type)
        print(f"\n{data_type.upper()} Schema:")
        print(f"Total fields: {schema_info['total_fields']}")
        print(f"Fields: {', '.join(schema_info['fields'].keys())}")


if __name__ == "__main__":
    main()
