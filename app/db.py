from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from app.config import settings

client = MongoClient(
    settings.MONGODB_URI,
    server_api=ServerApi('1'),
    tls=True,
    tlsCAFile=certifi.where()
)
db = client[settings.MONGODB_DB]

def get_collection(name: str):
    return db[name]
