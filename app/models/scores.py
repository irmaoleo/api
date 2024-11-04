from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from ..database import mock_tests_collections, exams_collections
from ..schemas.mock_test import individual_serial as MockTestSerial

from bson import ObjectId


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


class Question(BaseModel):
    question_id: str
    correct: bool


class Topic(BaseModel):
    topic: str
    questions: List[Question]


class Subject(BaseModel):
    subject: str
    topics: List[Topic]


class Summary(BaseModel):
    questions_answered: str
    percentage_score: str
    time_taken: str


class FormattedResponse(BaseModel):
    date: str
    title: str
    summary: Summary
    details: List[Subject]


class SubjectPerformanceResponse(BaseModel):
    subject: str
    percentage: float


class GeneralPerformanceResponse(BaseModel):
    answered: int
    correct: int
    errors: int


class PerformanceResponse(BaseModel):
    general_performance: GeneralPerformanceResponse
    subject_performance: List[SubjectPerformanceResponse]


def format_response_score(data: Score) -> FormattedResponse:
    # Extrai as informações principais

    date = datetime.strptime(data["date"], "%Y-%m-%d").strftime("%d de %B de %Y")

    # Contabiliza o total de acertos
    correct_answers = sum(
        1
        for subject in data["performance"]
        for topic in subject["topics"]
        for question in topic["questions"]
        if question["correct"]
    )


    total_questions = data["total_questions"]
    score = data["overall_score"]

    data["mock_test_id"]

    mock_test_data = MockTestSerial(
        mock_tests_collections.find_one({"_id": ObjectId(data["mock_test_id"])})
    )

    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    start_dt = datetime.strptime(mock_test_data["start_time"], fmt)
    end_dt = datetime.strptime(mock_test_data["end_time"], fmt)

    # Calcular a diferença entre as duas datas/hora
    elapsed_time = end_dt - start_dt

    # Obter o total de segundos
    total_seconds = int(elapsed_time.total_seconds())

    # Calcular minutos e segundos
    minutes, seconds = divmod(total_seconds, 60)

    # Estrutura do resultado final para o frontend
    result = {
        "date": date,
        "title": f"{'SIMULADO' if  mock_test_data['type'] == 'official' else 'REFORÇO'} {mock_test_data['exam_model'].upper()}",
        "summary": {
            "questions_answered": f"{correct_answers}/{total_questions}",
            "percentage_score": f"{score:.2f}%",
            "time_taken": f"{minutes}:{seconds}",  # Isso pode ser calculado se você tiver o tempo inicial e final
        },
        "details": [
            {
                "subject": subject["subject_name"],
                "topics": [
                    {
                        "topic": topic["topic_name"],
                        "questions": [
                            {"question_id": q["question_id"], "correct": q["correct"]}
                            for q in topic["questions"]
                        ],
                    }
                    for topic in subject["topics"]
                ],
            }
            for subject in data["performance"]
        ],
    }
    
    print({
        "summary": {
            "questions_answered": f"{correct_answers}/{total_questions}",
            "percentage_score": f"{score:.2f}%",
            "time_taken": f"{minutes}:{seconds}",  # Isso pode ser calculado se você tiver o tempo inicial e final
        }
    })

    return result


def general_analytics(data: List[Score]) -> PerformanceResponse:
    # Inicializa variáveis para contagem de acertos e erros
    total_respondidas = 0
    total_acertos = 0
    performance_materias = {}

    # Itera sobre todos os itens da lista de dados
    for simulacao in data:
        # Itera sobre o desempenho por matéria de cada simulação
        for item in simulacao["performance"]:
            materia = item["subject_name"]

            # Inicializa a matéria no dicionário se ainda não existir
            if materia not in performance_materias:
                performance_materias[materia] = {"questions": 0, "correct": 0}

            # Itera sobre os tópicos dentro de cada matéria
            for topic in item["topics"]:
                for question in topic["questions"]:
                    # Atualiza as contagens gerais
                    performance_materias[materia]["questions"] += 1
                    total_respondidas += 1
                    if question["correct"]:
                        performance_materias[materia]["correct"] += 1
                        total_acertos += 1

    # Calcula a performance por matéria
    performance_list = []
    for materia, stats in performance_materias.items():
        percentual = (stats["correct"] / stats["questions"]) * 100
        performance_list.append(
            {"subject": materia, "percentage": round(percentual, 2)}
        )

    # Calcula o total de erros
    total_erros = total_respondidas - total_acertos

    # Monta o JSON final
    resultado = {
        "general_performance": {
            "answered": total_respondidas,
            "correct": total_acertos,
            "errors": total_erros,
        },
        "subject_performance": performance_list,
    }

    return resultado
