# 🚀 Guide Rapide - Lancer Airflow

## ⚡ Démarrage Rapide (3 étapes)

### 1. Lancer tous les services

```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
docker compose up -d
```

### 2. Attendre l'initialisation (30-60 secondes)

```bash
# Vérifier les logs d'initialisation
docker compose logs -f airflow-init
```

Appuyez sur `Ctrl+C` une fois que vous voyez "✅ Initialisation terminée" ou que le container s'arrête.

### 3. Accéder à l'interface

Ouvrez : **http://localhost:8080**
- Username : `admin`
- Password : `admin`

---

## ✅ Vérification

### Vérifier que tous les services sont lancés

```bash
docker compose ps
```

Vous devriez voir :
- ✅ mlops-postgres (healthy)
- ✅ mlops-redis (healthy)
- ✅ mlops-minio
- ✅ mlops-mlflow
- ✅ mlops-airflow-webserver
- ✅ mlops-airflow-scheduler

### Vérifier les DAGs

1. Allez sur http://localhost:8080
2. Connectez-vous (admin/admin)
3. Vous devriez voir 2 DAGs :
   - `data_ingestion` (paused par défaut)
   - `training` (paused par défaut)

### Activer et tester un DAG

1. Cliquez sur le toggle pour **activer** le DAG
2. Cliquez sur **▶️** pour le déclencher manuellement
3. Cliquez sur le nom du DAG pour voir les détails
4. Surveillez l'exécution en temps réel

---

## 🔧 Installation des Dépendances Python (si nécessaire)

Si les DAGs échouent avec "Module not found", installez les dépendances :

```bash
# Se connecter au container
docker compose exec airflow-webserver bash

# Installer PyTorch (CPU version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Installer les autres dépendances
pip install boto3 mlflow pandas numpy Pillow scikit-learn requests

# Sortir du container
exit
```

---

## 📊 Services Disponibles

| Service | URL | Identifiants |
|---------|-----|--------------|
| **Airflow** | http://localhost:8080 | admin / admin |
| **MinIO** | http://localhost:9001 | minioadmin / minioadmin |
| **MLflow** | http://localhost:5001 | - |

---

## 🛑 Arrêter les Services

```bash
docker compose down
```

Pour arrêter et supprimer les volumes (réinitialisation complète) :

```bash
docker compose down -v
```

---

## 🆘 Dépannage

### Les DAGs n'apparaissent pas

```bash
# Vérifier les logs du scheduler
docker compose logs airflow-scheduler

# Redémarrer le scheduler
docker compose restart airflow-scheduler
```

### Erreur de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL est lancé
docker compose ps postgres

# Voir les logs
docker compose logs postgres
```

### Container ne démarre pas

```bash
# Voir tous les logs
docker compose logs

# Redémarrer un service spécifique
docker compose restart airflow-webserver
```

---

**🎉 Tout est prêt ! Ouvrez http://localhost:8080 pour commencer !**

