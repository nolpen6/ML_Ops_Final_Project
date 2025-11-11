"""
Script pour créer le bucket mlops-predictions dans MinIO
"""
import boto3
from botocore.client import Config

# Configuration MinIO
ENDPOINT_URL = "http://localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "mlops-predictions"

def create_predictions_bucket():
    """Crée le bucket mlops-predictions dans MinIO"""
    try:
        s3 = boto3.client('s3',
                         endpoint_url=ENDPOINT_URL,
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         config=Config(signature_version='s3v4'))
        
        # Vérifier si le bucket existe déjà
        try:
            s3.head_bucket(Bucket=BUCKET_NAME)
            print(f"✅ Bucket '{BUCKET_NAME}' existe déjà")
            return True
        except:
            # Le bucket n'existe pas, le créer
            try:
                s3.create_bucket(Bucket=BUCKET_NAME)
                print(f"✅ Bucket '{BUCKET_NAME}' créé avec succès")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de la création du bucket : {e}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur de connexion à MinIO : {e}")
        print(f"   Vérifiez que MinIO est accessible sur {ENDPOINT_URL}")
        return False

if __name__ == "__main__":
    print("🔧 Création du bucket mlops-predictions dans MinIO...")
    create_predictions_bucket()

