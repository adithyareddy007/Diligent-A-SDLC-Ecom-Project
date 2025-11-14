# Ecommerce Data Analysis Project

## Project Overview
This exercise includes:
1. **Synthetic Ecommerce Data Generation**: Creates 5 CSV files with realistic ecommerce data
2. **Data Ingestion**: Loads the generated data into a SQLite database
3. **SQL Analysis**: Queries that join multiple tables to generate insights

## Project Structure

```
.
├── data/
│   ├── raw/              # Generated synthetic data files
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   ├── order_items.csv
│   │   └── categories.csv
├── scripts/
│   ├── generate_data.py  # Script to generate synthetic ecommerce data
│   ├── ingest_data.py    # Script to ingest data into SQLite
│   └── queries.sql       # SQL queries for analysis
├── database/
│   └── ecommerce.db      # SQLite database (generated)
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Synthetic Data**
   ```bash
   python scripts/generate_data.py
   ```
   This will create 5 CSV files in the `data/raw/` directory.

3. **Ingest Data into SQLite**
   ```bash
   python scripts/ingest_data.py
   ```
   This will create the database and load all CSV files.

4. **Run SQL Queries**
   ```bash
   sqlite3 database/ecommerce.db < scripts/queries.sql
   ```
   Or use a SQLite browser to execute the queries.

## Generated Data Files
- **customers.csv**: Customer information (ID, name, email, address, etc.)
- **products.csv**: Product catalog (ID, name, category, price, etc.)
- **orders.csv**: Order records (ID, customer_id, order_date, total_amount)
- **order_items.csv**: Order line items (order_id, product_id, quantity, price)
- **categories.csv**: Product categories (ID, name, description)

## Database Schema
The SQLite database contains tables with the following relationships:
- `customers` → `orders` (one-to-many)
- `orders` → `order_items` (one-to-many)
- `products` → `order_items` (one-to-many)
- `categories` → `products` (one-to-many)

## SQL Queries
The `queries.sql` file contains multiple queries that:
- Join customers, orders, and order_items
- Aggregate sales by category
- Calculate customer lifetime value
- Find top-selling products
- Generate revenue reports

## Requirements
- Python 3.7+
- SQLite3 (included with Python)

