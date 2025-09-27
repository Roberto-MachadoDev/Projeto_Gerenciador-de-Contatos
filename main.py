# Programa de Gerenciamento de Contatos Comerciais

import json
import os
from datetime import datetime

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
    if not os.path.exists(ARQUIVO_JSON):
        return []

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Aviso: {ARQUIVO_JSON} inválido ({e}). Usando lista vazia.")
        return []

    if not isinstance(data, list):
        print("Formato inesperado no JSON (esperado lista). Ignorando conteúdo e iniciando vazio.")
        return []

    contatos = []
    for item in data:
        if not isinstance(item, dict):
            continue
        normalized = {k.strip().lower(): v for k,
                      v in item.items() if isinstance(k, str)}
        contatos.append({
            "id": str(normalized.get('id', '')),
            "nome": normalized.get('nome', ''),
            "sobrenome": normalized.get('sobrenome', ''),
            "telefone": normalized.get('telefone', ''),
            "email": normalized.get('email', ''),
            "atividade": normalized.get('atividade', '')
        })
    return contatos

# ---------- Gerenciamento de IDs ----------


def gerar_novo_id():
    global id_global
    novo = id_global
    id_global += 1
    return str(novo)


# Carrega contatos
listaContatos = carregar_contatos()

# Calcula id_global
existing_ids = [int(c['id'])
                for c in listaContatos if c.get('id') and c['id'].isdigit()]
id_global = max(existing_ids) + 1 if existing_ids else 5586954

# Atribui ids faltantes
changed = False
for c in listaContatos:
    if not c.get('id'):
        c['id'] = gerar_novo_id()
        changed = True
    else:
        c['id'] = str(c['id'])

if changed:
    salvar_contatos()

# ---------- Funções de exibição ----------


def exibir_contato(contato):
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
