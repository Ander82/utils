import openpyxl

def criar_excel(nome_arquivo):
    """Cria um novo arquivo Excel e adiciona dados."""
    # Criar um novo workbook e uma planilha ativa
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dados"

    # Adicionando cabeçalhos
    ws.append(["ID", "Nome", "Idade"])

    # Adicionando alguns dados de exemplo
    dados = [
        [1, "Anderson", 30],
        [2, "Maria", 25],
        [3, "Carlos", 40]
    ]

    for linha in dados:
        ws.append(linha)
    
    # Escrever na coluna M, posição 3
    ws["M3"] = "Novo Dado"

    # Salvando o arquivo
    wb.save(nome_arquivo)
    print(f"Arquivo Excel '{nome_arquivo}' criado com sucesso!")

if __name__ == "__main__":
    criar_excel("treinamento.xlsx")
