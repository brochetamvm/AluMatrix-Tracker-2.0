import customtkinter as ctk

from util import format_form
from tkinter import messagebox

class FormModific_Rapp_Elettr(ctk.CTkToplevel):    
    def __init__(self, master, matrice, on_save, registro_edicao=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # CONFIGURAÇÕES DA JANELA
        self.cod_matrice = matrice
        self.on_save = on_save
        self.registro_edicao = registro_edicao # Guarda se é uma edição
        self.title(f"Aggiunge nuovo storico - Articolo: {self.cod_matrice}")
        format_form(710, 440, self)     

        # Comportamento de foco e prioridade na tela
        self.transient(master)
        self.lift()
        self.focus_force()
        self.grab_set()
        #########################################################################################################################

        # PANEL PRINCIPAL QUE CONTEM TUDO
        self.pnl_principal = ctk.CTkFrame(self)
        self.pnl_principal.pack(fill="both", expand=True, pady=20, padx=20)

        self.pnl_principal.grid_rowconfigure(0, weight=1)
        self.pnl_principal.grid_rowconfigure(1, weight=2)
        self.pnl_principal.grid_rowconfigure(2, weight=1)
        self.pnl_principal.grid_columnconfigure(0, weight=1)
        #########################################################################################################################

        # PANEL TURNOS
        self.pnl_turno = ctk.CTkFrame(self.pnl_principal, height=10)
        self.pnl_turno.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")  
        
        self.pnl_turno.grid_columnconfigure(0, weight=1)
        self.pnl_turno.grid_columnconfigure(1, weight=1)
        self.pnl_turno.grid_columnconfigure(2, weight=1)

        self.title("Modificare storico" if registro_edicao else f"Aggiunge novo storico - Articolo: {self.cod_matrice}")
        #########################################################################################################################

        # RADIOBOX - OPCAOES DE TURNO 
        self.opcao_selecionada = ctk.StringVar(value="")

        # radiobox turno D
        self.rb_D = ctk.CTkRadioButton(self.pnl_turno, 
                                        text="D", 
                                        font=("", 30, "bold"),
                                        variable=self.opcao_selecionada, 
                                        value="D")
        self.rb_D.grid(row=0, column=0, padx=(50, 25), pady=(10, 0), sticky="nsew")  

        # radiobox turno E
        self.rb_E = ctk.CTkRadioButton(self.pnl_turno, 
                                        text="E", 
                                        font=("", 30, "bold"),
                                        variable=self.opcao_selecionada, 
                                        value="E")
        self.rb_E.grid(row=0, column=1, padx=(25, 25), pady=(10, 0), sticky="nsew")  

        # radiobox turno F
        self.rb_F = ctk.CTkRadioButton(self.pnl_turno, 
                                        text="F", 
                                        font=("", 30, "bold"),
                                        variable=self.opcao_selecionada, 
                                        value="F")
        self.rb_F.grid(row=0, column=2, padx=(25, 50), pady=(10, 0), sticky="nsew")  
        #########################################################################################################################

        # PANEL STORICO
        self.pnl_storico = ctk.CTkFrame(self.pnl_principal)
        self.pnl_storico.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")  

        self.texto = ctk.CTkLabel(self.pnl_storico, text="STORICO:", font=("Consolas", 16, "bold"), anchor="w")
        self.texto.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        self.lbl_storico = ctk.CTkTextbox(self.pnl_storico)
        self.lbl_storico.pack(expand=True, fill="both", padx=10, pady=(5, 10))    
        #########################################################################################################################

        # PANEL BUTTON
        self.pnl_button = ctk.CTkFrame(self.pnl_principal, height=40)
        self.pnl_button.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")  

        self.pnl_button.grid_rowconfigure(0, weight=1)
        self.pnl_button.grid_columnconfigure(0, weight=1)
        self.pnl_button.grid_columnconfigure(1, weight=0) # Coluna do botão OK
        self.pnl_button.grid_columnconfigure(2, weight=0) # Coluna do botão Cancelar
        self.pnl_button.grid_columnconfigure(3, weight=1)
        #########################################################################################################################

        if self.registro_edicao:
            # Preenche o turno e desabilita os RadioButtons para não poder trocar o turno
            self.opcao_selecionada.set(self.registro_edicao["turno"])
            self.rb_D.configure(state="disabled")
            self.rb_E.configure(state="disabled")
            self.rb_F.configure(state="disabled")
            
            # Preenche o campo de texto com o histórico atual
            self.lbl_storico.insert("1.0", self.registro_edicao["storico_antigo"])

        # ACAO BOTAO DE SALVAR
        def click_btn_salvar():
            # Captura os dados preenchidos pelo usuário
            turno_selecionado = self.opcao_selecionada.get()
            historico_digitado = self.lbl_storico.get("1.0", "end-1c").strip() # Pega todo o texto do Textbox

            # Validação básica
            if not turno_selecionado:
                messagebox.showwarning("", "Si prega di informare il turno.", parent=self)
                return
            
            if not historico_digitado:
                messagebox.showwarning("", "Si prega di informare il descritivo.", parent=self)
                return

            # Executa o callback passando os dados de volta para a tela principal
            if hasattr(self, 'registro_edicao') and self.registro_edicao is not None:
                self.on_save(turno_selecionado, historico_digitado, self.registro_edicao)
            else:
                self.on_save(turno_selecionado, historico_digitado)
            self.destroy()
        #########################################################################################################################


        # CRIAR BOTAO SALVAR     
        self.btn_salvar = ctk.CTkButton(self.pnl_button, 
                                        text="OK", 
                                        font=("Consolas", 20, "bold"), 
                                        anchor="center", 
                                        width=150,
                                        command=click_btn_salvar)   
        self.btn_salvar.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") 
        #########################################################################################################################


        # BOTAO DE CANCELAR
        def click_btn_cancelar():
            self.destroy()
        # cria bota cancelar    
        self.btn_cancelar = ctk.CTkButton(self.pnl_button, 
                                          text="Cancelar", 
                                          font=("Consolas", 20, "bold"), 
                                          anchor="center", 
                                          width=150, 
                                          command=click_btn_cancelar,
                                          fg_color="transparent", border_width=1)   
        self.btn_cancelar.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        #########################################################################################################################