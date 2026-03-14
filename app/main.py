from fastapi import FastAPI
from app.models.models import TestRequest, AnalysisItem, AnalysisResponse
from app.services.analyzer import analyze_text
from contextlib import asynccontextmanager
from app.database.database import init_db, save_analysis, get_all_analyses, get_analysis_by_id, init_pool, delete_analysis
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.utils.logger import logger
from app.utils.error_handler import global_exception_handler
from typing import List
from fastapi import Query

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_pool()
    init_db()
    logger.info("Application started and database initialized")
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(Exception, global_exception_handler)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: TestRequest):

    logger.info(f"Received analysis request (text length {len(request.text)})")

    result = analyze_text(request.text)

    if "analysis" in result:
        save_analysis(request.text, result["analysis"])
        logger.info("Analysis stored in database")

    return result


@app.get("/analyses", response_model=List[AnalysisItem])
def get_analyses(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0)
):

    logger.info("Fetching analyses list")

    result = get_all_analyses(limit,offset)
    return result


@app.get("/analyses/{analysis_id}", response_model=AnalysisItem)
def get_analysis(analysis_id: int):

    logger.info(f"Fetching analysis with id {analysis_id}")

    result = get_analysis_by_id(analysis_id)

    if result is None:
        logger.warning(f"Analysis {analysis_id} not found")
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    return result

@app.delete("/analyses/{analysis_id:int}")
def delete_analysis_endpoint(analysis_id: int):
    logger.info(f"Delete analysis {analysis_id}")
    result = get_analysis_by_id(analysis_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    delete_analysis(analysis_id)

    return {"message": "Analysis deleted"}


@app.get("/")
def serve_index():
    logger.info("Serving frontend UI")
    return FileResponse("static/index.html")