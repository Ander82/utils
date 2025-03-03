import pandas as pd
import time
import random
import os
from pathlib import Path
import sys
# ✅ Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import setup_logger  # ✅ Agora a importação funcionará corretamente
from utils.logger import setup_logger

logger = setup_logger("generate_report")

# Obter automaticamente o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent  # Vai até a raiz do projeto
TXT_DIR = BASE_DIR / "arquivos"  # Subpasta onde o TXT está armazenado
RESULT_FILE = TXT_DIR / "resultado_extracao.txt"  # Arquivo de entrada
EXCEL_FILE = TXT_DIR / "resultado_extracao.xlsx"  # Arquivo de saída

def generate_excel_report():
    """
    Lê o resultado_extracao.txt e gera um relatório Excel.
    Se o arquivo não existir, grava um erro no log.
    """
    try:
        logger.info("Verificando existência do arquivo de extração...")

        # ✅ Verifica se o arquivo TXT existe
        if not RESULT_FILE.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {RESULT_FILE}")

        logger.info("Lendo os dados do arquivo de extração...")

        # ✅ Lê os dados do TXT e separa em linhas
        with open(RESULT_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # ✅ Criando um DataFrame do Pandas para distribuir os dados em colunas
        df = pd.DataFrame({"Dados Extraídos": [line.strip() for line in lines]})

        logger.info("Gerando relatório Excel...")

        # ✅ Salvando o arquivo Excel na pasta arquivos/
        df.to_excel(EXCEL_FILE, index=False)

        logger.info(f"Relatório Excel gerado com sucesso: {EXCEL_FILE}")
        return EXCEL_FILE

    except Exception as e:
        logger.error(f"Erro ao gerar relatório Excel: {str(e)}")
        return None

# Executar se for chamado diretamente
if __name__ == "__main__":
    generate_excel_report()
