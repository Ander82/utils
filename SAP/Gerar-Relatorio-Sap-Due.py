import win32com.client
import sys
import subprocess
import requests
import os
import json
from base64 import b64encode
import pandas as pd
import datetime
import psutil
import openpyxl
import time
import warnings
from datetime import datetime, timedelta
import autoit

warnings.filterwarnings("ignore")
# autoit = win32com.client.Dispatch("AutoItX3.Control")
wShell = win32com.client.Dispatch("WScript.Shell")
# Lista de processos em execução
process_name = "saplogon.exe"
user_id = os.getlogin()

# Obter a data atual no formato necessário
#data_atual = datetime.now().strftime("%d.%m.%Y")
data_atual = (datetime.now() - timedelta(days=180)).strftime("%d.%m.%Y")
def obter_datas_mes():
    # Obter a data atual
    today = datetime.today()
    
    # Data de início do mês com ano fixo 2000
    month_start = today.replace(day=1, year=2000)
    
    # Calcular o último dia do mês com o ano atual
    current_month_start = today.replace(day=1)
    next_month = current_month_start.replace(day=28) + timedelta(days=4)  # Garante que passamos para o próximo mês
    month_end = next_month - timedelta(days=next_month.day)  # Subtrai os dias restantes para voltar ao último dia do mês atual
    
    # Formatar as datas como dd.MM.2000 e dd.MM.yyyy
    start_date_str = month_start.strftime("%d.%m.2000")
    end_date_str = month_end.strftime("%d.%m.%Y")
    return start_date_str, end_date_str

# # Criar objeto SAP
class SapGui():
    def __init__(self):
        self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
        if not type(self.SapGuiAuto) == win32com.client.CDispatch:
            raise Exception('Erro ao criar objeto!')
        application = self.SapGuiAuto.GetScriptingEngine
        # Verifique se há alguma conexão aberta
        if application.Connections.Count > 0:
            self.connection = application.Connections.Item(0)  # obtenha a primeira conexão
        else:
            raise Exception('Nenhuma conexão SAP aberta encontrada!')
        # Agora obtenha a sessão
        if self.connection.Sessions.Count > 0:
            self.session = self.connection.Sessions.Item(0)  # obtenha a primeira sessão
        else:
            raise Exception('Nenhuma sessão SAP aberta encontrada!')
    def Login(self):
        try:
            self.session.findById("wnd[0]/usr/txtRSYST-MANDT").Text = MANDT
            self.session.findById("wnd[0]/usr/txtRSYST-BNAME").Text = BNAME
            self.session.findById("wnd[0]/usr/pwdRSYST-BCODE").Text = BCODE
            self.session.findById("wnd[0]/usr/txtRSYST-LANGU").Text = LANGU
            self.session.findById("wnd[0]").sendVKey(0)
            try:
                self.session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").select()
                self.session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").setFocus()
                self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
            except:
                pass
        except:
            raise Exception('Erro login SAP: ' + str(sys.exc_info()[0]))
# # Iniciar
sap = SapGui()

# Maximizar
sap.session.findById("wnd[0]").maximize()

# Acessar a transacao SMARTTAX
sap.session.findById(f"wnd[0]/tbar[0]/okcd").text = '/n/TAX/SMARTTAX'
sap.session.findById(f"wnd[0]").sendVKey(0)

# Clicar em Expandir
sap.session.findById("wnd[0]/usr/cntlTREE_CONTAINER/shellcont/shell").expandNode ("SMARTC")
sap.session.findById("wnd[0]/usr/cntlTREE_CONTAINER/shellcont/shell").expandNode ("NOTA_FISC")
sap.session.findById("wnd[0]/usr/cntlTREE_CONTAINER/shellcont/shell").selectItem ("ZDPFISC_NF_I","2")
sap.session.findById("wnd[0]/usr/cntlTREE_CONTAINER/shellcont/shell").ensureVisibleHorizontalItem ("ZDPFISC_NF_I","2")
sap.session.findById("wnd[0]/usr/cntlTREE_CONTAINER/shellcont/shell").topNode = ("DPFISC")
sap.session.findById("wnd[0]/usr/cntlTREE_CONTAINER/shellcont/shell").clickLink ("ZDPFISC_NF_I","2")

# Digitar empresa
sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/radP_SAI").select()
sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/ctxtP_BUKRS").text = "1100"

# Digitar periodo
#sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/ctxtS_PSTDAT-LOW").text = "01.11.2024"
sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/ctxtS_PSTDAT-LOW").text = data_atual
#sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/ctxtS_PSTDAT-HIGH").text = "09.12.2024"

# Digitar CFOP
sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/btn%_S_CFOP_%_APP_%-VALU_PUSH").press()
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,0]").text = "7101"
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").text = "6501"
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,2]").text = "6504"
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,3]").text = "7102"
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,4]").text = "7504"
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,4]").setFocus()
sap.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,4]").caretPosition = 4
sap.session.findById("wnd[1]/tbar[0]/btn[8]").press()

# Clicar em executar
sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/ctxtS_CFOP-LOW").setFocus()
sap.session.findById("wnd[0]/usr/tabsTABSTRIP_TABB1/tabpFP/ssub%_SUBSCREEN_TABB1:ZDPFISC0003:0700/ctxtS_CFOP-LOW").caretPosition = 4
sap.session.findById("wnd[0]/tbar[1]/btn[8]").press()

# Salvar excel
# Localiza a grade
grid = sap.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell/shellcont[1]/shell")

# Abre o menu de contexto
grid.contextMenu()

# Define a linha atual como nenhuma (-1 para indicar nenhuma seleção específica)
grid.currentCellRow = -1

# Seleciona a coluna "DOCNUM"
grid.selectColumn("DOCNUM")

# Limpa as linhas selecionadas
grid.selectedRows = ""

# Abre o menu de contexto novamente e seleciona a opção de exportação "&XXL"
grid.contextMenu()
grid.selectContextMenuItem("&XXL")

# Pressiona o botão para confirmar a exportação
sap.session.findById("wnd[1]/tbar[0]/btn[20]").press()

# Define o caminho e o nome do arquivo para salvar
sap.session.findById("wnd[1]/usr/ctxtDY_PATH").text = str(dt['dirDownload'][0])
sap.session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = str(dt['nameDownload'][0])

# Pressiona o botão para salvar o arquivo
sap.session.findById("wnd[1]/tbar[0]/btn[0]").press()
