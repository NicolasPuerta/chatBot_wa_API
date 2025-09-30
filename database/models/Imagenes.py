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

    id = Column(String, primary_key=True, unique=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    url = Column(String, nullable=False)
    pedido = relationship("Pedido", back_populates="imagenes")