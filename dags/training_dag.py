"""
DAG Airflow : Training
Entraîne le modèle et upload vers MinIO
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

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
    from scripts.model_train import train_model
    
    print("🚀 Démarrage de l'entraînement...")
    model = train_model(epochs=3)
    print("✅ Entraînement terminé")
    return "Model trained"


def upload_model():
    """Upload le modèle vers MinIO"""
    from scripts.upload_model_to_minio import upload_file_to_minio, ensure_bucket_exists
    
    ENDPOINT_URL = "http://localhost:9000"
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "mlops-models"
    
    ensure_bucket_exists(BUCKET_NAME, ENDPOINT_URL, ACCESS_KEY, SECRET_KEY)
    
    # Upload le meilleur modèle
    model_path = "models/best_model_epoch_3.pth"
    if os.path.exists(model_path):
        upload_file_to_minio(
            model_path, BUCKET_NAME, "models/best_model.pth",
            ENDPOINT_URL, ACCESS_KEY, SECRET_KEY
        )
    else:
        print("⚠️ Modèle non trouvé")


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

