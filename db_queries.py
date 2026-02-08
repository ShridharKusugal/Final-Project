import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print("Database connection error:", e)
        return None

# ==========================
# PRODUCT QUERIES
# ==========================
def get_all_products(limit=None):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM products"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_products_by_category(category_id=None):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    if category_id:
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
    else:
        cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_related_products(category_id, current_product_id, limit=10):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    
    # 1. Try to get products from same category
    cursor.execute("""
        SELECT * FROM products 
        WHERE category_id = %s AND product_id != %s 
        LIMIT %s
    """, (category_id, current_product_id, limit))
    related = cursor.fetchall()
    
    # 2. If not enough, fill with other random products
    if len(related) < limit:
        needed = limit - len(related)
        exclude_ids = [current_product_id] + [p['product_id'] for p in related]
        format_strings = ','.join(['%s'] * len(exclude_ids))
        
        cursor.execute(f"""
            SELECT * FROM products 
            WHERE product_id NOT IN ({format_strings}) 
            ORDER BY RAND() 
            LIMIT %s
        """, (*exclude_ids, needed))
        
        others = cursor.fetchall()
        related.extend(others)
        
    cursor.close()
    conn.close()
    return related

def get_categories():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories


def get_filtered_products(category_id=None, brands=None, min_price=None, max_price=None, sort_by=None):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if category_id:
        query += " AND category_id = %s"
        params.append(category_id)
        
    if brands:
        if isinstance(brands, list):
            placeholders = ', '.join(['%s'] * len(brands))
            query += f" AND brand IN ({placeholders})"
            params.extend(brands)
        else:
            query += " AND brand = %s"
            params.append(brands)
            
    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)
        
    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)

    # Sorting logic
    if sort_by == 'price_low':
        query += " ORDER BY price ASC"
    elif sort_by == 'price_high':
        query += " ORDER BY price DESC"
    elif sort_by == 'newest':
        query += " ORDER BY product_id DESC"
    else:
        query += " ORDER BY product_id DESC" # Default newest
        
    cursor.execute(query, tuple(params))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_all_brands():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL AND brand != '' ORDER BY brand")
    brands = [row['brand'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return brands

def get_price_range():
    conn = get_db_connection()
    if not conn: return 0, 100000
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(price), MAX(price) FROM products")
    result = cursor.fetchone()
    min_p = result[0] if result[0] is not None else 0
    # Set a reasonable default max if database max is low, to allow broader filtering
    db_max = result[1] if result[1] is not None else 0
    max_p = max(float(db_max), 10000.0) # Ensure at least 10000 for a better UI range
    
    # Round to nearest 1000 for cleaner UI
    import math
    max_p = math.ceil(max_p / 1000) * 1000
    
    cursor.close()
    conn.close()
    return min_p, max_p

# ==========================
# END FILTER QUERIES
# ==========================

def get_product_details(product_id):
    conn = get_db_connection()
    if not conn: return None, [], 0, 0
    
    cursor = conn.cursor(dictionary=True)
    
    # 1. Product
    cursor.execute("""
        SELECT p.*, c.name AS category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = %s
    """, (product_id,))
    product = cursor.fetchone()
    
    reviews = []
    avg_rating = 0
    review_count = 0
    
    if product:
        # 2. Reviews
        cursor.execute("""
            SELECT r.*, u.username 
            FROM reviews r 
            JOIN users u ON r.user_id = u.user_id 
            WHERE r.product_id = %s 
            ORDER BY r.created_at DESC
        """, (product_id,))
        reviews = cursor.fetchall()
        
        # 3. Stats
        cursor.execute("SELECT AVG(rating) as avg, COUNT(*) as count FROM reviews WHERE product_id = %s", (product_id,))
        stats = cursor.fetchone()
        if stats and stats['avg']:
            avg_rating = round(float(stats['avg']), 1)
            review_count = stats['count']
            
        # 4. Media
        if reviews:
            review_ids = [r['review_id'] for r in reviews]
            format_strings = ','.join(['%s'] * len(review_ids))
            cursor.execute(f"SELECT * FROM review_media WHERE review_id IN ({format_strings})", tuple(review_ids))
            all_media = cursor.fetchall()
            
            media_map = {}
            for m in all_media:
                if m['review_id'] not in media_map:
                    media_map[m['review_id']] = []
                media_map[m['review_id']].append(m)
            
            for r in reviews:
                r['media'] = media_map.get(r['review_id'], [])
                
        # Parse Specs
        specs_dict = {}
        if product.get('specifications'):
            try:
                for line in product['specifications'].split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        specs_dict[key.strip()] = value.strip()
            except: pass
        product['specs_parsed'] = specs_dict

    cursor.close()
    conn.close()
    return product, reviews, avg_rating, review_count

# ==========================
# CART QUERIES
# ==========================
def get_cart_count(user_id):
    conn = get_db_connection()
    if not conn: return 0
    cursor = conn.cursor(dictionary=True)
    count = 0
    try:
        cursor.execute("SELECT SUM(quantity) as count FROM cart WHERE user_id = %s", (user_id,))
        res = cursor.fetchone()
        if res and res['count']: count = int(res['count'])
    except: pass
    cursor.close()
    conn.close()
    return count

def get_cart_items(user_id):
    conn = get_db_connection()
    if not conn: return [], 0
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.cart_id, c.quantity, c.product_id, p.name, p.price, p.image_url, (p.price * c.quantity) as total_price
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()
    total = sum(item['total_price'] for item in items)
    cursor.close()
    conn.close()
    return items, total

def add_to_cart_db(user_id, product_id, quantity):
    conn = get_db_connection()
    if not conn: return False, "Database error"
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, stock_quantity FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product: return False, "Product not found"
        
        if product['stock_quantity'] < quantity:
            return False, f"Only {product['stock_quantity']} units available."
            
        cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        existing = cursor.fetchone()
        
        if existing:
            new_qty = existing['quantity'] + quantity
            if new_qty > product['stock_quantity']:
                return False, f"Max limit reached. You have {existing['quantity']} in cart."
            cursor.execute("UPDATE cart SET quantity = %s WHERE cart_id = %s", (new_qty, existing['cart_id']))
        else:
            cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, quantity))
            
        conn.commit()
        return True, "Item added to cart"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def clear_cart(user_id):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def remove_from_cart(user_id, product_id):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        conn.commit()
        return True, "Item removed from cart"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_cart_quantity(user_id, product_id, quantity):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        if quantity <= 0:
            return remove_from_cart(user_id, product_id)
            
        cursor.execute("SELECT stock_quantity FROM products WHERE product_id = %s", (product_id,))
        res = cursor.fetchone()
        if not res: return False, "Product not found"
        stock = res[0]
        
        if quantity > stock:
            return False, f"Only {stock} units available"
            
        cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s", (quantity, user_id, product_id))
        conn.commit()
        return True, "Quantity updated"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# ==========================
