/*
# ALTER DATABASE crros_database SET search_path TO crros_schema;

This is applied automatically to every new connection to this database.
*/

-- Ensure correct schema (session-level safety)
SET search_path TO crros_schema;


-- ==================
-- 1. CREATE TABLES
-- ==================

-- Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    signup_date DATE NOT NULL,
    customer_segment VARCHAR(20) NOT NULL,
    location VARCHAR(50),
    acquisition_channel VARCHAR(50),
    age INT NOT NULL,
    gender VARCHAR(10)
);

-- Products Table
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    cost NUMERIC(10,2) NOT NULL,
    launch_date DATE NOT NULL
);

-- Interactions Table
CREATE TABLE interactions (
    interaction_id INT PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    product_id VARCHAR(10),
    interaction_timestamp TIMESTAMP NOT NULL,
    channel VARCHAR(50),

    CONSTRAINT fk_interactions_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_interactions_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- Transactions Table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    transaction_date DATE NOT NULL,
    quantity INT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    discount NUMERIC(10,2),

    CONSTRAINT fk_transactions_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_transactions_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- DROP TABLE customers, products, interactions, transactions CASCADE;

SELECT * FROM customers LIMIT 10;
SELECT * FROM products LIMIT 10;
SELECT * FROM interactions LIMIT 10;
SELECT * FROM transactions LIMIT 10;


-- =======================
-- 2. LOAD DATA FROM CSV
-- =======================

\copy customers FROM 'data/raw/customers.csv' DELIMITER ',' CSV HEADER;
\copy products FROM 'data/raw/products.csv' DELIMITER ',' CSV HEADER;
\copy interactions FROM 'data/raw/interactions.csv' DELIMITER ',' CSV HEADER;
\copy transactions FROM 'data/raw/transactions.csv' DELIMITER ',' CSV HEADER;

/*
This section loads CSV files into PostgreSQL tables using the \copy command.

Important:
- Run psql from the project root directory.
- Ensure tables are created before running these commands.
- CSV headers must match the table structure.
- Use TRUNCATE before reload to avoid duplicate data.

This step represents the data ingestion phase of the pipeline.
*/
