# TPC1: 
## 10/02/2025

## Autor

- A100681
- Sandra Fabiana Pires Cerqueira

## Resumo
### Objetivos 
**Somador on/off em Python**

O objetivo deste tpc foi criar um programa em Python que funcionasse como um somador on/off.
A ideia era somas todas as sequências de dígitos encontradas num texto, ligando ou desligando esse comportamento com as palavras "on" e "off", respetivamente, independentemente destas palavras estarem em maiúsculo ou minúsculo. Sempre que o caracter "=" for encontrado, o resultado da soma até ao momento é exibido no terminal.

### Resulato
O programa `somador.py` foi desenvolvido para atender aos requisitos do somador on/off.
O programa lê um file chamado `teste.txt` e processa seu conteúdo para identificar números e somá-los, controlando essa soma conforme as palavras "on" e "off" aparecem no texto. Sempre que o caractere "=" for encontrado, o total acumulado até a esse momento é impresso no ecrã.

Tendo o seguinte conteúdo no `teste.txt`:

```txt
45
2025-02-07=
oFf
789    43
on
5=
```
O output será:

```txt 
2079
2084
```

## Conclusão
O programa funciona corretamente, pois consegue identificar números e somá-los conforme a ativação/desativação do somador; ignorar letras e caracteres não numéricos; tratar palavras "on" e "off" de forma case-insensitive e dar print do total acumulado até ao momento em que encontra um "=".



