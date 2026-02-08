
import mysql.connector
from mysql.connector import Error

# Configuration WITHOUT database initially
db_config_no_db = {
    'host': 'localhost',
    'user': 'NK_Auto',
    'password': 'Shri@2004'
}

print("1. Attempting to connect to MySQL Server (no specific DB)...")
try:
    conn = mysql.connector.connect(**db_config_no_db)
    if conn.is_connected():
        print("   SUCCESS: Connected to MySQL server.")
        cursor = conn.cursor()
        
        print("\n2. Checking existing databases...")
        try:
            cursor.execute("SHOW DATABASES")
            dbs = [d[0] for d in cursor.fetchall()]
            print(f"   Databases found: {dbs}")
            
            target_db = 'nk_automobiles'
            if target_db in dbs:
                print(f"\n3. Database '{target_db}' exists. Attempting to select it...")
                try:
                    conn.database = target_db
                    print(f"   SUCCESS: Selected '{target_db}'.")
                except Error as e:
                    print(f"   FAILED: Could not select '{target_db}'. Error: {e}")
            else:
                print(f"\n3. Database '{target_db}' does NOT exist. Attempting to create it...")
                try:
                    cursor.execute(f"CREATE DATABASE {target_db}")
                    print(f"   SUCCESS: Database '{target_db}' created.")
                except Error as e:
                    print(f"   FAILED: Could not create database. Error: {e}")
                    
        except Error as e:
            print(f"   Failed to list/manage databases: {e}")
            
        conn.close()
except Error as e:
    print(f"FAILED: Could not connect to MySQL server. Error: {e}")
