
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def update_images():
    commands = [
        "UPDATE products SET image_url = 'splendor_air_filter.png' WHERE name LIKE '%Splendor Air Filter%'",
        # For others, we keep default.jpg or could update if we had valid images.
        # "UPDATE products SET image_url = 'honda_shine_piston.jpg' WHERE name LIKE '%Honda Shine Piston%'"
    ]

    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            for command in commands:
                cursor.execute(command)
            conn.commit()
            print("Images updated successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    update_images()
