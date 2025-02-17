import re

class AnalisadorCSV:
    def __init__(self, file_path: str):
        with open(file_path, encoding="utf-8") as f:
            linhas = f.readlines()

        self.dataset = self._reconstruct_records(linhas)
        self.header = self.dataset.pop(0)  # Remover cabeçalho

    def _split_csv_line(self, line):
        #dividir mas ignorar o ; de aspas.
        fields = re.split(r';(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
        return [field.strip().strip('"') for field in fields]

    def _reconstruct_records(self, linhas):
        records = []
        buffer = ""

        for line in linhas:
            buffer += " " + line.strip()
            if buffer.count(";") >= 6:  # Linha completa (7 campos = 6 separadores)
                records.append(self._split_csv_line(buffer.strip()))
                buffer = ""

        return records

    def listar_compositores(self):
        compositores = set()
        for linha in self.dataset:
            if len(linha) > 4:  # Garantir que tem pelo menos 5 colunas
                compositores.add(linha[4])  # Compositor
        return sorted(compositores)

    def distribuicao_obras_por_periodo(self):
        distribuicao = {}
        for linha in self.dataset:
            if len(linha) > 3:
                periodo = linha[3]
                distribuicao[periodo] = distribuicao.get(periodo, 0) + 1
        return distribuicao

    def obras_por_periodo(self):
        obras = {}
        for linha in self.dataset:
            if len(linha) > 3:
                titulo = linha[0]
                periodo = linha[3]
                if periodo not in obras:
                    obras[periodo] = []
                obras[periodo].append(titulo)
        for periodo in obras:
            obras[periodo].sort()
        return obras


analise = AnalisadorCSV('obras.csv')


while True:
    print("\nEscolhe uma opção:")
    print("1 - Lista ordenada alfabeticamente de compositores musicais")
    print("2 - Distribuição das obras por período")
    print("3 - Dicionário de obras por período")
    print("4 - Sair")

    opcao = input("Digita o número da opção desejada: ")

    match opcao:
        case "1":
            print("\nLista ordenada alfabeticamente de compositores musicais:")
            print(analise.listar_compositores())

        case "2":
            print("\nDistribuição das obras por período:")
            print(analise.distribuicao_obras_por_periodo())

        case "3":
            print("\nDicionário de obras por período:")
            print(analise.obras_por_periodo())

        case "4":
            print("Sair...")
            break

        case _:
            print("Opção inválida. Tenta novamente.")
