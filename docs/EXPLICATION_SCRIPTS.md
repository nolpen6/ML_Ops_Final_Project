# 📚 Explication Détaillée des Scripts Existant

## 📖 Table des Matières
1. [data_preparation.py](#1-data_preparationpy)
2. [model_train.py](#2-model_trainpy)
3. [api.py](#3-apipy)
4. [Outils ML Utilisés](#outils-ml-utilisés)
5. [Flux de Données](#flux-de-données)

---

## 1. `data_preparation.py` - Préparation des Données

### 🎯 Objectif
Préparer les images pour l'entraînement du modèle en :
- Chargant les images depuis les dossiers `data/grass` et `data/dandelion`
- Appliquant des transformations (redimensionnement, normalisation)
- Divisant en datasets d'entraînement et validation
- Créant des DataLoaders pour l'entraînement

### 🔧 Ce que fait le script

```python
def load_data(data_dir='data', batch_size=32):
```

#### Étape 1 : Définition des Transformations
```python
transform = transforms.Compose([
    transforms.Resize((128, 128)),          # Redimensionne à 128x128
    transforms.ToTensor(),                    # Convertit en tenseur PyTorch
    transforms.Normalize(...),               # Normalise les valeurs (ImageNet stats)
])
```

**Détails** :
- **Resize(128, 128)** : Uniformise la taille de toutes les images
- **ToTensor()** : Convertit PIL Image en tenseur PyTorch (0-1 range)
- **Normalize** : 
  - Mean : [0.485, 0.456, 0.406] = moyennes RGB d'ImageNet
  - Std : [0.229, 0.224, 0.225] = écarts-types d'ImageNet
  - Utilise les statistiques d'ImageNet pour compatibilité avec ResNet18 pré-entraîné

#### Étape 2 : Chargement du Dataset
```python
full_dataset = datasets.ImageFolder(root=data_dir, transform=transform)
```

**ImageFolder** :
- Scanne `data/grass/` et `data/dandelion/`
- Assigne automatiquement les labels :
  - `dandelion` → label 0
  - `grass` → label 1
- Applique les transformations à chaque image

#### Étape 3 : Split Train/Validation
```python
train_idx, val_idx = train_test_split(
    list(range(len(full_dataset))),
    test_size=0.2,           # 80% train, 20% validation
    stratify=full_dataset.targets  # Maintient la proportion des classes
)
```

**Stratify** : Garantit que chaque split contient la même proportion de dandelion et grass (50/50)

#### Étape 4 : Création des DataLoaders
```python
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
```

**DataLoader** :
- **Train** : `shuffle=True` (mélange les données pour chaque époque)
- **Validation** : `shuffle=False` (données fixes pour validation)
- **batch_size=32** : Traite 32 images à la fois

### 📊 Résultat
- **Train** : ~320 images (160 dandelion + 160 grass)
- **Validation** : ~80 images (40 dandelion + 40 grass)
- Prêt pour l'entraînement !

---

## 2. `model_train.py` - Entraînement du Modèle

### 🎯 Objectif
Entraîner un modèle de classification d'images avec :
- Transfer Learning (ResNet18 pré-entraîné)
- Tracking des métriques avec MLflow
- Sauvegarde du modèle

### 🔧 Ce que fait le script

#### Étape 1 : Définition de l'Architecture
```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.resnet18(pretrained=True)  # ResNet18 pré-entraîné
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)  # Couche finale
```

**Architecture** :
- **ResNet18** : Réseau profond de 18 couches pré-entraîné sur ImageNet
- **Transfer Learning** : Les premières couches gardent les features apprises
- **fc (fully connected)** : Dernière couche modifiée pour 2 classes (dandelion, grass)

#### Étape 2 : Définition de l'Entraînement
```python
criterion = nn.CrossEntropyLoss()              # Fonction de perte
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Optimiseur
```

**CrossEntropyLoss** : Parfait pour classification multi-classes
**Adam** : Optimiseur adaptatif (lr=0.001 = learning rate)

#### Étape 3 : Configuration MLflow
```python
mlflow.pytorch.autolog()
mlflow.start_run()
```

**Autolog** : Enregistre automatiquement :
- Paramètres (epochs, batch_size, lr, etc.)
- Métriques (loss, accuracy, etc.)
- Artifacts (modèle, graphes)

#### Étape 4 : Boucle d'Entraînement
```python
for epoch in range(epochs):
    model.train()                    # Mode entraînement
    for inputs, labels in train_loader:
        # Forward pass
        optimizer.zero_grad()         # Réinitialise gradients
        outputs = model(inputs)       # Prédiction
        loss = criterion(outputs, labels)  # Calcul de la perte
        
        # Backward pass
        loss.backward()               # Propagation arrière
        optimizer.step()               # Mise à jour des poids
```

**Forward Pass** : Calcule les prédictions
**Backward Pass** : Calcule les gradients et met à jour les poids

### 📈 Problèmes Identifiés
1. ❌ **Pas de validation** : Le script n'évalue jamais le modèle
2. ❌ **Pas de sauvegarde** : Le modèle n'est pas sauvegardé
3. ❌ **Pas de métriques** : Aucune métrique trackée
4. ❌ **Pas de GPU detection** : Nécessite un modèle entraîné en externe

---

## 3. `api.py` - API REST pour Prédictions

### 🎯 Objectif
Servir le modèle entraîné via une API REST pour faire des prédictions en temps réel

### 🔧 Ce que fait le script

#### Étape 1 : Chargement du Modèle
```python
model = SimpleCNN()
model.load_state_dict(torch.load("models/stage-1.pth", map_location=device))
model.eval()  # Mode évaluation (pas de dropout, etc.)
```

**Problème** : Le modèle doit être entraîné au préalable !

#### Étape 2 : Définition de l'Endpoint
```python
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
```

**FastAPI** : Framework web moderne et rapide
- `/predict/` : Endpoint POST pour recevoir les images
- **UploadFile** : Accepte upload d'image

#### Étape 3 : Transformation de l'Image
```python
image = Image.open(io.BytesIO(image_data)).convert('RGB')
transform = transforms.Compose([...])  # Même transformation qu'à l'entraînement
```

**Important** : Utilise les **MÊMES transformations** que l'entraînement !

#### Étape 4 : Prédiction
```python
output = model(input_tensor)
prediction = torch.argmax(output, 1).item()  # Classe prédite (0 ou 1)
label = "dandelion" if prediction == 0 else "grass"
```

### 🎯 Résultat
- API REST accessible sur `http://localhost:8000`
- Endpoint `/predict/` retourne `{"prediction": "dandelion"}` ou `{"prediction": "grass"}`

---

## 🛠️ Outils ML Utilisés

### 📚 PyTorch / Torchvision
- **PyTorch** : Framework de deep learning
- **torchvision** : Bibliothèque pour traitement d'images
  - `datasets.ImageFolder` : Charge automatiquement les images
  - `transforms` : Transformations d'images
  - `models.resnet18` : Architecture ResNet18

### 🤖 Transfer Learning
- **ResNet18** : Réseau de 18 couches
- **Pré-entraîné sur ImageNet** : 1.2M d'images, 1000 classes
- **Fine-tuning** : Dernière couche adaptée pour 2 classes

### 📊 SciKit-Learn
- `train_test_split` : Division train/validation

### 📈 MLflow
- **Tracking** : Logs des métriques et paramètres
- **Experiments** : Organisation des runs
- **Model Registry** : Versioning des modèles

### 🌐 FastAPI
- Framework web moderne pour API REST
- Asynchrone et rapide

---

## 🔄 Flux de Données

```
┌─────────────────────────────────────────────────────────┐
│  1. DATA_PREPARATION.PY                                 │
│  ─────────────────────────────────────────────────────  │
│  Images (data/grass, data/dandelion)                    │
│  ↓                                                       │
│  transformations (resize, normalize)                     │
│  ↓                                                       │
│  Split 80/20 (train/validation)                         │
│  ↓                                                       │
│  DataLoaders (batches de 32)                            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. MODEL_TRAIN.PY                                      │
│  ─────────────────────────────────────────────────────  │
│  ResNet18 (pré-entraîné)                                │
│  ↓                                                       │
│  Entraînement sur train_loader                           │
│  ↓                                                       │
│  Tracking avec MLflow                                   │
│  ↓                                                       │
│  Modèle entraîné → models/stage-1.pth                  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. API.PY                                              │
│  ─────────────────────────────────────────────────────  │
│  Charge models/stage-1.pth                              │
│  ↓                                                       │
│  Attend requêtes POST /predict/                         │
│  ↓                                                       │
│  Transforme l'image (même que training)                    │
│  ↓                                                       │
│  Prédiction → "dandelion" ou "grass"                    │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ Problèmes à Corriger

### 1. model_train.py
- ❌ Pas de validation pendant l'entraînement
- ❌ Pas de sauvegarde du modèle
- ❌ Pas de métriques calculées
- ❌ Pas de support pour train/validation

### 2. api.py
- ❌ Nécessite un modèle déjà entraîné
- ❌ Pas de gestion d'erreurs
- ❌ Pas de vérification du fichier modèle

### 3. Général
- ❌ Pas de gestion des chemins relatifs
- ❌ Pas de gestion des erreurs
- ❌ Pas de logging

---

## 🎯 Ce qu'il Faudra Ajouter

Pour compléter le pipeline MLOps :
1. ✅ Data preparation (existe)
2. ❌ Entraînement avec validation (à améliorer)
3. ❌ Sauvegarde du modèle
4. ❌ Upload vers MinIO
5. ❌ DAGs Airflow pour orchestrer
6. ❌ Dockerisation
7. ❌ Kubernetes
8. ❌ Monitoring

---

**Prochaine étape** : Corriger et compléter ces scripts dans l'ordre logique !

