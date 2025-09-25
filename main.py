# Programa de Gerenciamento de Contatos Comerciais

print('Bem-Vindo à Lista de Contatos de Roberto Machado'.center(75))
print('-' * 74)
print('-' * 30 + ' Menu Principal ' + '-' * 28)
print('-' * 74)

# Lista global para armazenar os contatos
listaContatos = []

# Variável global_ID  aparatir desta gera o id automático
id_global = 5586954

# Chamada da função gerar Id para cada dicionario


def gerar_novo_id():
    global id_global
    novo_id = id_global
    id_global += 1
    return str(novo_id)

# Menu principal


def exibir_menu() -> str:
    while True:
        print('\nEscolha a Opção Desejada:\n')
        print('1 - Cadastrar Contato')
        print('2 - Consultar Contatos')
        print('3 - Remover Contatos')
        print('4 - Encerrar Programa')
        print('-' * 74)

        opcao = input("Digite a Opção: ").strip()

        if not opcao.isdigit():
            print("Entrada inválida! Digite apenas números (1 a 4).")
            continue

        if opcao == '1':
            return cadastrar_contatos
        elif opcao == '2':
            return sub_menu_consultar_contatos
        elif opcao == '3':
            return remover_contatos
        elif opcao == '4':
            print("Encerrando Programa ...")
            return None
        else:
            print("Opção inválida. Tente novamente!")

# Cadastro de contatos e tratatamento e função para cadastro


def cadastrar_contatos() -> None:
    while True:
        print("\nNovo Contato")

        while True:
            nome = input("Digite o nome: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        while True:
            sobrenome = input("Digite o sobrenome: ").strip()
            if sobrenome.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        while True:
            telefone = input("Digite o telefone (somente números): ").strip()
            if telefone.isdigit() and 8 <= len(telefone) <= 15:
                break
            print("Telefone inválido! Entre 8 e 15 dígitos.")

        while True:
            email = input("Digite seu e-mail: ").strip()
            if "@" in email and "." in email and " " not in email:
                break
            print("E-mail inválido! Digite no formato nome@dominio.com.")

        while True:
            atividade = input("Digite sua Atividade: ").strip()
            if atividade.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

# Dicionario  chave e valores
        contato = {
            "id": gerar_novo_id(),
            "nome": nome,
            "sobrenome": sobrenome,
            "telefone": telefone,
            "email": email,
            "atividade": atividade,
        }

        listaContatos.append(contato)
        print("\n Contato cadastrado com sucesso!")

        print("\nLista Atualizada de Contatos :")
        for c in listaContatos:
            print(f"ID: {c['id']} \n Nome: {c['nome']} {c['sobrenome']} \n "
                  f"Telefone: {c['telefone']} \n Email: {c['email']} \n Atividade: {c['atividade']}")

        continuar = input(
            "\nDeseja cadastrar outro contato? (s/n): ").strip().lower()
        if continuar != 's':
            break

# Submenu de consulta


def sub_menu_consultar_contatos():
    print('\nEscolha a Opção Desejada:\n')
    print('1 - Consultar Todos')
    print('2 - Consultar por ID')
    print('3 - Consultar por Atividade')
    print('4 - Retornar ao Menu')

    consulta = input("Digite 1, 2, 3 ou 4: ").strip()

    if consulta == '1':
        if not listaContatos:
            print("\nNenhum contato cadastrado.")
        else:
            print("\nLista de Contatos:\n")
            for contato in listaContatos:
                print(f"ID: {contato['id']} \n Nome: {contato['nome']} {contato['sobrenome']} \n "
                      f"Telefone: {contato['telefone']} \n Email: {contato['email']} \n Atividade: {contato['atividade']}")

    elif consulta == '2':
        id_busca = input("Digite o ID do contato: ").strip()
        for contato in listaContatos:
            if contato['id'] == id_busca:
                print("\nContato encontrado:")
                print(f"ID: {contato['id']} \n Nome: {contato['nome']} {contato['sobrenome']} \n "
                      f"Telefone: {contato['telefone']} \n Email: {contato['email']} \n Atividade: {contato['atividade']}")
                break
        else:
            print("Contato com esse ID não foi encontrado.")

    elif consulta == '3':
        atividade_busca = input(
            "Digite a atividade que deseja consultar: ").strip().lower()

        encontrados = [
            contato for contato in listaContatos if contato['atividade'].lower() == atividade_busca]

        if encontrados:
            print(f"\nContatos com atividade '{atividade_busca}':\n")
            for contato in encontrados:
                print(f"ID: {contato['id']} \n Nome: {contato['nome']} {contato['sobrenome']} \n "
                      f"Telefone: {contato['telefone']} \n Email: {contato['email']} \n Atividade: {contato['atividade']}")
        else:
            print("Nenhum contato com essa atividade foi encontrado.")

    elif consulta == '4':
        print("Retornando ao menu principal...")

    else:
        print("Opção inválida. Tente novamente!")


# Remoção de contatos
def remover_contatos():
    id_remover = input("Digite o ID do contato que deseja remover: ").strip()

    for i, contato in enumerate(listaContatos):
        if contato["id"] == id_remover:
            print(
                f"Contato encontrado: {contato['nome']} {contato['sobrenome']}")
            confirmacao = input(
                "Deseja remover este contato? (s/n): ").strip().lower()
            if confirmacao == 's':
                del listaContatos[i]
                print("Contato removido com sucesso!")
            else:
                print("Remoção cancelada.")
            break
    else:
        print("Contato com esse ID não encontrado.")


# Execução principal main
if __name__ == "__main__":

    while True:
        funcao_escolhida = exibir_menu()
        if funcao_escolhida is None:
            print("Programa encerrando...")
            break
        else:
            funcao_escolhida()
