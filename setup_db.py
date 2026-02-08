
import mysql.connector
from mysql.connector import Error
import sys
import os

# Configuration 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles' # Try connecting to DB directly now as we know it's created
}

print("1. Connecting to 'nk_automobiles' database...")
try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("   SUCCESS: Connected to database.")
        cursor = conn.cursor()
        
        print("\n2. Checking existing tables...")
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"   Tables found: {tables}")
        
        if len(tables) < 5: # Arbitrary check, if few tables, we import
            print("\n3. Importing Schema from database.sql...")
            if os.path.exists('database.sql'):
                try:
                    with open('database.sql', 'r') as f:
                        sql_content = f.read()
                    
                    # Split commands by semicolon
                    commands = sql_content.split(';')
                    
                    success_count = 0
                    for cmd in commands:
                        cmd_strip = cmd.strip()
                        if cmd_strip:
                            try:
                                cursor.execute(cmd_strip)
                                success_count += 1
                            except Error as e_cmd:
                                # Start a new transaction/continue? 
                                # Some errors like "User already exists" or "Duplicate entry" might effectively be ignored for "IF NOT EXISTS" Logic
                                # But `database.sql` has `IF NOT EXISTS` for tables, but not for INSERTs mostly.
                                if "Duplicate entry" in str(e_cmd) or "already exists" in str(e_cmd):
                                    print(f"      [Info] Skipped (Duplicate/Exists): {cmd_strip[:50]}...")
                                else:
                                    print(f"      [Error] Failed to execute: {cmd_strip[:50]}... Error: {e_cmd}")
                    
                    conn.commit()
                    print(f"   SUCCESS: Executed {success_count} commands.")
                except Exception as e_file:
                    print(f"   FAILED to read/process file: {e_file}")
            else:
                print("   FAILED: database.sql file not found.")
        else:
            print("   Database seems populated. Skipping import.")

        cursor.close()
        conn.close()
except Error as e:
    print(f"FAILED: Connection error: {e}")
