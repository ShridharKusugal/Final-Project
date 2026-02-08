
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
