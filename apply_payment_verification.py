"""
Apply payment verification schema updates to the database
"""
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def apply_migration():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print("Applying payment verification migration...")
        
        # 1. Modify status enum to include 'Payment Pending'
        print("1. Adding 'Payment Pending' status...")
        cursor.execute("""
            ALTER TABLE orders 
            MODIFY COLUMN status ENUM('Payment Pending', 'Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending'
        """)
        print("   [OK] Status enum updated")
        
        # 2. Add payment_screenshot column
        print("2. Adding payment_screenshot column...")
        try:
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN payment_screenshot VARCHAR(255) AFTER transaction_id
            """)
            print("   [OK] payment_screenshot column added")
        except Error as e:
            if e.errno == 1060:  # Duplicate column name
                print("   [SKIP] payment_screenshot column already exists")
            else:
                raise
        
        # 3. Add payment_verified_at column
        print("3. Adding payment_verified_at column...")
        try:
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN payment_verified_at DATETIME AFTER payment_screenshot
            """)
            print("   [OK] payment_verified_at column added")
        except Error as e:
            if e.errno == 1060:
                print("   [SKIP] payment_verified_at column already exists")
            else:
                raise
        
        # 4. Add payment_verified_by column
        print("4. Adding payment_verified_by column...")
        try:
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN payment_verified_by INT AFTER payment_verified_at
            """)
            print("   [OK] payment_verified_by column added")
        except Error as e:
            if e.errno == 1060:
                print("   [SKIP] payment_verified_by column already exists")
            else:
                raise
        
        conn.commit()
        print("\n[SUCCESS] Migration completed successfully!")
        
    except Error as e:
        print(f"\n[ERROR] Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    apply_migration()
