from pydantic import BaseModel
from enum import Enum

class TipoTurno(str, Enum):
    TurnoD = "D"
    TurnoE = "E"
    TurnoF = "F"

# VALIDAÇÃO DE DADOS (Pydantic)
# Isso garante que a interface gráfica mande exatamente os campos que queremos (sem lixo)
class RapportinoCreate(BaseModel):
    matrice: str
    turno: TipoTurno
    storico: str
    
# Quando formos editar, o operador só vai alterar o texto do histórico
class RapportinoUpdate(BaseModel):
    storico: str