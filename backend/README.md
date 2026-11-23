# 🥩 Fresh Meat Market – Backend & Full-Stack Integration Guide

Complete, secure, scalable Python Flask REST API backend with MySQL database and seamless integration with the React + Vite Glassmorphism frontend.

---

## 1. Project Overview

**Fresh Meat Market** is a high-performance, luxury e-commerce platform for ordering farm-fresh chicken, tender mutton, fresh fish/seafood, and free-range farm eggs.
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide icons, Custom Glassmorphism UI with Dark Crimson luxury red theme.
- **Backend**: Python 3.10+, Flask REST API, Flask-SQLAlchemy ORM, Flask-JWT-Extended authentication, Flask-CORS, Werkzeug password hashing.
- **Database**: MySQL (with automatic SQLite fallback for resilient zero-crash local development).
- **Payment Modes**: Cash on Delivery (COD) and Razorpay Online Payment (Test Mode).

---

## 2. Technology Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | Python 3.10+, Flask 3.0.3, Flask RESTful Architecture |
| **Database & ORM** | MySQL 8.0 / PyMySQL 1.1.0, Flask-SQLAlchemy 3.1.1, Flask-Migrate |
| **Authentication** | Flask-JWT-Extended 4.6.0 (Bearer JWT tokens), Werkzeug security |
| **Payment Gateway** | Razorpay Python SDK (Test Mode / HMAC SHA256 Signature Verification) |
| **Testing** | pytest 8.2.2, pytest-flask |
| **Frontend** | React 18, Vite, Tailwind CSS, Vanilla CSS Glass Design System |

---

## 3. Project Directory Structure

```
MEATE SHOP/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory, CORS, error handlers, DB setup
│   │   ├── config.py            # Environment configurations (MySQL + SQLite fallback)
│   │   ├── extensions.py        # Extensions (db, jwt, cors, migrate)
│   │   ├── models/
│   │   │   ├── user.py          # User model (customer, admin roles, password hash)
│   │   │   ├── category.py      # Category model (slug, name, image, active)
│   │   │   ├── product.py       # Product model (weight calculation, stock, tags)
│   │   │   ├── cart.py          # Cart & CartItem models
│   │   │   ├── address.py       # Address model (PIN code validation, default flag)
│   │   │   ├── order.py         # Order & OrderItem snapshot models
│   │   │   └── payment.py       # Payment model (COD / Razorpay status tracking)
│   │   ├── routes/
│   │   │   ├── auth_routes.py       # Register, login, profile, password change
│   │   │   ├── category_routes.py   # Categories list & detail
│   │   │   ├── product_routes.py    # Products list, search, filter, detail
│   │   │   ├── cart_routes.py       # Cart view, add, update, remove, clear
│   │   │   ├── address_routes.py    # User address CRUD
│   │   │   ├── order_routes.py      # Order placement, history, cancellation
│   │   │   ├── payment_routes.py    # Razorpay order create, signature verify
│   │   │   └── admin_routes.py      # Admin dashboard metrics, orders, products, customers
│   │   ├── services/
│   │   │   ├── order_service.py     # Transactional order creation, stock deduction, coupons
│   │   │   └── payment_service.py   # Razorpay test order creation & HMAC verification
│   │   └── utils/
│   │       └── validators.py        # Email, phone, PIN validator, @admin_required decorator
│   ├── tests/
│   │   ├── conftest.py              # Pytest fixtures and test database setup
│   │   └── test_all_endpoints.py    # 12 automated unit/integration tests
│   ├── .env.example
│   ├── .env
│   ├── requirements.txt
│   ├── run.py                       # Server entry point (port 5001)
│   └── seed.py                      # Database seeder (Admin, Demo Customer, Products)
├── src/                             # React frontend components and pages
│   ├── services/
│   │   └── api.js                   # Centralized API service for frontend integration
│   ├── components/
│   │   ├── Navbar.jsx               # Header with user menu, admin badge, orders
│   │   ├── CartDrawer.jsx           # Multi-step checkout, COD & Razorpay flow
│   │   ├── LoginModal.jsx           # Glassmorphism auth modal with demo logins
│   │   ├── OrderHistoryModal.jsx    # Customer order history & tracking
│   │   ├── AdminDashboardModal.jsx  # Admin KPIs & order manager
│   │   └── ...
│   └── App.jsx                      # Main app container
├── package.json
└── README.md
```

---

## 4. Environment Variables Setup

Create `backend/.env` (or copy from `backend/.env.example`):

```bash
# Flask Config
FLASK_APP=run.py
FLASK_ENV=development
DEBUG=True
PORT=5001
SECRET_KEY=fresh-meat-market-super-secret-production-key-2026
JWT_SECRET_KEY=fresh-meat-market-jwt-secret-key-signature-2026

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fresh_meat_market
DB_USER=root
DB_PASSWORD=your_mysql_password

# Database Resilience Fallback
# If local MySQL is offline, automatically falls back to SQLite without crashing
USE_SQLITE_FALLBACK=true

# Razorpay Test Credentials (Development)
RAZORPAY_KEY_ID=rzp_test_freshmeatmarketdemo
RAZORPAY_KEY_SECRET=demo_secret_freshmeatmarket2026

# Initial Admin Seed Credentials
ADMIN_NAME=Fresh Market Admin
ADMIN_EMAIL=admin@freshmeatmarket.com
ADMIN_PHONE=9998887770
ADMIN_PASSWORD=Admin@123456
```

---

## 5. MySQL Database Setup

1. Start your local MySQL service:
   ```bash
   # macOS (Homebrew)
   brew services start mysql
   
   # Linux (systemd)
   sudo systemctl start mysql
   
   # Windows (MySQL service)
   net start mysql
   ```

