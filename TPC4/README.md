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
## Funcionalidades

 
## Utilização



