from fastapi import FastAPI, File, UploadFile, HTTPException
from model import FingerCountModel
from app import PredictionResponse

app = FastAPI()

model = FingerCountModel()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    try:
        image_bytes = await file.read()
        fingers_count = model.predict(image_bytes)
        return PredictionResponse(fingers_count=fingers_count, message="Prediction successful")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))