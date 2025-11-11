# model_train.py
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import sys
import os

# Ajouter le chemin des scripts au PYTHONPATH si nécessaire
# Dans le conteneur Airflow, utiliser directement le chemin Docker
# En local, utiliser le chemin relatif
if os.path.exists('/opt/airflow/scripts'):
    scripts_path = '/opt/airflow/scripts'
else:
    # En local, utiliser le répertoire parent de ce fichier
    scripts_path = os.path.dirname(os.path.abspath(__file__))

if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from data_preparation import load_data
import mlflow
import mlflow.pytorch

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)

    def forward(self, x):
        return self.model(x)


def calculate_accuracy(outputs, labels):
    """Calcule l'accuracy"""
    _, predicted = torch.max(outputs.data, 1)
    total = labels.size(0)
    correct = (predicted == labels).sum().item()
    return 100 * correct / total


def train_model(epochs=10):
    """
    Entraîne le modèle avec validation et suivi des métriques
    
    Args:
        epochs: Nombre d'époques d'entraînement
        
    Returns:
        Le modèle entraîné
    """
    # Changer le répertoire de travail pour éviter les problèmes de chemin
    original_cwd = os.getcwd()
    if os.path.exists('/opt/airflow'):
        os.chdir('/opt/airflow')
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🔧 Device utilisé : {device}")
    
    # Charger les données - utiliser le chemin Docker dans le conteneur
    if os.path.exists('/opt/airflow/data'):
        data_dir = '/opt/airflow/data'
    else:
        data_dir = 'data'
    train_loader, val_loader = load_data(data_dir=data_dir)
    print(f"📊 Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")
    
    # Créer le modèle
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Créer le dossier models/ s'il n'existe pas
    # Utiliser le chemin Docker dans le conteneur
    if os.path.exists('/opt/airflow/models'):
        models_dir = '/opt/airflow/models'
    else:
        models_dir = 'models'
        os.makedirs(models_dir, exist_ok=True)
    
    # Variables pour tracking
    best_val_acc = 0.0
    best_model_path = None
    
    # Configuration MLflow
    # Utiliser le serveur MLflow HTTP pour enregistrer les runs dans SQLite
    # Utiliser l'adresse IP du conteneur MLflow pour éviter l'erreur "Invalid Host header"
    if os.path.exists('/opt/airflow'):
        # Dans le conteneur Airflow, obtenir l'IP du conteneur MLflow
        import subprocess
        try:
            # Obtenir l'IP du conteneur MLflow via le réseau Docker
            result = subprocess.run(['getent', 'hosts', 'mlflow'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                mlflow_ip = result.stdout.split()[0]
                mlflow_uri = f"http://{mlflow_ip}:5000"
            else:
                # Fallback: utiliser le nom du service (peut causer l'erreur Invalid Host header)
                mlflow_uri = "http://mlflow:5000"
        except Exception as e:
            print(f"⚠️ Erreur lors de la résolution de l'IP MLflow: {e}")
            # Fallback: utiliser le nom du service
            mlflow_uri = "http://mlflow:5000"
        
        mlflow.set_tracking_uri(mlflow_uri)
        print(f"🔗 MLflow Tracking URI: {mlflow_uri}")
    else:
        # En local, utiliser le serveur MLflow sur localhost
        mlflow.set_tracking_uri("http://localhost:5001")
        print(f"🔗 MLflow Tracking URI: http://localhost:5001")
    mlflow.set_experiment("dandelion_vs_grass_classifier")
    
    mlflow.pytorch.autolog()
    
    print("\n" + "=" * 60)
    print("🚀 Démarrage de l'entraînement")
    print("=" * 60 + "\n")
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("learning_rate", 0.001)
        mlflow.log_param("optimizer", "Adam")
        mlflow.log_param("model_architecture", "ResNet18")
        
        for epoch in range(epochs):
            # ========== TRAINING ==========
            model.train()
            train_loss = 0.0
            train_acc = 0.0
            
            for batch_idx, (inputs, labels) in enumerate(train_loader):
                inputs, labels = inputs.to(device), labels.to(device)
                
                # Forward pass
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                train_acc += calculate_accuracy(outputs, labels)
            
            avg_train_loss = train_loss / len(train_loader)
            avg_train_acc = train_acc / len(train_loader)
            
            # ========== VALIDATION ==========
            model.eval()
            val_loss = 0.0
            val_acc = 0.0
            
            with torch.no_grad():
                for inputs, labels in val_loader:
                    inputs, labels = inputs.to(device), labels.to(device)
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    
                    val_loss += loss.item()
                    val_acc += calculate_accuracy(outputs, labels)
            
            avg_val_loss = val_loss / len(val_loader)
            avg_val_acc = val_acc / len(val_loader)
            
            # Afficher les résultats
            print(f"Epoch {epoch+1}/{epochs}")
            print(f"  Train - Loss: {avg_train_loss:.4f}, Acc: {avg_train_acc:.2f}%")
            print(f"  Val   - Loss: {avg_val_loss:.4f}, Acc: {avg_val_acc:.2f}%")
            
            # Log metrics to MLflow
            mlflow.log_metric("train_loss", avg_train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", avg_train_acc, step=epoch)
            mlflow.log_metric("val_loss", avg_val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", avg_val_acc, step=epoch)
            
            # Sauvegarder le meilleur modèle
            if avg_val_acc > best_val_acc:
                best_val_acc = avg_val_acc
                best_model_path = os.path.join(models_dir, f"best_model_epoch_{epoch+1}.pth")
                torch.save(model.state_dict(), best_model_path)
                print(f"  ✅ Nouveau meilleur modèle sauvegardé ! (Acc: {best_val_acc:.2f}%)")
                mlflow.log_metric("best_val_accuracy", best_val_acc)
        
        # Sauvegarder le modèle final
        final_model_path = os.path.join(models_dir, "final_model.pth")
        torch.save(model.state_dict(), final_model_path)
        # Logger l'artifact seulement si le chemin est valide (commence par /opt/airflow)
        if final_model_path.startswith('/opt/airflow'):
            try:
                mlflow.log_artifact(final_model_path)
            except Exception as e:
                print(f"⚠️ Impossible de logger l'artifact MLflow : {e}")
        
        # Sauvegarder le meilleur modèle
        if best_model_path and best_model_path.startswith('/opt/airflow'):
            try:
                mlflow.log_artifact(best_model_path)
            except Exception as e:
                print(f"⚠️ Impossible de logger l'artifact MLflow : {e}")
    
    # Restaurer le répertoire de travail original
    os.chdir(original_cwd)
    
    print("\n" + "=" * 60)
    print("✅ Entraînement terminé !")
    print("=" * 60)
    print(f"🏆 Meilleure accuracy de validation : {best_val_acc:.2f}%")
    print(f"📦 Modèles sauvegardés :")
    print(f"   - {final_model_path}")
    if best_model_path:
        print(f"   - {best_model_path}")
    print("=" * 60 + "\n")
    
    return model


if __name__ == "__main__":
    import sys
    
    # Prendre le nombre d'epochs en argument ou utiliser 5 par défaut
    epochs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"Entraînement sur {epochs} époques...\n")
    
    model = train_model(epochs=epochs)
    
    print("🎉 Modèle entraîné et sauvegardé avec succès !")
