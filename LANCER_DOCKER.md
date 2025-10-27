# 🐳 Guide pour Lancer Docker Compose

## ⚠️ Docker Desktop n'est pas lancé

Pour lancer les services (MinIO, MLflow, PostgreSQL, Redis), vous devez :

### 1. Ouvrir Docker Desktop
```bash
# Option 1 : Via le terminal
open -a Docker

# Option 2 : Via l'Application Finder
# Recherchez "Docker" et lancez-le
```

### 2. Attendre que Docker soit prêt
Attendez que l'icône Docker dans la barre de menu soit verte (Docker est running).

### 3. Lancer Docker Compose
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
docker compose up -d
```

## 🔍 Vérifier que Docker est lancé

```bash
docker ps
```

Si vous voyez des containers, Docker est bien lancé.

## 📦 Services qui seront lancés

Une fois Docker Compose lancé, vous aurez :

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| **MinIO** | 9000 | http://localhost:9000 | API MinIO |
| **MinIO Console** | 9001 | http://localhost:9001 | Interface web MinIO |
| **MLflow** | 5000 | http://localhost:5000 | Tracking UI |
| **PostgreSQL** | 5432 | localhost:5432 | Base de données |
| **Redis** | 6379 | localhost:6379 | Cache |

## 🔐 Identifiants par défaut

### MinIO
- **Username** : `minioadmin`
- **Password** : `minioadmin`

### PostgreSQL
- **User** : `airflow`
- **Password** : `airflow`
- **Database** : `mlops`

### Redis
- Pas d'authentification par défaut

## ✅ Une fois les services lancés

### 1. Vérifier que tout fonctionne
```bash
docker compose ps
```

### 2. Voir les logs
```bash
docker compose logs -f
```

### 3. Arrêter les services
```bash
docker compose down
```

## 🚀 Prochaines étapes après le lancement

1. **Accéder à MinIO Console** : http://localhost:9001
2. **Créer un bucket** pour stocker les modèles
3. **Uploader le modèle** vers MinIO
4. **Voir MLflow** : http://localhost:5000
5. **Modifier les scripts** pour utiliser MLflow server distant

---

**Quand Docker Desktop sera prêt, relancez moi pour continuer !** 🐳

