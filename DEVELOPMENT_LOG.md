# 📝 Development Log - Projet MLOps

## 📍 Emplacement Local
```
/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops
```

## 🌿 Branche de Travail
- **Branche** : `Matthieu`
- **Statut** : Travail en local uniquement
- **Remote** : Pas encore pushé sur GitHub

---

## 📅 Journal des Développements

### [Étape 0] Setup Initial - 27 Octobre 2024

**Objectif** : Organiser la structure du projet MLOps

**Actions réalisées** :
1. ✅ Création de la branche `Matthieu` à partir de `main`
2. ✅ Copie des scripts existants dans `scripts/`
   - `api.py` : API FastAPI pour prédictions
   - `data_preparation.py` : Préparation des données
   - `model_train.py` : Entraînement du modèle ResNet18
   - `upload_to_minio.py` : Upload vers MinIO (adapté depuis S3)
3. ✅ Création des configurations
   - `config/airflow_config.yaml` : Configuration Airflow
   - `config/mlflow_config.yaml` : Configuration MLflow
4. ✅ Création du docker-compose.yml
   - MinIO (http://localhost:9000)
   - MLflow (http://localhost:5000)
   - PostgreSQL (localhost:5432)
5. ✅ Documentation complète
   - `README.md` : Documentation principale
   - `docs/ROADMAP_MLOps_PROJECT.md` : Roadmap complète (27 jours)
   - `docs/RESUME_PROJECT.md` : Résumé rapide
   - `docs/GETTING_STARTED.md` : Guide de démarrage
6. ✅ Requirements.txt : Toutes les dépendances
7. ✅ .gitignore : Fichiers à ignorer

**Commit** : `2158c15` - feat: Structure MLOps organisée
**Fichiers** : 13 fichiers, 1322 lignes ajoutées

**État** : ✅ Complété

---

### [Étape 1] (À venir)

**Objectif** : 

**Actions à réaliser** :

**État** : 🔄 En attente

---

## 📊 Checklist Globale

### Phase 1 : Setup de base
- [x] Structure de dossiers
- [x] Scripts existants organisés
- [x] Configurations de base
- [x] Documentation
- [ ] Dataset téléchargé
- [ ] Environnement virtuel créé
- [ ] Dépendances installées

### Phase 2 : Data & Training
- [ ] Test des scripts de préparation
- [ ] Entraînement du premier modèle
- [ ] Test de l'API localement
- [ ] Upload du modèle vers MinIO

### Phase 3 : Airflow
- [ ] Installation Airflow local
- [ ] Création DAG data_ingestion
- [ ] Création DAG training
- [ ] Création DAG deployment
- [ ] Tests des DAGs

### Phase 4 : Dockerisation
- [ ] Dockerfile pour l'API
- [ ] Dockerfile pour WebApp
- [ ] Dockerfile pour Airflow
- [ ] Tests docker-compose

### Phase 5 : Kubernetes
- [ ] Manifests de déploiement
- [ ] Services et Ingress
- [ ] ConfigMaps et Secrets
- [ ] Tests de déploiement

### Phase 6 : Monitoring & CI/CD
- [ ] Setup Prometheus/Grafana
- [ ] Dashboard de monitoring
- [ ] CI/CD pipeline
- [ ] Tests finaux

---

## 🔗 Liens Utiles
- Repo GitHub : https://github.com/emmaloou/ML_Ops
- Branche main : https://github.com/emmaloou/ML_Ops/tree/main
- Branche Matthieu : (pas encore pushée)

---

## 💡 Notes
- Tous les fichiers sont trackés en local
- Utiliser `git log` pour voir l'historique
- Utiliser `git status` pour voir l'état actuel
- Chaque étape doit être commitée avec un message clair

