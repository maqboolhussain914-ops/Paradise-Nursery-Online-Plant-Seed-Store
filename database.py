import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from decimal import Decimal

load_dotenv()

# ─── Connection Manager ───
# Uses a context manager to ensure connections and cursors are always
# properly closed, even if an exception occurs mid-query.

@contextmanager
def get_db_cursor(dictionary=False):
    """Context manager that yields a (connection, cursor) pair and handles cleanup."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "paradise_nursery"),
            autocommit=False,
            connection_timeout=10
        )
        cursor = conn.cursor(dictionary=dictionary)
        yield conn, cursor
    except Error as e:
        print(f"[DB ERROR] Connection/query error: {e}")
        if conn and conn.is_connected():
            conn.rollback()
        raise
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass


# ─── READ Operations ───

def get_all_categories():
    """Fetch all product categories."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT * FROM categories ORDER BY category_name")
            return cursor.fetchall()
    except Error:
        return []


def get_all_products(category_id=None):
    """Fetch all products, optionally filtered by category_id."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            if category_id:
                cursor.execute(
                    "SELECT p.*, c.category_name FROM products p "
                    "JOIN categories c ON p.category_id = c.category_id "
                    "WHERE p.category_id = %s ORDER BY p.name",
                    (int(category_id),)
                )
            else:
                cursor.execute(
                    "SELECT p.*, c.category_name FROM products p "
                    "JOIN categories c ON p.category_id = c.category_id "
                    "ORDER BY p.name"
                )
            return cursor.fetchall()
    except Error:
        return []


def get_product_by_id(product_id):
    """Fetch a single product by its ID, including its category name."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute(
                "SELECT p.*, c.category_name FROM products p "
                "JOIN categories c ON p.category_id = c.category_id "
                "WHERE p.product_id = %s",
                (int(product_id),)
            )
            return cursor.fetchone()
    except Error:
        return None


# ─── ADMIN: Product Operations ───

def add_product(name, description, price, stock_quantity, category_id, image_url):
    """Insert a new product. Auto-generates the next product_id."""
    try:
        with get_db_cursor() as (conn, cursor):
            # Get next available ID
            cursor.execute("SELECT COALESCE(MAX(product_id), 0) + 1 FROM products")
            next_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO products (product_id, name, description, price, stock_quantity, category_id, image_url) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (next_id, str(name).strip(), description, float(price), int(stock_quantity), int(category_id), image_url)
            )
            conn.commit()
            return True
    except Error as e:
        print(f"[DB ERROR] add_product: {e}")
        return False


def update_product(product_id, name, description, price, stock_quantity, category_id, image_url):
    """Update an existing product by ID."""
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute(
                "UPDATE products SET name=%s, description=%s, price=%s, "
                "stock_quantity=%s, category_id=%s, image_url=%s WHERE product_id=%s",
                (str(name).strip(), description, float(price), int(stock_quantity), int(category_id), image_url, int(product_id))
            )
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] update_product: {e}")
        return False


def delete_product(product_id):
    """Delete a product by ID. CASCADE will remove related order_items."""
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("DELETE FROM products WHERE product_id=%s", (int(product_id),))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] delete_product: {e}")
        return False


# ─── ADMIN: Order Operations ───

def get_all_orders():
    """Fetch all orders with customer info, newest first."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT o.*, u.first_name, u.last_name, u.email
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                ORDER BY o.order_date DESC
            """)
            return cursor.fetchall()
    except Error:
        return []


def update_order_status(order_id, status):
    """Update the status of an order (Pending, Shipped, Delivered, Cancelled)."""
    valid_statuses = {'Pending', 'Shipped', 'Delivered', 'Cancelled'}
    if status not in valid_statuses:
        print(f"[DB ERROR] Invalid order status: {status}")
        return False

    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (status, int(order_id)))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] update_order_status: {e}")
        return False


# ─── ADMIN: Category Operations ───

def add_category(category_name, description):
    """Insert a new category. Auto-generates the next category_id."""
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM categories")
            next_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s)",
                (next_id, str(category_name).strip(), description)
            )
            conn.commit()
            return True
    except Error as e:
        print(f"[DB ERROR] add_category: {e}")
        return False


def update_category(category_id, category_name, description):
    """Update an existing category."""
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute(
                "UPDATE categories SET category_name=%s, description=%s WHERE category_id=%s",
                (str(category_name).strip(), description, int(category_id))
            )
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] update_category: {e}")
        return False


def delete_category(category_id):
    """Delete a category. Will fail if products reference it (unless CASCADE)."""
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("DELETE FROM categories WHERE category_id=%s", (int(category_id),))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] delete_category: {e}")
        return False


