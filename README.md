# KARTMART – Smart E-Commerce Shopping System

> **A modern, responsive Flask-based E-Commerce web application featuring a curated multi-category product catalogue, dynamic shopping cart drawer, simulated multi-mode checkout, order tracking with cancellation workflow, and a role-protected administrative management console.**

---

## 📌 Project Overview

**KARTMART** is a full-stack e-commerce web platform engineered with Python and Flask. Designed for both seamless customer shopping experiences and store operations management, the system delivers an end-to-end shopping workflow—from product browsing and category-based filtering to cart management, promo-code discounts, simulated checkout, customer order histories, and backend administrative operations.

---

## 🎯 Project Objectives

1. **End-to-End E-Commerce Workflow:** Deliver a complete user journey from catalog browsing to simulated payment and order placement.
2. **Robust Backend Architecture:** Build a modular Flask application following the Application Factory pattern and Blueprint architectural separation.
3. **Database Integrity & ORM Modeling:** Implement relational schema design with SQLAlchemy ORM handling Users, Categories, Products, Product Variants, Orders, Order Items, Carts, Coupons, Addresses, and Support Tickets.
4. **Role-Based Access Control (RBAC):** Maintain strict boundary separation between public Visitors, registered Customers, and authenticated Store Administrators.
5. **Interactive UI/UX:** Provide a responsive, modern dark/light glassmorphic frontend utilizing semantic HTML5, custom CSS3 design tokens, and vanilla JavaScript (no heavy runtime framework dependencies).
6. **Automated Quality Assurance:** Maintain a comprehensive Pytest test suite verifying authentication boundaries, cart calculations, stock deduction, coupon validation, and order state machines.

---

## ✨ Main Features

### 🛒 Customer Storefront & Shopping Experience
* **Curated 13-Category Product Catalogue:** Electronics & Tech, Men's Fashion, Women's Fashion, Kids & Baby, Footwear, Toys & Games, Home & Kitchen, Furniture & Living, Beauty & Skincare, Sports & Fitness, Books & Stationery, Bags & Accessories, and Gourmet Essentials.
* **Instant Keyword Search & Filtering:** Live catalog search with case-insensitive matching across product titles, descriptions, and category tags.
* **Product Detail Views:** Detailed views displaying pricing, stock status, descriptions, specifications, and related items.
* **Dynamic Shopping Bag Drawer:** Slide-out interactive cart drawer backed by asynchronous REST API endpoints (`/api/cart/*`) for instant quantity updates and removals without full page reloads.
* **Guest & Authenticated Cart Continuity:** Seamless merging of unauthenticated guest cart sessions into the user account upon login.
* **Coupon & Discount Engine:** Server-side coupon verification (e.g. `DIWALI50`) calculating discount deductions, minimum order thresholds, and expiry checks.
* **Simulated Checkout & Payment Options:** Multi-mode checkout supporting Simulated Online Payment (demonstration UPI / Card flows) and Cash on Delivery (COD). No real credit card or sensitive financial data is ever collected or processed.
* **Customer Account Hub:** Customer self-service portal for managing delivery addresses, viewing order tracking histories, monitoring cancellations, and toggling product wishlists.
* **Self-Service Order Cancellation:** Customers can cancel orders that are in `Placed` status with automatic inventory restock; cancellations are strictly blocked once orders are marked `Shipped`.

### 🛡️ Administrator Operations Console
* **Protected Dashboard (`/admin`):** Real-time operational telemetry including gross sales volume, total orders count, pending shipments, cancelled order count, active products count, and low-stock alerts.
* **Inventory & Product Management:** Add new products, update catalog metadata, restock warehouse inventory units, and toggle active/inactive listing status.
* **Order Fulfillment Pipeline:** Inspect customer orders, filter by status, and update lifecycle transitions (`Placed` &rarr; `Confirmed` &rarr; `Shipped` &rarr; `Out for Delivery` &rarr; `Delivered`).
* **Cancellations & Refunds Desk:** Centralized audit desk for reviewing customer cancellation requests and tracking inventory rollbacks.
* **Campaign & Coupon Management:** Inspect marketing campaigns, promotional banner highlights, and manage discount vouchers.
* **Support Ticket Desk:** Track and resolve customer inquiries and support tickets.
* **Secure Admin Provisioning:** Dedicated Administrator Login and key-protected Admin Registration (`/auth/admin/register`) requiring an authorized security passkey.

---

## 🛠️ Technologies Used

