
  
    

  create  table "orderwave_db"."marts_marts"."dim_products__dbt_tmp"
  
  
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
FROM "orderwave_db"."marts_staging"."stg_products"
  );
  