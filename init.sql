CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id        VARCHAR(50),
    customer_id     VARCHAR(50),
    customer_name   VARCHAR(100),
    customer_email  VARCHAR(100),
    product_id      VARCHAR(50),
    quantity        INTEGER,
    unit_price      NUMERIC(10, 2),
    total_amount    NUMERIC(10, 2),
    order_status    VARCHAR(30),
    order_date      DATE,
    city            VARCHAR(50),
    state           VARCHAR(50),
    ingested_at     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id      VARCHAR(50),
    product_name    VARCHAR(150),
    category        VARCHAR(80),
    sub_category    VARCHAR(80),
    brand           VARCHAR(80),
    unit_price      NUMERIC(10, 2),
    cost_price      NUMERIC(10, 2),
    ingested_at     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.inventory (
    product_id      VARCHAR(50),
    warehouse_id    VARCHAR(50),
    warehouse_name  VARCHAR(100),
    stock_quantity  INTEGER,
    reorder_level   INTEGER,
    last_updated    DATE,
    ingested_at     TIMESTAMP DEFAULT NOW()
);