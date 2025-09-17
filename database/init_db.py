import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)
from database.Base import Base
from database.model import DatabaseConfig
from database.models import *  # Esto importa y registra todos los modelos

def init_db():
    """
    Inicializa la base de datos creando las tablas definidas en los modelos.
    """
    db = DatabaseConfig()
    Base.metadata.create_all(bind=db.engine)