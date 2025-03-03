from apscheduler.schedulers.blocking import BlockingScheduler
from workflows.extract_key import extract_invoice_key
from workflows.check_gov import check_gov_site
from workflows.generate_report import generate_excel_report
from utils.logger import setup_logger

logger = setup_logger("scheduler")

def job_workflow_1():
    logger.info("Executando Workflow 1 - Extração da Chave da Nota Fiscal")
    extract_invoice_key()

def job_workflow_2():
    logger.info("Executando Workflow 2 - Consulta no site .gov")
    check_gov_site()

def job_workflow_3():
    logger.info("Executando Workflow 3 - Geração de Relatório Excel")
    report_data = "Exemplo de relatório"  # Pegaria os dados reais do workflow 2
    generate_excel_report(report_data)

scheduler = BlockingScheduler()

# Agendando workflows
scheduler.add_job(job_workflow_1, 'cron', hour=20, minute=30)
scheduler.add_job(job_workflow_2, 'cron', hour=20, minute=45)
scheduler.add_job(job_workflow_3, 'cron', hour=20, minute=55)

logger.info("Agendador iniciado...")
scheduler.start()
