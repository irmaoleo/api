from pydantic import BaseModel


class Exams(BaseModel): 
    _id: str
    exam_name: str
    subjects_composition: dict
    duration: int
