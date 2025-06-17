import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # Configuración general
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    TESTING = False

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/chatbot")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

    # Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_insegura")

    # Otros ajustes opcionales
    TOKENWTHASAPP = os.getenv("TOKENWTHASAPP")
    ACCOUNTID = os.getenv("ACCOUNTID")
    TESTNUMBER = os.getenv("TESTNUMBER")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")