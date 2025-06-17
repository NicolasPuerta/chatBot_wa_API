from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
URL = os.getenv("MONGO_URI")
class MongoDB:
    def __init__(self, uri=URL):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['whatsapp_bot']
        self.collection = self.db["messages"]