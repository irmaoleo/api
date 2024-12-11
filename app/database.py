from pymongo import MongoClient
from .config import mongoSettings
import os
from supabase import create_client, Client




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


# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client('https://kxhuetxstpjfzlubltmm.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt4aHVldHhzdHBqZnpsdWJsdG1tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM4NTQ2NTUsImV4cCI6MjA0OTQzMDY1NX0.pCKZ9gp602FKAMu2v367qZLf4t7-xxg4ka1Z-HrEEVc')