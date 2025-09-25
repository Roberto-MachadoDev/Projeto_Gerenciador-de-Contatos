<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

# Programa de Gerenciamento de Contatos Comerciais
=======
import json
import os
from datetime import datetime
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
import json
import os
from datetime import datetime
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
import json
import os
from datetime import datetime
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)

# -------- Configurações ----------
PASTA_GDC = os.path.join(os.path.expanduser("~"), "GDC")
os.makedirs(PASTA_GDC, exist_ok=True)
ARQUIVO_JSON = os.path.join(PASTA_GDC, "contatos.json")

# mensagens iniciais
print('Bem-Vindo à Lista de Contatos de Roberto Machado'.center(75))
print('_' * 74)
print('_' * 30 + ' Menu Principal ' + '_' * 28)
print('_' * 74)


# ---------- I/O (carregar / salvar) ----------------
def salvar_contatos():
    """Salva listaContatos no JSON (variável global listaContatos)."""
    try:
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(listaContatos, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print("Erro ao salvar arquivo:", e)


def carregar_contatos():
    """
    Carrega o JSON e normaliza cada registro para garantir as chaves esperadas.
    Retorna lista de contatos (cada um é dict com chaves: id, nome, sobrenome, telefone, email, atividade).
    """
    if not os.path.exists(ARQUIVO_JSON):
        return []

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(
            f"Aviso: {ARQUIVO_JSON} parece corrompido ({e}). Usando lista vazia.")
        return []
    except OSError as e:
        print(f"Aviso ao abrir {ARQUIVO_JSON}: {e}")
        return []

    if not isinstance(data, list):
        print("Formato inesperado no JSON (esperado lista). Ignorando conteúdo e iniciando vazio.")
        return []

    contatos = []
    for item in data:
        if not isinstance(item, dict):
            print("Aviso: registro inválido (não é objeto) ignorado:", item)
            continue

        # Normalizar chaves: mapear todas para lowercase sem espaços
        normalized = {k.strip().lower(): v for k,
                      v in item.items() if isinstance(k, str)}

        nome = normalized.get('nome') or normalized.get(
            'name') or normalized.get('nome_completo') or ""
        sobrenome = normalized.get(
            'sobrenome') or normalized.get('lastname') or ""
        telefone = normalized.get('telefone') or normalized.get('phone') or ""
        email = normalized.get('email') or normalized.get(
            'e-mail') or normalized.get('mail') or ""
        atividade = normalized.get('atividade') or normalized.get(
            'ocupacao') or normalized.get('role') or ""

        # id pode existir e ser número ou string
        id_raw = normalized.get('id')
        id_str = str(id_raw) if id_raw is not None and id_raw != "" else None

        contatos.append({
            "id": id_str,
            "nome": nome,
            "sobrenome": sobrenome,
            "telefone": telefone,
            "email": email,
            "atividade": atividade
        })

    return contatos


# ---------- Gerenciamento de IDs ----------
def gerar_novo_id():
    global id_global
    novo = id_global
    id_global += 1
    return str(novo)


# Carrega e normaliza contatos do disco
listaContatos = carregar_contatos()

# Calcula id_global baseado em ids válidos já existentes (somente inteiros)
existing_ids = []
for c in listaContatos:
    try:
        if c.get('id') not in (None, ""):
            existing_ids.append(int(c['id']))
    except (ValueError, TypeError):
        # id não-numérico: será substituído abaixo
        pass

id_global = 5586954 if not existing_ids else max(existing_ids) + 1

# Atribui ids faltantes e garante que todos os ids sejam string
changed = False
for c in listaContatos:
    if not c.get('id'):
        c['id'] = gerar_novo_id()
        changed = True
    else:
        c['id'] = str(c['id'])

# Se fizemos alterações (atribuição de ids), salvamos para atualizar o arquivo
if changed:
    # opcional: criar backup antes de sobrescrever
    try:
        backup_path = ARQUIVO_JSON + ".backup-" + \
            datetime.now().strftime("%Y%m%d%H%M%S")
        if os.path.exists(ARQUIVO_JSON):
            os.replace(ARQUIVO_JSON, backup_path)
            print("Backup do JSON criado em:", backup_path)
    except Exception:
        pass
    salvar_contatos()


# ---------- Funções de exibição e menu ----------
def exibir_contato(contato):
    """Exibe um contato sem gerar KeyError (usa get com defaults)."""
    print(f"\nID: {contato.get('id', '<sem id>')}")
    nome = contato.get('nome') or "<sem nome>"
    sobrenome = contato.get('sobrenome') or ""
    print(f"Nome: {nome} {sobrenome}".strip())
    print(f"Telefone: {contato.get('telefone', '')}")
    print(f"Email: {contato.get('email', '')}")
    print(f"Atividade: {contato.get('atividade', '')}")


def exibir_menu() -> str:
    while True:
        print('\nEscolha a Opção Desejada:\n')
        print('1 - Cadastrar Contato')
        print('2 - Consultar Contatos')
        print('3 - Remover Contatos')
        print('4 - Encerrar Programa')
        print('_' * 74)

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


# ---------- CRUD ----------
def cadastrar_contatos() -> None:
    while True:
        print("\n Novo Contato")

        # Nome
        while True:
            nome = input("Digite o nome ou 'sair' para cancelar: ").strip()
            if nome.upper() == "SAIR":
                return
            if nome.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        # Sobrenome
        while True:
            sobrenome = input(
                "Digite o sobrenome ou 'sair' para cancelar: ").strip()
            if sobrenome.upper() == "SAIR":
                return
            if sobrenome.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        # Telefone
        while True:
            telefone = input(
                "Digite o telefone ou 'sair' para cancelar: ").strip()
            if telefone.upper() == "SAIR":
                return
            if telefone.isdigit() and 8 <= len(telefone) <= 15:
                break
            print("Telefone inválido! Entre 8 e 15 dígitos.")

        # Email
        while True:
            email = input(
                "Digite seu e-mail ou 'sair' para cancelar: ").strip()
            if email.upper() == "SAIR":
                return
            if "@" in email and "." in email and " " not in email:
                break
            print("E-mail inválido! Digite no formato nome@dominio.com.")

        # Atividade
        while True:
            atividade = input(
                "Digite a atividade ou 'sair' para cancelar: ").strip()
            if atividade.upper() == "SAIR":
                return
            if atividade.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        # Criar contato
        contato = {
            "id": gerar_novo_id(),
            "nome": nome,
            "sobrenome": sobrenome,
            "telefone": telefone,
            "email": email,
            "atividade": atividade,
        }

        listaContatos.append(contato)
        salvar_contatos()  # salvar ao cadastrar

        print("\nContato cadastrado com sucesso!")
        exibir_contato(contato)

        continuar = input(
            "\nDeseja cadastrar outro contato? (s/n): ").strip().lower()
        if continuar != 's':
            break


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
                exibir_contato(contato)

    elif consulta == '2':
        id_busca = input("Digite o ID do contato: ").strip()
        for contato in listaContatos:
            if contato.get('id') == id_busca:
                print("\nContato encontrado:")
                exibir_contato(contato)
                break
        else:
            print("Contato com esse ID não foi encontrado.")

    elif consulta == '3':
        atividade_busca = input(
            "Digite a atividade que deseja consultar: ").strip().lower()
        encontrados = [c for c in listaContatos if c.get(
            "atividade", "").lower() == atividade_busca]

        if encontrados:
            print(f"\nContatos com atividade '{atividade_busca}':\n")
            for contato in encontrados:
                exibir_contato(contato)
        else:
            print("Nenhum contato com essa atividade foi encontrado.")

    elif consulta == '4':
        print("Retornando ao menu principal...")
    else:
        print("Opção inválida. Tente novamente!")


def remover_contatos():
    id_remover = input("Digite o ID do contato que deseja remover ou sair para sair: ").strip()
     
    for i, contato in enumerate(listaContatos):
        if contato.get("id") == id_remover:
            print("\nContato encontrado:")
            exibir_contato(contato)
            if id_remover =='sair':
             break
            confirmacao = input(
                "Deseja remover este contato? (s/n): ").strip().lower()
            if confirmacao == 's':
                del listaContatos[i]
                salvar_contatos()
                print("Contato removido com sucesso!")
            else:
                print("Remoção cancelada.")
            break
    else:
        print("Contato com esse ID não encontrado.")


# ---------- Execução ----------
if __name__ == "__main__":
    while True:
        funcao_escolhida = exibir_menu()
        if funcao_escolhida is None:
            break
        else:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            funcao_escolhida()

# Programa de Gerenciamento de Contatos Comerciais
=======
import json
import os
from datetime import datetime
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)

