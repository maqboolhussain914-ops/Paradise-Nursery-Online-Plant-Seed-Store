# Paradise Nursery - Dataflow Description

This document outlines the dataflow architecture for the Paradise Nursery Online Plant & Seed Store, satisfying Milestone 3 requirements.

## 1. Data Entry (Inputs)
Data enters the system through two primary actors:
- **Customers:** When a new user signs up, their profile and contact information flow into the `users` table. 
- **Administrators:** Admins manage the catalog. When they add new plant or seed categories, data is inserted into the `categories` table. When they add new inventory, data flows into the `products` table, referencing the appropriate `category_id`.

## 2. Active Shopping (Temporary State)
When a logged-in customer browses the catalog and adds a plant to their cart:
- A new record is created in the `cart` table if the user doesn't already have an active cart.
- Specific items selected flow into the `cart_items` table. This table references both the `cart` (and by extension the user) and the `products` they wish to purchase. 
- Data in the `cart_items` table is highly mutable; quantities change frequently as the user adjusts their basket.

## 3. Order Processing (Transactional Flow)
Upon checkout, the data transitions from a temporary state to a permanent, immutable record:
- An order record is generated in the `orders` table, pulling the user's shipping address and calculating the final `total_amount`.
- Data flows from `cart_items` into `order_items`. Crucially, the system captures the `price_at_purchase` from the `products` table at this exact moment. This ensures that future price changes do not alter historical order records.
- Once the transfer is complete, the corresponding records in the `cart` and `cart_items` tables are deleted (or marked as inactive/checked out).

## 4. Output & Reporting (Outputs)
Data leaves the system in several formats:
- **User Dashboard:** Customers query the `orders` and `order_items` tables to view their order history and current shipping status.
- **Admin Analytics:** Admins query aggregated data from `orders` to determine total revenue, and query `products` and `categories` to generate low-stock alerts.