# ORDER QUERIES
# ==========================
def get_order_for_tracking(order_id, email_or_phone):
    conn = get_db_connection()
    if not conn: return None, "Connection error"
    cursor = conn.cursor(dictionary=True)
    
    # Try creating a generic search logic
    # The email_or_phone could match either the user's email or the order's phone number
    # We join with users table to check email
    
    query = """
        SELECT o.*, u.email as user_email
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.order_id = %s 
        AND (
            LOWER(u.email) = LOWER(%s) 
            OR o.phone_number = %s 
            OR u.phone = %s
        )
    """
    
    cursor.execute(query, (order_id, email_or_phone, email_or_phone, email_or_phone))
    order = cursor.fetchone()
    
    items = []
    if order:
        cursor.execute("""
            SELECT oi.*, p.name 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.product_id 
            WHERE oi.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()
        
    cursor.close()
    conn.close()
    return order, items

def create_order(user_id, order_data):
    conn = get_db_connection()
    if not conn: return None, "Connection error"
    cursor = conn.cursor(dictionary=True)
    try:
        # Get Cart
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.price 
            FROM cart c JOIN products p ON c.product_id = p.product_id 
            WHERE c.user_id = %s
        """, (user_id,))
        items = cursor.fetchall()
        if not items: return None, "Cart empty"
        
        cart_total = sum(i['price'] * i['quantity'] for i in items)
        final_total = cart_total
        discount_amount = 0.0
        applied_coupon_id = None
        
        # Validate Coupon AGAIN server-side
        coupon_code = order_data.get('applied_coupon')
        if coupon_code:
            cursor.execute("""
                SELECT * FROM coupons 
                WHERE code = %s 
                AND (valid_from IS NULL OR valid_from <= NOW())
                AND (valid_until IS NULL OR valid_until >= NOW())
                AND (usage_limit IS NULL OR used_count < usage_limit)
                AND min_purchase <= %s
            """, (coupon_code, cart_total))
            coupon = cursor.fetchone()
            if coupon:
                applied_coupon_id = coupon['coupon_id']
                if coupon['discount_type'] == 'percentage':
                    discount_amount = (cart_total * float(coupon['discount_value'])) / 100
                else:
                    discount_amount = float(coupon['discount_value'])
                final_total = cart_total - discount_amount
        
        # Determine order status based on payment method
        order_status = 'Payment Pending' if order_data.get('payment_method') in ['UPI', 'UPI_QR'] else 'Pending'
        
        cursor.execute("""
            INSERT INTO orders (user_id, full_name, phone_number, address_line1, address_line2, city, state, pincode, total_amount, payment_method, transaction_id, status, discount_amount, coupon_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, order_data['full_name'], order_data['phone'], order_data['addr1'], order_data['addr2'], order_data['city'], order_data['state'], order_data['pincode'], final_total, order_data.get('payment_method', 'COD'), order_data.get('transaction_id', ''), order_status, discount_amount, applied_coupon_id))
        order_id = cursor.lastrowid
        
        # Track Coupon Usage
        if applied_coupon_id:
            cursor.execute("UPDATE coupons SET used_count = used_count + 1 WHERE coupon_id = %s", (applied_coupon_id,))
        
        for item in items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", (order_id, item['product_id'], item['quantity'], item['price']))
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s", (item['quantity'], item['product_id']))
            
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        conn.commit()
        return order_id, "Success"
    except Error as e:
        conn.rollback()
        return None, str(e)
    finally:
        cursor.close()
        conn.close()


def is_transaction_id_used(transaction_id):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM orders WHERE transaction_id = %s LIMIT 1", (transaction_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_order_details(order_id, user_id=None):
    conn = get_db_connection()
    if not conn: return None, []
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM orders WHERE order_id = %s"
    params = [order_id]
    if user_id:
        query += " AND user_id = %s"
        params.append(user_id)
        
    cursor.execute(query, tuple(params))
    order = cursor.fetchone()
    
    items = []
    if order:
        cursor.execute("""
            SELECT oi.*, p.name, p.image_url 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.product_id 
            WHERE oi.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()
        
    cursor.close()
    conn.close()
    return order, items

# ==========================
# USER QUERIES
# ==========================
def get_user_by_email(email):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def create_user(username, email, password_hash):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, 'customer')", (username, email, password_hash))
        conn.commit()
        return True, "Success"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_orders(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM orders 
        WHERE user_id = %s 
        ORDER BY created_at DESC
    """, (user_id,))
    orders = cursor.fetchall()
    
    # Fetch items for each order
    for order in orders:
        cursor.execute("""
            SELECT oi.quantity, p.name, p.image_url 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.product_id 
            WHERE oi.order_id = %s
        """, (order['order_id'],))
        order['order_items'] = cursor.fetchall()
        
    cursor.close()
    conn.close()
    return orders

def update_user_profile(user_id, data):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users 
            SET full_name = %s, phone = %s, address_line1 = %s, address_line2 = %s, 
                city = %s, state = %s, pincode = %s
            WHERE user_id = %s
        """, (data['full_name'], data['phone'], data['address_line1'], data['address_line2'], 
              data['city'], data['state'], data['pincode'], user_id))
        conn.commit()
        return True, "Profile updated successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# ==========================
