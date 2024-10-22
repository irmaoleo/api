from typing import Optional
from pydantic import BaseModel

class QuestionPerformance(BaseModel):
    question_id: str
    correct: bool

class TopicPerformance(BaseModel):
    topic_name: str
    questions: list[QuestionPerformance]

class SubjectPerformance(BaseModel):
    subject_name: str
    topics: list[TopicPerformance]

class Score(BaseModel):
    user_id: str
    mock_test_id: str
    performance: list[SubjectPerformance]
    overall_score: Optional[int]
    total_questions: int
    date: Optional[str]


class ScoreRequest(BaseModel):
    mock_test_id: str
    subject: str
    topic: str
    question_id: str
    correct: bool


