import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def migrate():
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # 1. Add transaction_id column if not exists
        print("Adding transaction_id column...")
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN transaction_id VARCHAR(50) AFTER payment_method")
            print(" - Added transaction_id column.")
        except Error as e:
            if "Duplicate column name" in str(e):
                print(" - transaction_id column already exists.")
            else:
                print(f" - Error adding transaction_id: {e}")

        # 2. Update payment_method enum
        print("Updating payment_method enum...")
        try:
            cursor.execute("ALTER TABLE orders MODIFY COLUMN payment_method ENUM('COD', 'UPI', 'Card') DEFAULT 'COD'")
            print(" - Updated payment_method enum.")
        except Error as e:
            print(f" - Error updating payment_method: {e}")

        conn.commit()
        print("\nMigration completed successfully!")
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    migrate()
