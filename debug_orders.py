import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def list_orders():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT o.order_id, o.phone_number, u.email, u.username 
                FROM orders o 
                JOIN users u ON o.user_id = u.user_id
            """)
            orders = cursor.fetchall()
            print(f"Found {len(orders)} orders:")
            for order in orders:
                print(order)
                
            cursor.close()
            conn.close()

    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_orders()
