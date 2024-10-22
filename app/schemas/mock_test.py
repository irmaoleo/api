

def individual_serial(mock_test) -> dict:
    return {
        "_id": str(mock_test["_id"]),
        "user_id": str(mock_test["user_id"]),
        "exam_model": str(mock_test["exam_model"]),
        "type": mock_test["type"],
        "questions": mock_test["questions"],
        "start_time": mock_test["start_time"],
        "end_time": mock_test["end_time"] if mock_test["end_time"] else None 
    }
    
def list_serial(mock_tests) -> list:
    return [individual_serial(mock_test) for mock_test in mock_tests]
