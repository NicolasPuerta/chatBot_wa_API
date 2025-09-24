# database/models/Pedidos.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-3])
sys.path.append(CURRENT_PATH)
from database.Base import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(String, nullable=True)
    cantidad = Column(Integer, nullable=True)
    direccion = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    total = Column(Integer, nullable=True)
    pago = Column(Boolean, nullable=True)
    tipo = Column(String, nullable=True)
    estado = Column(String, nullable=True)

    usuario = relationship("Usuario", back_populates="pedidos")
    imagenes = relationship("Imagen", back_populates="pedido", cascade="all, delete")
