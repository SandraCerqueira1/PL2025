
<h1 align="center">Construção de um Compilador para Pascal Standard</h1>


<p align="center">
  <img src='https://upload.wikimedia.org/wikipedia/commons/9/93/EEUMLOGO.png' width="30%" />
</p>

<h3 align="center">Licenciatura em Engenharia Informática <br> Processamento de Linguagens <br> 2024/2025 </h3>
<h3 align="center">Grupo 17 </h3>

<h3 align="center"> Autores 🤝 </h3>

<div align="center">

| Nome                           |  Número | Username GitHub |
|--------------------------------|---------|-----------------|
| Diogo Gabriel Lopes Miranda    | A100839 | DMirandex       |
| João Ricardo Ribeiro Rodrigues | A100598 | Mad-Karma       |
| Sandra Fabiana Pires Cerqueira | A100681 | SandraCerqueira1 |

</div>

## 1 Introdução
Este relatório documenta as várias etapas envolvidas no desenvolvimento de um compilador para a linguagem Pascal standard, no âmbito da unidade curricular de Processamento de Linguagens.

O objetivo principal do trabalho foi criar, com o suporte da linguagem de programação Python e do módulo ply, um programa capaz de realizar a análise léxica e sintática da linguagem Pascal, convertendo o código fonte para a máquina virtual fornecida pela equipa docente.

A análise sintática interpreta o código de entrada, identificando-o como uma sequência de tokens gerados pela análise léxica. Esses tokens correspondem aos elementos básicos da linguagem, como palavras-chave, identificadores e símbolos especiais.

A análise sintática processa o código de entrada, identificando-o como uma sequência de tokens gerados pela análise léxica. Esses tokens representam os elementos fundamentais da linguagem, como palavras-chave, identificadores e símbolos especiais.

### 1.1 Apresentação do Problema
O projeto consistiu no desenvolvimento de um compilador para a linguagem Pascal que abrangesse o padrão desta linguagem, com o propósito de gerar código compatível com a máquina virtual fornecida. Entre os requisitos mínimos para a implementação do compilador destacam-se a declaração de variáveis, expressões aritméticas e comandos de controlo de fluxo *(if, while, for)*.

### 1.2 Objetivo
Este projeto visa proporcionar experiência prática na construção de compiladores, com foco na aplicação de gramáticas tradutoras e no uso da tradução dirigida pela sintaxe, criando um compilador que irá ser capaz de gerar código para uma máquina virtual. Para isso, recorre-se ao módulo *PLY* em *Python*, que permite gerar analisadores léxicos, usando o *Lex*, e sintáticos, usando o *Yacc*, a partir de definições gramaticais, promovendo a compreensão dos mecanismos fundamentais do processamento de linguagens.

#
## Análise e Especialização
### 2.1 Descrição informal do problema
O problema abordado neste trabalho consiste na criação de um compilador para a linguagem de programação *Pascal*. A linguagem de programação *Pascal* é uma linguagem com sintaxe clara e rigorosa, que promove o uso de técnicas estruturadas. *Pascal* suporta a definição de tipos de dados, estruturas de controle como *if*, *while* e *for*, e permite a criação de subprogramas através de *procedures* e *functions*. O compilador ser capaz de interpretar código em *Pascal* e gerar código máquina para a máquina virtual a ser usada.
O maior desafio deste problema é a sintaxe rica e fortemente tipada da linguagem *Pascal*, assim como o tratamento de estruturas complexas, como arrays com intervalos personalizados.

### 2.2 Especificação dos requisitos
Com base na descrição informal do problema, os requisitos para o compilador da linguagem de progrmação *Pascal* são:
  
  - Análise léxica e sintática para reconhecer os tokens e estruturas da linguagem *Pascal*
  - Suportar declarações de variáveis, incluíndo arrays
  - Suportar expressões aritméticas
  - Suportar comandos de controlo condicionais (*if*, *then* e *else*)
  - Suportar comandos de controlo iterativos (*for* e *while*)
  - Gerar código máquina compatíevel com a máquina virtual usada

## Desenho da solução
Face ao problema em questão, a nossa solução pode ser dividida em quatro partes:
  
  - Analisador léxico
  - Analisador sintático
  - Árvore AST
  - Gerador de código para a máquina virutal

### 3.1 Analisador léxico
O analisador léxico é responsável por identificar e recolher os simbolos terminais (*tokens*) da linguagem em questão, *Pascal*, fazendo uso de expressões regulares para esse fim. Para a implementação do analisador léxico utilizámos o módulo lex do PLY em Python.
Os tokens definidos têm como objetivo capturar diferentes tipos de elementos da linguagem, como palavras especificas, identificadores, literais, operadores e símbolos de pontuação.

Os *tokens* e as expressões regulares de cada são os seguintes:

*Tokens*:
- **PROGRAM** : `r'(?i)program'`
- **VAR** : `r'(?i)var'`
- **BEGIN** : `r'(?i)begin'`
- **END** : `r'(?i)end'`
- **IF** : `r'(?i)if'`
- **THEN** : `r'(?i)then'`
- **ELSE** : `r'(?i)else'`
- **WHILE** : `r'(?i)while'`
- **DO** : `r'(?i)do'`
- **FOR** : `r'(?i)for'`
- **TO** : `r'(?i)to'`
- **DOWNTO** : `r'(?i)downto'`
- **READLN** : `r'(?i)readln'`
- **WRITE** : `r'(?i)write'`
- **WRITELN** : `r'(?i)writeln'`
- **INTEGER** : `r'(?i)integer'`
- **REAL** : `r'(?i)real'`
- **BOOLEAN** : `r'(?i)boolean'`
- **CHAR** : `r'(?i)char'`
- **STRING** : `r'(?i)string'`
- **AND** : `r'(?i)and'`
- **OR** : `r'(?i)or'`
- **NOT** : `r'(?i)not'`
- **ID** : `r'[a-zA-Z_][a-zA-Z0-9_]*'`
- **NUMBER** : `r'\d+'`
- **REAL_LITERAL** : `r'\d+\.\d+'`
- **STRING_LITERAL** : `r'\".*?\"'`
- **PLUS** : `r'\+'`
- **MINUS** : `r'-'`
- **TIMES** : `r'\*'`
- **DIVIDE** : `r'/'`
- **MODULO** : `r'%'`
- **ASSIGN** : `r':='`
- **SEMI** : `r';'`
- **COMMA** : `r','`
- **COLON** : `r':'`
- **DOT** : `r'\.'`
- **DOTDOT** : `r'\.\.'`
- **LPAREN** : `r'\('`
- **RPAREN** : `r'\)'`
- **LBRACKET** : `r'\['`
- **RBRACKET** : `r'\]'`
- **EQUAL** : `r'='`
- **NEQUAL** : `r'<>'`
- **LT** : `r'<'`
- **LE** : `r'<='`
- **GT** : `r'>'`
- **GE** : `r'>='`
- 
A seguir apresenta-se uma explicação detalhada sobre a função de cada grupo de *tokens*, a sua organização e a lógica utilizada na sua definição.

###   Métodos de Reconhecimento dos tokens

Como se pode ver no nosso `pascal_lex.py` a  definição de tokens foi feita de duas formas:

- **1 - Atribuições simples (`t_TOKEN = r'...'`)**
* Esta forma foi usada para tokens que correspondem diretamente a símbolos fixos e não precisam de processamento adicional, como operadores (`+`, `*`, `:=`) e separadores (`;`, `,`, `.`). É uma forma mais direta e eficiente para o lexer reconhecer rapidamente esses elementos.

```python
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_EQUAL = r'='
t_NEQUAL = r'<>'
t_LESSTHEN = r'<'
t_LESSEQUALS = r'<='
t_GREATTHAN = r'>'
t_GREATEQUALS = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_VIRG = r','
t_DOT = r'\.'
t_DOISPONTOS = r':'
t_LSQBRACKET = r'\['   
t_RSQBRACKET = r'\]'    
t_ignore = ' \t'
```

