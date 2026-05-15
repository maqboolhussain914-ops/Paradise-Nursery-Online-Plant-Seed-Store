import mysql.connector
import csv
import sys
import os

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Millat914@",
        database="paradise_nursery"
    )
    cursor = conn.cursor()

    # 1. Execute schema.sql
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()

    # split into statements
    statements = schema_sql.split(';')
    for stmt in statements:
        if stmt.strip():
            try:
                cursor.execute(stmt)
            except Exception as e:
                # ignore 'Table exists' or 'Index exists' errors
                pass
    conn.commit()
    print("Schema executed.")

    # 2. Insert data using Python to avoid LOAD DATA INFILE permission issues
    tables = ['users', 'categories', 'products', 'orders', 'order_items', 'cart', 'cart_items']
    for table in tables:
        csv_file = f"{table}.csv"
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                placeholders = ', '.join(['%s'] * len(headers))
                query = f"INSERT INTO {table} ({', '.join(headers)}) VALUES ({placeholders})"
                
                rows = []
                for row in reader:
                    # convert empty strings to None (NULL)
                    rows.append([val if val else None for val in row])
                
                try:
                    cursor.executemany(query, rows)
                    print(f"Loaded {len(rows)} rows into {table}.")
                except Exception as e:
                    print(f"Error loading {table}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Data load complete.")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
