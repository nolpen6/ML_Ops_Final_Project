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

## 🗂️ Structure du Projet

```
emmaloou-ML_Ops/
├── scripts/              # Scripts Python
│   ├── data_preparation.py    # Préparation des données
│   ├── model_train.py          # Entraînement du modèle
│   ├── api.py                  # API FastAPI
│   └── upload_to_minio.py     # Upload vers MinIO
├── dags/                 # DAGs Airflow (à venir)
├── config/               # Configurations (à venir)
├── docker/               # Dockerfiles (à venir)
├── kubernetes/           # Manifests K8s (à venir)
├── monitoring/           # Config monitoring (à venir)
├── docs/                 # Documentation
│   └── ROADMAP.md       # Roadmap détaillée
├── data/                 # Données (gitignored)
│   ├── grass/
│   └── dandelion/
├── models/               # Modèles (gitignored)
├── requirements.txt       # Dépendances Python
├── .gitignore            # Fichiers à ignorer
└── README.md             # Ce fichier
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- Docker & Docker Compose (pour services locaux)
- MinIO ou AWS S3

### Setup

1. **Cloner le repository**
```bash
git clone https://github.com/emmaloou/ML_Ops.git
cd ML_Ops
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Setup MinIO** (local ou Docker)
```bash
# Docker Compose pour MinIO + services
docker-compose up -d
```

5. **Télécharger les données**
```bash
# Créer les dossiers data/grass et data/dandelion
# Y placer les images d'entraînement
```

## 💻 Utilisation

### 1. Préparer les données
```bash
python scripts/data_preparation.py
```

### 2. Entraîner le modèle
```bash
python scripts/model_train.py
```

### 3. Uploader le modèle vers MinIO
```bash
python scripts/upload_to_minio.py
```

### 4. Lancer l'API
```bash
uvicorn scripts.api:app --reload
# API disponible sur http://localhost:8000
```

## 📊 Modèle

- **Architecture** : ResNet18 avec Transfer Learning
- **Classes** : Dandelion (0), Grass (1)
- **Input** : Images 128x128 RGB
- **Framework** : PyTorch
- **Tracking** : MLflow

## 🔄 Workflow MLOps

1. **Data Ingestion** → Airflow DAG scanne et upload vers MinIO
2. **Training** → Entraînement avec MLflow tracking
3. **Versioning** → Modèle versionné dans MLflow Registry
4. **Serving** → API déployée avec Kubernetes
5. **Monitoring** → Métriques et logs centralisés

## 📚 Documentation

- [Roadmap détaillée](docs/ROADMAP.md)
- Architecture complète à venir
- Guide de déploiement à venir

## 🛠️ Technologies

- **Orchestration** : Apache Airflow, Kubernetes
- **ML** : PyTorch, MLflow
- **Storage** : MinIO (S3-compatible)
- **API** : FastAPI
- **Containerization** : Docker
- **Monitoring** : Prometheus, Grafana

## 📝 Statut du Projet

- [x] Scripts de base (data prep, training, API)
- [ ] DAGs Airflow
- [ ] Dockerfile
- [ ] Kubernetes manifests
- [ ] WebApp
- [ ] Monitoring
- [ ] CI/CD

## 👤 Auteur

Projet réalisé dans le cadre du Master 2 - MLOps

## 📄 Licence

Ce projet est un projet éducatif.

---

**Note** : Ce projet est en cours de développement. Les fonctionnalités sont ajoutées progressivement selon la roadmap.
