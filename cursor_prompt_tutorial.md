# Cursor tutorial
# ================================================================

## Use case prompts ==============================================
1) Create two Python scritps:
    - generate_fake_data.py to generate fake valid data 
    - and generate_bad_records.py for  bad  records
    
    To be used in this use case:
        - e-commerce aplication, with users, products , sellers, sales, payments
        - create .csv files:
            -- tests/data_sources/sales.csv 
            -- tests/data_sources/payments.csv
            -- tests/data_sources/products.csv
            -- tests/data_sources/users.csv
        ** save all datasets at tests/data_sources/
        ** save all .png file ate images

2) Create a Python script called generate_metrics_dataframes.py  in order to generate dataframes outputs with some metrics, like:
    -- users distribution by address.
    -- Total sales
    -- The top 10 most saled product
    -- The top 10 buyers
    -- Which payment method is most used? 
    -- How many users are women or men and bought more?
    -- at tests/metrics/
    -- The metrics should have validate data and bad  data
    -- create a python class EcommerceAnalyzer to generate graphic static visualization using the file metrics generated

3) Pytest step, create a pytest.ini file

4) Create unit testing meethod with pytest lib to test:
    - generate_metrics_dataframes.py  (use Pytest fixtures)
    - generate_bad_records.py (use Pytest Mock, MagicMock)
    - generate_fake_data.py (use Pytest Mock, MagicMock)
    - ecommerce_analysis.py (use Pytest patch)
    -  Save the tests files at tests/

5) Create a qualty check class with Pydantic to validate schema from sales, sellers, users, products and payments, and a pytest for this class.

6) Create a qualty check class with Pydantic to validate data from sales, sellers, users, products and payments, and a pytest for this class.

7) Generate Documentantion (dosctring) for all *.py methods

8) Create a simple README.md file with a step by step teaching how to use this projetc.

# RUN COMMANDS
python generate_fake_data.py
python generate_bad_records.py
python generate_metrics_dataframes.py
python ecommerce_analysis.py

## TESTS
python -m pytest tests/ -v
python -m pytest tests/unit/
python -m pytest tests/unit/test_ecommerce_analyzer.py -v --tb=short
