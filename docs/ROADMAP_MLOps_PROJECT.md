# 🎯 Roadmap Complète du Projet MLOps

## 📋 Contexte et Objectifs

### Projet
Classification binaire d'images : **Dandelion** (pissenlit) vs **Grass** (herbe)

### Architecture Cible
Basée sur le diagramme fourni, composée de :
- **Airflow/Pipeline** : Orchestration des workflows
- **S3/MinIO** : Stockage des datasets et modèles
- **Modèle DL** : Deep Learning pour classification
- **MLflow/DVC** : Tracking et versioning
- **API** : Service de prédiction
- **WebApp** : Interface utilisateur
- **Kubernetes** : Orchestration des containers
- **Monitoring** : Centralisation des logs et métriques
- **CI/CD** : Automatisation du déploiement
- **Feature Store** : Versioning des features

---

## 🗺️ ROADMAP DÉTAILLÉE

---

## **PHASE 1 : Setup et Préparation (Jours 1-2)**

### 1.1 Structure du Projet
```
mlops-project/
├── dags/                    # DAGs Airflow
├── scripts/                 # Scripts Python
│   ├── data_ingestion.py
│   ├── train_model.py
│   ├── inference.py
│   └── evaluation.py
├── config/                  # Configurations
│   ├── airflow.cfg
│   ├── mlflow_config.yaml
│   └── model_config.yaml
├── models/                  # Modèles entraînés
├── notebooks/               # Notebooks exploration
├── tests/                   # Tests unitaires
├── docker/                  # Dockerfiles
│   ├── Dockerfile.airflow
│   ├── Dockerfile.api
│   └── Dockerfile.webapp
├── kubernetes/              # Manifests K8s
├── monitoring/              # Config monitoring
├── data/                    # Données locales (gitignore)
│   ├── grass/
│   └── dandelion/
├── requirements.txt
├── docker-compose.yml       # Pour développement local
└── README.md
```

### 1.2 Dépendances
- **Core** : Python 3.8+, Apache Airflow 2.x
- **ML** : TensorFlow/Keras ou PyTorch, scikit-learn
- **Tracking** : MLflow
- **Storage** : boto3 (S3), minio
- **API** : FastAPI ou Flask
- **Monitoring** : Prometheus, Grafana
- **Orchestration** : Docker, Kubernetes

### 1.3 Configuration Git
- Initialiser le repo Git
- Ajouter `.gitignore` (data/, models/, logs/)
- Cloner ou récupérer le dataset depuis le repo de référence

---

## **PHASE 2 : Ingestion et Stockage (Jours 3-4)**

### 2.1 Script d'Extraction de Métadonnées
**Scripts/data_ingestion.py**
```python
# Objectif : Extraire métadonnées des images (taille, format, chemin)
# Stocker dans DB (SQLite/PostgreSQL)
# Fonctions à créer :
- extract_image_metadata(image_path)
- store_metadata_to_db(metadata_list)
- generate_dataset_summary()
```

### 2.2 Pipeline Airflow - Ingestion
**DAGs/data_ingestion_dag.py**
- **Task 1** : Scan du dossier data/
- **Task 2** : Extraction métadonnées
- **Task 3** : Insertion en DB
- **Task 4** : Upload vers S3/MinIO
- **Task 5** : Validation et notification

### 2.3 Configuration S3/MinIO
- Setup bucket S3 ou instance MinIO locale
- Organisation :
  ```
  s3://mlops-bucket/
  ├── raw/                  # Images brutes
  ├── processed/            # Images traitées
  ├── train/                # Dataset d'entraînement
  ├── validation/           # Dataset de validation
  ├── test/                 # Dataset de test
  └── models/               # Checkpoints et modèles
  ```

### 2.4 Split Dataset
- Diviser en train/validation/test (70/15/15)
- Script de split automatique

---

## **PHASE 3 : Modèle de Deep Learning (Jours 5-7)**

### 3.1 Notebook Exploratoire
- Analyse des images
- Visualisation de la distribution
- Choix architecture (CNN avec Transfer Learning recommandé)

