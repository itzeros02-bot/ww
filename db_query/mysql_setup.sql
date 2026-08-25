-- MySQL Database Setup Script for Database Query Tool
-- This script creates databases, users, and sample data

-- Create databases
CREATE DATABASE IF NOT EXISTS testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS interview CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated database user (optional but recommended)
-- CREATE USER IF NOT EXISTS 'dbuser'@'localhost' IDENTIFIED BY 'dbuser2024!';
-- GRANT ALL PRIVILEGES ON testdb.* TO 'dbuser'@'localhost';
-- GRANT ALL PRIVILEGES ON interview.* TO 'dbuser'@'localhost';
-- FLUSH PRIVILEGES;

-- Use testdb for sample data
USE testdb;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (name, email, age, city) VALUES
    ('张三', 'zhangsan@example.com', 25, '北京'),
    ('李四', 'lisi@example.com', 30, '上海'),
    ('王五', 'wangwu@example.com', 28, '深圳'),
    ('赵六', 'zhaoliu@example.com', 35, '广州'),
    ('孙七', 'sunqi@example.com', 22, '杭州'),
    ('周八', 'zhouba@example.com', 27, '成都'),
    ('吴九', 'wujiu@example.com', 31, '重庆'),
    ('郑十', 'zhengshi@example.com', 29, '西安');

-- Create orders table for more complex queries
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample order data
INSERT INTO orders (user_id, product_name, quantity, price) VALUES
    (1, '笔记本电脑', 1, 5999.00),
    (2, '智能手机', 2, 3999.00),
    (1, '无线鼠标', 1, 199.00),
    (3, '机械键盘', 1, 699.00),
    (4, '显示器', 2, 1299.00),
    (2, '耳机', 1, 899.00),
    (5, '平板电脑', 1, 2999.00),
    (6, '智能手表', 1, 1599.00),
    (7, '移动电源', 3, 199.00),
    (8, '蓝牙音箱', 1, 399.00);

-- Create a view for user order summary
CREATE OR REPLACE VIEW user_order_summary AS
SELECT
    u.id as user_id,
    u.name as user_name,
    u.email as user_email,
    COUNT(o.id) as total_orders,
    SUM(o.quantity * o.price) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email;

-- Show created databases
SHOW DATABASES;

-- Show tables in testdb
USE testdb;
SHOW TABLES;

-- Sample queries to test
SELECT 'Users table:' as info;
SELECT * FROM users LIMIT 5;

SELECT 'Orders table:' as info;
SELECT * FROM orders LIMIT 5;

SELECT 'User order summary:' as info;
SELECT * FROM user_order_summary;