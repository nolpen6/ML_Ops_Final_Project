from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.error import S3Error
import uvicorn
from PIL import Image
import io
import numpy as np
from datetime import datetime
import uuid
from pydantic import BaseModel

# Modèle de réponse
class AnalysisResponse(BaseModel):
    is_grass: bool
    confidence: float
    minio_url: str
    filename: str
    timestamp: str

# Initialisation de FastAPI
app = FastAPI(
    title="API de détection de gazon",
    description="API pour détecter si une image contient du gazon approprié pour un pique-nique",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration MinIO
MINIO_ENDPOINT = "localhost:9000"  # Adresse de votre serveur MinIO
MINIO_ACCESS_KEY = "minioadmin"     # Clé d'accès par défaut
MINIO_SECRET_KEY = "minioadmin"     # Clé secrète par défaut
MINIO_BUCKET = "grass-images"       # Nom du bucket
MINIO_SECURE = False                # False pour HTTP, True pour HTTPS

# Initialisation du client MinIO
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)

# Créer le bucket s'il n'existe pas
def ensure_bucket_exists():
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)
            print(f"✅ Bucket '{MINIO_BUCKET}' créé avec succès")
        else:
            print(f"✅ Bucket '{MINIO_BUCKET}' existe déjà")
    except S3Error as e:
        print(f"❌ Erreur lors de la création du bucket: {e}")

# Fonction de détection de gazon (simplifiée)
def detect_grass(image: Image.Image) -> tuple[bool, float]:
    """
    Détecte si l'image contient du gazon.
    Retourne (is_grass, confidence)
    
    Cette version est simplifiée et se base sur l'analyse des couleurs.
    Pour une vraie application, utilisez un modèle de ML comme YOLO ou ResNet.
    """
    # Convertir en RGB si nécessaire
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Redimensionner pour accélérer le traitement
    image_small = image.resize((100, 100))
    
    # Convertir en array numpy
    img_array = np.array(image_small)
    
    # Extraire les canaux RGB
    red = img_array[:, :, 0]
    green = img_array[:, :, 1]
    blue = img_array[:, :, 2]
    
    # Calculer les moyennes
    mean_red = np.mean(red)
    mean_green = np.mean(green)
    mean_blue = np.mean(blue)
    
    # Logique de détection : le vert doit être dominant
    # et supérieur au rouge et au bleu
    green_dominant = (mean_green > mean_red) and (mean_green > mean_blue)
    
    # Calculer un score de "verdure"
    green_ratio = mean_green / (mean_red + mean_green + mean_blue + 1e-5)
    
    # Conditions pour du gazon :
    # 1. Le vert doit être dominant
    # 2. Le ratio de vert doit être > 0.38 (environ 38% de vert)
    # 3. La luminosité ne doit pas être trop faible (> 30) ni trop élevée (< 220)
    brightness = (mean_red + mean_green + mean_blue) / 3
    
    is_grass = (
        green_dominant and 
        green_ratio > 0.38 and 
        30 < brightness < 220
    )
    
    # Calculer la confiance (0-100%)
    if is_grass:
        confidence = min(95, green_ratio * 200)  # Max 95%
    else:
        confidence = max(5, (1 - green_ratio) * 100)  # Min 5%
    
    return is_grass, round(confidence, 2)

# Fonction pour uploader sur MinIO
def upload_to_minio(file_data: bytes, filename: str) -> str:
    """
    Upload un fichier sur MinIO et retourne l'URL
    """
    try:
        # Générer un nom unique
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{filename}"
        
        # Upload sur MinIO
        minio_client.put_object(
            MINIO_BUCKET,
            unique_filename,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type="image/jpeg"
        )
        
        # Construire l'URL
        url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{unique_filename}"
        return url
        
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur MinIO: {str(e)}")

# Endpoint racine
@app.get("/")
async def root():
    return {
        "message": "API de détection de gazon pour pique-nique",
        "version": "1.0.0",
        "endpoints": {
            "/analyze-image": "POST - Analyser une image",
            "/health": "GET - Vérifier l'état de l'API"
        }
    }

# Endpoint de santé
@app.get("/health")
async def health_check():
    try:
        # Vérifier la connexion à MinIO
        minio_client.bucket_exists(MINIO_BUCKET)
        minio_status = "OK"
    except:
        minio_status = "ERROR"
    
    return {
        "status": "healthy",
        "minio": minio_status,
        "timestamp": datetime.now().isoformat()
    }

# Endpoint principal d'analyse
@app.post("/analyze-image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyse une image pour détecter si elle contient du gazon.
    Upload l'image sur MinIO et retourne le résultat.
    """
    # Vérifier le type de fichier
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Format de fichier non supporté. Utilisez JPEG ou PNG."
        )
    
    try:
        # Lire le contenu du fichier
        file_data = await file.read()
        
        # Ouvrir l'image avec PIL
        image = Image.open(io.BytesIO(file_data))
        
        # Détecter le gazon
        is_grass, confidence = detect_grass(image)
        
        # Upload sur MinIO
        minio_url = upload_to_minio(file_data, file.filename)
        
        # Retourner le résultat
        return AnalysisResponse(
            is_grass=is_grass,
            confidence=confidence,
            minio_url=minio_url,
            filename=file.filename,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

# Événement au démarrage
@app.on_event("startup")
async def startup_event():
    print("Démarrage de l'API...")
    ensure_bucket_exists()
    print("API prête à recevoir des requêtes sur http://localhost:8000")

# Point d'entrée pour lancer l'application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )