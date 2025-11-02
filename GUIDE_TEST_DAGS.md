# 📚 Guide Pas-à-Pas : Tester vos DAGs Airflow

## 🎯 Objectif

Tester votre pipeline MLOps automatisé via Airflow. Chaque action a une signification importante dans votre architecture MLOps.

---

## 🚀 Étape 1 : Ouvrir l'interface Airflow

**Action :** Ouvrez http://localhost:8080 dans votre navigateur

**Ce que vous voyez :** La page "DAGs" avec la liste de vos 2 DAGs

**Signification dans votre projet :**
- C'est l'interface de contrôle de votre orchestration MLOps
- Vous pouvez surveiller et contrôler tous vos pipelines automatisés
- C'est l'équivalent d'un tableau de bord pour vos workflows ML

**Dans l'architecture MLOps :**
```
Utilisateur → Interface Airflow → Scheduler → Exécution des tâches → Services (MinIO, MLflow)
```

---

## 📊 Étape 2 : Comprendre l'état actuel

**Action :** Regardez l'état de vos DAGs

**Ce que vous voyez probablement :**
- `data_ingestion` : Interrupteur OFF (gris) → Statut "Paused"
- `training` : Interrupteur OFF (gris) → Statut "Paused"
- Compteurs : "Paused 2" (2 DAGs en pause)

**Signification dans votre projet :**

### 🔴 DAG en Pause (Paused) :
- **Signification technique :** Le DAG existe mais ne sera **pas exécuté automatiquement**
- **Impact MLOps :** Aucun run automatique ne sera déclenché selon le schedule
- **Pourquoi c'est important :** C'est une sécurité - vous contrôlez quand les pipelines s'exécutent

### 📅 Schedule visible :
- `data_ingestion` : "1 day, 0:00:00" → Devrait s'exécuter tous les jours
- `training` : "7 days, 0:00:00" → Devrait s'exécuter toutes les semaines
- **En pause** → Ces schedules sont ignorés

**Dans votre workflow MLOps :**
```
En production, ces DAGs s'exécuteraient automatiquement :
- data_ingestion : Chaque jour → Nouvelles images → MinIO
- training : Chaque semaine → Nouveau modèle → MLflow
```

---

## ✅ Étape 3 : Activer un DAG (Activer l'automatisation)

**Action :** Cliquez sur l'interrupteur OFF de `data_ingestion` pour le mettre en ON (vert)

**Ce qui va se passer :**
- L'interrupteur passe de gris (OFF) à vert (ON)
- Le statut passe de "Paused" à "Active"
- Le compteur "Paused" diminue, "Active" augmente

**Signification dans votre projet MLOps :**

### 🟢 DAG Active (ON) :
- **Signification technique :** Le DAG va maintenant respecter son **schedule automatique**
- **Impact MLOps :** 
  - Si le schedule est "1 day" → Le DAG s'exécutera automatiquement tous les jours
  - En production, c'est ainsi que vous automatisez vos pipelines
- **Pourquoi commencer par data_ingestion :**
  - Plus simple (juste upload d'images)
  - Plus rapide (quelques secondes)
  - Moins de dépendances (pas besoin de PyTorch)

**Dans votre architecture :**
```
DAG Active = Pipeline automatisé prêt à s'exécuter selon le schedule
```

**Ce que cela signifie pour votre projet :**
- ✅ Vous activez l'automatisation du pipeline d'ingestion de données
- ✅ Les nouvelles images dans `data/` seraient automatiquement uploadées vers MinIO
- ✅ C'est la base de votre pipeline MLOps automatisé

---

## ▶️ Étape 4 : Déclencher manuellement un DAG (Test)

**Action :** Cliquez sur le bouton ▶️ (Play/Trigger) à droite de `data_ingestion`

**Ce qui va se passer :**
1. Une popup s'ouvre pour confirmer
2. Vous pouvez choisir une date d'exécution (par défaut : aujourd'hui)
3. Le DAG passe en "Running"

**Signification dans votre projet MLOps :**

### 🔵 DAG Running :
- **Signification technique :** Un **run** (exécution) du DAG a été créé et est en cours
- **Impact MLOps :**
  - Le scheduler va exécuter les tâches dans l'ordre défini
  - Pour `data_ingestion` : `scan_images` → puis `upload_to_minio`

**Pourquoi déclencher manuellement :**
- **Test :** Vérifier que tout fonctionne avant d'activer l'automatisation
- **Debug :** Déclencher à la demande pour tester des corrections
- **Production :** Exécutions manuelles pour des cas spéciaux (retry, réentraînement urgent, etc.)

**Ce qui se passe dans votre architecture :**
```
Clic sur ▶️ → Création d'un "DAG Run" → Scheduler → Exécution des tâches → Logs
```

**Dans votre workflow :**
```
1. DAG Run créé avec une date d'exécution (ex: 2025-11-02)
2. Scheduler analyse le DAG Run
3. Exécute les tâches dans l'ordre :
   - scan_images : Compte les images dans data/
   - upload_to_minio : Upload 10 images vers MinIO
4. Résultat visible dans les logs
```

