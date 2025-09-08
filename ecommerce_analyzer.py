#!/usr/bin/env python3
"""
EcommerceAnalyzer class for generating static visualizations from metrics data.
Creates various charts and graphs using matplotlib and seaborn.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class EcommerceAnalyzer:
    """
    Comprehensive e-commerce analytics visualization generator.
    
    This class provides functionality to generate static visualizations from
    e-commerce metrics data, including sales analysis, customer demographics,
    product performance, and payment analytics. It supports both valid and
    invalid data comparison for data quality assessment.
    
    Attributes:
        metrics_path (str): Path to metrics CSV files
        data_path (str): Path to raw data CSV files  
        output_path (str): Path to save generated images
        data (dict): Loaded metrics data
        raw_data (dict): Loaded raw data (valid and bad)
        validation_results (dict): Data quality validation results
    """
    
    def __init__(self, metrics_path='tests/metrics/', data_path='tests/data_sources/', output_path='images/'):
        """
        Initialize the EcommerceAnalyzer with configuration paths.
        
        Sets up the analyzer with paths for metrics data, raw data, and output
        directory. Creates the output directory if it doesn't exist and configures
        matplotlib and seaborn styling for consistent visualizations.
        
        Args:
            metrics_path (str): Path to metrics CSV files directory
            data_path (str): Path to raw data CSV files directory  
            output_path (str): Path to save generated visualization images
            
        Note:
            The output directory will be created automatically if it doesn't exist.
        """
        self.metrics_path = metrics_path
        self.data_path = data_path
        self.output_path = output_path
        self.data = {}
        self.raw_data = {}
        self.validation_results = {}
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def load_metrics_data(self):
        """
        Load all metrics data from CSV files.
        
        Loads pre-calculated metrics data from CSV files including sales metrics,
        customer demographics, product performance, and payment analytics. This
        data is used for generating comprehensive visualizations.
        
        Returns:
            bool: True if all data loaded successfully, False otherwise
            
        Note:
            The method will print success/error messages to console.
        """
        print("Loading metrics data...")
        
        try:
            # Load all metrics files
            self.data = {
                'city_dist': pd.read_csv(f'{self.metrics_path}address_city_distribution.csv'),
                'state_dist': pd.read_csv(f'{self.metrics_path}address_state_distribution.csv'),
                'country_dist': pd.read_csv(f'{self.metrics_path}address_country_distribution.csv'),
                'sales_status': pd.read_csv(f'{self.metrics_path}sales_sales_by_status.csv'),
                'monthly_sales': pd.read_csv(f'{self.metrics_path}sales_monthly_sales.csv'),
                'top_products_qty': pd.read_csv(f'{self.metrics_path}products_top_products_quantity.csv'),
                'top_products_rev': pd.read_csv(f'{self.metrics_path}products_top_products_revenue.csv'),
                'top_buyers_amount': pd.read_csv(f'{self.metrics_path}buyers_top_buyers_amount.csv'),
                'top_buyers_freq': pd.read_csv(f'{self.metrics_path}buyers_top_buyers_frequency.csv'),
                'payment_dist': pd.read_csv(f'{self.metrics_path}payments_payment_distribution.csv'),
                'payment_amounts': pd.read_csv(f'{self.metrics_path}payments_payment_amounts.csv'),
                'gender_dist': pd.read_csv(f'{self.metrics_path}gender_gender_distribution.csv'),
                'gender_purchases': pd.read_csv(f'{self.metrics_path}gender_gender_purchases.csv')
            }
            print("✓ All metrics data loaded successfully!")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def load_raw_data(self):
        """
        Load raw data files including both valid and bad data.
        
        Loads the original e-commerce data files including users, products, sales,
        payments, and sellers. Also loads corresponding "bad" data files that
        contain intentional data quality issues for comparison and validation
        purposes.
        
        Returns:
            bool: True if all data loaded successfully, False otherwise
            
        Note:
            Bad data files are used for data quality assessment and comparison.
        """
        print("Loading raw data files...")
        
        try:
            # Load valid data
            self.raw_data['valid'] = {
                'users': pd.read_csv(f'{self.data_path}users.csv'),
                'products': pd.read_csv(f'{self.data_path}products.csv'),
                'sales': pd.read_csv(f'{self.data_path}sales.csv'),
                'payments': pd.read_csv(f'{self.data_path}payments.csv'),
                'sellers': pd.read_csv(f'{self.data_path}sellers.csv')
            }
            
            # Load bad data
            self.raw_data['bad'] = {
                'users': pd.read_csv(f'{self.data_path}bad_users.csv'),
                'products': pd.read_csv(f'{self.data_path}bad_products.csv'),
                'sales': pd.read_csv(f'{self.data_path}bad_sales.csv'),
                'payments': pd.read_csv(f'{self.data_path}bad_payments.csv')
            }
            
            print("✓ Raw data loaded successfully!")
            return True
        except Exception as e:
            print(f"✗ Error loading raw data: {e}")
            return False
    
    def validate_data_quality(self):
                """
        Validate data quality and compliance.
        
        Performs comprehensive data validation including schema validation,
        business rule enforcement, and data quality assessment. Provides
        detailed validation results and error reporting.
        
        Returns:
            Validation results with quality scores and error details
        """
        print("Validating data quality...")
        
        validation_results = {}
        
        for data_type in ['valid', 'bad']:
            validation_results[data_type] = {}
            
            for table_name, df in self.raw_data[data_type].items():
                issues = []
                
                # Check for missing values
                missing_values = df.isnull().sum()
                if missing_values.any():
                    issues.append(f"Missing values: {missing_values[missing_values > 0].to_dict()}")
                
                # Check for empty strings
                empty_strings = (df == '').sum()
                if empty_strings.any():
                    issues.append(f"Empty strings: {empty_strings[empty_strings > 0].to_dict()}")
                
                # Check for negative values in numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if col in ['price', 'cost', 'amount', 'final_amount', 'total_amount', 'age']:
                        negative_count = (df[col] < 0).sum()
                        if negative_count > 0:
                            issues.append(f"Negative values in {col}: {negative_count}")
                
                # Check for invalid email formats
                if 'email' in df.columns:
                    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    invalid_emails = ~df['email'].astype(str).str.match(email_pattern, na=False)
                    if invalid_emails.any():
                        issues.append(f"Invalid email formats: {invalid_emails.sum()}")
                
                # Check for invalid phone numbers (basic check)
                if 'phone' in df.columns:
                    phone_pattern = r'^[\d\s\-\+\(\)]+$'
                    invalid_phones = ~df['phone'].astype(str).str.match(phone_pattern, na=False)
                    if invalid_phones.any():
                        issues.append(f"Invalid phone formats: {invalid_phones.sum()}")
                
                # Check for XSS attempts
                text_cols = df.select_dtypes(include=['object']).columns
                xss_pattern = r'<script.*?>.*?</script>'
                for col in text_cols:
                    if df[col].dtype == 'object':
                        xss_attempts = df[col].astype(str).str.contains(xss_pattern, case=False, na=False)
                        if xss_attempts.any():
                            issues.append(f"XSS attempts in {col}: {xss_attempts.sum()}")
                
                validation_results[data_type][table_name] = {
                    'total_records': len(df),
                    'total_columns': len(df.columns),
                    'issues': issues,
                    'issue_count': len(issues)
                }
        
        self.validation_results = validation_results
        print("✓ Data validation completed!")
        return validation_results
    
    def create_data_quality_dashboard(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Data Quality Validation Dashboard', fontsize=16, fontweight='bold')
        
        # Data quality comparison
        valid_issues = sum([table['issue_count'] for table in self.validation_results['valid'].values()])
        bad_issues = sum([table['issue_count'] for table in self.validation_results['bad'].values()])
        
        ax1.bar(['Valid Data', 'Bad Data'], [valid_issues, bad_issues], color=['green', 'red'])
        ax1.set_title('Total Data Quality Issues')
        ax1.set_ylabel('Number of Issues')
        for i, v in enumerate([valid_issues, bad_issues]):
            ax1.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
        
        # Record counts comparison
        valid_records = sum([table['total_records'] for table in self.validation_results['valid'].values()])
        bad_records = sum([table['total_records'] for table in self.validation_results['bad'].values()])
        
        ax2.bar(['Valid Data', 'Bad Data'], [valid_records, bad_records], color=['blue', 'orange'])
        ax2.set_title('Total Records Count')
        ax2.set_ylabel('Number of Records')
        for i, v in enumerate([valid_records, bad_records]):
            ax2.text(i, v + 50, str(v), ha='center', va='bottom', fontweight='bold')
        
        # Issues by table type (valid data)
        valid_tables = list(self.validation_results['valid'].keys())
        valid_issue_counts = [self.validation_results['valid'][table]['issue_count'] for table in valid_tables]
        
        ax3.bar(valid_tables, valid_issue_counts, color='lightgreen')
        ax3.set_title('Issues in Valid Data by Table')
        ax3.set_ylabel('Number of Issues')
        ax3.tick_params(axis='x', rotation=45)
        
        # Issues by table type (bad data)
        bad_tables = list(self.validation_results['bad'].keys())
        bad_issue_counts = [self.validation_results['bad'][table]['issue_count'] for table in bad_tables]
        
        ax4.bar(bad_tables, bad_issue_counts, color='lightcoral')
        ax4.set_title('Issues in Bad Data by Table')
        ax4.set_ylabel('Number of Issues')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}data_quality_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Data quality dashboard created")
    
    def create_validation_comparison_chart(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Prepare data for comparison
        tables = ['users', 'products', 'sales', 'payments']
        valid_issues = [self.validation_results['valid'][table]['issue_count'] for table in tables]
        bad_issues = [self.validation_results['bad'][table]['issue_count'] for table in tables]
        
        x = np.arange(len(tables))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, valid_issues, width, label='Valid Data', color='lightgreen', alpha=0.8)
        bars2 = ax.bar(x + width/2, bad_issues, width, label='Bad Data', color='lightcoral', alpha=0.8)
        
        ax.set_xlabel('Data Tables')
        ax.set_ylabel('Number of Issues')
        ax.set_title('Data Quality Issues Comparison: Valid vs Bad Data')
        ax.set_xticks(x)
        ax.set_xticklabels(tables)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}validation_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Validation comparison chart created")
    
    def create_sales_overview_chart(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('E-commerce Sales Overview', fontsize=16, fontweight='bold')
        
        # Sales by status (pie chart)
        status_data = self.data['sales_status']
        ax1.pie(status_data['count'], labels=status_data['status'], autopct='%1.1f%%', startangle=90)
        ax1.set_title('Sales Distribution by Status')
        
        # Monthly sales trend
        monthly_data = self.data['monthly_sales'].tail(6)
        ax2.plot(range(len(monthly_data)), monthly_data['total_amount'], marker='o', linewidth=2)
        ax2.set_title('Monthly Sales Trend (Last 6 Months)')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Total Amount ($)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Top 5 products by quantity
        top_products = self.data['top_products_qty'].head(5)
        ax3.barh(range(len(top_products)), top_products['total_quantity_sold'])
        ax3.set_yticks(range(len(top_products)))
        ax3.set_yticklabels([name[:30] + '...' if len(name) > 30 else name for name in top_products['product_name']])
        ax3.set_title('Top 5 Products by Quantity Sold')
        ax3.set_xlabel('Quantity Sold')
        
        # Gender distribution
        gender_data = self.data['gender_dist']
        ax4.bar(gender_data['gender'], gender_data['user_count'])
        ax4.set_title('User Distribution by Gender')
        ax4.set_ylabel('Number of Users')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}sales_overview.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Sales overview chart created")
    
    def create_geographic_analysis(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Geographic Distribution Analysis', fontsize=16, fontweight='bold')
        
        # Top 10 states
        state_data = self.data['state_dist'].head(10)
        ax1.barh(range(len(state_data)), state_data['user_count'])
        ax1.set_yticks(range(len(state_data)))
        ax1.set_yticklabels(state_data['state'])
        ax1.set_title('Top 10 States by User Count')
        ax1.set_xlabel('Number of Users')
        
        # Top 10 countries
        country_data = self.data['country_dist'].head(10)
        ax2.barh(range(len(country_data)), country_data['user_count'])
        ax2.set_yticks(range(len(country_data)))
        ax2.set_yticklabels(country_data['country'])
        ax2.set_title('Top 10 Countries by User Count')
        ax2.set_xlabel('Number of Users')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}geographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Geographic analysis chart created")
    
    def create_payment_analysis(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Payment Method Analysis', fontsize=16, fontweight='bold')
        
        # Payment method distribution
        payment_data = self.data['payment_dist']
        ax1.pie(payment_data['transaction_count'], labels=payment_data['payment_method'], 
                autopct='%1.1f%%', startangle=90)
        ax1.set_title('Payment Method Distribution')
        
        # Payment amounts by method
        amount_data = self.data['payment_amounts']
        ax2.bar(amount_data['payment_method'], amount_data['total_amount'])
        ax2.set_title('Total Amount by Payment Method')
        ax2.set_ylabel('Total Amount ($)')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}payment_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Payment analysis chart created")
    
    def create_customer_analysis(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Customer Behavior Analysis', fontsize=16, fontweight='bold')
        
        # Top buyers by amount
        buyers_amount = self.data['top_buyers_amount'].head(8)
        ax1.barh(range(len(buyers_amount)), buyers_amount['total_spent'])
        ax1.set_yticks(range(len(buyers_amount)))
        ax1.set_yticklabels([f"{row['first_name']} {row['last_name']}" for _, row in buyers_amount.iterrows()])
        ax1.set_title('Top 8 Buyers by Total Amount')
        ax1.set_xlabel('Total Spent ($)')
        
        # Gender purchase comparison
        gender_data = self.data['gender_purchases']
        ax2.bar(gender_data['gender'], gender_data['total_spent'])
        ax2.set_title('Total Spending by Gender')
        ax2.set_ylabel('Total Spent ($)')
        
        # Average purchase by gender
        ax3.bar(gender_data['gender'], gender_data['average_purchase'])
        ax3.set_title('Average Purchase Amount by Gender')
        ax3.set_ylabel('Average Purchase ($)')
        
        # Transactions per buyer
        ax4.bar(gender_data['gender'], gender_data['transactions_per_buyer'])
        ax4.set_title('Average Transactions per Buyer by Gender')
        ax4.set_ylabel('Transactions per Buyer')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}customer_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Customer analysis chart created")
    
    def create_product_analysis(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Product Performance Analysis', fontsize=16, fontweight='bold')
        
        # Top products by revenue
        top_rev = self.data['top_products_rev'].head(8)
        ax1.barh(range(len(top_rev)), top_rev['total_revenue'])
        ax1.set_yticks(range(len(top_rev)))
        ax1.set_yticklabels([name[:25] + '...' if len(name) > 25 else name for name in top_rev['product_name']])
        ax1.set_title('Top 8 Products by Revenue')
        ax1.set_xlabel('Total Revenue ($)')
        
        # Product categories distribution
        category_data = self.data['top_products_qty']['category'].value_counts()
        ax2.pie(category_data.values, labels=category_data.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Product Distribution by Category')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_path}product_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Product analysis chart created")
    
    def create_comprehensive_dashboard(self):
                """
        Create new data or resources.
        
        Creates new data structures, files, or resources based on the
        specified parameters. Handles creation with proper validation
        and error handling.
        
        Returns:
            Created data structure or resource
        """
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        fig.suptitle('E-commerce Analytics Dashboard', fontsize=20, fontweight='bold', y=0.95)
        
        # Sales status pie chart
        ax1 = fig.add_subplot(gs[0, 0])
        status_data = self.data['sales_status']
        ax1.pie(status_data['count'], labels=status_data['status'], autopct='%1.1f%%', startangle=90)
        ax1.set_title('Sales Status Distribution', fontweight='bold')
        
        # Monthly sales trend
        ax2 = fig.add_subplot(gs[0, 1])
        monthly_data = self.data['monthly_sales'].tail(6)
        ax2.plot(range(len(monthly_data)), monthly_data['total_amount'], marker='o', linewidth=3, markersize=8)
        ax2.set_title('Monthly Sales Trend', fontweight='bold')
        ax2.set_ylabel('Amount ($)')
        ax2.grid(True, alpha=0.3)
        
        # Gender distribution
        ax3 = fig.add_subplot(gs[0, 2])
        gender_data = self.data['gender_dist']
        bars = ax3.bar(gender_data['gender'], gender_data['user_count'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax3.set_title('User Gender Distribution', fontweight='bold')
        ax3.set_ylabel('Number of Users')
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 5, f'{int(height)}', 
                    ha='center', va='bottom', fontweight='bold')
        
        # Payment methods
        ax4 = fig.add_subplot(gs[0, 3])
        payment_data = self.data['payment_dist']
        ax4.pie(payment_data['transaction_count'], labels=payment_data['payment_method'], 
                autopct='%1.1f%%', startangle=90)
        ax4.set_title('Payment Methods', fontweight='bold')
        
        # Top products by quantity
        ax5 = fig.add_subplot(gs[1, :2])
        top_products = self.data['top_products_qty'].head(6)
        bars = ax5.barh(range(len(top_products)), top_products['total_quantity_sold'], color='skyblue')
        ax5.set_yticks(range(len(top_products)))
        ax5.set_yticklabels([name[:40] + '...' if len(name) > 40 else name for name in top_products['product_name']])
        ax5.set_title('Top 6 Products by Quantity Sold', fontweight='bold')
        ax5.set_xlabel('Quantity Sold')
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax5.text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                    ha='left', va='center', fontweight='bold')
        
        # Geographic distribution (states)
        ax6 = fig.add_subplot(gs[1, 2:])
        state_data = self.data['state_dist'].head(8)
        bars = ax6.barh(range(len(state_data)), state_data['user_count'], color='lightcoral')
        ax6.set_yticks(range(len(state_data)))
        ax6.set_yticklabels(state_data['state'])
        ax6.set_title('Top 8 States by User Count', fontweight='bold')
        ax6.set_xlabel('Number of Users')
        
        # Customer spending by gender
        ax7 = fig.add_subplot(gs[2, :2])
        gender_purchases = self.data['gender_purchases']
        x = np.arange(len(gender_purchases))
        width = 0.25
        
        bars1 = ax7.bar(x - width, gender_purchases['total_spent'], width, label='Total Spent', color='#FF6B6B')
        bars2 = ax7.bar(x, gender_purchases['average_purchase'], width, label='Avg Purchase', color='#4ECDC4')
        bars3 = ax7.bar(x + width, gender_purchases['transactions_per_buyer'], width, label='Txns per Buyer', color='#45B7D1')
        
        ax7.set_xlabel('Gender')
        ax7.set_ylabel('Amount ($) / Count')
        ax7.set_title('Customer Spending Analysis by Gender', fontweight='bold')
        ax7.set_xticks(x)
        ax7.set_xticklabels(gender_purchases['gender'])
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        # Top buyers
        ax8 = fig.add_subplot(gs[2, 2:])
        top_buyers = self.data['top_buyers_amount'].head(6)
        bars = ax8.barh(range(len(top_buyers)), top_buyers['total_spent'], color='lightgreen')
        ax8.set_yticks(range(len(top_buyers)))
        ax8.set_yticklabels([f"{row['first_name']} {row['last_name']}" for _, row in top_buyers.iterrows()])
        ax8.set_title('Top 6 Buyers by Total Spent', fontweight='bold')
        ax8.set_xlabel('Total Spent ($)')
        
        # Summary statistics
        ax9 = fig.add_subplot(gs[3, :])
        ax9.axis('off')
        
        # Calculate summary stats
        total_sales = self.data['monthly_sales']['total_amount'].sum()
        total_users = self.data['gender_dist']['user_count'].sum()
        avg_purchase = self.data['gender_purchases']['average_purchase'].mean()
        most_used_payment = self.data['payment_dist'].iloc[0]['payment_method']
        
        summary_text = f"""
        📊 E-COMMERCE ANALYTICS SUMMARY
        {'='*50}
        💰 Total Sales Revenue: ${total_sales:,.2f}
        👥 Total Users: {total_users:,}
        💳 Average Purchase: ${avg_purchase:.2f}
        🏆 Most Used Payment: {most_used_payment}
        📈 Data Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        ax9.text(0.1, 0.5, summary_text, fontsize=14, fontweight='bold', 
                verticalalignment='center', bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        plt.savefig(f'{self.output_path}comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Comprehensive dashboard created")
    
    def generate_all_visualizations(self):
                """
        Generate data or metrics based on configuration.
        
        Creates and processes data according to the specified parameters
        and configuration. Handles data generation with proper validation
        and error reporting.
        
        Returns:
            Generated data structure or processing result
        """
        print("🎨 Generating E-commerce Analytics Visualizations...")
        print("=" * 50)
        
        # Load metrics data
        if not self.load_metrics_data():
            return False
        
        # Load raw data for validation
        if not self.load_raw_data():
            return False
        
        # Validate data quality
        self.validate_data_quality()
        
        try:
            # Generate business analytics charts
            self.create_sales_overview_chart()
            self.create_geographic_analysis()
            self.create_payment_analysis()
            self.create_customer_analysis()
            self.create_product_analysis()
            self.create_comprehensive_dashboard()
            
            # Generate data quality validation charts
            self.create_data_quality_dashboard()
            self.create_validation_comparison_chart()
            
            print("=" * 50)
            print("✅ All visualizations generated successfully!")
            print(f"📁 Images saved to: {self.output_path}")
            print(f"🖼️  Generated {len(os.listdir(self.output_path))} image files")
            
            # Print validation summary
            self.print_validation_summary()
            
            return True
        except Exception as e:
            print(f"❌ Error generating visualizations: {e}")
            return False
    
    def print_validation_summary(self):
                """
        Print Validation Summary.
        
        Performs the print validation summary operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
        print("\n" + "=" * 50)
        print("📊 DATA VALIDATION SUMMARY")
        print("=" * 50)
        
        for data_type in ['valid', 'bad']:
            print(f"\n{data_type.upper()} DATA:")
            total_issues = 0
            total_records = 0
            
            for table_name, results in self.validation_results[data_type].items():
                print(f"  {table_name.upper()}:")
                print(f"    Records: {results['total_records']:,}")
                print(f"    Issues: {results['issue_count']}")
                
                if results['issues']:
                    print("    Issue Details:")
                    for issue in results['issues'][:3]:  # Show first 3 issues
                        print(f"      - {issue}")
                    if len(results['issues']) > 3:
                        print(f"      ... and {len(results['issues']) - 3} more issues")
                
                total_issues += results['issue_count']
                total_records += results['total_records']
                print()
            
            print(f"  TOTAL: {total_records:,} records, {total_issues} issues")
            print(f"  QUALITY SCORE: {((total_records - total_issues) / total_records * 100):.1f}%" if total_records > 0 else "N/A")

def main():
            """
        Main.
        
        Performs the main operation with proper
        validation and error handling. Provides comprehensive functionality
        for the specified operation.
        """
    analyzer = EcommerceAnalyzer()
    analyzer.generate_all_visualizations()

if __name__ == "__main__":
    main()
