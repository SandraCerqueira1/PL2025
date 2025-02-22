# TPC2: Conversor de MD para HTML
## 22/02/2025

## Autor

- A100681
- Sandra Fabiana Pires Cerqueira

## Resumo
Este projeto é um conversor simples de MarkDown para HTML.
## Funcionalidades

- **Cabeçalhos:**
  - Transforma as linhas iniciadas por `#`, `##` e `###` em `<h1>`, `<h2>` e `<h3>`, respetivamente.

- **Negrito e Itálico:**
  - Converte pedaços de texto entre `**` em `<b>` e `</b>`.
  - Converte pedaços de texto entre `*` em `<i>` e `</i>`.

- **Linha Horizontal:**
  - Substitui sequências `---` por `<hr/>`.

- **Bloco de Código:**
  - Transforma  (``) em `<code>` e `</code>`.

- **Listas Numeradas e Não Numeradas:**
  - Converte listas numeradas iniciadas por `\d+\.` em `<ol>` e `<li>`.
  - Converte listas não numeradas iniciadas por `-` em `<ul>` e `<li>`.

- **Imagem:**
  - Substitui `![alt text](image path)` por `<img src="image path" alt="alt text"/>`.

- **Link:**
  - Transforma  `[link text](URL)` em `<a href="URL">link text</a>`.

## Utilização
Para correr o código utiliza-se o seguinte comando : python3 script.py


