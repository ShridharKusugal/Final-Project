CREATE DATABASE IF NOT EXISTS nk_automobiles;
USE nk_automobiles;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('customer', 'admin') DEFAULT 'customer',
    full_name VARCHAR(100),
    phone VARCHAR(15),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    reset_token VARCHAR(255),
    reset_token_expiry DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Default Admin (Password: admin123)
INSERT INTO users (username, email, password_hash, role) VALUES ('admin', 'admin@nkautomobiles.com', 'scrypt:32768:8:1$VjhMX9sd1hN7LGGI$166486b46ae1c7b0a794bc6bdd136c167bc783f5f5165c0e20422ca93bd0718ae23d8b0dde3266913d1690097a83f0232ce820f1fa76e443a6cd20997e7497c4', 'admin');

-- Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    specifications TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    category_id INT,
    brand VARCHAR(50),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

-- Cart Table
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- Review Media Table
CREATE TABLE IF NOT EXISTS review_media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    review_id INT,
    media_url VARCHAR(255) NOT NULL,
    media_type ENUM('image', 'video') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (review_id) REFERENCES reviews(review_id) ON DELETE CASCADE
);

-- Offers Table
CREATE TABLE IF NOT EXISTS offers (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    discount_percentage DECIMAL(5, 2),
    valid_until DATETIME
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(100),
    phone_number VARCHAR(15),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    total_amount DECIMAL(10, 2),
    payment_method ENUM('COD', 'UPI', 'Card') DEFAULT 'COD',
    transaction_id VARCHAR(255),
    status ENUM('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    tracking_number VARCHAR(100),
    courier_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert Categories
INSERT INTO categories (name, description) VALUES 
('Engine Parts', 'Pistons, slightly, valves, etc.'),
('Brake Parts', 'Brake pads, shoes, discs, etc.'),
('Electrical Parts', 'Lights, batteries, horns, etc.'),
('Body Parts', 'Fairings, mudguards, etc.'),
('Chain & Sprocket', 'Chains, sprockets, kits.'),
('Filters', 'Air filters, oil filters.'),
('Accessories', 'Stickers, covers, mobile holders.');

-- Insert Dummy Products (10 samples)
INSERT INTO products (name, description, price, stock_quantity, category_id, brand, image_url) VALUES
('Honda Shine Piston Kit', 'Original Honda Piston Kit for Shine 125cc', 1250.00, 50, 1, 'Honda', 'default.jpg'),
('Bajaj Pulsar Brake Pads', 'Front Disc Brake Pads for Pulsar 150', 350.00, 100, 2, 'Bajaj', 'default.jpg'),
('TVS Jupiter Battery', '4LB Battery for TVS Jupiter', 1100.00, 30, 3, 'TVS', 'default.jpg'),
('Yamaha R15 Chain Sprocket Kit', 'Brass Chain Sprocket Kit for R15 V3', 2500.00, 20, 5, 'Yamaha', 'default.jpg'),
('Hero Splendor Air Filter', 'Foam Air Filter for Splendor Plus', 150.00, 200, 6, 'Hero', 'default.jpg'),
('Royal Enfield Leg Guard', 'Stainless Steel Leg Guard for Classic 350', 1800.00, 15, 7, 'Royal Enfield', 'default.jpg'),
('Activa 6G Headlight Assembly', 'Complete Headlight Unit for Activa 6G', 1600.00, 25, 3, 'Honda', 'default.jpg'),
('ktm Duke 200 Indicator', 'LED Indicator for KTM Duke', 450.00, 60, 3, 'KTM', 'default.jpg'),
('Apache RTR 160 Mirror Set', 'Rear View Mirrors for Apache RTR 160', 550.00, 40, 4, 'TVS', 'default.jpg'),
('Fazer V2 Front Mudguard', 'Red color front mudguard for Yamaha Fazer', 850.00, 10, 4, 'Yamaha', 'default.jpg');

-- Contact Messages Table
CREATE TABLE IF NOT EXISTS contact_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    status ENUM('New', 'Read', 'Replied') DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
