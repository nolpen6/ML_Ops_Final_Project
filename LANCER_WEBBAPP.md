# 🌐 Lancer la WebApp Streamlit

## ⚠️ Problème Constaté

La WebApp ne démarre pas correctement en arrière-plan. Voici comment la lancer **manuellement** pour voir les erreurs.

---

## 🚀 Méthode : Lancer Manuellement

### 1. Ouvrir un nouveau terminal

Ouvrez **Terminal** ou **iTerm2**.

### 2. Naviguer vers le projet

```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
```

### 3. Activer l'environnement

```bash
source venv/bin/activate
```

### 4. Installer Streamlit et Requests (si nécessaire)

```bash
pip install streamlit requests
```

### 5. Lancer la WebApp

```bash
streamlit run scripts/webapp.py
```

**Vous verrez** :
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### 6. Ouvrir dans le navigateur

Copiez-collez le "Local URL" dans votre navigateur.

---

## ✅ Si Ça Marche

Vous verrez une interface avec :
- 📤 Zone d'upload d'image
- 🎯 Résultat de la prédiction
- 📊 Confiance du modèle

**L'API doit être lancée en arrière-plan** pour que ça fonctionne !

---

## 🔍 Vérifier que l'API Fonctionne

**Dans un AUTRE terminal** :

```bash
curl http://localhost:8000/health
```

Si ça retourne `{"status":"healthy"}`, l'API fonctionne ✅

---

## 🛠️ Si Ça Ne Marche Toujours Pas

### Option 1 : Lancer l'API aussi

```bash
# Terminal 1 - API
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate
python scripts/api.py

# Terminal 2 - WebApp
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate
streamlit run scripts/webapp.py
```

### Option 2 : Tester juste l'API

```bash
# Tester l'API directement
curl http://localhost:8000/
curl http://localhost:8000/health

# Tester avec une image
curl -X POST http://localhost:8000/predict/ \
  -F "file=@data/dandelion/00000000.jpg"
```

---

## 📝 Résumé

**Pour utiliser la WebApp** :
1. ✅ L'API doit tourner sur http://localhost:8000
2. ✅ Streamlit lance l'interface sur http://localhost:8501
3. ✅ Uploadez une image
4. ✅ Obtenez la prédiction !

**Essayez de la lancer manuellement maintenant !**

