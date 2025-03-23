import ply.lex as lex
tokens = (
    'ADD',
    'MINUS',
    'MULT',
    'DIV',
    'NUMBER',
    'AP',
    'FP'
)

t_ADD = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_AP = r'\('
t_FP = r'\)'

t_ignore = " \n\t"

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character:", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()