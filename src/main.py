# Projeto Rapportino Elettronico
# Info/Fluxo do Projeto
#   - Input codigo da matrice -->>> OK
#   - Pulsante cerca PDF/Disegno tecnico (2 input per path con e senza rete) -->>> OK
#   - Pulsante carica foto incestatura (2 input per path con e senza rete) -->>> OK
#   - Pulsante scheda tecnica -->>> OK
#       > creare la scheda tecnica orientato agli oggetti -->>> OK 
#       > apre un form: per creare/modificare/consultare -->>> OK
#           >> form con tutte i dati di estruzione della matrice -->>> OK
#   - Pulsante Rapportino Elettronico -->>> OK
#       > input TURNO (D/E/F), apre un form: consultare storico (banco de dados), con pulsante creare/modificare -->>> OK
#           >> form con tre grid di storici tutte tre turni -->>> OK 
#           >> creare/modificare: input con un memo per descrivere quello che vuoi -->>> OK

import os
import customtkinter as ctk

from tkinter import filedialog
from util import format_form, carrega_imagem, exec_cerca_PDF, somente_maiusculas, exec_scheda_tec, exec_rapp_elettr, exec_cerca_foto_incestatura, verifica_conexao_server
from frmscheda_tecnica import FormSchedaTecnica
from frmrapp_elettr import FormRappElettr
from url_api import CAMINHO_LOGO, salvar_caminho_logo

ctk.set_default_color_theme("dark-blue")

janela_scheda_ativa = None
janela_rapp_eletr = None

# FORM PRINCIPAL
frmPrincipal = ctk.CTk()
format_form(440, 710, frmPrincipal)
frmPrincipal.title("Rapportino Elettronico")
frmPrincipal.resizable(False, False)
###############################################################################################################################

# PANEL QUE CONTEM TODOS OS COMPONENTES
pnl_principal = ctk.CTkFrame(frmPrincipal)
pnl_principal.pack(fill="both", expand=True, pady=20, padx=20)
###############################################################################################################################

# LOGO IMAGEM
lbl_logo = ctk.CTkLabel(pnl_principal, text="", cursor="hand2")
lbl_logo.pack(pady=20)

