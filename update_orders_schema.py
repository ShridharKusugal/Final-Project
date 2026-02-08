import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def add_tracking_columns():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Check if columns exist
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'tracking_number'")
            if not cursor.fetchone():
                print("Adding tracking_number column...")
                cursor.execute("ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100) DEFAULT NULL")
            else:
                print("tracking_number column already exists.")

            cursor.execute("SHOW COLUMNS FROM orders LIKE 'courier_name'")
            if not cursor.fetchone():
                print("Adding courier_name column...")
                cursor.execute("ALTER TABLE orders ADD COLUMN courier_name VARCHAR(100) DEFAULT NULL")
            else:
                print("courier_name column already exists.")
            
            conn.commit()
            print("Schema updated successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    add_tracking_columns()
