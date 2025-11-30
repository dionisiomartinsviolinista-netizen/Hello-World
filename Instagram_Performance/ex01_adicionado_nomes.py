import pandas as pd

usuarios = pd.DataFrame(columns=["nome"])

while True:
    nome = input("\nDigite o nome do usuário ou (ENTER) para sair: ").strip().title()
    if nome == "":
        print("\nEncerrando o programa...\n")
        break
    else:
       # usuarios = pd.concat([usuarios, pd.DataFrame({"nome": [nome]})], ignore_index=True)
        usuarios.loc[len(usuarios) + 1] = [nome]
        print(f"Usuário {nome} adicionado com sucesso!\n")
        print(usuarios)