# ADMIN QUERIES (Partial)
# ==========================
def get_dashboard_stats():
    conn = get_db_connection()
    if not conn: return {}
    cursor = conn.cursor(dictionary=True)
    stats = {}
    
    # 1. Basic counts
    cursor.execute("SELECT COUNT(*) as c FROM products")
    stats['products'] = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM users")
    stats['users'] = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM orders")
    stats['orders'] = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM products WHERE stock_quantity < 10")
    stats['low_stock'] = cursor.fetchone()['c']
    
    # 2. Revenue stats (Excluding Cancelled orders)
    cursor.execute("SELECT SUM(total_amount) as total FROM orders WHERE status != 'Cancelled'")
    res = cursor.fetchone()
    stats['total_revenue'] = float(res['total']) if res['total'] else 0.0
    
    # 3. Monthly Sales
    cursor.execute("""
        SELECT SUM(total_amount) as total 
        FROM orders 
        WHERE status != 'Cancelled' 
        AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    """)
    res_month = cursor.fetchone()
    stats['monthly_revenue'] = float(res_month['total']) if res_month['total'] else 0.0
    
    # 4. Monthly Growth (Simplistic comparison)
    cursor.execute("""
        SELECT SUM(total_amount) as total 
        FROM orders 
        WHERE status != 'Cancelled' 
        AND created_at >= DATE_SUB(NOW(), INTERVAL 60 DAY)
        AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY)
    """)
    prev_month = cursor.fetchone()
    prev_total = float(prev_month['total']) if prev_month['total'] else 0.0
    
    if prev_total > 0:
        stats['growth'] = round(((stats['monthly_revenue'] - prev_total) / prev_total) * 100, 1)
    else:
        stats['growth'] = 100 if stats['monthly_revenue'] > 0 else 0

    # 5. Daily Sales Trend (Last 14 Days)
    cursor.execute("""
        SELECT DATE(created_at) as date, SUM(total_amount) as total
        FROM orders
        WHERE status != 'Cancelled'
        AND created_at >= DATE_SUB(NOW(), INTERVAL 14 DAY)
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """)
    trend_data = cursor.fetchall()
    stats['sales_trend'] = [{'date': d['date'].strftime('%d %b'), 'total': float(d['total'])} for d in trend_data]

    cursor.close()
    conn.close()
    return stats

