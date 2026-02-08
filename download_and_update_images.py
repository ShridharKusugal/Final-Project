import mysql.connector
from mysql.connector import Error
import urllib.request
import os

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shri@2004',
    'database': 'nk_automobiles'
}

# Keywords for loremflickr
product_keywords = {
    'Heavy Duty Drive Chain': 'motorcycle,chain',
    'Side Box Luggage Set': 'motorcycle,panniers',
    'Adjustable Brake/Clutch Levers': 'motorcycle,handlebar',
    'High-Flow Oil Filter': 'oil,filter',
    'Disc Brake Rotor 300mm': 'brake,disc',
    'Premium Seat Cover': 'motorcycle,seat',
    'Digital Instrument Cluster': 'motorcycle,speedometer',
    'Stainless Steel Exhaust System': 'motorcycle,exhaust',
    'LED Fog Light Kit': 'fog,light,lamp',
    'Performance Clutch Plate Set': 'engine,gear'
}

def download_images_and_update():
    upload_dir = os.path.join('static', 'products')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Use a session to keep connections open if needed, but urllib is fine
            import time
            
            for product_name, keywords in product_keywords.items():
                filename = product_name.lower().replace(' ', '_').replace('/', '_') + '.jpg'
                filepath = os.path.join(upload_dir, filename)
                
                # Add a random seed to get different images if needed, but here we just want one good one
                # LoremFlickr redirects to an image.
                # We need to follow redirects.
                url = f"https://loremflickr.com/800/600/{keywords}/all"
                
                print(f"Downloading {product_name} from {url}...")
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        if response.status == 200:
                            with open(filepath, 'wb') as f:
                                f.write(response.read())
                            
                            # Update DB
                            query = "UPDATE products SET image_url = %s WHERE name = %s"
                            cursor.execute(query, (filename, product_name))
                            print(f"Updated {product_name}")
                            # Sleep to be nice
                            time.sleep(1)
                except Exception as e: 
                    print(f"Failed to download for {product_name}: {e}")
                    continue
            conn.commit()
    except Exception as e: print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    download_images_and_update()
