# 🔄 Configuration d'Airflow

## 📋 Ce qui va être fait

1. ✅ Créer les dossiers Airflow (`AIRFLOW_HOME`)
2. ✅ Initialiser la base de données (SQLite pour simplifier)
3. ✅ Créer les premiers DAGs
4. ✅ Lancer Airflow webserver et scheduler

---

## 🗂️ Structure Créée

```
emmaloou-ML_Ops/
├── airflow/
│   ├── dags/              # DAGs Airflow
│   ├── logs/              # Logs des tâches
│   ├── plugins/           # Plugins personnalisés
│   └── config/            # Configurations Airflow
```

---

## 🚀 Commandes pour Lancer Airflow

### Initialiser la DB
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
export AIRFLOW_HOME=$(pwd)/airflow
source venv/bin/activate

# Initialiser la base de données
airflow db init

# Créer un utilisateur admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname Admin \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### Lancer Airflow (2 terminaux)

**Terminal 1 - Scheduler** :
```bash
airflow scheduler
```

**Terminal 2 - Webserver** :
```bash
airflow webserver --port 8080
```

### Accéder à l'interface
http://localhost:8080
- Username : `admin`
- Password : `admin`

---

## ⚙️ Pour Simplifier : Utiliser la Version Simplifiée

Pour éviter de configurer Airflow complet maintenant, nous allons :
1. Créer les DAGs dans le dossier `dags/`
2. Utiliser une version plus simple avec Docker plus tard
3. Se concentrer sur la création des DAGs

---

## 📝 Prochaines Étapes

Après la configuration de base, nous créerons :
1. `data_ingestion_dag.py` : Pour ingérer les données vers MinIO
2. `training_dag.py` : Pour orchestrer l'entraînement
3. `deployment_dag.py` : Pour déployer les modèles

