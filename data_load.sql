-- ==========================================
-- Paradise Nursery Database Data Population (DML)
-- ==========================================

-- 1. Load Data using LOAD DATA INFILE (MySQL specific approach)
-- Note: Replace 'C:/path/to/csv/' with the actual absolute path to your CSV files when running in MySQL Workbench.
-- Assuming secure_file_priv allows loading from this directory.

LOAD DATA INFILE 'users.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(user_id, first_name, last_name, email, password_hash, phone, street_address, city, state, zip_code, created_at);

LOAD DATA INFILE 'categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(category_id, category_name, description);

LOAD DATA INFILE 'products.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, name, description, price, stock_quantity, category_id, image_url, created_at);

LOAD DATA INFILE 'orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, user_id, order_date, total_amount, status, shipping_address);

LOAD DATA INFILE 'order_items.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_item_id, order_id, product_id, quantity, price_at_purchase);

LOAD DATA INFILE 'cart.csv'
INTO TABLE cart
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(cart_id, user_id, created_at);

LOAD DATA INFILE 'cart_items.csv'
INTO TABLE cart_items
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(cart_item_id, cart_id, product_id, quantity);


-- ==========================================
-- 2. DML Operations (UPDATE and DELETE)
-- ==========================================

-- Example UPDATE: Increase the price of a specific product by 10%
UPDATE products
SET price = price * 1.10
WHERE product_id = 1;

-- Example UPDATE: Change an order's status to 'Shipped'
UPDATE orders
SET status = 'Shipped'
WHERE order_id = 5 AND status = 'Pending';

-- Example DELETE: Remove a user who requested account deletion (cascades to their orders and cart)
DELETE FROM users
WHERE user_id = 60;

-- Example DELETE: Remove an item from a cart
DELETE FROM cart_items
WHERE cart_item_id = 15;


-- ==========================================
-- 3. Validation Queries
-- ==========================================

-- A. Row Counts for all tables
SELECT 'users' AS TableName, COUNT(*) AS RowCount FROM users
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'cart', COUNT(*) FROM cart
UNION ALL
SELECT 'cart_items', COUNT(*) FROM cart_items;

-- B. NULL Check on Key Columns
-- Checking if any required foreign keys or important fields are unexpectedly NULL
SELECT 
    (SELECT COUNT(*) FROM products WHERE category_id IS NULL) AS NULL_categories_in_products,
    (SELECT COUNT(*) FROM orders WHERE user_id IS NULL) AS NULL_users_in_orders,
    (SELECT COUNT(*) FROM order_items WHERE product_id IS NULL) AS NULL_products_in_order_items;

-- C. JOIN-based check to confirm Foreign Key integrity
-- This query finds any order_items that reference a non-existent product
SELECT oi.order_item_id, oi.product_id
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

-- This query joins orders with users to display order totals alongside customer emails
SELECT o.order_id, u.email, o.total_amount, o.status
FROM orders o
JOIN users u ON o.user_id = u.user_id
LIMIT 10;
