from bson import ObjectId

from ..database import scores_collections, mock_tests_collections

from ..schemas.scores import individual_serial as ScoreSerial, list_serial as ScoreListSerial
from ..schemas.mock_test import individual_serial as MockTestSerial

from ..models.scores import (
    Score,
    QuestionPerformance,
    TopicPerformance,
    SubjectPerformance,
)


def update_score(
    score_data: Score,
    question_id: str,
    correct: bool,
    topic_name: str,
    subject_name: str,
) -> Score:

    # Procura o subject correspondente
    subject = next((s for s in score_data["performance"] if s["subject_name"] == subject_name), None)
    
    if subject is None:
        # Se o subject não existe, cria um novo e adiciona à lista de performance
        subject = SubjectPerformance(subject_name=subject_name, topics=[]).dict()
        score_data["performance"].append(subject)

    # Procura o topic correspondente dentro do subject
    topic = next((t for t in subject["topics"] if t["topic_name"] == topic_name), None)
  
    
    if topic is None:
        # Se o topic não existe, cria um novo e adiciona à lista de topics do subject
        topic = TopicPerformance(topic_name=topic_name, questions=[]).dict()
        subject["topics"].append(topic)

    # Adiciona a nova questão ao topic
    question = QuestionPerformance(question_id=question_id, correct=correct).dict()
    topic["questions"].append(question)

    # Atualiza o total de questões
    score_data["total_questions"] += 1

    return score_data


def save_question_score(
    user_id: str,
    mock_test_id: str,
    subject_name: str,
    topic_name: str,
    question_id: str,
    correct: bool,
):
    # Ver se já existe score para esse mock test, se não cria um novo
    fonded_score = scores_collections.find_one({"mock_test_id": mock_test_id})
    
    mock_test = MockTestSerial(mock_tests_collections.find_one({"_id": ObjectId(mock_test_id)}))

    if fonded_score is None:

        questions = [QuestionPerformance(question_id=question_id, correct=correct)]
    
        

        topic = TopicPerformance(topic_name=topic_name, questions=questions)
        

        
        subject = SubjectPerformance(subject_name=subject_name, topics=[topic])


        score = Score(
            user_id=user_id,
            mock_test_id=mock_test_id,
            performance=[subject],
            overall_score=None,
            total_questions=len(mock_test['questions']),
            date=None,
        ).dict()
        
        

        result = scores_collections.insert_one(score)

        score["_id"] = str(result.inserted_id)

        return score

    else:

        score = ScoreSerial(fonded_score)

        new_score = update_score(score, question_id, correct, topic_name, subject_name)

        del new_score["_id"]
        
        result = scores_collections.update_one(
            {"_id": fonded_score["_id"]}, {"$set": new_score}
        )
        
        new_score["_id"] = str(fonded_score["_id"])

        return new_score

def get_mock_test_score(user_id: str, mock_test_id: str) -> Score:
    score = scores_collections.find_one({"user_id": user_id, "mock_test_id": mock_test_id})

    return ScoreSerial(score) if score else None

def get_user_scores(user_id: str, official: bool) -> list:
    
    if (official):
        mock_tests = mock_tests_collections.find({
            "user_id": user_id,
            "type": "official"
        },  {"_id": 1} )
        ids = [str(doc["_id"]) for doc in mock_tests]
        


    
        scores = scores_collections.find({"mock_test_id": {"$in": ids}})
        
    else:
        scores = scores_collections.find({"user_id": user_id})
    
    return ScoreListSerial(scores)