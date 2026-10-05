# StreamGuard — Real-Time Fraud Detection Pipeline
**Designed and Developed by NIKHIL CHARY SRIRAMOJU**

Kafka · Airflow · dbt · Delta Lake · PyTorch CNN · LangGraph agent · RAG (Qdrant) · Docker · Prometheus · Grafana

Live demo: https://nikhil-creat.github.io/streamguard/

## Resume line
Built a real-time fraud detection pipeline using Kafka for streaming, Airflow for orchestration, dbt for transformations, and Delta Lake for reliable analytics storage, with a CNN scorer and an agentic RAG investigator for flagged cases.

## Quick start
```
cp .env.example .env
docker compose up --build
python rag/seed.py     # load playbooks into Qdrant
```
API docs :8000/docs · Airflow :8080 · Grafana :3000 · MinIO :9001

## Status
Working skeleton: producer, stream processor, Delta writes, Airflow DAG, dbt model, agent graph, monitoring config, demo site. To finish: train the CNN (`ml/train_cnn.py`), seed playbooks, connect an LLM in `api/main.py`, add dbt silver models. The dashboard in `docs/` is a simulation.

## Author
Nikhil Chary Sriramoju · [GitHub](https://github.com/Nikhil-creat) · [LinkedIn](https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a) · [Instagram](https://www.instagram.com/nikhil__sriramoju) · [Facebook](https://www.facebook.com/profile.php?id=100079201124141) · sriramojunikhil66@gmail.com · +91 63005 56301

## v3 additions
Fraud ring graph view, per-transaction explanation bars, adjustable block threshold, human approval queue, audit trail endpoint (`/audit`), Prometheus metrics (`/metrics`), PSI drift check in Airflow, and a GitHub Actions CI workflow.
