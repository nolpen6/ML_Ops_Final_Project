"""
Script de test pour vérifier que les images sont bien lues
"""
import os
import torch
from data_preparation import load_data

def test_image_loading():
    """Test si les images sont bien chargées"""
    
    print("=" * 60)
    print("🧪 TEST 1 : Vérification des images")
    print("=" * 60)
    
    # Vérifier que le dossier data existe
    if not os.path.exists('data'):
        print("❌ Erreur : Le dossier 'data' n'existe pas")
        print("   📍 Assurez-vous d'être dans le dossier emmaloou-ML_Ops/")
        return False
    
    # Vérifier les sous-dossiers
    if not os.path.exists('data/grass'):
        print("❌ Erreur : Le dossier 'data/grass' n'existe pas")
        return False
    
    if not os.path.exists('data/dandelion'):
        print("❌ Erreur : Le dossier 'data/dandelion' n'existe pas")
        return False
    
    # Compter les images
    grass_count = len([f for f in os.listdir('data/grass') if f.endswith(('.jpg', '.jpeg', '.png'))])
    dandelion_count = len([f for f in os.listdir('data/dandelion') if f.endswith(('.jpg', '.jpeg', '.png'))])
    
    print(f"✅ Images grass trouvées : {grass_count}")
    print(f"✅ Images dandelion trouvées : {dandelion_count}")
    print(f"✅ Total : {grass_count + dandelion_count} images")
    
    if grass_count == 0 or dandelion_count == 0:
        print("❌ Erreur : Aucune image trouvée dans les dossiers")
        return False
    
    print("\n" + "=" * 60)
    print("🧪 TEST 2 : Chargement des données avec PyTorch")
    print("=" * 60)
    
    # Tester le chargement des données
    try:
        train_loader, val_loader = load_data()
        
        print(f"✅ Train loader créé : {len(train_loader)} batches")
        print(f"✅ Validation loader créé : {len(val_loader)} batches")
        
        # Afficher la taille d'un batch
        batch = next(iter(train_loader))
        images, labels = batch
        print(f"✅ Shape d'un batch : {images.shape}")
        print(f"✅ Shape des labels : {labels.shape}")
        
        print(f"\n🎯 Test réussi ! Les données sont prêtes pour l'entraînement.")
        print(f"   - Train set : ~{len(train_loader) * 32} images")
        print(f"   - Validation set : ~{len(val_loader) * 32} images")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données : {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🚀 Démarrage des tests d'images...\n")
    
    # Se placer dans le bon répertoire
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    print(f"📍 Répertoire de travail : {os.getcwd()}\n")
    
    success = test_image_loading()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS SONT RÉUSSIS !")
        print("=" * 60)
        print("\n🎯 Prochaines étapes :")
        print("   1. Vous pouvez maintenant entraîner le modèle")
        print("   2. Les données sont prêtes à être utilisées")
        exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ LES TESTS ONT ÉCHOUÉ")
        print("=" * 60)
        print("\nVérifiez que :")
        print("   - Le dossier data/ existe")
        print("   - Les dossiers data/grass/ et data/dandelion/ existent")
        print("   - Ils contiennent des images .jpg, .jpeg ou .png")
        exit(1)

