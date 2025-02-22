import re

def markdown_to_html(markdown):
    # Cabeçalhos
    markdown = re.sub(r'^#\s+(.+?)\s*$', r'<h1>\1</h1>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^##\s+(.+?)\s*$', r'<h2>\1</h2>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^###\s+(.+?)\s*$', r'<h3>\1</h3>', markdown, flags=re.MULTILINE)

    # Negrito
    markdown = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown)

    # Itálico
    markdown = re.sub(r'\*(.*?)\*', r'<i>\1</i>', markdown)

    # Linha horizontal
    markdown = re.sub(r'---', r'<hr/>', markdown)

    # Bloco de código
    markdown = re.sub(r'`(.*?)`', r'<code>\1</code>', markdown)

    # Lista numerada
    markdown = re.sub(r'^\d+\.\s+(.+?)\s*$', r'<li>\1</li>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^(\d+\.\s+.+\n)+', r'<ol>\g<0></ol>', markdown, flags=re.MULTILINE)

    # Lista não numerada
    markdown = re.sub(r'^-\s+(.+?)\s*$', r'<li>\1</li>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^(-\s+.+\n)+', r'<ul>\g<0></ul>', markdown, flags=re.MULTILINE)

    # Imagem
    markdown = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', markdown)

    # Link
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown)

    return markdown

def main():
    try:
        with open('input.md', 'r', encoding='utf-8') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        print("O ficheiro 'input.md' não foi encontrado.")
        return

    html_text = markdown_to_html(markdown_text)

    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(html_text)

    print("A conversão foi concluída com sucesso e o resultado foi salvo em 'output.html'.")

if __name__ == '__main__':
    main()
