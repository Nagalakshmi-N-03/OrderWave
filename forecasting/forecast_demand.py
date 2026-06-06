import pandas as pd
import psycopg2
import os
import logging
from prophet import Prophet

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DB_CONFIG = {
    "host":     os.getenv("PG_HOST",     "127.0.0.1"),
    "port":     int(os.getenv("PG_PORT", "5432")),
    "dbname":   os.getenv("PG_DB",       "orderwave_db"),
    "user":     os.getenv("PG_USER",     "orderwave"),
    "password": os.getenv("PG_PASSWORD", "orderwave123"),
}

def fetch_orders():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT order_date AS ds, SUM(quantity) AS y
        FROM marts_marts.fact_orders
        WHERE order_status NOT IN ('cancelled', 'returned')
        GROUP BY order_date
        ORDER BY order_date
    """, conn)
    conn.close()
    return df

def run_forecast():
    log.info("Fetching order data...")
    df = fetch_orders()
    log.info("Got %d data points", len(df))

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    model.fit(df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
    log.info("\n%s", output.to_string(index=False))

    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS marts_marts.demand_forecast (
                    forecast_date DATE,
                    predicted_qty NUMERIC(10,2),
                    lower_bound   NUMERIC(10,2),
                    upper_bound   NUMERIC(10,2),
                    created_at    TIMESTAMP DEFAULT NOW()
                )
            """)
            cur.execute("DELETE FROM marts_marts.demand_forecast")
            for _, row in output.iterrows():
                cur.execute("""
                    INSERT INTO marts_marts.demand_forecast
                        (forecast_date, predicted_qty, lower_bound, upper_bound)
                    VALUES (%s, %s, %s, %s)
                """, (row['ds'].date(), round(row['yhat'], 2),
                      round(row['yhat_lower'], 2), round(row['yhat_upper'], 2)))
    conn.close()
    log.info("Forecast saved to demand_forecast table ✓")

if __name__ == "__main__":
    run_forecast()