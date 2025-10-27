import boto3
from botocore.client import Config

def upload_to_minio(local_path, bucket_name, target_path, 
                   endpoint_url, access_key, secret_key):
    """
    Upload un fichier vers MinIO (compatible S3)
    
    Args:
        local_path: Chemin local du fichier à uploader
        bucket_name: Nom du bucket MinIO
        target_path: Chemin cible dans le bucket
        endpoint_url: URL du serveur MinIO (ex: http://localhost:9000)
        access_key: Clé d'accès MinIO
        secret_key: Clé secrète MinIO
    """
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      config=Config(signature_version='s3v4'))
    
    try:
        s3.upload_file(local_path, bucket_name, target_path)
        print(f"✅ Upload réussi vers MinIO : {endpoint_url}/{bucket_name}/{target_path}")
    except Exception as e:
        print(f"❌ Erreur lors de l'upload : {e}")


def download_from_minio(bucket_name, object_path, local_path,
                       endpoint_url, access_key, secret_key):
    """
    Télécharge un fichier depuis MinIO
    
    Args:
        bucket_name: Nom du bucket MinIO
        object_path: Chemin de l'objet dans le bucket
        local_path: Chemin local où sauvegarder le fichier
        endpoint_url: URL du serveur MinIO
        access_key: Clé d'accès MinIO
        secret_key: Clé secrète MinIO
    """
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      config=Config(signature_version='s3v4'))
    
    try:
        s3.download_file(bucket_name, object_path, local_path)
        print(f"✅ Download réussi depuis MinIO : {object_path}")
    except Exception as e:
        print(f"❌ Erreur lors du download : {e}")


if __name__ == "__main__":
    # Exemple d'utilisation
    upload_to_minio(
        local_path="models/stage-1.pth",
        bucket_name="mlops-models",
        target_path="models/stage-1.pth",
        endpoint_url="http://localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin"
    )

