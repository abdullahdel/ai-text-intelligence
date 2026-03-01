from fastapi import FastAPI
from app.models import TestRequest
from app.services.analyzer import analyze_text

app = FastAPI()

@app.get("/")
def root():
    return{"status":"running"}

@app.post("/analyze")
def analyze(request: TestRequest):
    return analyze_text(request.text)