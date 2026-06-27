import os
import json
import inspect
import customtkinter as ctk
import threading
import requests

from enum import Enum
from tkinter import messagebox, filedialog
from PIL import Image
from scheda_tecnica import TipoLega
from url_api import API_URL

# CLASSE DE COMPONENTE DE TELA - PAINEIS QUE ABREM E FECHANDO QUANDO CLICA
class CartaoExpandivel(ctk.CTkFrame):
    def __init__(self, master, titulo, **kwargs):
        super().__init__(master, **kwargs)
        self.aberto = False
        self.configure(fg_color="#1e1e1e", border_width=1, border_color="#333333")

        self.frame_cabecalho = ctk.CTkFrame(self, fg_color="#2b2b2b", height=50, cursor="hand2")
        self.frame_cabecalho.pack(fill="x", padx=2, pady=2)
        self.frame_cabecalho.pack_propagate(False)
        self.frame_cabecalho.bind("<Button-1>", self.alternar_expansao)

        self.lbl_titulo = ctk.CTkLabel(self.frame_cabecalho, text=titulo, font=("Consolas", 15, "bold"))
        self.lbl_titulo.pack(side="left", padx=20)
        self.lbl_titulo.bind("<Button-1>", self.alternar_expansao)

        self.lbl_seta = ctk.CTkLabel(self.frame_cabecalho, text="▼", font=("Consolas", 14))
        self.lbl_seta.pack(side="right", padx=20)
        self.lbl_seta.bind("<Button-1>", self.alternar_expansao)

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")

    def alternar_expansao(self, event=None):
        if self.aberto:
            self.frame_conteudo.pack_forget()
            self.lbl_seta.configure(text="▼")
            self.aberto = False
        else:
            self.frame_conteudo.pack(fill="x", padx=15, pady=15, after=self.frame_cabecalho)
            self.lbl_seta.configure(text="▲")
            self.aberto = True
#########################################################################################################################            


