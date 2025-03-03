import pandas as pd
import time
import random
from utils.logger import setup_logger

logger = setup_logger("generate_report")

def generate_excel_report(report_data):
    try:
        logger.info("Gerando relatório Excel...")
        time.sleep(random.randint(1, 3))  # Simula tempo de execução

        df = pd.DataFrame({"Relatório": [report_data]})
        df.to_excel("logs/report.xlsx", index=False)

        logger.info("Relatório Excel gerado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao gerar relatório Excel: {str(e)}")
