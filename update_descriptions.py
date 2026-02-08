import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2004',
    'database': 'nk_automobiles'
}

products_update = {
    'Honda Shine Piston Kit': """This is a 100% genuine Honda piston kit designed specifically for the CB Shine 125cc engine.
It includes the piston, piston rings, pin, and circlips, ensuring a complete overhaul solution.
Manufactured with high-grade aluminum alloy for superior durability and heat resistance.
Restores engine compression and power to factory standards, providing a smooth riding experience.""",

    'Bajaj Pulsar Brake Pads': """High-performance front disc brake pads suitable for Bajaj Pulsar 150/180 models.
Made from organic compound materials that offer excellent stopping power and reduced noise.
These pads are designed to minimize wear on the brake disc while ensuring maximum safety.
Easy to install and provides consistent braking performance in both wet and dry conditions.""",

    'TVS Jupiter Battery': """Maintenance-free 4LB battery compatible with TVS Jupiter and similar scooters.
Features advanced lead-calcium technology for longer life and reliable starting power.
Spill-proof design ensures safety and zero maintenance requirements throughout its lifespan.
Comes with a 48-month warranty against manufacturing defects for complete peace of mind.""",

    'Yamaha R15 Chain Sprocket Kit': """Premium brass-coated chain and sprocket kit for Yamaha R15 V3.
Includes a heavy-duty chain, front sprocket, and rear sprocket for optimal power transmission.
Designed to withstand high torque and reduce friction for a smoother ride.
Extends the life of your drivetrain and improves overall acceleration and efficiency.""",

    'Hero Splendor Air Filter': """Genuine foam air filter element for Hero Splendor Plus and Passion Pro.
Effectively filters out dust and debris, ensuring clean air intake for the engine.
Washable and reusable design makes it a cost-effective maintenance solution.
Regular replacement improves fuel efficiency and engine longevity.""",

    'Royal Enfield Leg Guard': """Heavy-duty stainless steel leg guard (Airfly type) for Royal Enfield Classic 350/500.
Provides superior protection for the engine and rider's legs in case of falls.
Chrome-plated finish adds a classic, premium look to your motorcycle.
Includes all necessary mounting hardware for a hassle-free installation.""",

    'Activa 6G Headlight Assembly': """Complete halogen headlight assembly for Honda Activa 6G.
Includes the main reflector, lens, and bulb holder for a direct plug-and-play fit.
Manufactured with UV-resistant plastic to prevent yellowing and ensure clear visibility at night.
Restores the original look and safety of your scooter.""",

    'ktm Duke 200 Indicator': """Sleek LED turn signal indicator compatible with KTM Duke 125/200/390.
Features high-intensity LEDs for maximum visibility even in bright daylight.
Flexible stem design prevents breakage during accidental impacts or falls.
Water-resistant construction ensures durability in all weather conditions.""",

    'Apache RTR 160 Mirror Set': """Set of left and right rear-view mirrors for TVS Apache RTR 160/180.
Aerodynamic design reduces wind resistance and vibration at high speeds.
Wide convex glass provides an expanded field of view for safer lane changes.
Sturdy build quality with adjustable stalks for customized positioning.""",

    'Fazer V2 Front Mudguard': """Genuine replacement front mudguard for Yamaha Fazer V2 (Red).
Made from high-quality ABS plastic that is flexible and resistant to cracks.
Factory-matched red paint finish ensures a seamless integration with your bike.
Protect your engine and radiator from mud splashes and road debris effectively."""
}

def update_descriptions():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            
            for name, desc in products_update.items():
                print(f"Updating: {name}")
                cursor.execute("UPDATE products SET description = %s WHERE name = %s", (desc, name))
            
            conn.commit()
            print("All product descriptions updated successfully!")
            
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error while updating descriptions: {e}")

if __name__ == '__main__':
    update_descriptions()
