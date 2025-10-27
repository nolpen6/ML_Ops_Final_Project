# 📖 Guide d'Utilisation - Pipeline MLOps Complet

## 🎯 Vue d'Ensemble

Vous avez maintenant un pipeline MLOps complet avec :
- ✅ Modèle entraîné (83.33% accuracy)
- ✅ API REST fonctionnelle
- ✅ WebApp Streamlit
- ✅ Services Docker (MinIO, MLflow, PostgreSQL, Redis)
- ✅ DAGs Airflow
- ✅ Upload vers MinIO

---

## 🚀 Comment Utiliser Chaque Composant

### 1. 📡 API REST

**Lancer l'API** :
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate
python scripts/api.py
```

**Accessible sur** : http://localhost:8000
- Page d'accueil : http://localhost:8000/
- Health check : http://localhost:8000/health
- Prédictions : http://localhost:8000/predict/
- Documentation : http://localhost:8000/docs

**Tester** :
```bash
curl -X POST http://localhost:8000/predict/ \
  -F "file=@data/dandelion/00000000.jpg"
```

---

### 2. 🌐 WebApp Streamlit

**Lancer la WebApp** :
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate

# Installer streamlit si nécessaire
pip install streamlit requests

# Lancer
streamlit run scripts/webapp.py
```

**Accessible sur** : http://localhost:8501

**Fonctionnalités** :
- Upload d'image via interface
- Prédiction en temps réel
- Affichage de la confiance
- Liens vers API, MLflow, MinIO

⚠️ **Note** : L'API doit être lancée sur le port 8000 pour que la WebApp fonctionne.

---

### 3. 🐳 Services Docker

**État actuel** :
```bash
docker compose ps
```

**Services disponibles** :
- **MinIO** : http://localhost:9001 (minioadmin/minioadmin)
- **MLflow** : http://localhost:5001
- **PostgreSQL** : localhost:5433 (airflow/airflow)
- **Redis** : localhost:6379

**Commandes utiles** :
```bash
# Voir les logs
docker compose logs -f mlflow

# Arrêter
docker compose down

# Redémarrer
docker compose restart
```

---

### 4. ☁️ MinIO

**Créer des buckets** (via l'interface web) :
1. Connectez-vous sur http://localhost:9001
2. Cliquez sur "Create Bucket"
3. Créez :
   - `mlops-models` (modèles entraînés)
   - `mlops-data` (datasets)
   - `mlops-artifacts` (MLflow artifacts)

**Uploader manuellement** :
```bash
# Via l'interface web
# Upload fichier → Bucket → Parcourir et uploader
```

**Via script** :
```bash
python scripts/upload_model_to_minio.py
```

---

### 5. 🔄 DAGs Airflow

**Les DAGs sont prêts** dans `dags/` :
- `data_ingestion_dag.py` : Scanne et upload les images
- `training_dag.py` : Entraîne et upload le modèle

**Pour les utiliser** :
1. Configurer Airflow (voir `SETUP_AIRFLOW.md`)
2. Copier les dags dans `airflow/dags/`
3. Les DAGs apparaîtront dans l'interface Airflow

---

## 📊 Architecture Complète

```
┌───────────────────────────────────────────────────┐
│                  UTILISATEUR                      │
└───────────────────────────────────────────────────┘
                          ↓
┌───────────────────────────────────────────────────┐
│              WEBAPP (Streamlit)                   │
│         http://localhost:8501                    │
└───────────────────────────────────────────────────┘
                          ↓
┌───────────────────────────────────────────────────┐
│              API (FastAPI)                       │
│         http://localhost:8000                    │
│  Charger modèle depuis models/                    │
└───────────────────────────────────────────────────┘
                          ↑
┌───────────────────────────────────────────────────┐
│              DAGs AIRFLOW                         │
│  • data_ingestion_dag                             │
│  • training_dag                                  │
└───────────────────────────────────────────────────┘
                          ↓
┌───────────────────────────────────────────────────┐
│              SERVICES DOCKER                      │
│  • MinIO : Storage (http://9001)                  │
│  • MLflow : Tracking (http://5001)               │
│  • PostgreSQL : Metadata (5433)                  │
│  • Redis : Cache (6379)                          │
└───────────────────────────────────────────────────┘
```

---

## 🧪 Tests Rapides

### Test 1 : API
```bash
curl http://localhost:8000/health
```

### Test 2 : WebApp
```bash
streamlit run scripts/webapp.py
# Ouvrir http://localhost:8501
```

### Test 3 : MinIO
```bash
open http://localhost:9001
# Login : minioadmin / minioadmin
```

### Test 4 : MLflow
```bash
open http://localhost:5001
```

---

## 📝 Fichiers Importants

| Fichier | Description |
|---------|-------------|
| `scripts/api.py` | API REST FastAPI |
| `scripts/webapp.py` | WebApp Streamlit |
| `scripts/model_train.py` | Entraînement avec validation |
| `scripts/upload_model_to_minio.py` | Upload vers MinIO |
| `dags/*.py` | DAGs Airflow |
| `docker-compose.yml` | Services Docker |

---

## 🎯 Prochaines Étapes Suggérées

### Court Terme
1. ✅ Tester la WebApp
2. ✅ Créer des buckets dans MinIO
3. ✅ Uploader plus de modèles vers MinIO
4. ✅ Configurer Airflow complet

### Moyen Terme
1. Créer Dockerfiles pour API et WebApp
2. Déployer sur Kubernetes
3. Ajouter monitoring (Prometheus, Grafana)
4. Configurer CI/CD

### Long Terme
1. Feature Store
2. Retraining automatique
3. A/B testing
4. Production-ready pipeline

---

## 💡 Tips

- **API + WebApp** : Lancer les deux en parallèle (2 terminaux)
- **MinIO** : Stockez les modèles ET les datasets
- **MLflow** : Utilisez pour comparer les modèles
- **Airflow** : Pour automatiser tout le pipeline

**🎉 Vous avez maintenant une infrastructure MLOps complète !**

