from workflows.extract_key import extract_invoice_key
from workflows.check_gov import check_gov_site
from workflows.generate_report import generate_excel_report
from utils.logger import setup_logger

logger = setup_logger("main")

def run_all_workflows():
    logger.info("Iniciando execução manual dos workflows...")

    # Workflow 1: Extrair chave da NF
    invoice_key = extract_invoice_key()

    # Workflow 2: Checar site .gov
    report_data = check_gov_site()

    # Workflow 3: Gerar relatório Excel
    generate_excel_report(report_data)

    logger.info("Todos os workflows foram executados com sucesso!")

if __name__ == "__main__":
    run_all_workflows()
