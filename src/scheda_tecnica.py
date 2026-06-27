# CLASSE DA SCHEDA TECNICA

from enum import Enum

###############################################################################################################################
class TipoRaffredamento(str, Enum):
    ARIA  = "ARIA"
    ACQUA = "ACQUA"
###############################################################################################################################


###############################################################################################################################
class PotenzaForno(str, Enum):
    BAIXA = "BASSA"
    MEDIA = "MEDIA"
    ALTA  = "ALTA"
###############################################################################################################################    


###############################################################################################################################
class TipoLega(str, Enum):
    Lega_1050       = "LEGA 1050"
    Lega_6060_PRI   = "LEGA 6060 PRI"
    Lega_6060_PRIMA = "LEGA 6060 PRIMA"
    Lega_6063_PRI   = "LEGA 6063 PRI"
    Lega_6063_PRIMA = "LEGA 6063 PRIMA"
    Lega_6005       = "LEGA 6005"
    Lega_6082       = "LEGA 6082"
    Lega_6082_SEC   = "LEGA 6082 SEC"
    Lega_6364_BRILL = "LEGA 6364 BRILL"
###############################################################################################################################    


###############################################################################################################################
class TipoIncestatura(str, Enum):
    NORMALE = "NORMALE"
    PIOLO   = "PIOLO"
###############################################################################################################################


###############################################################################################################################
class scheda_tecnica:
    def __init__(self, matrice: str, lega: TipoLega, velocita: float, oss: str, 
                 oss_partenza: str, disegno_tec: str):
        self.matrice = str(matrice)
        self.lega = TipoLega(lega)
        self.velocita = float(velocita)        
        self.oss_pressa = str(oss)
        self.oss_partenza = str(oss_partenza)
        self.disegno_tec = str(disegno_tec)

    class atenzione:
        def __init__(self, strapp: bool, righe: bool, scie: bool, oss: str):
            self.strapp = bool(strapp)
            self.righe = bool(righe)
            self.scie = bool(scie)
            self.oss = str(oss)

    class info_estrusione:
        def __init__(self, lung_bill: int, lung_estruso: float, fondello: int, 
                    scat_testa: float, scat_coda: float, perc_rall: int, 
                    temp_rall: int, tempo_pressata: int, tempo_morto: int, 
                    tempo_chiamata: int):
            self.lung_bill = int(lung_bill)
            self.lung_estruso = float(lung_estruso)
            self.fondello = int(fondello)
            self.scat_testa = float(scat_testa)
            self.scat_coda = float(scat_coda)
            self.perc_rall = int(perc_rall)
            self.tempo_rall = int(temp_rall)    
            self.tempo_pressata = int(tempo_pressata) 
            self.tempo_morto = int(tempo_morto)  
            self.tempo_chiamata = int(tempo_chiamata)  

    class info_forno:
        def __init__(self, potenza: PotenzaForno, zona1: int, zona2: int, zona3: int, 
                     zona4: int, zona5: int, zona6: int, zona7: int):
            self.potenza = PotenzaForno(potenza)
            self.zona1 = int(zona1)
            self.zona2 = int(zona2)
            self.zona3 = int(zona3)
            self.zona4 = int(zona4)
            self.zona5 = int(zona5)
            self.zona6 = int(zona6)    
            self.zona7 = int(zona7)
    
    class info_puller_sega:
        def __init__(self, tiro: int, altezza: int, vel_taglio: int, 
                     libera: bool, F11: bool, scarico_leggero: bool):
            self.tiro = int(tiro)
            self.altezza = int(altezza)
            self.vel_taglio = int(vel_taglio)
            self.libera = bool(libera)
            self.f11 = bool(F11)
            self.scarico_leggero = bool(scarico_leggero)

    class info_raff:
        def __init__(self, tipo: TipoRaffredamento, continuo: bool, altezza_cappa: int):
            self.tipo = TipoRaffredamento(tipo)
            self.continuo = bool(continuo)
            self.altezza_cappa = int(altezza_cappa)

        class info_aria_banco:
            def __init__(self, zona1: int, continuo1: bool, zona2: int, continuo2: bool, 
                        zona3: int, continuo3: bool, zona4: int, continuo4: bool, 
                        stiratrice1: int, stiratrice2: int):
                self.zona1 = int(zona1)
                self.continuo1 = bool(continuo1)
                self.zona2 = int(zona2)
                self.continuo2 = bool(continuo2)
                self.zona3 = int(zona3)
                self.continuo3= bool(continuo3)
                self.zona4 = int(zona4)
                self.continuo4 = bool(continuo4)
                self.stiratrice1 = int(stiratrice1)
                self.stiratrice2 = int(stiratrice2)       

        class info_aria:
            def __init__(self, perc_superiore: int, perc_inferiore: int, superiore_centro: int, 
                         superiore_destra: int, superiore_sinistra: int, inferiore_destra: int, 
                         inferiore_sinistra: int):
                self.perc_superiore = int(perc_superiore)
                self.perc_inferiore = int(perc_inferiore)
                self.superiore_centro = int(superiore_centro)
                self.superiore_destra = int(superiore_destra)
                self.superiore_sinistra = int(superiore_sinistra)
                self.inferiore_destra = int(inferiore_destra)
                self.inferiore_sinistra = int(inferiore_sinistra)

        class info_acqua:
            def __init__(self, superiore: int, inferiore: int, destra: int, sinistra: int):
                self.superiore = int(superiore)
                self.inferiore = int(inferiore)
                self.destra = int(destra)
                self.sinistra = int(sinistra)     
                
          
    
    class info_stiratrice:
        def __init__(self, valore: int, spessorato: bool, oss: str):
            self.valore = int(valore)
            self.spessorato = bool(spessorato)
            self.oss = str(oss)

    class info_taglio:
        def __init__(self, tipo_incestatura: TipoIncestatura, doppiare: bool, oss: str):
            self.tipo_incestatura = TipoIncestatura(tipo_incestatura)
            self.doppiare = bool(doppiare)
            self.oss = str(oss)
###############################################################################################################################
