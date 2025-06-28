# -------------------- imports --------------------
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)

from database.model import DatabaseConfig

Base = DatabaseConfig().Base
class Imagenes(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    nombre = Column(String, nullable=False)
    url = Column(String, nullable=False)

    pedido = relationship("Pedidos", back_populates="imagenes")

    def __repr__(self):
        return f"Imagen(id={self.id}, nombre={self.nombre}, url={self.url})"