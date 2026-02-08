import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def reset_admin_password():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        new_password = "admin123"
        hashed_password = generate_password_hash(new_password)
        
        cursor.execute("UPDATE users SET password_hash = %s WHERE email = 'admin@nkautomobiles.com'", (hashed_password,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Successfully reset password for admin@nkautomobiles.com to '{new_password}'")
        else:
            print("Admin user not found or password already matches.")
            
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_admin_password()
