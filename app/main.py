from contextlib import asynccontextmanager
from typing import List

from envs.myenv.Lib.fileinput import filename
from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pypdf import PdfReader

from app.database.database import init_db, init_pool
from app.models.models import TestRequest, AnalysisItem, AnalysisResponse
from app.services.analysis_service import (
    create_analysis,
    list_analyses,
    get_analysis as get_analysis_service,
    delete_analysis_by_id,
)
from app.utils.error_handler import global_exception_handler
from app.utils.logger import logger


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
    return create_analysis(request.text)

@app.post("/upload-analyze", response_model=AnalysisResponse)
def upload_analyze(file:UploadFile=File(...)):
    logger.info(f"Received file upload request: {file.filename}")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Keine Datei hochgeladen.")

    if not file.filename.lower().endswith((".txt", ".pdf")):
        raise HTTPException(status_code=400, detail="Nur .txt- und .pdf-Dateien sind erlaubt.")

    if file.filename.endswith(".txt"):
        try:
            content = file.file.read()
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Datei konnte nicht als UTF-8 Text gelesen werden.")

    elif file.filename.endswith(".pdf"):
        try:
            reader = PdfReader(file.file)
            parts = []

            for page in reader.pages:
                parts.append(page.extract_text() or "")

            text = "\n".join(parts).strip()
            if not text:
                raise HTTPException(status_code=400, detail="PDF enthält keinen extrahierbaren Text.")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=400, detail="PDF konnte nicht verarbeitet werden.")

    return create_analysis(text, "file", file.filename)


@app.get("/analyses", response_model=List[AnalysisItem])
def get_analyses(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0)
):
    logger.info("Fetching analyses list")
    return list_analyses(limit, offset)


@app.get("/analyses/{analysis_id}", response_model=AnalysisItem)
def get_analysis_endpoint(analysis_id: int):
    logger.info(f"Fetching analysis with id {analysis_id}")
    return get_analysis_service(analysis_id)


@app.delete("/analyses/{analysis_id}")
def delete_analysis_endpoint(analysis_id: int):
    logger.info(f"Deleting analysis {analysis_id}")
    return delete_analysis_by_id(analysis_id)


@app.get("/")
def serve_index():
    logger.info("Serving frontend UI")
    return FileResponse("static/index.html")

