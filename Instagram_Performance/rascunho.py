import pandas as pd
from datetime import datetime
import os

# Nomes dos arquivos de armazenamento
ARQUIVO_CSV = "history.csv"
ARQUIVO_EXCEL = "history.xlsx"

# -----------------------------------------------------
#  CARREGAMENTO AUTOMÁTICO DOS ARQUIVOS
# -----------------------------------------------------
if os.path.exists(ARQUIVO_CSV):
    history = pd.read_csv(ARQUIVO_CSV, dtype=str)
    # Garante que existam as colunas esperadas
    if "nome" not in history.columns or "data" not in history.columns:
        history = pd.DataFrame(columns=["nome", "data"])
else:
    history = pd.DataFrame(columns=["nome", "data"])

print("\n=== CADASTRO DE USUÁRIOS VISUALIZADORES ===\n")
print("Digite 'help' para ver a lista de comandos disponíveis.\n")


# -----------------------------------------------------
# Função para verificar se o usuário digitou "voltar"
# -----------------------------------------------------
def verificar_voltar(texto):
    """Retorna True se o usuário digitou 'voltar'."""
    if texto is None:
        return False
    if texto.strip().lower() == "voltar":
        print("\n↩ Retornando ao menu principal...\n")
        return True
    return False


# -----------------------------------------------------
# Função para excluir um nome (retorna history atualizado)
# -----------------------------------------------------
def excluir_nome(history_df, nome):
    """Exclui um nome do DataFrame se existir e retorna o DataFrame atualizado."""
    nome = nome.title().strip()
    # busca case-insensitive e strip para maior robustez
    matches = history_df["nome"].str.strip().str.lower() == nome.strip().lower()
    if matches.any():
        history_df = history_df.loc[~matches].reset_index(drop=True)
        print(f"✔ O nome '{nome}' foi excluído com sucesso!\n")
        salvar_arquivos(history_df)
    else:
        print(f"⚠ O nome '{nome}' não foi encontrado no cadastro.\n")
    return history_df


# -----------------------------------------------------
# Função para transformar formato nome/data -> colunas por data
# -----------------------------------------------------
def transformar_por_data(history_df):
    """
    Transforma o DataFrame no formato:
    Cada data vira uma coluna e os nomes ficam em linhas.
    """
    if history_df.empty:
        return pd.DataFrame()

    agrupado = history_df.groupby("data")["nome"].apply(list)
    max_len = max(len(lista) for lista in agrupado)

    tabela = {
        data: nomes + [""] * (max_len - len(nomes))
        for data, nomes in agrupado.items()
    }

    return pd.DataFrame(tabela)


# -----------------------------------------------------
# Função para salvar CSV e Excel (recebe history como argumento)
# -----------------------------------------------------
def salvar_arquivos(history_df):
    """Salva o DataFrame em CSV e Excel simultaneamente."""
    try:
        history_df.to_csv(ARQUIVO_CSV, index=False)
        history_df.to_excel(ARQUIVO_EXCEL, index=False)
        print("💾 Arquivos CSV e Excel atualizados automaticamente.\n")
    except Exception as e:
        print(f"⚠ Erro ao salvar arquivos: {e}\n")


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
excluir       - Exclui um usuário cadastrado
visualizar    - Mostra os usuários cadastrados
Procurar      - Procura arquivos de cadastro existentes
data          - Mostra a data atual
salvar        - Salva manualmente os arquivos
limpar        - Limpa a tela do terminal
voltar        - Retorna ao menu principal (quando em submenus)
sair          - Encerra o terminal
""")

    elif comando == "info":
        print("Sistema de cadastro em terminal simulado V1.0\nAutor: Dionisio Martins\n")

    elif comando == "cadastrar":
        original = input("\nCADASTRAR (ou digite 'voltar' para cancelar): ").strip()
        if verificar_voltar(original):
            continue

        nome = original.title().strip()
        # ---- IMPEDIR NOMES REPETIDOS (case-insensitive, strip) ----
        if (history["nome"].str.strip().str.lower() == nome.strip().lower()).any():
            print(f"⚠ O nome '{nome}' já está cadastrado! Cadastro ignorado.\n")
            continue

        # ---- ADICIONAR NOVO REGISTRO (usando data atual no momento do cadastro) ----
        data_atual = datetime.now().strftime("%d/%m/%Y")
        history.loc[len(history)] = [nome, data_atual]

        # ---- LIMITAR A 30 REGISTROS (REMOVER OS MAIS ANTIGOS) ----
        if len(history) > 30:
            # tenta ordenar por data com formato dd/mm/YYYY -> converte para datetime para ordenar corretamente
            try:
                history["__dt"] = pd.to_datetime(history["data"], format="%d/%m/%Y", errors="coerce")
                history.sort_values(by="__dt", inplace=True)
                history.drop(columns="__dt", inplace=True)
            except Exception:
                # fallback: ordena pela string (pior, mas evita crash)
                history.sort_values(by="data", inplace=True)
            history = history.iloc[-30:].reset_index(drop=True)
            print("⚠ Limite de 30 registros atingido. Cadastro mais antigo removido.")

        print(f"✔ Usuário '{nome}' cadastrado com sucesso!")
        salvar_arquivos(history)

    elif comando == "excluir":
        if history.empty:
            print("\nNenhum usuário cadastrado.\n")
            continue

        print("\nTabela de usuários cadastrados:")
        print(history)
        nome_excluir = input("\nDIGITE O NOME QUE DESEJA EXCLUIR (ou 'voltar'): ").strip()
        if verificar_voltar(nome_excluir):
            continue
        history = excluir_nome(history, nome_excluir)

    elif comando == "visualizar":
        if history.empty:
            print("\n=== TABELA DE CADASTRO (BRUTA) ===")
            print("Nenhum usuário cadastrado.\n")
            print("\n=== TABELA ORGANIZADA POR DATA ===")
            print("Nenhum usuário cadastrado.\n")
        else:
            print("\n=== TABELA DE CADASTRO (BRUTA) ===")
            print(history)
            print("\n=== TABELA ORGANIZADA POR DATA ===")
            print(transformar_por_data(history))

    elif comando == "procurar":
        print("\nPROCURANDO EXTENSÕES DE ARQUIVOS SUPORTADOS...\n")

        import glob

        padroes = ["*.csv", "*.xlsx", "*.txt"]
        arquivos_encontrados = False

        for padrao in padroes:
            for arquivo in glob.glob(padrao):
                print(f"📂 Arquivo encontrado: {arquivo}")
                arquivos_encontrados = True
        arquivo = input("\nACESSAR ARQUIVO: ").strip()
        
        if not arquivos_encontrados:
            print("⚠ Nenhum arquivo encontrado.\n")
            continue

    elif comando == "data":
        data_atual = datetime.now().strftime("%d/%m/%Y")
        print(f"📅 Data atual: {data_atual}\n")

    elif comando == "salvar":
        salvar_arquivos(history)

    elif comando == "limpar":
        # Limpa a tela do terminal de forma cross-platform
        os.system("cls" if os.name == "nt" else "clear")

    elif comando == "sair":
        print("Encerrando o sistema...")
        break

    else:
        print("❌ Comando inválido. Digite 'help' para ver os comandos.\n")
