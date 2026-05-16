import database as db

# High-quality Unsplash image URLs for plants
images = [
    "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800&q=80", # Potted plant
    "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=800&q=80", # Succulents
    "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?w=800&q=80", # Lush leaves
    "https://images.unsplash.com/photo-1545241047-6083a36a1c1c?w=800&q=80", # Monstera
    "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?w=800&q=80", # Hanging plant
    "https://images.unsplash.com/photo-1416879598555-27a3c3e2db78?w=800&q=80", # Seedlings
    "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=800&q=80", # Snake plant
    "https://images.unsplash.com/photo-1520302630591-fd1c66edc19d?w=800&q=80", # Various indoor
    "https://images.unsplash.com/photo-1512616239105-04b3eafe367a?w=800&q=80", # Outdoor bush
    "https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=800&q=80"  # Small fern
]

def update_product_images():
    conn = db.get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        return
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_id FROM products")
    products = cursor.fetchall()
    
    for i, product in enumerate(products):
        img = images[i % len(images)]
        cursor.execute("UPDATE products SET image_url=%s WHERE product_id=%s", (img, product['product_id']))
        
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully updated images for {len(products)} products.")

if __name__ == '__main__':
    update_product_images()