# ─── STOREFRONT: Checkout Operations ───

def get_or_create_user(first_name, last_name, email, phone, street_address, city, state, zip_code):
    """Finds a user by email or creates a new one if they don't exist."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return user['user_id']
            
            # Create new user
            cursor.execute("SELECT COALESCE(MAX(user_id), 0) + 1 FROM users")
            next_id = cursor.fetchone()['COALESCE(MAX(user_id), 0) + 1']
            
            # Using a default hash for guest users
            cursor.execute(
                "INSERT INTO users (user_id, first_name, last_name, email, password_hash, phone, street_address, city, state, zip_code) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (next_id, first_name, last_name, email, 'guest_account', phone, street_address, city, state, zip_code)
            )
            conn.commit()
            return next_id
    except Error as e:
        print(f"[DB ERROR] get_or_create_user: {e}")
        return None


def create_order(user_id, cart_items, total_amount, shipping_address):
    """Creates an order, adds order items, and deducts stock inside a transaction."""
    try:
        with get_db_cursor() as (conn, cursor):
            # 1. Create Order
            cursor.execute("SELECT COALESCE(MAX(order_id), 0) + 1 FROM orders")
            order_id = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO orders (order_id, user_id, total_amount, status, shipping_address) "
                "VALUES (%s, %s, %s, %s, %s)",
                (order_id, user_id, total_amount, 'Pending', shipping_address)
            )
            
            # 2. Add Order Items & Deduct Stock
            cursor.execute("SELECT COALESCE(MAX(order_item_id), 0) FROM order_items")
            last_item_id = cursor.fetchone()[0]
            
            for item in cart_items:
                product = item['product']
                qty = item['quantity']
                price = product['price']
                last_item_id += 1
                
                # Insert order item
                cursor.execute(
                    "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price_at_purchase) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (last_item_id, order_id, product['product_id'], qty, price)
                )
                
                # Deduct stock
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (qty, product['product_id'])
                )
                
            conn.commit()
            return order_id
    except Error as e:
        print(f"[DB ERROR] create_order: {e}")
        # conn.rollback() is handled by context manager if exception is raised, 
        # but since we catch it here, we should rollback manually just in case
        return None

def get_order_with_items(order_id):
    """Fetch an order and its items for the success page."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            
            if order:
                cursor.execute(
                    "SELECT oi.*, p.name, p.image_url FROM order_items oi "
                    "JOIN products p ON oi.product_id = p.product_id "
                    "WHERE oi.order_id = %s",
                    (order_id,)
                )
                order['items'] = cursor.fetchall()
                
                cursor.execute("SELECT first_name, last_name, email FROM users WHERE user_id = %s", (order['user_id'],))
                order['user'] = cursor.fetchone()
                
            return order
    except Error as e:
        print(f"[DB ERROR] get_order_with_items: {e}")
        return None

# ─── ADMIN: Dashboard Analytics ───

def get_dashboard_stats():
    """Get aggregate counts and revenue for the dashboard."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            stats = {}

            cursor.execute("SELECT COUNT(*) as total FROM products")
            stats['products'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM orders")
            stats['orders'] = cursor.fetchone()['total']

            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as revenue FROM orders")
            rev = cursor.fetchone()['revenue']
            stats['revenue'] = float(rev) if isinstance(rev, Decimal) else float(rev or 0)

            return stats
    except Error:
        return {'products': 0, 'orders': 0, 'revenue': 0.0}


def get_low_stock_products(threshold=15):
    """Get products with stock at or below the threshold."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute(
                "SELECT p.*, c.category_name FROM products p "
                "JOIN categories c ON p.category_id = c.category_id "
                "WHERE p.stock_quantity <= %s ORDER BY p.stock_quantity ASC",
                (int(threshold),)
            )
            return cursor.fetchall()
    except Error:
        return []


def get_recent_orders(limit=5):
    """Get the most recent N orders with customer names."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT o.*, u.first_name, u.last_name
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                ORDER BY o.order_date DESC LIMIT %s
            """, (int(limit),))
            return cursor.fetchall()
    except Error:
        return []


def get_sales_by_category():
    """Aggregate sales revenue by product category for the dashboard chart."""
    try:
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT c.category_name as label,
                       COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) as data
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                GROUP BY c.category_id, c.category_name
                ORDER BY data DESC
            """)
            data = cursor.fetchall()
            # Convert Decimal values to float for JSON serialization
            for row in data:
                row['data'] = float(row['data']) if isinstance(row['data'], Decimal) else float(row['data'] or 0)
            return data
    except Error:
        return []
