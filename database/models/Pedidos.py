# -------------------- imports --------------------
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

# -------------------- módulos --------------------
import os
import sys

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)

from database.model import DatabaseConfig

Base = DatabaseConfig().Base
class Pedidos(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    pago = Column(Boolean, nullable=False)

    usuario = relationship("Usuario", back_populates="pedidos")
    imagenes = relationship("Imagenes", back_populates="pedido", cascade="all, delete")

    def __repr__(self):
        return f"Pedido(id={self.id}, cliente_id={self.cliente_id}, fecha={self.fecha}, total={self.total}) - {self.descripcion}, cantidad={self.cantidad}, pago={self.pago})"