from sqlalchemy import Column, Integer, String, Float
from database import Base

class Clasificacion(Base):
    __tablename__ = "clasificaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String)
    etiqueta = Column(String)
    confianza = Column(Float)
    url_s3 = Column(String)
