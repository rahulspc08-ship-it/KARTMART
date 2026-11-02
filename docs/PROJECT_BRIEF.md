# PROJECT_BRIEF.md

## 1. Project Overview

**Project Name:** E-Commerce Shopping System

**Project Type:** Intermediate Software Engineering Mini Project

**Project Status:** Planning and documentation

**Initial Delivery Target:** A locally runnable responsive web application suitable for a laboratory demonstration.

**Development Environment:** Google Antigravity on Windows.

## 2. Problem Statement

Customers need a simple way to browse products, inspect product information, add products to a shopping cart, and place and review orders.

Administrators need a convenient way to manage products, categories, inventory, and customer orders.

The E-Commerce Shopping System will provide these capabilities through a responsive web application.

## 3. Target Users

### 3.1 Customer

Customers can browse the catalogue, search for products, manage their shopping cart, complete checkout, and view their orders.

### 3.2 Administrator

Administrators can manage products, categories, inventory, orders, and a basic sales summary.

### 3.3 Visitor

Visitors can browse publicly available products without creating an account.

## 4. Product Categories

The application may include the following categories:

* Electronics
* Clothing
* Accessories
* Books
* Home Products

Products will initially use externally hosted image URLs.

Image-upload infrastructure is outside the initial scope.

## 5. Project Objectives

The project aims to:

1. Build a functional e-commerce website.
2. Implement a responsive frontend.
3. Connect the frontend to a Python Flask backend.
4. Store application data in MySQL.
5. Implement customer authentication.
6. Implement product browsing and search.
7. Implement shopping cart and checkout functionality.
8. Support simulated online payment and Cash on Delivery.
9. Provide customer order history.
10. Provide administrator product and order management.
11. Apply appropriate validation, authorization, and database integrity controls.
12. Demonstrate software engineering practices through documentation, testing, and version control.

## 6. Proposed Technology Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Backend

* Python
* Flask

### Database

* MySQL Community Server

### Development Tools

* Google Antigravity
* Git
* MySQL Workbench
* Chrome or Microsoft Edge

### Testing

* pytest or another approved Python testing framework
* Manual browser testing
* Optional browser automation after the initial application is stable

## 7. Minimum Viable Product

The initial version should provide:

1. Customer registration and login.
2. Customer logout.
3. Product catalogue.
4. Product search and category filtering.
5. Product details.
6. Shopping cart operations.
7. Checkout and order creation.
8. Simulated online payment.
9. Cash on Delivery.
10. Order confirmation.
11. Customer order history.
12. Basic order-status tracking.
13. Administrator authentication and authorization.
14. Product and category management.
15. Inventory management.
16. Order management.
17. Basic sales summary.
18. Responsive layouts.
19. Automated tests for important business rules and security boundaries.
20. Documented local setup and demonstration instructions.

## 8. Constraints

* Keep the application appropriate for an intermediate-level project.
* Prefer free development tools.
* Use a single responsive web application.
* Avoid unnecessary frameworks and microservices.
* Do not integrate a real payment gateway.
* Do not store payment-card information.
* Do not require paid external services for the MVP.
* Keep the initial release local.
* Inspect and reconcile the owner's existing software engineering diagrams before implementation.

## 9. Out-of-Scope Features

The initial release will not include:

* Real payment processing
* Payment gateway integration
* Credit or debit card storage
* Courier or delivery-provider integration
* AI-based product recommendations
* Separate native Android or iOS applications
* Product image-upload infrastructure
* Multi-vendor marketplace functionality
* Public production deployment
* Advanced loyalty programs
* Complex promotional campaigns
* Advanced business analytics

These features may be considered later if the owner approves a scope change.

## 10. Success Criteria

The project will be considered ready for a local demonstration when:

* The application starts using documented instructions.
* Customers can register, log in, and log out.
* Customers can browse, search, and inspect products.
* Customers can add, update, and remove cart items.
* Checkout creates valid orders.
* Simulated payment and Cash on Delivery are handled correctly.
* Customers can view only their own orders.
* Administrators can manage products, stock, and orders.
* Server-side validation and authorization work.
* Core tests run successfully.
* Desktop and mobile-sized layouts are usable.
* Setup, test, and demonstration instructions are documented.

## 11. Assumptions

* The initial release is for local demonstration.
* A responsive website is sufficient for desktop and mobile browsers.
* The owner has already prepared software engineering diagrams.
* Product images will be supplied as URLs.
* Online payment is simulated and does not process real money.
* Exact dependency versions will be confirmed during environment preparation.

## 12. Open Questions

The following decisions must be resolved before implementation where they materially affect the project:

1. Do the existing diagrams match the requirements?
2. Does the course require particular database names or documentation formats?
3. Which order statuses are required?
4. Which database-access approach is most appropriate?
5. How should the initial administrator account be provisioned?

## 13. Scope Change Policy

Any material change to project scope, architecture, payment behavior, database design, or deployment must be recorded in the relevant project document and approved by the owner before implementation.
