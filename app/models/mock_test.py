from typing import Literal
from pydantic import BaseModel


class MockTestRequest(BaseModel):
    exam_id: str
    quantity: int
    type: Literal["official", "reinforcement"]
    subjects: list[str]
    
class ReportRequest(BaseModel):
    message: str
    

    
    