from fastapi import FastAPI
from pydantic import BaseModel
from model import predict

app = FastAPI()

class InputFeatures(BaseModel):
    x1: float
    x2: float

@app.post("/predict")
def get_prediction(features: InputFeatures):
    result = predict(features.x1, features.x2)
    return {"prediction": result}
