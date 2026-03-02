from fastapi import FastAPI
from app.models import TestRequest
from app.services.analyzer import analyze_text
from contextlib import asynccontextmanager
from app.database import init_db, save_analysis, get_all_analyses, get_analysis_by_id
from fastapi import HTTPException


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return{"status":"running"}

@app.post("/analyze")
def analyze(request: TestRequest):
    result = analyze_text(request.text)

    if "analysis" in result:
        save_analysis(request.text, result["analysis"])

    return result


@app.get("/analyses")
def get_analyses():
    result = get_all_analyses()

    return result

@app.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int):
    result = get_analysis_by_id(analysis_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")
    return result

