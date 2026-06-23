import uvicorn
from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from server.model_db import RapportinoCreate

# CONFIGURAÇÃO DO BANCO DE DADOS
SQLALCHEMY_DATABASE_URL = "sqlite:///./banco_rex.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AluMatrixDB(Base):
    __tablename__ = "rapportini"
    id = Column(Integer, primary_key=True, index=True)
    matrice = Column(String, index=True)
    turno = Column(String)
    storico = Column(String)
    data_ora = Column(String)

Base.metadata.create_all(bind=engine)

# Função para abrir e fechar a conexão com o banco com segurança
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROTAS DA API (As "Portas")
app = FastAPI(title="Servidor AluMatrix")

# ROTA POST: Para SALVAR um novo histórico
@app.post("/rapportini/")
def salvar_historico(rap: RapportinoCreate, db: Session = Depends(get_db)):
    novo_registro = AluMatrixDB(
        matrice=rap.matrice.upper(),
        turno=rap.turno,
        storico=rap.storico,
        data_ora=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # A data é gerada pelo servidor!
    )
    db.add(novo_registro)
    db.commit()
    return {"mensagem": "Registered in the SQL Database successfully!"}

# ROTA GET: Para LER o histórico de uma matriz específica
@app.get("/rapportini/{matrice:path}")
def ler_historicos(matrice: str, db: Session = Depends(get_db)):
    # O resto do código continua igual...
    registros = db.query(AluMatrixDB).filter(AluMatrixDB.matrice == matrice.upper()).all()
    return registros

if __name__ == "__main__":
    print("🚀 Iniciando o servidor na porta 8000...")
    uvicorn.run("server.api_server:app", host="127.0.0.1", port=8000, reload=True)