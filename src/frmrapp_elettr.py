import customtkinter as ctk
import threading
import json
import tkinter as tk
import requests

from tkinter import messagebox
from datetime import datetime
from CTkTable import CTkTable
from frmmodific_rapp_elettr import FormModific_Rapp_Elettr

API_URL = "http://127.0.0.1:8000"

class FormRappElettr(ctk.CTkToplevel):    
    def __init__(self, master, matrice, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.janela_rapp_eletr_inc = None
        self.cod_matrice = matrice

        # Configurações da Janela
        self.title(f"Rapportino Elettronico - Articolo: {self.cod_matrice}")
        self.state('zoomed')        
        self.resizable(False, False)

        # Panel principal que contem tudo
        self.pnl_principal = ctk.CTkFrame(self)
        self.pnl_principal.pack(fill="both", expand=True, pady=5, padx=20)

        # Comportamento de foco e prioridade na tela        
        self.lift()
        self.focus_force()
        self.transient(master) # Mantém a janela sempre na frente da principal SEM quebrar os menus de clique direito!
        #self.grab_set()  # Torna a janela modal (opcional, impede clicar na principal enquanto aberta)

        # panel titutlo
        self.pnl_titulo = ctk.CTkFrame(self.pnl_principal)
        self.pnl_titulo.pack(fill="both", pady=5)

        # Título do Formulário
        self.lbl_titulo = ctk.CTkLabel(self.pnl_titulo, 
                                       text=f"Rapportino Elettronico - Articolo: {self.cod_matrice}", 
                                       font=("Consolas", 20, "bold"))
        self.lbl_titulo.pack(side="left", padx=(20, 10)) 

        # botao de incluir
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
                                                                 on_save=self.atualizar_tabelas)
        self.btn_incluir = ctk.CTkButton(self.pnl_titulo, 
                                         text="Aggiungere", 
                                         font=("Consolas", 18, "bold"), 
                                         anchor="center", 
                                         command=click_btn_rapp_elettr_inc)        
        
        # criacao da tela da barra de progresso
        self.pnl_loading = ctk.CTkFrame(self.pnl_principal, fg_color="transparent")
        self.pnl_loading.pack(expand=True, fill="both")

        self.lbl_loading = ctk.CTkLabel(self.pnl_loading, text="Caricamento dei dati...", font=("Consolas", 18))
        self.lbl_loading.pack(pady=10)

        # Barrinha correndo (Indeterminada)
        self.progress_bar = ctk.CTkProgressBar(self.pnl_loading, mode="indeterminate", width=500)
        self.progress_bar.pack(pady=5)        
        self.progress_bar.start()

        # Em vez de iniciar a Thread direto, damos 400ms para a animação da barra 
        # aparecer lisa na tela e estabilizar o estado 'zoomed'.
        self.after(100, self.iniciar_thread_carregamento)    

    '''
    def adicionar_info_JSON(self, turno, data_ora, storico):
        # Executa a leitura, inserção e reescrita do JSON em uma Thread separada
        # para garantir a alta performance da interface gráfica.
        def salvar_novo_registro():
            try:
                path_json = f"json/info_turno{turno}.json"
                
                # Tenta abrir o arquivo existente, ou cria um dicionário vazio se não existir
                try:
                    with open(path_json, "r", encoding="utf-8") as file:
                        dados = json.load(file)
                except FileNotFoundError:
                    dados = {}

                # Garante que a estrutura básica de chaves exista no dicionário
                if turno not in dados:
                    dados[turno] = {}
                if self.cod_matrice not in dados[turno]:
                    dados[turno][self.cod_matrice] = []

                # Cria o novo objeto no formato esperado pelo seu JSON
                novo_item = {
                    "data_ora": data_ora,
                    "storico": storico
                }

                # Adiciona o item à lista da matriz correspondente
                dados[turno][self.cod_matrice].append(novo_item)

                # ordena json
                # Função robusta de ordenação retrocompatível
                def extrair_data_blindada(item):
                    texto = item.get('data_ora', '').strip()
                    for formato in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]:
                        try:
                            return datetime.strptime(texto, formato)
                        except ValueError:
                            continue
                    return datetime(1970, 1, 1)

                lista_hist = dados[turno][self.cod_matrice]
                dados[turno][self.cod_matrice] = sorted(
                    lista_hist,
                    key=extrair_data_blindada,
                    reverse=True
                )

                # Gravação Atômica: Salva os dados atualizados de volta no arquivo
                with open(path_json, "w", encoding="utf-8") as file_w:
                    json.dump(dados, file_w, indent=4, ensure_ascii=False)

                # Sincroniza a memória local da classe
                nova_lista_string = json.dumps(dados[turno][self.cod_matrice], indent=4)
                if turno == "D": self.dadosD = nova_lista_string
                elif turno == "E": self.dadosE = nova_lista_string
                elif turno == "F": self.dadosF = nova_lista_string

            except Exception as e:
                # Dispara o erro de volta para a Thread Principal de forma segura
                self.after(0, lambda: messagebox.showerror("Errore durante il salvataggio del JSON", 
                                                           f"Impossibile salvare le informazioni nel file.", parent=self))

        # Dispara a thread em background de modo daemon
        thread_insercao = threading.Thread(target=salvar_novo_registro, daemon=True)
        thread_insercao.start()
    '''

    def adicionar_info_JSON(self, turno, data_ora, storico):
        # Agora essa função manda os dados para a API em vez de gravar no arquivo JSON
        def salvar_novo_registro():
            try:
                # 1. Prepara o pacote com o molde exato que o Pydantic exige no servidor
                dados_para_api = {
                    "matrice": self.cod_matrice,
                    "turno": turno,
                    "storico": storico
                }

                # 2. Faz o "telefone" (POST) para o servidor, enviando o pacote como JSON
                resposta = requests.post(f"{API_URL}/rapportini/", json=dados_para_api, timeout=5)

                # 3. Verifica se o servidor respondeu com Sucesso (Status 200 OK)
                if resposta.status_code == 200:
                    # Sucesso! Sincronizamos a memória local para a tabela recarregar perfeitamente
                    registros_atualizados = requests.get(f"{API_URL}/rapportini/{self.cod_matrice}").json()
                    registros_turno = [reg for reg in registros_atualizados if reg["turno"] == turno]
                    
                    nova_lista_string = json.dumps(registros_turno, indent=4)
                    if turno == "D": self.dadosD = nova_lista_string
                    elif turno == "E": self.dadosE = nova_lista_string
                    elif turno == "F": self.dadosF = nova_lista_string
                else:
                    self.after(0, lambda: messagebox.showerror("Erro da API", f"O servidor recusou os dados: {resposta.text}", parent=self))

            except requests.exceptions.ConnectionError:
                self.after(0, lambda: messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao Servidor AluMatrix. O registro não foi salvo.", parent=self))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro Crítico", f"Falha ao enviar dados:\n\n[{e}]", parent=self))

        # Dispara a thread em background (como você já fazia com maestria)
        thread_insercao = threading.Thread(target=salvar_novo_registro, daemon=True)
        thread_insercao.start()    

    # ATUALIZAR HISTORICO INSERIDO
    def atualizar_tabelas(self, turno, historico, registro_edicao=None):
        # Método de callback executado quando o usuário clica em OK na tela de inclusão.
        # Gera a data/hora atual formatada para a nova linha
        agora = datetime.now()

        # SE FOR UMA EDIÇÃO/ALTERAÇÃO
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

            # Dispara a atualização do arquivo JSON em background
            self.alterar_no_json_background(turno, data_ora_json, historico)
            return
        
        # Data formatada para salvar no JSON padronizado ISO
        data_atual = agora.strftime("%Y-%m-%d %H:%M:%S")
        
        # Data formatada para exibição humana na tabela da tela
        data_atual_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
        nova_linha = [data_atual_formatada, historico]

        # funcao adiciona info JSON
        self.adicionar_info_JSON(turno, data_atual, historico)

        # SE A TABELA NÃO EXISTE (Turno estava vazio com a label "Nessuno storico...")
        if not hasattr(self, 'dic_tabelas') or turno not in self.dic_tabelas:
            nome_pnl = "pnl_Turno" + turno
            container = getattr(self, f"{nome_pnl}", None)
            
            if container and container.winfo_exists():
                # Remove a label cinza de erro ("Nessuno storico...") antes de montar a tabela
                for filho in container.winfo_children():
                    filho.destroy()
                
                # Sincroniza a variável de dados local com o novo registro para a tabela ler
                dados_novos = [{"data_ora": data_atual, "storico": historico}]
                if turno == "D": self.dadosD = json.dumps(dados_novos)
                elif turno == "E": self.dadosE = json.dumps(dados_novos)
                elif turno == "F": self.dadosF = json.dumps(dados_novos)
                
                # Reconstrói a tabela do zero de forma limpa
                self.Carrega_tabelas_historicos(turno)
        else:
            # SE A TABELA JÁ EXISTIA NA TELA, apenas insere a nova linha no topo
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

    # FAZ CORRER A BARRA DE ROLAGEM
    def iniciar_thread_carregamento(self):
        # Inicializa a thread de leitura somente após a janela estar estável 
        self.progress_bar.start()

        thread_carga = threading.Thread(target=self.processar_carregamento_background)
        thread_carga.start()

    # CARREGA DADOS
    def processar_carregamento_background(self):
        self.dadosD = self.carregar_dados_JSON("D", self.cod_matrice)
        self.dadosE = self.carregar_dados_JSON("E", self.cod_matrice)
        self.dadosF = self.carregar_dados_JSON("F", self.cod_matrice)

        # Depois de carregar os arquivos pesados, chama a montagem da tela 
        # de volta na Thread Principal (segurança do Tkinter)
        self.after(100, self.montar_interface_final)    

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

        # Preenche od dados TURNO D
        if self.dadosD:
            if not self.Carrega_tabelas_historicos("D"):  
                self.destroy()
                return              
        else:
            self.registro_0(None, "D")            

        # Preenche od dados TURNO E
        if self.dadosE:
            if not self.Carrega_tabelas_historicos("E"):  
                self.destroy()
                return  
        else:
            self.registro_0(None, "E")
        
        # Preenche od dados TURNO F           
        if self.dadosF: 
            if not self.Carrega_tabelas_historicos("F"):  
                self.destroy()
                return  
        else:
            self.registro_0(None, "F")

        pnl_turnos.pack(fill="both", expand=True, pady=10, padx=10)

        # Destruímos o loading e exibimos o container já montado no exato mesmo momento!
        try:
            self.progress_bar.stop()
            self.pnl_loading.destroy()
        except:
            pass        

        # Coloca botao de incluir na tela
        self.btn_incluir.pack(side="right", padx=15, pady=10)  

        # Força o CustomTkinter a processar e desenhar internamente tudo o que criamos acima
        self.update_idletasks()

    # CONTROI GRID DE INFORMACOES ENCONTRADAS NO JSON
    def Carrega_tabelas_historicos(self, turno):
        # Prepara os dados no formato que a CTkTable precisa (Lista de Listas)   
        try:        
            nome_pnl = "pnl_Turno" + turno
            container = getattr(self, f"{nome_pnl}", None)               

            nome_lbl = getattr(self, "lbl_turno" + turno, None) 
            nome_lbl = ctk.CTkLabel(container, text=f"Turno {turno}", font=ctk.CTkFont(weight="bold"), text_color="#ffffff", height=20, anchor="center")
            nome_lbl.pack(fill="both")  

            # A primeira linha precisa ser o cabeçalho 
            dados_tabela = [["DATA ORA", "STORICO"]]

            if turno == "D": info = self.dadosD
            elif turno == "E": info = self.dadosE
            elif turno == "F": info = self.dadosF

            if isinstance(info, str):
                info = json.loads(info)

            # Adiciona as linhas do JSON para dentro da lista
            for item in info:
                data_objeto = datetime.strptime(item["data_ora"], "%Y-%m-%d %H:%M:%S") 

                data_formatada = data_objeto.strftime("%d/%m/%Y %H:%M:%S")

                linha = [data_formatada, item.get("storico", "").strip()]
                dados_tabela.append(linha)

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

            nome_tabela.update_values(nome_tabela.values)        

            # Chama a função auxiliar para colocar os cliques direito na criação
            self.vincular_clique_direito_tabela(nome_tabela, turno)

            return True
        except Exception as e:
            messagebox.showwarning("", f"Errore durante la creazione della tabella:\n\n[{e}]", parent=self)        
            return False
        
    # EXIBE O MENU FLUTUANTE NA COORDENADA DO MOUSE
    def exibir_menu_contexto(self, event, tabela_alvo, turno, linha_clicada):
        # Ignora cliques na linha de cabeçalho (linha 0)
        if linha_clicada == 0:
            return

        # Cria o menu nativo associado explicitamente a esta janela (self)
        menu = tk.Menu(
            self, 
            tearoff=0, 
            bg="#ffffff",         # Cor de fundo (igual à tabela)
            fg="black",           # Cor do texto
            font=("Consolas", 18, "bold"),
            activebackground="#1f538d", # Cor quando passa o rato por cima
            activeforeground="white",
            bd=1
        )

        menu.add_command(label="Opzioni per lo storico selezionato...",
            state="disabled",
            hidemargin=True 
        )
        
        # Adiciona uma LINHA SEPARADORA real
        menu.add_separator()

        # Configura a opção chamando o método de alteracao passando os parâmetros necessários
        menu.add_command(
            label="Modificare", 
            command=lambda: self.alterar_registro_tabela(tabela_alvo, turno, linha_clicada)
        )

        # Configura a opção chamando o método de exclusão passando os parâmetros necessários
        menu.add_command(
            label="Elimina", 
            command=lambda: self.excluir_registro_tabela(tabela_alvo, turno, linha_clicada)
        )
        
        # Abre o menu usando post() posicionando nas coordenadas absolutas da tela (x_root, y_root)
        try:
            menu.post(event.x_root, event.y_root)
        except Exception:
            menu.tk_popup(event.x_root, event.y_root)
        

    '''    
    # FUNÇÃO PARA CARREGAR DADOS DO JSON (local)
    def carregar_dados_JSON(self, turno, matrice):
        try:
            path_json = "info_turno" + turno + ".json"
            with open(f"json/{path_json}", "r", encoding="utf-8") as file:
                dados = json.load(file)
                # Verificação preventiva: Garante que a chave existe no arquivo antes de retornar
                if turno in dados and matrice in dados[turno] and len(dados[turno][self.cod_matrice]) != 0:
                    lista_hist = dados[turno][matrice]

                    # múltiplos formatos de data
                    def extrair_data_blindada(item):
                        texto = item.get('data_ora', '').strip()
                        for formato in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]:
                            try:
                                return datetime.strptime(texto, formato)
                            except ValueError:
                                continue
                        return datetime(1970, 1, 1)

                    dados[turno][matrice] = sorted(
                        lista_hist,
                        key=extrair_data_blindada,
                        reverse=True
                    )

                    # Converte de volta para string JSON (com indentação para ficar bonito na tela/arquivo)
                    return json.dumps(dados[turno][matrice], indent=4)
                else:
                    return {}
        except FileNotFoundError:
            return {}
    '''        

    # FUNÇÃO PARA CARREGAR DADOS DA API SQL (Substitui o JSON local)
    def carregar_dados_JSON(self, turno, matrice):
        try:
            # Bate na porta GET do Servidor
            resposta = requests.get(f"{API_URL}/rapportini/{matrice}", timeout=5)
            
            if resposta.status_code == 200:
                registros_api = resposta.json() # O servidor devolve uma lista de dicionários
                
                # Filtra apenas os registros do turno específico que estamos a montar
                registros_turno = [reg for reg in registros_api if reg["turno"] == turno]
                
                if len(registros_turno) > 0:
                    # Converte de volta para string (pois a sua tela atual espera uma string JSON)
                    return json.dumps(registros_turno, indent=4)
                else:
                    return {}
            else:
                messagebox.showerror("", f"Errore na API: {resposta.status_code}")  
                return {}
                
        except requests.exceptions.ConnectionError:
            # Se o servidor estiver desligado, o programa não trava, apenas não carrega os dados
            messagebox.showerror("", "Errore critico: impossibile connettersi al server AluMatrix.")  
            return {}
        
    # EXECUTA A ALTERACAO LÓGICA E VISUAL
    def alterar_registro_tabela(self, tabela_alvo, turno, linha):
        # Recupera os dados direto da linha da tabela
        dados_linha = tabela_alvo.values[linha]
        data_ora_tela = dados_linha[0]
        historico_antigo = dados_linha[1]

        # Monta o pacote de dados que a tela de edição precisa saber
        registro_edicao = {
            "linha_index": linha,          # Guarda qual linha da tabela da tela deve atualizar
            "turno": turno,                # Turno atual locked
            "data_ora_antigo": data_ora_tela, # Usado para achar a linha visual
            "storico_antigo": historico_antigo
        }

        # Abre a tela de inclusão passando o parâmetro de edição
        if self.janela_rapp_eletr_inc is not None and self.janela_rapp_eletr_inc.winfo_exists():
            self.janela_rapp_eletr_inc.lift()
            self.janela_rapp_eletr_inc.focus_force()
        else:
            self.janela_rapp_eletr_inc = FormModific_Rapp_Elettr(
                master=self, 
                matrice=self.cod_matrice,
                registro_edicao=registro_edicao,
                on_save=self.atualizar_tabelas # Usa a mesma função, ela vai tratar se é edição
            )

    # EXECUTA A REMOÇÃO LÓGICA E VISUAL
    def excluir_registro_tabela(self, tabela_alvo, turno, linha):
        # Recupera os dados da linha antes de apagar (útil se precisar atualizar o JSON/Banco depois)
        dados_linha = tabela_alvo.values[linha]
        data_ora_tela = dados_linha[0]
        historico = dados_linha[1]

        # Caixa de confirmação de segurança (Boas práticas de UX)
        confirmar = messagebox.askyesno(
            "Conferma", 
            f"Vuoi davvero eliminare questo storico?\n\nData: {data_ora_tela}\nStorico: {historico}",
            parent=self
        )
        
        if confirmar:
            try:
                # Converte o formato da tela para o padrão ISO do JSON antes de apagar
                try:
                    data_objeto = datetime.strptime(data_ora_tela, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    data_objeto = datetime.strptime(data_ora_tela, "%d/%m/%Y %H:%M")
                
                data_ora_json = data_objeto.strftime("%Y-%m-%d %H:%M:%S")

                # Remove a linha visualmente do componente gráfico
                tabela_alvo.delete_row(index=linha)
                tabela_alvo.update_values(tabela_alvo.values)     

                # VERIFICAÇÃO ATUALIZADA: len == 1 significa que sobrou apenas o cabeçalho ["DATA ORA", "STORICO"]
                if len(tabela_alvo.values) <= 1:
                    # Removemos a tabela inteira do dicionário e passamos None para limpar o container e exibir a Label
                    if hasattr(self, 'dic_tabelas') and turno in self.dic_tabelas:
                        del self.dic_tabelas[turno]
                    self.registro_0(None, turno)
                else:
                    # Caso ainda existam linhas, apenas reaplicamos os binds normalmente
                    self.vincular_clique_direito_tabela(tabela_alvo, turno)

                # Sincroniza e apaga do arquivo JSON (Chamada com o nome corrigido)
                self.remover_do_json_background(turno, data_ora_json)

            except Exception as e:
                messagebox.showerror("Erro", f"Non è stato possibile eliminare:\n\n[{e}]", parent=self)

    # ATUALIZAR O VISUAL DA TABELA QUANDO NAO TEM REGISTRO
    def registro_0(self, tabela_alvo, turno):
        nome_pnl = "pnl_Turno" + turno
        container = getattr(self, f"{nome_pnl}", None)
        if container and container.winfo_exists():
            # Se a tabela_alvo for None, significa que precisamos limpar o container 
            # e exibir a mensagem "Nessuno storico trovato"
            if tabela_alvo is None:
                # Destrói os widgets antigos dentro do frame do turno para não sobrepor componentes
                for filho in container.winfo_children():
                    filho.destroy()
                
                # Cria e exibe a mensagem de erro centralizada
                self.nome_lbl_erro = ctk.CTkLabel(container, text=f"Nessuno storico trovato. [TURNO {turno}]", 
                                                    text_color="gray", font=("Consolas", 14, "bold"))
                self.nome_lbl_erro.pack(expand=True, pady=20)

    # EXCLUIR REGISTRO DO JASON
    def remover_do_json_background(self, turno, data_ora_alvo):
        def buscar_e_excluir():
            try:
                path_json = f"json/info_turno{turno}.json"
                
                # Abre o arquivo para leitura
                with open(path_json, "r", encoding="utf-8") as file:
                    dados = json.load(file)
                
                # Verifica as chaves estruturais preventivamente
                if turno in dados and self.cod_matrice in dados[turno]:
                    lista_registros = dados[turno][self.cod_matrice]
                    
                    # Filtra os dados da lista de registros removendo o item alvo pelo padrão ISO correto
                    def extrair_data_blindada(item):
                        texto = item.get('data_ora', '').strip()
                        for formato in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]:
                            try:
                                return datetime.strptime(texto, formato)
                            except ValueError:
                                continue
                        return datetime(1970, 1, 1)

                    # Executa a filtragem segura
                    novos_registros = []
                    for item in lista_registros:
                        d_item = extrair_data_blindada(item)
                        try:
                            d_alvo = datetime.strptime(data_ora_alvo, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            d_alvo = datetime.strptime(data_ora_alvo, "%Y-%m-%d %H:%M")
                        
                        if d_item != d_alvo:
                            novos_registros.append(item)

                    dados[turno][self.cod_matrice] = sorted(
                        novos_registros,
                        key=extrair_data_blindada,
                        reverse=True
                    )
                    
                    # Escrita Atômica/Segura: Grava de volta no arquivo
                    with open(path_json, "w", encoding="utf-8") as file_w:
                        json.dump(dados, file_w, indent=4, ensure_ascii=False)
                    
                    # Atualiza os dados na memória da classe para que fiquem sincronizados
                    # Se o usuário fechar e reabrir sem carregar, a memória estará certa
                    nova_lista_ordenada = sorted(
                        dados[turno][self.cod_matrice],
                        key=lambda x: datetime.strptime(x['data_ora'], "%Y-%m-%d %H:%M:%S"),
                        reverse=True
                    )
                    
                    if turno == "D": self.dadosD = json.dumps(nova_lista_ordenada, indent=4)
                    elif turno == "E": self.dadosE = json.dumps(nova_lista_ordenada, indent=4)
                    elif turno == "F": self.dadosF = json.dumps(nova_lista_ordenada, indent=4)

            except Exception as e:
                # Como estamos numa Thread separada, usamos o after para mandar o alerta de erro para a Main Thread
                self.after(0, lambda: messagebox.showerror("Errore", f"Non è stato possibile eliminare il file:\n\n[{e}]", parent=self))

        # Dispara o processo em background
        thread_exclusao = threading.Thread(target=buscar_e_excluir, daemon=True)
        thread_exclusao.start()

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

    # ALTERAR REGISTRO NO JSON EM BACKGROUND
    def alterar_no_json_background(self, turno, data_ora_alvo, novo_historico):
        def buscar_e_alterar():
            try:
                path_json = f"json/info_turno{turno}.json"
                
                with open(path_json, "r", encoding="utf-8") as file:
                    dados = json.load(file)
                
                if turno in dados and self.cod_matrice in dados[turno]:
                    lista_registros = dados[turno][self.cod_matrice]
                    
                    # Função para comparar as datas de forma cega contra formatos
                    def extrair_data_blindada(item):
                        texto = item.get('data_ora', '').strip()
                        for formato in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]:
                            try:
                                return datetime.strptime(texto, formato)
                            except ValueError:
                                continue
                        return datetime(1970, 1, 1)

                    try:
                        d_alvo = datetime.strptime(data_ora_alvo, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        d_alvo = datetime.strptime(data_ora_alvo, "%Y-%m-%d %H:%M")

                    # Percorre os registros buscando o item com a data idêntica para editar
                    modificado = False
                    for item in lista_registros:
                        if extrair_data_blindada(item) == d_alvo:
                            item["storico"] = novo_historico
                            modificado = True
                            break # Encontrou, pode parar o laço

                    if modificado:
                        # Salva de volta no arquivo de forma organizada
                        with open(path_json, "w", encoding="utf-8") as file_w:
                            json.dump(dados, file_w, indent=4, ensure_ascii=False)
                        
                        # Sincroniza a memória de strings da classe principal
                        nova_lista_string = json.dumps(dados[turno][self.cod_matrice], indent=4)
                        if turno == "D": self.dadosD = nova_lista_string
                        elif turno == "E": self.dadosE = nova_lista_string
                        elif turno == "F": self.dadosF = nova_lista_string

            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Errore", f"La modifica non è stata salvata:\n\n[{e}]", parent=self))

        # Roda o processo em background para não travar os cliques da tela
        thread_edicao = threading.Thread(target=buscar_e_alterar, daemon=True)
        thread_edicao.start()