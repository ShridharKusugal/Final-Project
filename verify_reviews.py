import mysql.connector
from mysql.connector import Error
import os

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

def verify_reviews():
    print("Verifying Review System...")
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # 1. Get a user and a product
        cursor.execute("SELECT user_id FROM users LIMIT 1")
        user = cursor.fetchone()
        cursor.execute("SELECT product_id FROM products LIMIT 1")
        product = cursor.fetchone()
        
        if not user or not product:
            print("Skipping verification: Need at least one user and one product.")
            return

        user_id = user['user_id']
        product_id = product['product_id']
        print(f"Using User ID: {user_id}, Product ID: {product_id}")

        # 2. Insert a Test Review
        print("Inserting test review...")
        cursor.execute("""
            INSERT INTO reviews (user_id, product_id, rating, comment)
            VALUES (%s, %s, %s, %s)
        """, (user_id, product_id, 5, "This is a test review from verification script."))
        review_id = cursor.lastrowid
        print(f"Review inserted with ID: {review_id}")

        # 3. Insert Test Media
        print("Inserting test media...")
        cursor.execute("""
            INSERT INTO review_media (review_id, media_url, media_type)
            VALUES (%s, %s, %s)
        """, (review_id, "test_image.jpg", "image"))
        print("Media inserted.")
        
        conn.commit()

        # 4. Fetch and Verify
        print("Fetching reviews for product...")
        cursor.execute("""
            SELECT r.*, u.username 
            FROM reviews r 
            JOIN users u ON r.user_id = u.user_id 
            WHERE r.product_id = %s AND r.review_id = %s
        """, (product_id, review_id))
        fetched_review = cursor.fetchone()
        
        if fetched_review:
            print(f"SUCCESS: Review found! Rating: {fetched_review['rating']}, Comment: {fetched_review['comment']}")
            
            cursor.execute("SELECT * FROM review_media WHERE review_id = %s", (review_id,))
            media = cursor.fetchall()
            print(f"SUCCESS: Found {len(media)} media items attached.")
        else:
            print("FAILURE: Review not found after insertion.")

        # Cleanup (Optional: remove the test review to keep DB clean)
        # cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
        # conn.commit()
        # print("Cleanup: Test review deleted.")

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    verify_reviews()
