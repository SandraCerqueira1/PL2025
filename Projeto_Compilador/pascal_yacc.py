import ply.yacc as yacc
from pascal_lex import tokens  
from ast_nodes import *
from codegen import *
import os
from semantica import check_semantics

# precedências: de cima para baixo -> menor para maior prioridade
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

# Produção principal: Programa -> PROGRAM ID SEMI opt_variable block DOT
def p_programa(p):
    '''Programa : PROGRAM ID SEMI opt_variable block DOT'''
    p[0] = ProgramaNode(p[2], p[4], p[5])

# opt_variable -> variables | empty
def p_opt_variable(p):
    '''opt_variable : variables
                    | empty'''
    if p[1] is None:
        p[0] = Opt_variableNode(EmptyNode())
    else:
        p[0] = Opt_variableNode(p[1])

# variables -> VAR vars
def p_variables(p):
    '''variables : VAR vars'''
    # p[2] deverá ser uma lista de declarações; encapsulamo-la em VariablesNode
    p[0] = VariablesNode(p[2])

# vars -> listVar DOISPONTOS datatype SEMI
def p_vars_single(p):
    '''vars : listVar DOISPONTOS datatype SEMI'''
    # Cria uma lista com uma declaração única
    # p[1] é um ListVarNode; extraímos a lista de IDs dele
    p[0] = [VarDeclNode(p[1].ids, p[3])]

# vars -> listVar DOISPONTOS datatype SEMI vars
def p_vars_multiple(p):
    '''vars : listVar DOISPONTOS datatype SEMI vars'''
    # Junta a declaração atual com as restantes (p[5] já é uma lista)
    p[0] = [VarDeclNode(p[1].ids, p[3])] + p[5]

# listVar -> ID
def p_listVar_single(p):
    '''listVar : ID'''
    p[0] = ListVarNode([p[1]])

# listVar -> ID VIRG listVar
def p_listVar_multiple(p):
    '''listVar : ID VIRG listVar'''
    # Junta o ID atual com a lista já construída (p[3] é um ListVarNode)
    p[0] = ListVarNode([p[1]] + p[3].ids)

# datatype -> simpleType | structuredType
def p_datatype_simple(p):
    '''datatype : simpleType'''
    p[0] = DatatypeNode(p[1])
def p_datatype_structured(p):
    '''datatype : structuredType'''
    p[0] = DatatypeNode(p[1])

# simpleType -> INTEGER_TYPE | BOOLEAN_TYPE | STRING_TYPE | REAL_TYPE | CHAR_TYPE
def p_simpleType(p):
    '''simpleType : INTEGER_TYPE
                  | BOOLEAN_TYPE
                  | STRING_TYPE
                  | REAL_TYPE
                  | CHAR_TYPE'''
    p[0] = SimpleTypeNode(p[1])

# structuredType -> arrayType
def p_structuredType(p):
    '''structuredType : arrayType'''
    p[0] = StructuredTypeNode(p[1])

# arrayType -> ARRAY LSQBRACKET NUM RANGE NUM RSQBRACKET OF simpleType
def p_arrayType(p):
    '''arrayType : ARRAY LSQBRACKET NUMBER RANGE NUMBER RSQBRACKET OF simpleType'''
    p[0] = ArrayTypeNode(p[3], p[5], p[8])

# empty -> 
def p_empty(p):
    'empty :'
    p[0] = None

def p_variable_simple(p):
    '''variable : ID'''
    p[0] = VariableNode(p[1])

def p_variable_array(p):
    '''variable : ID LSQBRACKET expression RSQBRACKET'''
    p[0] = VariableNode(p[1], p[3])

# --- Produções do bloco ---

# block -> BEGIN stmt_list END
def p_block(p):
    'block : BEGIN stmt_list opt_semi END'
    p[0] = BlockNode(p[2])

def p_opt_semi(p):
    '''opt_semi : SEMI
                | empty'''
    # nada especial para devolver
    p[0] = None

# stmt_list -> stmt SEMI 
def p_stmt_list_single(p):
    '''stmt_list : stmt'''
    p[0] = StmtListNode([p[1]])

# stmt_list -> stmt SEMI stmt_list 
def p_stmt_list_multiple(p):
    '''stmt_list : stmt_list SEMI stmt'''
    # p[1] é um stmt; p[3] é o restante da lista (StmtListNode)
    # Junta numa lista
    p[0] = StmtListNode(p[1].statements + [p[3]])



