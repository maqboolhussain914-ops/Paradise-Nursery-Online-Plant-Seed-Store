import csv
import random
from datetime import datetime, timedelta

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def main():
    num_users = 60
    num_categories = 5
    num_products = 50
    num_orders = 70
    num_carts = 30
    
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 5, 1)

    # 1. Users
    first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan', 'Judy', 'Maqbool', 'Ali', 'Sara', 'Omar']
    last_names = ['Smith', 'Doe', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Hussain', 'Khan', 'Ahmed']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Peshawar', 'Islamabad', 'Lahore', 'Karachi']
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'KP', 'IS', 'PB', 'SD']
    
    users = []
    for i in range(1, num_users + 1):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        users.append([
            i, 
            fn, 
            ln, 
            f"{fn.lower()}.{ln.lower()}{i}@example.com",
            f"hash_pwd_{random.randint(1000, 9999)}",
            f"555-{random.randint(100,999)}-{random.randint(1000,9999)}",
            f"{random.randint(1, 9999)} Main St",
            random.choice(cities),
            random.choice(states),
            f"{random.randint(10000, 99999)}",
            generate_random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
        ])
    
    with open('users.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'first_name', 'last_name', 'email', 'password_hash', 'phone', 'street_address', 'city', 'state', 'zip_code', 'created_at'])
        writer.writerows(users)

    # 2. Categories
    category_names = ['Indoor Plants', 'Outdoor Plants', 'Succulents', 'Vegetable Seeds', 'Flower Seeds']
    categories = []
    for i in range(1, num_categories + 1):
        categories.append([i, category_names[i-1], f"Beautiful {category_names[i-1].lower()} for your garden"])
        
    with open('categories.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category_id', 'category_name', 'description'])
        writer.writerows(categories)

    # 3. Products
    plant_names = ['Monstera', 'Snake Plant', 'Ficus', 'Aloe Vera', 'Rose', 'Tulip', 'Tomato', 'Basil', 'Mint', 'Lavender', 'Cactus', 'Fern', 'Orchid']
    products = []
    for i in range(1, num_products + 1):
        cat_id = random.randint(1, num_categories)
        products.append([
            i,
            f"{random.choice(plant_names)} {i}",
            "A wonderful addition to your home or garden.",
            round(random.uniform(5.99, 49.99), 2),
            random.randint(10, 200),
            cat_id,
            f"http://example.com/images/plant_{i}.jpg",
            generate_random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    with open('products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['product_id', 'name', 'description', 'price', 'stock_quantity', 'category_id', 'image_url', 'created_at'])
        writer.writerows(products)

    # 4. Orders
    orders = []
    statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
    for i in range(1, num_orders + 1):
        u_id = random.randint(1, num_users)
        orders.append([
            i,
            u_id,
            generate_random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S"),
            round(random.uniform(15.00, 150.00), 2),
            random.choice(statuses),
            f"{random.randint(1, 999)} Shipping Ave"
        ])
        
    with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['order_id', 'user_id', 'order_date', 'total_amount', 'status', 'shipping_address'])
        writer.writerows(orders)

    # 5. Order Items
    order_items = []
    order_item_id = 1
    for o_id in range(1, num_orders + 1):
        num_items = random.randint(1, 4)
        for _ in range(num_items):
            p_id = random.randint(1, num_products)
            order_items.append([
                order_item_id,
                o_id,
                p_id,
                random.randint(1, 5),
                products[p_id-1][3] # price at purchase
            ])
            order_item_id += 1
            
    with open('order_items.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['order_item_id', 'order_id', 'product_id', 'quantity', 'price_at_purchase'])
        writer.writerows(order_items)

    # 6. Cart
    carts = []
    for i in range(1, num_carts + 1):
        u_id = random.randint(1, num_users)
        carts.append([
            i,
            u_id,
            generate_random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    with open('cart.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['cart_id', 'user_id', 'created_at'])
        writer.writerows(carts)

    # 7. Cart Items
    cart_items = []
    cart_item_id = 1
    for c_id in range(1, num_carts + 1):
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            p_id = random.randint(1, num_products)
            cart_items.append([
                cart_item_id,
                c_id,
                p_id,
                random.randint(1, 3)
            ])
            cart_item_id += 1
            
    with open('cart_items.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['cart_item_id', 'cart_id', 'product_id', 'quantity'])
        writer.writerows(cart_items)

    print("Data generation complete. 7 CSV files created.")

if __name__ == '__main__':
    main()
