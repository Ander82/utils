# 📌 RPA Orquestrador com Python e Selenium

## 📖 Sobre o Projeto
Este projeto implementa um **orquestrador RPA** (Robotic Process Automation) utilizando **Python, Selenium e APScheduler**. O objetivo é **automatizar a extração de dados fiscais** a partir de um site do governo, lidar com **CAPTCHAs**, gerar relatórios em **Excel** e gerenciar a execução de workflows com um **scheduler automático**.

## 🚀 Tecnologias Utilizadas

- **Python 3.9+**
- **Selenium WebDriver** – Automação de Navegador
- **APScheduler** – Agendamento de Tarefas
- **Pandas** – Manipulação de Dados e Geração de Excel
- **2Captcha API** – Resolução Automática de CAPTCHAs
- **Logging** – Monitoramento e Depuração

## 📂 Estrutura do Projeto

```
rpa_orquestrador_c_encerrar/
│── arquivos/                    # Armazena arquivos gerados
│   ├── chave_acesso.txt          # Chave extraída da Nota Fiscal
│   ├── resultado_extracao.txt    # Dados extraídos do site do governo
│   ├── resultado_extracao.xlsx   # Relatório final em Excel
│── workflows/                    # Scripts de automação
│   ├── __init__.py               # Arquivo para reconhecimento como módulo
│   ├── extract_key.py            # Extrai a chave da Nota Fiscal do PDF
│   ├── check_gov.py              # Consulta no site do governo
│   ├── generate_report.py        # Gera o relatório em Excel
│── utils/                        # Scripts auxiliares
│   ├── __init__.py               # Arquivo para reconhecimento como módulo
│   ├── logger.py                 # Configuração de logs
│── scheduler.py                   # Gerenciador de execução automatizada
│── main.py                        # Execução manual dos workflows
│── README.md                      # Documentação do projeto
```

## 🔧 Configuração do Ambiente

### 1️⃣ **Instalar as Dependências**
Certifique-se de ter o **Python 3.9+** instalado e execute:

```sh
pip install -r requirements.txt
```

### 2️⃣ **Configurar o Selenium WebDriver**
Baixe o **ChromeDriver** correspondente à versão do seu navegador e configure o caminho em `workflows/check_gov.py`:

```python
CHROMEDRIVER_PATH = r"C:\\Users\\SeuUsuario\\Downloads\\chromedriver.exe"
```

### 3️⃣ **Configurar a API 2Captcha** *(Opcional)*
Caso queira automação do CAPTCHA, insira sua **API Key** em `check_gov.py`:

```python
API_KEY = "sua_api_key_aqui"
```

## ⚙️ Como Usar

### 📅 Configuração do Scheduler para Diferentes Frequências
O `scheduler.py` pode ser configurado para rodar automaticamente em diferentes frequências, conforme necessário:

- **Rodar todos os dias às 08:00:**
  ```python
  scheduler.add_job(safe_extract_invoice_key, 'cron', hour=8, minute=0)
  scheduler.add_job(safe_check_gov_site, 'cron', hour=8, minute=15)
  scheduler.add_job(safe_generate_excel_report, 'cron', hour=8, minute=30)
  ```

- **Rodar somente nos finais de semana (sábado e domingo) às 10:00:**
  ```python
  scheduler.add_job(safe_extract_invoice_key, 'cron', day_of_week='sat,sun', hour=10, minute=0)
  ```

- **Rodar em dias específicos da semana (segunda, quarta e sexta) às 14:30:**
  ```python
  scheduler.add_job(safe_extract_invoice_key, 'cron', day_of_week='mon,wed,fri', hour=14, minute=30)
  ```

- **Rodar apenas no primeiro dia do mês às 09:00:**
  ```python
  scheduler.add_job(safe_extract_invoice_key, 'cron', day=1, hour=9, minute=0)
  ```

- **Rodar a cada 6 horas:**
  ```python
  scheduler.add_job(safe_extract_invoice_key, 'interval', hours=6)
  ```

Essas opções permitem personalizar a execução do RPA conforme a necessidade do usuário.


### 📌 **Execução Manual dos Workflows**
Você pode executar cada workflow separadamente:

```sh
python workflows/extract_key.py      # Extrai a chave da Nota Fiscal
python workflows/check_gov.py        # Consulta no site do governo
python workflows/generate_report.py  # Gera o relatório Excel
```

### 📌 **Execução Automatizada com o Scheduler**
Para rodar **todos os workflows automaticamente** na ordem correta:

```sh
python scheduler.py
```

📌 O **scheduler**:
- **Ajusta horários automaticamente** para garantir que os workflows sejam executados corretamente.
- **Fecha automaticamente após completar todas as tarefas.**

## 🛠 Solução de Problemas

**1️⃣ Erro de Importação (`ModuleNotFoundError`)**
- Execute os comandos abaixo para garantir que os módulos estão corretamente instalados:
```sh
pip install -r requirements.txt
```
- Certifique-se de que os diretórios `workflows/` e `utils/` contêm um `__init__.py`.

**2️⃣ `ChromeDriver` não encontrado**
- Verifique se o caminho do **ChromeDriver** está correto.
- Baixe a versão compatível com seu navegador [aqui](https://chromedriver.chromium.org/downloads).

**3️⃣ O `scheduler.py` não encerra automaticamente**
- Se o script não estiver finalizando corretamente, edite `scheduler.py` para incluir:
```python
import os
os._exit(0)
```

## 📌 Contribuições
Sinta-se à vontade para contribuir com melhorias! Para isso:
1. **Fork** este repositório
2. Crie uma **branch** (`git checkout -b minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionei uma nova feature'`)
4. Envie para análise (`git push origin minha-feature`)

## 📜 Licença
Este projeto é de código aberto e distribuído sob a licença **MIT**.

---
🚀 **Desenvolvido para automação eficiente e confiável!**

