import pandas as pd
from sqlalchemy import create_engine

ENGINE = create_engine(
    "postgresql+psycopg2://rfm_user:rfm_pass@postgres:5432/rfm_analytics"
)

def ingest_transactions(csv_path):
    df = pd.read_csv(csv_path)

    df.columns = df.columns.str.lower()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date

    df.to_sql(
        "raw_transactions",
        ENGINE,
        if_exists="append",
        index=False
    )

if __name__ == "__main__":
    ingest_transactions("/opt/airflow/ingestion/transactions.csv")
