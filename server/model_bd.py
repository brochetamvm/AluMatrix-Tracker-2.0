# server/models.py
from sqlalchemy import Column, Integer, String, JSON
from server.database import Base

# Tabela: rapportini 
class RapportiniDB(Base):
    __tablename__ = "rapportini"
    id = Column(Integer, primary_key=True, index=True)
    matrice = Column(String, index=True)
    turno = Column(String)
    storico = Column(String)
    data_ora = Column(String)
####################################################################################################################

# Tabela: scheda_tecnica 
class SchedaTecnicaDB(Base):
    __tablename__ = "scheda_tecnica"   
    id = Column(Integer, primary_key=True, index=True)
    matrice = Column(String, index=True) 
    lega = Column(String, index=True)    
    dados = Column(JSON) # JSON complexo dentro de uma única coluna "Blob/Variant"
####################################################################################################################