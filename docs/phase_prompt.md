# PHASE 0 — FOUNDATION AUDIT

Do not implement application features in this phase.

Inspect the current KARTMART workspace and verify the project's setup. Preserve all existing work.

### Tasks

1. Confirm the actual workspace path.
2. Inspect all five documentation files in `docs/` and report their existence and any important unresolved decisions.
3. Inspect `.gitignore`, `.env.example`, `requirements.txt`, and the `.venv` directory if present.
4. Verify Python, pip, Git, and the packages installed in the project's virtual environment.
5. Run `pip check` using the virtual environment.
6. Verify the current Git branch, working-tree status, Git identity configuration, and whether any commits exist.
7. Confirm that `.env` and `.venv` are ignored by Git.
8. Verify MySQL Server installation and service status, client availability, and whether the expected port is listening. Do not expose credentials.
9. Check whether MySQL Workbench is installed.
10. If MySQL is not available or its installation is still waiting for user approval, report it as blocked. Do not launch another installer or attempt to bypass a Windows security prompt.
11. Compare the installed dependencies against the intended MySQL + Flask-SQLAlchemy architecture. Identify missing packages or unnecessary/conflicting dependencies, but do not change dependencies without reporting the proposed change first.
12. Check whether the configured SQLAlchemy and MySQL driver versions can be imported successfully.

### Restrictions

* Do not write application code.
* Do not create a database or modify existing database data.
* Do not install software.
* Do not modify the five project documentation files.
* Do not change Git configuration or create commits.
* Do not print secret values.
* Do not create a SQLite application database.
* Do not work on diagrams.

### Acceptance criteria

Return a report that distinguishes Verified, Failed, and Blocked items. Include the actual commands used and their results.

Finish with a short list of prerequisites that the project owner must complete before implementation can begin. Wait for approval before proceeding to another phase.



# PHASE 1 — IMPLEMENTATION PLANNING

Read the five existing documentation files and the approved Phase 0 report.

Do not implement application features yet.

### Tasks

1. Review the existing requirements and architecture for contradictions, missing decisions, or technical risks.
2. Confirm Flask/Jinja2 server-rendered pages, vanilla JavaScript, Flask-SQLAlchemy, SQLAlchemy, PyMySQL, and MySQL as the agreed stack.
3. Plan a maintainable Flask application structure, including configuration, database models, routes or blueprints, templates, static assets, forms/validation, and tests.
4. Plan database entities and relationships for users, categories, products, cart items, orders, and order items. Include the fields and constraints needed for the agreed features.
5. Define customer and administrator authorization boundaries.
6. Define cart persistence and ownership rules.
7. Define checkout transaction behavior, server-side pricing, inventory validation, and order creation.
8. Define the simulated payment and COD workflows without collecting real payment credentials.
9. Define allowed order-status transitions and the restriction on cancelling shipped or delivered orders.
10. Define a practical testing strategy for models, authentication, access control, cart operations, checkout, stock handling, and administration.
11. Divide implementation into small vertical slices with clear acceptance criteria and dependencies.
12. Identify any dependency or documentation changes that should be approved before implementation.

### Restrictions

Do not implement the application, modify the database, install software, change the agreed stack, or silently rewrite project documentation.

If a requirement is ambiguous, explain the ambiguity and recommend a decision instead of inventing one.

### Deliverable

Provide a proposed implementation plan with:

* Proposed file and directory structure.
* Data model and relationships.
* Security and validation approach.
* Phase order and dependencies.
* Tests and acceptance criteria for each phase.
* Decisions requiring project-owner approval.

Wait for the project owner's review before implementing Phase 2.



# PHASE 2 — APPLICATION SKELETON

Implement only the approved application foundation and configuration.

### Tasks

1. Create the agreed Flask application structure.
2. Implement the application factory and configuration approach, if approved in Phase 1.
3. Load configuration from environment variables using the existing configuration dependencies.
4. Configure Flask-SQLAlchemy to use MySQL through the agreed SQLAlchemy/PyMySQL setup.
5. Keep secrets and credentials outside source control.
6. Add a minimal health or home route and a base Jinja2 template.
7. Add basic static CSS and a responsive page shell.
8. Add a clear, safe database-connection check suitable for development.
9. Add initial tests for application creation, configuration behavior, and the basic route.
10. Document setup instructions and environment variables without including real secrets.

### Restrictions

Do not implement full authentication, product management, shopping cart, checkout, payments, or admin functionality yet.

