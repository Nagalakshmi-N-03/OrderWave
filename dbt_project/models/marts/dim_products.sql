SELECT
    product_id,
    product_name,
    category,
    sub_category,
    brand,
    unit_price,
    cost_price
FROM {{ ref('stg_products') }}