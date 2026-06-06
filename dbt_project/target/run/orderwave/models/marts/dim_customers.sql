
  
    

  create  table "postgres"."marts_marts"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    SELECT DISTINCT
    customer_id,
    customer_name,
    customer_email,
    city,
    state
FROM "postgres"."marts_staging"."stg_orders"
  );
  