def get_recent_products(limit=5):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.product_id DESC LIMIT %s
    """, (limit,))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

# ==========================
# REVIEWS QUERIES
# ==========================

def get_all_reviews_admin():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, u.username, u.email, p.name as product_name
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        JOIN products p ON r.product_id = p.product_id
        ORDER BY r.created_at DESC
    """)
    reviews = cursor.fetchall()
    
    # Get media for each review
    for r in reviews:
        cursor.execute("SELECT * FROM review_media WHERE review_id = %s", (r['review_id'],))
        r['media'] = cursor.fetchall()
        
    cursor.close()
    conn.close()
    return reviews

def delete_review(review_id):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        # Related media will be deleted automatically due to ON DELETE CASCADE
        cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
        conn.commit()
        return True, "Review deleted successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# ==========================
# COUPON QUERIES
# ==========================

def get_all_coupons():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coupons ORDER BY created_at DESC")
    coupons = cursor.fetchall()
    cursor.close()
    conn.close()
    return coupons

def add_coupon(data):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO coupons (code, discount_value, discount_type, min_purchase, valid_from, valid_until, usage_limit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['code'], data['discount_value'], data['discount_type'], data['min_purchase'], data['valid_from'], data['valid_until'], data['usage_limit']))
        conn.commit()
        return True, "Coupon created successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_coupon(coupon_id):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM coupons WHERE coupon_id = %s", (coupon_id,))
        conn.commit()
        return True, "Coupon deleted"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def validate_coupon(code, cart_total):
    conn = get_db_connection()
    if not conn: return None, "Database error"
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM coupons 
            WHERE code = %s 
            AND (valid_from IS NULL OR valid_from <= NOW())
            AND (valid_until IS NULL OR valid_until >= NOW())
            AND (usage_limit IS NULL OR used_count < usage_limit)
        """, (code,))
        coupon = cursor.fetchone()
        
        if not coupon:
            return None, "Invalid or expired coupon code"
            
        if cart_total < float(coupon['min_purchase']):
            return None, f"Minimum purchase of ₹{coupon['min_purchase']} required for this coupon"
            
        return coupon, "Coupon applied!"
    finally:
        cursor.close()
        conn.close()

# ==========================
# ADMIN CATEGORY QUERIES
# ==========================

def get_categories_with_stats():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, COUNT(p.product_id) as product_count
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        GROUP BY c.category_id
    """)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def add_category(name, description):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        return True, "Category added successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_category(category_id, name, description):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE categories SET name=%s, description=%s WHERE category_id=%s", (name, description, category_id))
        conn.commit()
        return True, "Category updated successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_category(category_id):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        # Check if products exist in category
        cursor.execute("SELECT COUNT(*) as c FROM products WHERE category_id = %s", (category_id,))
        if cursor.fetchone()[0] > 0:
            return False, "Cannot delete category with existing products."
        
        cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
        conn.commit()
        return True, "Category deleted successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# ==========================
