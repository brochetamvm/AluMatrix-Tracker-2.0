# file per func utilitarias
import os
import sys
import customtkinter as ctk
import requests
import threading
import tempfile

from tkinter import messagebox
from PIL import Image
from pathlib import Path
from url_api import API_URL


# FORMATA FORM
def format_form(frm_l, frm_a, frm_self):
    # Defina o tamanho que você quer para ESTA janela
    largura_janela = frm_l
    altura_janela = frm_a
    
    # Descubra a largura e altura total da tela do usuário
    largura_tela = frm_self.winfo_screenwidth()
    altura_tela = frm_self.winfo_screenheight()
    
    # Calcule a posição X e Y para a janela ficar no centro
    posicao_x = int((largura_tela / 2) - (largura_janela / 2) + 100)
    posicao_y = int((altura_tela / 2) - (altura_janela / 2))
    
    # Aplique a geometria no formato: "LARGURAxALTURA+X+Y"
    frm_self.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
####################################################################################################################


# CARREGAR IMAGEM EM UM LABEL
def carrega_imagem(path_img, largura, altura):
    return ctk.CTkImage(
            light_image=Image.open(path_img),
            dark_image=Image.open(path_img),
            size=(largura, altura))
####################################################################################################################


# CONVERTER MINUSCALAS EM LETRAS MAIUSCULAS
def somente_maiusculas(campo):
    def converter(event):
        texto = campo.get().upper()
        posicao = campo.index("insert")
        campo.delete(0, "end")
        campo.insert(0, texto)
        campo.icursor(posicao)

    campo.bind("<KeyRelease>", converter) 
####################################################################################################################


# EXECUTA SCHEDA TECNICA
def exec_scheda_tec(cod_matrice):
    if valida_cod_matrice(cod_matrice, True) == True:
        return True  # Retorna True se passou na validação da engenharia
    return False  # Retorna False se falhou
####################################################################################################################


# EXECUTA RAPPORTINO ELETTRONICO
def exec_rapp_elettr(cod_matrice):
    if valida_cod_matrice(cod_matrice, True) == True:
        return True  # Retorna True se passou na validação da engenharia
    return False  # Retorna False se falhou    
####################################################################################################################
    
# VALIDA CAMPO CODIGO MATRICE
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
####################################################################################################################


# EXECUTA PROCURA DO PDF/DESENHO TECNICO
def exec_cerca_PDF(cod_matrice):   
    encontrou = False

    if valida_cod_matrice(cod_matrice, False) == True:        
        codigo = cod_matrice[:8]
        
        # Tentar baixar do servidor (api)
        try:
            # Bate na futura porta da API que vamos criar
            resposta = requests.get(f"{API_URL}/arquivos/pdf/{codigo}", timeout=3)
            
            if resposta.status_code == 200:
                # Cria um caminho seguro na pasta temporária do Windows
                caminho_temp = os.path.join(tempfile.gettempdir(), f"{codigo}.pdf")
                
                # Escreve os bytes baixados (wb = write binary) no arquivo local
                with open(caminho_temp, 'wb') as arquivo_pdf:
                    arquivo_pdf.write(resposta.content)
                
                # Manda o Windows abrir o arquivo físico
                os.startfile(caminho_temp)
                return True
                
        except requests.exceptions.RequestException:
            pass # Se a API estiver desligada, ignora o erro
            
        # Buscar na pasta local (offline)
        if getattr(sys, 'frozen', False):
            dir_base = os.path.dirname(sys.executable)
        else:
            dir_base = os.path.dirname(os.path.abspath(__file__))
            
        dir_local = Path(dir_base) / "PDF"
        
        if dir_local.is_dir():
            arquivo = dir_local / f"{codigo}.pdf"
            if arquivo.exists() and arquivo.is_file():         
                os.startfile(arquivo)
                encontrou = True  
            else:
                messagebox.showwarning("Attenzione!", f"Articolo [{codigo}] non trovato!\n\n[{arquivo}]") 
        else:
            messagebox.showwarning("Errore", "Server offline e cartella locale non trovata!")
          
    return encontrou
####################################################################################################################


# EXECUTA PROCURA FOTO INCESTATURA
def exec_cerca_foto_incestatura(cod_matrice):   
    encontrou = False

    if valida_cod_matrice(cod_matrice, False) == True:        
        codigo = cod_matrice[:8]
        
        # Tentar baixar do servidor (api)
        try:
            # Bate na futura porta da API que vamos criar
            resposta = requests.get(f"{API_URL}/arquivos/fotos/{codigo}", timeout=3)
            
            if resposta.status_code == 200:
                # Cria um caminho seguro na pasta temporária do Windows
                caminho_temp = os.path.join(tempfile.gettempdir(), f"{codigo}.jpg")
                
                # Escreve os bytes baixados (wb = write binary) no arquivo local
                with open(caminho_temp, 'wb') as arquivo_pdf:
                    arquivo_pdf.write(resposta.content)
                
                # Manda o Windows abrir o arquivo físico
                os.startfile(caminho_temp)
                return True
                
        except requests.exceptions.RequestException:
            pass # Se a API estiver desligada, ignora o erro
            
        # Buscar na pasta local (offline)
        if getattr(sys, 'frozen', False):
            dir_base = os.path.dirname(sys.executable)
        else:
            dir_base = os.path.dirname(os.path.abspath(__file__))
            
        dir_local = Path(dir_base) / "FOTOS"
        
        if dir_local.is_dir():
            arquivo = dir_local / f"{codigo}.jpg"
            if arquivo.exists() and arquivo.is_file():         
                os.startfile(arquivo)
                encontrou = True  
            else:
                messagebox.showwarning("Attenzione!", f"Articolo [{codigo}] non trovato!\n\n[{arquivo}]") 
        else:
            messagebox.showwarning("Errore", "Server offline e cartella locale non trovata!")
          
    return encontrou
####################################################################################################################


# VERIFICA CONEXAO COM O SERVIDOR, SENAO PEGA DADOS (PDF/FOTOS) LOCAIS 
def verifica_conexao_server(tipo, funcao_retorno):
    def verifica_background():
        try:
            # Tenta bater no servidor com um timeout curto (2 segundos)
            resposta = requests.get(f"{API_URL}/{tipo}", timeout=2)
            
            # Se não deu erro, o servidor está vivo
            if resposta.status_code == 200 or resposta.status_code == 404: 
                status = "[Status: SERVER]"
                caminho = "API" # Marcador para sabermos que devemos baixar o arquivo
                
        except requests.exceptions.RequestException:
            # O servidor está offline. Vamos usar o modo local.
            if getattr(sys, 'frozen', False):
                diretorio_executavel = os.path.dirname(sys.executable)
            else:
                diretorio_executavel = os.path.dirname(os.path.abspath(__file__))
            
            caminho_local = Path(diretorio_executavel) / tipo
            caminho = caminho_local

            if not caminho_local.is_dir():
                status = "[Status: ERRORE - DIR LOCALE]"
            else:
                status = "[Status: LOCALE]"

        # Usa o "telefone" para mandar os dados de volta para o main.py
        if funcao_retorno:
            funcao_retorno(caminho, status)
    
    # Dispara a thread em background
    thread_verificacao = threading.Thread(target=verifica_background, daemon=True)
    thread_verificacao.start()
    ####################################################################################################################