Do not substitute SQLite for the application database. If MySQL is unavailable, implement only the approved, independently testable parts and clearly mark database-dependent checks as blocked.

Do not overwrite existing project files without inspecting them first.

### Acceptance criteria

* The Flask application can be created using the agreed entry point.
* Configuration is not hard-coded with credentials.
* The basic route behaves as intended.
* Automated tests for the implemented foundation pass.
* MySQL connectivity is verified only if the server is actually available.
* Setup instructions accurately describe the current state.

Report changed files, commands, test results, and blockers. Wait for approval.



# PHASE 3 — DATABASE MODELS AND AUTHENTICATION

Implement the approved data models and account authentication.

### Tasks

1. Implement the approved SQLAlchemy models and relationships.
2. Add appropriate database constraints, indexes, and validation.
3. Implement customer registration, login, and logout.
4. Store passwords using a suitable secure password-hashing method.
5. Enforce unique account identifiers as defined in the approved requirements.
6. Implement session and authentication protections appropriate to Flask.
7. Prevent unauthenticated access to protected customer routes.
8. Implement administrator authorization using a secure role or equivalent approved design.
9. Ensure public registration cannot grant administrator privileges.
10. Use a safe, explicitly controlled process for creating the initial administrator account, without hard-coded production credentials.
11. Add tests for valid and invalid registration, login/logout, duplicate accounts, password verification, and access-control boundaries.

### Restrictions

Do not implement the full catalog, cart, checkout, or order management yet.

Do not print passwords, secret keys, or environment values. Do not silently reset or delete database tables or data.

Use the agreed MySQL database. Clearly report any tests that could not run because MySQL is unavailable.

### Acceptance criteria

Authentication works for the implemented routes, passwords are not stored in plaintext, and protected routes enforce server-side authorization. Automated tests cover the agreed authentication cases.

Report actual test results and wait for approval.



# PHASE 4 — PRODUCT CATALOG

Implement the customer-facing product catalog using the approved application architecture.

### Tasks

1. Implement category and product listing pages.
2. Implement individual product detail pages.
3. Support product search.
4. Support category filtering and approved sorting options.
5. Show price, description, stock availability, category, and product image.
6. Use image URLs and a graceful fallback when an image is unavailable.
7. Ensure inactive or unavailable products are handled appropriately.
8. Use server-side validation and safe database queries.
9. Implement responsive styling for desktop and mobile browsers.
10. Add tests for listing, search, category filtering, product details, and unavailable products.

### Restrictions

Do not implement product image uploads, external product feeds, AI recommendations, or unapproved third-party integrations.

Do not create fake test results or claim external image URLs were verified unless they were actually checked.

### Acceptance criteria

Customers can browse and search the catalog, view product details, and use the responsive interface. Tests cover the main catalog behavior.

Report changed files, tests, and known limitations. Wait for approval.



# PHASE 5 — DATABASE-BACKED SHOPPING CART

Implement the approved persistent shopping-cart functionality.

### Tasks

1. Allow authenticated customers to add available products to their carts.
2. Persist cart contents in MySQL.
3. Allow customers to change quantities and remove items.
4. Display current product information and calculated subtotals.
5. Validate quantities and product availability on the server.
6. Ensure a customer cannot access or modify another customer's cart.
7. Recalculate all prices and totals on the server.
8. Handle inactive products and insufficient stock safely.
9. Add tests for add, update, remove, persistence, ownership, invalid quantities, and unavailable products.

### Restrictions

Do not trust prices, totals, customer IDs, or stock values submitted by the browser.

Do not implement checkout or payment yet. Do not switch to session-only cart storage or SQLite.

### Acceptance criteria

Cart contents persist in the database, cart ownership is enforced, and all calculations and validation occur server-side.

Report the tests actually run and wait for approval.



# PHASE 6 — CHECKOUT, ORDERS, AND SIMULATED PAYMENTS

Implement the approved checkout and order workflow.

### Tasks

