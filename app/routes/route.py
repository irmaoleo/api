from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from ..database import users_collections, mock_tests_collections, exams_collections, reports_collection
from ..auth import validate_token, bcrypt_context

from ..models.users import Users
from ..models.mock_test import MockTestRequest, ReportRequest
from ..models.scores import ScoreRequest, format_response_score, general_analytics

from ..schemas.mock_test import individual_serial as MockTestSerial
from ..schemas.users import individual_serial as UserSerial
from ..schemas.exams import list_serial as ExamSerials

from ..services.mock_test import build_mock_test, get_all_questions, submit_mock_test
from ..services.score import save_question_score, get_mock_test_score, get_user_scores



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


## USERS
@router.get("/user", response_model=Users)
async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)

    response = users_collections.find_one({"_id": ObjectId(user_id)})

    user = UserSerial(response)


    if user is None:
        return {"message": "User not found"}

    del user["password"]
    return user


@router.patch("/user", response_model=Users)
async def update_user(user_data: Users, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)

    if (user_data.password):
        hashed_password = bcrypt_context.hash(user_data.password)
        user_data.password = hashed_password
        
    user = users_collections.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": user_data.dict(exclude_unset=True)},
        return_document=True,
    )

    del user["password"]
    return user


## DASHBOARD
@router.get("/dashboard")
async def dashboard(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    analytics = get_user_scores(user_id, True)
    
    dashboard_data = general_analytics(analytics)
    return {"data": dashboard_data }


@router.get("/dashboard/history")
async def dashboard(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    analytics = get_user_scores(user_id, False)
    
    dashboard_data = [format_response_score(x) for x in analytics ]
    return {"data": dashboard_data }


@router.get("/dashboard/history/{mock_test_id}")
async def dashboard(mock_test_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = validate_token(token)
    analytics = get_mock_test_score(user_id, mock_test_id)

    resposne = format_response_score(analytics)
    return resposne


## SUBJECTS AND EXAMAS AND REPORTS

@router.get("/exams")
async def get_exams(token: Annotated[str, Depends(oauth2_scheme)]):
    validate_token(token)
    exams = ExamSerials(exams_collections.find())
    return {"exams": exams }

@router.post("/report/{question_id}")
async def get_exams(req: ReportRequest, question_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    validate_token(token)
    response = reports_collection.insert_one({
        "question_id": question_id,
        "message": req.message
    })
    return {"report": True, "report_id": str(response.inserted_id) }

## MOCK TESTS
@router.post("/start_mock_test")
async def create_mock_test(
    req: MockTestRequest, token: Annotated[str, Depends(oauth2_scheme)]
):
    user_id = validate_token(token)
    created_mock_test = build_mock_test(user_id, req.exam_id, req.quantity, req.type, req.subjects)

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
