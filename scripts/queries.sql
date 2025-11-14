-- SQL Queries for Ecommerce Data Analysis

-- ============================================
-- Query 1: Customer Order Summary with Total Revenue
-- Joins: customers, orders, order_items
-- ============================================
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.subtotal) AS total_revenue,
    AVG(oi.subtotal) AS avg_order_value,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date
FROM 
    customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY 
    c.customer_id, c.first_name, c.last_name, c.email
ORDER BY 
    total_revenue DESC
LIMIT 20;

-- ============================================
-- Query 2: Sales by Product Category
-- Joins: categories, products, order_items
-- ============================================
SELECT 
    cat.category_id,
    cat.category_name,
    COUNT(DISTINCT oi.product_id) AS products_sold,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue,
    AVG(oi.unit_price) AS avg_product_price
FROM 
    categories cat
    JOIN products p ON cat.category_id = p.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY 
    cat.category_id, cat.category_name
ORDER BY 
    total_revenue DESC;

-- ============================================
-- Query 3: Top Selling Products with Category Information
-- Joins: products, categories, order_items
-- ============================================
SELECT 
    p.product_id,
    p.product_name,
    cat.category_name,
    p.price AS current_price,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue,
    COUNT(DISTINCT oi.order_id) AS number_of_orders
FROM 
    products p
    JOIN categories cat ON p.category_id = cat.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY 
    p.product_id, p.product_name, cat.category_name, p.price
ORDER BY 
    total_revenue DESC
LIMIT 20;

-- ============================================
-- Query 4: Monthly Sales Report
-- Joins: orders, order_items, customers
-- ============================================
SELECT 
    strftime('%Y-%m', o.order_date) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(oi.subtotal) AS total_revenue,
    AVG(oi.subtotal) AS avg_order_value
FROM 
    orders o
    JOIN order_items oi ON o.order_id = oi.order_id
WHERE 
    o.status != 'cancelled'
GROUP BY 
    strftime('%Y-%m', o.order_date)
ORDER BY 
    month DESC;

-- ============================================
-- Query 5: Customer Lifetime Value by State
-- Joins: customers, orders, order_items
-- ============================================
SELECT 
    c.state,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.subtotal) AS total_revenue,
    AVG(oi.subtotal) AS avg_order_value,
    SUM(oi.subtotal) / COUNT(DISTINCT c.customer_id) AS avg_customer_lifetime_value
FROM 
    customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE 
    o.status != 'cancelled' OR o.status IS NULL
GROUP BY 
    c.state
HAVING 
    total_customers > 0
ORDER BY 
    avg_customer_lifetime_value DESC;

-- ============================================
-- Query 6: Order Details with Customer and Product Information
-- Joins: orders, customers, order_items, products, categories
-- ============================================
SELECT 
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email AS customer_email,
    oi.product_id,
    p.product_name,
    cat.category_name,
    oi.quantity,
    oi.unit_price,
    oi.subtotal
FROM 
    orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
WHERE 
    o.order_date >= date('now', '-30 days')
ORDER BY 
    o.order_date DESC, o.order_id
LIMIT 50;

-- ============================================
-- Query 7: Product Performance Analysis
-- Joins: products, categories, order_items, orders
-- ============================================
SELECT 
    p.product_id,
    p.product_name,
    cat.category_name,
    p.price,
    p.stock_quantity,
    COUNT(DISTINCT oi.order_id) AS times_ordered,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.subtotal) AS total_revenue,
    CASE 
        WHEN p.stock_quantity < 10 THEN 'Low Stock'
        WHEN p.stock_quantity < 50 THEN 'Medium Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM 
    products p
    JOIN categories cat ON p.category_id = cat.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status != 'cancelled'
GROUP BY 
    p.product_id, p.product_name, cat.category_name, p.price, p.stock_quantity
ORDER BY 
    total_revenue DESC NULLS LAST;

-- ============================================
-- Query 8: Customer Segmentation by Purchase Behavior
-- Joins: customers, orders, order_items
-- ============================================
SELECT 
    CASE 
        WHEN total_revenue >= 1000 THEN 'High Value'
        WHEN total_revenue >= 500 THEN 'Medium Value'
        WHEN total_revenue >= 100 THEN 'Low Value'
        ELSE 'No Purchase'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    AVG(total_revenue) AS avg_revenue,
    AVG(total_orders) AS avg_orders
FROM (
    SELECT 
        c.customer_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COALESCE(SUM(oi.subtotal), 0) AS total_revenue
    FROM 
        customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE 
        o.status != 'cancelled' OR o.status IS NULL
    GROUP BY 
        c.customer_id
)
GROUP BY 
    customer_segment
ORDER BY 
    CASE customer_segment
        WHEN 'High Value' THEN 1
        WHEN 'Medium Value' THEN 2
        WHEN 'Low Value' THEN 3
        ELSE 4
    END;

