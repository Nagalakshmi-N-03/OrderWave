import os
import logging
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

PRODUCTS = [
    ("PROD-501", "Men's Running Shoes",        "Footwear",    "Sports Shoes", "Nike",      899.00,  450.00),
    ("PROD-502", "Women's Kurti Set",           "Clothing",    "Ethnic Wear",  "Biba",     1299.00,  600.00),
    ("PROD-503", "Stainless Steel Water Bottle","Kitchen",     "Bottles",      "Milton",    499.00,  180.00),
    ("PROD-504", "Wireless Bluetooth Speaker",  "Electronics", "Audio",        "boAt",     2499.00, 1100.00),
    ("PROD-505", "Cotton Bedsheet Set",         "Home",        "Bedding",      "Spaces",    349.00,  140.00),
    ("PROD-506", "Notebook 5-Pack",             "Stationery",  "Notebooks",    "Classmate", 199.00,   70.00),
    ("PROD-507", "Air Fryer 4L",                "Kitchen",     "Appliances",   "Philips",  3999.00, 2200.00),
    ("PROD-508", "Face Wash Gel 100ml",         "Beauty",      "Skin Care",    "Mamaearth", 599.00,  220.00),
    ("PROD-509", "Kids Colouring Set",          "Toys",        "Art & Craft",  "Camlin",    249.00,   90.00),
    ("PROD-510", "Yoga Mat Non-Slip",           "Sports",      "Fitness",      "Boldfit",   799.00,  300.00),
]

INSERT_SQL = """
    INSERT INTO raw.products
        (product_id, product_name, category, sub_category, brand, unit_price, cost_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""

def ingest_products():
    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, PRODUCTS)
    conn.close()
    log.info("Products ingestion complete ✓")

if __name__ == "__main__":
    ingest_products()
