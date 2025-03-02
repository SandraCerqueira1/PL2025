# TPC4: Analisador Léxico
## 02/03/2025

## Autor

- A100681
- Sandra Fabiana Pires Cerqueira

## Resumo
Este projeto teve como objetivo a construção de um analisador léxico para uma linguagem de query com o qual se podem escrever frases do genero:
```
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000

```
## A Saber
Para desenvolver esta solução usei o ply.lex e obtive o seguinte output
```
COMMENT # DBPedia: obras de Chuck Berry
SELECT select
VAR ?nome
VAR ?desc
WHERE where
LCB {
VAR ?s
A a
URI dbo:MusicalArtist
DOT .
VAR ?s
URI foaf:name
STRING "Chuck Berry"
LANG @en
DOT .
VAR ?w
URI dbo:artist
VAR ?s
DOT .
VAR ?w
URI foaf:name
VAR ?nome
DOT .
VAR ?w
URI dbo:abstract
VAR ?desc
RCB }
LIMIT LIMIT
INT 1000
```


 




