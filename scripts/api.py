# api.py
from torchvision import transforms
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import torch
from model_train import SimpleCNN

app = FastAPI()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = SimpleCNN()
model.load_state_dict(torch.load("models/stage-1.pth", map_location=device))
model.eval()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.argmax(output, 1).item()
    label = "dandelion" if prediction == 0 else "grass"
    return {"prediction": label}
