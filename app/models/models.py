from pydantic import BaseModel

class TestRequest(BaseModel):
    text:str

class AnalysisResponse(BaseModel):
    analysis:str


class AnalysisItem(BaseModel):
    id: int
    input_text: str
    analysis: str
    created_at: str