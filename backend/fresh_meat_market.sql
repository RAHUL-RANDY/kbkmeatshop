-- ========================================================
-- Fresh Meat Market - Full MySQL Database Schema & Seed
-- Compatible with MySQL 8.x, MariaDB, XAMPP, phpMyAdmin
-- ========================================================

CREATE DATABASE IF NOT EXISTS `fresh_meat_market` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `fresh_meat_market`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `carts`;
DROP TABLE IF EXISTS `addresses`;
DROP TABLE IF EXISTS `cart_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `payments`;

-- --------------------------------------------------------
-- Table structure for `users`
-- --------------------------------------------------------
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `full_name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `phone` VARCHAR(20) NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` VARCHAR(20) NOT NULL DEFAULT 'customer',
  `is_active` BOOLEAN NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `categories`
-- --------------------------------------------------------
CREATE TABLE `categories` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `slug` VARCHAR(50) NOT NULL UNIQUE,
  `name` VARCHAR(100) NOT NULL,
  `description` TEXT NULL,
  `image` VARCHAR(255) NULL,
  `display_order` INT NOT NULL DEFAULT 0,
  `is_active` BOOLEAN NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `products`
-- --------------------------------------------------------
CREATE TABLE `products` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_id` INT NOT NULL,
  `product_code` VARCHAR(60) NOT NULL UNIQUE,
  `product_name` VARCHAR(150) NOT NULL,
  `description` TEXT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `original_price` DECIMAL(10,2) NULL,
  `unit` VARCHAR(50) NOT NULL DEFAULT 'kg',
  `default_weight` VARCHAR(50) NOT NULL DEFAULT '1 kg',
  `weight_options` TEXT NOT NULL,
  `pieces` VARCHAR(50) NULL,
  `serves` VARCHAR(50) NULL,
  `rating` DECIMAL(3,2) NOT NULL DEFAULT 4.8,
  `reviews` INT NOT NULL DEFAULT 0,
  `image` VARCHAR(255) NULL,
  `is_bestseller` BOOLEAN NOT NULL DEFAULT 0,
  `is_available` BOOLEAN NOT NULL DEFAULT 1,
  `stock_quantity` INT NOT NULL DEFAULT 100,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `carts`
-- --------------------------------------------------------
CREATE TABLE `carts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL UNIQUE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `addresses`
-- --------------------------------------------------------
CREATE TABLE `addresses` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `title` VARCHAR(50) NOT NULL DEFAULT 'Home',
  `street_address` VARCHAR(255) NOT NULL,
  `landmark` VARCHAR(150) NULL,
  `city` VARCHAR(100) NOT NULL,
  `state` VARCHAR(100) NOT NULL DEFAULT 'Tamil Nadu',
  `pincode` VARCHAR(10) NOT NULL,
  `is_default` BOOLEAN NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `cart_items`
-- --------------------------------------------------------
CREATE TABLE `cart_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `cart_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `selected_weight` VARCHAR(50) NOT NULL,
  `quantity` INT NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`cart_id`) REFERENCES `carts`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `orders`
-- --------------------------------------------------------
CREATE TABLE `orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_number` VARCHAR(50) NOT NULL UNIQUE,
  `user_id` INT NOT NULL,
  `address_id` INT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  `delivery_charge` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `discount_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `coupon_code` VARCHAR(50) NULL,
  `total_amount` DECIMAL(10,2) NOT NULL,
  `order_status` VARCHAR(50) NOT NULL DEFAULT 'Placed',
  `payment_status` VARCHAR(50) NOT NULL DEFAULT 'Pending',
  `payment_method` VARCHAR(50) NOT NULL DEFAULT 'COD',
  `estimated_delivery` VARCHAR(100) NULL,
  `delivery_notes` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `order_items`
-- --------------------------------------------------------
CREATE TABLE `order_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `product_id` INT NULL,
  `product_name` VARCHAR(150) NOT NULL,
  `product_image` VARCHAR(255) NULL,
  `selected_weight` VARCHAR(50) NOT NULL,
  `quantity` INT NOT NULL,
  `unit_price` DECIMAL(10,2) NOT NULL,
  `total_price` DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `payments`
-- --------------------------------------------------------
CREATE TABLE `payments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL UNIQUE,
  `payment_method` VARCHAR(50) NOT NULL,
  `payment_status` VARCHAR(50) NOT NULL DEFAULT 'Pending',
  `amount` DECIMAL(10,2) NOT NULL,
  `currency` VARCHAR(10) NOT NULL DEFAULT 'INR',
  `razorpay_order_id` VARCHAR(100) NULL,
  `razorpay_payment_id` VARCHAR(100) NULL,
  `razorpay_signature` VARCHAR(255) NULL,
  `paid_at` DATETIME NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed data for `users`
