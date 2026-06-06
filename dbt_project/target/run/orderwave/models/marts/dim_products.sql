
  
    

  create  table "postgres"."marts_marts"."dim_products__dbt_tmp"
  
  
    as
  
  (
    SELECT
    product_id,
    product_name,
    category,
    sub_category,
    brand,
    unit_price,
    cost_price
FROM "postgres"."marts_staging"."stg_products"
  );
  