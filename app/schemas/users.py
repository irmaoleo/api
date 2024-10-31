
def individual_serial(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "fullName": user["fullName"],
        "email": user["email"],
        "password": user["password"],
        "birthDate": user["birthDate"],
        "postalCode": user["postalCode"],
        "gender": user["gender"]
    }


def list_serial(users) -> list:
    return [individual_serial(user) for user in users]