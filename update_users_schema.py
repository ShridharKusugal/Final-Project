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
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Check if columns exist
            cursor.execute("SHOW COLUMNS FROM users LIKE 'reset_token'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(100) DEFAULT NULL")
                print("Added reset_token column.")
            else:
                print("reset_token column already exists.")

            cursor.execute("SHOW COLUMNS FROM users LIKE 'reset_token_expiry'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME DEFAULT NULL")
                print("Added reset_token_expiry column.")
            else:
                print("reset_token_expiry column already exists.")

            conn.commit()
            cursor.close()
            conn.close()
            print("Database schema updated successfully.")

    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_schema()
