# -------------------- imports --------------------
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)

from database.model import DatabaseConfig

Base = DatabaseConfig().Base
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cliente = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cedula = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)

    pedidos = relationship("Pedidos", back_populates="usuario", cascade="all, delete")

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre_cliente={self.nombre_cliente}, estado={self.estado}, cedula={self.cedula}, direccion={self.direccion}, telefono={self.telefono})"