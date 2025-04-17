

## 🔧 Use Case
You're deploying a regression model:  
**Model equation**:  
```
y = 10X1 + 3X2 - 20
```

We'll expose this via FastAPI and deploy it using Minikube.

---

## ✅ Step 1: Build a FastAPI App

Let’s first create a FastAPI app that exposes an endpoint to get predictions from this model.

### 📁 Folder Structure
```
regression_app/
│
├── app/
│   ├── main.py
│   └── model.py
├── requirements.txt
├── Dockerfile
└── README.md
```

### 🔹 `app/model.py`
```python
def predict(x1: float, x2: float) -> float:
    return 10 * x1 + 3 * x2 - 20
```

### 🔹 `app/main.py`
```python
from fastapi import FastAPI
from pydantic import BaseModel
from app.model import predict

app = FastAPI()

class InputFeatures(BaseModel):
    x1: float
    x2: float

@app.post("/predict")
def get_prediction(features: InputFeatures):
    result = predict(features.x1, features.x2)
    return {"prediction": result}
```

### 🔹 `requirements.txt`
```
fastapi
uvicorn
```

---

## ✅ Step 2: Dockerize the App

### 🔹 `Dockerfile`
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

Build and test locally:

```bash
docker build -t regression-fastapi .
docker run -d -p 8000:80 regression-fastapi
```

Test locally:

```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"x1": 1.0, "x2": 2.0}'
```

---

## ✅ Step 3: Deploy to Minikube

### 🧱 Create Kubernetes Manifests

#### `deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: regression-model
spec:
  replicas: 1
  selector:
    matchLabels:
      app: regression-model
  template:
    metadata:
      labels:
        app: regression-model
    spec:
      containers:
      - name: regression-model
        image: regression-fastapi:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 80
```

#### `service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: regression-service
spec:
  selector:
    app: regression-model
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

### 🚀 Deploy to Minikube

```bash
minikube start
eval $(minikube docker-env)  # Use local Docker inside Minikube
docker build -t regression-fastapi .
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Get the URL to access:

```bash
minikube service regression-service --url
```

You can now POST to that URL to get predictions.

---

## ✅ Step 4: Call the API from Your Local System

Example using `curl`:

```bash
curl -X POST "<minikube_url>/predict" -H "Content-Type: application/json" -d '{"x1": 4.0, "x2": 1.0}'
```