# CLASSE FICHA TECNICA - TELA
class FormSchedaTecnica(ctk.CTkToplevel):
    def __init__(self, master, matrice, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # CONFIG TELA
        self.cod_matrice = matrice

        self.banco_completo = {}
        self.ligas_cadastradas = []
        self.indice_liga_atual = 0
        self.liga_selecionada = ""
        self.modo_insercao = False  
        self.carregando_dados = False  

        self.inputs = {}          
        self.dados_originais = {} 

        self.title(f"Scheda Tecnica - Articolo: {self.cod_matrice}")
        self.state("zoomed")
        self.transient(master)
        ##############################################################

        # CRIACAO DA TELA DA BARRA DE PROGRESSO
        self.pnl_loading = ctk.CTkFrame(self, fg_color="transparent")
        self.pnl_loading.pack(expand=True, fill="both")
        self.lbl_loading = ctk.CTkLabel(self.pnl_loading, text="Caricamento dei dati...", font=("Consolas", 18))
        self.lbl_loading.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.pnl_loading, mode="indeterminate", width=500)
        self.progress_bar.pack(pady=5)        
        self.progress_bar.start()

        # 200 milissegundos para desenhar o Loading na tela e só depois faz trabalho pesado.
        self.after(200, self.carrega_tela) 
    #########################################################################################################################

    
    # INICIA THREAD PARA O CARREGAMENTO DA TELA
    def carrega_tela(self):
        # Disparamos uma thread para ler o ficheiro SEM bloquear a tela
        threading.Thread(target=self._processo_carregamento_thread, daemon=True).start()    
    #########################################################################################################################


    # FAZ O CARREGAMENTO DO JSON EM BACKGROUND
    def _processo_carregamento_thread(self):
        self.carregar_dados_do_json()
        
        # 2. Volta para o Thread Principal para desenhar os componentes
        self.after(0, self._finalizar_renderizacao)    
    #########################################################################################################################


    # TERMINA DE MONTAR A TELA
    def _finalizar_renderizacao(self):
        self.pnl_conteudo = ctk.CTkFrame(self, fg_color="transparent")

        # cabecalho
        self.pnl_topo = ctk.CTkFrame(self.pnl_conteudo, fg_color="transparent")
        self.pnl_topo.pack(fill="x", padx=20, pady=(15, 5))
        self.lbl_titulo = ctk.CTkLabel(self.pnl_topo, text=f"Scheda Tecnica - Articolo: {self.cod_matrice}", font=("Consolas", 24, "bold"))
        self.lbl_titulo.pack(side="left")

        self.pnl_navegacao = ctk.CTkFrame(self.pnl_topo, fg_color="transparent")
        self.pnl_navegacao.pack(side="right")
        self.combo_lega = ctk.CTkComboBox(self.pnl_navegacao, width=180, font=("Consolas", 13), state="readonly", command=self._mudanca_manual_combo)
        self.combo_lega.pack(side="left", padx=5)
        self.btn_ant = ctk.CTkButton(self.pnl_navegacao, text="◀", width=35, command=self.registro_anterior)
        self.btn_ant.pack(side="left", padx=2)
        self.lbl_contador = ctk.CTkLabel(self.pnl_navegacao, text="0/0", font=("Consolas", 13, "bold"), width=40)
        self.lbl_contador.pack(side="left", padx=3)
        self.btn_prox = ctk.CTkButton(self.pnl_navegacao, text="▶", width=35, command=self.proximo_registro)
        self.btn_prox.pack(side="left", padx=2)
        self.btn_novo = ctk.CTkButton(self.pnl_navegacao, text="＋", width=35, fg_color="#2b7337", command=self.preparar_nova_lega)
        self.btn_novo.pack(side="left", padx=(10, 2))

        # corpo
        self.scroll_principal = ctk.CTkScrollableFrame(self.pnl_conteudo)
        self.scroll_principal.pack(fill="both", expand=True, padx=20, pady=10)

        # rodape
        self.pnl_acoes = ctk.CTkFrame(self.pnl_conteudo, fg_color="transparent")
        self.pnl_acoes.pack(fill="x", side="bottom", pady=(0, 70), padx=20)
        self.btn_salvar = ctk.CTkButton(self.pnl_acoes, text="Salva i dati", font=("Consolas", 16, "bold"), height=40, state="disabled", command=self.salvar_dados)
        self.btn_salvar.pack(side="right")

        self.renderizar_formulario_recursivo()        
        self.sincronizar_navegacao_lega()
        self.update_idletasks()
        self.atualizar_valores_tela()

        # destroi tela de barra de progresso
        try:
            self.progress_bar.stop()
            self.pnl_loading.destroy()
        except:
            pass
            
        self.pnl_conteudo.pack(fill="both", expand=True)
        self.grab_set()
    #########################################################################################################################


    # FAZ REQUISICAO AO SERVER DE TODOS OS DADOS DAS FICHAS
    def carregar_dados_do_json(self):
        try:
            # Tenta buscar do servidor
            resposta = requests.get(f"{API_URL}/scheda", timeout=5)
            if resposta.status_code == 200:
                self.banco_completo = resposta.json()
            else:
                raise Exception("Erro no servidor")
        except:
            #messagebox.showwarning("Modo Offline", "Não foi possível conectar ao servidor.")
            self.banco_completo = {}
            
        self.ligas_cadastradas = [c.split("|")[1] for c in self.banco_completo.keys() if c.startswith(f"{self.cod_matrice}|")]
    #########################################################################################################################


    #
    def sincronizar_navegacao_lega(self):
        if not self.ligas_cadastradas and not self.modo_insercao: self.modo_insercao = True
        if self.modo_insercao:
            ligas_livres = [l.value for l in TipoLega if l.value not in self.ligas_cadastradas]
            self.combo_lega.configure(values=ligas_livres, state="readonly")
            self.combo_lega.set(ligas_livres[0]); self.liga_selecionada = ligas_livres[0]
            self.lbl_contador.configure(text="New")
            self.btn_ant.configure(state="disabled"); self.btn_prox.configure(state="disabled"); self.btn_novo.configure(state="disabled")
            self.dados_originais = {}
        else:
            self.btn_novo.configure(state="normal")
            if self.ligas_cadastradas:
                self.combo_lega.configure(values=self.ligas_cadastradas, state="readonly")
                self.liga_selecionada = self.ligas_cadastradas[self.indice_liga_atual]
                self.combo_lega.set(self.liga_selecionada)
                self.btn_ant.configure(state="normal"); self.btn_prox.configure(state="normal")
                self.lbl_contador.configure(text=f"{self.indice_liga_atual+1}/{len(self.ligas_cadastradas)}")
                self.dados_originais = self.banco_completo.get(f"{self.cod_matrice}|{self.liga_selecionada}", {})
    #########################################################################################################################                


    #
    def _obter_valor_widget(self, escopo, campo):
        ref = self.inputs[escopo][campo]
        if isinstance(ref, ctk.StringVar): return ref.get()
        if isinstance(ref, ctk.CTkTextbox): return ref.get("1.0", "end-1c").strip()
        return ""
    #########################################################################################################################


    #
    def atualizar_valores_tela(self):
        self.carregando_dados = True
        
        for escopo, campos in self.inputs.items():
            dados = self.dados_originais.get(escopo, {})
            classe = self._obter_classe_por_escopo(escopo)
            sig = inspect.signature(classe.__init__) if classe else None

            for campo, ref in campos.items():
                val = dados.get(campo)
                
                if escopo == "principal" and campo == "matrice": txt = self.cod_matrice
                elif escopo == "principal" and campo == "lega": txt = self.liga_selecionada
                else:
                    tipo = sig.parameters[campo].annotation if (sig and campo in sig.parameters) else str
                    if tipo == bool: txt = "True" if val is True else "False"
                    else: txt = str(val) if val is not None else ""

                if isinstance(ref, ctk.StringVar): ref.set(txt)
                elif isinstance(ref, ctk.CTkTextbox): ref.delete("1.0", "end"); ref.insert("1.0", txt)
        
        path_atual = self.inputs["principal"]["disegno_tec"].get()
        self._atualizar_preview_imagem(path_atual)

        self.btn_salvar.configure(state="normal" if self.modo_insercao else "disabled")
        self.carregando_dados = False
    #########################################################################################################################    


    #
    def _atualizar_preview_imagem(self, caminho):
        try:
            if not caminho or len(caminho.strip()) < 4:
                self.btn_imagem.configure(image=None, text="CLICCA PER CARICARE DISEGNO\n(Nessuna Immagine)", fg_color="transparent", border_width=1)
                self.btn_imagem.image = None
                return
                
            caminho_nativo = os.path.normpath(caminho.strip())

            if caminho_nativo.lower().endswith(".pdf"):
                self.btn_imagem.configure(image=None, text=f"DOCUMENTO PDF ALLEGATO:\n\n{os.path.basename(caminho_nativo)}\n\n(Impossibile mostrare l'anteprima)", fg_color="transparent", border_width=1)
                self.btn_imagem.image = None
                return

            if not os.path.exists(caminho_nativo):
                self.btn_imagem.configure(image=None, text=f"FILE NON TROVATO:\n\n{caminho_nativo}", fg_color="transparent", border_width=1)
                self.btn_imagem.image = None
                return

            img_pil = Image.open(caminho_nativo)
            img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(520, 400))
            
            # BLINDAGEM SÊNIOR: Desativa as propriedades cinzas do botão e força a renderização atômica
            self.btn_imagem.configure(image=img_ctk, text="", fg_color="transparent", border_width=0, hover=False)
            self.btn_imagem.image = img_ctk 
            
            # Força o motor gráfico do customtkinter a redesenhar as texturas internas imediatamente
            self.btn_imagem._draw()
        except Exception as e:
            self.btn_imagem.configure(image=None, text=f"ERRORE FORMATO IMMAGINE:\n\n{str(e)}", fg_color="transparent", border_width=1)
            self.btn_imagem.image = None
    #########################################################################################################################            


    #
    def _view_layout_refresh(self):
        # Callback auxiliar para reajustar o canvas caso a janela mude de estado
        path_atual = self.inputs["principal"]["disegno_tec"].get()
        self._atualizar_preview_imagem(path_atual)
    #########################################################################################################################    


    #
    def _selecionar_imagem(self):
        path = filedialog.askopenfilename(filetypes=[("Immagini standard", "*.png *.jpg *.jpeg *.bmp"), ("Tutti i file", "*.*")])
        if path:
            path_limpo = os.path.normpath(path)
            self.inputs["principal"]["disegno_tec"].set(path_limpo)
            self._atualizar_preview_imagem(path_limpo)
            self.verificar_alteracoes()
    #########################################################################################################################                        


    #
    def renderizar_formulario_recursivo(self):
        from scheda_tecnica import scheda_tecnica
        
        # geral
        card_geral = CartaoExpandivel(self.scroll_principal, titulo="PRESSA")
        card_geral.pack(fill="x", padx=10, pady=5)
        card_geral.alternar_expansao()

        frame_esquerda = ctk.CTkFrame(card_geral.frame_conteudo, fg_color="transparent")
        frame_esquerda.pack(side="left", fill="both", expand=True)

        frame_direita = ctk.CTkFrame(card_geral.frame_conteudo, fg_color="#121212", width=520, height=400)
        frame_direita.pack(side="right", padx=(70, 0), pady=5)
        frame_direita.pack_propagate(False)

        self.btn_imagem = ctk.CTkButton(frame_direita, text="CARICA DISEGNO", fg_color="transparent", 
                                        border_width=1, border_color="#444", hover_color="#2b2b2b",
                                        width=520, height=400, image=None, command=self._selecionar_imagem)
        self.btn_imagem.place(relx=0.5, rely=0.5, anchor="center")

        self.inputs["principal"] = {}
        sig = inspect.signature(scheda_tecnica.__init__)
        
        int_row, int_col = 0, 0
        for nome, param in sig.parameters.items():
            if nome == "self": continue
            
            if nome == "disegno_tec":
                var_img = ctk.StringVar()
                self.inputs["principal"][nome] = var_img
                continue

            ref, int_row, int_col = self._criar_widget_dinamico(frame_esquerda, nome, param.annotation, None, int_row, int_col)
            
            if nome in ["matrice", "lega"]:
                todos_filhos = frame_esquerda.winfo_children()
                if todos_filhos:
                    ultimo_widget = todos_filhos[-1]
                    if isinstance(ultimo_widget, (ctk.CTkEntry, ctk.CTkComboBox)):
                        ultimo_widget.configure(state="disabled")

            self.inputs["principal"][nome] = ref
            self.update()

        # o resto
        subclasses = inspect.getmembers(scheda_tecnica, inspect.isclass)
        for nome_sub, classe_sub in subclasses:
            if not classe_sub.__qualname__.startswith("scheda_tecnica."): continue
            card = CartaoExpandivel(self.scroll_principal, titulo=nome_sub.replace("_", " ").upper())
            card.pack(fill="x", padx=10, pady=5)
            self._processar_nivel_classe(classe_sub, card.frame_conteudo, escopo_pai=nome_sub)
    #########################################################################################################################


    #
    def _processar_nivel_classe(self, classe, container, escopo_pai):
        self.inputs[escopo_pai] = {}
        frame_inputs = ctk.CTkFrame(container, fg_color="transparent")
        frame_inputs.pack(fill="x", padx=10, pady=5)
        
        sig = inspect.signature(classe.__init__)
        int_row, int_col = 0, 0
        for nome, param in sig.parameters.items():
            if nome == "self": continue
            ref, int_row, int_col = self._criar_widget_dinamico(frame_inputs, nome, param.annotation, None, int_row, int_col)
            self.inputs[escopo_pai][nome] = ref
            self.update()

        subclasses = inspect.getmembers(classe, inspect.isclass)
        for n_sub, c_sub in subclasses:
            if not c_sub.__qualname__.startswith(classe.__qualname__ + "."): continue
            card_sub = ctk.CTkFrame(container, border_width=1, border_color="#333", fg_color="#252525")
            card_sub.pack(fill="x", padx=10, pady=10)
            ctk.CTkLabel(card_sub, text=n_sub.upper(), font=("Consolas", 13, "bold")).pack(anchor="w", padx=10, pady=5)
            grid_sub = ctk.CTkFrame(card_sub, fg_color="transparent")
            grid_sub.pack(fill="both", expand=True, padx=5, pady=5)
            self._processar_nivel_classe(c_sub, grid_sub, f"{escopo_pai}.{n_sub}")
    #########################################################################################################################            


    #
    def _criar_widget_dinamico(self, frame, nome_param, tipo_esperado, valor_json, int_row, int_col):
        if nome_param == "oss" or nome_param.startswith("oss_"):
            if int_col == 2: int_row += 1; int_col = 0
            lbl = ctk.CTkLabel(frame, text=nome_param.replace("_", " ").title() + ":", font=("Consolas", 13, "bold"))
            lbl.grid(row=int_row, column=0, padx=8, pady=5, sticky="ne")
            textbox = ctk.CTkTextbox(frame, width=380, height=65, font=("Consolas", 12))
            textbox.grid(row=int_row, column=1, columnspan=3, padx=8, pady=5, sticky="w")
            textbox.bind("<KeyRelease>", lambda e: self.verificar_alteracoes())
            return textbox, int_row + 1, 0

        var = ctk.StringVar()
        lbl = ctk.CTkLabel(frame, text=nome_param.replace("_", " ").title() + ":", font=("Consolas", 13))
        lbl.grid(row=int_row, column=int_col, padx=8, pady=5, sticky="e")

        if tipo_esperado == bool:
            widget = ctk.CTkCheckBox(frame, text="", variable=var, onvalue="True", offvalue="False")
        elif inspect.isclass(tipo_esperado) and issubclass(tipo_esperado, Enum):
            widget = ctk.CTkComboBox(frame, values=[str(e.value) for e in tipo_esperado], variable=var, width=160, state="readonly")
        elif tipo_esperado == int or tipo_esperado == float: 
            widget = ctk.CTkEntry(frame, width=60, textvariable=var)
        else:
            widget = ctk.CTkEntry(frame, width=160, textvariable=var)

        widget.grid(row=int_row, column=int_col + 1, padx=8, pady=5, sticky="w")
        var.trace_add("write", self.verificar_alteracoes)
        
        int_col += 2
        if int_col >= 4: int_col = 0; int_row += 1
        return var, int_row, int_col
    #########################################################################################################################


    #
    def _obter_classe_por_escopo(self, escopo):
        from scheda_tecnica import scheda_tecnica
        if escopo == "principal": return scheda_tecnica
        classe = scheda_tecnica
        try:
            for parte in escopo.split('.'): classe = getattr(classe, parte)
            return classe
        except: return None
    #########################################################################################################################


    #
    def verificar_alteracoes(self, *args):
        if self.carregando_dados: return
        if self.modo_insercao:
            self.btn_salvar.configure(state="normal")
            return

        alterado = False
        for escopo, campos in self.inputs.items():
            dados_orig = self.dados_originais.get(escopo, {})
            classe = self._obter_classe_por_escopo(escopo)
            sig = inspect.signature(classe.__init__) if classe else None
            for campo, ref in campos.items():
                atual = self._obter_valor_widget(escopo, campo)
                json_v = dados_orig.get(campo)
                
                if escopo == "principal" and campo in ["matrice", "lega"]: continue

                tipo = sig.parameters[campo].annotation if (sig and campo in sig.parameters) else str
                orig_str = ("True" if json_v is True else "False") if tipo == bool else (str(json_v) if json_v is not None else "")
                if atual != orig_str: alterado = True; break
            if alterado: break

        self.btn_salvar.configure(state="normal" if alterado else "disabled")
        self.combo_lega.configure(state="disabled" if alterado else "readonly")
        self.btn_ant.configure(state="disabled" if alterado else "normal")
        self.btn_prox.configure(state="disabled" if alterado else "normal")
        self.btn_novo.configure(state="disabled" if alterado else "normal")
    #########################################################################################################################


    #
    def registro_anterior(self):
        self.indice_liga_atual = (self.indice_liga_atual - 1) % len(self.ligas_cadastradas)
        self.sincronizar_navegacao_lega(); self.atualizar_valores_tela()
    #########################################################################################################################        


    #
    def proximo_registro(self):
        self.indice_liga_atual = (self.indice_liga_atual + 1) % len(self.ligas_cadastradas)
        self.sincronizar_navegacao_lega(); self.atualizar_valores_tela()
    #########################################################################################################################


    #
    def _mudanca_manual_combo(self, escolha):
        if self.modo_insercao: self.liga_selecionada = escolha; self.atualizar_valores_tela()
        elif escolha in self.ligas_cadastradas:
            self.indice_liga_atual = self.ligas_cadastradas.index(escolha)
            self.sincronizar_navegacao_lega(); self.atualizar_valores_tela()
    #########################################################################################################################


    # 
    def preparar_nova_lega(self):
        self.modo_insercao = True; self.sincronizar_navegacao_lega(); self.atualizar_valores_tela()
    #########################################################################################################################


    # ACAO DO BOTAO SALVAR DADOS 
    def salvar_dados(self):
        try:
            dados_finais = {}
            for escopo, campos in self.inputs.items():
                dados_finais[escopo] = {}
                classe = self._obter_classe_por_escopo(escopo)
                sig = inspect.signature(classe.__init__) if classe else None
                for campo, ref in campos.items():
                    val_str = self._obter_valor_widget(escopo, campo)
                    
                    if escopo == "principal" and campo == "matrice": val_str = self.cod_matrice
                    elif escopo == "principal" and campo == "lega": val_str = self.liga_selecionada

                    tipo = sig.parameters[campo].annotation if (sig and campo in sig.parameters) else str
                    if tipo == bool: val = True if val_str == "True" else False
                    elif tipo == int: val = int(val_str) if val_str else 0
                    elif tipo == float: val = float(val_str) if val_str else 0.0
                    else: val = val_str
                    dados_finais[escopo][campo] = val
            
            # Atualiza o banco local antes de enviar
            chave_final = f"{self.cod_matrice}|{self.liga_selecionada}"
            self.banco_completo[chave_final] = dados_finais
            
            # ENVIO PARA A API
            resposta = requests.post(f"{API_URL}/scheda/salvar", json=self.banco_completo, timeout=10)
            
            if resposta.status_code == 200:
                messagebox.showinfo("Sucesso", "Dados salvos no servidor!")
                self.modo_insercao = False
            else:
                raise Exception(f"Servidor retornou erro: {resposta.status_code}")
            
            # Recarrega a tela para refletir as mudanças
            self.carregar_dados_do_json()
            self.sincronizar_navegacao_lega()
            self.atualizar_valores_tela()
            
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao salvar no servidor:\n\n{e}")        
    #########################################################################################################################