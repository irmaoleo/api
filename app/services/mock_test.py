from bson import ObjectId
from datetime import datetime
import random
import string
import math

from ..database import (
    exams_collections,
    questions_collections,
    mock_tests_collections,
    scores_collections,
)
from ..schemas.exams import individual_serial as exam_serial
from ..schemas.questions import individual_serial as question_serial
from ..schemas.mock_test import individual_serial as mock_test_serial
from ..schemas.scores import individual_serial as score_serial

from ..models.scores import Score


def shuffle_options(question):
    # Extrai as opções originais e a chave correta original
    options = list(question["options"].values())  # Pega apenas os valores das opções
    correct_value = question["options"][
        question["correct_option"]
    ]  # Valor da opção correta

    # Embaralha as opções
    random.shuffle(options)

    # Gera novas chaves (a, b, c, d, ...) com base na quantidade de opções
    new_keys = list(string.ascii_lowercase[: len(options)])

    # Cria o novo dicionário de opções embaralhadas
    shuffled_options = dict(zip(new_keys, options))

    # Encontra a nova chave correspondente ao valor da opção correta
    new_correct_option = next(
        key for key, value in shuffled_options.items() if value == correct_value
    )

    # Atualiza o dicionário original
    question["options"] = shuffled_options
    question["correct_option"] = new_correct_option

    return question


def build_mock_test(user_id: str, exam_id: str, question_quantity: int, type: str, subjects: list[str]) -> dict:
    questions = []

    # Busca o exame escolhido no banco de dados
    chosen_exam = exam_serial(exams_collections.find_one({"_id": ObjectId(exam_id)}))

    # Filtro para manter apenas as matérias da lista 'subjects', se ela não estiver vazia
    if subjects:
        selected_subjects = {
            name: percentual
            for name, percentual in chosen_exam["subjects_composition"].items()
            if name in subjects
        }
    else:
        selected_subjects = chosen_exam["subjects_composition"]

    # Ajustar o percentual relativo para as matérias selecionadas
    total_percentual = sum(selected_subjects.values())
    adjusted_subjects = {
        name: (percentual / total_percentual) * 100
        for name, percentual in selected_subjects.items()
    }

    # Itera sobre cada matéria selecionada para escolher as questões
    for subject_name, subject_percentual in adjusted_subjects.items():
        questions_in_mock = math.ceil((subject_percentual / 100) * question_quantity)

        pipeline = [
            {"$match": {"subject": subject_name}},  # Filtra pelo subject
            {"$sample": {"size": questions_in_mock}},  # Seleciona questões aleatórias
            {"$project": {"_id": 1}},  # Retorna apenas o campo _id
        ]

        questions_choosen = [
            str(q["_id"]) for q in questions_collections.aggregate(pipeline)
        ]

        questions.extend(questions_choosen)

    # Retorna o mock test construído
    return {
        "type": type,
        "exam_model": chosen_exam["exam_name"],
        "user_id": user_id,
        "questions": questions,
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
    }


def get_all_questions(questions_id: list[str]):

    questions = []

    for question_id in questions_id:

        question = question_serial(
            questions_collections.find_one({"_id": ObjectId(question_id)})
        )
        shuffled_options = shuffle_options(question)
        questions.append(shuffled_options)

    return questions


def submit_mock_test(user_id: str, mock_test_id: str):

    mock_test = mock_test_serial(
        mock_tests_collections.find_one({"_id": ObjectId(mock_test_id)})
    )
    
    
    mocktest_score = scores_collections.find_one({"user_id": user_id, "mock_test_id": mock_test_id})

    if mocktest_score == None:
        mocktest_score = Score(
            user_id=user_id,
            mock_test_id=mock_test_id,
            performance=[],
            overall_score=0,
            total_questions=len(mock_test['questions']),
            date=str(datetime.utcnow().date()),
        ).dict()
        

        
        
        result = scores_collections.insert_one(mocktest_score)
        
        mocktest_score["_id"] = str(result.inserted_id)


    
    score = score_serial(
        mocktest_score
    )
    

    ## atualizar score

    correct_answers = sum(
        1
        for subject in score["performance"]
        for topic in subject["topics"]
        for question in topic["questions"]
        if question["correct"]
    )
 


    total_questions = score["total_questions"]
  
    overall_score = round((correct_answers / total_questions) * 100, 2)

    score["overall_score"] = overall_score
    score["date"] = datetime.now().strftime("%Y-%m-%d")

    del score["_id"]

    scores_collections.update_one(
        {"user_id": user_id, "mock_test_id": mock_test_id}, {"$set": score}
    )

    ## atualizar mock_test

    mock_test["end_time"] = datetime.now().isoformat()
    
    del mock_test["_id"]



    mock_tests_collections.update_one(
        {"_id": ObjectId(mock_test_id)}, {"$set": mock_test}
    )

    return score