| Domain | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.11+ / Flask 3.1 | Application routing, request handling, template rendering |
| **ORM & Database** | Flask-SQLAlchemy 3.1 / SQLite (Default) | Relational database abstraction and data persistence |
| **Production WSGI** | Gunicorn 22.0+ | Production multi-worker WSGI HTTP server |
| **Password Security** | Werkzeug Security | Secure cryptographic password hashing (PBKDF2/SHA-256) |
| **Frontend UI** | Semantic HTML5, CSS3, Vanilla JavaScript | Responsive glassmorphic UI, theme toggle, asynchronous cart drawer |
| **Typography & Icons** | Google Fonts (*Plus Jakarta Sans*, *Inter*) | Modern design system typography |
| **Test Suite** | Pytest 8.3+ | Automated testing for routes, models, services, and authorization |
| **Containerization** | Docker / Dockerfile | Standardized containerized runtime environment |
| **Cloud Deployment** | Render / Railway / Procfile / render.yaml | Continuous cloud deployment and orchestration |

---

## 📂 Project Folder Structure

```text
KARTMART/
├── app/
│   ├── models/                # SQLAlchemy database models
│   │   ├── __init__.py        # Model exports
│   │   ├── address.py         # Customer address book
│   │   ├── campaign.py        # Marketing campaigns & promotions
│   │   ├── cart.py            # Cart & CartItem models
│   │   ├── category.py        # Product categories
│   │   ├── coupon.py          # Discount coupons & promo codes
│   │   ├── notification.py    # In-app notifications
│   │   ├── order.py           # Orders, OrderItems, status tracking
│   │   ├── payment.py         # Simulated payment records
│   │   ├── product.py         # Products & inventory
│   │   ├── review.py          # Customer ratings & reviews
│   │   ├── support.py         # Customer support tickets
│   │   ├── user.py            # User accounts & RBAC roles
│   │   ├── variant.py         # Product variations (sizes, colors)
│   │   └── wishlist.py        # Customer wishlist records
│   ├── routes/                # Blueprint controller modules
│   │   ├── __init__.py        # Blueprint registrations
│   │   ├── account.py         # User profile, addresses, wishlist
│   │   ├── admin.py           # Protected admin console & management
│   │   ├── api.py             # Asynchronous JSON APIs (Cart, Health)
│   │   ├── auth.py            # Customer & Admin login/register/logout
│   │   ├── cart.py            # Full shopping bag view & actions
│   │   ├── checkout.py        # Checkout workflow & order placement
│   │   ├── orders.py          # Customer order history & tracking
│   │   ├── products.py        # Storefront, search & catalog views
│   │   └── support.py         # Help center & policies
│   ├── services/              # Domain business logic & state machines
│   │   ├── __init__.py
│   │   ├── cart_service.py    # Cart calculations & guest merges
│   │   ├── inventory_service.py # Stock allocation & restock
│   │   └── order_service.py   # Order placement & status updates
│   ├── static/                # Static assets
│   │   ├── css/style.css      # Comprehensive design system stylesheet
│   │   ├── js/main.js         # Cart drawer, theme switcher, notifications
│   │   └── img/               # Category & product image assets
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── account/           # Profile, address book, wishlist, cancellation views
│   │   ├── admin/             # Dashboard, inventory, orders, campaigns, support
│   │   ├── auth/              # Customer & Admin login and register pages
│   │   ├── support/           # Help center, privacy policy, terms
│   │   ├── base.html          # Global layout template
│   │   ├── catalogue.html     # Product catalog & filter UI
│   │   ├── checkout.html      # Multi-step checkout UI
│   │   ├── index.html         # Homepage hero & category showcases
│   │   ├── orders.html        # Order history UI
│   │   └── product_detail.html# Product detail view
│   ├── config.py              # Application configuration environments
│   ├── extensions.py          # SQLAlchemy extension instance
│   └── __init__.py            # Application Factory (`create_app`)
├── docs/                      # Architectural & project documentation
│   ├── ARCHITECTURE.md        # System architecture & data flow
│   ├── IMPLEMENTATION_PLAN.md # Development roadmap & milestones
│   ├── PROJECT_BRIEF.md       # Project brief & domain specifications
│   ├── QUALITY_AND_RELEASE.md # Quality metrics, test plans & release notes
│   ├── REQUIREMENTS.md        # Detailed functional & non-functional requirements
│   └── phase_prompt.md        # Detailed phase instructions
├── instance/                  # Local runtime database (excluded from Git)
├── tests/                     # Automated Pytest suite
│   ├── __init__.py
│   └── test_app.py            # Comprehensive test suite (16 tests)
├── .env.example               # Template environment configuration file
├── .gitignore                 # Git ignore file for secrets and virtual environments
├── Dockerfile                 # Container build specification
├── Procfile                   # Cloud process execution command
├── pytest.ini                 # Pytest test discovery settings
├── render.yaml                # Render cloud deployment blueprint
├── requirements.txt           # Python dependency specifications
├── run.py                     # Local development entry point
└── seed_catalog_expanded.py   # Catalog & demo data seeder script
```

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
* **Python:** Version 3.10, 3.11, or 3.12 installed.
* **Git:** Installed on your workstation.

