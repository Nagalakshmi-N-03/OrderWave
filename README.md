OrderWave — E-commerce Data & Demand Forecasting Platform
A production-grade data engineering project that simulates the backend data platform of companies like Flipkart, Meesho, and Nykaa.

Raw e-commerce data goes in one end → clean insights, forecasts, and stock alerts come out the other.

🔗 Live Dashboard: Click here

🧱 Architecture
Raw Data (CSV / Inline)
        ↓
   PostgreSQL (raw schema)
        ↓
  Apache Airflow (daily 6am)
        ↓
    dbt (staging → marts)
        ↓
  ┌─────────────────────┐
  │  Prophet Forecast   │
  │  Low Stock Alerts   │
  │  Streamlit Dashboard│
  └─────────────────────┘
        ↓
   Supabase (cloud DB)
        ↓
  Streamlit Cloud (live)
⚙️ Tech Stack
Layer	Tool
Containerization	Docker
Database	PostgreSQL + Supabase
Orchestration	Apache Airflow 2.8
Transformation	dbt 1.7
Forecasting	Prophet (Meta)
Dashboard	Streamlit + Plotly
Deployment	Streamlit Cloud
Version Control	GitHub
📁 Project Structure
orderwave/
│
├── docker-compose.yml        # Postgres + Airflow containers
├── init.sql                  # Raw schema + table creation
├── requirements.txt          # Python dependencies
│
├── data/
│   └── sample_orders.csv     # 30 sample Indian e-commerce orders
│
├── ingestion/
│   ├── ingest_orders.py      # CSV → raw.orders
│   ├── ingest_products.py    # Catalogue → raw.products
│   └── ingest_inventory.py   # Warehouses → raw.inventory
│
├── dags/
│   └── ecommerce_pipeline.py # Airflow DAG (daily 6am)
│
├── dbt_project/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_orders.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_inventory.sql
│   │   │   └── schema.yml        # 8 data quality tests
│   │   └── marts/
│   │       ├── fact_orders.sql
│   │       ├── dim_customers.sql
│   │       ├── dim_products.sql
│   │       └── dim_dates.sql
│
├── forecasting/
│   └── forecast_demand.py    # Prophet 30-day forecast
│
├── alerting/
│   └── alert_lowstock.py     # Email alert for low stock
│
└── dashboard/
    └── app.py                # Streamlit dashboard
🚀 Run Locally
Prerequisites
Docker Desktop
Python 3.11
Git
1. Clone the repo
git clone https://github.com/Nagalakshmi-N-03/OrderWave
cd OrderWave
2. Start containers
docker compose up -d
3. Create virtual environment
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
4. Run ingestion
python ingestion/ingest_orders.py
python ingestion/ingest_products.py
python ingestion/ingest_inventory.py
5. Run dbt
cd dbt_project
dbt run
dbt test
cd ..
6. Run forecasting and alerts
python forecasting/forecast_demand.py
python alerting/alert_lowstock.py
7. Launch dashboard
streamlit run dashboard/app.py
Open http://localhost:8501

📊 What the Dashboard Shows
KPIs — Total orders, revenue, gross profit, average order value
Daily Revenue Trend — Line chart over time
Revenue by Category — Bar chart (Footwear, Electronics, Kitchen and more)
Order Status Breakdown — Pie chart (delivered, shipped, cancelled, returned)
Low Stock Alerts — Products below reorder level across warehouses
30-Day Demand Forecast — Prophet prediction with confidence bands
🗄️ Data Model (Star Schema)
                 dim_customers
                      │
dim_dates ──── fact_orders ──── dim_products
                      │
                 dim_dates
Staging layer — views that clean raw data
Marts layer — tables optimized for analytics

📦 Data Quality Tests (dbt)
Test	Model	Status
not_null	stg_orders.order_id	✅
unique	stg_orders.order_id	✅
not_null	stg_orders.customer_id	✅
not_null	stg_orders.product_id	✅
not_null	stg_orders.total_amount	✅
not_null	stg_products.product_id	✅
unique	stg_products.product_id	✅
not_null	stg_inventory.product_id	✅
🏗️ Build Phases
Phase	What was built
Phase 1	Docker setup, PostgreSQL raw schema, 3 ingestion scripts
Phase 2	Airflow DAG wiring all ingestion tasks
Phase 3	dbt staging views + mart tables + 8 quality tests
Phase 4	Prophet demand forecast + low stock email alert
Phase 5	Streamlit dashboard deployed on Streamlit Cloud
🧩 Data Flow
sample_orders.csv
       +
product catalogue      →   raw.orders
       +                   raw.products      →   stg_orders
warehouse inventory    →   raw.inventory         stg_products      →   fact_orders
                                                  stg_inventory         dim_customers
                                                                        dim_products
                                                                        dim_dates
                                                                              ↓
                                                                    demand_forecast
                                                                              ↓
                                                                    Streamlit Dashboard
⚠️ Low Stock Alert Sample Output
Product                        Warehouse                  Stock  Reorder
-------------------------------------------------------------------------
Face Wash Gel 100ml            Mumbai Warehouse               5       30
Yoga Mat Non-Slip              Delhi Warehouse                7       20
Cotton Bedsheet Set            Chennai Warehouse              8       25

🔮 Forecast Sample Output
Prophet predicts daily order quantity for next 30 days with upper and lower confidence bounds, saved to demand_forecast table in Supabase.

🛠️ Troubleshooting
Problem	Fix
Docker not starting	Open Docker Desktop, wait for whale icon
Port 5432 conflict	Stop local PostgreSQL service
dbt Python error	Use Python 3.11 venv, not 3.13
Streamlit can't connect	Use Supabase pooler URL, not direct
psycopg2 error	pip install psycopg2-binary

👤 Author
Nagalakshmi
Data Engineering Project — OrderWave
