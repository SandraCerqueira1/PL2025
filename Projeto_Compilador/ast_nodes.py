# ast_nodes.py

# Classe base para todos os nós da AST (opcional, mas útil para ter uma interface comum)
class ASTNode:
    def __init__(self):
        pass

    def __repr__(self):
        return self.__str__()

# Nó correspondente ao não-terminal Programa
class ProgramaNode(ASTNode):
    def __init__(self, prog_id, opt_variable, block):
        self.prog_id = prog_id            # Nome do programa (string)
        self.opt_variable = opt_variable  # Nó do não-terminal opt_variable
        self.block = block                # Nó do não-terminal block
    
    def __str__(self):
        return f"Programa({self.prog_id}, {self.opt_variable}, {self.block})"

#----------------------------------Variables parte -----------------------------

# Nó para o não-terminal opt_variable (pode ser variables ou empty)
class Opt_variableNode(ASTNode):
    def __init__(self, child):
        self.child = child  # Instância de VariablesNode ou EmptyNode

    def __str__(self):
        return f"Opt_variable({self.child})"

# Nó para o não-terminal variables (quando há declarações de variáveis)
class VariablesNode(ASTNode):
    def __init__(self, vars_node):
        self.vars_node = vars_node  # Espera receber o nó "vars" uma lista de declarações

    def __str__(self):
        return f"Variables({self.vars_node})"

# Nó para o não-terminal vars que contém uma lista de declarações de variáveis
class VarsNode(ASTNode):
    def __init__(self, var_decls):
        self.var_decls = var_decls  # Lista de VarDeclNode

    def __str__(self):
        return f"Vars({self.var_decls})"

# Nó para a produção listVar (lista de identificadores)
class ListVarNode(ASTNode):
    def __init__(self, ids):
        self.ids = ids  # Lista de strings

    def __str__(self):
        return f"ListVar({self.ids})"

# Nó para o não-terminal datatype que pode ser um tipo (simples ou estruturado)
class DatatypeNode(ASTNode):
    def __init__(self, type_node):
        self.type_node = type_node  # Instância de SimpleTypeNode ou StructuredTypeNode

    def __str__(self):
        return f"Datatype({self.type_node})"

# Nó para o não-terminal simpleType
class SimpleTypeNode(ASTNode):
    def __init__(self, type_name):
        self.type_name = type_name  # String por exemplo "INTEGER_TYPE"
    
    def __str__(self):
        return f"SimpleType({self.type_name})"

# Nó para o não-terminal structuredType (aka arrayType)
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

# Nó para declarações de variáveis (representa a produção: listVar DOISPONTOS datatype SEMI)
class VarDeclNode(ASTNode):
    def __init__(self, list_var_ids, datatype):
        self.list_var_ids = list_var_ids  # Lista de strings (identificadores)
        self.datatype = datatype          # Nó DatatypeNode
    def __str__(self):
        return f"VarDecl({self.list_var_ids}, {self.datatype})"

# Nó para produções vazias
class EmptyNode(ASTNode):
    def __str__(self):
        return "Empty"

#----------------------------------Block parte -----------------------------
# Nó para o bloco
class BlockNode(ASTNode):
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list 
    def __str__(self):
        return f"Block({self.stmt_list})"
    
# Nó para a lista de comandos (stmt_list)
class StmtListNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # Lista de nós que representam comandos
    def __str__(self):
        return f"StmtList({self.statements})"

#só para facilitar  a travessia da arvore    
class StmtNode(ASTNode):
    def __init__(self, stmt):
        self.stmt = stmt  # O tipo de stmt real do comando (por exemplo, ReadStmtNode)
    def __str__(self):
        return f"Stmt({self.stmt})"


# Nó para read_stmt
class ReadLnStmtNode(ASTNode):
    def __init__(self, var_node):
        self.var_node = var_node  # Espera um nó da variável (do tipo VariableNode)
    def __str__(self):
        return f"ReadLnStmt({self.var_node})"

# Nó para write_stmt
class WriteStmtNode(ASTNode):
    def __init__(self, output_args):
        self.output_args = output_args  # Um OutputArgsNode
    def __str__(self):
        return f"WriteStmt({self.output_args})"
    
# Nó para writeln_stmt
class WriteLnStmtNode(ASTNode):
    def __init__(self, output_args=None):
        self.output_args = output_args  # Pode ser um OutputArgsNode ou None pk se for vvazio é um \n
    def __str__(self):
        return f"WriteLnStmt({self.output_args})"  

# Nó para output_args (lista de itens a imprimir)
class OutputArgsNode(ASTNode):
    def __init__(self, items):
        self.items = items  # Lista de OutputItemNode
    def __str__(self):
        return f"OutputArgs({self.items})"


# Nó para output_item
class OutputItemNode(ASTNode):
    def __init__(self, value):
        self.value = value  # Pode ser um literal de string ou um ID
    def __str__(self):
        return f"OutputItem({self.value})"    

# -----------------------------------------------------------------------------
# Variáveis/arrays
# -----------------------------------------------------------------------------
class VariableNode(ASTNode):
    def __init__(self, id, index=None):
        self.id    = id
        self.index = index
    def __str__(self):
        if self.index is None:
            return f"Variable({self.id})"
        else:
            return f"Variable({self.id}[{self.index}])"

# -----------------------------------------------------------------------------
# Expressões e atribuições
# -----------------------------------------------------------------------------
class AssignNode(ASTNode):
    def __init__(self, variable, expression):
        self.variable   = variable
        self.expression = expression
    def __str__(self):
        return f"Assign({self.variable}, {self.expression})"

class RelOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right
    def __str__(self):
        return f"RelOp({self.op}, {self.left}, {self.right})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right
    def __str__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"Number({self.value})"

class RealNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"Real({self.value})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"String({self.value})"

class BoolNode(ASTNode):
    def __init__(self, value: bool):
        self.value = value
    def __str__(self):
        return f"Bool({self.value})"

class NotNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return f"Not({self.expr})"

class LengthNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return f"Length({self.expr})"

# -----------------------------------------------------------------------------
# Ifs
# -----------------------------------------------------------------------------

class IfStmtNode(ASTNode):
    def __init__(self, condition, then_stmt, else_stmt=None):
        self.condition = condition      
        self.then_stmt = then_stmt     
        self.else_stmt = else_stmt     

    def __str__(self):
        if self.else_stmt:
            return f"If({self.condition}, Then={self.then_stmt}, Else={self.else_stmt})"
        else:
            return f"If({self.condition}, Then={self.then_stmt})"
        
#-----------------------------------------------------------------------------
# Ciclos
# -----------------------------------------------------------------------------
class WhileStmtNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition}, {self.body})"


class ForStmtNode(ASTNode):
    def __init__(self, init_assign, direction, bound_expr, body):
        self.init_assign = init_assign   # nó AssignNode
        self.direction   = direction     # 'to' ou 'downto'
        self.bound_expr  = bound_expr    # nó SimpleExp (BinOpNode, NumberNode)
        self.body        = body          # nó BlockNode ou StmtNode

    def __str__(self):
        return (f"For({self.init_assign}, "
                f"{self.direction.upper()} {self.bound_expr}, "
                f"{self.body})")
