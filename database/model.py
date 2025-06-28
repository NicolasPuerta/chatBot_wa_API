# -------------------- imports --------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# -------------------- modulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('', '/').split('/')[:-1])
sys.path.append(CURRENT_PATH)
# --------------- Modules ---------------
from config import Config   

DATABASE_URL = Config().POSTGRES_URL

class DatabaseConfig():
    """Database configuration class."""
    def __init__(self, database_url=DATABASE_URL):
        super().__init__()
        self.database_url = database_url

        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

