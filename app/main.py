from fastapi import FastAPI
from app.models.models import TestRequest
from app.services.analyzer import analyze_text
from contextlib import asynccontextmanager
from app.database.database import init_db, save_analysis, get_all_analyses, get_analysis_by_id, init_pool
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_pool()
    init_db()
    logger.info("Application started and database initialized")
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/analyze")
def analyze(request: TestRequest):

    logger.info(f"Received analysis request (text length {len(request.text)})")

    result = analyze_text(request.text)

    if "analysis" in result:
        save_analysis(request.text, result["analysis"])
        logger.info("Analysis stored in database")

    return result


@app.get("/analyses")
def get_analyses():

    logger.info("Fetching analyses list")

    return get_all_analyses()


@app.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int):

    logger.info(f"Fetching analysis with id {analysis_id}")

    result = get_analysis_by_id(analysis_id)

    if result is None:
        logger.warning(f"Analysis {analysis_id} not found")
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    return result


@app.get("/")
def serve_index():
    logger.info("Serving frontend UI")
    return FileResponse("static/index.html")