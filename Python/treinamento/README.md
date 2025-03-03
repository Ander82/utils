# 📌 RPA Orquestrador - Guia de Bibliotecas e Automação 🚀

![Automação RPA](https://source.unsplash.com/800x300/?automation,technology)

# 📌 Documentação de Bibliotecas para Automação RPA

## 📖 Introdução 🏗️
Esta documentação cobre bibliotecas essenciais para **automação de aplicações web, leitura de documentos, automação SAP GUI/SAP Fiori** e tarefas complementares como **OCR, CAPTCHA, automação de elementos visuais e manipulação de Excel**.

---
## 🌐 1️⃣ Bibliotecas para Automação Web
Essas bibliotecas são essenciais para **automação de aplicações web**, como interagir com sites, manipular APIs e simular ações do usuário.

### **📌 Selenium**  
🔗 [Documentação Oficial](https://www.selenium.dev/documentation/)  
**Motivação:** Permite automação de navegadores, facilitando interações com páginas web para preenchimento de formulários, cliques e extração de dados.

**Instalação:**
```sh
pip install selenium
```
**Exemplo:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicia o navegador
driver = webdriver.Chrome()
driver.get("https://www.google.com")

# Encontra um elemento e interage
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Automação com Selenium")
search_box.submit()
```

### **📌 Requests**  
🔗 [Documentação Oficial](https://docs.python-requests.org/en/latest/)  
**Motivação:** Facilita chamadas a APIs e interações com páginas via HTTP, sem precisar carregar um navegador.

**Instalação:**
```sh
pip install requests
```
**Exemplo:**
```python
import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts")
print(response.json())
```

### **📌 BeautifulSoup**  
🔗 [Documentação Oficial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
**Motivação:** Permite **parsear HTML** de forma eficiente para **extração de dados de páginas web**.

**Instalação:**
```sh
pip install beautifulsoup4
```
**Exemplo:**
```python
from bs4 import BeautifulSoup
import requests

html = requests.get("https://example.com").text
soup = BeautifulSoup(html, "html.parser")
print(soup.title.text)
```

---
## 📄 2️⃣ Bibliotecas para Leitura de Documentos
Essas bibliotecas ajudam na **extração de informações de documentos como PDFs e imagens**.

### **📌 PyPDF2**  
🔗 [Documentação Oficial](https://pypdf2.readthedocs.io/en/latest/)  
**Motivação:** Permite ler e manipular **arquivos PDF**.

**Instalação:**
```sh
pip install PyPDF2
```
**Exemplo:**
```python
import PyPDF2

with open("documento.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        print(page.extract_text())
```

### **📌 Tesseract OCR**  
🔗 [Documentação Oficial](https://tesseract-ocr.github.io/tessdoc/)  
**Motivação:** Utilizado para **reconhecimento óptico de caracteres (OCR)** em imagens.

**Instalação:**
```sh
pip install pytesseract
```
**Exemplo:**
```python
import pytesseract
from PIL import Image

img = Image.open("imagem.png")
text = pytesseract.image_to_string(img)
print(text)
```

---
## 🏢 3️⃣ Automação SAP GUI
Essas bibliotecas facilitam a automação do **SAP GUI**, permitindo manipular telas e interagir com campos.

### **📌 Pywinauto**  
🔗 [Documentação Oficial](https://pywinauto.readthedocs.io/en/latest/)  
**Motivação:** Permite automatizar aplicações Windows, incluindo o **SAP GUI**.

**Instalação:**
```sh
pip install pywinauto
```
**Exemplo:**
```python
from pywinauto import Application

app = Application().start("saplogon.exe")
window = app.window(title="SAP Logon")
window.print_control_identifiers()
```

---
## 🔄 4️⃣ Automação SAP Fiori
Para aplicações SAP Fiori, que rodam no navegador, podemos usar **Selenium** e ferramentas de **gravação de elementos**.

### **📌 Recorder Elements**
**Motivação:** Ferramentas como **FlaUI** ajudam na captura de elementos para automação de interfaces web.

**Exemplo de automação SAP Fiori via Selenium:**
```python
from selenium import webdriver

# Abre o navegador e acessa SAP Fiori
driver = webdriver.Chrome()
driver.get("https://sapfiori.example.com")

# Interage com elementos
driver.find_element(By.ID, "username").send_keys("usuario")
driver.find_element(By.ID, "password").send_keys("senha")
driver.find_element(By.ID, "loginBtn").click()
```

---
## 📊 5️⃣ Manipulação de Planilhas Excel
O **OpenPyXL** permite manipular planilhas Excel **sem precisar instalar o Excel na máquina**.

### **📌 OpenPyXL**  
🔗 [Documentação Oficial](https://openpyxl.readthedocs.io/en/stable/)  
**Motivação:** Manipular e editar planilhas Excel.

**Instalação:**
```sh
pip install openpyxl
```
**Exemplo:**
```python
import openpyxl

# Criar uma nova planilha
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "Dados"
sheet["A1"] = "Nome"
sheet["B1"] = "Idade"

# Salvar
wb.save("dados.xlsx")
```

### **📌 Melhorando Função para Escrever no Excel**
Podemos criar uma **função dinâmica para inserir novos dados** de forma fácil.

```python
def escrever_excel(arquivo, dados):
    wb = openpyxl.load_workbook(arquivo)
    sheet = wb.active
    sheet.append(dados)  # Adiciona na próxima linha disponível
    wb.save(arquivo)
```

**Uso:**
```python
escrever_excel("dados.xlsx", ["Maria", 30])
escrever_excel("dados.xlsx", ["João", 25])
```

---
## 💡 6️⃣ Recursos Adicionais e Dicas

### **AutoIt**  
🔗 [Documentação Oficial](https://www.autoitscript.com/site/autoit/)  
**Motivação:** Permite automação de janelas e interações em aplicações Windows que não possuem APIs abertas.  
**Exemplo:**
```autoit
WinWaitActive("Janela de Login")
Send("meu_usuario{TAB}minha_senha{ENTER}")
```

### **Tracker (STSchnell)**  
🔗 [Documentação Oficial](https://tracker.stschnell.de/)  
**Motivação:** Ferramenta avançada para **captura e rastreamento de elementos visuais** em automações RPA.  
**Exemplo de rastreamento de elemento:**  
```python
import tracker
# Código para rastreamento de um botão ou elemento gráfico na tela
```

### **OCR e Tesseract**
- OCR permite extrair **texto de imagens**.
- Tesseract OCR funciona bem, mas pode exigir **tratamento da imagem** para melhorar a precisão.

### **CAPTCHA e 2Captcha**
- Captchas podem ser resolvidos manualmente ou usando **APIs como 2Captcha**.
- Alguns CAPTCHAs são mais complexos e exigem soluções mais avançadas (ex: ReCaptcha V3).

### **Headless Browsers**
- O modo **headless** permite rodar navegadores sem interface gráfica.
- Pode ser ativado no **Selenium** com:
```python
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
```

### **PyAutoGUI e Automação Visual**  
🔗 [Documentação Oficial](https://pyautogui.readthedocs.io/en/latest/)  
- Usado para **clicar em botões**, digitar textos e interagir com janelas **sem APIs nativas**.
- Exemplo:
```python
import pyautogui
pyautogui.click(100, 200)  # Clica nas coordenadas (100, 200)
```

---
## **📌 Conclusão**
Esta documentação cobre as principais bibliotecas para **automação de web, SAP GUI, SAP Fiori, manipulação de documentos e planilhas**. A escolha das ferramentas depende do escopo do projeto e da complexidade da automação.

🚀 **Agora você tem um guia completo para criar automações RPA eficientes!**