# ADMIN CRUD QUERIES
# ==========================

def get_admin_products():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.product_id DESC
    """)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_low_stock_products():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.stock_quantity < 10
        ORDER BY p.stock_quantity ASC
    """)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def search_admin_products(query):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.name LIKE %s OR p.brand LIKE %s
        ORDER BY p.product_id DESC
    """, (search_term, search_term))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def add_product(data):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (name, brand, category_id, price, stock_quantity, description, specifications, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['name'], data['brand'], data['category_id'], data['price'], data['stock_quantity'], data['description'], data['specifications'], data['image_url']))
        conn.commit()
        return True, "Product added successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_product(product_id, data):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE products SET name=%s, brand=%s, category_id=%s, price=%s, 
            stock_quantity=%s, description=%s, specifications=%s, image_url=%s WHERE product_id=%s
        """, (data['name'], data['brand'], data['category_id'], data['price'], data['stock_quantity'], data['description'], data['specifications'], data['image_url'], product_id))
        conn.commit()
        return True, "Product updated successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()
        return True, "Product deleted successfully"
    except Error as e:
        return False, str(e)
    return True, "Product deleted successfully"

def set_reset_token(email, token, expiry):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE email = %s", (token, expiry, email))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_user_by_reset_token(token):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE reset_token = %s AND reset_token_expiry > NOW()", (token,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_password(user_id, password_hash):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = %s, reset_token = NULL, reset_token_expiry = NULL WHERE user_id = %s", (password_hash, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_all_orders():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, u.username, u.email 
        FROM orders o 
        JOIN users u ON o.user_id = u.user_id 
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

def update_order_status(order_id, status):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, order_id))
        conn.commit()
        return True, "Status updated"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_order_tracking(order_id, status, tracking_number, courier_name):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE orders 
            SET status = %s, tracking_number = %s, courier_name = %s 
            WHERE order_id = %s
        """, (status, tracking_number, courier_name, order_id))
        conn.commit()
        return True, "Order updated successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def get_all_users():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def toggle_wishlist(user_id, product_id):
    conn = get_db_connection()
    if not conn: return False, "Database error"
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        if cursor.fetchone():
            cursor.execute("DELETE FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            conn.commit()
            return True, "Removed from wishlist"
        else:
            cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
            conn.commit()
            return True, "Added to wishlist"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_wishlist_items(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT w.wishlist_id, p.*, c.name as category_name
        FROM wishlist w
        JOIN products p ON w.product_id = p.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE w.user_id = %s
        ORDER BY w.added_at DESC
    """, (user_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def is_in_wishlist(user_id, product_id):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# ==========================
# SYSTEM LOGS
# ==========================

def add_log(log_type, user_id=None, recipient=None, subject=None, content=None):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO system_logs (type, user_id, recipient, subject, content)
            VALUES (%s, %s, %s, %s, %s)
        """, (log_type, user_id, recipient, subject, content))
        conn.commit()
    except Error as e:
        print(f"Failed to write log: {e}")
    finally:
        cursor.close()
        conn.close()

def get_system_logs(log_type=None, limit=100):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT l.*, u.username FROM system_logs l LEFT JOIN users u ON l.user_id = u.user_id"
    params = []
    
    if log_type:
        query += " WHERE l.type = %s"
        params.append(log_type)
        
    query += " ORDER BY l.created_at DESC LIMIT %s"
    params.append(limit)
    
    cursor.execute(query, tuple(params))
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs

# ==========================
# CONTACT QUERIES
# ==========================

def add_contact_message(data):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contact_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)", (data['name'], data['email'], data['subject'], data['message']))
        conn.commit()
        return True, "Message sent successfully"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_contact_messages(limit=50):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT %s", (limit,))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages

def update_contact_status(message_id, status):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE contact_messages SET status = %s WHERE message_id = %s", (status, message_id))
        conn.commit()
        return True, "Status updated"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_contact_message(message_id):
    conn = get_db_connection()
    if not conn: return False, "Connection error"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM contact_messages WHERE message_id = %s", (message_id,))
        conn.commit()
        return True, "Message deleted"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()
