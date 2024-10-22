def individual_serial(score) -> dict:
    return {
        "_id": str(score["_id"]),
        "user_id": score["user_id"],
        "mock_test_id": score["mock_test_id"],
        "performance": score["performance"],
        "overall_score": score["overall_score"],
        "total_questions": score["total_questions"],
        "date": score["date"]
    }
    
def list_serial(scores) -> list:
    return [individual_serial(score) for score in scores]




