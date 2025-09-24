import os
from dotenv import load_dotenv

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # Configuración general
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    TESTING = False

    # PostgreSQL
    CONTRASENA_SECRETA = os.getenv("CONTRASENA_SECRETA")
    POSTGRES_URL = F"postgresql://postgres:{CONTRASENA_SECRETA}@localhost:5432/chatbotdb"
    # Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_insegura")

    # Otros ajustes opcionales
    TOKENWTHASAPP = os.getenv("TOKENWTHASAPP")
    ACCOUNTID = os.getenv("ACCOUNTID")
    TESTNUMBER = os.getenv("TESTNUMBER")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

    GEMINI_API_KEY = os.getenv("TOKEN_GEMINI")

