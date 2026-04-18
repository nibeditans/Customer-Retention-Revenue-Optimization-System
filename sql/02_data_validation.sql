-- ======================
-- ROW COUNT VALIDATION
-- ======================

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions
UNION ALL
SELECT 'interactions', COUNT(*) FROM interactions;


-- ==================
-- DUPLICATE CHECKS
-- ==================

-- Customers
SELECT customer_id, COUNT(*)
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Products
SELECT product_id, COUNT(*)
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;

-- Transactions
SELECT transaction_id, COUNT(*)
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- Interactions
SELECT customer_id, interaction_type, interaction_timestamp, COUNT(*)
FROM interactions
GROUP BY customer_id, interaction_type, interaction_timestamp
HAVING COUNT(*) > 1;

-- Max Duplicate Count
SELECT MAX(cnt) AS max_duplicate_count
FROM (
    SELECT COUNT(*) AS cnt
    FROM interactions
    GROUP BY customer_id, interaction_type, interaction_timestamp
) t;


-- ==================
-- NULL VALUE CHECK
-- ==================

-- Customers
SELECT 
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(customer_id) AS null_customer_id,
	COUNT(*) - COUNT(signup_date) AS null_signup_date,
	COUNT(*) - COUNT(customer_segment) AS null_customer_segment,
	COUNT(*) - COUNT(location) AS null_location,
	COUNT(*) - COUNT(acquisition_channel) AS null_channel,
    COUNT(*) - COUNT(age) AS null_age,
    COUNT(*) - COUNT(gender) AS null_gender
FROM customers;

-- Products
SELECT 
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(product_id) AS null_product_id,
    COUNT(*) - COUNT(category) AS null_category,
    COUNT(*) - COUNT(price) AS null_price,
	COUNT(*) - COUNT(cost) AS null_cost,
	COUNT(*) - COUNT(launch_date) AS null_date
FROM products;

-- Interactions
SELECT 
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(interaction_id) AS null_interaction_id,
    COUNT(*) - COUNT(customer_id) AS null_customer_id,
    COUNT(*) - COUNT(interaction_type) AS null_type,
	COUNT(*) - COUNT(product_id) AS null_product_id,
    COUNT(*) - COUNT(interaction_timestamp) AS null_timestamp,
    COUNT(*) - COUNT(channel) AS null_channel
FROM interactions;

/*
What our query actually tells us?
• COUNT(*) = ~250,000
• NULL product_id = 74,945

So non-null product_id ≈ 175,055 (~70%)

That means:
• ~70% interactions have a product_id → product-related
• ~30% have NULL product_id → general engagement
*/

-- Transactions
SELECT 
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(transaction_id) AS null_transaction_id,
    COUNT(*) - COUNT(customer_id) AS null_customer_id,
    COUNT(*) - COUNT(product_id) AS null_product_id,
	COUNT(*) - COUNT(transaction_date) AS null_date,
    COUNT(*) - COUNT(quantity) AS null_quantity,
    COUNT(*) - COUNT(price) AS null_price,
    COUNT(*) - COUNT(discount) AS null_discount
FROM transactions;


-- =============================
-- REFERENTIAL INTEGRITY CHECK
-- =============================

-- Interactions ↠ Customers
SELECT COUNT(*) AS invalid_customer_refs
FROM interactions i
LEFT JOIN customers c 
    ON i.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Interactions ↠ Products
SELECT COUNT(*) AS invalid_product_refs
FROM interactions i
LEFT JOIN products p 
    ON i.product_id = p.product_id
WHERE i.product_id IS NOT NULL
  AND p.product_id IS NULL;

/*
Why ONLY when product_id is NOT NULL?

Because:
• We already KNOW NULL is valid (non-product interactions)
• So we only validate existing references
*/

-- Transactions ↠ Customers
SELECT COUNT(*) AS invalid_customer_refs
FROM transactions t
LEFT JOIN customers c 
    ON t.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Transactions ↠ Products
SELECT COUNT(*) AS invalid_product_refs
FROM transactions t
LEFT JOIN products p 
    ON t.product_id = p.product_id
WHERE p.product_id IS NULL;
