

def individual_serial(exam) -> dict:
    return {
        "_id": str(exam["_id"]),
        "exam_name": exam["exam_name"],
        "subjects_composition": exam["subjects_composition"],
        "duration": exam["duration"]
    }

def list_serial(exams) -> list:
    return [individual_serial(exam) for exam in exams]