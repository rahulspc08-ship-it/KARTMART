# REQUIREMENTS.md

## 1. Purpose

This document defines the functional and non-functional requirements of the E-Commerce Shopping System.

Requirements are prioritized as follows:

* **Must:** Required for the initial release.
* **Should:** Important but secondary.
* **Could:** Optional enhancement.
* **Won't:** Explicitly excluded from the initial release.

Every requirement must have observable acceptance criteria.

## 2. User Roles

### Visitor

Can browse the public product catalogue.

### Customer

Can authenticate, manage a shopping cart, place orders, and view their own order history.

### Administrator

Can manage products, categories, inventory, and orders.

## 3. Functional Requirements

### FR-01: Product Catalogue — Must

The system shall display active products.

Acceptance criteria:

* Products display their name, image, price, category, and availability.
* Broken image URLs do not break the page.
* An appropriate message appears when no products are available.
* Database errors are handled safely.

### FR-02: Product Search and Filtering — Must

The system shall support product search and category filtering.

Acceptance criteria:

* Search results correspond to the supplied search term.
* Customers can apply and clear category filters.
* No-match results display a useful message.
* Search inputs are validated safely.

### FR-03: Product Details — Must

The system shall provide a product detail view.

Acceptance criteria:

* The page displays product name, description, price, category, image, and stock availability.
* Unknown or inactive products display a safe not-found state.

### FR-04: Customer Registration — Must

Visitors shall be able to register as customers.

Acceptance criteria:

* Required fields are validated.
* Duplicate email addresses are rejected.
* Passwords are securely hashed.
* Plaintext passwords are never stored.
* Invalid submissions do not create accounts.

### FR-05: Customer Login and Logout — Must

Customers shall be able to authenticate and terminate their sessions.

Acceptance criteria:

* Valid credentials establish an authenticated session.
* Invalid credentials produce a safe error message.
* Protected routes require authentication.
* Logout invalidates the current session.

### FR-06: Shopping Cart — Must

Customers shall be able to add products, update quantities, and remove items.

Acceptance criteria:

* Quantities must be positive integers.
* Products must exist and be available.
* Quantities cannot exceed available stock at validation time.
* Prices and totals are calculated using trusted server-side data.
* Empty carts display an appropriate message.
* Cart persistence is documented in the architecture.

### FR-07: Checkout and Order Creation — Must

Authenticated customers shall be able to place orders using a valid cart.

Acceptance criteria:

* Checkout collects the agreed minimum delivery and contact details.
* Stock and prices are revalidated before order creation.
* Orders and order items are stored consistently.
* Related inventory updates are handled transactionally where appropriate.
* Successful checkout displays an order reference.
* Repeated submissions are handled to reduce duplicate orders.
* Invalid or unavailable items prevent checkout.

### FR-08: Payment Options — Must

The system shall offer:

1. Simulated online payment.
2. Cash on Delivery.

Acceptance criteria:

* Simulated payment is clearly identified as a demonstration feature.
* No real payment is processed.
* No card numbers or CVVs are collected or stored.
* Cash on Delivery is recorded as the selected payment method.
* The system does not claim that simulated payment represents a real financial transaction.

### FR-09: Customer Order History — Must

Customers shall be able to view their own orders.

Acceptance criteria:

* Orders show their reference, date, total, payment method, and status.
* Customers cannot access other customers' orders.
* Empty order histories are handled clearly.
* Order statuses and allowed transitions are documented.

### FR-10: Administrator Authentication — Must

Administrative operations shall be restricted to authorized administrators.

Acceptance criteria:

* Admin routes enforce server-side role checks.
* Customers cannot obtain admin privileges by modifying browser-side data.
* Unauthorized requests are rejected.
* Administrator account provisioning is documented.

### FR-11: Product and Category Management — Must

Administrators shall be able to create, view, update, and deactivate products and manage categories.

Acceptance criteria:

* Product fields are validated.
* Prices cannot be negative.
* Stock cannot be negative.
* Invalid category references are rejected.
* Historical orders remain consistent if a product is deactivated.

### FR-12: Inventory Management — Must

Administrators shall be able to update and view stock quantities.

Acceptance criteria:

* Stock quantities are non-negative integers.
* Cart and checkout operations respect inventory.
* Checkout handles stock changes that occur after a product was added to the cart.
* Inventory updates remain consistent with order creation.

### FR-13: Order Management — Must

Administrators shall be able to view orders and update their statuses.

Acceptance criteria:

* Orders display relevant reference, date, total, customer reference, payment method, and status.
* Only administrators can change order status.
* Invalid status transitions are rejected or handled according to the documented rules.
* Customers see status updates for their own orders.

### FR-14: Basic Sales Summary — Should

Administrators should be able to view a basic summary of orders.

Acceptance criteria:

* Summary calculations use documented rules.
* Cancelled orders are handled consistently.
* Summary values can be reconciled against stored order data.
* Simulated payment is not represented as actual collected revenue.

### FR-15: Responsive Interface — Must

The application shall be usable in desktop and mobile browsers.

Acceptance criteria:

* Navigation and essential pages remain usable at narrow viewport widths.
* Forms have meaningful labels.
* Keyboard focus is visible.
* Essential functionality does not depend on hover.
* Loading, empty, error, success, and disabled states are handled where applicable.

## 4. Non-Functional Requirements

### NFR-01: Security — Must

* Passwords must be hashed.
* Database operations must use parameterized queries or a suitable ORM.
* Input validation must occur on the server.
* Customer and admin authorization must be enforced on the server.
* Customers must not access other customers' orders.
* Secrets must not be committed to version control.
* Payment-card information must not be stored.
* User-facing errors must not expose internal stack traces.

### NFR-02: Data Integrity — Must

* Money must use a suitable fixed-precision database representation.
* Orders and order items must remain consistent.
* Checkout should use transactions for related database changes.
* Foreign keys and appropriate constraints must be used.
* Database initialization and seed-data instructions must be documented.
* Destructive database changes require owner approval.

### NFR-03: Maintainability — Must

* The application must use understandable modules and functions.
* Unnecessary complexity must be avoided.
* Setup and testing instructions must be documented.
* Architecture and implementation documentation must remain current.

### NFR-04: Compatibility — Must

* Support current Chrome and Microsoft Edge on Windows.
* Support desktop and mobile-sized browser viewports.
* Provide reproducible local setup instructions.

### NFR-05: Accessibility — Should

* Use semantic HTML.
* Provide form labels and meaningful image alternative text.
* Support keyboard navigation.
* Provide visible focus indicators.
* Maintain readable contrast.

### NFR-06: Performance — Should

* Avoid unnecessary database queries.
* Keep catalogue queries manageable.
* Introduce pagination if required by the catalogue size.
* Do not claim performance results without measurements.

## 5. Explicitly Excluded Features

The initial release excludes:

* Real payment processing
* Payment gateway integration
* Card-data storage
* Courier integrations
* AI recommendations
* Native mobile applications
* Public production deployment
* Product image uploads
* Multi-vendor marketplace functionality
* Advanced loyalty and promotional systems

## 6. Verification Mapping

Every Must requirement must map to:

1. An implementation task.
2. One or more acceptance criteria.
3. A test or reproducible manual verification.
4. Recorded evidence of the result.

Priority verification areas include authentication, authorization, cart totals, inventory, checkout integrity, customer order ownership, and administrator access.

## 7. Document Status

This is the proposed initial requirements baseline.

The owner must review it against the existing software engineering diagrams before implementation. Material contradictions must be reported and resolved explicitly.
