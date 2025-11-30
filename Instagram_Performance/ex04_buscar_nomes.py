import pandas as pd

usuarios = pd.DataFrame(columns=["nome"])

while True:
    nome = input("\nDigite o nome do usuario, (REMOVER), (BUSCAR) ou (ENTER) para sair: ").title().strip()

    if nome == "":
        print("\nEncerrando o programa...\n")
        break

    if nome.lower() == "remover":
        nome_remover = input("\nDigite o nome do usuário que deseja removar: ").title().strip()
        if nome_remover in usuarios["nome"].values:
            usuarios = usuarios[usuarios["nome"] != nome_remover]
            print(f"\nO nome '{nome_remover}' foi removido com sucesso\n")
            print("\nUSUÁRIOS ATUALIZADOS:\n")
            print(usuarios)
            print(f"\nQuantidade de usuários cadastrados: {len(usuarios)}\n")
        else:
            print(f"\nO nome '{nome_remover}' não foi encontrado no cadastro. Tente novamente \n")
        continue
    
    if nome.lower() == "buscar":
        nome_buscar = input("\nDigite a letra inicial para filtrar os nomes: ").title().upper().strip()
        nomes_encontrados = usuarios[usuarios["nome"].str.startswith(nome_buscar)] # Filtrar nomes que começam com a string fornecida
        print("\nNOMES ENCONTRADOS:\n")
        print(nomes_encontrados)
        print(f"\nQuantidade de nomes encontrados: {len(nomes_encontrados)}\n")
        continue

    if nome in usuarios["nome"].values:
        print(f"\nO nome '{nome}' já existe no cadastro! Tente outro.\n")
        continue

    usuarios.loc[len(usuarios) + 1] =  [nome]
    print(f"\nO nome '{nome}, foi cadastrado com sucesso!\n")
    print("\nUSUÁRIOS CADASTRADOS:")
    print(usuarios)
    print(f"\nQuantidade de usuários cadastrados: {len(usuarios)}\n")
