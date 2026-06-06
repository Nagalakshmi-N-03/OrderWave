import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="OrderWave Dashboard", page_icon="🌊", layout="wide")

DB_CONFIG = {
    "host": "db.nwxvxmpiyfgbgkfayetk.supabase.co",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "OrderWave.2.30"
}

@st.cache_data
def query(sql):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

st.title("🌊 OrderWave — E-commerce Dashboard")

# KPIs
col1, col2, col3, col4 = st.columns(4)
kpi = query("SELECT COUNT(*) AS orders, SUM(total_amount) AS revenue, SUM(gross_profit) AS profit, AVG(total_amount) AS avg_order FROM marts_marts.fact_orders WHERE order_status NOT IN ('cancelled','returned')")
col1.metric("Total Orders", int(kpi['orders'][0]))
col2.metric("Total Revenue", f"₹{kpi['revenue'][0]:,.0f}")
col3.metric("Gross Profit", f"₹{kpi['profit'][0]:,.0f}")
col4.metric("Avg Order Value", f"₹{kpi['avg_order'][0]:,.0f}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Daily Revenue")
    df = query("SELECT order_date, SUM(total_amount) AS revenue FROM marts_marts.fact_orders WHERE order_status NOT IN ('cancelled','returned') GROUP BY order_date ORDER BY order_date")
    fig = px.line(df, x="order_date", y="revenue", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Revenue by Category")
    df = query("SELECT category, SUM(total_amount) AS revenue FROM marts_marts.fact_orders WHERE order_status NOT IN ('cancelled','returned') GROUP BY category ORDER BY revenue DESC")
    fig = px.bar(df, x="category", y="revenue", color="category")
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Order Status Breakdown")
    df = query("SELECT order_status, COUNT(*) AS count FROM marts_marts.fact_orders GROUP BY order_status")
    fig = px.pie(df, names="order_status", values="count")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⚠️ Low Stock Items")
    df = query("SELECT p.product_name, i.warehouse_name, i.stock_quantity, i.reorder_level FROM marts_staging.stg_inventory i JOIN marts_staging.stg_products p ON i.product_id = p.product_id WHERE i.is_low_stock = true ORDER BY i.stock_quantity")
    st.dataframe(df, use_container_width=True)

st.subheader("🔮 30-Day Demand Forecast")
df = query("SELECT forecast_date, predicted_qty, lower_bound, upper_bound FROM marts_marts.demand_forecast ORDER BY forecast_date")
fig = px.line(df, x="forecast_date", y=["predicted_qty", "lower_bound", "upper_bound"], markers=True)
st.plotly_chart(fig, use_container_width=True)