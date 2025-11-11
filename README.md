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

## 🚀 Installation et Démarrage

### Prérequis
- **Docker** & **Docker Compose** (version récente)
- **Python 3.9+**
- **Git**

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/nolpen6/ML_Ops_Final_Project.git
cd ML_Ops_Final_Project
```

### Étape 2 : Configuration de l'environnement

1. **Créer le fichier `.env`** (copier depuis `.env.example` si disponible) :
```bash
# Générer une clé Fernet pour Airflow
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

2. **Créer le fichier `.env`** à la racine du projet :
```bash
AIRFLOW_FERNET_KEY=<la_clé_générée>
```

### Étape 3 : Préparer les données (optionnel)

Si tu as des images d'entraînement, place-les dans :
```
data/
├── dandelion/
│   ├── image1.jpg
│   └── ...
└── grass/
    ├── image1.jpg
    └── ...
```

### Étape 4 : Lancer les services Docker

```bash
docker compose up -d
```

**⏱️ Attendre 2-3 minutes** que tous les services démarrent (surtout Airflow).

Vérifier que tous les services sont en cours d'exécution :
```bash
docker compose ps
```

### Étape 5 : Configurer l'environnement Python

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 6 : Initialiser la base de données PostgreSQL

```bash
# Créer la table predictions
python scripts/init_predictions_db.py

# Créer le bucket MinIO pour les prédictions
python scripts/create_predictions_bucket.py
```

### Étape 7 : Lancer l'API

```bash
# Dans le venv activé
uvicorn scripts.api:app --reload
```

L'API sera accessible sur : http://localhost:8000
Documentation Swagger : http://localhost:8000/docs

### Étape 8 : Utiliser les DAGs Airflow

1. **Accéder à Airflow** : http://localhost:8080
   - Username : `admin`
   - Password : `admin`

2. **Exécuter le DAG d'ingestion de données** :
   - Trouver le DAG `data_ingestion`
   - Cliquer sur le bouton ▶️ (Play) pour déclencher manuellement
   - Attendre que les tâches `scan_images` et `upload_to_minio` passent au vert ✅

3. **Exécuter le DAG d'entraînement** :
   - Trouver le DAG `training`
   - Cliquer sur le bouton ▶️ (Play) pour déclencher manuellement
   - Attendre la fin de l'entraînement (2-5 minutes)
   - Vérifier les runs dans MLflow : http://localhost:5001

## 🌐 Services Disponibles

| Service | URL | Identifiants |
|---------|-----|--------------|
| **Airflow** | http://localhost:8080 | admin / admin |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin |
| **MLflow** | http://localhost:5001 | - |
| **pgAdmin** | http://localhost:5050 | admin@mlops.com / admin |
| **API FastAPI** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin / admin |

## 📖 Utilisation

### Faire une prédiction via l'API

1. Aller sur http://localhost:8000/docs
2. Utiliser l'endpoint `POST /predict/`
3. Uploader une image (dandelion ou grass)
4. La réponse contient :
   - La prédiction (dandelion ou grass)
   - Le niveau de confiance
   - L'ID de la prédiction
   - Le chemin MinIO de l'image sauvegardée

### Voir les prédictions stockées

- **Dans MinIO** : http://localhost:9001 → bucket `mlops-predictions`
- **Dans PostgreSQL** : http://localhost:5050 (pgAdmin) → table `predictions`
- **Via l'API** : http://localhost:8000/predictions/

### Voir les runs d'entraînement

- **MLflow** : http://localhost:5001 → Expérience "dandelion_vs_grass_classifier"

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

## 🔧 Configuration pgAdmin (Interface PostgreSQL)

1. Accéder à http://localhost:5050
2. Se connecter avec : `admin@mlops.com` / `admin`
3. Ajouter un nouveau serveur :
   - **Name** : MLOps PostgreSQL
   - **Host** : `postgres` (nom du service Docker)
   - **Port** : `5432`
   - **Database** : `mlops`
   - **Username** : `airflow`
   - **Password** : `airflow`
4. Explorer la table `predictions` pour voir toutes les prédictions

## 🐛 Troubleshooting

### L'API ne démarre pas
- Vérifier que le venv est activé : `which python` doit pointer vers `venv/bin/python`
- Vérifier que toutes les dépendances sont installées : `pip list | grep psycopg2`
- Vérifier que le modèle existe : `ls models/best_model_epoch_3.pth`

### Les DAGs Airflow ne s'exécutent pas
- Vérifier que PostgreSQL est accessible : `docker ps | grep postgres`
- Vérifier les logs : `docker logs mlops-airflow-scheduler`
- Attendre que Airflow soit complètement initialisé (2-3 minutes)

### MLflow ne montre pas les runs
- Vérifier que MLflow est démarré : `docker ps | grep mlflow`
- Vérifier que le DAG training a bien été exécuté
- Redémarrer MLflow : `docker compose restart mlflow`

### MinIO ne montre pas les images
- Vérifier que MinIO est démarré : `docker ps | grep minio`
- Vérifier que le DAG data_ingestion a été exécuté
- Vérifier les buckets : http://localhost:9001

### PostgreSQL ne contient pas de données
- Vérifier que la table existe : `python scripts/init_predictions_db.py`
- Vérifier que l'API sauvegarde bien : regarder les logs de l'API lors d'une prédiction

## 🔄 Commandes Utiles

```bash
# Voir les logs d'un service
docker logs mlops-airflow-scheduler
docker logs mlops-mlflow
docker logs mlops-postgres

# Redémarrer un service
docker compose restart <service_name>

# Arrêter tous les services
docker compose down

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker compose down -v

# Voir l'état des services
docker compose ps
```

## 📝 Notes Importantes

- **Premier démarrage** : Airflow prend 2-3 minutes pour s'initialiser complètement
- **Modèle** : Le modèle doit être entraîné avant de pouvoir faire des prédictions (via le DAG `training`)
- **Données** : Les images d'entraînement doivent être dans `data/dandelion/` et `data/grass/`
- **Ports** : Assure-toi que les ports 8000, 8080, 5001, 9000, 9001, 5433, 5050 ne sont pas déjà utilisés

## 📝 License

Ce projet est un projet éducatif.
