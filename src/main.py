# Projeto Rapportino Elettronico Alexia
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

from util import format_form, carrega_imagem, exec_cerca_PDF, somente_maiusculas, exec_scheda_tec, exec_rapp_elettr, exec_cerca_foto_incestatura, ler_json_path
from frmscheda_tecnica import FormSchedaTecnica
from frmrapp_elettr import FormRappElettr

ctk.set_default_color_theme("dark-blue")

janela_scheda_ativa = None
janela_rapp_eletr = None

# FORM PRINCIPAL
frmPrincipal = ctk.CTk()
format_form(440, 710, frmPrincipal)
frmPrincipal.title("Rapportino Elettronico")
caminho_icone = os.path.join(os.path.dirname(__file__), "imagens", "logo_alexia.ico")
frmPrincipal.iconbitmap(caminho_icone)
frmPrincipal.resizable(False, False)

# panel que contem todos os componentes
pnl_principal = ctk.CTkFrame(frmPrincipal)
pnl_principal.pack(fill="both", expand=True, pady=20, padx=20)

# titulo - imagem
logo_img = carrega_imagem(r"src\imagens\logo.png", 310, 65)
lbl_titulo = ctk.CTkLabel(pnl_principal, image=logo_img, text="")
lbl_titulo.pack(pady=50)

# codigo da matriz - label
lbl_codmatrice = ctk.CTkLabel(pnl_principal, text="Articolo", font=("Consolas", 20, "bold", "italic"), anchor="center")
lbl_codmatrice.pack(padx=100, fill="x")

# codigo matrice _ edit
edit_matrice = ctk.CTkEntry(pnl_principal, width=320, justify="center", placeholder_text="Articolo", font=("Consolas", 48, "bold"))
edit_matrice.pack()
def key_press_campo(event):
    exec_cerca_PDF(edit_matrice.get())
    atualiza_status("PDF")

edit_matrice.bind("<Return>", key_press_campo) 
somente_maiusculas(edit_matrice)

# para teste
#edit_matrice.insert(0, "3DI12345/1")

# label separador
lbl_sep = ctk.CTkLabel(pnl_principal, text="", font=("", 1))
lbl_sep.pack(padx=0, pady=0)

# Panel com dois botoes
pnl_button = ctk.CTkFrame(pnl_principal)
pnl_button.pack()

# label rodape cria
lbl_rodape = ctk.CTkLabel(frmPrincipal, text="", font=("Consolas", 13, "bold", "italic"), anchor="w")
lbl_rodape.pack(side="bottom", fill="x")
def atualiza_status(tipo):
    status1, status2 = ler_json_path(tipo)
    lbl_rodape.configure(text="  "+status2)
atualiza_status("PDF")

# Botao de procurar PDF/Desenho Tecnico   
def click_btn_pdf():
    exec_cerca_PDF(edit_matrice.get()) 
    atualiza_status("PDF")
btn_pdf = ctk.CTkButton(pnl_button, text="Cerca Disegno Tecnico", font=("Consolas", 22, "bold"), 
                        anchor="center", height=60, width=300, command=click_btn_pdf)
btn_pdf.pack(padx=10, pady=10, fill="x")

# Botao de procurar foto incestatura
def click_btn_foto_incestatura():
    exec_cerca_foto_incestatura(edit_matrice.get()) 
    atualiza_status("FOTO")
btn_foto_incestatura = ctk.CTkButton(pnl_button, text="Foto Incestatura", font=("Consolas", 22, "bold"), 
                        anchor="center", height=60, width=300, command=click_btn_foto_incestatura)
btn_foto_incestatura.pack(padx=10, pady=10, fill="x")

# Botao de procurar scheda tecnica
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
            janela_scheda_ativa = FormSchedaTecnica(
                master=frmPrincipal, matrice=edit_matrice.get())
            
btn_scheda_tec = ctk.CTkButton(pnl_button, text="Scheda Tecnica", font=("Consolas", 22, "bold"), 
                               anchor="center", height=60, width=300, command=click_btn_scheda_tec)
btn_scheda_tec.pack(padx=10, pady=10, fill="x")

# Botao de rapportino elettronico
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
            janela_rapp_eletr = FormRappElettr(master=frmPrincipal, matrice=edit_matrice.get())
    
btn_rapp_elettr = ctk.CTkButton(pnl_button, text="Rapportino Elettronico", font=("Consolas", 22, "bold"), 
                               anchor="center", height=60, width=300, command=click_btn_rapp_elettr)
btn_rapp_elettr.pack(padx=10, pady=10, fill="x")

# focus no primeiro campo
frmPrincipal.after(70, lambda: edit_matrice.focus_set())

# execucao form principal
frmPrincipal.mainloop()