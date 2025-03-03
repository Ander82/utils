import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import re
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import setup_logger

# Configuração de Logs
logger = setup_logger("workflow_2")

# Configuração do ChromeDriver
CHROMEDRIVER_PATH = r"C:\Users\ander\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
API_KEY = "4784bf6f58fc5dd0459c22d2ac9705f0"  # Substitua pela sua chave de API do 2Captcha
URL_SITE = "https://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx?tipoConsulta=resumo&tipoConteudo=7PhJ+gAVw2g="

# Diretório do projeto e caminho para o arquivo da Chave de Acesso
BASE_DIR = Path(__file__).resolve().parent.parent
TXT_DIR = BASE_DIR / "arquivos"
TXT_FILE = TXT_DIR / "chave_acesso.txt"
RESULT_FILE = TXT_DIR / "resultado_extracao.txt"

# Configuração do Selenium
def configure_selenium():
    if not os.path.isfile(CHROMEDRIVER_PATH):
        raise FileNotFoundError(f"ChromeDriver não encontrado no caminho: {CHROMEDRIVER_PATH}")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Obtém a Chave de Acesso do arquivo TXT
def get_chave_acesso():
    try:
        with open(TXT_FILE, "r", encoding="utf-8") as file:
            chave_acesso = file.read().strip()
            if not chave_acesso or not re.match(r"^\d{44}$", chave_acesso):
                raise ValueError("Chave de acesso inválida.")
            logger.info(f"Chave de Acesso lida com sucesso: {chave_acesso}")
            return chave_acesso
    except Exception as e:
        logger.error(f"Erro ao ler a chave de acesso: {str(e)}")
        return None

# Obtém a sitekey para o CAPTCHA
def get_sitekey(driver):
    try:
        logger.info("Obtendo sitekey do CAPTCHA...")
        captcha_element = driver.find_element(By.CSS_SELECTOR, ".h-captcha")
        return captcha_element.get_attribute("data-sitekey")
    except Exception as e:
        logger.error(f"Erro ao obter sitekey: {str(e)}")
        return None

# Resolve o CAPTCHA usando a API 2Captcha
def solve_captcha(api_key, site_key, page_url):
    try:
        logger.info("Enviando CAPTCHA para resolução...")
        url = "http://2captcha.com/in.php"
        payload = {"key": api_key, "method": "hcaptcha", "sitekey": site_key, "pageurl": page_url, "json": 1}
        response = requests.post(url, data=payload).json()

        if response.get("status") != 1:
            raise Exception(f"Erro ao criar tarefa: {response.get('request')}")

        task_id = response.get("request")
        result_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={task_id}&json=1"

        while True:
            time.sleep(5)
            result_response = requests.get(result_url).json()
            if result_response.get("status") == 1:
                logger.info("CAPTCHA resolvido com sucesso!")
                return result_response.get("request")
            elif result_response.get("request") != "CAPCHA_NOT_READY":
                raise Exception(f"Erro ao obter solução: {result_response.get('request')}")
    except Exception as e:
        logger.error(f"Erro ao resolver o CAPTCHA: {str(e)}")
        return None

# Insere a solução do CAPTCHA e submete o formulário (com até 3 tentativas)
def fill_captcha_and_submit(driver, captcha_solution, chave_acesso):
    attempts = 0
    while attempts < 3:
        try:
            logger.info(f"Tentativa {attempts + 1}: Inserindo solução do CAPTCHA...")

            captcha_field = driver.find_element(By.CSS_SELECTOR, "[id^='h-captcha-response']")
            driver.execute_script("arguments[0].style.display = 'block';", captcha_field)
            captcha_field.clear()
            captcha_field.send_keys(captcha_solution)

            logger.info("Clicando no botão 'Continuar'...")
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnConsultarHCaptcha").click()
            time.sleep(10)

            if "Resumo da Nota Fiscal" in driver.page_source or "Consulta Realizada com Sucesso" in driver.page_source:
                logger.info("CAPTCHA resolvido com sucesso! Saindo do loop.")
                return True

            attempts += 1

        except Exception as e:
            logger.error(f"Erro ao enviar CAPTCHA na tentativa {attempts + 1}: {str(e)}")
            attempts += 1

    logger.error("Número máximo de tentativas atingido. Falha no CAPTCHA.")
    return False

# Extrai os dados da página após a consulta e salva no TXT
def extract_data(driver):
    try:
        logger.info("Extraindo dados da consulta via Selenium...")

        wait = WebDriverWait(driver, 15)
        element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#conteudoDinamico > div:nth-child(3) > div.XSLTNFeResumida > div:nth-child(13)")
        ))

        extracted_text = element.text.strip()

        with open(RESULT_FILE, "w", encoding="utf-8") as file:
            file.write(extracted_text)

        logger.info("Dados extraídos via Selenium e salvos com sucesso!")
        return extracted_text

    except Exception as e:
        error_message = f"Erro ao extrair dados: {str(e)}"
        logger.error(error_message)

        with open(RESULT_FILE, "w", encoding="utf-8") as file:
            file.write(error_message)

        return None

# **Função principal para ser chamada pelo `scheduler.py`**
def check_gov_site():
    try:
        logger.info("Iniciando consulta no site do governo...")
        print("Executando check_gov_site...")

        chave_acesso = get_chave_acesso()
        if not chave_acesso:
            raise Exception("Nenhuma chave de acesso válida encontrada.")

        driver = configure_selenium()

        logger.info("Acessando o site...")
        driver.get(URL_SITE)
        time.sleep(5)

        logger.info("Preenchendo a chave de acesso...")
        input_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtChaveAcessoResumo")
        input_field.send_keys(chave_acesso)

        logger.info("Chave de acesso preenchida com sucesso!")

        sitekey = get_sitekey(driver)
        captcha_solution = solve_captcha(API_KEY, sitekey, URL_SITE)

        if fill_captcha_and_submit(driver, captcha_solution, chave_acesso):
            extract_data(driver)
            logger.info("Consulta concluída com sucesso!")
        else:
            raise Exception("Erro ao submeter o formulário após 3 tentativas.")

    except Exception as e:
        logger.error(f"Erro fatal no Workflow 2: {str(e)}")
    finally:
        driver.quit()

# **Executando SOMENTE quando rodado diretamente**
if __name__ == "__main__":
    check_gov_site()
