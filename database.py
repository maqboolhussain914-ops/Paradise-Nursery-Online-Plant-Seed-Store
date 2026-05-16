import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "paradise_nursery")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_all_categories():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories

def get_all_products(category_id=None):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    if category_id:
        cursor.execute("SELECT p.*, c.category_name FROM products p JOIN categories c ON p.category_id = c.category_id WHERE p.category_id = %s", (category_id,))
    else:
        cursor.execute("SELECT p.*, c.category_name FROM products p JOIN categories c ON p.category_id = c.category_id")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.*, c.category_name FROM products p JOIN categories c ON p.category_id = c.category_id WHERE p.product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product

# --- Admin Operations ---

def add_product(name, description, price, stock_quantity, category_id, image_url):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        # Determine the next ID (since original DDL might not have AUTO_INCREMENT)
        cursor.execute("SELECT MAX(product_id) FROM products")
        result = cursor.fetchone()
        next_id = 1 if result[0] is None else result[0] + 1
        
        cursor.execute(
            "INSERT INTO products (product_id, name, description, price, stock_quantity, category_id, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (next_id, name, description, price, stock_quantity, category_id, image_url)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error adding product: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_product(product_id, name, description, price, stock_quantity, category_id, image_url):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE products SET name=%s, description=%s, price=%s, stock_quantity=%s, category_id=%s, image_url=%s WHERE product_id=%s",
            (name, description, price, stock_quantity, category_id, image_url, product_id)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error updating product: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error deleting product: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_orders():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, u.first_name, u.last_name, u.email
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_date DESC
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

def get_dashboard_stats():
    conn = get_db_connection()
    if not conn: return {'products': 0, 'orders': 0, 'revenue': 0}
    cursor = conn.cursor(dictionary=True)
    stats = {}
    
    cursor.execute("SELECT COUNT(*) as total FROM products")
    stats['products'] = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM orders")
    stats['orders'] = cursor.fetchone()['total']
    
    cursor.execute("SELECT SUM(total_amount) as revenue FROM orders")
    rev = cursor.fetchone()['revenue']
    stats['revenue'] = float(rev) if rev else 0.0
    
    cursor.close()
    conn.close()
    return stats
