import mysql.connector
import sys

try:
    # First connect without a database to check/create paradise_nursery
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Millat914@"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS paradise_nursery;")
    cursor.execute("USE paradise_nursery;")
    
    # Check if tables exist
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    if len(tables) > 0:
        print(f"Connected successfully! Found {len(tables)} tables in 'paradise_nursery'.")
    else:
        print("Connected successfully! Database 'paradise_nursery' created but is empty.")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Connection Failed: {e}")
    sys.exit(1)
