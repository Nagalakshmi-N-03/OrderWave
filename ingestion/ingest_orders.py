import csv
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

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/sample_orders.csv")

INSERT_SQL = """
    INSERT INTO raw.orders (
        order_id, customer_id, customer_name, customer_email,
        product_id, quantity, unit_price, total_amount,
        order_status, order_date, city, state
    ) VALUES (
        %(order_id)s, %(customer_id)s, %(customer_name)s, %(customer_email)s,
        %(product_id)s, %(quantity)s, %(unit_price)s, %(total_amount)s,
        %(order_status)s, %(order_date)s, %(city)s, %(state)s
    )
    ON CONFLICT DO NOTHING;
"""

def ingest_orders():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "order_id":       row["order_id"].strip(),
                "customer_id":    row["customer_id"].strip(),
                "customer_name":  row["customer_name"].strip(),
                "customer_email": row["customer_email"].strip(),
                "product_id":     row["product_id"].strip(),
                "quantity":       int(row["quantity"]),
                "unit_price":     float(row["unit_price"]),
                "total_amount":   float(row["total_amount"]),
                "order_status":   row["order_status"].strip(),
                "order_date":     row["order_date"].strip(),
                "city":           row["city"].strip(),
                "state":          row["state"].strip(),
            })
    log.info("Read %d rows from CSV", len(rows))

    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, rows)
    conn.close()
    log.info("Orders ingestion complete ✓")

if __name__ == "__main__":
    ingest_orders()
