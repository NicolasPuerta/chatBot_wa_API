import os
import sys
# -------------------- imports --------------------
CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)

from database.models.Usuarios import Usuario
from database.models.Pedidos import Pedido
from database.models.Imagenes import Imagen
from database.model import DatabaseConfig

# -------------------- imports --------------------
import os
import shutil
from uuid import uuid4

UPLOAD_FOLDER = 'uploads'  # Define your upload folder path here

class Database:

    """
    Clase para manejar las operaciones de la base de datos.
    Esta clase proporciona métodos para insertar, actualizar, eliminar y obtener datos de la base de datos.
    Utiliza SQLAlchemy para interactuar con la base de datos.
    """
    def __init__(self):
        self.db = DatabaseConfig().SessionLocal()

    # -------------------- Inserts --------------------
    def insertar_usuario(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def insertar_pedido(self, pedido: Pedido):
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def insertar_imagen(self, imagen: Imagen):
        # Copiar imagen a carpeta local
        self.db.add(imagen)
        self.db.commit()
        return imagen
    
    # -------------------- Selects --------------------
    def obtener_usuarios(self):
        return self.db.query(Usuario).all()
    
    def obtener_usuario(self, telefono: str):
        return self.db.query(Usuario).filter(Usuario.telefono == telefono).first()

    def obtener_pedidos(self):
        return self.db.query(Pedido).all()

    def obtener_imagenes(self):
        return self.db.query(Imagen).all()

    # -------------------- Updates --------------------

    def actualizar_usuario(self, usuario: Usuario):
        self.db.merge(usuario)
        self.db.commit()
        return usuario
    
    def actualizar_pedido(self, pedido: Pedido):
        self.db.merge(pedido)
        self.db.commit()
        return pedido

    ## -------------------- Deletes -------------------
    def eliminar_usuario(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()

    def eliminar_pedido(self, pedido: Pedido):
        self.db.delete(pedido)
        self.db.commit()

    def eliminar_imagen(self, imagen: Imagen):
        self.db.delete(imagen)
        self.db.commit()