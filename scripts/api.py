# api.py
from torchvision import transforms
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import torch
import os
from model_train import SimpleCNN

app = FastAPI()

# Configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_PATH = "models/best_model_epoch_3.pth"

# Charger le modèle au démarrage
print("🚀 Chargement du modèle...")
try:
    model = SimpleCNN()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
    print(f"✅ Modèle chargé depuis {MODEL_PATH}")
except FileNotFoundError:
    print(f"❌ Erreur : Le fichier {MODEL_PATH} n'existe pas")
    print("   💡 Vous devez d'abord entraîner le modèle avec : python scripts/model_train.py")
    raise
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")
    raise

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Dandelion vs Grass Classifier API",
        "status": "ready",
        "model": MODEL_PATH,
        "device": str(device)
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Prédit si une image est dandelion ou grass
    
    Args:
        file: Fichier image à uploader
        
    Returns:
        dict: {"prediction": "dandelion" ou "grass"}
    """
    try:
        # Lire l'image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Transformer l'image (même transformations qu'à l'entraînement)
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
        ])
        
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # Faire la prédiction
        with torch.no_grad():
            output = model(input_tensor)
            probability = torch.nn.functional.softmax(output, dim=1)
            confidence = torch.max(probability).item() * 100
            prediction = torch.argmax(output, 1).item()
        
        label = "dandelion" if prediction == 0 else "grass"
        
        return {
            "prediction": label,
            "confidence": f"{confidence:.2f}%"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du traitement de l'image : {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("🌿 API Dandelion vs Grass Classifier")
    print("=" * 60)
    print(f"📍 Modèle : {MODEL_PATH}")
    print(f"🔧 Device : {device}")
    print("=" * 60 + "\n")
    print("🚀 Démarrage du serveur...")
    print("📡 API accessible sur : http://localhost:8000")
    print("📖 Documentation : http://localhost:8000/docs")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