### 2. Clone the Repository
```bash
git clone https://github.com/rahulspc08-ship-it/KARTMART-Smart-E-Commerce-System.git
cd KARTMART-Smart-E-Commerce-System
```

### 3. Create and Activate a Virtual Environment

* **On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

* **On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Copy `.env.example` to create your local `.env` file:
```bash
cp .env.example .env
```
*(On Windows PowerShell: `Copy-Item .env.example .env`)*

You can customize runtime variables such as `SECRET_KEY`, `FLASK_ENV`, and `DATABASE_URL`. By default, the application runs on SQLite (`sqlite:///kartmart.db`) with zero external database installation required.

### 6. Seed the Database
Populate all 13 categories, 30+ products, promotional coupons, and initial test accounts:
```bash
python seed_catalog_expanded.py
```

### 7. Run the Application
Start the local development server:
```bash
python run.py
```
The server will start at: **`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests

The project includes automated integration and unit tests covering user registration, authentication boundaries, cart manipulation, checkout, order cancellations, coupon engine validation, and administrative access control.

Execute the test suite with:
```bash
pytest
```
*All 16 tests should pass successfully.*

---

## 📸 Screenshots

> *Project screenshots can be captured from the running application and referenced under `docs/screenshots/`.*

| Section | Description |
| :--- | :--- |
| **Storefront & Hero Banner** | Dark/light glassmorphic hero showcasing festive Diwali sales and category navigation pills |
| **Product Catalogue & Search** | 13-category product grid with search queries and stock indicators |
| **Sliding Cart Drawer** | Asynchronous cart drawer displaying order subtotal, item quantities, and checkout buttons |
| **Simulated Checkout** | Delivery address form, coupon code verification, and simulated payment selector |
| **Admin Operations Console** | Telemetry overview cards, low-stock alerts, product restock, and order status transitions |

---

## ⚠️ Current Implementation Limitations

To maintain academic and demonstration honesty, the following constraints are explicitly documented:
* **Simulated Payments:** The application does not connect to live banking networks or commercial payment gateways (such as Stripe or Razorpay). All online payments are simulated for demonstration safety.
* **In-Process Recommendations:** Product relationships are dynamically rendered via category clustering rather than an external distributed AI recommendation engine.
* **Synchronous Notifications:** In-app and order notices are processed synchronously; an external asynchronous task queue (e.g., Celery/Redis) is not bundled.
* **Default Database:** By default, the application runs on an embedded SQLite database suitable for single-instance demonstrations. While SQLAlchemy models support MySQL via PyMySQL, MySQL is not pre-configured as the active default in the repository.

---

## 🔮 Future Enhancements

* **Production Payment Gateway Integration:** Secure integration with Stripe / Razorpay webhooks using verified sandbox keys.
* **AI-Powered Recommendation Microservice:** Collaborative filtering model trained on customer purchase patterns.
* **Live Courier Tracking APIs:** Webhook integration with logistics providers (e.g. Shiprocket, BlueDart).
* **Automated Email & SMS Notifications:** Asynchronous background dispatch of order confirmation receipts via SendGrid/Twilio.
* **Multi-Vendor Marketplace Support:** Vendor dashboard allowing third-party sellers to list products and fulfill orders.

---

## 👤 Author Information

* **Developer:** **D. Rahul Sai Teja**
* **Roll Number:** **5241412014**
* **Institution:** **Gayatri Vidya Parishad College for Degree and PG Courses (A)**
* **Repository:** [KARTMART-Smart-E-Commerce-System](https://github.com/rahulspc08-ship-it/KARTMART-Smart-E-Commerce-System)

---

## 📄 License
This project is developed for educational and academic mini-project demonstration purposes. All rights reserved &copy; 2026.
