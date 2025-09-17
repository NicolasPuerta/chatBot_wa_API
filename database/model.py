# -------------------- imports --------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)
# --------------- Modules ---------------
from config import Config   

DATABASE_URL = Config().POSTGRES_URL

class DatabaseConfig():
    """Database configuration class."""

    def __init__(self, database_url=str(DATABASE_URL)):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)