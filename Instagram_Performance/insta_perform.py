import pandas as pd
from datetime import datetime
import os

# Obtém a data atual no formato DIA/MÊS/ANO
data_atual = datetime.now().strftime("%d/%m/%Y")
print(f"📅 Data atual: {data_atual}\n")

# Nomes dos arquivos de armazenamento
ARQUIVO_CSV = "history.csv"
ARQUIVO_EXCEL = "history.xlsx"

# -----------------------------------------------------
#  CARREGAMENTO AUTOMÁTICO DOS ARQUIVOS
# -----------------------------------------------------
if os.path.exists(ARQUIVO_CSV):
    history = pd.read_csv(ARQUIVO_CSV)
else:
    history = pd.DataFrame(columns=["nome", "data"])

print("\n=== CADASTRO DE USUÁRIOS VISUALIZADORES ===\n")
print("Digite 'help' para ver a lista de comandos disponíveis.\n")


# -----------------------------------------------------
# Função para verificar se o usuário digitou "voltar"
# -----------------------------------------------------
def verificar_voltar(texto):
    """Retorna True se o usuário digitou 'voltar'."""
    if texto.strip().lower() == "voltar":
        print("\n↩ Retornando ao menu principal...\n")
        return True
    return False


# -----------------------------------------------------
# Função para transformar formato nome/data -> colunas por data
# -----------------------------------------------------
def transformar_por_data(history):
    """
    Transforma o DataFrame no formato:
    Cada data vira uma coluna e os nomes ficam em linhas.
    """
    if history.empty:
        return pd.DataFrame()

    # Agrupa os nomes por data
    agrupado = history.groupby("data")["nome"].apply(list)

    # Maior número de nomes em uma data
    max_len = max(len(lista) for lista in agrupado)

    # Criação da tabela organizada
    tabela = {
        data: nomes + [""] * (max_len - len(nomes))
        for data, nomes in agrupado.items()
    }

    return pd.DataFrame(tabela)


# -----------------------------------------------------
# Função para salvar CSV e Excel
# -----------------------------------------------------
def salvar_arquivos():
    """Salva o DataFrame em CSV e Excel simultaneamente."""
    history.to_csv(ARQUIVO_CSV, index=False)
    history.to_excel(ARQUIVO_EXCEL, index=False)
    print("💾 Arquivos CSV e Excel atualizados automaticamente.\n")


# -----------------------------------------------------
# LOOP PRINCIPAL DO SISTEMA
# -----------------------------------------------------
while True:

    comando = input(">>> ").lower().strip()

    if comando == "help":
        print("""
Comandos disponíveis:
help          - Mostra esta lista de comandos
info          - Exibe informações do sistema
cadastrar     - Cadastra usuários na tabela
visualizar    - Mostra os usuários cadastrados
data          - Mostra a data atual
salvar        - Salva manualmente os arquivos
limpar        - Limpa a tela do terminal
voltar        - Retorna ao menu principal
sair          - Encerra o terminal
""")

    elif comando == "info":
        print("Sistema de cadastro em terminal simulado V1.0\nAutor: Dionisio Martins\n")

    elif comando == "cadastrar":
        nome = input("\nCADASTRAR: ")

        if verificar_voltar(nome):
            continue

        # ---- IMPEDIR NOMES REPETIDOS ----
        if nome.lower() in history["nome"].str.lower().values:
            print(f"⚠ O nome '{nome}' já está cadastrado! Cadastro ignorado.\n")
            continue

        # ---- ADICIONAR NOVO REGISTRO ----
        history.loc[len(history)] = [nome, data_atual]

        # ---- LIMITAR A 30 REGISTROS (REMOVER OS MAIS ANTIGOS) ----
        if len(history) > 30:
            history.sort_values(by="data", inplace=True)
            history = history.iloc[-30:]  # mantém apenas os últimos 30
            history.reset_index(drop=True, inplace=True)
            print("⚠ Limite de 30 registros atingido. Cadastro mais antigo removido.")

        print(f"✔ Usuário '{nome}' cadastrado com sucesso!")

        salvar_arquivos()

    elif comando == "visualizar":
        print("\n=== TABELA DE CADASTRO (BRUTA) ===")
        print(history)
        print("\n=== TABELA ORGANIZADA POR DATA ===")
        print(transformar_por_data(history))
        print()

    elif comando == "data":
        print(f"📅 Data atual: {data_atual}\n")

    elif comando == "salvar":
        salvar_arquivos()

    elif comando == "sair":
        print("Encerrando o sistema...")
        break

    else:
        print("❌ Comando inválido. Digite 'help' para ver os comandos.\n")
