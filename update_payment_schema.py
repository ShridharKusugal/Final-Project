import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def update_schema():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn:
            cursor = conn.cursor()
            # Check if columns exist before adding (or just use try-catch for simplicity in this script)
            try:
                print("Adding payment_method column...")
                cursor.execute("ALTER TABLE orders MODIFY COLUMN payment_method ENUM('COD', 'UPI', 'Card') DEFAULT 'COD'")
            except Error as e:
                print(f"Column payment_method might already exist or error: {e}")

            try:
                print("Adding transaction_id column...")
                cursor.execute("ALTER TABLE orders ADD COLUMN transaction_id VARCHAR(100) AFTER payment_method")
            except Error as e:
                 print(f"Column transaction_id might already exist or error: {e}")
            
            conn.commit()
            print("Database schema updated successfully.")
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Database connection error: {e}")

if __name__ == '__main__':
    update_schema()
