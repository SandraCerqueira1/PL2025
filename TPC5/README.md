# TPC5: Vending Machine
## 09/03/2025

## Autor

- A100681
- Sandra Fabiana Pires Cerqueira

## Resumo
O TPC consiste na construção de uma máquina de venda automática em Python, onde o utilizador pode interagir através de uma série de comandos para efetuar a compra de produtos. Os comandos disponíveis são:

- **LISTAR:** Listar os produtos disponíveis na máquina.
- **MOEDA <moedas>:** Inserir moedas na máquina (exemplo: MOEDA 1e 50c).
- **SELECIONAR <ID>:** Selecionar um produto para comprar com base no seu ID.
- **SAIR:** Encerrar a compra e receber o troco.

## Funcionalidades Implementadas
- **Listagem de Produtos:** Ao digitar o comando "LISTAR", a máquina exibe a lista de produtos disponíveis com os seus IDs, nomes e preços.
- **Inserção de Moedas:** Ao usar o comando "MOEDA <moedas>", o utilizador pode inserir moedas na máquina para aumentar o saldo disponível.
- **Seleção de Produto:** O comando "SELECIONAR <ID>" permite ao utilizador escolher um produto para comprar, considerando o saldo disponível na máquina.
- **Encerramento da Compra:** O comando "SAIR" finaliza a interação, exibindo o troco de acordo com o saldo restante.

## Instruções de Utilização
1. Executar o comando `python3 script.py `
2. Utilizar os comandos descritos acima para interagir com a máquina.



