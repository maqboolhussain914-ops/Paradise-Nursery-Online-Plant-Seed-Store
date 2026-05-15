# Version Control Doc - DB Lab

**Group Name:** Paradise Nursery Group
**Members:** Maqbool Hussain & [Partner Name - Please Fill In]
**GitHub Repository Link:** [https://github.com/maqboolhussain914-ops/Paradise-Nursery-Online-Plant-Seed-Store](https://github.com/maqboolhussain914-ops/Paradise-Nursery-Online-Plant-Seed-Store)

---

## 1. Updated ERD Diagram
*(Please insert your ERD diagram image here from your original `Paradise Nursery ERD.docx` document after updating it to match the final schema)*

---

## 2. Normalization Walkthrough (1NF to 3NF)

**Initial Schema Considerations**
Based on standard, unnormalized data models, the initial conceptual schema had the following issues:
1. `Users` table contained composite fields like full name and combined address blocks.
2. `Products` table had category information stored directly alongside product details.
3. Order-product relationships required a bridging table with its own distinct attributes.

**First Normal Form (1NF)**
- **Issue:** The `Users` table originally had non-atomic attributes such as a combined `Name` and a combined `Address` block.
- **Change Made:** Split `Name` into `first_name` and `last_name`. Split `Address` into `street_address`, `city`, `state`, and `zip_code`. Ensured `phone` contains only a single phone number.
- **Justification:** 1NF requires atomicity. By breaking down the name and address, we allow for easier querying (e.g., finding all users in a specific `city` or sorting by `last_name`).

**Second Normal Form (2NF)**
- **Issue:** The relationship between `Orders` and `Products` requires a bridging table, `Order_Items`. Initially, if `Order_Items` used a composite primary key of `(order_id, product_id)`, including `product_name` or `product_current_price` in the `Order_Items` table would create a partial dependency.
- **Change Made:** We added a surrogate primary key `order_item_id` to the `Order_Items` table. We ensured that product-specific information (like `name` and `description`) remains strictly in the `Products` table. We only kept `price_at_purchase` in `Order_Items`.
- **Justification:** This eliminates partial dependencies. We only keep `price_at_purchase` in `Order_Items` because the price of a product can change over time, and the order needs to reflect the historical price at the time of purchase.

**Third Normal Form (3NF)**
- **Issue:** In the `Products` table, storing both `category_name` and `category_description` alongside product details creates a transitive dependency.
- **Change Made:** We created a separate `Categories` table with `category_id` (PK), `category_name`, and `description`. The `Products` table was updated to include a `category_id` foreign key.
- **Justification:** This removes the transitive dependency. If a category name changes, we only need to update it once in the `Categories` table, rather than updating every individual product belonging to that category in the `Products` table.

---

## 3. Dataflow Description

**1. Data Entry (Inputs)**
Data enters the system through two primary actors:
- **Customers:** When a new user signs up, their profile and contact information flow into the `users` table. 
- **Administrators:** Admins manage the catalog. When they add new plant or seed categories, data is inserted into the `categories` table. When they add new inventory, data flows into the `products` table, referencing the appropriate `category_id`.

**2. Active Shopping (Temporary State)**
When a logged-in customer browses the catalog and adds a plant to their cart:
- A new record is created in the `cart` table if the user doesn't already have an active cart.
- Specific items selected flow into the `cart_items` table. This table references both the `cart` (and by extension the user) and the `products` they wish to purchase. 
- Data in the `cart_items` table is highly mutable; quantities change frequently as the user adjusts their basket.

**3. Order Processing (Transactional Flow)**
Upon checkout, the data transitions from a temporary state to a permanent, immutable record:
- An order record is generated in the `orders` table, pulling the user's shipping address and calculating the final `total_amount`.
- Data flows from `cart_items` into `order_items`. Crucially, the system captures the `price_at_purchase` from the `products` table at this exact moment. This ensures that future price changes do not alter historical order records.
- Once the transfer is complete, the corresponding records in the `cart` and `cart_items` tables are deleted (or marked as inactive).

**4. Output & Reporting (Outputs)**
Data leaves the system in several formats:
- **User Dashboard:** Customers query the `orders` and `order_items` tables to view their order history and current shipping status.
- **Admin Analytics:** Admins query aggregated data from `orders` to determine total revenue, and query `products` and `categories` to generate low-stock alerts.
