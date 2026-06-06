SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.quantity,
    o.unit_price,
    o.total_amount,
    o.order_status,
    o.city,
    o.state,
    p.category,
    p.brand,
    p.cost_price,
    (o.unit_price - p.cost_price) * o.quantity AS gross_profit
FROM "orderwave_db"."marts_staging"."stg_orders" o
LEFT JOIN "orderwave_db"."marts_staging"."stg_products" p ON o.product_id = p.product_id