# RFM Analysis & Customer Segmentation Platform

An end-to-end **Data Engineering pipeline** that generates customer transaction data, computes RFM metrics, and performs customer segmentation using K-Means clustering — orchestrated with Apache Airflow and PostgreSQL.

---

## 🚀 Tech Stack
- Python (Pandas, NumPy, scikit-learn)
- Apache Airflow
- PostgreSQL
- Docker & Docker Compose

---

## 🏗️ Architecture Overview

1. **Data Generation**
   - Synthetic customer transaction data is generated daily.

2. **Batch Ingestion**
   - Transactions are ingested into PostgreSQL using Airflow.

3. **Transformation**
   - RFM (Recency, Frequency, Monetary) metrics are computed at the customer level.

4. **Machine Learning**
   - K-Means clustering is applied to segment customers.

5. **Storage**
   - Results are persisted for analytics and downstream use.

---

## 📊 Output Tables
- `raw_transactions` – transaction-level data
- `fct_customer_rfm` – customer-level RFM metrics
- `customer_segments` – clustered customer segments

---

## ▶️ How to Run Locally

```bash
docker-compose up
