import importlib
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler  # 🔹 Alterado para `BackgroundScheduler`
from workflows.extract_key import extract_invoice_key
from workflows.generate_report import generate_excel_report
from utils.logger import setup_logger

logger = setup_logger("scheduler")

#  Importação segura de check_gov
try:
    check_gov = importlib.import_module("workflows.check_gov")
    check_gov_site = getattr(check_gov, "check_gov_site", None)  # Importa apenas a função, se existir
except ImportError as e:
    logger.error(f"Erro ao importar check_gov_site: {str(e)}")
    check_gov_site = None

# Criando o agendador
scheduler = BackgroundScheduler()

#  Ajustando horários para sempre serem no futuro
hora_atual = datetime.now()
extract_time = hora_atual + timedelta(seconds=10)  # Executa em 10s
check_time = extract_time + timedelta(seconds=40)  # Executa 40s depois
report_time = check_time + timedelta(seconds=120)  # Executa 120s depois
shutdown_time = report_time + timedelta(seconds=10)  # Encerra 10s após a última tarefa

logger.info(f"Agendador iniciado às {hora_atual.strftime('%H:%M:%S')}.")
print(f"Agendador iniciado às {hora_atual.strftime('%H:%M:%S')}.")

#  Adicionando as tarefas ao scheduler com logs e proteção contra falhas
def safe_extract_invoice_key():
    try:
        logger.info("Executando extração da chave da nota fiscal...")
        print("Executando extração da chave da nota fiscal...")
        extract_invoice_key()
    except Exception as e:
        logger.error(f"Erro no workflow de extração: {str(e)}")

def safe_check_gov_site():
    if check_gov_site:
        try:
            logger.info("Executando consulta no site do governo...")
            print("Executando consulta no site do governo...")
            check_gov_site()
        except Exception as e:
            logger.error(f"Erro no workflow de consulta ao site do governo: {str(e)}")

def safe_generate_excel_report():
    try:
        logger.info("Gerando relatório Excel...")
        print("Gerando relatório Excel...")
        generate_excel_report()
    except Exception as e:
        logger.error(f"Erro no workflow de geração de relatório: {str(e)}")

#  Função para encerrar o scheduler após todos os jobs
def shutdown_scheduler():
    logger.info("Todas as tarefas foram concluídas. Encerrando o agendador...")
    print("Todas as tarefas foram concluídas. Encerrando o agendador...")
    
    #  Aguarda alguns segundos antes de desligar para evitar erro de "cannot join current thread"
    time.sleep(5)

    scheduler.shutdown(wait=False)

#  Adicionando os jobs com proteção e horários dinâmicos
scheduler.add_job(safe_extract_invoice_key, 'date', run_date=extract_time, misfire_grace_time=60)
if check_gov_site:
    scheduler.add_job(safe_check_gov_site, 'date', run_date=check_time, misfire_grace_time=60)
scheduler.add_job(safe_generate_excel_report, 'date', run_date=report_time, misfire_grace_time=60)

#  Agendando o encerramento automático do scheduler
scheduler.add_job(shutdown_scheduler, 'date', run_date=shutdown_time)

#  Iniciando o scheduler
scheduler.start()

#  Mantém o programa rodando até a última tarefa ser concluída
while scheduler.get_jobs():
    time.sleep(5)  # Aguarda para evitar consumo excessivo de CPU

logger.info("Agendador encerrado automaticamente.")
print("Agendador encerrado automaticamente.")