- **2 - Funções (`def t_TOKEN(t): ...`)**
  - Para tokens que requerem um processamento extra, como conversão de valores numéricos para tipos nativos (`int` e `float`), strings literais, ou para garantir que palavras reservadas não sejam confundidas com identificadores, foi usada a definição através de funções.
  Esta abordagem também permite o uso do modificador `(?i)` para fazer o reconhecimento case-insensitive (ignorar maiúsculas/minúsculas), essencial para palavras-especifcas de Pascal, uma vez que esta linguagem é case-insensitive.
  ```python
  def t_PROGRAM(t):
    r'(?i)program'
    return t
  def t_VAR(t):
      r'(?i)var'
      return t

  def t_INTEGER_TYPE(t):
      r'(?i)integer'
      return t
  
  def t_BOOLEAN_TYPE(t):
      r'(?i)boolean'
      return t
  
  def t_STRING_TYPE(t):
      r'(?i)string'
      return t
  
  def t_REAL_TYPE(t):
      r'(?i)real'
      return t
  
  def t_CHAR_TYPE(t):
      r'(?i)char'
      return t

  def t_BEGIN(t):
      r'(?i)begin'
      return t
  
  def t_END(t):
      r'(?i)end'
      return t
  
  def t_IF(t):
      r'(?i)if'
      return t
  
  def t_THEN(t):
      r'(?i)then'
      return t
  
  def t_ELSE(t):
      r'(?i)else'
      return t
  
  def t_WHILE(t):
      r'(?i)while'
      return t
  
  
  def t_FOR(t):
      r'(?i)for'
      return t

  def t_DOWNTO(t):
      r'(?i)downto'
      return t
  
  def t_DO(t):
      r'(?i)do'
      return t
  
  def t_TO(t):
      r'(?i)to'
      return t
  
  
  def t_WRITELN(t):
      r'(?i)writeln'
      return t
  
  def t_WRITE(t):
      r'(?i)write'
      return t

  def t_READLN(t):
      r'(?i)readln'
      return t
  
  def t_LENGTH(t):
      r'(?i)length'
      return t
  
  def t_MODULO(t):
      r'(?i)mod'
      return t
  
  def t_DIV_INT(t):
      r'(?i)div'
      return t
  
  def t_TRUE(t):
      r'(?i)true'
      return t

  def t_FALSE(t):
      r'(?i)false'
      return t
  
  def t_AND(t):
      r'(?i)and'
      return t
  
  def t_OR(t):
      r'(?i)or'
      return t
  
  def t_NOT(t):
      r'(?i)not'
      return t
  
  def t_ARRAY(t):
      r'(?i)array'
      return t
  
  def t_OF(t):
      r'(?i)of'
      return t

  def t_ID(t):
      r'[a-zA-Z_][a-zA-Z_0-9]*'
      return t

  def t_RANGE(t):
      r'\.\.'
      return t

  def t_REAL_LITERAL(t):
      r'(\-)?\d+\.\d+'
      t.value = float(t.value)
      return t
 
  def t_NUMBER(t):
      r'(\-)?\d+'
      t.value = int(t.value)
      return t
  
  def t_STRING_LITERAL(t):
      r'\'[^\']*\''
      t.value = t.value[1:-1]  # Remove as aspas
      return t

  def t_COMMENT(t):
      r'(?s)\(\*.*?\*\)|\{.*?\}'
      t.lexer.lineno += t.value.count("\n")
      pass  

  def t_newline(t):
      r'\n+'
      t.lexer.lineno += len(t.value)
  

  def t_error(t):
      print(f"Caractere inválido: {t.value[0]}")
      t.lexer.skip(1)
  ```

#### Palavras especificas vs Identificadores (`ID`)
- As palavras especificas como *PROGRAM*, *VAR*, *BEGIN*, *END* até ao token *NOT*, são elementos fundamentais da linguagem Pascal e portanto foram definidos como tokens próprios. 
A definição das funções destes tokens surge primeiro que a do *ID* para evitar ambiguidades, assegurando que palavras especificas não sejam incorretamente tratadas como identificadores definidos pelo utilizador.

- **Identificadores (`ID`)**:
    O token *ID* reconhece identificadores válidos em Pascal *(variáveis, nomes de funções, etc.)*, que devem começar por uma letra ou underscore, podendo conter letras, dígitos ou underscores.

#### Reconhecimento de Números , Literais e Strings literais

- **Números inteiros (`NUMBER`) e reais (`REAL_LITERAL`)**:  
  São definidos por **funções** para permitir a conversão do valor capturado em `int` ou `float`.  

  A ordem de definição das funções é importante e o token `REAL_LITERAL` foi definido **antes** de `NUMBER`, para garantir que números com parte decimal (ex. `3.14`, `2.0`) sejam corretamente reconhecidos como valores reais, e **não** como inteiros.  
  Se `NUMBER` fosse definido antes, um número como `3.14` poderia ser lido parcialmente como `3` (`NUMBER`) e o restante `.14` causaria erro ou seria interpretado incorretamente.
  
