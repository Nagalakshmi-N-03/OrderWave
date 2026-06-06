import os
import logging
from datetime import date
import psycopg2

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DB_CONFIG = {
    "host":     os.getenv("PG_HOST",     "127.0.0.1"),
    "port":     int(os.getenv("PG_PORT", "5432")),
    "dbname":   os.getenv("PG_DB",       "orderwave_db"),
    "user":     os.getenv("PG_USER",     "orderwave"),
    "password": os.getenv("PG_PASSWORD", "orderwave123"),
}

TODAY = date.today().isoformat()

INVENTORY = [
    ("PROD-501", "WH-CHN", "Chennai Warehouse",     45, 20, TODAY),
    ("PROD-502", "WH-CHN", "Chennai Warehouse",     30, 15, TODAY),
    ("PROD-503", "WH-CHN", "Chennai Warehouse",    120, 50, TODAY),
    ("PROD-504", "WH-CHN", "Chennai Warehouse",     18, 10, TODAY),
    ("PROD-505", "WH-CHN", "Chennai Warehouse",      8, 25, TODAY),  # below reorder
    ("PROD-501", "WH-MUM", "Mumbai Warehouse",      60, 20, TODAY),
    ("PROD-502", "WH-MUM", "Mumbai Warehouse",      22, 15, TODAY),
    ("PROD-506", "WH-MUM", "Mumbai Warehouse",     200, 80, TODAY),
    ("PROD-507", "WH-MUM", "Mumbai Warehouse",      12, 10, TODAY),
    ("PROD-508", "WH-MUM", "Mumbai Warehouse",       5, 30, TODAY),  # below reorder
    ("PROD-503", "WH-DEL", "Delhi Warehouse",       80, 50, TODAY),
    ("PROD-504", "WH-DEL", "Delhi Warehouse",       25, 10, TODAY),
    ("PROD-509", "WH-DEL", "Delhi Warehouse",      150, 60, TODAY),
    ("PROD-510", "WH-DEL", "Delhi Warehouse",        7, 20, TODAY),  # below reorder
    ("PROD-505", "WH-DEL", "Delhi Warehouse",       40, 25, TODAY),
    ("PROD-506", "WH-HYD", "Hyderabad Warehouse",  180, 80, TODAY),
    ("PROD-507", "WH-HYD", "Hyderabad Warehouse",   14, 10, TODAY),
    ("PROD-508", "WH-HYD", "Hyderabad Warehouse",   55, 30, TODAY),
    ("PROD-509", "WH-HYD", "Hyderabad Warehouse",   90, 60, TODAY),
    ("PROD-510", "WH-HYD", "Hyderabad Warehouse",   35, 20, TODAY),
]

INSERT_SQL = """
    INSERT INTO raw.inventory
        (product_id, warehouse_id, warehouse_name, stock_quantity, reorder_level, last_updated)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""

def ingest_inventory():
    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, INVENTORY)
    conn.close()
    log.info("Inventory ingestion complete ✓")

if __name__ == "__main__":
    ingest_inventory()
