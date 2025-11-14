"""
Generate synthetic ecommerce data.
This script creates 5 CSV files with realistic ecommerce data:
- customers.csv
- products.csv
- orders.csv
- order_items.csv
- categories.csv
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from pathlib import Path

fake = Faker()
Faker.seed(42)
random.seed(42)

script_dir = Path(__file__).parent
project_root = script_dir.parent

output_dir = project_root / 'data' / 'raw'
os.makedirs(output_dir, exist_ok=True)

print("Generating synthetic ecommerce data...")

print("1. Generating categories...")
categories = []
category_names = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports & Outdoors', 
                 'Toys & Games', 'Health & Beauty', 'Automotive', 'Food & Beverages', 'Office Supplies']
for i, name in enumerate(category_names, 1):
    categories.append({
        'category_id': i,
        'category_name': name,
        'description': f'Products in the {name} category'
    })
categories_df = pd.DataFrame(categories)
categories_df.to_csv(str(output_dir / 'categories.csv'), index=False)
print(f"   Created categories.csv with {len(categories)} categories")

print("2. Generating products...")
products = []
product_names = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch', 'Camera', 'Speaker', 'Monitor'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress', 'Hat', 'Socks', 'Shorts'],
    'Home & Garden': ['Lamp', 'Chair', 'Table', 'Plant Pot', 'Garden Tool', 'Cushion', 'Curtains', 'Rug'],
    'Books': ['Novel', 'Textbook', 'Cookbook', 'Biography', 'Mystery', 'Science Fiction', 'History', 'Poetry'],
    'Sports & Outdoors': ['Bicycle', 'Tent', 'Running Shoes', 'Yoga Mat', 'Dumbbells', 'Basketball', 'Tennis Racket', 'Hiking Boots'],
    'Toys & Games': ['Board Game', 'Action Figure', 'Puzzle', 'LEGO Set', 'Doll', 'Remote Car', 'Building Blocks', 'Card Game'],
    'Health & Beauty': ['Shampoo', 'Moisturizer', 'Toothbrush', 'Vitamins', 'Perfume', 'Makeup Kit', 'Hair Dryer', 'Face Mask'],
    'Automotive': ['Car Battery', 'Tire', 'Oil Filter', 'Brake Pad', 'Car Cover', 'Floor Mat', 'Air Freshener', 'Jump Starter'],
    'Food & Beverages': ['Coffee', 'Tea', 'Chocolate', 'Snacks', 'Juice', 'Cereal', 'Pasta', 'Sauce'],
    'Office Supplies': ['Notebook', 'Pen Set', 'Stapler', 'File Folder', 'Desk Organizer', 'Calculator', 'Printer Paper', 'Binder']
}

product_id = 1
for category_id, category_name in enumerate(category_names, 1):
    for product_name in product_names[category_name]:
        products.append({
            'product_id': product_id,
            'product_name': f'{product_name} {fake.word().capitalize()}',
            'category_id': category_id,
            'price': round(random.uniform(10, 500), 2),
            'stock_quantity': random.randint(0, 1000),
            'description': fake.text(max_nb_chars=100),
            'created_at': fake.date_between(start_date='-2y', end_date='today').isoformat()
        })
        product_id += 1

products_df = pd.DataFrame(products)
products_df.to_csv(str(output_dir / 'products.csv'), index=False)
print(f"   Created products.csv with {len(products)} products")

print("3. Generating customers...")
customers = []
used_emails = set()
for i in range(1, 501):
    email = fake.email()
    while email in used_emails:
        email = fake.email()
    used_emails.add(email)
    
    customers.append({
        'customer_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': email,
        'phone': fake.phone_number(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'zip_code': fake.zipcode(),
        'country': 'USA',
        'registration_date': fake.date_between(start_date='-3y', end_date='today').isoformat()
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(str(output_dir / 'customers.csv'), index=False)
print(f"   Created customers.csv with {len(customers)} customers")

print("4. Generating orders...")
orders = []
order_id = 1
start_date = datetime.now() - timedelta(days=365)

for customer_id in range(1, 501):
    num_orders = random.randint(0, 10)
    for _ in range(num_orders):
        order_date = fake.date_between(start_date='-1y', end_date='today')
        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date.isoformat(),
            'status': random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
            'shipping_address': fake.street_address(),
            'shipping_city': fake.city(),
            'shipping_state': fake.state_abbr(),
            'shipping_zip': fake.zipcode()
        })
        order_id += 1

orders_df = pd.DataFrame(orders)
orders_df.to_csv(str(output_dir / 'orders.csv'), index=False)
print(f"   Created orders.csv with {len(orders)} orders")

print("5. Generating order items...")
order_items = []
order_item_id = 1

product_prices = dict(zip(products_df['product_id'], products_df['price']))

for order_id in range(1, len(orders) + 1):
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 5)
        price = product_prices[product_id]
        
        order_items.append({
            'order_item_id': order_item_id,
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': price,
            'subtotal': round(quantity * price, 2)
        })
        order_item_id += 1

order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv(str(output_dir / 'order_items.csv'), index=False)
print(f"   Created order_items.csv with {len(order_items)} order items")

print("6. Calculating order totals...")
order_totals = order_items_df.groupby('order_id')['subtotal'].sum().reset_index()
order_totals.columns = ['order_id', 'total_amount']
orders_df = orders_df.merge(order_totals, on='order_id', how='left')
orders_df['total_amount'] = orders_df['total_amount'].fillna(0).round(2)
orders_df.to_csv(str(output_dir / 'orders.csv'), index=False)

print("\n[SUCCESS] All data files generated successfully!")
print(f"\nGenerated files in {output_dir}/:")
print("  - categories.csv")
print("  - products.csv")
print("  - customers.csv")
print("  - orders.csv")
print("  - order_items.csv")

