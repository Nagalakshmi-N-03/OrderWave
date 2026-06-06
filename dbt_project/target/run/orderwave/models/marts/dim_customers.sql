
  
    

  create  table "orderwave_db"."marts_marts"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    SELECT DISTINCT
    customer_id,
    customer_name,
    customer_email,
    city,
    state
FROM "orderwave_db"."marts_staging"."stg_orders"
  );
  