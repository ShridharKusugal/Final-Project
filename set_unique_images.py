
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def set_unique_filenames():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT product_id, name FROM products")
            products = cursor.fetchall()

            for p in products:
                # Generate filename like 'honda_shine_piston_kit.png'
                safe_name = "".join([c if c.isalnum() else "_" for c in p['name']]).lower()
                filename = f"{safe_name}.png"
                
                # Update DB
                update_query = "UPDATE products SET image_url = %s WHERE product_id = %s"
                cursor.execute(update_query, (filename, p['product_id']))
                print(f"Updated {p['name']} -> {filename}")

            conn.commit()
            print("Database updated with unique filenames.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    set_unique_filenames()
