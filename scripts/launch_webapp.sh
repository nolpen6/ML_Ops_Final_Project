#!/bin/bash
# Script pour lancer la WebApp

echo "🌿 Lancement de la WebApp - Dandelion vs Grass Classifier"
echo "=================================================="

# Activer l'environnement virtuel
source ../venv/bin/activate

# Installer streamlit si nécessaire
pip install streamlit requests -q

# Lancer la WebApp
cd "$(dirname "$0")"
streamlit run webapp.py --server.port=8501

