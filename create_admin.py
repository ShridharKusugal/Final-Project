import mysql.connector
from werkzeug.security import generate_password_hash
from app import db_config

def create_admin():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Admin details
        username = "admin"
        email = "admin@nkautomobiles.com"
        password = "admin123"
        hashed_password = generate_password_hash(password)
        
        # Check if admin already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            print("Admin user already exists.")
        else:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, 'admin')
            """, (username, email, hashed_password))
            conn.commit()
            print(f"Admin user created successfully.\nEmail: {email}\nPassword: {password}")
            
            # Print the INSERT statement for database.sql
            print("\n--- SQL Statement for database.sql ---")
            print(f"INSERT INTO users (username, email, password_hash, role) VALUES ('{username}', '{email}', '{hashed_password}', 'admin');")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_admin()
