# 🚀 Commandes pour Lancer Tous les Services

## 📍 Dans quel dossier vous positionner ?

```bash
/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops
```

**C'est le dossier de VOTRE projet** où se trouvent :
- `scripts/webapp.py`
- `scripts/api.py`
- `dags/`
- `data/`
- `models/`
- etc.

---

## 🖥️ Commandes à Taper (Copier-Coller)

### Option 1 : Via le Finder
```bash
# Ouvrir Terminal
# Aller dans le dossier du projet
cd ~/Documents/Master\ 2/MLOps/emmaloou-ML_Ops

# Activer l'environnement
source venv/bin/activate

# Lancer Streamlit
streamlit run scripts/webapp.py
```

### Option 2 : Chemin Absolu
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate
streamlit run scripts/webapp.py
```

---

## 🎯 Services à Lancer (Si Nécessaire)

### 1. Lancer Docker Services (Déjà fait ✅)
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
docker compose up -d
```

**Accessible sur** :
- MinIO : http://localhost:9001
- MLflow : http://localhost:5001

### 2. Lancer l'API (Déjà fait ✅)
L'API tourne déjà en arrière-plan sur le port 8000 ✅

**Accessible sur** : http://localhost:8000

### 3. Lancer la WebApp (À faire maintenant)
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate
streamlit run scripts/webapp.py
```

**Accessible sur** : http://localhost:8501

---

## 📝 Résumé : Où se Positionner ?

**Dossier** : 
```
/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops
```

**Commande dans ce dossier** :
```bash
streamlit run scripts/webapp.py
```

⚠️ **Important** : Vous devez être DANS le dossier `emmaloou-ML_Ops` (la racine du projet) !

