# file per func utilitarias
import os
import sys
import customtkinter as ctk
import json

from tkinter import messagebox
from PIL import Image
from pathlib import Path

# formata form
def format_form(frm_l, frm_a, frm_self):
    # 1. Defina o tamanho que você quer para ESTA janela
    largura_janela = frm_l
    altura_janela = frm_a
    
    # 2. Descubra a largura e altura total da tela do usuário
    largura_tela = frm_self.winfo_screenwidth()
    altura_tela = frm_self.winfo_screenheight()
    
    # 3. Calcule a posição X e Y para a janela ficar no centro
    posicao_x = int((largura_tela / 2) - (largura_janela / 2) + 100)
    posicao_y = int((altura_tela / 2) - (altura_janela / 2))
    
    # 4. Aplique a geometria no formato: "LARGURAxALTURA+X+Y"
    frm_self.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

# carregar imagem em um label
def carrega_imagem(path_img, largura, altura):
    return ctk.CTkImage(
            light_image=Image.open(path_img),
            dark_image=Image.open(path_img),
            size=(largura, altura))
    
# valida campo codgo matrice
def valida_cod_matrice(valor_campo, scheda_tecnica):
    validacao = True
    tamanho = len(valor_campo)

    if tamanho > 11:
        validacao = False
    else:
        if scheda_tecnica == True and tamanho < 10:
            validacao = False
        else:
            if scheda_tecnica == False and tamanho < 8:    
                validacao = False

    tamanho_antes_da_barra = len(valor_campo.split("/")[0])

    if tamanho_antes_da_barra != 8:
        validacao = False

    if (scheda_tecnica == True) and ("/" not in valor_campo):
        validacao = False

    if tamanho == 0:
      validacao == False   
      messagebox.showinfo("Informare l'articolo", "Informare l'articolo!")
      return validacao

    if validacao == False: 
        messagebox.showwarning("Atenzione!", f"Articolo non valido - [{valor_campo}]")         

    return validacao

# executa procura do PDF/desenho tecnico
def exec_cerca_PDF(cod_matrice):   
    encontrou = False

    if valida_cod_matrice(cod_matrice, False) == True:        
        codigo = cod_matrice[:8]
        dir, status = ler_json_path("PDF") 
        dir = Path(dir)

        if dir.is_dir() == True:
            path_pdf = Path(dir)
            arquivo = path_pdf / f"{codigo}.pdf"

            if arquivo.exists() and arquivo.is_file():         
                os.startfile(arquivo)
                encontrou = True  
            else:
                messagebox.showwarning("Atenzione!", f"Articolo [{codigo}] non trovato!\n\n[{arquivo}]") 
          
    return encontrou   

# executa procura foto incestatura
def exec_cerca_foto_incestatura(cod_matrice):   
    encontrou = False

    if valida_cod_matrice(cod_matrice, False) == True:        
        codigo = cod_matrice[:8]
        dir, status = ler_json_path("FOTO") 
        dir = Path(dir)
        
        if dir.is_dir() == True:
            path_pdf = Path(dir)
            arquivo = path_pdf / f"{codigo}.jpg"

            if arquivo.exists() and arquivo.is_file():         
                os.startfile(arquivo)
                encontrou = True  
            else:
                messagebox.showwarning("Atenzione!", f"Articolo [{codigo}] non trovato!\n\n[{arquivo}]") 
          
    return encontrou   

# converter minuscalas em letras maiusculas
def somente_maiusculas(campo):
    def converter(event):
        texto = campo.get().upper()
        posicao = campo.index("insert")
        campo.delete(0, "end")
        campo.insert(0, texto)
        campo.icursor(posicao)

    campo.bind("<KeyRelease>", converter) 

# ler json
def ler_json_path(tipo):
    dir = verifica_path_exec()
    dir = Path(dir)  
    caminho = dir / f"json/path.json" 
    path_dir = None
    status = "[Status: ]"

    if tipo == "PDF":
        chave_rete = "path_pdf_rete"
        chave_local = "path_pdf_locale"
    elif tipo == "FOTO":
        chave_rete = "path_foto_rete"
        chave_local = "path_foto_locale"

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        path_dir = Path(dados[f"{chave_rete}"])
        status = "[Status: RETE]"
        if path_dir.is_dir() == False:
            path_dir = Path(dados[f"{chave_local}"])
            status = "[Status: LOCALE]"

        if path_dir.is_dir() == False:
            messagebox.showwarning("", f"Impossibile trovare i file. Contattare il reparto IT.\n\n[{path_dir}]") 
            status = "[Status: ERRORE1]"
    except FileNotFoundError:
        messagebox.showwarning("", f"Impossibile trovare i file [JSON]. Contattare il reparto IT.\n\n[{caminho}]")
        status = "[Status: ERRORE2]"

    return path_dir, status

# pega o diretorio do executavel
def verifica_path_exec():
    if getattr(sys, 'frozen', False):
        diretorio_executavel = os.path.dirname(sys.executable)
    else:
        diretorio_executavel = os.path.dirname(os.path.abspath(__file__))

    return diretorio_executavel

# executa scheda tecnica
def exec_scheda_tec(cod_matrice):
    if valida_cod_matrice(cod_matrice, True) == True:
        return True  # Retorna True se passou na validação da engenharia
    return False  # Retorna False se falhou

# executa rapportino elettronico
def exec_rapp_elettr(cod_matrice):
    if valida_cod_matrice(cod_matrice, True) == True:
        return True  # Retorna True se passou na validação da engenharia
    return False  # Retorna False se falhou