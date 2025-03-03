import PyPDF2
import time
import random
import re
import os
from pathlib import Path
from utils.logger import setup_logger  # Certifique-se de que este módulo está correto

logger = setup_logger("extract_key")

# Obter automaticamente o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent  # Vai até a raiz do projeto
PDF_DIR = BASE_DIR / "arquivos"  # Subpasta onde os PDFs estarão armazenados
TXT_FILE = PDF_DIR / "chave_acesso.txt"  # Caminho do arquivo de saída

def extract_invoice_key(pdf_filename="NFe_Chave_Acesso_Modificado.pdf"):
    """
    Extrai a Chave de Acesso do PDF e a salva em um arquivo TXT.
    """
    try:
        logger.info("Iniciando extração da chave da nota fiscal...")

        time.sleep(random.randint(1, 3))  # Simula tempo de execução

        # Caminho dinâmico para o arquivo PDF
        pdf_path = PDF_DIR / pdf_filename

        if not pdf_path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

        # Abrir e ler o PDF
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

        # Converter texto para minúsculas e remover espaços extras
        text = text.lower().strip()

        # Log do texto extraído para depuração
        logger.info("Texto extraído do PDF:\n" + text)

        # Expressão regular para encontrar a Chave de Acesso (44 dígitos numéricos)
        chave_acesso = None
        match = re.search(r"chave de acesso[:\s]*([\d\s]{44,})", text)

        if match:
            chave_acesso = match.group(1)
            chave_acesso = re.sub(r"\s+", "", chave_acesso)  # Remover espaços extras

        if not chave_acesso:
            raise ValueError("Chave de acesso não encontrada no PDF")

        logger.info(f"Chave extraída com sucesso: {chave_acesso}")

        # Salvar a chave de acesso em um arquivo TXT
        os.makedirs(PDF_DIR, exist_ok=True)  # Garantir que a pasta existe
        with open(TXT_FILE, "w", encoding="utf-8") as file:
            file.write(chave_acesso)

        logger.info(f"Chave salva no arquivo: {TXT_FILE}")
        return chave_acesso

    except Exception as e:
        logger.error(f"Erro na extração da chave: {str(e)}")
        return None

# Teste chamando dinamicamente dentro da pasta do projeto
if __name__ == "__main__":
    chave = extract_invoice_key()
    if chave:
        print(f"Chave de Acesso Extraída e salva em {TXT_FILE}")
    else:
        print("Falha na extração da chave de acesso.")
