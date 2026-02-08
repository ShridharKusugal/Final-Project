-- Add Payment Pending status to orders table
ALTER TABLE orders 
MODIFY COLUMN status ENUM('Payment Pending', 'Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending';

-- Add payment screenshot field
ALTER TABLE orders 
ADD COLUMN payment_screenshot VARCHAR(255) AFTER transaction_id;

-- Add payment verified timestamp
ALTER TABLE orders 
ADD COLUMN payment_verified_at DATETIME AFTER payment_screenshot;

-- Add payment verified by admin
ALTER TABLE orders 
ADD COLUMN payment_verified_by INT AFTER payment_verified_at,
ADD FOREIGN KEY (payment_verified_by) REFERENCES users(user_id);
