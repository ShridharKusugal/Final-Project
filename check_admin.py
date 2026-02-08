import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def check_admin():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, email, role, password_hash FROM users WHERE role = 'admin' OR username = 'admin' OR email = 'admin@nkautomobiles.com'")
        users = cursor.fetchall()
        print(f"Found {len(users)} potential admin users:")
        for u in users:
            print(f"ID: {u['user_id']}, Username: {u['username']}, Email: {u['email']}, Role: {u['role']}")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_admin()
