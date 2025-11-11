"""
DAG Airflow : Training
Entraîne le modèle et upload vers MinIO
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'MLOps Team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'training',
    default_args=default_args,
    description='Entraînement du modèle de classification',
    schedule_interval=timedelta(days=7),  # Exécution hebdomadaire
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['mlops', 'training'],
)


def train_model():
    """Entraîne le modèle"""
    import sys
    
    # Ajouter le chemin des scripts au PYTHONPATH
    scripts_path = "/opt/airflow/scripts"
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    
    from model_train import train_model
    
    print("🚀 Démarrage de l'entraînement...")
    model = train_model(epochs=3)
    print("✅ Entraînement terminé")
    return "Model trained"


def upload_model():
    """Upload le modèle vers MinIO"""
    import sys
    
    # Ajouter le chemin des scripts au PYTHONPATH
    scripts_path = "/opt/airflow/scripts"
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    
    from upload_model_to_minio import upload_file_to_minio, ensure_bucket_exists
    
    ENDPOINT_URL = "http://minio:9000"  # Utiliser le nom du service Docker
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "mlops-models"
    
    ensure_bucket_exists(BUCKET_NAME, ENDPOINT_URL, ACCESS_KEY, SECRET_KEY)
    
    # Upload le meilleur modèle - chercher dans différents chemins possibles
    possible_paths = [
        "models/best_model_epoch_3.pth",
        "/opt/airflow/models/best_model_epoch_3.pth",
        "./models/best_model.pth"
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path:
        upload_file_to_minio(
            model_path, BUCKET_NAME, "models/best_model.pth",
            ENDPOINT_URL, ACCESS_KEY, SECRET_KEY
        )
        print(f"✅ Modèle uploadé depuis {model_path}")
    else:
        print("⚠️ Modèle non trouvé dans aucun des chemins suivants:")
        for path in possible_paths:
            print(f"   - {path}")


train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

upload_model_task = PythonOperator(
    task_id='upload_model',
    python_callable=upload_model,
    dag=dag,
)

train_task >> upload_model_task

