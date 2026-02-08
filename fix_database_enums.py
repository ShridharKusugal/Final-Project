import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Shri@2004',
            database='nk_automobiles'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def fix_enums():
    conn = get_db_connection()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        try:
            print("Updating `payment_method` ENUM...")
            # We add 'UPI_QR' and also 'Razorpay' just in case, to be safe and compatible with previous data if any
            cursor.execute("ALTER TABLE orders MODIFY COLUMN payment_method ENUM('COD', 'UPI', 'Card', 'Razorpay', 'UPI_QR') DEFAULT 'COD'")
            print("Successfully updated `payment_method` column.")

            print("Updating `status` ENUM...")
            # We add 'Payment Pending' to the status enum
            cursor.execute("ALTER TABLE orders MODIFY COLUMN status ENUM('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled', 'Payment Pending') DEFAULT 'Pending'")
            print("Successfully updated `status` column.")
            
            conn.commit()
            print("All database updates committed successfully.")
            
        except Error as e:
            print(f"Error updating database: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fix_enums()
