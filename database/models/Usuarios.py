# database/models/Usuarios.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-3])
sys.path.append(CURRENT_PATH)
from database.Base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cliente = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cedula = Column(String, nullable=True)
    telefono = Column(String, nullable=True)

    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete")
