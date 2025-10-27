"""
WebApp Streamlit - Classification Dandelion vs Grass
"""
import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import requests
import os

st.set_page_config(
    page_title="🌿 Dandelion vs Grass Classifier",
    page_icon="🌿",
    layout="wide"
)

# Configuration
st.title("🌿 Dandelion vs Grass Classifier")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload d'image")
    uploaded_file = st.file_uploader(
        "Choisissez une image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload une image de pissenlit ou d'herbe"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image uploadée", use_container_width=True)

with col2:
    st.header("🎯 Résultat")
    
    if uploaded_file is not None:
        # Tester avec l'API locale
        try:
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'image/jpeg')}
            
            with st.spinner("⏳ Analyse en cours..."):
                response = requests.post("http://localhost:8000/predict/", files=files)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction']
                confidence = result['confidence']
                
                st.success(f"✅ Prédiction : **{prediction}**")
                st.info(f"📊 Confiance : **{confidence}**")
                
                # Visualisation
                if prediction == "dandelion":
                    st.balloons()
                    st.markdown("### 🌼 C'est un pissenlit !")
                else:
                    st.markdown("### 🌱 C'est de l'herbe !")
            else:
                st.error("❌ Erreur lors de la prédiction")
                st.text(response.text)
                
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
            st.info("💡 Assurez-vous que l'API est lancée sur http://localhost:8000")
    else:
        st.info("👆 Upload une image pour obtenir une prédiction")

# Informations
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Modèle", "ResNet18")
    
with col2:
    st.metric("🎯 Accuracy", "83.33%")

with col3:
    st.metric("📦 Classes", "2")

st.markdown("---")
st.markdown("### ℹ️ À propos")
st.markdown("""
Cette application utilise un modèle de deep learning entraîné sur :
- 200 images de pissenlits (dandelion)
- 200 images d'herbe (grass)

**Architecture** : ResNet18 avec Transfer Learning
**Framework** : PyTorch
**API** : FastAPI
**Frontend** : Streamlit
""")

# Lien API
st.sidebar.markdown("## 🔗 Links")
st.sidebar.markdown("[📡 API Documentation](http://localhost:8000/docs)")
st.sidebar.markdown("[📊 MLflow Tracking](http://localhost:5001)")
st.sidebar.markdown("[☁️ MinIO Console](http://localhost:9001)")

st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Statistiques")
st.sidebar.info("Modèle entraîné sur 400 images")

