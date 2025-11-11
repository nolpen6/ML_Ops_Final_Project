# api.py
from torchvision import transforms
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import torch
import os
import uuid
import psycopg2
from datetime import datetime
import boto3
from botocore.client import Config
from scripts.model_train import SimpleCNN

app = FastAPI()

# Configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_PATH = "models/best_model_epoch_3.pth"

# Configuration PostgreSQL
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5433"),
    "user": os.getenv("POSTGRES_USER", "airflow"),
    "password": os.getenv("POSTGRES_PASSWORD", "airflow"),
    "database": os.getenv("POSTGRES_DB", "mlops")
}

# Configuration MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_PREDICTIONS_BUCKET = "mlops-predictions"

def init_database():
    """Initialise la table predictions dans PostgreSQL"""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                prediction_id VARCHAR(255) UNIQUE NOT NULL,
                filename VARCHAR(255) NOT NULL,
                prediction VARCHAR(50) NOT NULL,
                confidence DECIMAL(5, 2) NOT NULL,
                minio_path VARCHAR(500) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_predictions_prediction_id 
            ON predictions(prediction_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_predictions_created_at 
            ON predictions(created_at);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Base de données initialisée")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation de la base de données : {e}")

def ensure_minio_bucket():
    """Crée le bucket MinIO pour les prédictions s'il n'existe pas"""
    try:
        s3 = boto3.client('s3',
                         endpoint_url=MINIO_ENDPOINT,
                         aws_access_key_id=MINIO_ACCESS_KEY,
                         aws_secret_access_key=MINIO_SECRET_KEY,
                         config=Config(signature_version='s3v4'))
        
        try:
            s3.head_bucket(Bucket=MINIO_PREDICTIONS_BUCKET)
            print(f"✅ Bucket '{MINIO_PREDICTIONS_BUCKET}' existe déjà")
        except:
            s3.create_bucket(Bucket=MINIO_PREDICTIONS_BUCKET)
            print(f"✅ Bucket '{MINIO_PREDICTIONS_BUCKET}' créé")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation de MinIO : {e}")

# Initialiser la base de données et MinIO de manière asynchrone (non bloquant)
# L'initialisation se fera au premier appel à /predict/
_db_initialized = False
_minio_initialized = False

def ensure_initialized():
    """Initialise la base de données et MinIO si ce n'est pas déjà fait"""
    global _db_initialized, _minio_initialized
    
    if not _db_initialized:
        try:
            init_database()
            _db_initialized = True
        except Exception as e:
            print(f"⚠️ Erreur lors de l'initialisation de la base de données : {e}")
    
    if not _minio_initialized:
        try:
            ensure_minio_bucket()
            _minio_initialized = True
        except Exception as e:
            print(f"⚠️ Erreur lors de l'initialisation de MinIO : {e}")

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

@app.get("/predictions/")
async def get_predictions(limit: int = 10):
    """
    Récupère les dernières prédictions depuis PostgreSQL
    
    Args:
        limit: Nombre de prédictions à récupérer (défaut: 10)
        
    Returns:
        list: Liste des prédictions
    """
    # Initialiser la base de données si nécessaire
    ensure_initialized()
    
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT prediction_id, filename, prediction, confidence, minio_path, created_at
            FROM predictions
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        predictions = []
        for row in results:
            predictions.append({
                "prediction_id": row[0],
                "filename": row[1],
                "prediction": row[2],
                "confidence": f"{row[3]:.2f}%",
                "minio_path": row[4],
                "created_at": row[5].isoformat() if row[5] else None
            })
        
        return {"predictions": predictions, "count": len(predictions)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des prédictions : {str(e)}")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Prédit si une image est dandelion ou grass et stocke le résultat
    
    Args:
        file: Fichier image à uploader
        
    Returns:
        dict: {"prediction": "dandelion" ou "grass", "confidence": "XX.XX%", "prediction_id": "uuid"}
    """
    # Initialiser la base de données et MinIO si nécessaire
    ensure_initialized()
    
    prediction_id = str(uuid.uuid4())
    
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
        
        # Sauvegarder l'image dans MinIO
        filename = file.filename or f"prediction_{prediction_id}.jpg"
        file_extension = os.path.splitext(filename)[1] or ".jpg"
        minio_path = f"{prediction_id}{file_extension}"
        
        try:
            # Sauvegarder temporairement l'image
            # Utiliser tempfile pour un chemin compatible cross-platform
            import tempfile
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"{prediction_id}{file_extension}")
            
            image.save(temp_path, "JPEG")
            print(f"📁 Image temporaire sauvegardée : {temp_path}")
            
            # Upload vers MinIO
            s3 = boto3.client('s3',
                             endpoint_url=MINIO_ENDPOINT,
                             aws_access_key_id=MINIO_ACCESS_KEY,
                             aws_secret_access_key=MINIO_SECRET_KEY,
                             config=Config(signature_version='s3v4'))
            
            print(f"📤 Upload vers MinIO : {MINIO_PREDICTIONS_BUCKET}/{minio_path}")
            s3.upload_file(temp_path, MINIO_PREDICTIONS_BUCKET, minio_path)
            
            # Vérifier que l'upload a réussi
            try:
                s3.head_object(Bucket=MINIO_PREDICTIONS_BUCKET, Key=minio_path)
                print(f"✅ Image sauvegardée et vérifiée dans MinIO : {MINIO_PREDICTIONS_BUCKET}/{minio_path}")
            except Exception as verify_error:
                print(f"⚠️ Upload réussi mais vérification échouée : {verify_error}")
            
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"🗑️ Fichier temporaire supprimé : {temp_path}")
        except Exception as e:
            import traceback
            error_msg = f"⚠️ Erreur lors de la sauvegarde dans MinIO : {e}"
            print(error_msg)
            traceback.print_exc()
            # Continuer même si MinIO échoue, mais on log l'erreur complète
        
        # Sauvegarder les métadonnées dans PostgreSQL
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO predictions (prediction_id, filename, prediction, confidence, minio_path)
                VALUES (%s, %s, %s, %s, %s)
            """, (prediction_id, filename, label, round(confidence, 2), minio_path))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Métadonnées sauvegardées dans PostgreSQL : {prediction_id}")
        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde dans PostgreSQL : {e}")
            # Continuer même si PostgreSQL échoue
        
        return {
            "prediction": label,
            "confidence": f"{confidence:.2f}%",
            "prediction_id": prediction_id,
            "minio_path": f"{MINIO_PREDICTIONS_BUCKET}/{minio_path}"
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
