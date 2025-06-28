from models.Usuarios import Usuario
from models.Pedidos import Pedidos
from models.Imagenes import Imagenes
from model import DatabaseConfig

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

        self.db = DatabaseConfig().SessionLocal
        self.Base = DatabaseConfig().Base
        self.engine = DatabaseConfig().engine
        # crear las tablas si no existen
        self.Base.metadata.create_all(bind=self.engine)

    # -------------------- Inserts --------------------
    def insertar_usuario(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def insertar_pedido(self, pedido: Pedidos):
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def insertar_imagen(self, imagen: Imagenes):
        # Copiar imagen a carpeta local
        _, ext = os.path.splitext(imagen.url)
        nombre_archivo = f"{uuid4().hex}{ext}"
        destino = os.path.join(UPLOAD_FOLDER, nombre_archivo)
        shutil.copy(imagen.url, destino)
        imagen.url = destino
        self.db.add(imagen)
        self.db.commit()
        self.db.refresh(imagen)
        return imagen
    
    # -------------------- Selects --------------------
    def obtener_usuarios(self):
        return self.db.query(Usuario).all()

    def obtener_pedidos(self):
        return self.db.query(Pedidos).all()

    def obtener_imagenes(self):
        return self.db.query(Imagenes).all()
    

    # -------------------- Updates --------------------

    def actualizar_usuario(self, usuario: Usuario):
        self.db.merge(usuario)
        self.db.commit()
        return usuario
    def actualizar_pedido(self, pedido: Pedidos):
        self.db.merge(pedido)
        self.db.commit()
        return pedido

    ## -------------------- Deletes -------------------
    def eliminar_usuario(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()

    def eliminar_pedido(self, pedido: Pedidos):
        self.db.delete(pedido)
        self.db.commit()

    def eliminar_imagen(self, imagen: Imagenes):
        self.db.delete(imagen)
        self.db.commit()