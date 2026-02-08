import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def apply_changes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product_id INT,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
        """)
        print("Reviews table created or already exists.")

        # Create review_media table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_media (
                media_id INT AUTO_INCREMENT PRIMARY KEY,
                review_id INT,
                media_url VARCHAR(255) NOT NULL,
                media_type ENUM('image', 'video') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (review_id) REFERENCES reviews(review_id) ON DELETE CASCADE
            )
        """)
        print("Review_media table created or already exists.")
        
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    apply_changes()
