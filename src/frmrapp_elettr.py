import customtkinter as ctk
import threading
import tkinter as tk
import requests

from tkinter import messagebox
from datetime import datetime
from CTkTable import CTkTable
from frmmodific_rapp_elettr import FormModific_Rapp_Elettr
from url_api import API_URL


class FormRappElettr(ctk.CTkToplevel):    
    def __init__(self, master, matrice, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.janela_rapp_eletr_inc = None
        self.cod_matrice = matrice

        # Configurações da Janela
        self.title(f"Rapportino Elettronico - Articolo: {self.cod_matrice}")
        self.state('zoomed')        

        # Panel principal que contem tudo
        self.pnl_principal = ctk.CTkFrame(self)
        self.pnl_principal.pack(fill="both", expand=True, pady=(5, 60), padx=20)

        # Comportamento de foco e prioridade na tela        
        self.lift()
        self.focus_force()
        self.transient(master) # Mantém a janela sempre na frente da principal SEM quebrar os menus de clique direito!
        self.grab_set()  # Torna a janela modal (opcional, impede clicar na principal enquanto aberta)

        # Panel titutlo
        self.pnl_titulo = ctk.CTkFrame(self.pnl_principal)
        self.pnl_titulo.pack(fill="both", pady=5)

        # Título do Formulário
        self.lbl_titulo = ctk.CTkLabel(self.pnl_titulo, 
                                       text=f"Rapportino Elettronico - Articolo: {self.cod_matrice}", 
                                       font=("Consolas", 20, "bold"))
        self.lbl_titulo.pack(side="left", padx=(20, 10)) 

        # Botao de incluir
        def click_btn_rapp_elettr_inc():
            global janela_rapp_eletr_inc
            # verifica se a janela já não está aberta na tela
            if self.janela_rapp_eletr_inc is not None and self.janela_rapp_eletr_inc.winfo_exists():
                self.janela_rapp_eletr_inc.lift()
                self.janela_rapp_eletr_inc.focus_force()
            else:
                # Abre o formulário OO passando o código validado
                self.janela_rapp_eletr_inc = FormModific_Rapp_Elettr(master=self, 
                                                                 matrice=self.cod_matrice,
                                                                 registro_edicao=None,
                                                                 on_save=self.atualiza_info_tela)
        self.btn_incluir = ctk.CTkButton(self.pnl_titulo, 
                                         text="Aggiungere", 
                                         font=("Consolas", 18, "bold"), 
                                         anchor="center", 
                                         command=click_btn_rapp_elettr_inc)        

        # Criacao da tela da barra de progresso
        self.pnl_loading = ctk.CTkFrame(self.pnl_principal, fg_color="transparent")
        self.pnl_loading.pack(expand=True, fill="both")

        self.lbl_loading = ctk.CTkLabel(self.pnl_loading, text="Caricamento dei dati...", font=("Consolas", 18))
        self.lbl_loading.pack(pady=10)

        # Barrinha correndo (Indeterminada)
        self.progress_bar = ctk.CTkProgressBar(self.pnl_loading, mode="indeterminate", width=500)
        self.progress_bar.pack(pady=5)        
        self.progress_bar.start()

        # Em vez de iniciar a Thread direto, deixa 200ms para a animação da barra 
        # aparecer lisa na tela e estabilizar o estado zoomed
        self.after(200, self.iniciar_thread_carregamento)    
    ####################################################################################################################


    # FAZ CORRER A BARRA DE ROLAGEM
    def iniciar_thread_carregamento(self):
        # Inicializa a thread de leitura somente após a janela estar estável 
        self.progress_bar.start()

        thread_carga = threading.Thread(target=self.processar_carregamento_background)
        thread_carga.start()
    ####################################################################################################################
    

    # CARREGA DADOS
    def processar_carregamento_background(self):
        self.dadosD = self.carregar_dados_API("D", self.cod_matrice)
        self.dadosE = self.carregar_dados_API("E", self.cod_matrice)
        self.dadosF = self.carregar_dados_API("F", self.cod_matrice)

        # Depois de carregar os arquivos pesados, chama a montagem da tela de volta na Thread Principal
        self.after(100, self.montar_interface_final)   
    ####################################################################################################################


    # TERMINA CRIACAO DA TELA
    def montar_interface_final(self):
        # Panel turnos
        pnl_turnos = ctk.CTkFrame(self.pnl_principal)        

        pnl_turnos.grid_rowconfigure(0, weight=1)
        pnl_turnos.grid_rowconfigure(1, weight=1)
        pnl_turnos.grid_rowconfigure(2, weight=1)

        pnl_turnos.grid_columnconfigure(0, weight=1)

        # Panel TURNO D  
        self.pnl_TurnoD = ctk.CTkFrame(pnl_turnos)
        self.pnl_TurnoD.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")  

        # Panel TURNO E
        self.pnl_TurnoE = ctk.CTkFrame(pnl_turnos)
        self.pnl_TurnoE.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")   

        # Panel TURNO F
        self.pnl_TurnoF = ctk.CTkFrame(pnl_turnos)
        self.pnl_TurnoF.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # Preenche os dados TURNO D
        if self.dadosD:
            if not self.carrega_info_tabelas_historicos("D"):  
                self.destroy()
                return              
        else:
            self.registro_0(None, "D")            

        # Preenche os dados TURNO E
        if self.dadosE:
            if not self.carrega_info_tabelas_historicos("E"):  
                self.destroy()
                return  
        else:
            self.registro_0(None, "E")
        
        # Preenche os dados TURNO F           
        if self.dadosF: 
            if not self.carrega_info_tabelas_historicos("F"):  
                self.destroy()
                return  
        else:
            self.registro_0(None, "F")               

        # Destroi o loading e exibe o container já montado no exato momento
        try:
            self.progress_bar.stop()
            self.pnl_loading.destroy()
        except:
            pass     

        pnl_turnos.pack(fill="both", expand=True, pady=10, padx=10)
        self.btn_incluir.pack(side="right", padx=15, pady=10)  
    ####################################################################################################################


    # FUNCAO ADICONA NA API
    def adicionar_info_API(self, turno, storico):
        # Funcao manda os dados para a API
        def POST_novo_registro():
            try:
                # Prepara o pacote com o molde exato que o Pydantic exige no servidor
                dados_para_api = {
                    "matrice": self.cod_matrice,
                    "turno": turno,
                    "storico": storico
                }

                # Faz o POST para o servidor, enviando o pacote como JSON
                resposta = requests.post(f"{API_URL}/rapportini/", json=dados_para_api, timeout=5)

                # Verifica se o servidor respondeu com Sucesso (Status 200 OK)
                if resposta.status_code == 200:
                    # Sincronizacao com a memória local para a tabela recarregar perfeitamente
                    registros_atualizados = requests.get(f"{API_URL}/rapportini/{self.cod_matrice}").json()
                    registros_turno = [reg for reg in registros_atualizados if reg["turno"] == turno]

                    if turno == "D": self.dadosD = registros_turno
                    elif turno == "E": self.dadosE = registros_turno
                    elif turno == "F": self.dadosF = registros_turno
                else:
                    self.after(0, lambda: messagebox.showerror("Error API", f"The server rejected the data. {resposta.text}", parent=self))

            except requests.exceptions.ConnectionError:
                self.after(0, lambda: messagebox.showerror("Connection Erroro", "We were unable to connect to the AluMatrix Server. The record was not saved.", parent=self))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Critical Error", f"Failed to send data:\n\n[{e}]", parent=self))

        # Dispara a thread em background
        thread_insercao = threading.Thread(target=POST_novo_registro, daemon=True)
        thread_insercao.start()    
    ####################################################################################################################


    # ATUALIZA TELA 
    def atualiza_info_tela(self, turno, historico, registro_edicao=None):
        # Se for uma edição/alteração
        if registro_edicao is not None:
            linha_tabela = registro_edicao["linha_index"]
            tabela_alvo = self.dic_tabelas[turno]

            # Atualiza visualmente apenas a coluna do histórico (Coluna 1) na tela
            tabela_alvo.insert(row=linha_tabela, column=1, value=historico)
            tabela_alvo.update_values(tabela_alvo.values)

            # Converte a data da tela para o padrão ISO antes de atualizar o arquivo JSON
            data_ora_tela = registro_edicao["data_ora_antigo"]
            try:
                data_objeto = datetime.strptime(data_ora_tela, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                data_objeto = datetime.strptime(data_ora_tela, "%d/%m/%Y %H:%M")
            data_ora_json = data_objeto.strftime("%Y-%m-%d %H:%M:%S")

            self.vincular_clique_direito_tabela(tabela_alvo, turno)       

            # Dispara a atualização para o SERVIDOR via API 
            self.atualizar_info_API(registro_edicao["id_banco_dados"], turno, historico)
            return
        
        # SE FOR INCLUSAO
        # Data hora atual
        agora = datetime.now()

        # Data formatada para salvar no JSON padronizado
        data_atual = agora.strftime("%Y-%m-%d %H:%M:%S")
        
        # Data formatada para exibição humana na tabela da tela
        data_atual_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
        nova_linha = [data_atual_formatada, historico]

        # Funcao adiciona info API
        self.adicionar_info_API(turno, historico)

        # Se a tabela não existe (Turno estava vazio com a label "Nessuno storico...")
        if not hasattr(self, 'dic_tabelas') or turno not in self.dic_tabelas:
            nome_pnl = "pnl_Turno" + turno
            container = getattr(self, f"{nome_pnl}", None)
            
            if container and container.winfo_exists():
                # Remove a label cinza de erro ("Nessuno storico...") antes de montar a tabela
                for filho in container.winfo_children():
                    filho.destroy()
                
                # Sincroniza a variável de dados local com o novo registro para a tabela ler
                dados_novos = [{"data_ora": data_atual, "storico": historico}]
                if turno == "D": self.dadosD = dados_novos
                elif turno == "E": self.dadosE = dados_novos
                elif turno == "F": self.dadosF = dados_novos
                
                # Reconstrói a tabela do zero de forma limpa
                self.carrega_info_tabelas_historicos(turno)
        else:
            # Se a tabela já existia na tela, apenas insere a nova linha no topo
            tabela_alvo = self.dic_tabelas[turno]        
            try:
                tabela_alvo.add_row(index=1, values=nova_linha)
                tabela_alvo.update_values(tabela_alvo.values)    
                self.vincular_clique_direito_tabela(tabela_alvo, turno)        
            except Exception:
                try:
                    tabela_alvo.values.insert(1, nova_linha)
                    tabela_alvo.update_values(tabela_alvo.values)
                    self.vincular_clique_direito_tabela(tabela_alvo, turno)
                except Exception as erro_critico:
                    messagebox.showerror("Errore", f"Non è stato possibile aggiungere le informazioni:\n\n[{erro_critico}]", parent=self)
    #####################################################################################################################################


    # CONTROI GRID DE INFORMACOES ENCONTRADAS NA LISTA
    def carrega_info_tabelas_historicos(self, turno):
        # Prepara os dados no formato que a CTkTable precisa (Lista de Listas)   
        try:        
            nome_pnl = "pnl_Turno" + turno
            container = getattr(self, f"{nome_pnl}", None)               

            nome_lbl = getattr(self, "lbl_turno" + turno, None) 
            nome_lbl = ctk.CTkLabel(container, text=f"Turno {turno}", font=ctk.CTkFont(weight="bold"), 
                                    text_color="#ffffff", height=20, anchor="center")
            nome_lbl.pack(fill="both")  

            # A primeira linha precisa ser o cabeçalho 
            dados_tabela = [["DATA ORA", "STORICO"]]

            # info agora é uma lista direta
            info = getattr(self, f"dados{turno}")

            for item in info:
                # O servidor já entrega formatado, mas para exibição fazemos o parse
                data_objeto = datetime.strptime(item["data_ora"], "%Y-%m-%d %H:%M:%S") 
                data_formatada = data_objeto.strftime("%d/%m/%Y %H:%M:%S")
                dados_tabela.append([data_formatada, item["storico"].strip()])

            # Cria o Frame rolável apenas para envelopar a tabela
            nome_scroll = getattr(self, "pnl_scroll" + turno, None) 
            nome_scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
            nome_scroll.pack(fill="both", expand=True, padx=5, pady=5)

            # Cria a tabela passando a matriz de dados de uma vez só
            nome_tabela = getattr(self, "tabela" + turno, None) 
            nome_tabela = CTkTable(master=nome_scroll, 
                              values=dados_tabela, 
                              colors=["#2a2d2e", "#343638"], # Efeito Zebra automático!                                        
                              header_color="#1f538d",
                              font=("Consolas", 16),
                              hover_color="#2b719e",                      
                              text_color="white")
            nome_tabela.pack(fill="x", expand=True)

            # Inicializa o dicionário de tabelas se ele não existir
            if not hasattr(self, 'dic_tabelas'):
                self.dic_tabelas = {}

            # referência da tabela mapeada pelo turno correspondente
            self.dic_tabelas[turno] = nome_tabela    

            # Configura a coluna do STORICO no container para se ajustar
            nome_tabela.grid_columnconfigure(1, weight=1)

            nome_tabela.edit_column(0, width=200)
            nome_tabela.edit_column(1, width=800, anchor="w")

            # Chama a função auxiliar para colocar os cliques direito na criação
            self.vincular_clique_direito_tabela(nome_tabela, turno)

            return True
        except Exception as e:
            messagebox.showwarning("", f"Errore durante la creazione della tabella:\n\n[{e}]", parent=self)        
            return False
    ####################################################################################################################    
        

    # EXIBE O MENU FLUTUANTE NA COORDENADA DO MOUSE
    def exibir_menu_contexto(self, event, tabela_alvo, turno, linha_clicada):
        # Ignora cliques na linha de cabeçalho (linha 0)
        if linha_clicada == 0:
            return

        # Cria o menu nativo associado explicitamente a esta janela (self)
        menu = tk.Menu(self, 
                       tearoff=0, 
                       bg="#ffffff",         
                       fg="black",         
                       font=("Consolas", 18, "bold"),
                       activebackground="#1f538d", 
                       activeforeground="white",
                       bd=1)

        # Menu "titulo" desabilito
        menu.add_command(label="Opzioni per lo storico selezionato...", state="disabled", hidemargin=True)
        menu.add_separator()

        # Menu Modificacao
        menu.add_command(label="Modificare", command=lambda: self.alterar_registro_tabela(tabela_alvo, turno, linha_clicada))

        # Menu Exclusao
        menu.add_command(label="Elimina", command=lambda: self.excluir_registro_tabela(tabela_alvo, turno, linha_clicada))
        
        # Abre o menu usando post() posicionando nas coordenadas absolutas da tela (x_root, y_root)
        try:
            menu.post(event.x_root, event.y_root)
        except Exception:
            menu.tk_popup(event.x_root, event.y_root)
    ####################################################################################################################     


    # FUNÇÃO PARA CARREGAR DADOS DA API
    def carregar_dados_API(self, turno, matrice):
        try:
            resposta = requests.get(f"{API_URL}/rapportini/{matrice}", timeout=5)
            
            if resposta.status_code == 200:
                return [reg for reg in resposta.json() if reg["turno"] == turno]
            else:
                return []
        except:
            return []
    ####################################################################################################################
    

    # EXECUTA A ALTERACAO NO BANCO DE DADOS E NO VISUAL
    def alterar_registro_tabela(self, tabela_alvo, turno, linha):
        dados_linha = tabela_alvo.values[linha]
        data_ora_tela = dados_linha[0]
        historico_antigo = dados_linha[1]
        
        info = getattr(self, f"dados{turno}")
        
        # Pesca o ID invisível na memória
        indice_real = linha - 1
        id_invisivel = info[indice_real]["id"]

        registro_edicao = {"id_banco_dados": id_invisivel, 
                           "linha_index": linha,
                           "turno": turno,                
                           "data_ora_antigo": data_ora_tela, 
                           "storico_antigo": historico_antigo}

        if self.janela_rapp_eletr_inc is not None and self.janela_rapp_eletr_inc.winfo_exists():
            self.janela_rapp_eletr_inc.lift()
            self.janela_rapp_eletr_inc.focus_force()
        else:
            self.janela_rapp_eletr_inc = FormModific_Rapp_Elettr(master=self, 
                                                                 matrice=self.cod_matrice,
                                                                 registro_edicao=registro_edicao,
                                                                 on_save=self.atualiza_info_tela)
    ####################################################################################################################


    # EXECUTA A REMOÇÃO DO BANCO DE DADOS E NO VISUAL
    def excluir_registro_tabela(self, tabela_alvo, turno, linha):
        # Recupera os dados da linha antes de apagar (útil se precisar atualizar o JSON/Banco depois)
        dados_linha = tabela_alvo.values[linha]
        data_ora_tela = dados_linha[0]
        historico = dados_linha[1]

        # Caixa de confirmação
        confirmar = messagebox.askyesno("Conferma",
                                        f"Vuoi davvero eliminare questo storico?\n\nData: {data_ora_tela}\nStorico: {historico}", 
                                        parent=self)
        
        # exclusao server
        if confirmar:
            # Puxa os dados reais da memória
            info = getattr(self, f"dados{turno}")

            # Encontra o ID invisível
            indice_real = linha - 1
            id_invisivel = info[indice_real]["id"]

            # Dispara para o Servidor deletar no SQL
            self.apagar_info_API(id_registro=id_invisivel, turno=turno)

            # Remove a linha da tela instantaneamente para o usuário não ficar esperando
            tabela_alvo.delete_row(index=linha)
            tabela_alvo.update_values(tabela_alvo.values)     

            if len(tabela_alvo.values) <= 1:
                if hasattr(self, 'dic_tabelas') and turno in self.dic_tabelas:
                    del self.dic_tabelas[turno]
                self.registro_0(None, turno)
                
            self.vincular_clique_direito_tabela(tabela_alvo, turno)
    ####################################################################################################################


    # ATUALIZAR O VISUAL DA TABELA QUANDO NAO TEM REGISTRO
    def registro_0(self, tabela_alvo, turno):
        nome_pnl = "pnl_Turno" + turno
        container = getattr(self, f"{nome_pnl}", None)
        if container and container.winfo_exists():
            # Se a tabela_alvo for None, significa que precisamos limpar o container e exibir a mensagem "Nessuno storico trovato"
            if tabela_alvo is None:
                # Destrói os widgets antigos dentro do frame do turno para não sobrepor componentes
                for filho in container.winfo_children():
                    filho.destroy()
                
                # Cria e exibe a mensagem de erro centralizada
                self.nome_lbl_erro = ctk.CTkLabel(container, text=f"Nessuno storico trovato. [TURNO {turno}]", 
                                                    text_color="gray", font=("Consolas", 14, "bold"))
                self.nome_lbl_erro.pack(expand=True, pady=20)
    ####################################################################################################################
    

    # FUNÇÃO AUXILIAR PARA REAPLICAR OS BINDS DO CLIQUE DIREITO
    def vincular_clique_direito_tabela(self, tabela, turno):
        # Percorre todas as células geradas internamente pela CTkTable
        for (row, col), widget in tabela.frame.items():
            # Ignora cliques na linha de cabeçalho (linha 0)
            if row == 0:
                continue
            
            # Captura o escopo correto da linha usando parâmetro padrão (r=row)
            def disparar_menu(event, r=row, t=tabela):
                self.exibir_menu_contexto(event, t, turno, r)

            # Vincula o clique direito no quadrado da célula
            widget.bind("<Button-3>", disparar_menu)
            
            # Vincula o clique direito nos TEXTOS internos
            for child in widget.winfo_children():
                child.bind("<Button-3>", disparar_menu)
    ####################################################################################################################


    # EXCLUSAO DOS DADOS PELA API (BANCO DE DADOS)
    def apagar_info_API(self, id_registro, turno):
        def deletar_registro():
            try:
                # Bate na porta DELETE do servidor passando o ID
                resposta = requests.delete(f"{API_URL}/rapportini/{id_registro}", timeout=5)

                # Se o servidor confirmar a exclusão (200 OK)
                if resposta.status_code == 200:
                    # Sincroniza a memória local puxando os dados atualizados
                    registros_atualizados = requests.get(f"{API_URL}/rapportini/{self.cod_matrice}").json()
                    registros_turno = [reg for reg in registros_atualizados if reg["turno"] == turno]
                    
                    # Atualiza a variável do turno correspondente (Isso fará sua CTkTable/Grid se redesenhar)
                    if turno == "D": self.dadosD = registros_turno
                    elif turno == "E": self.dadosE = registros_turno
                    elif turno == "F": self.dadosF = registros_turno
                else:
                    self.after(0, lambda: messagebox.showerror("Error API", f"The server refused the deletion: {resposta.text}", parent=self))

            except requests.exceptions.ConnectionError:
                self.after(0, lambda: messagebox.showerror("Connection Error", "Unable to connect to the AluMatrix Server.", parent=self))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Critical Error", f"Data deletion failed:\n\n[{e}]", parent=self))

        # Dispara a thread em background
        thread_exclusao = threading.Thread(target=deletar_registro, daemon=True)
        thread_exclusao.start()  
    ####################################################################################################################


    # ALTERACAO PELA API (BANCO DE DADOS)
    def atualizar_info_API(self, id_registro, turno, novo_storico):
        def editar_registro():
            try:
                # Empacota o novo texto seguindo o modelo Pydantic (RapportinoUpdate)
                dados_para_api = {"storico": novo_storico}

                # Bate na porta PUT do servidor passando o ID e o novo texto
                resposta = requests.put(f"{API_URL}/rapportini/{id_registro}", json=dados_para_api, timeout=5)

                # Se o servidor confirmar a alteração (200 OK)
                if resposta.status_code == 200:
                    # Sincroniza a memória local puxando os dados atualizados
                    registros_atualizados = requests.get(f"{API_URL}/rapportini/{self.cod_matrice}").json()
                    registros_turno = [reg for reg in registros_atualizados if reg["turno"] == turno]
                    
                    # Atualiza a variável do turno
                    if turno == "D": self.dadosD = registros_turno
                    elif turno == "E": self.dadosE = registros_turno
                    elif turno == "F": self.dadosF = registros_turno
                else:
                    self.after(0, lambda: messagebox.showerror("Error API", f"The server rejected the change: {resposta.text}", parent=self))

            except requests.exceptions.ConnectionError:
                self.after(0, lambda: messagebox.showerror("Connection Error", "Unable to connect to the AluMatrix Server.", parent=self))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Critical Error", f"Failed to edit data:\n\n[{e}]", parent=self))

        # Dispara a thread em background
        thread_edicao = threading.Thread(target=editar_registro, daemon=True)
        thread_edicao.start()
    ####################################################################################################################