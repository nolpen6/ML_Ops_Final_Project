# 🔐 Identifiants MinIO

## 📍 Où sont-ils configurés ?

Les identifiants sont définis dans `docker-compose.yml` aux lignes **14-15** :

```yaml
environment:
  MINIO_ROOT_USER: minioadmin      # ← Username par défaut
  MINIO_ROOT_PASSWORD: minioadmin  # ← Password par défaut
```

## 🔑 Identifiants par Défaut

Pour se connecter à MinIO Console :

- **Username** : `minioadmin`
- **Password** : `minioadmin`

## 💡 Pourquoi ces identifiants ?

Ce sont les **identifiants par défaut** que nous avons configurés dans le fichier `docker-compose.yml`.

Ils sont identiques aux identifiants MinIO par défaut pour faciliter le développement local.

### ⚠️ Important pour Production

En production, vous devriez :
1. **Changer ces identifiants** pour des identifiants sécurisés
2. **Utiliser des secrets** (via fichiers .env ou outils de gestion de secrets)
3. **Ne jamais commiter** des identifiants en clair dans Git

## 🔒 Comment Changer les Identifiants

Si vous voulez changer les identifiants :

1. Modifier `docker-compose.yml` :
```yaml
environment:
  MINIO_ROOT_USER: votre_username
  MINIO_ROOT_PASSWORD: votre_password
```

2. Redémarrer les services :
```bash
docker compose down
docker compose up -d
```

3. Se reconnecter avec les nouveaux identifiants

---

**Pour l'instant, utilisez** : `minioadmin` / `minioadmin` ✅

