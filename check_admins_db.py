import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def check_admins():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, email, role FROM users WHERE role = 'admin'")
        admins = cursor.fetchall()
        print("Admins found:")
        for admin in admins:
            print(f"- Username: {admin['username']}, Email: {admin['email']}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_admins()
