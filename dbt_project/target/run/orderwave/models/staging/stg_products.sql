
  create view "postgres"."marts_staging"."stg_products__dbt_tmp"
    
    
  as (
    SELECT
    product_id,
    product_name,
    category,
    sub_category,
    brand,
    unit_price,
    cost_price,
    ingested_at
FROM raw.products
WHERE product_id IS NOT NULL
  );