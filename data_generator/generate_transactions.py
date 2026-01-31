import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

def generate_transactions(
    num_customers=500,
    transactions_per_customer=20
):
    records = []
    today = datetime.today()

    for cust in range(1, num_customers + 1):
        customer_id = f"CUST_{cust}"

        for _ in range(random.randint(1, transactions_per_customer)):
            records.append({
                "transaction_id": str(uuid.uuid4()),
                "customer_id": customer_id,
                "transaction_date": (
                    today - timedelta(days=random.randint(1, 365))
                ).strftime("%Y-%m-%d"),
                "amount": round(random.uniform(100, 5000), 2)
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = generate_transactions()
    df.to_csv("/opt/airflow/ingestion/transactions.csv", index=False)

