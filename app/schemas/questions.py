
def individual_serial(question) -> dict:
    return {
        "_id": str(question["_id"]),
        "subject": question["subject"],
        "topic": question["topic"],
        "text": question["text"],
        "options": question["options"],
        "correct_option": question["correct_option"],
        "comment": question["comment"],
        "difficulty": question["difficulty"],
        "category": question["category"],
        "tags": question["tags"],
    }
    
def list_serial(questions) -> list:
    return [individual_serial(question) for question in questions]