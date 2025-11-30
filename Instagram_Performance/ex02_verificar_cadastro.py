import pandas as pd

usuarios = pd.DataFrame(columns=["Nome"])

while True:
    nome = input("Digite o nome para cadastrar ou (ENTER) para sair: ").strip().title()
    if nome == "":
        print("\nEncerrando o programa...\n")
        break
    
    if nome in usuarios.values:
        print(f" O nome '{nome}' já está cadastrado! Tente outro.\n")
    else:
        usuarios.loc[len(usuarios) + 1] = [nome]
        print(f"Nome '{nome}' cadastrado com sucesso!\n")
        print("\nUsuários cadastrados:")
        print(usuarios)