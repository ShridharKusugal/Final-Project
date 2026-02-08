
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

# Map Product Name (or part of it) to Filename
image_mapping = {
    'Honda Shine Piston Kit': 'honda_shine_piston_kit.png',
    'Bajaj Pulsar Brake Pads': 'bajaj_pulsar_brake_pads.png',
    'TVS Jupiter Battery': 'tvs_jupiter_battery.png',
    'Yamaha R15 Chain Sprocket Kit': 'yamaha_r15_chain_sprocket_kit.png',
    'Hero Splendor Air Filter': 'hero_splendor_air_filter.png',
    'Royal Enfield Leg Guard': 'royal_enfield_leg_guard.png',
    'Activa 6G Headlight Assembly': 'activa_6g_headlight_assembly.png',
    'ktm Duke 200 Indicator': 'ktm_duke_200_indicator.png',
    'Apache RTR 160 Mirror Set': 'apache_rtr_160_mirror_set.png',
    'Fazer V2 Front Mudguard': 'fazer_v2_front_mudguard.png',
    
    # Extra matches if needed (fuzzy matching logic could be better but this is explicit)
    'Bajaj Discover Carburetor': 'bajaj_discover_carburetor.png',
    'Hero Passion Meter': 'hero_passion_meter.png',
    'RE Classic Silencer': 're_classic_silencer.png',
    'Yamaha FZ Rear Disc': 'yamaha_fz_rear_disc.png'
}

try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        cursor = conn.cursor()
        
        print("Updating product images...")
        count = 0
        
        # 1. Direct Name Match
        for product_name, filename in image_mapping.items():
            cursor.execute("UPDATE products SET image_url = %s WHERE name = %s", (filename, product_name))
            if cursor.rowcount > 0:
                print(f"   Updated '{product_name}' -> {filename}")
                count += cursor.rowcount
            else:
                # Try partial match if full match failed
                # e.g. "KTM Duke 200 Indicator" in DB vs "ktm Duke 200 Indicator" key
                cursor.execute("UPDATE products SET image_url = %s WHERE name LIKE %s", (filename, f"%{product_name}%"))
                if cursor.rowcount > 0:
                     print(f"   Updated (partial) '{product_name}' -> {filename}")
                     count += cursor.rowcount
        
        conn.commit()
        print(f"Successfully updated {count} product images.")
        
        cursor.close()
        conn.close()
except Error as e:
    print(f"Error: {e}")