# Define o que acontece ao clicar na Label
def ao_clicar_no_logo(event):
    # Abre a janela do Windows para o utilizador escolher a foto
    novo_caminho = filedialog.askopenfilename(title="Seleziona il Logo",
        filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp")])
    
    if novo_caminho:
        # Salva a preferência no config.txt
        salvar_caminho_logo(novo_caminho)
        
        # Atualiza a tela imediatamente sem precisar reiniciar o sistema
        try:
            img_atualizada = carrega_imagem(novo_caminho, 310, 80)
            lbl_logo.configure(image=img_atualizada, text="", height=80)
        except Exception as e:
            print(f"Erro ao carregar nova imagem: {e}")

# Associa o evento do Botão Esquerdo do Mouse ("<Button-1>") à nossa função
lbl_logo.bind("<Button-1>", ao_clicar_no_logo)

# Lógica de inicialização (Quando o programa arranca)
if CAMINHO_LOGO and os.path.exists(CAMINHO_LOGO):
    try:
        logo_img = carrega_imagem(CAMINHO_LOGO, 310, 80)
        lbl_logo.configure(image=logo_img)
    except Exception:
        lbl_logo.configure(text="Logo qui", font=("Consolas", 20, "underline"), text_color="blue", height=120)
else:        
    lbl_logo.configure(text="Logo qui", font=("Consolas", 20, "underline"), text_color="blue", height=120)
###############################################################################################################################

# CODIGO DA MATRIZ - LABEL
lbl_codmatrice = ctk.CTkLabel(pnl_principal, text="Articolo", font=("Consolas", 20, "bold", "italic"), anchor="center")
lbl_codmatrice.pack(padx=100, pady=(40, 0), fill="x")
###############################################################################################################################


# CODIGO MATRICE _ EDIT
edit_matrice = ctk.CTkEntry(pnl_principal, width=320, justify="center", placeholder_text="Articolo", font=("Consolas", 48, "bold"))
edit_matrice.pack()
def key_press_campo(event):
    exec_cerca_PDF(edit_matrice.get())
    atualiza_status("PDF")

edit_matrice.bind("<Return>", key_press_campo) 
somente_maiusculas(edit_matrice)
###############################################################################################################################

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
# para teste
edit_matrice.insert(0, "1PT00001/12")
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

# LABEL SEPARADOR
lbl_sep = ctk.CTkLabel(pnl_principal, text="", font=("", 1))
lbl_sep.pack(padx=0, pady=0)
###############################################################################################################################

# PANEL COM DOIS BOTOES
pnl_button = ctk.CTkFrame(pnl_principal)
pnl_button.pack()
###############################################################################################################################

# LABEL RODAPE CRIA
lbl_rodape = ctk.CTkLabel(frmPrincipal, text="  Verificando connessione...", font=("Consolas", 13, "bold", "italic"), anchor="w")
lbl_rodape.pack(side="bottom", fill="x")
# Esta é a função de comunicacao que a Thread vai chamar quando terminar de testar a rede
def atualizar_label_status(caminho, status_texto):
    lbl_rodape.configure(text="  " + status_texto)
def atualiza_status(tipo):
    verifica_conexao_server(tipo, atualizar_label_status)
atualiza_status("pdf")
###############################################################################################################################

# BOTAO DE PROCURAR PDF/DESENHO TECNICO   
def click_btn_pdf():
    exec_cerca_PDF(edit_matrice.get()) 
    atualiza_status("pdf")
btn_pdf = ctk.CTkButton(pnl_button, text="Cerca Disegno Tecnico", font=("Consolas", 22, "bold"), 
                        anchor="center", height=60, width=300, command=click_btn_pdf)
btn_pdf.pack(padx=10, pady=10, fill="x")
###############################################################################################################################

# BOTAO DE PROCURAR FOTO INCESTATURA
def click_btn_foto_incestatura():
    exec_cerca_foto_incestatura(edit_matrice.get()) 
    atualiza_status("fotos")
btn_foto_incestatura = ctk.CTkButton(pnl_button, text="Foto Incestatura", font=("Consolas", 22, "bold"), 
                        anchor="center", height=60, width=300, command=click_btn_foto_incestatura)
btn_foto_incestatura.pack(padx=10, pady=10, fill="x")
###############################################################################################################################

# BOTAO DE PROCURAR SCHEDA TECNICA
def click_btn_scheda_tec():
    global janela_scheda_ativa 
    # Primeiro executa a regra de validação que está dentro do seu util.py
    if exec_scheda_tec(edit_matrice.get()):
        # Se passou na validação, verifica se a janela já não está aberta na tela
        if janela_scheda_ativa is not None and janela_scheda_ativa.winfo_exists():
            janela_scheda_ativa.lift()
            janela_scheda_ativa.focus_force()
        else:
            # Abre o formulário OO passando o código validado
            janela_scheda_ativa = FormSchedaTecnica(master=frmPrincipal, 
                                                    matrice=edit_matrice.get())
                        
btn_scheda_tec = ctk.CTkButton(pnl_button, text="Scheda Tecnica", font=("Consolas", 22, "bold"), 
                               anchor="center", height=60, width=300, command=click_btn_scheda_tec)
btn_scheda_tec.pack(padx=10, pady=10, fill="x")
###############################################################################################################################

# BOTAO DE RAPPORTINO ELETTRONICO
def click_btn_rapp_elettr():
    global janela_rapp_eletr
    # Primeiro executa a regra de validação que está dentro do seu util.py
    if exec_rapp_elettr(edit_matrice.get()):
        # Se passou na validação, verifica se a janela já não está aberta na tela
        if janela_rapp_eletr is not None and janela_rapp_eletr.winfo_exists():
            janela_rapp_eletr.lift()
            janela_rapp_eletr.focus_force()
        else:
            # Abre o formulário OO passando o código validado
            janela_rapp_eletr = FormRappElettr(master=frmPrincipal, 
                                               matrice=edit_matrice.get())    
btn_rapp_elettr = ctk.CTkButton(pnl_button, text="Rapportino Elettronico", font=("Consolas", 22, "bold"), 
                               anchor="center", height=60, width=300, command=click_btn_rapp_elettr)
btn_rapp_elettr.pack(padx=10, pady=10, fill="x")
###############################################################################################################################

# FOCUS NO PRIMEIRO CAMPO
frmPrincipal.after(70, lambda: edit_matrice.focus_set())
###############################################################################################################################

# EXECUCAO FORM PRINCIPAL
frmPrincipal.mainloop()
###############################################################################################################################