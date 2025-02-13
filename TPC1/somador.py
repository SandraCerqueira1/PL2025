def somador_on_off(arquivo):
    with open(arquivo, "r") as file:
        content = file.read().lower()  # Ler file e passar tudo para minusculas

    total = 0
    i = 0
    active = True  #meti a começar com a soma ativa
    number = ""

    while i < len(content):
        # Começar a juntar o numero
        if content[i].isdigit():
            number += content[i]
        else:
            if number:  # Se um número foi formado, somar ao total se estiver "on" true
                if active:
                    total += int(number)
                number = ""  # Limpa o número para o próximo valor

            # Verificar se encontramos as palavras "on" ou "off"
            if content[i:i+2] == "on":  
                active = True
                i += 1  
            elif content[i:i+3] == "off":  
                active = False
                i += 2  
            elif content[i] == "=":  # Quando encontrar "=", imprime o total até ali
                print(total)

        i += 1  

    # Se houver um número final e a soma estiver ligada, soma o último número
    if number and active:
        total += int(number)


somador_on_off("teste.txt")
