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
    
    # Essayer plusieurs chemins possibles (local ou Docker)
    possible_data_dirs = [
        "data",
        "/opt/airflow/data",
        "./data"
    ]
    
    data_dir = None
    for dir_path in possible_data_dirs:
        if os.path.exists(dir_path):
            data_dir = dir_path
            break
    
    if not data_dir:
        print("⚠️ Dossier data/ non trouvé dans aucun des chemins suivants:")
        for dir_path in possible_data_dirs:
            print(f"   - {dir_path}")
        return 0
    
    grass_images = glob.glob(f'{data_dir}/grass/*.jpg')
    dandelion_images = glob.glob(f'{data_dir}/dandelion/*.jpg')
    
    print(f"✅ Dossier trouvé : {data_dir}")
    print(f"✅ Images grass : {len(grass_images)}")
    print(f"✅ Images dandelion : {len(dandelion_images)}")
    print(f"✅ Total : {len(grass_images) + len(dandelion_images)} images")
    
    return len(grass_images) + len(dandelion_images)


def upload_to_minio():
    """Upload des images vers MinIO"""
    import sys
    import os
    
    # Ajouter le chemin des scripts au PYTHONPATH
    scripts_path = "/opt/airflow/scripts"
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    
    from upload_to_minio import upload_to_minio as upload_file_to_minio
    from upload_model_to_minio import ensure_bucket_exists
    import glob
    
    ENDPOINT_URL = "http://minio:9000"  # Utiliser le nom du service Docker
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "mlops-data"
    
    # Créer le bucket
    ensure_bucket_exists(BUCKET_NAME, ENDPOINT_URL, ACCESS_KEY, SECRET_KEY)
    
    # Trouver le dossier data
    possible_data_dirs = ["data", "/opt/airflow/data", "./data"]
    data_dir = None
    for dir_path in possible_data_dirs:
        if os.path.exists(dir_path):
            data_dir = dir_path
            break
    
    if not data_dir:
        print("⚠️ Dossier data/ non trouvé")
        return
    
    # Upload images grass
    grass_images = glob.glob(f'{data_dir}/grass/*.jpg')[:10]  # Limiter à 10 pour test
    for img_path in grass_images:
        filename = os.path.basename(img_path)
        upload_file_to_minio(
            img_path, BUCKET_NAME, f"grass/{filename}",
            ENDPOINT_URL, ACCESS_KEY, SECRET_KEY
        )
    
    # Upload images dandelion
    dandelion_images = glob.glob(f'{data_dir}/dandelion/*.jpg')[:10]  # Limiter à 10 pour test
    for img_path in dandelion_images:
        filename = os.path.basename(img_path)
        upload_file_to_minio(
            img_path, BUCKET_NAME, f"dandelion/{filename}",
            ENDPOINT_URL, ACCESS_KEY, SECRET_KEY
        )
    
    print(f"✅ Upload vers MinIO terminé (depuis {data_dir})")


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