INSERT INTO `users` (`id`, `full_name`, `email`, `phone`, `password_hash`, `role`, `is_active`, `created_at`) VALUES (1, 'Market Administrator', 'admin@freshmeatmarket.com', '9876543210', 'scrypt:32768:8:1$ZQNX3Pc4WDqk4tp1$75f94bfe102806b518512f8d66b1bd2b32dfb6d9b8bd3164d7b6be58de42d6380b67f5c11ea83340ba272f2f7da6ef1bdc218c5e6388f56e45079fc1721b00f3', 'admin', 1, '2026-11-14 04:33:54.266863');

INSERT INTO `users` (`id`, `full_name`, `email`, `phone`, `password_hash`, `role`, `is_active`, `created_at`) VALUES (2, 'Rahul Sharma', 'rahul@example.com', '9876543211', 'scrypt:32768:8:1$barQx83m7nevJtZ0$de83fbad02751dce154bdbdc3ab5328c7b383b16e0b03453af9c6c6cd1319566610c9ed9d0e3e991593426d75efd8e2520caf6a006e42e248855f268a811a000', 'customer', 1, '2026-11-14 04:33:58.539480');

-- Seed data for `categories`
INSERT INTO `categories` (`id`, `category_name`, `slug`, `subtitle`, `description`, `image`, `item_count_label`, `is_active`, `created_at`) VALUES (1, 'Fresh Chicken', 'chicken', 'Hygienic & Farm Fresh', 'Free-range, antibiotic-free poultry sourced directly from bio-secured local farms.', '/images/cat-chicken.jpg', '18 Items', 1, '2026-11-14 04:33:58.620095');

INSERT INTO `categories` (`id`, `category_name`, `slug`, `subtitle`, `description`, `image`, `item_count_label`, `is_active`, `created_at`) VALUES (2, 'Fresh Mutton', 'mutton', 'Tender & High Quality', 'Grass-fed tender lamb and goat meat, artfully hand-cut and quality graded.', '/images/cat-mutton.jpg', '12 Items', 1, '2026-11-14 04:33:58.633386');

INSERT INTO `categories` (`id`, `category_name`, `slug`, `subtitle`, `description`, `image`, `item_count_label`, `is_active`, `created_at`) VALUES (3, 'Fresh Fish', 'fish', 'Daily Catch & Cleaned', 'Daily ocean catch, whole cleaned, gutted, and chilled on ice beds for supreme freshness.', '/images/cat-fish.jpg', '15 Items', 1, '2026-11-14 04:33:58.817178');

INSERT INTO `categories` (`id`, `category_name`, `slug`, `subtitle`, `description`, `image`, `item_count_label`, `is_active`, `created_at`) VALUES (4, 'Farm Fresh Eggs', 'eggs', 'Nutritious & Chemical Free', 'Organic, farm-laid table eggs with deep golden yolks and thick natural shells.', '/images/cat-eggs.jpg', '8 Packs', 1, '2026-11-14 04:33:58.821768');