### 3.2 Architecture du Modèle
**Recommandation** : Transfer Learning avec ResNet50 ou EfficientNet
```python
# Base : Pre-trained model
# Ajout : Couches fully connected
# Output : Binary classification (dandelion/grass)
```

### 3.3 Script d'Entraînement
**Scripts/train_model.py**
- Chargement dataset depuis S3
- Data augmentation
- Entraînement du modèle
- Sauvegarde des checkpoints
- Export du modèle final

### 3.4 Pipeline Airflow - Training
**DAGs/training_dag.py**
- **Task 1** : Validation des données disponibles
- **Task 2** : Téléchargement dataset depuis S3
- **Task 3** : Preprocessing et augmentation
- **Task 4** : Entraînement du modèle
- **Task 5** : Sauvegarde vers S3
- **Task 6** : Notification de fin

**Dépendances** :
- Trigger automatique après ingestion
- Possibilité de réentraînement manuel

---

## **PHASE 4 : MLflow Tracking et Versioning (Jours 8-9)**

### 4.1 Configuration MLflow
**Config/mlflow_config.yaml**
- URI serveur MLflow
- Expériences et runs
- Métriques à tracker : accuracy, loss, f1-score

### 4.2 Intégration dans le Training
**Modifications à apporter :**
- Logger hyperparamètres
- Logger métriques à chaque epoch
- Logger artifacts (graphiques, modèles)
- Enregistrer le modèle dans le Model Registry

### 4.3 Pipeline Airflow - MLflow Integration
**DAGs/mlflow_dag.py**
- **Task 1** : Récupérer le meilleur modèle depuis MLflow
- **Task 2** : Comparer avec modèle en production
- **Task 3** : Décision de déploiement
- **Task 4** : Staging → Production

### 4.4 Système de Versioning
- Git pour le code
- MLflow pour les modèles
- DVC pour les datasets (optionnel)

---

## **PHASE 5 : API de Prédiction (Jours 10-11)**

### 5.1 Développement de l'API REST
**Scripts/api.py** (FastAPI recommandé)

**Endpoints** :
- `POST /predict` : Prédiction sur une image
- `GET /health` : Health check
- `GET /model/info` : Infos du modèle chargé
- `POST /feedback` : Collecter feedback (pour monitoring)

### 5.2 Chargement du Modèle
- Charger depuis S3 ou MLflow Model Registry
- Cache du modèle en mémoire
- Validation format d'input

### 5.3 Tests de l'API
- Tests unitaires
- Tests d'intégration
- Tests de charge

---

## **PHASE 6 : Interface WebApp (Jours 12-13)**

### 6.1 Développement Frontend
**Options** :
- Streamlit (simple et rapide)
- Flask/FastAPI avec templates HTML
- React/Vue.js (plus complexe)

### 6.2 Fonctionnalités
- Upload d'image
- Affichage prédiction (probabilité + classe)
- Historique des prédictions
- Upload par lot

### 6.3 Intégration avec l'API
- Appels REST vers l'API backend
- Gestion erreurs et fallback

---

## **PHASE 7 : Containerisation Docker (Jours 14-15)**

### 7.1 Dockerfile pour Airflow
**Docker/Dockerfile.airflow**
```dockerfile
FROM apache/airflow:2.x
# Install dependencies
# Copy DAGs, scripts, config
```

### 7.2 Dockerfile pour l'API
**Docker/Dockerfile.api**
```dockerfile
FROM python:3.9-slim
# Install dependencies
# Copy application code
# Expose port 8000
```

### 7.3 Dockerfile pour la WebApp
**Docker/Dockerfile.webapp**
```dockerfile
# Selon choix technologique
```

### 7.4 Docker Compose pour Dev Local
**docker-compose.yml**
- Services : Airflow, API, WebApp, MinIO, PostgreSQL, MLflow
- Networking
- Volumes
- Environment variables

### 7.5 Tests Locaux
- Tester tout le pipeline en local
- Vérifier les interactions entre services

---

## **PHASE 8 : Déploiement Kubernetes (Jours 16-18)**

