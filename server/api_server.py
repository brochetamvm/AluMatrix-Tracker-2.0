import uvicorn
import os

from server import model_bd
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from server.model_db_valid import RapportinoCreate, RapportinoUpdate
from fastapi.responses import FileResponse
from server.config import DATABASE_URL
from server.database import get_db, engine


# Rotas da api (as "portas")
app = FastAPI(title="Servidor AluMatrix")
model_bd.Base.metadata.create_all(bind=engine)
####################################################################################################################

# ROTA GET: Se servidor esta de pe
@app.get("/ping")
def ping():
    return True
####################################################################################################################


# ROTA GET: Arquivos pdf 
@app.get("/arquivos/pdf/{codigo}")
def baixar_pdf(codigo: str):
    # Monta o caminho apontando para a nova pasta no servidor
    caminho_arquivo = f"server/arquivos/pdf/{codigo}.pdf"
    
    # Verifica se o arquivo físico existe no disco do servidor
    if os.path.exists(caminho_arquivo):
        # Envia o arquivo como um anexo pela rede
        return FileResponse(path=caminho_arquivo, filename=f"{codigo}.pdf", media_type='application/pdf')
    else:
        # Devolve um erro 404 limpo para o CustomTkinter ativar o Plano B (Offline)
        raise HTTPException(status_code=404, detail="PDF não encontrado no servidor.")
####################################################################################################################


# ROTA GET: Fotos incestatura 
@app.get("/arquivos/fotos/{codigo}")
def baixar_foto(codigo: str):
    # Monta o caminho da foto
    caminho_arquivo = f"server/arquivos/fotos/{codigo}.jpg"
    
    if os.path.exists(caminho_arquivo):
        return FileResponse(path=caminho_arquivo, filename=f"{codigo}.jpg", media_type='image/jpeg')
    else:
        raise HTTPException(status_code=404, detail="Foto não encontrada no servidor.")
####################################################################################################################


# ROTA GET: Busca tudo no banco a ficha tecnica e transforma no formato JSON que seu frontend espera
@app.get("/scheda")
def get_todas_schedas(db: Session = Depends(get_db)):
    # Busca todos os registros da tabela
    registros = db.query(model_bd.SchedaTecnicaDB).all()
    
    # Reconstitui o dicionário "matrice|lega": {dados} que seu cliente Tkinter usa
    banco_formatado = {}
    for r in registros:
        chave = f"{r.matrice}|{r.lega}"
        banco_formatado[chave] = r.dados
        
    return banco_formatado
####################################################################################################################


# ROTA POST: Salva ou Atualiza no banco a ficha tecnica
@app.post("/scheda/salvar")
def salvar_scheda(dados: dict, db: Session = Depends(get_db)):
    try:
        # 'dados' é o dicionário completo enviado pelo Tkinter
        for chave, valores in dados.items():
            # A chave é "3DI12345/1|LEGA 6060"
            matrice, lega = chave.split("|")
            
            # Verifica se já existe no banco (o seu "Locate" do Delphi)
            registro = db.query(model_bd.SchedaTecnicaDB).filter(
                model_bd.SchedaTecnicaDB.matrice == matrice,
                model_bd.SchedaTecnicaDB.lega == lega
            ).first()
            
            if registro:
                # Se existe, damos um Update
                registro.dados = valores
            else:
                # Se não, criamos um novo (Insert)
                novo_registro = model_bd.SchedaTecnicaDB(
                    matrice=matrice,
                    lega=lega,
                    dados=valores
                )
                db.add(novo_registro)
        
        # Só comitamos uma vez no final, como se fosse um ApplyUpdates em lote
        db.commit()
        return {"status": "sucesso"}
    
    except Exception as e:
        db.rollback() # Segurança: Se der erro, desfaz tudo
        raise HTTPException(status_code=500, detail=str(e))
####################################################################################################################


# ROTA POST: Para SALVAR um novo histórico
@app.post("/rapportini/")
def salvar_historico(rap: RapportinoCreate, db: Session = Depends(get_db)):
    novo_registro = model_bd.RapportiniDB(
        matrice=rap.matrice.upper(),
        turno=rap.turno,
        storico=rap.storico,
        data_ora=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # A data é gerada pelo servidor!
    )
    db.add(novo_registro)
    db.commit()
    return {"mensagem": "Registered in the SQL Database successfully!"}
####################################################################################################################


# ROTA GET: Para LER o histórico de uma matriz específica
@app.get("/rapportini/{matrice:path}")
def ler_historicos(matrice: str, db: Session = Depends(get_db)):
    # O resto do código continua igual...
    registros = db.query(model_bd.RapportiniDB).filter(model_bd.RapportiniDB.matrice == matrice.upper()).all()
    return registros
####################################################################################################################


# ROTA PUT: Para MODIFICAR um histórico existente (Equivalente ao Edit + Post)
@app.put("/rapportini/{id}")
def atualizar_historico(id: int, rap: RapportinoUpdate, db: Session = Depends(get_db)):
    # Faz um "SELECT * FROM rapportini WHERE id = :id" para achar o registro
    registro = db.query(model_bd.RapportiniDB).filter(model_bd.RapportiniDB.id == id).first()
    
    # Se o ID não existir, avisa o cliente
    if not registro:
        return {"Error": "Record not found in the database."}
    
    # Atualiza os campos com os novos dados recebidos
    registro.storico = rap.storico
    registro.data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Atualiza a estampa de tempo
    
    # Salva definitivamente no banco (Commit)
    db.commit()
    return {"message": f"Record ID {id} updated successfully!"}
####################################################################################################################


# ROTA DELETE: Para APAGAR um histórico existente (Equivalente ao Delete)
@app.delete("/rapportini/{id}")
def apagar_historico(id: int, db: Session = Depends(get_db)):
    # Procura o registro pelo ID
    registro = db.query(model_bd.RapportiniDB).filter(model_bd.RapportiniDB.id == id).first()
    
    if not registro:
        return {"error": "Record not found in the database."}
    
    # Manda o banco deletar a linha
    db.delete(registro)
    db.commit()
    return {"message": f"Record ID {id} successfully deleted!"}
####################################################################################################################


if __name__ == "__main__":
    uvicorn.run("server.api_server:app", host="127.0.0.1", port=8000, reload=True)