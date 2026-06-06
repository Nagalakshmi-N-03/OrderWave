SELECT DISTINCT
    order_date AS date_day,
    EXTRACT(YEAR FROM order_date)::int AS year,
    EXTRACT(MONTH FROM order_date)::int AS month,
    EXTRACT(DAY FROM order_date)::int AS day,
    TO_CHAR(order_date, 'Month') AS month_name,
    EXTRACT(DOW FROM order_date)::int AS day_of_week,
    TO_CHAR(order_date, 'Day') AS day_name
FROM "postgres"."marts_staging"."stg_orders"