import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# -----------------------------
# DB connection
# -----------------------------
ENGINE = create_engine(
    "postgresql+psycopg2://rfm_user:rfm_pass@postgres:5432/rfm_analytics"
)

st.set_page_config(
    page_title="RFM Pipeline Validation",
    layout="wide"
)

st.title("📊 RFM Data Pipeline – Validation Dashboard")

# -----------------------------
# Helper: check table existence
# -----------------------------
def table_exists(table_name: str) -> bool:
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = :table
    );
    """
    with ENGINE.connect() as conn:
        return conn.execute(
            text(query), {"table": table_name}
        ).scalar()

# -----------------------------
# Row Counts
# -----------------------------
st.header("📌 Table Row Counts")

tables = [
    "raw_transactions",
    "fct_customer_rfm",
    "customer_segments"
]

cols = st.columns(3)

for i, table in enumerate(tables):
    if table_exists(table):
        count = pd.read_sql(
            f"SELECT COUNT(*) AS count FROM {table}",
            ENGINE
        )["count"][0]
        cols[i].metric(label=table, value=count)
    else:
        cols[i].metric(label=table, value="—")
        cols[i].warning(f"{table} not loaded yet")

st.divider()

# -----------------------------
# Table Preview
# -----------------------------
st.header("🔍 Preview Tables")

available_tables = [t for t in tables if table_exists(t)]

if not available_tables:
    st.info("No tables available yet. Run the Airflow pipeline first.")
else:
    table_choice = st.selectbox(
        "Select table",
        available_tables
    )

    df = pd.read_sql(
        f"SELECT * FROM {table_choice} LIMIT 100",
        ENGINE
    )
    st.dataframe(df, use_container_width=True)

st.divider()

# -----------------------------
# Cluster Distribution
# -----------------------------
st.header("📈 Customer Segment Distribution")

if table_exists("customer_segments"):
    cluster_df = pd.read_sql("""
        SELECT cluster_id, COUNT(*) AS customers
        FROM customer_segments
        GROUP BY cluster_id
        ORDER BY cluster_id
    """, ENGINE)

    st.bar_chart(cluster_df.set_index("cluster_id"))
else:
    st.info("Customer segments not generated yet.")