# stmt -> assign_stmt 
    # | conditional_stmt 
    # | cicle_stmt 
    # | read_stmt 
    # | write_stmt 
    # | writeln_stmt
def p_stmt(p):
    '''stmt : assign_stmt
            | conditional_stmt
            | cicle_stmt
            | readLn_stmt
            | write_stmt
            | writeln_stmt'''
    p[0] = p[1]    

#----------------ASSIGN STMT-------------------------------------
def p_assign_stmt(p):
    '''assign_stmt : variable ASSIGN expression'''
    p[0] =  AssignNode(p[1], p[3])

def p_expression(p):
    'expression : logical_or_expr'
    p[0] = p[1]

# OR mais baixo
def p_logical_or(p):
    'logical_or_expr : logical_or_expr OR logical_and_expr'
    p[0] = BinOpNode(p[1], 'or', p[3])
def p_logical_or_single(p):
    'logical_or_expr : logical_and_expr'
    p[0] = p[1]

# AND intermédio
def p_logical_and(p):
    'logical_and_expr : logical_and_expr AND logical_not_expr'
    p[0] = BinOpNode(p[1], 'and', p[3])

def p_logical_and_single(p):
    'logical_and_expr : logical_not_expr'
    p[0] = p[1]

# NOT 
def p_logical_not(p):
    'logical_not_expr : NOT logical_not_expr'
    p[0] = NotNode(p[2])
    
def p_logical_not_rel(p):
    'logical_not_expr : relational_expr'
    p[0] = p[1]

# comparação relacional
def p_relational_expr_simple(p):
    'relational_expr : simple_exp'
    p[0] = p[1]

def p_relational_expr_rel(p):
    'relational_expr : simple_exp relational_operator simple_exp'
    p[0] = RelOpNode(p[1], p[2], p[3])


def p_relational_operator(p):
    '''relational_operator : EQUAL
                            | NEQUAL
                            | LESSTHEN
                            | LESSEQUALS
                            | GREATTHAN
                            | GREATEQUALS'''
    p[0] = p[1]

# simple_exp -> termo add_op simple_exp 
def p_simple_exp_binop(p):
    'simple_exp : simple_exp add_op termo'
    p[0] = BinOpNode(p[1], p[2], p[3])

# simple_exp -> termo    
def p_simple_exp_termo(p):
    'simple_exp : termo'
    p[0] = p[1]

def p_add_op_plus(p):
    'add_op : PLUS'
    p[0]= '+'

def p_add_op_minus(p):
    'add_op : MINUS'
    p[0]='-'

# termo -> termo mul_op factor
def p_termo_binop(p):
    'termo : termo mul_op fator'
    p[0] = BinOpNode(p[1], p[2], p[3])

# termo -> fator
def p_termo_factor(p):
    'termo : fator'
    p[0] = p[1]

# mul_op -> MULT | DIVIDE | MODULO | DIV_INT
def p_mul_op_mult(p):
    'mul_op : MULT'
    p[0] = '*'

def p_mul_op_div(p):
    'mul_op : DIVIDE'
    p[0] = '/'

def p_mul_op_mod(p):
    'mul_op : MODULO'
    p[0] = 'mod'

def p_mul_op_divint(p):
    'mul_op : DIV_INT'
    p[0] = 'div'

# fator -> LENGTH LPAREN expression RPAREN
def p_fator_length(p):
    'fator : LENGTH LPAREN expression RPAREN'
    p[0] = LengthNode(p[3])

# fator -> LPAREN expression RPAREN
def p_fator_group(p):
    'fator : LPAREN expression RPAREN'
    p[0] = p[2]

# fator → variable
def p_fator_variable(p):
    'fator : variable'
    p[0] = p[1]
# fator -> NUMBER
def p_fator_number(p):
    'fator : NUMBER'
    p[0] = NumberNode(p[1])

# fator -> REAL_LITERAL
def p_fator_real(p):
    'fator : REAL_LITERAL'
    p[0] = RealNode(p[1])

# fator -> STRING_LITERAL
def p_fator_string(p):
    'fator : STRING_LITERAL'
    p[0] = StringNode(p[1])

