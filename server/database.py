from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server.config import DATABASE_URL

# O Engine é o motor que gerencia a conexão (como o TFDConnection)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# O SessionLocal é o que abriremos para fazer operações (equivale ao StartTransaction)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# O Base é a classe mãe que todos os seus Models (Tabelas) vão herdar
Base = declarative_base()

# Função para obter a sessão (o equivalente a abrir uma query)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()