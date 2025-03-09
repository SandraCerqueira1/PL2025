import re
import ply.lex as lex
import json
from tabulate import tabulate

tokens = ('LISTAR', 'MOEDA', 'SELECIONAR', 'SAIR')

def t_MOEDA(t):
    r'MOEDA\s+((\d+e|\d+c)(,\s*(\d+e|\d+c))*)'
    valores = re.findall(r'(\d+e|\d+c)', t.value)
    for valor in valores:
        if valor[-1] == 'e':
            t.lexer.saldo += int(valor[:-1]) * 100  # Converter euros para cêntimos
        else:
            t.lexer.saldo += int(valor[:-1])
    
    euros = t.lexer.saldo // 100
    centimos = t.lexer.saldo % 100
    print(f"Saldo = {euros}e{centimos}c")
    return t

def t_LISTAR(t):
    r'LISTAR'
    print("\nLista de produtos:")
    headers = ["COD", "NOME", "QUANTIDADE", "PREÇO"]
    table = [[p['cod'], p['nome'], p['quant'], f"{p['preco']}€"] for p in t.lexer.data]
    print(tabulate(table, headers, tablefmt="grid"))
    return t

def t_SELECIONAR(t):
    r'SELECIONAR\s+\w+'
    produto_cod = t.value.split()[1]
    produto = next((p for p in t.lexer.data if p['cod'] == produto_cod), None)

    if not produto:
        print(f"Produto inexistente com código: {produto_cod}")
        return t
    
    if produto['quant'] == 0:
        print(f"Produto {produto_cod} esgotado.")
        return t

    preco_em_centimos = int(produto['preco'] * 100)
    if t.lexer.saldo >= preco_em_centimos:
        t.lexer.saldo -= preco_em_centimos
        produto['quant'] -= 1
        print(f"Pode retirar o produto dispensado \"{produto['nome']}\"")
    else:
        saldo_euros = t.lexer.saldo // 100
        saldo_centimos = t.lexer.saldo % 100
        pedido_euros = preco_em_centimos // 100
        pedido_centimos = preco_em_centimos % 100
        print(f"Saldo insuficiente para satisfazer o seu pedido")
        print(f"Saldo = {saldo_euros}e{saldo_centimos}c; Pedido = {pedido_euros}e{pedido_centimos}c")

    # Atualizar stock no STOCK
    with open("stock.json", "w") as file:
        json.dump(t.lexer.data, file, indent=4)
    
    return t

def t_SAIR(t):
    r'SAIR'
    if t.lexer.saldo > 0:
        print(f"Pode retirar o troco: {calcular_troco(t.lexer.saldo)}.")
    print("Até à próxima!")
    t.lexer.flag = True
    return t

def calcular_troco(saldo):
    moedas = [200, 100, 50, 20, 10, 5, 2, 1]  # Valores das moedas em cêntimos
    troco = []
    for moeda in moedas:
        qtd, saldo = divmod(saldo, moeda)
        if qtd > 0:
            troco.append(f"{qtd}x {moeda}c" if moeda < 100 else f"{qtd}x {moeda // 100}e")
    return ", ".join(troco) if troco else "Sem troco"

def t_error(t):
    print("Comando inválido. Tente novamente.")
    t.lexer.skip(1)

t_ignore = ' \t\n'

def main():
    lexer = lex.lex()

    try:
        with open("stock.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Arquivo stock.json não encontrado")

    lexer.data = data
    lexer.flag = False
    lexer.saldo = 0

    print("\nBem-vindo à máquina de venda automática!")
    print("\nComandos disponíveis:")
    print("-> LISTAR")
    print("-> MOEDA <VALOR>")
    print("-> SELECIONAR <COD>")
    print("-> SAIR\n")

    while not lexer.flag:
        input_user = input("Operação: ").strip()
        lexer.input(input_user)
        token = lexer.token()
        if not token:
            print("Comando inválido.")

if __name__ == "__main__":
    main()
