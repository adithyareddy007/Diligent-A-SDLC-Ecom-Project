"""
Test script to run SQL queries and display results.
"""

import sqlite3
from pathlib import Path

# Get database path
script_dir = Path(__file__).parent
project_root = script_dir.parent
db_path = project_root / 'database' / 'ecommerce.db'

# Connect to database
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("Testing SQL Queries")
print("=" * 60)

# Test Query 1: Customer Order Summary
print("\n1. Top 10 Customers by Revenue:")
print("-" * 60)
cursor.execute("""
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.subtotal), 2) AS total_revenue
    FROM 
        customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY 
        c.customer_id, c.first_name, c.last_name
    ORDER BY 
        total_revenue DESC
    LIMIT 10
""")

results = cursor.fetchall()
for row in results:
    print(f"  Customer {row[0]}: {row[1]} - {row[2]} orders, ${row[3]:.2f}")

# Test Query 2: Sales by Category
print("\n2. Sales by Product Category:")
print("-" * 60)
cursor.execute("""
    SELECT 
        cat.category_name,
        COUNT(DISTINCT oi.product_id) AS products_sold,
        SUM(oi.quantity) AS total_quantity_sold,
        ROUND(SUM(oi.subtotal), 2) AS total_revenue
    FROM 
        categories cat
        JOIN products p ON cat.category_id = p.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY 
        cat.category_id, cat.category_name
    ORDER BY 
        total_revenue DESC
""")

results = cursor.fetchall()
for row in results:
    print(f"  {row[0]}: {row[1]} products, {row[2]} units sold, ${row[3]:.2f} revenue")

# Test Query 3: Top Selling Products
print("\n3. Top 10 Selling Products:")
print("-" * 60)
cursor.execute("""
    SELECT 
        p.product_name,
        cat.category_name,
        SUM(oi.quantity) AS total_quantity_sold,
        ROUND(SUM(oi.subtotal), 2) AS total_revenue
    FROM 
        products p
        JOIN categories cat ON p.category_id = cat.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY 
        p.product_id, p.product_name, cat.category_name
    ORDER BY 
        total_revenue DESC
    LIMIT 10
""")

results = cursor.fetchall()
for row in results:
    print(f"  {row[0]} ({row[1]}): {row[2]} units, ${row[3]:.2f}")

print("\n" + "=" * 60)
print("[SUCCESS] All queries executed successfully!")
print("=" * 60)

conn.close()

