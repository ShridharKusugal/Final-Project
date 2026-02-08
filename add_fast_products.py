import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

products = [
    # Generated Images
    ("Hero Passion Pro Speedometer", "Digital speedometer console for Hero Passion Pro", 1200.00, 50, "hero_passion_meter.png", "Spare Parts"),
    ("Bajaj Discover Carburetor", "High efficiency carburetor for Bajaj Discover 125", 1850.50, 50, "bajaj_discover_carburetor.png", "Engine Parts"),
    ("Yamaha FZ Rear Disc Plate", "Stainless steel rear disc rotor for Yamaha FZ", 950.00, 50, "yamaha_fz_rear_disc.png", "Brakes"),
    ("RE Classic 350 Silencer", "Chrome finish exhaust silencer for Royal Enfield Classic", 3500.00, 50, "re_classic_silencer.png", "Exhaust"),
    
    # Placeholders (using existing images temporarily to ensure uniqueness in DB but speed for user)
    ("TVS Apache RTR Headlamp", "LED Headlamp assembly for TVS Apache RTR 200", 2200.00, 50, "hero_passion_meter.png", "Lighting"), 
    ("Honda Activa Shock Absorber", "Front suspension shock absorbers for Honda Activa", 850.00, 50, "bajaj_discover_carburetor.png", "Suspension"),
    ("Suzuki Access Drive Belt", "CVT transmission belt for Suzuki Access 125", 450.00, 50, "yamaha_fz_rear_disc.png", "Engine Parts"),
    ("KTM Duke Handlebar Grips", "Sporty rubber grips for KTM Duke series", 350.00, 50, "re_classic_silencer.png", "Accessories"),
    ("Hero Splendor Plus Seat", "Comfortable long seat for Hero Splendor Plus", 700.00, 50, "hero_passion_meter.png", "Body Parts"),
    ("Honda Dio Body Kit Blue", "Full fiber body kit set for Honda Dio", 4500.00, 50, "bajaj_discover_carburetor.png", "Body Parts")
]

def add_products():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Ensure categories exist
            categories = set(p[5] for p in products)
            for cat in categories:
                cursor.execute("SELECT category_id FROM categories WHERE name = %s", (cat,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (cat, f"Category for {cat}"))
                    print(f"Created category: {cat}")
            
            conn.commit()

            # Insert products
            for p in products:
                name, desc, price, stock, img, cat_name = p
                
                # Get category ID
                cursor.execute("SELECT category_id FROM categories WHERE name = %s", (cat_name,))
                cat_id = cursor.fetchone()[0]
                
                # Check if product exists
                cursor.execute("SELECT product_id FROM products WHERE name = %s", (name,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO products (name, description, price, stock_quantity, image_url, category_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (name, desc, price, stock, img, cat_id))
                    print(f"Added product: {name}")
                else:
                    print(f"Product already exists: {name}")

            conn.commit()
            cursor.close()
            conn.close()
            print("All 10 products processed successfully.")

    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_products()
