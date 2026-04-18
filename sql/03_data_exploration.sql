-- =================================
-- CUSTOMER & TRANSACTION OVERVIEW
-- =================================

-- 1. Total Customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Total Transactions
SELECT COUNT(*) AS total_transactions
FROM transactions;

-- 3. Total Revenue
SELECT SUM(price * quantity * (1 - discount)) AS total_revenue
FROM transactions;

-- 4. Average Order Value (AOV)
SELECT 
    SUM(price * quantity * (1 - discount)) / COUNT(*) AS avg_order_value
FROM transactions;

-- 5. Unique Purchasing Customers
SELECT COUNT(DISTINCT customer_id) AS purchasing_customers
FROM transactions;

/*
• Large inactive population: 6998 users ↠ no purchase
• Small revenue-driving group: 1002 users ↠ all revenue

=> Conversion Rate = 12.5%
Most users don't buy, only a subset converts.

This is exactly what businesses look like in real-world.
*/


-- ================================
-- CUSTOMER ACTIVITY SEGMENTATION
-- ================================

-- Customers who made at least one purchase
SELECT 
    CASE 
        WHEN t.customer_id IS NOT NULL 
			THEN 'Buyer'
        ELSE 'Non-Buyer'
    END AS customer_type,
    COUNT(DISTINCT c.customer_id) AS customer_count
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY customer_type;

-- Customers with interactions vs no interactions
SELECT 
    CASE 
        WHEN i.customer_id IS NOT NULL 
			THEN 'Engaged'
        ELSE 'Not Engaged'
    END AS engagement_status,
    COUNT(DISTINCT c.customer_id) AS customer_count
FROM customers c
LEFT JOIN interactions i
    ON c.customer_id = i.customer_id
GROUP BY engagement_status;

/*
• Engaged users = 1197
• Buyers = 1002

That means ~83.7% of engaged users are buyers.
=> Engagement is highly correlated with purchase.

• 6803 users are neither engaged nor buying. These are basically dead / dormant users.
• 195 users are engaged but not buying. These people may already be interested, just need conversion push.
*/


-- ===========================
-- REPEAT vs ONE-TIME BUYERS
-- ===========================
SELECT 
    CASE 
        WHEN purchase_count = 1 
			THEN 'One-Time Buyer'
        ELSE 'Repeat Buyer'
    END AS buyer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT customer_id, COUNT(*) AS purchase_count
    FROM transactions
    GROUP BY customer_id
) t
GROUP BY buyer_type;

/*
Out of 1002 buyers:
• ~90% are repeat buyers
• ~10% are one-time buyers
*/


-- ===============================
-- CUSTOMER REVENUE DISTRIBUTION
-- ===============================
SELECT 
    customer_id,
    SUM(price * quantity * (1 - discount)) AS total_spent
FROM transactions
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

/*
• Top spender: ~2.8M
• Top 10 range: ~1.8M ↠ 2.8M
*/


-- =================================
-- REVENUE CONCENTRATION (TOP 10%)
-- =================================
WITH customer_revenue AS (
    SELECT 
        customer_id,
        SUM(price * quantity * (1 - discount)) AS total_spent
    FROM transactions
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT *,
           NTILE(10) OVER (ORDER BY total_spent DESC) AS decile
    FROM customer_revenue
)
SELECT 
    decile,
    COUNT(*) AS customers,
    SUM(total_spent) AS revenue
FROM ranked_customers
GROUP BY decile
ORDER BY decile;

/*
Compare top vs bottom
• Top 10% (Decile 1) 
	• Revenue: 154M
• Bottom 10% (Decile 10)
	• Revenue: 768K

=> Top customers generate ~200 times more revenue than the lowest group.

• Top 20% (Decile 1 + 2)
	• 154M + 85M ≈ 239M
• Total revenue ≈ 436M

=> Top 20% customers generate ~55% of total revenue.

This clearly tells us: not all customers are equal, some customers are way more valuable.🙂
*/


-- =================================
-- ENGAGEMENT vs PURCHASE BEHAVIOR
-- =================================
WITH interaction_counts AS (
    SELECT 
        customer_id,
        COUNT(*) AS interaction_count
    FROM interactions
    GROUP BY customer_id
),
purchase_counts AS (
    SELECT 
        customer_id,
        COUNT(*) AS purchase_count
    FROM transactions
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN ic.interaction_count IS NULL 
			THEN 'No Interaction'
        WHEN ic.interaction_count <= 10 
			THEN 'Low Engagement'
        WHEN ic.interaction_count <= 50 
			THEN 'Medium Engagement'
        ELSE 'High Engagement'
    END AS engagement_level,

    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(DISTINCT pc.customer_id) AS buyers

FROM customers c
LEFT JOIN interaction_counts ic 
    ON c.customer_id = ic.customer_id
LEFT JOIN purchase_counts pc 
    ON c.customer_id = pc.customer_id

GROUP BY engagement_level
ORDER BY engagement_level;

/*
1. High Engagement ↠ 100% Conversion
	• Every highly engaged user ended up purchasing
2. Medium Engagement ↠ 60% conversion
	• Engagement ↠ strong purchase likelihood
3. Low Engagement ↠ 25% conversion
	• Lower, but still meaningful
4. No Interaction ↠ Zero Conversion
	• No engagement = No purchase

Engagement is a strong leading indicator of purchase behavior.
Not correlation... almost causation-level signal in your dataset.😀
*/