-- Seed data for `products`
INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (1, 'country-chicken', 'Country Chicken', 'Rich, natural free-roaming country chicken with tender fibrous texture and authentic rustic flavor. No antibiotics or hormones.', 1, 320.0, 380.0, 'kg', '["500 g", "1 kg", "2 kg"]', '1 kg', '/images/prod-country-chicken.jpg', 150, 1, 1, 4.9, 428, '12-16 Pieces', '3-4 Persons', '2026-11-14 04:33:58.841122');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (2, 'broiler-chicken', 'Broiler Chicken', 'Juicy and succulent chicken drumsticks and curry cuts, chilled at optimum 0-4°C to retain natural juices and tenderness.', 1, 220.0, 260.0, 'kg', '["500 g", "1 kg", "2 kg"]', '1 kg', '/images/prod-broiler-chicken.jpg', 200, 1, 0, 4.8, 310, '8-10 Pieces', '2-3 Persons', '2026-11-14 04:33:58.847383');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (3, 'chicken-breast', 'Chicken Breast', 'Skinless, boneless lean fillets packed with high protein. Ideal for grilling, keto diets, gym meal preps, and stir-fry recipes.', 1, 380.0, 420.0, 'kg', '["500 g", "1 kg", "1.5 kg"]', '1 kg', '/images/prod-chicken-breast.jpg', 120, 1, 0, 4.9, 580, '4-6 Fillets', '4 Persons', '2026-11-14 04:33:58.851796');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (4, 'mutton-curry-cut', 'Mutton Curry Cut', 'A balance of bone-in and boneless lamb and goat cuts selected from ribs, shoulder, and leg for decadent slow-cooked curries.', 2, 780.0, 850.0, 'kg', '["500 g", "1 kg", "2 kg"]', '1 kg', '/images/prod-mutton-curry.jpg', 80, 1, 1, 5.0, 692, '16-20 Pieces', '4-5 Persons', '2026-11-14 04:33:58.862213');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (5, 'mutton-boneless', 'Mutton Boneless', 'Uniformly diced prime chunks of pure boneless goat meat. Perfect for pan roasts, mutton biryani, kebabs, and gourmet gravies.', 2, 980.0, 1080.0, 'kg', '["500 g", "1 kg", "1.5 kg"]', '1 kg', '/images/prod-mutton-boneless.jpg', 60, 1, 1, 4.9, 385, 'Bite Size Cubes', '4 Persons', '2026-11-14 04:33:58.863796');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (6, 'farm-fresh-eggs', 'Farm Fresh Eggs', 'Farm-laid antibiotic-free table eggs with rich golden yolks and thick shells. Washed, graded, and quality inspected daily.', 4, 160.0, 190.0, '30 Eggs', '["6 Eggs", "12 Eggs", "1 Pack (30 Eggs)"]', '1 Pack (30 Eggs)', '/images/prod-farm-eggs.jpg', 300, 1, 1, 4.9, 840, '30 Fresh Eggs', 'Whole Family', '2026-11-14 04:33:58.864929');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (7, 'salmon-steak', 'Atlantic Salmon Steak', 'Fresh Norwegian Atlantic salmon cut into uniform steaks, rich in Omega-3 fatty acids, vibrant natural color, and tender flaky texture.', 3, 650.0, 750.0, '500 g', '["250 g", "500 g", "1 kg"]', '500 g', '/images/prod-salmon-steak.jpg', 50, 1, 0, 4.9, 210, '2-3 Thick Steaks', '2 Persons', '2026-11-14 04:33:58.865800');

INSERT INTO `products` (`id`, `product_code`, `product_name`, `description`, `category_id`, `price`, `original_price`, `unit`, `weight_options`, `default_weight`, `image`, `stock_quantity`, `is_available`, `is_bestseller`, `rating`, `reviews_count`, `pieces`, `serves`, `created_at`) VALUES (8, 'fresh-mackerel', 'Fresh Mackerel & Seabass', 'Daily ocean catch, whole cleaned and gutted. Ready for spicy coastal tawa fry or aromatic coconut fish curry.', 3, 360.0, 420.0, 'kg', '["500 g", "1 kg"]', '1 kg', '/images/cat-fish.jpg', 90, 1, 0, 4.7, 145, '3-4 Whole Fish', '3 Persons', '2026-11-14 04:33:58.866485');

-- Seed data for `carts`
INSERT INTO `carts` (`id`, `user_id`, `created_at`, `updated_at`) VALUES (1, 1, '2026-11-14 04:33:54.759409', '2026-11-14 04:33:54.759416');

INSERT INTO `carts` (`id`, `user_id`, `created_at`, `updated_at`) VALUES (2, 2, '2026-11-14 04:33:58.550234', '2026-11-14 04:33:58.550241');

-- Seed data for `addresses`
INSERT INTO `addresses` (`id`, `user_id`, `recipient_name`, `phone`, `address_line`, `city`, `state`, `pincode`, `is_default`, `created_at`) VALUES (1, 2, 'Rahul Sharma', '9876543211', 'No. 42, Anna Nagar West, 2nd Avenue', 'Chennai', 'Tamil Nadu', '600040', 1, '2026-11-14 04:33:58.547318');

SET FOREIGN_KEY_CHECKS = 1;