# fator -> TRUE
def p_fator_true(p):
    'fator : TRUE'
    p[0] = BoolNode(True)

# fator -> FALSE
def p_fator_false(p):
    'fator : FALSE'
    p[0] = BoolNode(False)


#---------------------------------------------Fim das do Assign----------        

# readLn_stmt -> READLN LPAREN ID RPAREN
def p_readLn_stmt(p):
    '''readLn_stmt : READLN LPAREN variable RPAREN'''
    p[0] = ReadLnStmtNode(p[3])

# write_stmt -> WRITE LPAREN output_args RPAREN
def p_write_stmt(p):
    '''write_stmt : WRITE LPAREN output_args RPAREN'''
    p[0] = WriteStmtNode(p[3])   

# writeln_stmt -> WRITELN LPAREN output_args RPAREN
def p_writeln_stmt_not_empty(p):
    '''writeln_stmt : WRITELN LPAREN output_args RPAREN'''
    p[0] = WriteLnStmtNode(p[3])

# writeln_stmt -> WRITELN LPAREN RPAREN    
def p_writeln_stmt_empty(p):
    '''writeln_stmt : WRITELN LPAREN RPAREN''' #usado pk vi que no pascal o vazio no writeln é um \n
    p[0] = WriteLnStmtNode() 

# output_args -> output_item
def p_output_args_single(p):
    '''output_args : output_item'''
    p[0] = OutputArgsNode([p[1]])

# output_args -> output_item VIRG output_args
def p_output_args_multiple(p):
    '''output_args : output_item VIRG output_args'''
    p[0] = OutputArgsNode([p[1]] + p[3].items)

# output_item -> STRING_LITERAL
def p_output_item_string(p):
    '''output_item : STRING_LITERAL'''
    p[0] = OutputItemNode(p[1])

# output_item -> variable
def p_output_item_variable(p):
    '''output_item : variable'''
    p[0] = OutputItemNode(p[1])   


def p_conditional_stmt(p):
    '''conditional_stmt : if_stmt'''
    p[0] = p[1]

def p_if_then(p):
    '''if_stmt : IF expression THEN stmt'''
    p[0] = IfStmtNode(p[2], p[4])

def p_if_then_else(p):
    '''if_stmt : IF expression THEN stmt ELSE stmt'''
    p[0] = IfStmtNode(p[2], p[4], p[6])    

def p_cicle_stmt(p):
    '''cicle_stmt : while_stmt
                  | for_stmt'''
    p[0] = p[1]         

# while_stmt -> WHILE expression DO cicle_body
def p_while_stmt(p):
    'while_stmt : WHILE expression DO cicle_body'
    p[0] = WhileStmtNode(p[2], p[4])

# cicle_body -> block | stmt
                
def p_cicle_body(p):
    '''cicle_body : block
                  | stmt'''
    p[0] = p[1]


def p_for_stmt_to(p):
    'for_stmt : FOR assign_stmt TO simple_exp DO cicle_body'
    p[0] = ForStmtNode(p[2], 'to',   p[4], p[6])

# for_stmt -> FOR assign_stmt DOWNTO simple_exp DO cicle_body
def p_for_stmt_downto(p):
    'for_stmt : FOR assign_stmt DOWNTO simple_exp DO cicle_body'
    p[0] = ForStmtNode(p[2], 'downto', p[4], p[6])
    
def p_error(p):
    if p:
        print("Erro de sintaxe em:", p.value)
    else:
        print("Erro de sintaxe no final da entrada")

# Criação do parser
parser = yacc.yacc()

input_path = os.path.join("Tests", "test_2.txt")

try:
    with open(input_path, "r", encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:
    print(f"Ficheiro {input_path} não encontrado.")
    data = ""

ast = parser.parse(data)
symbol_table = build_symbol_table(ast)
erros = check_semantics(ast, symbol_table)

if erros:
    for err in erros:
        print(err)
else:
    with open("Output/yacc_out.txt", "w", encoding="utf-8") as f:
        pretty_symbol_table(symbol_table)

        # AST
        f.write("AST:\n")
        f.write(str(ast) + "\n\n")

        # VM Code
        vm_code = generate_program_code(ast)
        f.write("Código para a VM:\n")
        for instr in vm_code:
            f.write(instr + "\n")
