"""
Ingest synthetic ecommerce data into SQLite database.
This script reads the CSV files and creates a normalized database schema.
"""

import pandas as pd
import sqlite3
import os
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent

data_dir = project_root / 'data' / 'raw'
db_path = project_root / 'database' / 'ecommerce.db'

db_path.parent.mkdir(parents=True, exist_ok=True)

print("Starting data ingestion into SQLite database...")

if db_path.exists():
    os.remove(db_path)
    print("Removed existing database")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\nCreating database schema...")

cursor.execute('''
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category_id INTEGER,
    price REAL NOT NULL,
    stock_quantity INTEGER,
    description TEXT,
    created_at TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
''')

cursor.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT,
    registration_date TEXT
)
''')

cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT NOT NULL,
    status TEXT,
    total_amount REAL,
    shipping_address TEXT,
    shipping_city TEXT,
    shipping_state TEXT,
    shipping_zip TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

cursor.execute('''
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')

print("Creating indexes...")
cursor.execute('CREATE INDEX idx_orders_customer_id ON orders(customer_id)')
cursor.execute('CREATE INDEX idx_orders_order_date ON orders(order_date)')
cursor.execute('CREATE INDEX idx_order_items_order_id ON order_items(order_id)')
cursor.execute('CREATE INDEX idx_order_items_product_id ON order_items(product_id)')
cursor.execute('CREATE INDEX idx_products_category_id ON products(category_id)')

print("[SUCCESS] Database schema created\n")

print("Loading data from CSV files...")

if (data_dir / 'categories.csv').exists():
    categories_df = pd.read_csv(data_dir / 'categories.csv')
    categories_df.to_sql('categories', conn, if_exists='append', index=False)
    print(f"  [OK] Loaded {len(categories_df)} categories")
else:
    print("  [ERROR] categories.csv not found")

if (data_dir / 'products.csv').exists():
    products_df = pd.read_csv(data_dir / 'products.csv')
    products_df.to_sql('products', conn, if_exists='append', index=False)
    print(f"  [OK] Loaded {len(products_df)} products")
else:
    print("  [ERROR] products.csv not found")

if (data_dir / 'customers.csv').exists():
    customers_df = pd.read_csv(data_dir / 'customers.csv')
    customers_df.to_sql('customers', conn, if_exists='append', index=False)
    print(f"  [OK] Loaded {len(customers_df)} customers")
else:
    print("  [ERROR] customers.csv not found")

if (data_dir / 'orders.csv').exists():
    orders_df = pd.read_csv(data_dir / 'orders.csv')
    orders_df.to_sql('orders', conn, if_exists='append', index=False)
    print(f"  [OK] Loaded {len(orders_df)} orders")
else:
    print("  [ERROR] orders.csv not found")

if (data_dir / 'order_items.csv').exists():
    order_items_df = pd.read_csv(data_dir / 'order_items.csv')
    order_items_df.to_sql('order_items', conn, if_exists='append', index=False)
    print(f"  [OK] Loaded {len(order_items_df)} order items")
else:
    print("  [ERROR] order_items.csv not found")

conn.commit()

print("\nVerifying data...")
cursor.execute("SELECT COUNT(*) FROM categories")
print(f"  Categories: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM products")
print(f"  Products: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM customers")
print(f"  Customers: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM orders")
print(f"  Orders: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM order_items")
print(f"  Order Items: {cursor.fetchone()[0]}")

conn.close()

print(f"\n[SUCCESS] Data ingestion completed successfully!")
print(f"Database created at: {db_path.absolute()}")

