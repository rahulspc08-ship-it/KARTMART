# QUALITY_AND_RELEASE.md

## 1. Purpose

This document defines the quality checks required before the E-Commerce Shopping System can be considered ready for demonstration.

**Initial release target:** Local Windows demonstration.

**Public deployment:** Not approved.

**Current status:** Documentation and environment assessment.

## 2. Verification Principles

* Evidence is required for every claimed test result.
* Acceptance criteria must map to verification methods.
* Automated tests should cover important business rules.
* Manual browser testing should cover complete user journeys.
* Failed and skipped tests must be reported.
* An AI review or visual preview is not proof that tests passed.
* Known limitations must be documented honestly.

## 3. Unit Testing

Unit tests should cover:

* Input validation
* Cart calculations
* Quantity restrictions
* Product price calculations
* Stock validation
* Order totals
* Order status transitions
* Sales-summary calculations

## 4. Integration Testing

Integration tests should cover:

* Customer registration
* Duplicate email handling
* Login and logout
* Protected routes
* Product search and filtering
* Product details
* Cart validation
* Checkout
* Order creation
* Inventory updates
* Transaction failure behavior
* Customer order ownership
* Administrator authorization
* Product and category validation

Tests must use a dedicated test configuration and must not accidentally delete valuable development data.

Destructive test-database resets must be clearly separated from normal development operations.

## 5. End-to-End and Manual Testing

The following workflows must be checked:

1. Browse the product catalogue.
2. Search for a product.
3. Filter products by category.
4. Open product details.
5. Register a customer account.
6. Log in and log out.
7. Add products to the shopping cart.
8. Update quantities and remove items.
9. Complete checkout using simulated payment.
10. Complete checkout using Cash on Delivery.
11. View order confirmation.
12. View order history.
13. Confirm customers cannot access other customers' orders.
14. Confirm customers cannot access administrator functions.
15. Manage products and inventory as an administrator.
16. Manage orders as an administrator.
17. Check empty, validation, success, and error states.
18. Check the application in desktop and mobile-sized browser windows.

Browser automation may be introduced after the initial application and tests are stable.

## 6. Security Checks

Before the local demonstration:

* Passwords are hashed.
* Secrets are not committed to Git.
* Database queries are parameterized or safely handled by the selected ORM.
* Inputs are validated on the server.
* Administrator permissions are enforced on the server.
* Customers cannot access other customers' orders.
* Inventory and order totals are calculated using trusted server-side data.
* State-changing forms have appropriate CSRF protection where applicable.
* User-facing errors do not expose internal stack traces.
* No payment-card information is collected or stored.
* Simulated payment is clearly distinguished from real payment.

Passing these checks does not constitute formal security certification.

## 7. Accessibility and Responsive Design

Verify:

* Semantic HTML.
* Meaningful labels for form fields.
* Visible keyboard focus.
* Keyboard-accessible navigation.
* Appropriate image alternative text.
* Readable contrast.
* No essential hover-only actions.
* Usable desktop and mobile layouts.
* Clear loading, empty, error, success, and disabled states.

## 8. Environment Setup Documentation

The final project documentation must record tested versions and instructions for:

* Windows development environment
* Python
* Git
* MySQL Server
* MySQL Workbench
* Python virtual environment
* Dependency installation
* Environment variables
* Database initialization
* Seed data
* Application startup
* Automated testing

Actual credentials must never be placed in tracked files.

The .env.example file may contain configuration variable names and safe placeholder values only.

## 9. Quality Gates

### Gate A: Before Implementation

* All five core Markdown documents have been reviewed.
* Existing diagrams have been inspected or their absence recorded.
* Requirements and architecture agree.
* Material contradictions are resolved.
* Every Must requirement has acceptance criteria.
* Requirements map to implementation tasks and verification methods.
* The environment and repository baseline are understood.

### Gate B: Before Accepting a Development Slice

* Relevant tests have actually run.
* Test results have been inspected.
* Acceptance criteria have been checked.
* Changes have been reviewed.
* Secrets and unintended changes have been checked for.
* Documentation has been updated.
* Remaining defects are recorded.

### Gate C: Before Local Demonstration

* The setup instructions work.
* Database initialization is repeatable.
* Core customer workflows work.
* Administrator workflows work.
* Authentication and authorization checks pass.
* Checkout and inventory consistency checks pass.
* Simulated payment and COD behave correctly.
* No unaddressed critical defect remains.
* Known limitations are disclosed.
* Test evidence is recorded.
* Demonstration instructions are available.

## 10. Release and Recovery

The initial release is local-only.

* Public deployment is not authorized.
* Keep a known-good Git baseline.
* Back up valuable database data before risky changes.
* Obtain owner approval before destructive migrations or database resets.
* If a change breaks the application, record the failure and recover using a reviewed procedure.
* Never claim a release, deployment, or recovery occurred unless it was actually performed and verified.

Any future public deployment requires a separate approved plan.

## 11. Handover Checklist

* [ ] Project scope documented
* [ ] Architecture documented
* [ ] Database schema documented
* [ ] Setup instructions tested
* [ ] Run instructions documented
* [ ] Test instructions documented
* [ ] Database initialization documented
* [ ] Seed-data instructions documented
* [ ] Administrator setup documented safely
* [ ] Core requirements verified
* [ ] Known limitations recorded
* [ ] Git changes reviewed
* [ ] No secrets committed
* [ ] Local demonstration is reproducible

## 12. Test Evidence Log

Maintain a record of actual verification results.

| Check                   | Status  | Evidence                                 |
| ----------------------- | ------- | ---------------------------------------- |
| Environment assessment  | Pending | Not yet performed                        |
| Application startup     | Pending | Application not yet implemented          |
| Automated tests         | Pending | Test suite not yet implemented           |
| Database integration    | Pending | Database integration not yet implemented |
| Browser workflow checks | Pending | Application not yet implemented          |
| Security checks         | Pending | Application not yet implemented          |

Update this table only when checks have actually been performed.

Never convert a planned check into a passed check without evidence.
