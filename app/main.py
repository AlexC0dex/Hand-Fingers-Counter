from datetime import datetime
import os

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from model import FingerCountModel
from app import PredictionResponse

app = FastAPI()

DATASET_DIR = "./data/dataset_nao"

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR, exist_ok=True)

model = FingerCountModel()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), etiqueta_real: int = Form(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    try:
        image_bytes = await file.read()

        subcarpeta = os.path.join(DATASET_DIR, str(etiqueta_real))
        if not os.path.exists(subcarpeta):
            os.makedirs(subcarpeta, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        fingers_count = model.predict(image_bytes)

        nombre_archivo = f"{fingers_count}_img_{timestamp}.jpg"
        ruta_completa = os.path.join(subcarpeta, nombre_archivo)
        
        with open(ruta_completa, "wb") as f:
            f.write(image_bytes)

        return PredictionResponse(fingers_count=fingers_count, message="Prediction successful", saved_path=ruta_completa)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))