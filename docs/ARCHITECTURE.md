# ARCHITECTURE.md

## 1. Architecture Status

**Status:** Proposed architecture awaiting review.

The system should use a simple, modular architecture appropriate for an intermediate software engineering project.

The selected stack must not be changed materially without explaining the reason and obtaining the owner's approval.

## 2. Technology Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Backend

* Python
* Flask

### Database

* MySQL Community Server

### Database Access

The project will use one consistent database-access approach:

* Parameterized SQL with a maintained MySQL driver, or
* SQLAlchemy with a suitable MySQL driver.

The final approach must be selected and documented before implementation.

### Development

* Google Antigravity on Windows
* Git for version control
* MySQL Workbench for database inspection
* Chrome or Microsoft Edge for browser testing

### Testing

* pytest or another documented Python testing framework
* Integration tests for database-backed behavior
* Manual browser tests
* Optional browser automation after the initial application is stable

## 3. High-Level Components

### 3.1 Browser Interface

Responsible for:

* Product catalogue display
* Search and filtering
* Product details
* Shopping cart interactions
* Checkout forms
* Order history
* Administrator screens
* Form validation feedback and user messages

### 3.2 Flask Application

Responsible for:

* HTTP routes
* Request validation
* Authentication and sessions
* Authorization
* Business logic coordination
* Error handling
* Rendering responses

### 3.3 Business Logic

Responsible for:

* Product operations
* Cart calculations
* Price validation
* Stock validation
* Order creation
* Inventory updates
* Simulated payment behavior
* Order status management
* Sales-summary calculations

### 3.4 Database Access

Responsible for:

* Reading and writing application records
* Parameterized queries or ORM operations
* Transaction management
* Mapping application operations to database records

### 3.5 MySQL Database

Stores customers, administrators, products, categories, orders, and related records.

### 3.6 Test Suite

Verifies business rules, database interactions, authorization, and important application workflows.

## 4. Proposed Data Model

The exact schema must be finalized after reviewing the owner's existing diagrams.

Potential entities include:

### Users

Stores customer and administrator accounts.

Potential fields:

* User ID
* Name
* Email
* Password hash
* Role
* Account status
* Created timestamp

### Categories

Stores product categories.

Potential fields:

* Category ID
* Category name
* Description

### Products

Stores catalogue items.

Potential fields:

* Product ID
* Category ID
* Product name
* Description
* Price
* Image URL
* Stock quantity
* Active status
* Created and updated timestamps

### Cart Items

The cart may be session-backed or database-backed. The final strategy must be documented before implementation.

### Orders

Stores order-level information.

Potential fields:

* Order ID
* Customer ID
* Order reference
* Delivery/contact details
* Total amount
* Payment method
* Simulated payment outcome, if applicable
* Order status
* Created timestamp

### Order Items

Stores products purchased in each order.

Potential fields:

* Order item ID
* Order ID
* Product reference where appropriate
* Product-name snapshot
* Unit-price snapshot
* Quantity
* Line total

The schema may be adjusted after diagram review.

## 5. Data Integrity Rules

* Passwords must never be stored in plaintext.
* Money must use an appropriate fixed-precision representation.
* Order items should preserve the price at the time of purchase.
* Foreign keys and appropriate constraints must be used.
* Stock values must not become negative.
* Checkout must revalidate stock and prices.
* Related order and inventory changes must be handled consistently.
* Prefer deactivating products over deleting records needed by historical orders.
* Payment-card details must never be stored.

## 6. Main Application Flows

### Catalogue Flow

1. Browser requests products.
2. Flask validates search and filter parameters.
3. The application queries MySQL.
4. Results are returned to the browser.
5. The interface displays products or an appropriate empty/error state.

### Cart Flow

1. Customer selects a product.
2. The server validates the product and quantity.
3. The cart is updated using the approved persistence strategy.
4. The server calculates totals using trusted prices.
5. The interface displays the updated cart.

### Checkout Flow

1. The authenticated customer submits checkout details.
2. The server validates the cart.
3. Prices and inventory are rechecked.
4. A database transaction creates the order and order items and updates inventory consistently.
5. The selected payment method and simulated outcome, where relevant, are recorded.
6. The customer receives an order confirmation.

### Administration Flow

1. The administrator authenticates.
2. Flask verifies the administrator's role.
3. Administrative requests are validated.
4. Changes are stored in MySQL.
5. The application displays success or safe error messages.

## 7. Security Architecture

* Use established password-hashing facilities.
* Validate all important inputs on the server.
* Use parameterized database queries or appropriate ORM protections.
* Enforce administrator permissions on the server.
* Ensure customers can access only their own orders.
* Apply CSRF protection to state-changing browser forms where applicable.
* Keep secrets outside tracked source files.
* Use a local environment file or environment variables for development configuration.
* Exclude real environment files and credentials from Git.
* Do not expose internal stack traces to users.
* Do not collect or store real payment-card information.

## 8. Payment Architecture

The application will provide two options.

### Simulated Online Payment

A demonstration-only flow that records a simulated outcome.

It must not connect to a real payment gateway, collect payment-card information, or claim to have processed a real payment.

### Cash on Delivery

Records the customer's selected payment method and creates an order after the required validation.

The order status and payment-related fields must be defined consistently.

## 9. User Interface

The interface should include:

* Responsive navigation
* Product cards
* Search and category controls
* Product detail pages
* Shopping cart
* Checkout
* Order confirmation
* Customer order history
* Administrator dashboard
* Product and category management
* Inventory management
* Order management

The design should define loading, empty, error, success, disabled, and keyboard-focus states.

A separate DESIGN_SPEC.md may be added after the main requirements and existing diagrams are reviewed.

## 10. Development Environment

The application will be developed on Windows using Antigravity.

The project should use:

* A Python virtual environment
* A tracked dependency manifest
* A safe .env.example
* Local environment configuration
* Documented database initialization
* Repeatable setup and testing commands

Exact versions must be checked and recorded before implementation.

## 11. Architecture Decisions to Resolve

Before implementation, review and document:

1. Existing diagrams and any contradictions.
2. Database driver versus SQLAlchemy.
3. Session-backed versus database-backed shopping cart.
4. Flask-rendered pages versus JSON endpoints.
5. Order statuses and allowed transitions.
6. Administrator account provisioning.
7. Test runner and test database strategy.

Do not silently resolve material architectural decisions.

## 12. Deployment

The initial release is local-only.

Public deployment, production database configuration, external hosting, and production secrets are not approved as part of the initial milestone.

Any future deployment requires a separate owner-approved plan.
