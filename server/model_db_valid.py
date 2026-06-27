from pydantic import BaseModel
from enum import Enum

# VALIDAÇÃO DE DADOS (Pydantic)

# tipos de turnos
class TipoTurno(str, Enum):
    TurnoD = "D"
    TurnoE = "E"
    TurnoF = "F"
####################################################################################################################

# VALIDA DADOS: Rapportino na criacao
class RapportinoCreate(BaseModel):
    matrice: str
    turno: TipoTurno
    storico: str
####################################################################################################################    
    
# VALIDA DADOS: Rapportino na alteracao
class RapportinoUpdate(BaseModel):
    storico: str
####################################################################################################################    