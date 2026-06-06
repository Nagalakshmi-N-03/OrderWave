SELECT DISTINCT
    customer_id,
    customer_name,
    customer_email,
    city,
    state
FROM {{ ref('stg_orders') }}