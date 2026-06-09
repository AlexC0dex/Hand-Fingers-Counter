from pydantic import BaseModel

class PredictionResponse(BaseModel):
    fingers_count: int
    message: str