# 🎯 Résumé Rapide - Projet MLOps

## 📌 Objectif
Classifier des images : **Dandelion** vs **Grass**

## 🏗️ Architecture à Implémenter

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   Airflow   │────▶│   S3/    │────▶│  DL      │────▶│ MLflow   │
│  (Orchestre)│     │  MinIO   │     │  Model   │     │ (Track)  │
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
                                                             │
                                                             ▼
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   WebApp    │────▶│   API    │────▶│    S3    │     │ Monitoring│
│  (Frontend) │     │ (Backend)│     │ (Models) │     │ (Metrics) │
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
                            ▲
                            │
                     ┌──────────────┐
                     │ Kubernetes   │
                     │ (Orchestré) │
                     └──────────────┘
```

## ⏱️ Timeline (27 jours)

| Phase | Durée | Activités Clés |
|-------|-------|----------------|
| **1-2** | Jours 1-4 | Setup projet + Ingestion données |
| **3-4** | Jours 5-9 | Entraînement modèle + MLflow |
| **5-6** | Jours 10-13 | API + WebApp |
| **7-8** | Jours 14-18 | Dockerisation + K8s |
| **9-10** | Jours 19-22 | Monitoring + CI/CD |
| **11-12** | Jours 23-27 | Feature Store + Documentation |

## 🛠️ Technologies Clés

- **Orchestration** : Apache Airflow, Kubernetes
- **ML** : TensorFlow/Keras, MLflow
- **Storage** : S3/MinIO
- **API** : FastAPI
- **Frontend** : Streamlit ou Flask
- **Monitoring** : Prometheus + Grafana
- **CI/CD** : GitHub Actions/GitLab CI
- **Containerization** : Docker

## 📋 Livrables Attendus

1. ✅ Pipeline Airflow complet
2. ✅ Modèle entraîné (accuracy > 90%)
3. ✅ API REST fonctionnelle
4. ✅ Interface WebApp
5. ✅ Déploiement K8s
6. ✅ Monitoring opérationnel
7. ✅ CI/CD automatisé
8. ✅ Documentation complète

## 📁 Structure Projet Recommandée

```
mlops-project/
├── dags/              # DAGs Airflow
├── scripts/           # Scripts Python
├── config/            # Configurations
├── docker/            # Dockerfiles
├── kubernetes/        # Manifests K8s
├── monitoring/        # Config monitoring
├── tests/             # Tests
├── docs/              # Documentation
└── data/              # Dataset (gitignored)
```

## 🚀 Prochaines Étapes Immediates

1. **Jour 1** : Setup structure projet
2. **Jour 2** : Récupérer le dataset du repo de référence
3. **Jour 3** : Configurer Airflow localement
4. **Jour 4** : Créer le premier DAG d'ingestion

## 📖 Document Complet

Pour plus de détails, consultez : **`ROADMAP_MLOps_PROJECT.md`**

---
*Good luck! 🍀*

