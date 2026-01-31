import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import date

ENGINE = create_engine(
    "postgresql+psycopg2://rfm_user:rfm_pass@postgres:5432/rfm_analytics"
)

def run_segmentation():
    df = pd.read_sql("SELECT * FROM fct_customer_rfm", ENGINE)

    features = df[["recency", "frequency", "monetary"]]
    scaled = StandardScaler().fit_transform(features)

    kmeans = KMeans(n_clusters=4, random_state=42)
    df["cluster_id"] = kmeans.fit_predict(scaled)
    df["model_run_date"] = date.today()

    df[["customer_id", "cluster_id", "model_run_date"]].to_sql(
        "customer_segments",
        ENGINE,
        if_exists="append",
        index=False
    )

if __name__ == "__main__":
    run_segmentation()
