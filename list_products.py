
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def list_products():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT product_id, name, image_url FROM products")
            products = cursor.fetchall()
            print(f"Found {len(products)} products:")
            for p in products:
                print(f"ID: {p['product_id']}, Name: {p['name']}, Current Image: {p['image_url']}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    list_products()
