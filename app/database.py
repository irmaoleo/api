from pymongo import MongoClient
from .config import mongoSettings

# Conectar ao MongoDB usando a URI do Atlas
client = MongoClient(mongoSettings.mongodb_uri)

# Acessar o banco de dados específico
db = client[mongoSettings.mongodb_name]

exams_collections = db["exams"]
mock_tests_collections = db["mock_tests"]
questions_collections = db["questions"]
scores_collections = db["scores"]
subjects_collections = db["subjects"]
users_collections = db["users"]
reports_collection = db["reports"]

