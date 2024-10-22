from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from ..database import users_collections, mock_tests_collections
from ..auth import validate_token

from ..models.users import Users
from ..models.mock_test import MockTestRequest
from ..models.scores import ScoreRequest

from ..schemas.mock_test import individual_serial as MockTestSerial
from ..schemas.users import individual_serial as UserSerial

from ..services.mock_test import build_mock_test, get_all_questions, submit_mock_test
from ..services.score import save_question_score, get_mock_test_score, get_user_scores


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


## USERS
@router.get("/user", response_model=Users)
async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    user = UserSerial(users_collections.find_one({"_id": ObjectId(user_id)}))
    if user is None:
        return {"message": "User not found"}

    del user["password"]
    return user


@router.patch("/user", response_model=Users)
async def update_user(user_data: Users, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    user = users_collections.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": user_data.dict(exclude_unset=True)},
        return_document=True,
    )

    del user["password"]
    return user


## DASHBOARD
@router.get("/dashboard")
async def dashboard():
    return {"message": "Welcome to the Exams API"}


@router.get("/dashboard/history")
async def dashboard(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    analytics = get_user_scores(user_id)
    return {"analytics": analytics }


@router.get("/dashboard/history/{mock_test_id}")
async def dashboard(mock_test_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    analytics = get_mock_test_score(user_id, mock_test_id)
    return {"analytics": analytics }


@router.get("/dashboard/subjects/")
async def dashboard():
    return {"message": "Welcome to the Exams API"}


@router.get("/dashboard/subjects/{subject_name}")
async def dashboard():
    return {"message": "Welcome to the Exams API"}


## MOCK TESTS
@router.post("/start_mock_test")
async def create_mock_test(
    req: MockTestRequest, token: Annotated[str, Depends(oauth2_scheme)]
):
    user_id = validate_token(token)
    created_mock_test = build_mock_test(user_id, req.exam_id, req.quantity, req.type)

    created_mock_test = mock_tests_collections.insert_one(created_mock_test)

    return {
        "mock_test_id": str(created_mock_test.inserted_id),
        "message": "Mock test started successfully",
    }


@router.get("/mock_test/{mock_test_id}")
async def get_mock_test(mock_test_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    validate_token(token)
    
    session_mock_test = MockTestSerial(
        mock_tests_collections.find_one({"_id": ObjectId(mock_test_id)})
    )

    session_questions = get_all_questions(session_mock_test["questions"])

    session_mock_test["questions"] = session_questions

    return session_mock_test


@router.post("/answer_question")
async def answer_question(
    req: ScoreRequest, token: Annotated[str, Depends(oauth2_scheme)]
):

    user_id = validate_token(token)

    score = save_question_score(
        user_id, req.mock_test_id, req.subject, req.topic, req.question_id, req.correct
    )

    return {"message": "Answer submitted successfully", "score": score}


@router.post("/submit_test/{mock_test_id}")
async def submit_test(mock_test_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)

    analytics = submit_mock_test(user_id, mock_test_id)
    return {
        "message": f"Score submitted successfully for user {user_id} on exam {mock_test_id}",
        "analytics": analytics,
    }