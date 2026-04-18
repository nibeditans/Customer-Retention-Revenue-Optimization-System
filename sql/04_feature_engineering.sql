-- ======================================
-- Create customer-level features table
-- ======================================

-- DROP TABLE IF EXISTS customer_features;

CREATE TABLE customer_features AS

WITH reference_date AS (
    SELECT MAX(transaction_date) AS max_date
    FROM transactions
),

-- ==============
-- RFM Features
-- ==============
rfm AS (
    SELECT
        t.customer_id,

        (r.max_date::date - MAX(t.transaction_date)::date) AS recency_days,

        COUNT(t.transaction_id) AS frequency,

        SUM(t.quantity * t.price * (1 - t.discount)) AS monetary

    FROM transactions t
    CROSS JOIN reference_date r
    GROUP BY t.customer_id, r.max_date
),

-- =====================
-- Engagement Features
-- =====================
engagement AS (
    SELECT
        i.customer_id,

        COUNT(i.interaction_id) AS total_interactions,

        (r.max_date::date - MAX(i.interaction_timestamp)::date) AS last_interaction_days,

        COUNT(DISTINCT i.interaction_type) AS interaction_types_count

    FROM interactions i
    CROSS JOIN reference_date r
    GROUP BY i.customer_id, r.max_date
)

-- =====================
-- Final Feature Table
-- =====================
SELECT
    c.customer_id,

    -- =================
    -- RFM Features
    -- =================
    COALESCE(
        r.recency_days,
        (ref.max_date::date - c.signup_date::date)
    ) AS recency_days,

    COALESCE(r.frequency, 0) AS frequency,

    COALESCE(r.monetary, 0) AS monetary,

    COALESCE(
        r.monetary / NULLIF(r.frequency, 0),
        0
    ) AS avg_order_value,

    -- =====================
    -- Engagement Features
    -- =====================
    COALESCE(e.total_interactions, 0) AS total_interactions,

    COALESCE(
        e.last_interaction_days,
        (ref.max_date::date - c.signup_date::date)
    ) AS last_interaction_days,

    COALESCE(e.interaction_types_count, 0) AS interaction_types_count,

    CASE
        WHEN COALESCE(e.total_interactions, 0) = 0 THEN 'No Interaction'
        WHEN e.total_interactions < 5 THEN 'Low Engagement'
        WHEN e.total_interactions < 15 THEN 'Medium Engagement'
        ELSE 'High Engagement'
    END AS engagement_segment,

    -- =================
    -- Behavioral Features
    -- =================
    CASE 
        WHEN COALESCE(r.frequency, 0) > 0 THEN 1 
        ELSE 0 
    END AS has_purchased,

    CASE 
        WHEN COALESCE(e.total_interactions, 0) > 0 
             AND COALESCE(r.frequency, 0) = 0 
        THEN 1 
        ELSE 0 
    END AS engaged_not_purchased,

    COALESCE(
        r.frequency / NULLIF(
            (ref.max_date::date - c.signup_date::date), 0
        ),
        0
    ) AS purchase_frequency_rate,

    COALESCE(
        e.total_interactions / NULLIF(r.frequency, 0),
        0
    ) AS interaction_purchase_ratio,

    -- ===============
    -- Customer Info
    -- ===============
    c.customer_segment,
    c.location,
    c.acquisition_channel,
    c.age,
    c.gender

FROM customers c
LEFT JOIN rfm r 
    ON c.customer_id = r.customer_id
LEFT JOIN engagement e 
    ON c.customer_id = e.customer_id
CROSS JOIN reference_date ref;


-- Quick validation
SELECT * FROM customer_features;
