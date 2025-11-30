import pandas as pd

usuarios = pd.DataFrame(columns=["nome"])

while True:

    nome = input("\nDigite o nome do usuario, (REMOVER) ou (ENTER) para sair: ").title().strip()

    if nome == "": # Sair se a entrada for vazia
        print("\nEncerrando o programa...\n")
        break
    
    if nome.lower() == "remover": # Iniciar processo de remoção
        nome_remover = input("\nDigite o nome do usuário que deseja remover: ").title().strip()

        if nome_remover in usuarios["nome"].values: # Verificar se o nome existe para remoção
            usuarios = usuarios[usuarios["nome"] != nome_remover] # Remove o usuário
            print(f"\nO nome '{nome_remover}' foi removido com sucesso\n")
            print("\nUSUÁRIOS ATUALIZADOS:\n")
            print(f"\nQuandidade de usuários cadastrados: {len(usuarios)}\n")
        else:
            print(f"\nO nome '{nome_remover}' não foi encontrado no cadastro. Tente novamente \n")
        continue 

    if nome in usuarios["nome"].values: # Verificar se o nome já existe
        print(f"\nO nome '{nome}' já existe no cadastro! Tente outro.\n")
        continue 
    
    # Adicionar novo usuário
    usuarios.loc[len(usuarios) + 1] = [nome]
    print(f"\nO nome '{nome}, foi cadastrado com sucesso!\n")
    print("\nUSUÁRIOS CADASTRADOS:")
    print(usuarios)
    print(f"\nQuandidade de usuários cadastrados: {len(usuarios)}\n")