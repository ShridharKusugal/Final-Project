import mysql.connector
from werkzeug.security import check_password_hash

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def verify_admin_password():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password_hash FROM users WHERE email = 'admin@nkautomobiles.com'")
        user = cursor.fetchone()
        if user:
            hash = user['password_hash']
            if check_password_hash(hash, 'admin123'):
                print("Password 'admin123' is CORRECT for admin@nkautomobiles.com")
            else:
                print("Password 'admin123' is INCORRECT.")
        else:
            print("Admin user not found.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_admin_password()
