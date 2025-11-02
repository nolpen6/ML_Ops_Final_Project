# 🔄 Configuration d'Airflow avec Docker

## 📋 Vue d'Ensemble

Airflow est maintenant configuré pour fonctionner avec Docker Compose. Cela simplifie grandement la configuration et l'utilisation.

---

## 🚀 Lancement Rapide (Docker)

### Étape 1 : Créer les dossiers nécessaires

```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
mkdir -p airflow/logs airflow/config
```

### Étape 2 : Lancer tous les services

```bash
# Arrêter les services existants (si lancés)
docker compose down

# Lancer tous les services (MinIO, MLflow, PostgreSQL, Redis, Airflow)
docker compose up -d

# Vérifier que tous les services sont lancés
docker compose ps
```

### Étape 3 : Vérifier les logs d'initialisation

```bash
# Voir les logs d'Airflow init (pour vérifier que l'initialisation est réussie)
docker compose logs airflow-init

# Voir les logs du webserver
docker compose logs airflow-webserver

# Voir les logs du scheduler
docker compose logs airflow-scheduler
```

### Étape 4 : Accéder à l'interface Airflow

Ouvrez votre navigateur sur : **http://localhost:8080**

- **Username** : `admin`
- **Password** : `admin`

Les DAGs devraient apparaître automatiquement :
- `data_ingestion` : Ingestion des données vers MinIO
- `training` : Entraînement du modèle

---

## 📦 Services Docker

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| **Airflow Webserver** | 8080 | http://localhost:8080 | Interface web Airflow |
| **Airflow Scheduler** | - | - | Planificateur des tâches |
| **MinIO** | 9001 | http://localhost:9001 | Storage S3-compatible |
| **MLflow** | 5001 | http://localhost:5001 | Tracking ML |
| **PostgreSQL** | 5433 | localhost:5433 | Base de données Airflow |
| **Redis** | 6379 | localhost:6379 | Cache Airflow |

---

## 🔧 Installation des Dépendances Python dans Airflow

Les scripts Airflow nécessitent PyTorch et d'autres dépendances. Pour les installer dans les containers :

### Option 1 : Installation manuelle (si nécessaire)

```bash
# Se connecter au container Airflow
docker compose exec airflow-webserver bash

# Installer les dépendances
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install boto3 mlflow pandas numpy Pillow scikit-learn requests

# Ou utiliser le script
bash /opt/airflow/docker/install_airflow_dependencies.sh
```

### Option 2 : Utiliser le Dockerfile personnalisé (recommandé)

Pour installer automatiquement les dépendances, vous pouvez utiliser le Dockerfile personnalisé :

```bash
# Construire l'image personnalisée
docker build -f docker/Dockerfile.airflow -t mlops-airflow:custom .

# Puis modifier docker-compose.yml pour utiliser cette image
# Remplacer: image: apache/airflow:2.8.0
# Par: image: mlops-airflow:custom
```

---

## 📁 Structure des Volumes

Les dossiers suivants sont montés dans les containers Airflow :

```
./dags              → /opt/airflow/dags       (DAGs Airflow)
./airflow/logs      → /opt/airflow/logs      (Logs des tâches)
./airflow/config    → /opt/airflow/config    (Configuration)
./scripts           → /opt/airflow/scripts   (Scripts Python)
./models            → /opt/airflow/models     (Modèles entraînés)
./data              → /opt/airflow/data       (Données d'entraînement)
```

---

## 🧪 Tester les DAGs

### Dans l'interface Airflow

1. Allez sur http://localhost:8080
2. Connectez-vous (admin/admin)
3. Vous devriez voir 2 DAGs :
   - `data_ingestion`
   - `training`
4. Cliquez sur le bouton **▶️** pour déclencher un DAG manuellement
5. Cliquez sur le nom du DAG pour voir les détails
6. Cliquez sur une tâche pour voir les logs

### Via la ligne de commande

```bash
# Lister les DAGs
docker compose exec airflow-webserver airflow dags list

# Déclencher un DAG manuellement
docker compose exec airflow-webserver airflow dags trigger data_ingestion

# Voir les logs d'une tâche
docker compose exec airflow-webserver airflow tasks logs data_ingestion scan_images 2024-01-01
```

---

## 🛠️ Commandes Utiles

### Gestion des services

```bash
# Démarrer les services
docker compose up -d

# Arrêter les services
docker compose down

# Redémarrer un service spécifique
docker compose restart airflow-webserver

# Voir les logs en temps réel
docker compose logs -f airflow-webserver
docker compose logs -f airflow-scheduler
```

### Gestion d'Airflow

```bash
# Se connecter au container
docker compose exec airflow-webserver bash

# Créer un nouvel utilisateur (depuis le container)
airflow users create \
    --username user \
    --firstname User \
    --lastname User \
    --role User \
    --email user@example.com \
    --password password

# Lister les connexions
docker compose exec airflow-webserver airflow connections list
```

---

## ⚠️ Configuration des Connexions

Si vous devez configurer des connexions (MinIO, etc.) dans Airflow :

1. Allez dans **Admin → Connections**
2. Ajoutez une nouvelle connexion :
   - **Connection Type** : S3
   - **Host** : `http://minio:9000`
   - **Login** : `minioadmin`
   - **Password** : `minioadmin`

Ou via la CLI :

```bash
docker compose exec airflow-webserver airflow connections add minio \
    --conn-type s3 \
    --conn-host http://minio:9000 \
    --conn-login minioadmin \
    --conn-password minioadmin
```

---

## 🔍 Dépannage

### Les DAGs n'apparaissent pas

1. Vérifiez les logs : `docker compose logs airflow-scheduler`
2. Vérifiez que les DAGs sont dans `./dags/`
3. Vérifiez les erreurs Python dans les logs
4. Redémarrez le scheduler : `docker compose restart airflow-scheduler`

### Erreur "Module not found"

Les dépendances Python ne sont pas installées. Installez-les :

```bash
docker compose exec airflow-webserver pip install torch torchvision boto3 mlflow
```

### Erreur de connexion PostgreSQL

Vérifiez que PostgreSQL est démarré :

```bash
docker compose ps postgres
docker compose logs postgres
```

### Réinitialiser complètement Airflow

```bash
# Arrêter et supprimer les volumes
docker compose down -v

# Supprimer les dossiers Airflow locaux (ATTENTION : supprime les logs)
rm -rf airflow/logs/* airflow/config/*

# Relancer
docker compose up -d
```

---

## 📝 Configuration Alternative (Local - Sans Docker)

Si vous préférez utiliser Airflow localement sans Docker :

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
export AIRFLOW_HOME=$(pwd)/airflow
source venv/bin/activate
airflow scheduler
```

**Terminal 2 - Webserver** :
```bash
export AIRFLOW_HOME=$(pwd)/airflow
source venv/bin/activate
airflow webserver --port 8080
```

---

## 🎯 Prochaines Étapes

1. ✅ **Airflow configuré** avec Docker
2. ✅ **DAGs créés** et prêts à être utilisés
3. ➡️ **Tester les DAGs** manuellement dans l'interface
4. ➡️ **Configurer les connexions** MinIO si nécessaire
5. ➡️ **Automatiser** l'entraînement avec le DAG training

---

**🎉 Airflow est maintenant prêt à être utilisé !**
