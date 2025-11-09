from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.config import settings

client = MongoClient(settings.MONGODB_URI, ServerApi=ServerApi('1'))
db = client[settings.model_config]

def get_collection(name: str):
    return db[name]