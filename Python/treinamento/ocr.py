import pytesseract
from PIL import Image
import json
import re

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    """Extrai texto da imagem usando OCR."""
    return pytesseract.image_to_string(Image.open(image_path))

def format_output_text(text):
    """Formata o texto removendo espaços extras e caracteres indesejados."""
    text = text.strip()
    text = re.sub(r'\n+', '\n', text)  # Remove múltiplas quebras de linha
    text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
    return text

def format_output_json(text):
    """Formata o texto extraído como JSON."""
    formatted_text = format_output_text(text)
    return json.dumps({"text_extracted": formatted_text}, indent=4, ensure_ascii=False)

def save_text_to_file(text, filename=r"C:\Users\ander\Downloads\output.txt"):
    """Salva o texto extraído em um arquivo TXT."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"\n✅ Texto salvo em {filename}")

if __name__ == "__main__":
    image_path = r"C:\Users\ander\Downloads\Projeto-100-Texto-19-1.png"
   
    extracted_text = extract_text(image_path)
    
    print("\n🔹 Texto Extraído (Bruto):\n")
    print(extracted_text)
    
    formatted_text = format_output_text(extracted_text)
    print("\n🔹 Texto Formatado:\n")
    print(formatted_text)
    
    json_output = format_output_json(extracted_text)
    print("\n🔹 Texto em JSON:\n")
    print(json_output)
    
    save_text_to_file(formatted_text)
