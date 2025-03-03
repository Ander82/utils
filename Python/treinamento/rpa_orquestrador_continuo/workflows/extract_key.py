import time
import random
from utils.logger import setup_logger

logger = setup_logger("extract_key")

def extract_invoice_key():
    try:
        logger.info("Iniciando extração da chave da nota fiscal...")
        time.sleep(random.randint(1, 3))  # Simula tempo de execução
        invoice_key = "NFe-1234567890123456789012345678901234567890"
        logger.info(f"Chave extraída com sucesso: {invoice_key}")
        return invoice_key
    except Exception as e:
        logger.error(f"Erro na extração da chave: {str(e)}")
