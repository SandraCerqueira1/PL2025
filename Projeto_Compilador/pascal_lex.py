import ply.lex as lex


# Lista de tokens
tokens = [
    'PROGRAM', 
    'VAR',
    'INTEGER_TYPE', 
    'BOOLEAN_TYPE', 
    'STRING_TYPE', 
    'REAL_TYPE', 
    'CHAR_TYPE',
    'BEGIN',
    'END',
    'IF', 
    'THEN', 
    'ELSE',
    'WHILE', 
    'DO', 
    'FOR', 
    'TO', 
    'DOWNTO',
    'WRITELN', 
    'WRITE', 
    'READLN', 
    'LENGTH',
    'MODULO', 
    'DIV_INT',
    'TRUE',
    'FALSE',
    'AND', 
    'OR', 
    'NOT',
    'ARRAY', 
    'OF',


    'ID',              # Identificadores
    'NUMBER',          # Números inteiros
    'REAL_LITERAL',    # Números reais (decimais)
    'STRING_LITERAL',  # Literais de string (entre aspas simples)
    
    # Operadores aritméticos
    'PLUS',            # +
    'MINUS',           # -
    'MULT',            # *
    'DIVIDE',          # /
    
    'ASSIGN',          # :=

    # Operadores relacionais
    'EQUAL',           # =
    'NEQUAL',          # <>
    'LESSTHEN',        # <
    'LESSEQUALS',      # <=
    'GREATTHAN',       # >
    'GREATEQUALS',     # >=

    'LPAREN',          # (
    'RPAREN',          # )

    # Separadores
    'SEMI',            # ;
    'VIRG',            # ,
    'DOT',             # .
    'DOISPONTOS',      # :

    # Tokens para arrays
    'LSQBRACKET',      # [
    'RSQBRACKET',      # ]
    'RANGE'            # ..
]


# Expressões regulares para tokens simples
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
t_LSQBRACKET = r'\['    # [
t_RSQBRACKET = r'\]'    # ]


# Ignorar espaços e tabs
t_ignore = ' \t'


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


# Identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# RANGE como função para garantir que nao é confundido com ponto
def t_RANGE(t):
    r'\.\.'
    return t

def t_REAL_LITERAL(t):
    r'(\-)?\d+\.\d+'
    t.value = float(t.value)
    return t
# Números inteiros e reais
def t_NUMBER(t):
    r'(\-)?\d+'
    t.value = int(t.value)
    return t

# Strings entre aspas simples
def t_STRING_LITERAL(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Comentários em pascal (ignorados)
#    { Este é um comentário }
#    (* Este também é um comentário *)
def t_COMMENT(t):
    r'(?s)\(\*.*?\*\)|\{.*?\}'
    t.lexer.lineno += t.value.count("\n")
    pass  

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()

# Teste do lexer
# data = """
# program ExemploReal;
# var
#   num1, num2, soma: real;

# begin
#   writeln('*** Soma de Dois Números Reais ***');
#   writeln;
#   write('Digite o primeiro número real: ');
#   readln(num1);
#   write('Digite o segundo número real: ');
#   readln(num2);
#   soma := num1 + num2;
#   writeln;
#   writeln('O resultado da soma é: ', soma:0:2);
#   writeln;
#   writeln('Pressione ENTER para sair...');
#   readln;
# end.
# """

# lexer.input(data)

# for token in lexer:
#     print(token)
