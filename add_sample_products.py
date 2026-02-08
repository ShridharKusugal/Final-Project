import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def add_products():
    products = [
        ('Performance Clutch Plate Set', 'High-performance clutch plates for 150cc+ bikes', 1450.00, 45, 1, 'BrandX', 'default.jpg'),
        ('LED Fog Light Kit', 'Dual LED Fog Lights with wiring harness and switch', 3200.00, 20, 3, 'Lumax', 'default.jpg'),
        ('Stainless Steel Exhaust System', 'Full system exhaust for performance and sound', 7500.00, 5, 1, 'Akrapovic Style', 'default.jpg'),
        ('Digital Instrument Cluster', 'Universal digital speedometer/tachometer', 4200.00, 15, 3, 'Koso', 'default.jpg'),
        ('Premium Seat Cover', 'Waterproof anti-slip seat cover for comfort', 650.00, 80, 7, 'Autoform', 'default.jpg'),
        ('Disc Brake Rotor 300mm', 'Large diameter disc rotor for better stopping power', 2800.00, 12, 2, 'Brembo Style', 'default.jpg'),
        ('High-Flow Oil Filter', 'Synthetic media oil filter for better engine life', 450.00, 150, 6, 'K&N', 'default.jpg'),
        ('Adjustable Brake/Clutch Levers', 'CNC machined 6-way adjustable levers', 1200.00, 35, 7, 'Rizoma', 'default.jpg'),
        ('Heavy Duty Drive Chain', 'O-ring gold chain for durability', 3800.00, 18, 5, 'DID', 'default.jpg'),
        ('Side Box Luggage Set', 'Hard shell side boxes with mounting brackets', 5500.00, 8, 7, 'Studds', 'default.jpg')
    ]

    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            query = """INSERT INTO products (name, description, price, stock_quantity, category_id, brand, image_url) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(query, products)
            conn.commit()
            print(f"Successfully added {cursor.rowcount} products.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    add_products()
