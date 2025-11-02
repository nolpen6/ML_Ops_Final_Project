# 🌿 MLOps Project - Dandelion vs Grass Classifier

## 📋 Description du Projet

Projet MLOps complet pour classifier des images : **Pissenlit (Dandelion)** vs **Herbe (Grass)**.

### Architecture

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   Airflow   │────▶│  MinIO   │────▶│  DL      │────▶│ MLflow   │
│  (Orchestre)│     │ (Storage)│     │  Model   │     │ (Track)  │
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
                                                             │
                                                             ▼
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   WebApp    │────▶│   API    │────▶│  MinIO   │     │Monitoring│
│  (Frontend) │     │ (Backend) │     │ (Models) │     │ (Metrics) │
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
                           ▲
                           │
                    ┌──────────────┐
                    │ Kubernetes   │
                    │ (Orchestré)  │
                    └──────────────┘
```

## 🚀 Quick Start

### Prérequis
- Docker & Docker Compose
- Python 3.9+

### Lancer les services

```bash
docker compose up -d
```

Services disponibles :
- **Airflow** : http://localhost:8080 (admin/admin)
- **MinIO** : http://localhost:9001 (minioadmin/minioadmin)
- **MLflow** : http://localhost:5001
- **Prometheus** : http://localhost:9090
- **Grafana** : http://localhost:3000 (admin/admin)

### Lancer l'API

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn scripts.api:app --reload
```

### Lancer la WebApp

```bash
streamlit run scripts/webapp.py
```

## 📁 Structure du Projet

```
emmaloou-ML_Ops/
├── scripts/              # Scripts Python
│   ├── api.py           # API FastAPI
│   ├── webapp.py        # WebApp Streamlit
│   ├── model_train.py   # Entraînement
│   └── ...
├── dags/                # DAGs Airflow
│   ├── data_ingestion_dag.py
│   └── training_dag.py
├── docker/              # Dockerfiles
│   ├── Dockerfile.api
│   ├── Dockerfile.webapp
│   └── Dockerfile.airflow
├── kubernetes/          # Manifests K8s
│   ├── api-deployment.yaml
│   ├── webapp-deployment.yaml
│   └── ...
├── monitoring/          # Config Monitoring
│   ├── prometheus.yml
│   └── grafana/
├── config/              # Configurations
│   ├── airflow_config.yaml
│   └── mlflow_config.yaml
├── docker-compose.yml   # Services Docker
├── requirements.txt     # Dépendances
└── README.md
```

## 🔧 Technologies

- **Orchestration** : Apache Airflow, Kubernetes
- **ML** : PyTorch, MLflow
- **Storage** : MinIO (S3-compatible)
- **API** : FastAPI
- **Frontend** : Streamlit
- **Monitoring** : Prometheus, Grafana
- **CI/CD** : GitHub Actions
- **Containerization** : Docker

## 📊 Modèle

- **Architecture** : ResNet18 avec Transfer Learning
- **Classes** : Dandelion (0), Grass (1)
- **Input** : Images 128x128 RGB
- **Performance** : 83.33% accuracy

## 🔄 Déploiement

### Docker Compose (Développement)
```bash
docker compose up -d
```

### Kubernetes (Production)
```bash
kubectl apply -f kubernetes/
```

## 📝 License

Ce projet est un projet éducatif.