2. Create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS fresh_meat_market CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. Update `DB_PASSWORD` and `DB_USER` in `backend/.env`.

> **Note on Zero-Downtime Fallback**: If MySQL is not currently running or credentials are not yet configured, the application automatically boots on `backend/fresh_meat_market.db` (SQLite) so development, automated tests, and frontend UI remain 100% operational!

---

## 6. Installation & Execution

### Backend Setup:
```bash
# 1. Navigate to project root and create Python virtual environment
cd "/Users/rahul/MEATE SHOP"
python3 -m venv backend/venv

# 2. Activate virtual environment
source backend/venv/bin/activate    # macOS / Linux
# backend\venv\Scripts\activate     # Windows

# 3. Install required Python packages
pip install -r backend/requirements.txt

# 4. Seed the Database (Admin, Demo Customer, Categories, Products)
python backend/seed.py

# 5. Start the Flask Backend Server
python backend/run.py
```
Backend will start on: **`http://127.0.0.1:5001`**

### Frontend Setup:
```bash
# In another terminal window:
cd "/Users/rahul/MEATE SHOP"
npm install
npm run dev
```
Frontend will be accessible at: **`http://127.0.0.1:5173`**

---

## 7. Automated Testing

Run the automated pytest test suite to verify all endpoints, security rules, and database integrity:

```bash
./backend/venv/bin/pytest backend/tests -v
```

### Tested Scenarios (12 / 12 Passing):
- `test_registration_success`: Full name, email, phone, password hashing.
- `test_duplicate_email_registration`: Prevents account duplication with 409 Conflict.
- `test_login_invalid_password`: Enforces secure password rejection.
- `test_login_success`: Issues JWT bearer access token and user payload.
- `test_get_profile`: Verifies protected `/api/auth/profile` route with JWT.
- `test_get_categories`: Returns category catalog.
- `test_get_products`: Returns products with weight options, rating, stock.
- `test_search_products`: Case-insensitive search on name, description, tags.
- `test_cart_operations`: Add, update quantity, compute server-side subtotals.
- `test_checkout_and_cod_order`: Transactional order placement, stock deduction, address snapshot.
- `test_online_payment_verification`: Razorpay payment verification with HMAC-SHA256 signature.
- `test_admin_authorization`: Enforces role-based access control (RBAC), blocking customers from admin routes.

---

## 8. REST API Documentation

### Authentication (`/api/auth`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register customer (`full_name`, `email`, `phone`, `password`, `confirm_password`) | No |
| `POST` | `/api/auth/login` | Login with email & password, returns JWT token | No |
| `GET` | `/api/auth/profile` | Retrieve current authenticated user profile | Yes (Bearer JWT) |
| `PUT` | `/api/auth/profile` | Update user profile (name, phone) | Yes (Bearer JWT) |
| `PUT` | `/api/auth/change-password` | Change user password | Yes (Bearer JWT) |

### Products & Categories (`/api/products`, `/api/categories`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/categories` | List all active product categories | No |
| `GET` | `/api/categories/<id_or_slug>` | Get category details with products | No |
| `GET` | `/api/products` | Filterable product catalog (`category`, `search`, `sort`, `bestseller`) | No |
| `GET` | `/api/products/<id_or_code>` | Get single product details | No |
| `GET` | `/api/products/search?q=...` | Full-text query on products | No |

### Shopping Cart (`/api/cart`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/cart` | View customer cart with calculated subtotals | Yes |
| `POST` | `/api/cart/add` | Add product to cart with selected weight & qty | Yes |
| `PUT` | `/api/cart/update/<item_id>` | Update item quantity | Yes |
| `DELETE` | `/api/cart/remove/<item_id>` | Remove item from cart | Yes |
| `DELETE` | `/api/cart/clear` | Clear all items in cart | Yes |

### Addresses (`/api/addresses`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/addresses` | List saved delivery addresses | Yes |
| `POST` | `/api/addresses` | Add new delivery address with PIN validation | Yes |
| `PUT` | `/api/addresses/<id>` | Update delivery address | Yes |
| `DELETE` | `/api/addresses/<id>` | Delete delivery address | Yes |

### Orders (`/api/orders`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/orders` | Place order (from cart or direct payload) | Yes |
| `GET` | `/api/orders` | Get user order history | Yes |
| `GET` | `/api/orders/<id>` | Get order detail with item snapshots | Yes |
| `PUT` | `/api/orders/<id>/cancel` | Cancel order (restores stock if pending) | Yes |

### Payments (`/api/payments`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/payments/create` | Create Razorpay payment order for order ID | Yes |
| `POST` | `/api/payments/verify` | Verify Razorpay payment signature & update status | Yes |

### Admin Console (`/api/admin`) – *Role: Admin Only*
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/admin/dashboard` | Overall KPIs (sales, orders, customers, pending) | Yes (Admin) |
| `GET` | `/api/admin/orders` | View all customer orders with filter | Yes (Admin) |
| `PUT` | `/api/admin/orders/<id>/status`| Update order status (Pending → Confirmed → Out for Delivery → Delivered) | Yes (Admin) |
| `POST` | `/api/admin/products` | Create new product | Yes (Admin) |
| `PUT` | `/api/admin/products/<id>` | Edit product price, stock, description | Yes (Admin) |
| `DELETE`| `/api/admin/products/<id>` | Delete product | Yes (Admin) |
| `GET` | `/api/admin/customers` | View registered customer list and stats | Yes (Admin) |

---

## 9. Seed Demo Accounts

For instant testing, use the pre-seeded credentials:

- **Customer Account**:
  - Email: `rahul@example.com`
  - Password: `Customer@123`
- **Admin Account**:
  - Email: `admin@freshmeatmarket.com`
  - Password: `Admin@123456`
