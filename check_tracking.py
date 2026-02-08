import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def check_tracking():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT order_id, status, tracking_number, courier_name FROM orders WHERE tracking_number IS NOT NULL OR courier_name IS NOT NULL")
            orders = cursor.fetchall()
            
            if orders:
                print(f"Found {len(orders)} orders with tracking info:")
                for order in orders:
                    print(order)
            else:
                print("No orders found with tracking information.")
                
            cursor.close()
            conn.close()

    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tracking()