# -------- Configurações ----------
PASTA_GDC = os.path.join(os.path.expanduser("~"), "GDC")
os.makedirs(PASTA_GDC, exist_ok=True)
ARQUIVO_JSON = os.path.join(PASTA_GDC, "contatos.json")

# mensagens iniciais
print('Bem-Vindo à Lista de Contatos de Roberto Machado'.center(75))
print('_' * 74)
print('_' * 30 + ' Menu Principal ' + '_' * 28)
print('_' * 74)


# ---------- I/O (carregar / salvar) ----------------
def salvar_contatos():
    """Salva listaContatos no JSON (variável global listaContatos)."""
    try:
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(listaContatos, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print("Erro ao salvar arquivo:", e)


def carregar_contatos():
    """
    Carrega o JSON e normaliza cada registro para garantir as chaves esperadas.
    Retorna lista de contatos (cada um é dict com chaves: id, nome, sobrenome, telefone, email, atividade).
    """
    if not os.path.exists(ARQUIVO_JSON):
        return []

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(
            f"Aviso: {ARQUIVO_JSON} parece corrompido ({e}). Usando lista vazia.")
        return []
    except OSError as e:
        print(f"Aviso ao abrir {ARQUIVO_JSON}: {e}")
        return []

    if not isinstance(data, list):
        print("Formato inesperado no JSON (esperado lista). Ignorando conteúdo e iniciando vazio.")
        return []

    contatos = []
    for item in data:
        if not isinstance(item, dict):
            print("Aviso: registro inválido (não é objeto) ignorado:", item)
            continue

        # Normalizar chaves: mapear todas para lowercase sem espaços
        normalized = {k.strip().lower(): v for k,
                      v in item.items() if isinstance(k, str)}

        nome = normalized.get('nome') or normalized.get(
            'name') or normalized.get('nome_completo') or ""
        sobrenome = normalized.get(
            'sobrenome') or normalized.get('lastname') or ""
        telefone = normalized.get('telefone') or normalized.get('phone') or ""
        email = normalized.get('email') or normalized.get(
            'e-mail') or normalized.get('mail') or ""
        atividade = normalized.get('atividade') or normalized.get(
            'ocupacao') or normalized.get('role') or ""

        # id pode existir e ser número ou string
        id_raw = normalized.get('id')
        id_str = str(id_raw) if id_raw is not None and id_raw != "" else None

        contatos.append({
            "id": id_str,
            "nome": nome,
            "sobrenome": sobrenome,
            "telefone": telefone,
            "email": email,
            "atividade": atividade
        })

    return contatos


# ---------- Gerenciamento de IDs ----------
def gerar_novo_id():
    global id_global
    novo = id_global
    id_global += 1
    return str(novo)


# Carrega e normaliza contatos do disco
listaContatos = carregar_contatos()

# Calcula id_global baseado em ids válidos já existentes (somente inteiros)
existing_ids = []
for c in listaContatos:
    try:
        if c.get('id') not in (None, ""):
            existing_ids.append(int(c['id']))
    except (ValueError, TypeError):
        # id não-numérico: será substituído abaixo
        pass

id_global = 5586954 if not existing_ids else max(existing_ids) + 1

# Atribui ids faltantes e garante que todos os ids sejam string
changed = False
for c in listaContatos:
    if not c.get('id'):
        c['id'] = gerar_novo_id()
        changed = True
    else:
        c['id'] = str(c['id'])

# Se fizemos alterações (atribuição de ids), salvamos para atualizar o arquivo
if changed:
    # opcional: criar backup antes de sobrescrever
    try:
        backup_path = ARQUIVO_JSON + ".backup-" + \
            datetime.now().strftime("%Y%m%d%H%M%S")
        if os.path.exists(ARQUIVO_JSON):
            os.replace(ARQUIVO_JSON, backup_path)
            print("Backup do JSON criado em:", backup_path)
    except Exception:
        pass
    salvar_contatos()


# ---------- Funções de exibição e menu ----------
def exibir_contato(contato):
    """Exibe um contato sem gerar KeyError (usa get com defaults)."""
    print(f"\nID: {contato.get('id', '<sem id>')}")
    nome = contato.get('nome') or "<sem nome>"
    sobrenome = contato.get('sobrenome') or ""
    print(f"Nome: {nome} {sobrenome}".strip())
    print(f"Telefone: {contato.get('telefone', '')}")
    print(f"Email: {contato.get('email', '')}")
    print(f"Atividade: {contato.get('atividade', '')}")


def exibir_menu() -> str:
    while True:
        print('\nEscolha a Opção Desejada:\n')
        print('1 - Cadastrar Contato')
        print('2 - Consultar Contatos')
        print('3 - Remover Contatos')
        print('4 - Encerrar Programa')
        print('_' * 74)

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


# ---------- CRUD ----------
def cadastrar_contatos() -> None:
    while True:
        print("\n Novo Contato")

        # Nome
        while True:
            nome = input("Digite o nome ou 'sair' para cancelar: ").strip()
            if nome.upper() == "SAIR":
                return
            if nome.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        # Sobrenome
        while True:
            sobrenome = input(
                "Digite o sobrenome ou 'sair' para cancelar: ").strip()
            if sobrenome.upper() == "SAIR":
                return
            if sobrenome.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        # Telefone
        while True:
            telefone = input(
                "Digite o telefone ou 'sair' para cancelar: ").strip()
            if telefone.upper() == "SAIR":
                return
            if telefone.isdigit() and 8 <= len(telefone) <= 15:
                break
            print("Telefone inválido! Entre 8 e 15 dígitos.")

        # Email
        while True:
            email = input(
                "Digite seu e-mail ou 'sair' para cancelar: ").strip()
            if email.upper() == "SAIR":
                return
            if "@" in email and "." in email and " " not in email:
                break
            print("E-mail inválido! Digite no formato nome@dominio.com.")

        # Atividade
        while True:
            atividade = input(
                "Digite a atividade ou 'sair' para cancelar: ").strip()
            if atividade.upper() == "SAIR":
                return
            if atividade.replace(" ", "").isalpha():
                break
            print("Entrada inválida! Digite apenas letras.")

        # Criar contato
        contato = {
            "id": gerar_novo_id(),
            "nome": nome,
            "sobrenome": sobrenome,
            "telefone": telefone,
            "email": email,
            "atividade": atividade,
        }

        listaContatos.append(contato)
        salvar_contatos()  # salvar ao cadastrar

        print("\nContato cadastrado com sucesso!")
        exibir_contato(contato)

        continuar = input(
            "\nDeseja cadastrar outro contato? (s/n): ").strip().lower()
        if continuar != 's':
            break


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
                exibir_contato(contato)

    elif consulta == '2':
        id_busca = input("Digite o ID do contato: ").strip()
        for contato in listaContatos:
            if contato.get('id') == id_busca:
                print("\nContato encontrado:")
                exibir_contato(contato)
                break
        else:
            print("Contato com esse ID não foi encontrado.")

    elif consulta == '3':
        atividade_busca = input(
            "Digite a atividade que deseja consultar: ").strip().lower()
        encontrados = [c for c in listaContatos if c.get(
            "atividade", "").lower() == atividade_busca]

        if encontrados:
            print(f"\nContatos com atividade '{atividade_busca}':\n")
            for contato in encontrados:
                exibir_contato(contato)
        else:
            print("Nenhum contato com essa atividade foi encontrado.")

    elif consulta == '4':
        print("Retornando ao menu principal...")
    else:
        print("Opção inválida. Tente novamente!")


def remover_contatos():
    id_remover = input("Digite o ID do contato que deseja remover ou sair para sair: ").strip()
     
    for i, contato in enumerate(listaContatos):
        if contato.get("id") == id_remover:
            print("\nContato encontrado:")
            exibir_contato(contato)
            if id_remover =='sair':
             break
            confirmacao = input(
                "Deseja remover este contato? (s/n): ").strip().lower()
            if confirmacao == 's':
                del listaContatos[i]
                salvar_contatos()
                print("Contato removido com sucesso!")
            else:
                print("Remoção cancelada.")
            break
    else:
        print("Contato com esse ID não encontrado.")


# ---------- Execução ----------
if __name__ == "__main__":
    while True:
        funcao_escolhida = exibir_menu()
        if funcao_escolhida is None:
            break
        else:
<<<<<<< HEAD
            funcao_escolhida()
>>>>>> > b9caaeb(Primeiro commit do projeto Python)
=======
=======
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
            try:
                funcao_escolhida()
            except Exception as e:
                print("Ocorreu um erro durante a execução:", e)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
=======
>>>>>>> 20a8532 (Adicionei condição para sair do fluxo com break em Cadastrar_contatos e remover_contatos)
