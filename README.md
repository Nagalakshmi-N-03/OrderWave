
## OrderWave — E-commerce Data & Demand Forecasting Platform

A production-grade data engineering project that simulates the backend data platform of companies like Flipkart, Meesho, and Nykaa.

Raw e-commerce data flows through an automated pipeline — ingested into PostgreSQL, transformed with dbt, forecasted with Prophet, and visualized on a live Streamlit dashboard backed by Supabase.

🔗 Live Dashboard: https://nagalakshmi-n-03-orderwave-dashboardapp-4y9yyo.streamlit.app
## Tech Stack

Docker | PostgreSQL | Apache Airflow | dbt | Prophet | Streamlit | Supabase | GitHub

| Layer            | Tool                  |
|----------------  |-----------------------|
| Containerization | Docker              |
| Database         | PostgreSQL + Supabase |
| Orchestration    | Apache Airflow 2.8    |
| Transformation   | dbt 1.7               |
| Forecasting    | Prophet (Meta)        |
| Dashboard      | Streamlit + Plotly    |
| Deployment     | Streamlit Cloud       |
| Version Control| GitHub                |

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white) ![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

## 🧱 Architecture

This project is built as a fully automated data pipeline. Raw e-commerce data is ingested into PostgreSQL, cleaned and transformed using dbt, forecasted using Prophet, and served on a live Streamlit dashboard backed by Supabase.

```
Raw Data (CSV / Inline)
        ↓
   PostgreSQL (raw schema)
   └── raw.orders
   └── raw.products
   └── raw.inventory
        ↓
  Apache Airflow (daily 6am)
  └── ingest_orders
  └── ingest_products
  └── ingest_inventory
        ↓
    dbt Transformations
    └── staging/
    │   └── stg_orders
    │   └── stg_products
    │   └── stg_inventory
    └── marts/
        └── fact_orders
        └── dim_customers
        └── dim_products
        └── dim_dates
        ↓
  ┌─────────────────────────┐
  │   Prophet Forecast      │  →  demand_forecast table
  │   Low Stock Alerts      │  →  email notification
  │   Streamlit Dashboard   │  →  live at Streamlit Cloud
  └─────────────────────────┘
        ↓
   Supabase (cloud PostgreSQL)
        ↓
   Streamlit Cloud (public URL)
```
## Project Structure

```
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
```
## 🚀 Run Locally

### Prerequisites
- Docker Desktop
- Python 3.11
- Git

### 1. Clone the repo
```bash
git clone https://github.com/Nagalakshmi-N-03/OrderWave
cd OrderWave
```

### 2. Start containers
```bash
docker compose up -d
```

### 3. Create virtual environment
```bash
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Run ingestion
```bash
python ingestion/ingest_orders.py
python ingestion/ingest_products.py
python ingestion/ingest_inventory.py
```

### 5. Run dbt
```bash
cd dbt_project
dbt run
dbt test
cd ..
```

### 6. Run forecasting and alerts
```bash
python forecasting/forecast_demand.py
python alerting/alert_lowstock.py
```

### 7. Launch dashboard
```bash
streamlit run dashboard/app.py
```

Open `http://localhost:8501`
## 🗄️ Data Model (Star Schema)

The data is modeled as a star schema with one fact table and four dimension tables.

```
                    dim_customers
                    (customer_id)
                          │
                          │
dim_dates ────────── fact_orders ────────── dim_products
(date_day)           (order_id)             (product_id)
                     (customer_id)
                     (product_id)
                     (order_date)
                     (quantity)
                     (total_amount)
                     (gross_profit)
                          │
                          │
                    dim_dates
                    (date_day)
```

| Table | Type | Description |
|---|---|---|
| fact_orders | Fact | One row per order with metrics |
| dim_customers | Dimension | Unique customer details |
| dim_products | Dimension | Product catalogue |
| dim_dates | Dimension | Date attributes |
| stg_orders | Staging View | Cleaned raw orders |
| stg_products | Staging View | Cleaned raw products |
| stg_inventory | Staging View | Cleaned raw inventory |
## 📦 Data Quality Tests (dbt)

8 automated tests run on every pipeline execution using dbt test.

| Test | Model | Column | Status |
|---|---|---|---|
| not_null | stg_orders | order_id | ✅ Pass |
| unique | stg_orders | order_id | ✅ Pass |
| not_null | stg_orders | customer_id | ✅ Pass |
| not_null | stg_orders | product_id | ✅ Pass |
| not_null | stg_orders | total_amount | ✅ Pass |
| not_null | stg_products | product_id | ✅ Pass |
| unique | stg_products | product_id | ✅ Pass |
| not_null | stg_inventory | product_id | ✅ Pass |

```
11:00:33  Found 7 models, 8 tests
11:00:36  Finished running 8 tests

PASS=8   WARN=0   ERROR=0   SKIP=0   TOTAL=8
```
## 📦 Data Quality Tests (dbt)

8 automated tests run on every pipeline execution using dbt test.

| Test | Model | Column | Status |
|---|---|---|---|
| not_null | stg_orders | order_id | ✅ Pass |
| unique | stg_orders | order_id | ✅ Pass |
| not_null | stg_orders | customer_id | ✅ Pass |
| not_null | stg_orders | product_id | ✅ Pass |
| not_null | stg_orders | total_amount | ✅ Pass |
| not_null | stg_products | product_id | ✅ Pass |
| unique | stg_products | product_id | ✅ Pass |
| not_null | stg_inventory | product_id | ✅ Pass |

```
11:00:33  Found 7 models, 8 tests
11:00:36  Finished running 8 tests

PASS=8   WARN=0   ERROR=0   SKIP=0   TOTAL=8
```
## 🏗️ Build Phases

| Phase | What was built | Tools |
|---|---|---|
| Phase 1 | Docker setup, PostgreSQL raw schema, 3 ingestion scripts | Docker, PostgreSQL, Python |
| Phase 2 | Airflow DAG wiring all ingestion tasks | Apache Airflow |
| Phase 3 | dbt staging views + mart tables + 8 quality tests | dbt, PostgreSQL |
| Phase 4 | Prophet demand forecast + low stock email alert | Prophet, smtplib |
| Phase 5 | Streamlit dashboard deployed on Streamlit Cloud | Streamlit, Plotly, Supabase |
## 📸 Dashboard Preview



> Live at: [https://nagalakshmi-n-03-orderwave-dashboardapp-4y9yyo.streamlit.app](https://nagalakshmi-n-03-orderwave-dashboardapp-4y9yyo.streamlit.app)
## 🛠️ Troubleshooting

| Problem | Error | Fix |
|---|---|---|
| Docker not starting | `Docker Desktop is unable to start` | Open Docker Desktop, wait for whale icon in taskbar |
| Port 5432 conflict | `role "orderwave" does not exist` | Stop local PostgreSQL service from Windows Services |
| Wrong Postgres image | `exec format error` | Use `postgres:15-bullseye` instead of `postgres:15` |
| dbt Python error | `KeyError: javascript` | Use Python 3.11 venv, not Python 3.13 |
| dbt version error | `postgres adapter not supported` | Use `dbt-core==1.7.0` not `dbt-core==2.0.0` |
| Streamlit can't connect | `connection failed` | Use Supabase pooler URL, not direct connection |
| psycopg2 error | `module not found` | `pip install psycopg2-binary` |
| Git push rejected | `fetch first` | Run `git pull origin main --rebase` then push |
## 👤 Author

**Nagalakshmi N**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nagalakshmi-N-03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nagalakshmi-n-5a7672268)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nagalakshmi.n.23003@gmail.com)


