SELECT
    product_id,
    warehouse_id,
    warehouse_name,
    stock_quantity,
    reorder_level,
    last_updated::date AS last_updated,
    CASE WHEN stock_quantity < reorder_level THEN true ELSE false END AS is_low_stock,
    ingested_at
FROM raw.inventory
WHERE product_id IS NOT NULL