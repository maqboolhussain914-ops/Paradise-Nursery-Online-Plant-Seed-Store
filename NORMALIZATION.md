# Database Normalization Walkthrough (1NF to 3NF)

This document provides the formal justification for the normalization of the Paradise Nursery database schema, satisfying Milestone 2 requirements.

## Initial Schema Considerations
Based on standard, unnormalized data models, the initial conceptual schema had the following issues:
1. `Users` table contained composite fields like full name and combined address blocks.
2. `Products` table had category information stored directly alongside product details.
3. Order-product relationships (many-to-many) required a bridging table with its own distinct attributes.

## First Normal Form (1NF)
**Goal:** Ensure all attributes are atomic, with a primary key for each row, and no repeating groups.

**Issues Addressed:** 
- The `Users` table originally had non-atomic attributes such as a combined `Name` and a combined `Address` block.
- **Change Made:** Split `Name` into `first_name` and `last_name`. Split `Address` into `street_address`, `city`, `state`, and `zip_code`. Ensured `phone` contains only a single phone number.
- **Justification:** 1NF requires atomicity. By breaking down the name and address, we allow for easier querying (e.g., finding all users in a specific `city` or sorting by `last_name`).

## Second Normal Form (2NF)
**Goal:** Ensure 1NF is met, and remove partial dependencies (where an attribute depends on only part of a composite primary key).

**Issues Addressed:**
- The relationship between `Orders` and `Products` requires a bridging table, `Order_Items`. Initially, if `Order_Items` used a composite primary key of `(order_id, product_id)`, including `product_name` or `product_current_price` in the `Order_Items` table would create a partial dependency (as these depend solely on `product_id`, not the order itself).
- **Change Made:** We added a surrogate primary key `order_item_id` to the `Order_Items` table. We ensured that product-specific information (like `name` and `description`) remains strictly in the `Products` table. We only kept `price_at_purchase` in `Order_Items`, as the price of a product can change over time, and the order needs to reflect the historical price at the time of purchase. This is fully dependent on the specific order item.
- **Justification:** This eliminates partial dependencies and ensures that updating a product's name only needs to happen in one place (the `Products` table).

## Third Normal Form (3NF)
**Goal:** Ensure 2NF is met, and remove transitive dependencies (where a non-key attribute depends on another non-key attribute).

**Issues Addressed:**
- In the `Products` table, storing both `category_name` and `category_description` alongside product details creates a transitive dependency, as these depend on the category, not the specific product.
- **Change Made:** We created a separate `Categories` table with `category_id` (PK), `category_name`, and `description`. The `Products` table was updated to include a `category_id` foreign key.
- **Justification:** This removes the transitive dependency. If a category name changes, we only need to update it once in the `Categories` table, rather than updating every individual product belonging to that category in the `Products` table.

## Final Schema (3NF Compliant)
The final schema consists of the following 7 tables:
1. `users` (user_id PK)
2. `categories` (category_id PK)
3. `products` (product_id PK, category_id FK)
4. `orders` (order_id PK, user_id FK)
5. `order_items` (order_item_id PK, order_id FK, product_id FK)
6. `cart` (cart_id PK, user_id FK)
7. `cart_items` (cart_item_id PK, cart_id FK, product_id FK)
