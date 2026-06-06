SELECT
    order_id,
    customer_id,
    customer_name,
    customer_email,
    product_id,
    quantity,
    unit_price,
    total_amount,
    order_status,
    order_date::date AS order_date,
    city,
    state,
    ingested_at
FROM raw.orders
WHERE order_id IS NOT NULL