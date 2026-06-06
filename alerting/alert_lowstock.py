import psycopg2
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DB_CONFIG = {
    "host":     os.getenv("PG_HOST",     "127.0.0.1"),
    "port":     int(os.getenv("PG_PORT", "5432")),
    "dbname":   os.getenv("PG_DB",       "orderwave_db"),
    "user":     os.getenv("PG_USER",     "orderwave"),
    "password": os.getenv("PG_PASSWORD", "orderwave123"),
}

SMTP_HOST     = os.getenv("SMTP_HOST",     "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER",     "your_email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")
ALERT_TO      = os.getenv("ALERT_TO",      "your_email@gmail.com")

def fetch_low_stock():
    conn = psycopg2.connect(**DB_CONFIG)
    df_rows = []
    with conn.cursor() as cur:
        cur.execute("""
            SELECT i.product_id, i.warehouse_name,
                   i.stock_quantity, i.reorder_level,
                   p.product_name
            FROM marts_staging.stg_inventory i
            JOIN marts_staging.stg_products p ON i.product_id = p.product_id
            WHERE i.is_low_stock = true
            ORDER BY i.stock_quantity ASC
        """)
        df_rows = cur.fetchall()
    conn.close()
    return df_rows

def send_alert(rows):
    if not rows:
        log.info("No low stock items found. No alert sent.")
        return

    body = "Low Stock Alert — OrderWave\n\n"
    body += f"{'Product':<30} {'Warehouse':<25} {'Stock':>6} {'Reorder':>8}\n"
    body += "-" * 75 + "\n"
    for row in rows:
        product_id, warehouse, stock, reorder, product_name = row
        body += f"{product_name:<30} {warehouse:<25} {stock:>6} {reorder:>8}\n"

    log.info("Low stock items:\n%s", body)

    try:
        msg = MIMEMultipart()
        msg['From']    = SMTP_USER
        msg['To']      = ALERT_TO
        msg['Subject'] = f"⚠️ OrderWave Low Stock Alert — {len(rows)} items need reorder"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, ALERT_TO, msg.as_string())

        log.info("Alert email sent ✓")
    except Exception as e:
        log.warning("Email not sent (check SMTP config): %s", e)
        log.info("Alert logged above — email skipped.")

if __name__ == "__main__":
    rows = fetch_low_stock()
    send_alert(rows)