import ply.lex as lex

tokens = [
    'COMMENT',    
    'VAR',        # ?nome, ?desc
    'INT',        # 1000
    'URI',        # dbo:MusicalArtist
    'STRING',     # Strings entre aspas (ex: "Chuck Berry")
    'LANG',       # Tags de idioma (ex: @en, @pt)
    'A',         
    'DOT',       
    'LCB',       
    'RCB',        
    'ID'          
]

# Palavras-chave reservadas
reserved = {
    'SELECT': 'SELECT',
    'WHERE': 'WHERE',
    'LIMIT': 'LIMIT'
}

tokens = tokens + list(reserved.values())


t_DOT = r'\.'
t_LCB = r'\{'
t_RCB = r'\}' 
t_COMMENT = r'\#.*'
t_LANG = r'@[a-z]{2,3}(-[a-z]{2,3})?'  
t_ignore = ' \t'


def t_VAR(t):
    r'\?[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_URI(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*:[a-zA-Z_][a-zA-Z0-9_-]*'
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_A(t):
    r'\ba\b'
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value) 
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'ID') 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Caractere inesperado: {t.value[0]}")
    t.lexer.skip(1)

# Criar o analisador léxico
lexer = lex.lex()

# Teste
data = """
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
"""

lexer.input(data)
for tok in lexer:
    print(tok.type, tok.value)
