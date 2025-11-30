import pandas as pd
import os
import glob

nomes = []

print("\nBUSCANDO ARQUIVOS USPORTADOS NO SISTEMA...\n")

extensao = ["*.csv", "*.xlsx", "*.txt"]
arquivos_encontrados = False

for padrao in extensao:
    for arquivo in glob.glob(padrao):
        print(f"📂 Arquivo encontrado: {arquivo}")
        arquivos_encontrados = True

if not arquivos_encontrados:
    print("⚠ Nenhum arquivo encontrado.\n")

acessar_arquivo = input("\nDIGITE O NOME DO ARQUIVO QUE DESEJA ACESSAR: ").strip()
if not os.path.isfile(acessar_arquivo):
    print(f"\n⚠ O arquivo '{acessar_arquivo}' não foi encontrado.\n")
else:
    if acessar_arquivo.endswith(".csv"):
        df = pd.read_csv(acessar_arquivo)
    elif acessar_arquivo.endswith(".xlsx"):
        df = pd.read_excel(acessar_arquivo)
    elif acessar_arquivo.endswith(".txt"):
        nomes = []
        with open(acessar_arquivo, "r", encoding="utf-8") as file:
            for line in file:
                linha = line.strip()
                if linha:                   # IGNORA LINHAS VAZIAS
                    nomes.append(linha)
        
        df = pd.DataFrame(nomes, columns=["nome"], index=range(1, len(nomes)+1))

    # --------------------------
    # REMOVER LINHAS VAZIAS
    # --------------------------
        df = df.dropna().reset_index(drop=True)

        print("\n📊 ARQUIVO CARREGADO COM SUCESSO!")
        print(df)
        print(f"\nQuantidade de nomes carregados: {len(df)}\n")
