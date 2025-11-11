"""
Script pour initialiser la table des prédictions dans PostgreSQL
"""
import psycopg2
import os
from datetime import datetime

# Configuration PostgreSQL
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5433"),
    "user": os.getenv("POSTGRES_USER", "airflow"),
    "password": os.getenv("POSTGRES_PASSWORD", "airflow"),
    "database": os.getenv("POSTGRES_DB", "mlops")
}

def create_predictions_table():
    """Crée la table predictions si elle n'existe pas"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Créer la table predictions
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
        
        # Créer un index sur prediction_id pour les recherches rapides
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_predictions_prediction_id 
            ON predictions(prediction_id);
        """)
        
        # Créer un index sur created_at pour les recherches par date
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_predictions_created_at 
            ON predictions(created_at);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Table 'predictions' créée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table : {e}")
        return False

if __name__ == "__main__":
    print("🔧 Initialisation de la table predictions...")
    create_predictions_table()

