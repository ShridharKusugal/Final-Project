
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def update_user_schema():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            
            print("Checking users table schema...")
            
            # List of columns to check/add
            columns_to_add = [
                ("full_name", "VARCHAR(100)"),
                ("address_line1", "VARCHAR(255)"),
                ("address_line2", "VARCHAR(255)"),
                ("city", "VARCHAR(100)"),
                ("state", "VARCHAR(100)"),
                ("pincode", "VARCHAR(20)")
            ]
            
            for col_name, col_type in columns_to_add:
                cursor.execute(f"SHOW COLUMNS FROM users LIKE '{col_name}'")
                if not cursor.fetchone():
                    print(f"Adding '{col_name}' column...")
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type} DEFAULT NULL")
                else:
                    print(f"'{col_name}' already exists.")

            conn.commit()
            print("User schema updated successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    update_user_schema()
