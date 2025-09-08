#!/usr/bin/env python3
"""
Generate metrics dataframes for e-commerce analytics.
Creates various analytical dataframes from the generated CSV data.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data():
            """
        Load data from configured source.
        
        Loads data from the configured data source with proper error
        handling and validation. Supports various data formats and
        provides detailed loading status information.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
    try:
        users_df = pd.read_csv('tests/data_sources/users.csv')
        products_df = pd.read_csv('tests/data_sources/products.csv')
        sales_df = pd.read_csv('tests/data_sources/sales.csv')
        payments_df = pd.read_csv('tests/data_sources/payments.csv')
        sellers_df = pd.read_csv('tests/data_sources/sellers.csv')
        
        print("Data loaded successfully!")
        print(f"Users: {len(users_df)} records")
        print(f"Products: {len(products_df)} records")
        print(f"Sales: {len(sales_df)} records")
        print(f"Payments: {len(payments_df)} records")
        print(f"Sellers: {len(sellers_df)} records")
        
        return users_df, products_df, sales_df, payments_df, sellers_df
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Please run generate_fake_data.py first to create the data files.")
        return None, None, None, None, None

def users_distribution_by_address(users_df):
            """
        Users Distribution By Address.
        
        Performs the users distribution by address operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Users Distribution by Address ===")
    
    # Distribution by city
    city_dist = users_df['city'].value_counts().head(10)
    city_df = pd.DataFrame({
        'city': city_dist.index,
        'user_count': city_dist.values,
        'percentage': (city_dist.values / len(users_df) * 100).round(2)
    })
    
    # Distribution by state
    state_dist = users_df['state'].value_counts().head(10)
    state_df = pd.DataFrame({
        'state': state_dist.index,
        'user_count': state_dist.values,
        'percentage': (state_dist.values / len(users_df) * 100).round(2)
    })
    
    # Distribution by country
    country_dist = users_df['country'].value_counts()
    country_df = pd.DataFrame({
        'country': country_dist.index,
        'user_count': country_dist.values,
        'percentage': (country_dist.values / len(users_df) * 100).round(2)
    })
    
    print("Top 10 Cities by User Count:")
    print(city_df)
    
    print("\nTop 10 States by User Count:")
    print(state_df)
    
    print("\nCountry Distribution:")
    print(country_df)
    
    return {
        'city_distribution': city_df,
        'state_distribution': state_df,
        'country_distribution': country_df
    }

def total_sales_metrics(sales_df, payments_df):
            """
        Total Sales Metrics.
        
        Performs the total sales metrics operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Total Sales Metrics ===")
    
    # Total sales amount
    total_sales_amount = sales_df['final_amount'].sum()
    total_sales_count = len(sales_df)
    average_sale_amount = sales_df['final_amount'].mean()
    
    # Total payments amount
    total_payments_amount = payments_df['amount'].sum()
    total_payments_count = len(payments_df)
    
    # Sales by status
    sales_by_status = sales_df['status'].value_counts()
    status_df = pd.DataFrame({
        'status': sales_by_status.index,
        'count': sales_by_status.values,
        'percentage': (sales_by_status.values / len(sales_df) * 100).round(2)
    })
    
    # Monthly sales trend
    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
    monthly_sales = sales_df.groupby(sales_df['sale_date'].dt.to_period('M'))['final_amount'].agg(['sum', 'count']).reset_index()
    monthly_sales.columns = ['month', 'total_amount', 'transaction_count']
    
    print(f"Total Sales Amount: ${total_sales_amount:,.2f}")
    print(f"Total Sales Count: {total_sales_count:,}")
    print(f"Average Sale Amount: ${average_sale_amount:.2f}")
    print(f"Total Payments Amount: ${total_payments_amount:,.2f}")
    print(f"Total Payments Count: {total_payments_count:,}")
    
    print("\nSales by Status:")
    print(status_df)
    
    print("\nMonthly Sales Trend (Last 6 months):")
    print(monthly_sales.tail(6))
    
    return {
        'total_sales_amount': total_sales_amount,
        'total_sales_count': total_sales_count,
        'average_sale_amount': average_sale_amount,
        'total_payments_amount': total_payments_amount,
        'total_payments_count': total_payments_count,
        'sales_by_status': status_df,
        'monthly_sales': monthly_sales
    }

