#!/bin/bash
# Script pour installer les dépendances Python nécessaires dans les containers Airflow
# Ce script peut être exécuté dans les containers Airflow pour installer PyTorch et autres dépendances

echo "📦 Installation des dépendances Python pour Airflow..."

# Installer PyTorch CPU (version légère)
pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Installer les autres dépendances
pip install --no-cache-dir \
    boto3>=1.28.0 \
    mlflow>=2.7.0 \
    pandas>=2.0.0 \
    numpy>=1.24.0 \
    Pillow>=10.0.0 \
    scikit-learn>=1.3.0 \
    requests>=2.31.0

echo "✅ Dépendances installées avec succès !"