### 8.1 Création des Manifests K8s
**Kubernetes/manifests/**
- `namespace.yaml` : Namespace dédié
- `airflow-deployment.yaml` : Déploiement Airflow
- `airflow-service.yaml` : Service pour Airflow UI
- `api-deployment.yaml` : Déploiement de l'API
- `api-service.yaml` : Service LoadBalancer
- `webapp-deployment.yaml` : Déploiement WebApp
- `webapp-service.yaml` : Service
- `minio-deployment.yaml` : MinIO (si local)
- `mlflow-deployment.yaml` : MLflow (si local)
- `secrets.yaml` : Secrets et credentials
- `configmap.yaml` : Configurations partagées

### 8.2 Déploiement
- Appliquer les manifests
- Configurer Ingress pour exposition
- Vérifier la connectivité

### 8.3 ConfigMaps et Secrets
- S3 credentials
- Database credentials
- API keys

---

## **PHASE 9 : Monitoring et Observabilité (Jours 19-20)**

### 9.1 Setup Monitoring Stack
**Options** :
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Jaeger pour tracing

### 9.2 Métriques à Monitorer
**Airflow** :
- Taux de succès des DAGs
- Durée d'exécution des tâches
- Erreurs et retries

**API** :
- Latence (ms)
- Throughput (req/s)
- Taux d'erreur
- Utilisation CPU/Memory

**Modèle** :
- Drift detection
- Prédictions par classe
- Feedback utilisateurs

### 9.3 Logging Centralisé
- Configuration loggers Python
- Forward logs vers système centralisé
- Alertes sur erreurs critiques

### 9.4 Dashboards Grafana
- Vue d'ensemble du système
- Métriques métier (prédictions par heure)
- Métriques techniques (latence, erreurs)

---

## **PHASE 10 : CI/CD Pipeline (Jours 21-22)**

### 10.1 GitHub Actions / GitLab CI
**Workflows** :
- **Trigger** : Push sur main/develop
- **Lint** : Vérification code quality
- **Tests** : Exécution tests unitaires et intégration
- **Build** : Build des images Docker
- **Push** : Push vers Docker Registry
- **Deploy** : Déploiement sur Kubernetes (staging/prod)

### 10.2 Docker Registry
- Setup registry (Docker Hub, AWS ECR, GCR)
- Configuration Kubernetes pour pull

### 10.3 Stratégie de Déploiement
- **Development** : Latest images
- **Staging** : Tagged versions
- **Production** : Stable releases seulement

---

## **PHASE 11 : Feature Store (Optionnel, Jours 23-24)**

### 11.1 Implémentation Simple
- Fichiers JSON/YAML pour features définies
- Versioning des features avec Git
- Documentation de chaque feature

### 11.2 Intégration dans le Pipeline
- Consulter Feature Store pour features à utiliser
- Éviter la réingénierie de features

---

## **PHASE 12 : Documentation et Livrables (Jours 25-27)**

### 12.1 Documentation Technique
**README.md** :
- Description du projet
- Architecture
- Instructions d'installation
- Guide d'utilisation

**docs/**
- **Architecture.md** : Diagramme et explications
- **Deployment.md** : Guide de déploiement
- **Contributing.md** : Guide de contribution
- **API.md** : Documentation API

### 12.2 Diagrammes
- Diagramme d'architecture globale
- Diagramme de flux de données
- Diagramme de séquence pour prediction

### 12.3 Documentation Utilisateur
- Guide d'utilisation de la WebApp
- Guide pour upload d'images
- FAQ

### 12.4 Présentation
- Slides de présentation du projet
- Démo du système en fonctionnement
- Résultats et métriques

---

## 📊 Vue d'Ensemble du Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     ML PIPELINE COMPLET                         │
└─────────────────────────────────────────────────────────────────┘

1. DATA INGESTION (Airflow DAG)
   ├── Scan images data/{grass, dandelion}
   ├── Extract metadata → PostgreSQL
   └── Upload to S3/MinIO

2. DATA PREPARATION (Airflow Task)
   ├── Download from S3
   ├── Split train/val/test
   └── Preprocessing & Augmentation

3. MODEL TRAINING (Airflow DAG)
   ├── Load dataset
   ├── Train CNN model
   ├── Save checkpoints to S3
   └── Log metrics to MLflow

4. MODEL VERSIONING (MLflow)
   ├── Track experiments
   ├── Compare models
   └── Register best model

5. DEPLOYMENT (Kubernetes)
   ├── API service loads model from S3
   ├── WebApp frontend connects to API
   └── Services exposed via Ingress

6. MONITORING (Continuous)
   ├── Track predictions
   ├── Monitor drift
   ├── Collect feedback
   └── Alert on issues

7. RETRAINING (Automated)
   ├── Schedule periodic retrain
   ├── Check model performance
   └── Deploy if improvement
```

---

## 🛠️ Outils et Technologies

### Orchestration
- **Apache Airflow** : Workflow orchestration
- **Kubernetes** : Container orchestration
- **Docker** : Containerization

### ML
- **TensorFlow/Keras** : Deep Learning framework
- **MLflow** : Experiment tracking
- **Pandas/NumPy** : Data manipulation

### Storage
- **S3/MinIO** : Object storage
- **PostgreSQL/SQLite** : Metadata database

### API & Frontend
- **FastAPI** : REST API
- **Streamlit/Flask** : Web interface

### Monitoring
- **Prometheus** : Metrics collection
- **Grafana** : Visualization
- **ELK** : Log aggregation

### CI/CD
- **GitHub Actions / GitLab CI** : Automation
- **Docker Registry** : Image storage

---

## 📝 Checklist de Validation

### Phase 1-2 : Setup ✅
- [ ] Structure projet créée
- [ ] Dépendances installées
- [ ] Dataset récupéré
- [ ] S3/MinIO accessible

### Phase 3-4 : ML ✅
- [ ] Modèle entraîne avec succès
- [ ] Métriques > 90% accuracy
- [ ] MLflow tracking opérationnel
- [ ] Modèle sauvegardé sur S3

### Phase 5-6 : API & WebApp ✅
- [ ] API répond aux requêtes
- [ ] Prédictions correctes
- [ ] WebApp fonctionnelle
- [ ] Tests passent

### Phase 7-8 : Containerisation ✅
- [ ] Images Docker buildées
- [ ] docker-compose fonctionne
- [ ] K8s manifests créés
- [ ] Déploiement réussi

### Phase 9 : Monitoring ✅
- [ ] Métriques collectées
- [ ] Dashboards créés
- [ ] Alertes configurées

### Phase 10 : CI/CD ✅
- [ ] Pipeline automatisé
- [ ] Tests automatisés
- [ ] Déploiement automatique

### Phase 11-12 : Finalisation ✅
- [ ] Documentation complète
- [ ] Présentation prête
- [ ] Code commenté
- [ ] Demo fonctionnelle

---

## 🚀 Points d'Attention Importants

1. **Dataset** : Vérifier que le dataset est bien équilibré (50/50)
2. **Versioning** : Toujours versionner code, données, modèles
3. **Sécurité** : Ne pas commiter les credentials
4. **Performance** : Optimiser pour latence < 500ms
5. **Scalabilité** : Prévoir scaling horizontal (K8s HPA)
6. **Monitoring** : Toujours monitorer le drift du modèle
7. **Documentation** : Documenter chaque étape pour reproducibilité

---

## 📚 Ressources et Références

- Repo de référence : https://github.com/btphan95/greenr-airflow.git
- Documentation Airflow : https://airflow.apache.org/docs/
- Documentation MLflow : https://www.mlflow.org/docs/latest/index.html
- Documentation Kubernetes : https://kubernetes.io/docs/
- Documentation FastAPI : https://fastapi.tiangolo.com/
- Documentation S3 : https://docs.aws.amazon.com/s3/

---

## 💡 Conseils Pratiques

1. **Commencer Simple** : MVP fonctionnel avant optimisation
2. **Tester Régulièrement** : Tests à chaque étape
3. **Versionner** : Git commit fréquents
4. **Documenter** : Prendre des notes pendant le développement
5. **Itérer** : Améliorer petit à petit
6. **Demander Aide** : Utiliser les ressources des sessions

---

**🎯 Bon courage pour votre projet MLOps !**