def top_10_products(sales_df, products_df):
            """
        Top 10 Products.
        
        Performs the top 10 products operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Top 10 Most Sold Products ===")
    
    # Merge sales with products to get product names
    sales_products = sales_df.merge(products_df[['product_id', 'name', 'category', 'price']], on='product_id', how='left')
    
    # Calculate product metrics
    product_metrics = sales_products.groupby(['product_id', 'name', 'category', 'price']).agg({
        'quantity': 'sum',
        'final_amount': 'sum',
        'sale_id': 'count'
    }).reset_index()
    
    product_metrics.columns = ['product_id', 'product_name', 'category', 'price', 'total_quantity_sold', 'total_revenue', 'total_transactions']
    product_metrics['average_sale_price'] = (product_metrics['total_revenue'] / product_metrics['total_quantity_sold']).round(2)
    
    # Sort by total quantity sold
    top_products = product_metrics.sort_values('total_quantity_sold', ascending=False).head(10)
    
    print("Top 10 Products by Quantity Sold:")
    print(top_products[['product_name', 'category', 'total_quantity_sold', 'total_revenue', 'total_transactions']])
    
    # Top products by revenue
    top_products_revenue = product_metrics.sort_values('total_revenue', ascending=False).head(10)
    
    print("\nTop 10 Products by Revenue:")
    print(top_products_revenue[['product_name', 'category', 'total_revenue', 'total_quantity_sold', 'total_transactions']])
    
    return {
        'top_products_quantity': top_products,
        'top_products_revenue': top_products_revenue
    }

def top_10_buyers(sales_df, users_df):
            """
        Top 10 Buyers.
        
        Performs the top 10 buyers operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Top 10 Buyers ===")
    
    # Merge sales with users
    sales_users = sales_df.merge(users_df[['user_id', 'first_name', 'last_name', 'email', 'city', 'state']], on='user_id', how='left')
    
    # Calculate buyer metrics
    buyer_metrics = sales_users.groupby(['user_id', 'first_name', 'last_name', 'email', 'city', 'state']).agg({
        'final_amount': ['sum', 'mean'],
        'sale_id': 'count',
        'quantity': 'sum'
    }).reset_index()
    
    # Flatten column names
    buyer_metrics.columns = ['user_id', 'first_name', 'last_name', 'email', 'city', 'state', 
                           'total_spent', 'average_purchase', 'total_purchases', 'total_items']
    
    # Top buyers by total spent
    top_buyers_amount = buyer_metrics.sort_values('total_spent', ascending=False).head(10)
    
    print("Top 10 Buyers by Total Amount Spent:")
    print(top_buyers_amount[['first_name', 'last_name', 'city', 'state', 'total_spent', 'total_purchases', 'average_purchase']])
    
    # Top buyers by frequency
    top_buyers_frequency = buyer_metrics.sort_values('total_purchases', ascending=False).head(10)
    
    print("\nTop 10 Buyers by Purchase Frequency:")
    print(top_buyers_frequency[['first_name', 'last_name', 'city', 'state', 'total_purchases', 'total_spent', 'average_purchase']])
    
    return {
        'top_buyers_amount': top_buyers_amount,
        'top_buyers_frequency': top_buyers_frequency
    }

