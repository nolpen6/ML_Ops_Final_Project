# 🧪 Guide de Test - Environnement Python

## ✅ Ce qui a été fait

L'environnement Python est maintenant configuré avec toutes les dépendances nécessaires :

- **PyTorch** 2.9.0 : Framework de deep learning
- **FastAPI** 0.117.1 : Framework web pour l'API
- **MLflow** 3.5.1 : Tracking des expériences ML
- **Torchvision** : Pour le traitement d'images
- **Boto3** : Pour MinIO/S3
- **Autres dépendances** : scikit-learn, pandas, etc.

**Lieu** : `/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops/`

---

## 🧪 Comment tester que tout fonctionne

### Test 1 : Vérifier Python
```bash
cd "/Users/matthieudollfus/Documents/Master 2/MLOps/emmaloou-ML_Ops"
source venv/bin/activate
python --version
# Doit afficher : Python 3.12.x
```

### Test 2 : Vérifier PyTorch
```bash
source venv/bin/activate
python -c "import torch; print('PyTorch:', torch.__version__)"
# Doit afficher : PyTorch: 2.9.0
```

### Test 3 : Vérifier FastAPI
```bash
source venv/bin/activate
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
# Doit afficher : FastAPI: 0.117.1
```

### Test 4 : Vérifier MLflow
```bash
source venv/bin/activate
python -c "import mlflow; print('MLflow:', mlflow.__version__)"
# Doit afficher : MLflow: 3.5.1
```

---

## 🚀 Prochaine Étape

Vous êtes maintenant prêt pour **ÉTAPE 2** : Corriger et améliorer les scripts !

**On continue ?** On va maintenant :
1. Corriger `model_train.py` pour ajouter validation et sauvegarde
2. Améliorer `data_preparation.py` si nécessaire
3. Tester les scripts

Prenez votre temps pour tester, on avance quand vous êtes prêt ! 🎯

