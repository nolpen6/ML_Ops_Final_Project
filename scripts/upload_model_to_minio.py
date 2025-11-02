"""
Script pour uploader les modèles entraînés vers MinIO
"""
import boto3
from botocore.client import Config
import os

# Configuration MinIO
ENDPOINT_URL = "http://localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "mlops-models"

def ensure_bucket_exists(bucket_name, endpoint_url, access_key, secret_key):
    """Crée le bucket s'il n'existe pas"""
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      config=Config(signature_version='s3v4'))
    
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' existe déjà")
    except:
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' créé avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors de la création du bucket : {e}")
            print(f"   (Peut-être qu'il existe déjà)")


def upload_file_to_minio(local_path, bucket_name, target_path, 
                         endpoint_url, access_key, secret_key):
    """Upload un fichier vers MinIO"""
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      config=Config(signature_version='s3v4'))
    
    try:
        s3.upload_file(local_path, bucket_name, target_path)
        file_size = os.path.getsize(local_path) / (1024 * 1024)  # MB
        print(f"✅ Upload réussi : {bucket_name}/{target_path} ({file_size:.2f} MB)")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'upload : {e}")
        return False


def main():
    print("=" * 60)
    print("📦 Upload des modèles vers MinIO")
    print("=" * 60)
    
    # 1. Créer le bucket s'il n'existe pas
    ensure_bucket_exists(BUCKET_NAME, ENDPOINT_URL, ACCESS_KEY, SECRET_KEY)
    
    # 2. Uploader les modèles
    models_dir = "models"
    
    if not os.path.exists(models_dir):
        print(f"❌ Le dossier '{models_dir}' n'existe pas")
        return
    
    models_to_upload = [
        "best_model_epoch_3.pth",  # Le meilleur
        "final_model.pth"          # Le final
    ]
    
    success_count = 0
    for model_file in models_to_upload:
        model_path = os.path.join(models_dir, model_file)
        if os.path.exists(model_path):
            print(f"\n📤 Upload de {model_file}...")
            if upload_file_to_minio(
                local_path=model_path,
                bucket_name=BUCKET_NAME,
                target_path=f"models/{model_file}",
                endpoint_url=ENDPOINT_URL,
                access_key=ACCESS_KEY,
                secret_key=SECRET_KEY
            ):
                success_count += 1
        else:
            print(f"⚠️ Fichier non trouvé : {model_path}")
    
    print("\n" + "=" * 60)
    print(f"✅ Upload terminé : {success_count}/{len(models_to_upload)} fichiers")
    print("=" * 60)
    print(f"\n🌐 Vérifiez sur MinIO Console : http://localhost:9001")
    print(f"   Bucket : {BUCKET_NAME}")


if __name__ == "__main__":
    main()

