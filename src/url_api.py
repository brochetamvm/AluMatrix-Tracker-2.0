import os
import sys
import configparser

# Descobre onde o programa está
if getattr(sys, 'frozen', False):
    DIRETORIO_BASE = os.path.dirname(sys.executable)
else:
    DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
###############################################################################################################################    

# AGORA É CONFIG.TXT
ARQUIVO_CONFIG = os.path.join(DIRETORIO_BASE, "config.txt")
###############################################################################################################################

###############################################################################################################################
###############################################################################################################################
# VALORES PADRÃO
API_URL = "http://127.0.0.1:8000"
CAMINHO_LOGO = ""
###############################################################################################################################
###############################################################################################################################

# LEITURA DO ARQUIVO
config = configparser.ConfigParser()

if os.path.exists(ARQUIVO_CONFIG):
    try:
        config.read(ARQUIVO_CONFIG, encoding="utf-8")
        if 'SERVIDOR' in config and 'Url' in config['SERVIDOR']:
            url_lida = config['SERVIDOR']['Url'].strip()
            if url_lida: API_URL = url_lida
            
        if 'PERSONALIZACAO' in config and 'Logo' in config['PERSONALIZACAO']:
            CAMINHO_LOGO = config['PERSONALIZACAO']['Logo'].strip()
    except: pass
else:
    # Se não existir, cria o config.txt com a estrutura correta
    config['SERVIDOR'] = {'Url': 'http://127.0.0.1:8000'}
    config['PERSONALIZACAO'] = {'Logo': ''}
    try:
        with open(ARQUIVO_CONFIG, 'w', encoding="utf-8") as f:
            config.write(f)
    except: pass
###############################################################################################################################    

# SALVA A ESCOLHA DO USUÁRIO DE VOLTA NO CONFIG.TXT
def salvar_caminho_logo(novo_caminho):
    if not config.has_section('PERSONALIZACAO'):
        config.add_section('PERSONALIZACAO')
        
    config.set('PERSONALIZACAO', 'Logo', novo_caminho)
    try:
        with open(ARQUIVO_CONFIG, 'w', encoding="utf-8") as f:
            config.write(f)
    except Exception as e:
        print(f"Erro ao salvar imagem no config.txt: {e}")
###############################################################################################################################        