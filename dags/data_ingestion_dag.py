"""
DAG Airflow : Data Ingestion
Scanne les images locales et les upload vers MinIO
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# Définition du DAG
default_args = {
    'owner': 'MLOps Team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_ingestion',
    default_args=default_args,
    description='Ingestion des données vers MinIO',
    schedule_interval=timedelta(days=1),  # Exécution quotidienne
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['mlops', 'data'],
)


def scan_images():
    """Scan le dossier data/ pour compter les images"""
    import glob
    
    grass_images = glob.glob('data/grass/*.jpg')
    dandelion_images = glob.glob('data/dandelion/*.jpg')
    
    print(f"✅ Images grass : {len(grass_images)}")
    print(f"✅ Images dandelion : {len(dandelion_images)}")
    print(f"✅ Total : {len(grass_images) + len(dandelion_images)} images")
    
    return len(grass_images) + len(dandelion_images)


def upload_to_minio():
    """Upload des images vers MinIO"""
    from scripts.upload_to_minio import upload_file_to_minio
    import glob
    import os
    
    ENDPOINT_URL = "http://localhost:9000"
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "mlops-data"
    
    # Créer le bucket
    from scripts.upload_model_to_minio import ensure_bucket_exists
    ensure_bucket_exists(BUCKET_NAME, ENDPOINT_URL, ACCESS_KEY, SECRET_KEY)
    
    # Upload images grass
    grass_images = glob.glob('data/grass/*.jpg')[:10]  # Limiter à 10 pour test
    for img_path in grass_images:
        filename = os.path.basename(img_path)
        upload_file_to_minio(
            img_path, BUCKET_NAME, f"grass/{filename}",
            ENDPOINT_URL, ACCESS_KEY, SECRET_KEY
        )
    
    # Upload images dandelion
    dandelion_images = glob.glob('data/dandelion/*.jpg')[:10]  # Limiter à 10 pour test
    for img_path in dandelion_images:
        filename = os.path.basename(img_path)
        upload_file_to_minio(
            img_path, BUCKET_NAME, f"dandelion/{filename}",
            ENDPOINT_URL, ACCESS_KEY, SECRET_KEY
        )
    
    print("✅ Upload vers MinIO terminé")


# Tâches du DAG
scan_task = PythonOperator(
    task_id='scan_images',
    python_callable=scan_images,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_to_minio',
    python_callable=upload_to_minio,
    dag=dag,
)

# Définir l'ordre d'exécution
scan_task >> upload_task

