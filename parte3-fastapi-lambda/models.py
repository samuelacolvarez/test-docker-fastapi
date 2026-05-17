from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Imagen(Base):
    __tablename__ = "imagenes"

    id          = Column(Integer, primary_key=True, index=True)
    usuario     = Column(String(100))
    ruta_s3     = Column(String(300))
    fecha       = Column(DateTime, default=datetime.utcnow)