---

## 📈 Étape 5 : Suivre l'exécution (Monitoring)

**Action :** Cliquez sur le nom `data_ingestion` pour voir les détails

**Ce que vous allez voir :**

### Vue "Graph" (par défaut) :
- 2 tâches connectées : `scan_images` → `upload_to_minio`
- Cercles colorés :
  - ⚪ Gris/Blanc : Pas encore exécuté
  - 🔵 Bleu : En cours d'exécution
  - 🟢 Vert : Réussi (success)
  - 🔴 Rouge : Échoué (failed)

**Signification dans votre projet MLOps :**

### État des tâches :
- **Succès (vert) :** ✅ La tâche a réussi
  - Pour `scan_images` : Les images ont été comptées avec succès
  - Pour `upload_to_minio` : Les images ont été uploadées vers MinIO
  
- **Échec (rouge) :** ❌ La tâche a échoué
  - Probable cause : Module Python manquant (boto3, etc.)
  - Action : Vérifier les logs pour identifier l'erreur

**Pourquoi suivre l'exécution :**
- **Monitoring :** Voir en temps réel l'état de votre pipeline
- **Debugging :** Identifier où ça bloque si ça échoue
- **Production :** Surveiller l'état de santé de vos pipelines automatisés

**Dans votre workflow MLOps :**
```
Monitoring = Surveillance de l'état de santé de vos pipelines
C'est crucial en production pour détecter les problèmes rapidement
```

---

## 📝 Étape 6 : Voir les logs (Debugging)

**Action :** 
1. Cliquez sur une tâche (ex: `scan_images`)
2. Cliquez sur l'icône "Log" en bas

**Ce que vous allez voir :**
- Logs détaillés de l'exécution de la tâche
- Messages de print Python
- Erreurs éventuelles

**Signification dans votre projet MLOps :**

### Logs des tâches :
- **Succès :** Vous verrez les messages de vos fonctions :
  ```
  ✅ Images grass : 200
  ✅ Images dandelion : 200
  ✅ Total : 400 images
  ```
- **Échec :** Vous verrez les erreurs :
  ```
  ModuleNotFoundError: No module named 'boto3'
  ```

**Pourquoi les logs sont importants :**
- **Debugging :** Comprendre pourquoi une tâche a échoué
- **Monitoring :** Vérifier que tout s'est bien passé
- **Audit :** Historique de ce qui a été fait

**Dans votre workflow MLOps :**
```
Logs = Traçabilité de chaque exécution
C'est essentiel pour comprendre ce qui s'est passé et diagnostiquer les problèmes
```

---

## 🎯 Étape 7 : Interpréter les résultats

### Si tout est vert ✅ :
- **Signification :** Votre pipeline fonctionne !
- **Impact :**
  - Les images ont été uploadées vers MinIO
  - Vous pouvez vérifier dans MinIO (http://localhost:9001)
- **Prochaine étape :** Tester le DAG `training`

### Si c'est rouge 🔴 :
- **Signification :** Une erreur s'est produite
- **Actions :**
  1. Lire les logs pour identifier l'erreur
  2. Installer les dépendances manquantes si nécessaire
  3. Corriger le code si c'est un bug
  4. Redéclencher le DAG

---

## 📊 Résumé : Ce que vous avez fait et pourquoi

| Action | Signification Technique | Impact MLOps |
|--------|------------------------|--------------|
| **Activer le DAG** | Active l'automatisation selon le schedule | Pipeline prêt à s'exécuter automatiquement |
| **Déclencher manuellement** | Crée un DAG Run à la demande | Test du pipeline avant automation |
| **Suivre l'exécution** | Monitoring en temps réel | Surveillance de l'état de santé |
| **Voir les logs** | Traçabilité de l'exécution | Debugging et audit |

---

## 🔄 Dans votre architecture MLOps complète

```
┌─────────────────────────────────────────────────────────────┐
│              VOUS (Interface Airflow)                        │
│  Activez DAGs → Déclenchez → Suivez → Vérifiez résultats    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│           AIRFLOW (Orchestrateur)                            │
│  Scheduler → Exécute tâches → Logs → Statut                 │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│           TÂCHES PYTHON (Vos scripts)                        │
│  scan_images() → upload_to_minio()                          │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│           SERVICES (MinIO, MLflow)                            │
│  Stockage des données et modèles                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Points clés à retenir

1. **Activer un DAG** = Activer l'automatisation (pas l'exécution immédiate)
2. **Déclencher manuellement** = Exécuter maintenant pour tester
3. **Suivre l'exécution** = Monitoring de votre pipeline
4. **Logs** = Traçabilité et debugging

**En production :**
- Les DAGs actifs s'exécutent automatiquement selon leur schedule
- Vous surveillez via l'interface pour détecter les problèmes
- Vous pouvez déclencher manuellement pour des cas spéciaux

---

**🎉 Maintenant vous comprenez comment contrôler votre pipeline MLOps !**

Commencez par activer `data_ingestion` et suivez ces étapes. Dites-moi ce que vous voyez à chaque étape et je vous guiderai ! 🚀