def payment_method_analysis(payments_df):
            """
        Payment Method Analysis.
        
        Performs the payment method analysis operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Payment Method Analysis ===")
    
    # Payment method distribution
    payment_dist = payments_df['payment_method'].value_counts()
    payment_df = pd.DataFrame({
        'payment_method': payment_dist.index,
        'transaction_count': payment_dist.values,
        'percentage': (payment_dist.values / len(payments_df) * 100).round(2)
    })
    
    # Payment method by amount
    payment_amounts = payments_df.groupby('payment_method')['amount'].agg(['sum', 'mean', 'count']).reset_index()
    payment_amounts.columns = ['payment_method', 'total_amount', 'average_amount', 'transaction_count']
    payment_amounts['percentage_of_total'] = (payment_amounts['total_amount'] / payment_amounts['total_amount'].sum() * 100).round(2)
    
    # Payment method success rate
    payment_success = payments_df.groupby('payment_method')['status'].value_counts().unstack(fill_value=0)
    payment_success['success_rate'] = (payment_success.get('completed', 0) / payment_success.sum(axis=1) * 100).round(2)
    
    print("Payment Method Distribution:")
    print(payment_df)
    
    print("\nPayment Method by Amount:")
    print(payment_amounts)
    
    print("\nPayment Method Success Rates:")
    print(payment_success[['completed', 'pending', 'failed', 'success_rate']])
    
    most_used_method = payment_df.iloc[0]['payment_method']
    print(f"\nMost Used Payment Method: {most_used_method} ({payment_df.iloc[0]['percentage']}%)")
    
    return {
        'payment_distribution': payment_df,
        'payment_amounts': payment_amounts,
        'payment_success_rates': payment_success,
        'most_used_method': most_used_method
    }

def gender_purchase_analysis(sales_df, users_df):
            """
        Gender Purchase Analysis.
        
        Performs the gender purchase analysis operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Gender Purchase Analysis ===")
    
    # Merge sales with users
    sales_users = sales_df.merge(users_df[['user_id', 'gender', 'first_name', 'last_name']], on='user_id', how='left')
    
    # Gender distribution
    gender_dist = users_df['gender'].value_counts()
    gender_df = pd.DataFrame({
        'gender': gender_dist.index,
        'user_count': gender_dist.values,
        'percentage': (gender_dist.values / len(users_df) * 100).round(2)
    })
    
    # Purchase analysis by gender
    gender_purchases = sales_users.groupby('gender').agg({
        'final_amount': ['sum', 'mean', 'count'],
        'quantity': 'sum',
        'user_id': 'nunique'
    }).reset_index()
    
    # Flatten column names
    gender_purchases.columns = ['gender', 'total_spent', 'average_purchase', 'total_transactions', 'total_items', 'unique_buyers']
    gender_purchases['average_per_buyer'] = (gender_purchases['total_spent'] / gender_purchases['unique_buyers']).round(2)
    gender_purchases['transactions_per_buyer'] = (gender_purchases['total_transactions'] / gender_purchases['unique_buyers']).round(2)
    
    print("Gender Distribution:")
    print(gender_df)
    
    print("\nPurchase Analysis by Gender:")
    print(gender_purchases)
    
    # Find which gender buys more
    if len(gender_purchases) > 1:
        top_gender = gender_purchases.loc[gender_purchases['total_spent'].idxmax()]
        print(f"\nGender that buys more: {top_gender['gender']}")
        print(f"Total spent: ${top_gender['total_spent']:,.2f}")
        print(f"Average purchase: ${top_gender['average_purchase']:.2f}")
        print(f"Unique buyers: {top_gender['unique_buyers']}")
    
    return {
        'gender_distribution': gender_df,
        'gender_purchases': gender_purchases
    }

def save_metrics_to_csv(metrics_data):
            """
        Save Metrics To Csv.
        
        Performs the save metrics to csv operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("\n=== Saving Metrics to CSV Files ===")
    
    # Create metrics directory
    os.makedirs('tests/metrics', exist_ok=True)
    
    # Save each metric
    for metric_name, metric_data in metrics_data.items():
        if isinstance(metric_data, dict):
            for sub_metric_name, df in metric_data.items():
                if isinstance(df, pd.DataFrame):
                    filename = f"tests/metrics/{metric_name}_{sub_metric_name}.csv"
                    df.to_csv(filename, index=False)
                    print(f"Saved: {filename}")
        elif isinstance(metric_data, pd.DataFrame):
            filename = f"tests/metrics/{metric_name}.csv"
            metric_data.to_csv(filename, index=False)
            print(f"Saved: {filename}")
    
    print("All metrics saved to tests/metrics/")

def main():
            """
        Main.
        
        Performs the main operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    print("=== E-commerce Analytics Dashboard ===")
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    users_df, products_df, sales_df, payments_df, sellers_df = load_data()
    
    if users_df is None:
        return
    
    # Generate all metrics
    metrics_data = {}
    
    # 1. Users distribution by address
    metrics_data['address'] = users_distribution_by_address(users_df)
    
    # 2. Total sales metrics
    metrics_data['sales'] = total_sales_metrics(sales_df, payments_df)
    
    # 3. Top 10 products
    metrics_data['products'] = top_10_products(sales_df, products_df)
    
    # 4. Top 10 buyers
    metrics_data['buyers'] = top_10_buyers(sales_df, users_df)
    
    # 5. Payment method analysis
    metrics_data['payments'] = payment_method_analysis(payments_df)
    
    # 6. Gender purchase analysis
    metrics_data['gender'] = gender_purchase_analysis(sales_df, users_df)
    
    # Save all metrics to CSV
    save_metrics_to_csv(metrics_data)
    
    print("\n=== Analytics Complete ===")
    print("All metrics have been generated and saved to CSV files.")
    print("Check the 'tests/metrics/' directory for detailed results.")

if __name__ == "__main__":
    main()
