# database/models/Imagenes.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-3])
sys.path.append(CURRENT_PATH)
from database.Base import Base

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    nombre = Column(String, nullable=False)
    url = Column(String, nullable=False)

    pedido = relationship("Pedido", back_populates="imagenes")
