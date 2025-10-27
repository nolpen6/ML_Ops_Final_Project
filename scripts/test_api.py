"""
Script pour tester l'API de prédiction
"""
import requests
import os

def test_api_with_image(image_path, expected_class=None):
    """
    Teste l'API avec une image
    
    Args:
        image_path: Chemin vers l'image
        expected_class: Classe attendue (dandelion ou grass)
    """
    url = "http://localhost:8000/predict/"
    
    print(f"\n📸 Test de l'image : {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Erreur : Le fichier {image_path} n'existe pas")
        return
    
    # Upload l'image
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        prediction = result.get('prediction', 'unknown')
        confidence = result.get('confidence', 'unknown')
        
        print(f"✅ Prédiction : {prediction}")
        print(f"📊 Confiance : {confidence}")
        
        if expected_class:
            if prediction == expected_class:
                print(f"✅ Bonne prédiction ! Attendu : {expected_class}")
            else:
                print(f"⚠️ Prédiction incorrecte. Attendu : {expected_class}")
    else:
        print(f"❌ Erreur : {response.status_code}")
        print(f"   {response.text}")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Test de l'API Dandelion vs Grass Classifier")
    print("=" * 60)
    
    # Tester avec quelques images
    test_images = [
        ("data/dandelion/00000000.jpg", "dandelion"),
        ("data/grass/00000000.jpg", "grass"),
    ]
    
    for image_path, expected in test_images:
        test_api_with_image(image_path, expected)
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés !")
    print("=" * 60)
    print("\n💡 Pour tester d'autres images :")
    print("   python scripts/test_api.py")

