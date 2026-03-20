from fastapi import HTTPException
from app.services.analyzer import analyze_text, answer_question_with_context
from app.database.database import save_analysis, get_all_analyses, get_analysis_by_id, delete_analysis
from app.utils.logger import logger



def create_analysis(text, source_type="manual", source_name=None):
    result = analyze_text(text)

    if "error" in result:
        raise HTTPException(status_code= 400, detail=result["error"])

    save_analysis(text,result["analysis"], source_type, source_name)
    logger.info("Analysis stored in database")

    return result

def list_analyses(limit, offset):
    return get_all_analyses(limit, offset)

def get_analysis(analysis_id):
    result = get_analysis_by_id(analysis_id)

    if result is None:
        logger.warning(f"Analysis {analysis_id} not found")
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    return result

def delete_analysis_by_id(analysis_id):
    result = get_analysis_by_id(analysis_id)

    if result is None:
        logger.warning(f"Analysis {analysis_id} not found")
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    delete_analysis(analysis_id)
    logger.info(f"Analysis {analysis_id} deleted")

    return {"message": "Analysis deleted"}

def ask_question_about_analysis(analysis_id: int, question: str):
    analysis  = get_analysis_by_id(analysis_id)

    if analysis is None:
        logger.warning(f"Analysis {analysis_id} not found")
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    input_text = analysis["input_text"]

    result = answer_question_with_context(question, input_text)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "analysis_id": analysis_id,
        "question": question,
        "answer": result["answer"]
    }