- **Cadeia de caracteres (STRING_LITERAL)**:
Este token reconhece sequências de caracteres entre aspas duplas ("), como por exemplo `"texto"`.
É definido por uma função, permitindo a remoção das aspas e o retorno apenas do conteúdo textual da string.
O padrão utilizado é não guloso, o que significa que captura apenas até à próxima aspa de fecho. Esta estratégia evita que múltiplas strings sejam incorretamente agregadas como uma só, garantindo um reconhecimento correto e isolado de cada literal de string.
#### Comentários e Erros Léxicos

##### **Comentários**
Em Pascal, os comentários são delimitados por `{...}` ou `(*...*)` e devem ser ignorados pelo analisador léxico, e para esse efeito definimos a função `t_comment`
##### **Erros léxicos**
A função `t_error` trata erros léxicos ao identificar caracteres inesperados. Ela mostra uma mensagem de erro clara mas permite a continuidade da análise ao avançar um caractere no texto de entrada.

### Exemplo de Entrada e Output do Analisador Léxico
Para o seguinte programa:
```pascall
program Fatorial;
var
n, i, fat: integer;
begin
writeln('Introduza um número inteiro positivo:');
readln(n);
fat := 1;
for i := 1 to n do
fat := fat * i;
writeln('Fatorial de ', n, ': ', fat);
end.

```
O resultado do nosso lexer foi o seguinte:
```python
LexToken(PROGRAM,'program',2,1)
LexToken(ID,'Fatorial',2,9)
LexToken(SEMI,';',2,17)
LexToken(VAR,'var',3,19)
LexToken(ID,'n',4,23)
LexToken(VIRG,',',4,24)
LexToken(ID,'i',4,26)
LexToken(VIRG,',',4,27)
LexToken(ID,'fat',4,29)
LexToken(DOISPONTOS,':',4,32)
LexToken(INTEGER_TYPE,'integer',4,34)
LexToken(SEMI,';',4,41)
LexToken(BEGIN,'begin',5,43)
LexToken(WRITELN,'writeln',6,49)
LexToken(LPAREN,'(',6,56)
LexToken(STRING_LITERAL,'Introduza um número inteiro positivo:',6,57)
LexToken(RPAREN,')',6,96)
LexToken(SEMI,';',6,97)
LexToken(READLN,'readln',7,99)
LexToken(LPAREN,'(',7,105)
LexToken(ID,'n',7,106)
LexToken(RPAREN,')',7,107)
LexToken(SEMI,';',7,108)
LexToken(ID,'fat',8,110)
LexToken(ASSIGN,':=',8,114)
LexToken(NUMBER,1,8,117)
LexToken(SEMI,';',8,118)
LexToken(FOR,'for',9,120)
LexToken(ID,'i',9,124)
LexToken(ASSIGN,':=',9,126)
LexToken(NUMBER,1,9,129)
LexToken(TO,'to',9,131)
LexToken(ID,'n',9,134)
LexToken(DO,'do',9,136)
LexToken(ID,'fat',10,139)
LexToken(ASSIGN,':=',10,143)
LexToken(ID,'fat',10,146)
LexToken(MULT,'*',10,150)
LexToken(ID,'i',10,152)
LexToken(SEMI,';',10,153)
LexToken(WRITELN,'writeln',11,155)
LexToken(LPAREN,'(',11,162)
LexToken(STRING_LITERAL,'Fatorial de ',11,163)
LexToken(VIRG,',',11,177)
LexToken(ID,'n',11,179)
LexToken(VIRG,',',11,180)
LexToken(STRING_LITERAL,': ',11,182)
LexToken(VIRG,',',11,186)
LexToken(ID,'fat',11,188)
LexToken(RPAREN,')',11,191)
LexToken(SEMI,';',11,192)
LexToken(END,'end',12,194)
LexToken(DOT,'.',12,197)
```
Como podemos ver o lexer identificou corretamente todos os tokens do programa de exemplo, incluindo palavras especificas, identificadores, operadores, literais etc.  
O resultado demonstra que o lexer está a funcionar como esperado, reconhecendo os elementos da linguagem de forma precisa e eficiente.
#

### 3.2 Gramática e Geração de código VM

O analisador sintático, foi construído com o auxilio do módulo `ply.yacc` e é responsável por validar a estrutura sintática dos programas escritos em *Pascal*. A gramática implementada cobre um subconjunto representativo da linguagem, nomeadamente:
- declaração de variáveis
- expressões aritméticas
- estruturas de controlo de fluxo *(if, while e for)*
- chamadas de leitura/escrita (readln,writeln)
- tipos de dados estruturados como arrays

#### Especificação formal da gramática
Abaixo, apresentamos a especificação formal da nossa gramática que segue uma abordagem **bottom-up**. Posteriormente, neste documento iremos explorar a mesma em mais detalhe.
```bash
Programa           -> PROGRAM ID SEMI opt_variable block DOT

opt_variable       -> variables
                   | empty

variables          -> VAR vars

vars               -> listVar DOISPONTOS datatype SEMI
                   | listVar DOISPONTOS datatype SEMI vars

listVar            -> ID
                   | ID VIRG listVar

datatype           -> simpleType
                   | structuredType

simpleType         -> INTEGER_TYPE
                   | BOOLEAN_TYPE
                   | STRING_TYPE
                   | REAL_TYPE
                   | CHAR_TYPE

structuredType     -> arrayType

arrayType          -> ARRAY LSQBRACKET NUM RANGE NUM RSQBRACKET OF simpleType

block              -> BEGIN stmt_list opt_semi END

opt_semi          -> SEMI
                   | empty

stmt_list          -> stmt
                   | stmt_list SEMI stmt

stmt               -> assign_stmt
                   | conditional_stmt
                   | cicle_stmt
                   | read_stmt
                   | write_stmt
                   | writeLn_stmt

read_stmt         -> READLN LPAREN variable RPAREN

write_stmt        -> WRITE LPAREN output_args RPAREN

writeLn_stmt      -> WRITELN LPAREN output_args RPAREN
                   | WRITELN LPAREN RPAREN

output_args       -> output_item
                   | output_item VIRG output_args

output_item       -> STRING_LITERAL
                   | variable

variable          -> ID
                   | ID LSQBRACKET expression RSQBRACKET

assign_stmt       -> variable ASSIGN expression

expression        -> logical_or_expr

logical_or_expr   -> logical_or_expr OR logical_and_expr
                   | logical_and_expr

logical_and_expr  -> logical_and_expr AND logical_not_expr
                   | logical_not_expr

logical_not_expr  -> NOT logical_not_expr
                   | relational_expr

relational_expr   -> simple_exp
                   | simple_exp relational_op simple_exp

relational_operator -> EQUAL
                     | NEQUAL
                     | LESSTHEN
                     | LESSEQUALS
                     | GREATTHAN
                     | GREATEQUALS

simple_exp        -> simple_exp add_op termo
                   | termo

add_op            -> PLUS
                   | MINUS

termo             -> termo mul_op factor
                   | factor

mul_op            -> MULT
                   | DIVIDE
                   | MODULO
                   | DIV_INT

factor            -> LENGTH LPAREN expression RPAREN
                   | LPAREN expression RPAREN
                   | variable
                   | NUMBER
                   | REAL_LITERAL
                   | STRING_LITERAL
                   | TRUE
                   | FALSE

conditional_stmt  -> if_stmt

if_stmt           -> IF expression THEN stmt
                   | IF expression THEN stmt ELSE stmt

cicle_stmt        -> while_stmt
                   | for_stmt

while_stmt        -> WHILE expression DO cicle_body

cicle_body        -> block
                   | stmt

for_stmt          -> FOR assign_stmt TO simple_exp DO cicle_block
                   | FOR assign_stmt DOWNTO simple_exp DO cicle_block

empty             -> ε

```

#### Descrição geral do processo de implementação
Todo o processo de construção gramatical foi incremental,começámos pelas declarações de variáveis,  e a partir daí fomos alargando o suporte ao resto. A prioridade foi garantir que cada parte estivesse funcional antes de avançar para a seguinte, permitindo testes frequentes e localizados.

##### Representação intermédia do programa 

Para responder à necessidade de ter uma representação intermédia do programa, para ser utilizada na geração do código máquina a utilizar na *VM*, optámos por definir uma árvore de sintaxe abstrata, seguindo os exemplos presentes na documentação oficial do *ply*, secção *6.10*.
Dentro das diferentes opções fornecidas pela documentação, como se pode ver no `ast_nodes.py`, optámos por definir uma classe para cada nó da nossa árvore porque, apesar de ser mais complexo de implementar, simplificou o processo de geração de código, uma vez que, para cada classe temos um tratamento especifico para a mesma dependendo do que é pretendido.

#### Geração de código

O nosso `codegen.py` é responsável por percorrer a árvore e, consoante a classe do nó em que se encontra, gerar o respetivo código máquina para essa instrução. Cada instrução gerada é então adicionada à lista que vai acumulando todo o código do programa, que será posteriormente interpretado pela máquina virtual.

##### Tabela de simbolos

Durante a geração de código, percebemos que era necessário manter um registo das variáveis declaradas no programa, para garantir que cada acesso ou operação sobre elas fosse corretamente traduzido para instruções da VM. Para isso, criámos então um dicionário onde guardamos as variáveis do programa, com toda a informação relevante associada a cada uma.

A função `build_symbol_table` percorre a **árvore** e constrói essa tabela, registando atributos fundamentais de cada variável, tais como:
- **`offset`**: posição da variável na stack global.
- **`type`**: tipo da variável (*integer, real, string, boolean* ou *structured* para arrays).
- **`elem_type`**: no caso de arrays, indica o tipo dos elementos que o compõem.
- **`size`**: se for um array, calcula o número de elementos.
- **`low_bound`**: limite inferior dos índices do array.

O código distingue entre **variáveis simples e arrays**, garantindo que os arrays recebem atributos adicionais, como limites e tamanho. Cada variável declarada é inserida no dicionário com os seus atributos, e o *offset* é incrementado a cada inserção, garantindo uma correta disposição na memória.

A tabela de símbolos é essencial para o funcionamento do `codegen.py`, pois permite que ele aceda às variáveis corretamente e traduza operações e acessos de forma precisa para a máquina virtual. Só desta forma conseguimos ter controlo sobre essas variáveis e gerar instruções como PUSHG, STOREG, ETC, e ainda gerar as diferentes intruções para a VM para os diferentes tipos de dados.

Segue-se a nossa função `build_symbol_table`

```python
def build_symbol_table(ast):
    """
    Constrói a tabela de símbolos a partir de ast.opt_variable,
    mapeando cada variável global a:
      - offset: posição no stack global
      - type: “integer”, “real”, “string”, “boolean” ou “structured”
      - elem_type: se for structured (array), tipo dos elementos
      - size: se for array, número de elementos
    """
    table = {}
    offset = 0

    def process_vars(node):
        nonlocal offset
        if isinstance(node, Opt_variableNode):
            process_vars(node.child)
        elif isinstance(node, VariablesNode):
            for decl in node.vars_node:
                # detecta se é tipo simples ou array
                if isinstance(decl.datatype.type_node, SimpleTypeNode):
                    base_type = decl.datatype.type_node.type_name.lower()
                    elem_type = None
                    size = None
                    low = None  
                    vtype = base_type
                else:
                    # array
                    vtype = "structured"
                    array = decl.datatype.type_node.array_type
                    elem_type = array.simple_type.type_name.lower()
                    # calcula tamanho
                    size = int(array.high_bound) - int(array.low_bound) + 1
                    low = int(array.low_bound)

                for var in decl.list_var_ids:
                    table[var] = {
                        "offset": offset,
                        "type": vtype,
                        "elem_type": elem_type,
                        "size": size,
                        "low_bound": low
                    }
                    offset += 1

    process_vars(ast.opt_variable)
    return table
```
#
### Explicação detalhada de cada componente
Na secção anterior, apresentámos uma visão geral do nosso projeto e da sua estrutura. Agora, iremos aprofundar cada um dos seus componentes, explorando em detalhe a sua implementação, desafios enfrentados e decisões tomadas ao longo do desenvolvimento.
#
### Declaração de Variáveis
Para garantir que o nosso compilador suportasse corretamente a declaração de variáveis, começámos por analisar a sintaxe do Pascal. Identificámos que a estrutura típica para a declaração de variáveis segue o seguinte padrão:

```bash
var
n, i, fat: integer;
```
Ou seja: o bloco de declaração das variáveis é  sempre iniciado pela palavra  VAR, seguida da lista das variáveis e do respetivo tipo de dados. O tipo pode ser simples  ou estruturado. Além disso, a declaração de variáveis é opcional, o que significa que um programa pode ou não conter este bloco.

Para garantir que o nosso analisador sintático reconhece corretamente esta estrutura, tal como visto anteriormente, definimos as seguintes produções gramaticais:
```bash
Programa           -> PROGRAM ID SEMI opt_variable block DOT

opt_variable       -> variables
                   | empty

variables          -> VAR vars

vars               -> listVar DOISPONTOS datatype SEMI
                   | listVar DOISPONTOS datatype SEMI vars

listVar            -> ID
                   | ID VIRG listVar

datatype           -> simpleType
                   | structuredType

simpleType         -> INTEGER_TYPE
                   | BOOLEAN_TYPE
                   | STRING_TYPE
                   | REAL_TYPE
                   | CHAR_TYPE

structuredType     -> arrayType

arrayType          -> ARRAY LSQBRACKET NUM RANGE NUM RSQBRACKET OF simpleType
```
Tendo por base a gramática criada, identificamos o que seria necessário guardar na nossa AST e concluímos que uma das informações fundamentais a preservar é a lista de identificadores, pois permite que cada variável declarada seja posteriormente utilizada na geração de código.
Para representar essa lista na AST, definimos o nó ListVarNode, que armazena todos os identificadores declarados no programa. 
A implementação deste nó é apresentada abaixo:
```python
# Nó para a produção listVar (lista de identificadores)
class ListVarNode(ASTNode):
    def __init__(self, ids):
        self.ids = ids  # Lista de strings

    def __str__(self):
        return f"ListVar({self.ids})"

```
De modo a associar essas variáveis a um tipo de dados foi criado o nodo *DatatypeNode*:
```python
class DatatypeNode(ASTNode):
    def __init__(self, type_node):
        self.type_node = type_node  # Instância de SimpleTypeNode ou StructuredTypeNode

    def __str__(self):
        return f"Datatype({self.type_node})"
```
Com type_node podendo ser do tipo simples *(inteiros, strings)* ou do tipo estruturado *(arrays)*, para representar estas hipoteses foram criados os nodos:

```bash
class SimpleTypeNode(ASTNode):
    def __init__(self, type_name):
        self.type_name = type_name  # String, por exemplo "INTEGER_TYPE"
    
    def __str__(self):
        return f"SimpleType({self.type_name})"

# Nó para o não-terminal structuredType (neste caso, arrayType)
class StructuredTypeNode(ASTNode):
    def __init__(self, array_type):
        self.array_type = array_type  # Instância de ArrayTypeNode

    def __str__(self):
        return f"StructuredType({self.array_type})"

# Nó para o não-terminal arrayType
class ArrayTypeNode(ASTNode):
    def __init__(self, low_bound, high_bound, simple_type):
        self.low_bound = low_bound    # Valor inferior (NUM)
        self.high_bound = high_bound  # Valor superior (NUM)
        self.simple_type = simple_type  # Nó SimpleTypeNode
    def __str__(self):
        return f"ArrayType({self.low_bound}, {self.high_bound}, {self.simple_type})"

```

Por fim, tendo o **YACC** e a **AST**, passamos então para o `codegen.py`, que ficou da seguinte maneira:
```python
elif isinstance(node, VarDeclNode):
        if isinstance(node.datatype.type_node, SimpleTypeNode):
            t = node.datatype.type_node.type_name.lower()
            if t == "integer":
                for _ in node.list_var_ids:
                    code.append("PUSHI 0")
            elif t == "boolean":
                for _ in node.list_var_ids:
                    code.append("PUSHI 0")
            elif t == "string":
                for _ in node.list_var_ids:
                    code.append('PUSHS ""')
            elif t == "real":
                for _ in node.list_var_ids:
                    code.append("PUSHF 0.0")
            elif t == "char":
                for _ in node.list_var_ids:
                    code.append('PUSHS ""')

        elif isinstance(node.datatype.type_node, StructuredTypeNode):
            array_node = node.datatype.type_node.array_type
            low = int(array_node.low_bound)
            high = int(array_node.high_bound)
            size = high - low + 1
            for _ in node.list_var_ids:
                code.append(f"ALLOC {size}")
```
Como podemos verificar acima, o nosso programa lê da **AST** o tipo de dados da variável a declarar e gera a instrução correta baseada nesse tipo. Caso seja um inteiro ou um *booblean*, a instrução gerada vai ser um **pushi 0**, por outro lado caso seja uma *string* ou um *char*, a intrução gerada sera um **pushs ""**, por último caso seja do tipo real a instrução gerada será **pushf 0.0**. No caso dos *arrays*, a instrução gerada será **alloc n**, com n correspondendo ao tamanho do array.

Desta forma conseguimos alocar espaço na stack (armazenando um 0 para os inteiros, uma *string* vazia para as *strings*, etc), para todas as variáveis declaradas pelo nosso programa.
#

### Operações de escrita e leitura
Em Pascal, as operações de escrita são realizadas com as instruções **Write** e **Writeln**, que permitem imprimir mensagens, valores de variáveis ou uma combinação de ambos. Por outro lado, a leitura de dados é feita através da instrução **Readln**, que capta um valor introduzido pelo utilizador e armazena-o variável.

Para suportar estas funcionalidades, expandimos a nossa gramática com as seguintes produções:
 ```bash
read_stmt ->READLN LPAREN variable RPAREN
write_stmt-> WRITE LPAREN  output_args   RPAREN
writeLn-stmt-> WRITELN LPAREN    output_args   RPAREN
	    |  WRITELN LPAREN RPAREN
output_args   -> output_item
            | output_item VIRG output_args
output_item  -> STRING_LITERAL
            | variable
```
A partir disto, adaptámos o analisador léxico e sintático, garantindo que estas instruções fossem corretamente reconhecidas e processadas. Além disso, também expandimos a AST, criando novos nós que representam estas operações, nomeadamente: 

-  O `ReadLnStmtNode` que representa uma instrução de leitura, contendo um nó da variável.
- O `WriteStmtNode` e o `WriteLnStmtNode` que representam instruções de escrita, armazenando os argumentos a serem impressos.
- O `OutputArgsNode` que gerencia uma lista de itens de saída, e o `OutputItemNode` que encapsula um único elemento, que pode ser um literal de string ou uma variável.

Após isto, foi necessário atualizar também o `codegen.py`, garantindo que para o *readln*, o código gerado começa sempre com READ, seguido de uma conversão (ATOI ou ATOF) conforme o tipo da variável. Se for um array, calcula-se o índice (corrigido pelo limite inferior) antes de armazenar o valor com STOREN; caso contrário, usa-se STOREG.

As instruções *write* e *writeln* percorrem a lista de argumentos e, dependendo do tipo, empilham o valor correspondente. Se for variável, verifica-se se é simples ou array para usar PUSHG ou LOADN, e escolhe-se a instrução de escrita adequada: WRITEI, WRITEF ou WRITES. O *writeln*, além disso, termina sempre com um WRITELN, mesmo quando não há argumentos.
De seguida encontra-se então o código desa parte do codegen:
```python
elif isinstance(node, ReadLnStmtNode):
        var = node.var_node
        info = symbol_table[var.id]
        if var.index is None:
            code.append("READ")
            if info["type"] == "integer":
                code.append("ATOI")
            elif info["type"] == "real":
                code.append("ATOF")
            code.append(f"STOREG {info['offset']}")
        else:
            code.append(f"PUSHG {info['offset']}")
            code.extend(generate_code(var.index, symbol_table))
            code.append(f"PUSHI {info['low_bound']}")
            code.append("SUB")
            code.append("READ")
            if info["elem_type"] == "integer":
                code.append("ATOI")
            elif info["elem_type"] == "real":
                code.append("ATOF")
            code.append("STOREN")
    
    elif isinstance(node, WriteStmtNode):
        for item in node.output_args.items:
            val = item.value
            if isinstance(val, VariableNode):
                info = symbol_table[val.id]
                if val.index is None:
                    code.append(f"PUSHG {info['offset']}")
                else:
                    code.append(f"PUSHG {info['offset']}")           
                    code.extend(generate_code(val.index, symbol_table))  
                    code.append("LOADN")                  
                # escolhe WRITEI/WRITEF/WRITES
                t = info["elem_type"] if val.index is not None else info["type"]
                if t in ("integer", "boolean"):
                    code.append("WRITEI")
                elif t == "real":
                    code.append("WRITEF")
                else:
                    code.append("WRITES")
            else:
                code.append(f'PUSHS "{val}"')
                code.append("WRITES")

    elif isinstance(node, WriteLnStmtNode):
        if node.output_args is not None:
            for item in node.output_args.items:
                val = item.value
                if isinstance(val, VariableNode):
                    info = symbol_table[val.id]
                    if val.index is None:
                        code.append(f"PUSHG {info['offset']}")
                    else:
                        code.append(f"PUSHG {info['offset']}")           
                        code.extend(generate_code(val.index, symbol_table))  
                        code.append("LOADN")                  
                    t = info["elem_type"] if val.index is not None else info["type"]
                    if t in ("integer", "boolean"):
                        code.append("WRITEI")
                    elif t == "real":
                        code.append("WRITEF")
                    else:
                        code.append("WRITES")
                else:
                    code.append(f'PUSHS "{val}"')
                    code.append("WRITES")
        # em todos os casos, termina com WRITELN
        code.append("WRITELN")

```
#
### Expressões aritméticas
Para lidar corretamente com as expressões aritméticas, bem como operações lógicas e relacionais, foi essencial definir e respeitar a precedência entre os operadores. Ou seja, tivemos de garantir que a ordem de avaliação das expressões seguisse as regras da linguagem, garantindo que:

Operadores relacionais *(>, <, >=, <=, ==)* fossem avaliados antes dos operadores lógicos (AND, OR, NOT).

Operações matemáticas fossem processadas corretamente dentro da hierarquia de prioridade.

Funções predefinidas, como LENGTH, DIV *(divisão inteira)* e MOD, fossem tratadas como expressões aritméticas.

Para organizar esta estrutura, desenvolvemos a seguinte gramática:
```bash
variable → ID
    | ID LSQBRACKET expression RSQBRACKET

assign_stmt → variable ASSIGN expression

expression       → logical_or_expr

logical_or_expr  → logical_or_expr OR logical_and_expr
                  | logical_and_expr

logical_and_expr → logical_and_expr AND logical_not_expr
                 | logical_not_expr

logical_not_expr → NOT logical_not_expr
                 | relational_expr

relational_expr  → simple_exp
                 | simple_exp relational_op simple_exp

relational_operator-> EQUAL
		     | NEQUAL
		     | LESSTHEN
		     |LESSEQUALS
		     |GREATTHAN
		     |GREATEQUALS

simple_exp -> simple_exp add_op termo
  	   | termo

add_op → PLUS
	| MINUS

termo   → termo mul_op factor
	| factor

mul_op  → MULT
	| DIVIDE
	| MODULO
	| DIV_INT


factor  → LENGTH LPAREN expression RPAREN
	| LPAREN expression RPAREN
	| variable
        | NUMBER
        | REAL_LITERAL
        | STRING_LITERAL
        | TRUE
        | FALSE

```
Como se pode ver a gramática foi organizada de forma hierárquica para respeitar a precedência dos operadores. Operadores com menor prioridade *(como OR e AND)* aparecem nos níveis superiores, enquanto que os de maior precedência *(como MULT, DIVIDE e MODULO)* estão mais abaixo. Isto garante que a *AST* reflita corretamente a ordem de avaliação das expressões, processando primeiro os cálculos mais específicos antes das operações lógicas e relacionais.

Para reforçar esta organização, também atualizámos o **Yacc** com uma tabela de precedências, permitindo que o parser resolva ambiguidades durante a análise sintática. Ordenada da menor para a maior prioridade, esta tabela garante que o Yacc aplique corretamente as regras de associatividade e precedência entre operadores, preservando na AST a semântica correta das expressões. 
```python
# precedências: de cima para baixo → menor para maior prioridade
precedence = (
    ('left',  'OR'),
    ('left',  'AND'),
    ('right', 'NOT'),
    ('nonassoc',
       'EQUAL','NEQUAL',
       'LESSTHEN','LESSEQUALS',
       'GREATTHAN','GREATEQUALS'
    ),
    ('left',  'PLUS', 'MINUS'),
    ('left',  'MULT', 'DIVIDE', 'MODULO', 'DIV_INT'),
)
```
Após termos atualizado o `ast_nodes.py` com os novos nós necessários, passámos à expansão do codegen.py para dar suporte à geração de código para expressões.
Nesta secção, foram tratados vários tipos de nós que representam operações binárias, relacionais, booleanas, valores literais (inteiros, reais, booleanos, strings) e acessos a variáveis simples ou indexadas. Cada um destes nós gera instruções específicas da VM, como ADD, SUB, EQUAL, PUSHI, entre outras, sendo o código gerado acumulado na nossa lista principal de instruções.

```python
# ------------------- Expressões -------------------
    elif isinstance(node, BinOpNode):
        code.extend(generate_code(node.left, symbol_table))
        code.extend(generate_code(node.right, symbol_table))
        # depois operador
        op = node.op
        if op == '+':   code.append("ADD")
        elif op == '-': code.append("SUB")
        elif op == '*': code.append("MUL")
        elif op == '/': code.append("DIV")
        elif op == 'mod': code.append("MOD")
        elif op == 'div': code.append("DIV")
        elif op == 'and': code.append("AND")
        elif op == 'or':  code.append("OR")

    elif isinstance(node, NotNode):
        # NOT expr
        code.extend(generate_code(node.expr, symbol_table))
        code.append("NOT")


    elif isinstance(node, RelOpNode):
        code.extend(generate_code(node.left, symbol_table))
        code.extend(generate_code(node.right, symbol_table))
        ro = node.op
        if ro == '=':      code.append("EQUAL")
        elif ro == '<>':
            code.append("EQUAL")
            code.append("NOT")
        elif ro == '<':    code.append("INF")
        elif ro == '<=':   code.append("INFEQ")
        elif ro == '>':    code.append("SUP")
        elif ro == '>=':   code.append("SUPEQ")

    elif isinstance(node, NumberNode):
        code.append(f"PUSHI {node.value}")

    elif isinstance(node, RealNode):
        code.append(f"PUSHF {node.value}")

    elif isinstance(node, StringNode):
        code.append(f'PUSHS "{node.value}"')
        if len(node.value) == 1:
            code.append("CHRCODE")

    elif isinstance(node, BoolNode):
        # true → 1, false → 0
        code.append(f"PUSHI {1 if node.value else 0}")

    elif isinstance(node, LengthNode):
        code.extend(generate_code(node.expr, symbol_table))
        # se for string → STRLEN, se for array → PUSHI size
        if isinstance(node.expr, VariableNode):
            info = symbol_table[node.expr.id]
            if info["type"] == "string":
                code.append("STRLEN")
            else:  # array
                code.append(f"PUSHI {info['size']}")
        else:
            # caso genérico (assume string)
            code.append("STRLEN")

    elif isinstance(node, VariableNode):
        if node.index is None:
            code.append(f"PUSHG {symbol_table[node.id]['offset']}")
        else:
            info = symbol_table[node.id]
            code.append(f"PUSHG {info['offset']}")
            code.extend(generate_code(node.index, symbol_table))
            if info["type"] == "string":
                code.append("PUSHI 1")
                code.append("SUB")
                code.append("CHARAT")    
            else:
                code.append(f"PUSHI {info['low_bound']}")
                code.append("SUB")
                code.append("LOADN")  

```
Importa ainda referir que, no caso de operações sobre strings em que se pretende aceder a uma posição específica, é necessário subtrair uma unidade ao índice desejado. Isto deve-se ao facto de, em Pascal, a indexação de strings começar em 1, enquanto na máquina virtual utilizada, a indexação é feita a partir do 0. Para garantir o acesso correto à posição pretendida, o codegen gera instruções adicionais que subtraem 1 ao valor do índice antes de aceder à string. Esta mesma lógica aplica-se aos arrays, uma vez que, em Pascal, é possível declarar arrays cuja posição inicial não seja 0.
#

#### If
Para lidar com o bloco condicional *(IF)*, desenvolvemos as seguintes produções gramaticais.

```bash
conditional_stmt  -> if_stmt

if_stmt           -> IF expression THEN stmt
                   | IF expression THEN stmt ELSE stmt

```
Dentro do **if** temos de ter uma expressão logica, para conseguirmos obter um valor booleano. E em contrapartida após um **then** e um **else** podemos ter qualquer `statement`, sendo que o bloco **else** é opcional.

Desta forma, após expandirmos o YACC, acrescentamos ao `ast_nodes.py`, o seguinte nodo:

- O `IfStmtNode` que é responsável por armazenar a condição do if, o bloco correspondente ao ramo then e, opcionalmente, o bloco else. Caso o programa original não contenha um ramo else, este campo é definido como `None`.

Posto isto, procedemos à expansão do `codegen.py` para suportar a geração do código máquina das instruções condicionais para a máquina virtual. 

Para cada bloco  if, associamos uma **label** única que é utilizada nas instruções **JZ** e **JUMP** para redirecionar a execução para a *label* correspondente, de acordo com o resultado da avaliação da condição.

Assim sendo, para o seguinte trecho de código Pascal:
```bash
if x > 0 then
    writeln("positivo")
else
    writeln("negativo")
```
Seriam geradas as seguintes instruções:
```bash
...		 # Condição do IF
JZ else1         # caso condição for falsa, salta para else1
...              # bloco do then
JUMP endif1      # salta o else
else1:           # início do else
...              # bloco do else
endif1:          # fim do if

```
- Caso a condição seja falsa salta para o *else1*, ignorando o bloco do *then*. 

- Por outro lado, caso a condição seja verdadeira, executa o bloco dentro do *then* e por fim salta para o *endif1*, ignorando o bloco do *else*.

Para garantir que cada bloco **if** possui identificadores únicos, definimos a função `_new_if_id`, que gera um número sequencial exclusivo para cada ocorrência:

```python
_if_counter = 0
def _new_if_id():
    """
    Incrementa o contador de ifs e devolve um número único.
    """
    global _if_counter
    _if_counter += 1
    return _if_counter
```

Com esta abordagem, conseguimos gerar *labels* únicas como else1, endif1, else2, etc, que são utilizadas para identificar os blocos then e else no código da VM.

Tendo por base toda esta estrutura, chegamos ao seguinte `codegen.py`:
```python
elif isinstance(node, IfStmtNode):
        code.extend(generate_code(node.condition, symbol_table))
        n = _new_if_id()
        else_lbl   = f"else{n}"
        endif_lbl  = f"endif{n}"

        if node.else_stmt is None:
            # if sem else
            code.append(f"JZ {endif_lbl}")
            code.extend(generate_code(node.then_stmt, symbol_table))
            code.append(f"{endif_lbl}:")
        else:
            # if com else
            code.append(f"JZ {else_lbl}")
            # then
            code.extend(generate_code(node.then_stmt, symbol_table))
            code.append(f"JUMP {endif_lbl}")
            # else
            code.append(f"{else_lbl}:")
            code.extend(generate_code(node.else_stmt, symbol_table))
            code.append(f"{endif_lbl}:")
```
Vale ainda acrescentar, que para fazer verificacçõs com strings, de modo a tirar proveito das funcionalidades que a VM oferece, para fazer uma verificacção do tipo `bin[i] = '1'`, utilizamos a função `CHARAT` para obter o codigo ASCII do caracter que se encotra na posição i da string bin e de seguida utilizamos a função `CHRCODE` para obter o código ASCII do elemento ao qual estamos a comparar, que neste caso é a string `'1'`. 
Uma solução alternativa seria tratar as strings como um array de caracteres, mas da forma referida anteriormente conseguimos tirar total proveito das funcionalidades oferecidas pela VM, facultada pelas professores.

#### While

Para suportar os ciclos do Pascal definimos na nossa gramática o `cicle_stmt`. Começando pelo desenvolvimento dos ciclos *while*, de acordo com a recomendação do docente. Após alguma análise da linguagem, chegámos às seguintes produções gramaticais:
```bash
cicle_stmt        -> while_stmt
                   | for_stmt

while_stmt        -> WHILE expression DO cicle_body

cicle_body        -> block
                   | stmt
```
Como se pode ver, o bloco do *while* começa sempre com o token `WHILE` e é seguido por uma condição *booleana*, à semelhança do bloco `IF`. As instruções dentro do bloco começam sempre com a palavra `DO`e as instruções podem ser apenas uma instrução, ou várias instruções contidas dentro de um bloco que começa por  `BEGIN` e termina com `END`.

Tendo isto foram adicionadas as novas funções ao YACC e adicionamos ainda um novo nodo ao `ast_nodes.py`, sendo ele:

- O `WhileStmtNode` que é responsável por armazenar a condição do ciclo while e as instruções a realizar dentro dele

Com o YACC e as AST prontos para lidar com as novas instruções while, faltava atualizar o `codegen.py` para que o mesmo esteja pronto para gerar as novas instruções para a vm.
À semelhança do que foi feito para as instruções *if*, a implementação do ciclo *while* exigiu a criação de labels para controlar o fluxo de execução na *VM*. Estas labels, como referido anteriormente, são essenciais para serem utilizadas juntamente com as instruções **JZ** e **JUMP**, e permitem repetir o bloco de instruções enquanto a condição for verdadeira.

Desta forma, para o seguinte exemplo de código Pascal:
```bash
while x > 0 do
    x := x - 1;
```
Seriam geradas as seguintes instruções:
```bash
while1:           # início do ciclo
...               # verificação da condição (x > 0)
JZ endwhile1      # se a condição for falsa, salta para o fim do ciclo
...               # corpo do ciclo (x := x - 1;)
JUMP while1       # volta ao início do ciclo
endwhile1:        # fim do ciclo
```
Neste exemplo, o programa começa por avaliar a condição 'x > 0'. 
- Se for falsa, salta diretamente para **endwhile1**, e termina o ciclo.
- Caso contrário, executa o bloco do *while* e, no final, salta novamente para while1, repetindo o processo. Garantindo assim que o comportamento do while é respeitado dentro da VM.

Para garantir que cada ciclo while possui identificadores únicos, tal como no exemplo acima, definimos a função `_new_loop_id`, responsável por gerar um número sequencial exclusivo para cada instância do ciclo:
```python
_loop_counter = 0
def _new_loop_id():
    """
    Incrementa o contador de loops e devolve um número único.
    """
    global _loop_counter
    _loop_counter += 1
    return _loop_counter
```

Assim sendo, conseguimos gerar labels únicas, como while1, endwhile1, etc, que são usadas para identificar o ínicio e o fim de cada ciclo. 

Desta forma, chegamos ao seguinte `codegen.py`:
```python
elif isinstance(node, WhileStmtNode):
        n = _new_loop_id()
        start_lbl = f"while{n}"
        end_lbl   = f"endwhile{n}"
        # início do loop
        code.append(f"{start_lbl}:")
        code.extend(generate_code(node.condition, symbol_table))
        # se condição for falsa, salta para fim
        code.append(f"JZ {end_lbl}")
        # corpo do loop
        code.extend(generate_code(node.body, symbol_table))
        # volta ao início
        code.append(f"JUMP {start_lbl}")
        # rótulo de saída
        code.append(f"{end_lbl}:")
```

#### For

Por fim, para tratar do segundo tipo de ciclo existente, o ciclo `FOR`, definimos as seguintes produções  gramáticais:
```bash
for_stmt          -> FOR assign_stmt TO simple_exp DO cicle_block
                   | FOR assign_stmt DOWNTO simple_exp DO cicle_block
```
O ciclo `FOR` é sempre iniciado pelo token `FOR`, e é seguindo de uma atribuição inical do tipo `assign_stmt`. 
A variável de controlo é então incrementada ou decrementada consoante se trate de um ciclo do tipo `TO` ou `DOWNTO`, respetivamente.

À semelança do ciclo `WHILE` o ciclo `FOR` pode conter apenas uma instrução simples ou várias instruções contidas entre um `BEGIN` e um `END`.

Após termos atualizado o YACC com as funções de acordo com as novas produções gramaticais, definimos o novo nodo no `ast_nodes.py`: 

- O `ForStmtNode` que é responsável por representar o *for*, armazenando a atribuição inicial, o tipo de iteração (*TO* ou *DOWNTO*), a condição de paragem e, por fim, o conjunto de instruções a executar dentro do ciclo.

Tal como no ciclo *while*, o ciclo *for* irá utilizar o mesmo sistema de *labels*, para marcar o inicio e fim do ciclo, juntamente com as intruções de salto da VM, para garantir o comportamento ciclíco dos mesmos. No entanto, os blocos internos são ajustados para refletir a lógica específica do *for*, incluindo a inicialização da variável de controlo, a verificação da condição de paragem com base na direção (*TO* ou *DOWNTO*) e o respetivo incremento ou decremento da variável após cada iteração.

Tendo isso, para o seguinte exemplo pascal:
```bash
for i := 1 to 2 do
    writeln(i);
```
Seriam geradas as seguintes instruções:
```bash
PUSHI 1         # inicialização: i := 1
STOREG 0        # guarda no i (supondo que o i está na posição 0 da stack)

for1:           # início do ciclo
PUSHG 0         # get do valor atual de i
PUSHI 2         # limite superior
INFEQ           # verifica se i <= 2
JZ endfor1      # casoseja  falso, salta para o fim do ciclo

PUSHG 0         # carrega i
WRITES          # escreve o valor de i

PUSHG 0         # incremento: i := i + 1
PUSHI 1
ADD
STOREG 0        # atualiza o valor de i

JUMP for1       # volta ao início do ciclo
endfor1:        # fim do ciclo
```
Neste exemplo, o ciclo começa por inicializar a variável 'i' com o valor 1. Em cada iteração, verifica se i <= 2. Se a condição for verdadeira, executa o corpo do ciclo (neste caso, imprime i) e incrementa o valor de i (uma vez que o ciclo é do tipo *TO* e não *DOWNTO*, se não tinhamos de decrementar). Quando a condição deixa de ser satisfeita, o programa salta para `endfor1`, terminando o ciclo.

Desta forma, atualizamos o `codegen.py` para refeltir esta nova funcionalidade:

```python
    if isinstance(node, ForStmtNode):
        code.extend(generate_code(node.init_assign, symbol_table))

        n = _new_loop_id()
        start_lbl = f"for{n}"
        end_lbl   = f"endfor{n}"

        code.append(f"{start_lbl}:")
        # condição i <= limit ou i >= limit
        var    = node.init_assign.variable
        offset = symbol_table[var.id]['offset']
        code.append(f"PUSHG {offset}")
        code.extend(generate_code(node.bound_expr, symbol_table))
        code.append("INFEQ" if node.direction == 'to' else "SUPEQ")
        code.append(f"JZ {end_lbl}")

        code.extend(generate_code(node.body, symbol_table))

        # incremento/decremento
        code.append(f"PUSHG {offset}")
        code.append("PUSHI 1")
        code.append("ADD" if node.direction == 'to' else "SUB")
        code.append(f"STOREG {offset}")

        code.append(f"JUMP {start_lbl}")
        code.append(f"{end_lbl}:")
```

## 4 Análise Semântica
De forma a garantir que o código Pascal que está a ser compilado está de acordo com as regras da linguagem Pascal implementamos um analisador léxico. Este é responsável por verificar que todas as variáveis usadas foram declaradas, que os tipos de dados envolvidos nas operações são compativeis e uma coerência geral do código.

Com esse objetivo foi criada a função `check_semantics(ast, symbol_table)`. Esta recebe a representação intermédia (AST) criada e a tabela de símbolos, e percorre todos os nodos da árvore para aplicar as verificações consoante o nodo recebido, estando a verificação da declaração das variáveis e a verificação dos tipos de dados separadas nas funções `check_variable` e `infer_type`, respetivamente. A função `check_semantics` devolve um array de erros, que será vazio no caso de o código ser válido ou, em caso contrário, listará os erros encontrados.

### Verificação da declaração das variáveis
Esta verificação é aplicada nos seguinte nodos:
- `AssignNode`
- `VariableNode`
- `ForStmtNode`
- `ReadLnStmtNode`
- `WriteStmtNode`
- `WriteLnStmtNode`

A função `check_variable` é  responsável por esta verificação, e podemos verificar a sua estrutura no código abaixo.

```python
def check_variable(var_node):
        var_id = var_node.id
        if var_id not in symbol_table:
            errors.append(f"Erro: Variável '{var_id}' usada mas não declarada.")
            return

        if var_node.index is not None:
            var_info = symbol_table[var_id]
            if var_info["type"] != "structured" and var_info["type"] != "string":
                errors.append(f"Erro: Variável '{var_id}' não é um array mas foi indexada.")
            visit(var_node.index)
            index_type = infer_type(var_node.index)
            if index_type != "integer":
                errors.append(f"Erro: Índice de array '{var_id}' deve ser do tipo 'integer', mas é do tipo '{index_type}'.")
```

A função recebe um nodo de uma variável, `var_node`. A função obtém o _id_ do nodo e verifica se o _id_ existe na tabela de símbolos. Em caso negativo, é adicionado ao array de erros uma mensagem a indicar que a variável em questão não foi declarada. Após essa verificação inicial a função verifica se o atributo _index_ do nodo possui um valor, o que indica se se trata de um acesso a uma posição da variável, algo que apenas é possível para variáveis do tipo _string_ e _structured_. Em caso afirmativo, irá aceder à tabela de símbolos para obter o __type__ da variável e, se este for diferente de _structured_ ou _string_, irá adicionar ao array de erros uma mensagem indicando que a variável não é um array mas está a ser indexada. Verifica ainda o tipo do valor no _index_ (usando a função `infer_type`), e no caso deste não ser _integer_, adiciona ao array de erros uma mensagem a indicar que o índice do array deve ser do tipo _integer_.

### Verificação dos tipos de dados

Esta verificação é aplicada nos seguintes nodos:

- `AssignNode`
- `RelOpNode`
- `BinOpNode`

A função `infer_type(node)`, abaixo apresentada, infere o tipo de dados do nodo recebido.

```python
def infer_type(node):
        if isinstance(node, NumberNode):
            return "integer"
        elif isinstance(node, RealNode):
            return "real"
        elif isinstance(node, StringNode):
            return "string"
        elif isinstance(node, BoolNode):
            return "boolean"
        elif isinstance(node, VariableNode):
            var_id = node.id
            if var_id in symbol_table:
                var_info = symbol_table[var_id]
                if node.index is not None:
                    if var_info["type"] == "structured":
                        return var_info["elem_type"]
                    elif var_info["type"] == "string":
                        return "string" 
                    else:
                        return "unknown"
                return var_info["type"]
            return "unknown"
        elif isinstance(node, BinOpNode):
            left_type = infer_type(node.left)
            right_type = infer_type(node.right)
            if left_type == right_type:
                return left_type
            return "unknown"
        elif isinstance(node, RelOpNode):
            return "boolean"
        elif isinstance(node, NotNode):
            return "boolean"
        elif isinstance(node, LengthNode):
            return "integer"
        else:
            return "unknown"
```

A função recebe um nodo e verifica a que classe é que o nodo pertence. No caso de ser um nodo das classes `NumberNode`,`RealNode`, `StringNode` ou `BoolNode` irá retornar _integer__, _real_, _string_ ou _boolean_, respetivamente. Se o nodo for das classes `RelOpNode` ou `NotNode`, que são operações booleanas, irá retornar _boolean__ e se o nodo for `LengthNode`, que corresponde à função _length_ que devolve o tamanho de um array, irá retornar _integer_. Os dois casos que necessitam de verificações adicionais são: `VariableNode` e `BinOpNode`.

No caso de o nodo ser da classe `VariableNode` irá verificar se se trata de um acesso a um indíce de um array ou não. Não sendo, este irá devolver o _type_ da variável. No caso de ser um indíce de um array, a função determina se é do tipo _structured_, para o qual irá devolver o tipo dos elementos do array, ou _string_, para o qual irá devolver _string_.

Para os nodos da classe `BinOpNode`, irá, recursivamente, verificar o tipo do lado direito e do lado esquerdo da operação. No caso de serem iguais, a função devolve o tipo do lado esquerdo.

Se a função não for capaz de determinar o tipo, esta devolve _unknown_.

Fazendo uso dos tipos devolvidos por esta função, a função global de verificação irá verificar se os tipos inferidos são compativeis, e se não forem adicionar ao array de erros uma mensagem a indicar que os tipos são incompatíveis.

## 5 Testes Realizados e resultados obtidos
A seguir, mostramos os testes realizados, os **outputs gerados** e a respetiva validação dos resultados. Os testes cobrem diferentes cenários, de forma a verificar que o compilador se comporta corretamente em diferentes situações.

### Teste 1
Para um seguinte exemplo em pascal:
```bash
program HelloWorld;
begin
writeln('Ola, Mundo!');
end.
```
Obtivemos o seguinte output:
```bash
START
PUSHS "Ola, Mundo!"
WRITES
WRITELN
STOP
```

### Teste 2
Para um seguinte exemplo em pascal:
```bash
program Maior3;
var
num1, num2, num3, maior: Integer;
begin
{ Ler 3 números }
Write('Introduza o primeiro número: ');
ReadLn(num1);
Write('Introduza o segundo número: ');
ReadLn(num2);
Write('Introduza o terceiro número: ');
ReadLn(num3);
{ Calcular o maior }
if num1 > num2 then
if num1 > num3 then maior := num1
else maior := num3
else
if num2 > num3 then maior := num2
else maior := num3;
{ Escrever o resultado }
WriteLn('O maior é: ', maior)
end.
```
Obtivemos o seguinte output:
```bash
PUSHI 0
PUSHI 0
PUSHI 0
PUSHI 0
START
PUSHS "Introduza o primeiro número: "
WRITES
READ
ATOI
STOREG 0
PUSHS "Introduza o segundo número: "
WRITES
READ
ATOI
STOREG 1
PUSHS "Introduza o terceiro número: "
WRITES
READ
ATOI
STOREG 2
PUSHG 0
PUSHG 1
SUP
JZ else1
PUSHG 0
PUSHG 2
SUP
JZ else2
PUSHG 0
STOREG 3
JUMP endif2
else2:
PUSHG 2
STOREG 3
endif2:
JUMP endif1
else1:
PUSHG 1
PUSHG 2
SUP
JZ else3
PUSHG 1
STOREG 3
JUMP endif3
else3:
PUSHG 2
STOREG 3
endif3:
endif1:
PUSHS "O maior é: "
WRITES
PUSHG 3
WRITEI
WRITELN
STOP
```

### Teste 3
Para um seguinte exemplo em pascal:
```bash
program Fatorial;
var
n, i, fat: integer;
begin
writeln('Introduza um número inteiro positivo:');
readln(n);
fat := 1;
for i := 1 to n do
fat := fat * i;
writeln('Fatorial de ', n, ': ', fat);
end.
```
Obtivemos o seguinte output:
```bash
PUSHI 0
PUSHI 0
PUSHI 0
START
PUSHS "Introduza um número inteiro positivo:"
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHI 1
STOREG 2
PUSHI 1
STOREG 1
for1:
PUSHG 1
PUSHG 0
INFEQ
JZ endfor1
PUSHG 2
PUSHG 1
MUL
STOREG 2
PUSHG 1
PUSHI 1
ADD
STOREG 1
JUMP for1
endfor1:
PUSHS "Fatorial de "
WRITES
PUSHG 0
WRITEI
PUSHS ": "
WRITES
PUSHG 2
WRITEI
WRITELN
STOP
```

### Teste 4
Para um seguinte exemplo em pascal:
```bash
program NumeroPrimo;
var
num, i: integer;
primo: boolean;
begin
writeln('Introduza um número inteiro positivo:');
readln(num);
primo := true;
i := 2;
while (i <= (num div 2)) and primo do
begin
if (num mod i) = 0 then
primo := false;
i := i + 1;
end;
if primo then
writeln(num, ' é um número primo')
else
writeln(num, ' não é um número primo')
end.
```
Obtivemos o seguinte output:
```bash
PUSHI 0
PUSHI 0
PUSHI 0
START
PUSHS "Introduza um número inteiro positivo:"
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHI 1
STOREG 2
PUSHI 2
STOREG 1
while1:
PUSHG 1
PUSHG 0
PUSHI 2
DIV
INFEQ
PUSHG 2
AND
JZ endwhile1
PUSHG 0
PUSHG 1
MOD
PUSHI 0
EQUAL
JZ endif1
PUSHI 0
STOREG 2
endif1:
PUSHG 1
PUSHI 1
ADD
STOREG 1
JUMP while1
endwhile1:
PUSHG 2
JZ else2
PUSHG 0
WRITEI
PUSHS " é um número primo"
WRITES
WRITELN
JUMP endif2
else2:
PUSHG 0
WRITEI
PUSHS " não é um número primo"
WRITES
WRITELN
endif2:
STOP
```

### Teste 5
Para um seguinte exemplo em pascal:
```bash
program SomaArray;
var
numeros: array[1..5] of integer;
i, soma: integer;
begin
soma := 0;
writeln('Introduza 5 números inteiros:');
for i := 1 to 5 do
begin
readln(numeros[i]);
soma := soma + numeros[i];
end;
writeln('A soma dos números é: ', soma);
end.
```
Obtivemos o seguinte output:
```bash
ALLOC 5
PUSHI 0
PUSHI 0
START
PUSHI 0
STOREG 2
PUSHS "Introduza 5 números inteiros:"
WRITES
WRITELN
PUSHI 1
STOREG 1
for1:
PUSHG 1
PUSHI 5
INFEQ
JZ endfor1
PUSHG 0
PUSHG 1
PUSHI 1
SUB
READ
ATOI
STOREN
PUSHG 2
PUSHG 0
PUSHG 1
PUSHI 1
SUB
LOADN
ADD
STOREG 2
PUSHG 1
PUSHI 1
ADD
STOREG 1
JUMP for1
endfor1:
PUSHS "A soma dos números é: "
WRITES
PUSHG 2
WRITEI
WRITELN
STOP
```

### Teste 6
Para um seguinte exemplo em pascal:
```bash
program BinarioParaInteiro;
var
bin: string;
i, valor, potencia: integer;
begin
writeln('Introduza uma string binária:');
readln(bin);
valor := 0;
potencia := 1;
for i := length(bin) downto 1 do
begin
if bin[i] = '1' then
valor := valor + potencia;
potencia := potencia * 2;
end;
writeln('O valor inteiro correspondente é: ', valor);
end.
```
Obtivemos o seguinte output:
```bash
PUSHS ""
PUSHI 0
PUSHI 0
PUSHI 0
START
PUSHS "Introduza uma string binária:"
WRITES
WRITELN
READ
STOREG 0
PUSHI 0
STOREG 2
PUSHI 1
STOREG 3
PUSHG 0
STRLEN
STOREG 1
for1:
PUSHG 1
PUSHI 1
SUPEQ
JZ endfor1
PUSHG 0
PUSHG 1
PUSHI 1
SUB
CHARAT
PUSHS "1"
CHRCODE
EQUAL
JZ endif1
PUSHG 2
PUSHG 3
ADD
STOREG 2
endif1:
PUSHG 3
PUSHI 2
MUL
STOREG 3
PUSHG 1
PUSHI 1
SUB
STOREG 1
JUMP for1
endfor1:
PUSHS "O valor inteiro correspondente é: "
WRITES
PUSHG 2
WRITEI
WRITELN
STOP
```

### Teste 7
Para um seguinte exemplo em pascal:
```bash
program SequenciaFibonacci;
var
  n, a, b, temp, contador: integer;
begin
  writeln('Quantos termos da sequência de Fibonacci deseja ver?');
  readln(n);
  a := 0;
  b := 1;
  contador := 1;
  writeln('Sequência de Fibonacci:');
  while contador <= n do
  begin
    writeln(a);
    temp := a + b;
    a := b;
    b := temp;
    contador := contador + 1;
  end;
end.
```
Obtivemos o seguinte output:
```bash
PUSHI 0
PUSHI 0
PUSHI 0
PUSHI 0
PUSHI 0
START
PUSHS "Quantos termos da sequência de Fibonacci deseja ver?"
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHI 0
STOREG 1
PUSHI 1
STOREG 2
PUSHI 1
STOREG 4
PUSHS "Sequência de Fibonacci:"
WRITES
WRITELN
while1:
PUSHG 4
PUSHG 0
INFEQ
JZ endwhile1
PUSHG 1
WRITEI
WRITELN
PUSHG 1
PUSHG 2
ADD
STOREG 3
PUSHG 2
STOREG 1
PUSHG 3
STOREG 2
PUSHG 4
PUSHI 1
ADD
STOREG 4
JUMP while1
endwhile1:
STOP
```

Os testes realizados permitiram validar o funcionamento do compilador desenvolvido, abrangendo uma variedade de estruturas e instruções da linguagem Pascal, como condicionais, ciclos, arrays, strings e operações aritméticas. Em todos os casos, o código gerado apresentou o comportamento esperado dentro da máquina virtual (VM), executando corretamente as instruções e produzindo os outputs previstos para cada programa de entrada. Estes resultados demonstram que o compilador está a traduzir de forma eficaz os programas em Pascal para o código da VM, garantindo a execução correta dos mesmos.


## 6 Conclusão
Durante o desenvolvimento deste projeto, enfrentámos inúmeros desafios, mas também aprofundámos significativamente o nosso conhecimento sobre linguagens de programação, compiladores e o funcionamento interno destes sistemas. Ao longo do percurso, aplicámos os conceitos adquiridos em Processamento de Linguagens, conseguindo implementar com sucesso um compilador standard de Pascal que atende a todos os requisitos base definidos no enunciado.

Um dos maiores desafios que encontrámos foi a escassa documentação disponível para a máquina virtual. A falta de mais exemplos  e de uma referência mais detalhada dificultou consideravelmente a geração de código máquina, exigindo uma dedicação extra para compreender, por tentativa e erro, o que era necessário produzir para garantir a compatibilidade com a VM. Sendo a nossa primeira experiência com este tipo de implementação, o processo exigiu longas horas de análise e experimentação.

Apesar das dificuldades, conseguimos superar cada obstáculo, encontrar soluções para as incertezas e, no final, alcançar com sucesso os objetivos estabelecidos. Este projeto proporcionou-nos uma valiosa experiência prática num domínio que, até então, nos era desconhecido, contribuindo para o nosso crescimento e aprofundamento técnico.
  


