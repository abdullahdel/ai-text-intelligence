from pydantic import BaseModel

class TestRequest(BaseModel):
    text:str

class AnalysisResponse(BaseModel):
    analysis:str


class AnalysisItem(BaseModel):
    id: int
    input_text: str
    analysis: str
    source_type: str
    source_name: str| None = None
    created_at: str