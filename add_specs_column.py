import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def add_specs_column():
    print("Adding 'specifications' column to products table...")
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM products LIKE 'specifications'")
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("ALTER TABLE products ADD COLUMN specifications TEXT")
            conn.commit()
            print("SUCCESS: 'specifications' column added.")
        else:
            print("INFO: 'specifications' column already exists.")

        # Update existing products with dummy data if empty
        cursor.execute("SELECT product_id, name, category_id FROM products")
        products = cursor.fetchall()
        
        for p in products:
            pid = p[0]
            name = p[1]
            cat_id = p[2]
            
            # Dummy specs based on category
            specs = ""
            if cat_id == 1: # Engine
                specs = "Material: High-Grade Alloy\nWeight: 450g\nWarranty: 6 Months\nCompatibility: Standard Models"
            elif cat_id == 2: # Brake
                specs = "Material: Ceramic Composite\nPosition: Front/Rear\nDurability: High Heat Resistance"
            elif cat_id == 3: # Electrical
                specs = "Voltage: 12V\nPower: 35W/55W\nLifespan: 20000 Hours"
            else:
                specs = "Material: Standard\nWarranty: Manufacturer Warranty\nFitment: Universal"
                
            cursor.execute("UPDATE products SET specifications = %s WHERE product_id = %s AND (specifications IS NULL OR specifications = '')", (specs, pid))
        
        conn.commit()
        print("SUCCESS: Existing products updated with sample specifications.")

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    add_specs_column()
