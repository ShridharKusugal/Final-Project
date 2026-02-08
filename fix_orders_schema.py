
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def fix_orders_schema():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            
            print("Checking orders table schema...")
            
            # Check for transaction_id
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'transaction_id'")
            if not cursor.fetchone():
                print("Adding 'transaction_id' column...")
                cursor.execute("ALTER TABLE orders ADD COLUMN transaction_id VARCHAR(100) DEFAULT NULL")
            else:
                print("'transaction_id' already exists.")

            # Check for tracking_number (just in case)
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'tracking_number'")
            if not cursor.fetchone():
                print("Adding 'tracking_number' column...")
                cursor.execute("ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100) DEFAULT NULL")
            
            # Check for courier_name
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'courier_name'")
            if not cursor.fetchone():
                print("Adding 'courier_name' column...")
                cursor.execute("ALTER TABLE orders ADD COLUMN courier_name VARCHAR(100) DEFAULT NULL")

            conn.commit()
            print("Schema update completed successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fix_orders_schema()
