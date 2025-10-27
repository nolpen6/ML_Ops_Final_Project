# 🚀 Guide de Démarrage - Projet MLOps

## 📍 Où en sommes-nous ?

Le repository **emmaloou/ML_Ops** est maintenant organisé avec :
- ✅ Scripts de base (data_preparation, model_train, api)
- ✅ Configuration pour Airflow et MLflow
- ✅ Docker Compose pour services locaux (MinIO, MLflow, PostgreSQL)
- ✅ Roadmap détaillée dans `docs/ROADMAP_MLOps_PROJECT.md`
- ✅ README principal
- ✅ Requirements.txt

## 🎯 Prochaines Étapes (selon la roadmap)

### Phase 1 : Setup Local (Jours 1-2)

1. **Lancer les services avec Docker Compose**
```bash
cd /path/to/emmaloou-ML_Ops
docker-compose up -d
```

Cela lance :
- MinIO sur http://localhost:9000
- MLflow sur http://localhost:5000
- PostgreSQL sur localhost:5432

2. **Créer le bucket MinIO**
```bash
# Via l'interface web http://localhost:9001
# ou avec mc (MinIO Client)
```

3. **Télécharger le dataset**
```bash
# Récupérer les images depuis le repo de référence ou créer vos dossiers
mkdir -p data/{grass,dandelion}
# Placer les images dans ces dossiers
```

### Phase 2 : Tests Locaux (Jours 3-4)

1. **Tester la préparation des données**
```bash
python scripts/data_preparation.py
```

2. **Entraîner un premier modèle**
```bash
python scripts/model_train.py
```

3. **Tester l'API**
```bash
uvicorn scripts.api:app --reload
# Tester avec : curl -X POST http://localhost:8000/predict
```

### Phase 3 : Créer les DAGs Airflow (Jours 5-7)

À créer dans le dossier `dags/` :
- `data_ingestion_dag.py` : Pour ingérer les données
- `training_dag.py` : Pour orchestrer l'entraînement
- `model_deployment_dag.py` : Pour déployer les modèles

### Phase 4 : Dockerisation (Jours 8-10)

À créer dans le dossier `docker/` :
- `Dockerfile.airflow` : Pour les DAGs Airflow
- `Dockerfile.api` : Pour l'API
- `Dockerfile.webapp` : Pour la WebApp

### Phase 5 : Kubernetes (Jours 11-13)

À créer dans le dossier `kubernetes/` :
- Manifests pour déployer tous les services
- ConfigMaps et Secrets
- Services et Ingress

### Phase 6 : Monitoring & Finalisation (Jours 14-27)

- Setup Prometheus et Grafana
- Créer les dashboards
- Finaliser la documentation
- Tests et validation

## 📁 À Compléter (dossiers vides)

Ces dossiers sont créés mais vides pour l'instant :
- `dags/` : À ajouter les DAGs Airflow
- `docker/` : À ajouter les Dockerfiles
- `kubernetes/` : À ajouter les manifests K8s
- `monitoring/` : À ajouter config Prometheus/Grafana

## 🔗 Ressources Utiles

- **Repo de référence** : https://github.com/btphan95/greenr-airflow.git
- **Documentation Airflow** : https://airflow.apache.org/docs/
- **Documentation MLflow** : https://www.mlflow.org/docs/
- **Documentation MinIO** : https://min.io/docs/
- **Documentation FastAPI** : https://fastapi.tiangolo.com/

## 💡 Conseils

1. **Commencez simple** : Testez chaque script individuellement
2. **Versionnez** : Faites des commits fréquents
3. **Testez localement** : Docker Compose pour tout tester en local
4. **Suivez la roadmap** : `docs/ROADMAP_MLOps_PROJECT.md` contient les étapes détaillées

---

**C'est parti ! 🚀**