1. Collect and validate the required shipping details.
2. Offer simulated online payment and Cash on Delivery.
3. Never collect or store real card numbers, CVVs, banking passwords, or payment credentials.
4. Clearly label online payment as simulated and never claim that real money was charged.
5. Recalculate item prices and order totals on the server.
6. Validate stock and product availability at checkout.
7. Create the order and order items safely, using database transactions where needed.
8. Preserve the ordered product descriptions, quantities, and prices in order records as appropriate.
9. Prevent duplicate submissions from creating unintended duplicate orders where practical.
10. Update inventory consistently and handle insufficient stock.
11. Clear or update the cart only after successful order creation.
12. Implement customer order history and order-detail pages.
13. Enforce order ownership.
14. Implement the agreed order statuses and valid transitions.
15. Prevent cancellation after Shipped or Delivered.
16. Add tests for successful checkout, insufficient stock, invalid shipping data, transaction failure handling, order ownership, payment-mode behavior, and status transitions.

### Restrictions

No real payment gateway, delivery integration, or real financial transactions.

Do not claim concurrency or overselling protection is verified unless the relevant tests were actually performed.

Do not delete or reset existing order data.

### Acceptance criteria

Orders are created consistently, totals are calculated server-side, inventory is handled safely, customers can view only their own orders, and simulated payment is clearly identified.

Report tests and limitations. Wait for approval.



# PHASE 7 — ADMIN DASHBOARD AND MANAGEMENT

Implement the approved administrative functionality.

### Tasks

1. Implement a protected admin dashboard.
2. Allow authorized administrators to create, view, edit, and deactivate or delete products as appropriate.
3. Implement category management.
4. Allow administrators to manage prices, stock, descriptions, and image URLs.
5. Allow administrators to view orders and update their statuses using the approved transition rules.
6. Display a basic sales summary based on actual database records.
7. Enforce server-side administrator authorization for every admin operation.
8. Validate all input and handle missing or invalid records gracefully.
9. Add tests for unauthorized access, product management, category management, inventory changes, order updates, and sales-summary calculations.

### Restrictions

Do not rely on hiding navigation links as an access-control mechanism.

Do not expose customer passwords or secrets. Do not silently delete order history. Do not introduce unapproved business features.

### Acceptance criteria

Only authorized administrators can access administrative operations. Product, category, inventory, order, and summary functions behave according to the approved requirements.

Report actual test results and wait for approval.



# PHASE 8 — QUALITY ASSURANCE AND RESPONSIVE POLISH

Review and improve the implemented application without changing the approved scope.

### Tasks

1. Run the complete automated test suite.
2. Fix reproducible defects found in the implemented functionality.
3. Review authentication, authorization, CSRF protection, input validation, output escaping, and secret handling.
4. Review cart ownership, order ownership, server-side totals, inventory updates, and order-status rules.
5. Check application error handling and user-facing messages.
6. Review responsive layouts at representative desktop and mobile viewport sizes using available tools.
7. Check forms, navigation, empty states, invalid inputs, and unavailable images.
8. Review database configuration and setup instructions.
9. Check Git ignore rules for secrets, databases, virtual environments, caches, and generated artifacts.
10. Run dependency-integrity checks and report relevant warnings.
11. Update the quality documentation to reflect the actual checks performed.

### Restrictions

Do not add unrelated features, change the agreed stack, remove tests just to obtain a passing result, or claim browser/device testing that was not performed.

Do not expose secrets in screenshots, logs, or reports.

### Acceptance criteria

Report test counts and outcomes from actual execution, unresolved defects, untested scenarios, dependency warnings, and responsive checks performed. Clearly separate verified results from assumptions.

Wait for approval before the release-readiness phase.



# PHASE 9 — DOCUMENTATION AND RELEASE READINESS

Prepare the project for a local demonstration and handoff. Public deployment is out of scope.

### Tasks

1. Review and update setup documentation based on the actual implemented application.
2. Document prerequisites, virtual-environment setup, dependency installation, MySQL setup, environment configuration, database initialization, and the development start command.
3. Explain how the initial administrator is provisioned without including real credentials.
4. Document customer and admin workflows.
5. Document how to run the automated tests.
6. Document simulated payment behavior and its limitations.
7. Document known defects, unverified behavior, and limitations.
8. Review the Git working tree and confirm that no secrets or local database files are staged.
9. If the project owner explicitly asks for a commit, show the proposed staged-file list first and commit only after approval.
10. Provide a final, evidence-based project status report.

### Restrictions

Do not deploy publicly, push to a remote repository, buy services, or change permissions without explicit approval.

Do not claim the application is production-ready merely because it works locally.

Do not commit secrets or user-specific environment files.

### Acceptance criteria

A beginner can follow the documented steps to set up and run the application locally, subject to the documented prerequisites. The final report distinguishes verified functionality from limitations and untested behavior.

Wait for the project owner's review.


