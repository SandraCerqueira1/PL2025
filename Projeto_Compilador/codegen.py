from ast_nodes import *
import json

_if_counter = 0
def _new_if_id():
    """
    Incrementa o contador de ifs e devolve um número único.
    """
    global _if_counter
    _if_counter += 1
    return _if_counter

_loop_counter = 0
def _new_loop_id():
    """
    Incrementa o contador de loops e devolve um número único.
    """
    global _loop_counter
    _loop_counter += 1
    return _loop_counter


def build_symbol_table(ast):
    """
    Constrói a tabela de símbolos a partir de ast.opt_variable,
    guarda para cada variável global a:
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


"""
    Gera o codigo para a Vm de acrodo com o nodo da arvore em questão e aquilo que queremos gerar
"""
def generate_code(node, symbol_table):
    code = [] # lista que vai conter o codigo da Vm
    
    if isinstance(node, ProgramaNode):
        code.extend(generate_code(node.opt_variable, symbol_table))
        code.extend(generate_code(node.block, symbol_table))
    
    elif isinstance(node, Opt_variableNode):
        code.extend(generate_code(node.child, symbol_table))
    
    elif isinstance(node, VariablesNode):
        for decl in node.vars_node:
            code.extend(generate_code(decl, symbol_table))
    
    elif isinstance(node, list):
        for item in node:
            code.extend(generate_code(item, symbol_table))
    
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
                
    elif isinstance(node, BlockNode):
        code.extend(generate_code(node.stmt_list, symbol_table))
    
    elif isinstance(node, StmtListNode):
        for stmt in node.statements:
            code.extend(generate_code(stmt, symbol_table))

    # ------------------- Atribuições -------------------
    elif isinstance(node, AssignNode):
        var  = node.variable
        expr = node.expression              # qualquer expressão
        info = symbol_table[var.id]

        if var.index is None:
            code.extend(generate_code(expr, symbol_table))
            code.append(f"STOREG {info['offset']}")
        else:
            code.append(f"PUSHG {info['offset']}")
            code.extend(generate_code(var.index, symbol_table))
            code.extend(generate_code(expr, symbol_table))
            code.append("STOREN")
            
# ─── IfStmtNode ───────────────────────────────────────────────────────────────
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
    # ────────────────────────────────────────────────────────────────────────────────

    # ------------------- Expressões -------------------
    elif isinstance(node, BinOpNode):
        # gera código para filhos
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
        # se for literal de 1 char, converte para código ASCII:
        if len(node.value) == 1: 
            code.append("CHRCODE")

    elif isinstance(node, BoolNode):
        # true -> 1, false -> 0
        code.append(f"PUSHI {1 if node.value else 0}")

    elif isinstance(node, LengthNode):
        # length(expr)
        code.extend(generate_code(node.expr, symbol_table))
        # se for string -> STRLEN, se for array -> PUSHI size
        if isinstance(node.expr, VariableNode):
            info = symbol_table[node.expr.id]
            if info["type"] == "string":
                code.append("STRLEN")
            else:  # array
                code.append(f"PUSHI {info['size']}")
        else:
            # caso genérico
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
                code.append("CHARAT")    # calcula char code da string
            else:
                code.append(f"PUSHI {info['low_bound']}")
                code.append("SUB")
                code.append("LOADN")     # da push do elemento de array

    # ------------------- IO -------------------

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
                    code.append(f"PUSHG {info['offset']}")            # endereço do array
                    code.extend(generate_code(val.index, symbol_table))  # avalia o índice
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
                        code.append(f"PUSHG {info['offset']}")            # endereço do array
                        code.extend(generate_code(val.index, symbol_table))  # avalia o índice
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

    # ─── WhileStmtNode ─────────────────────────────────────────────────────────────
    elif isinstance(node, WhileStmtNode):
        # gera labels únicas para o loop
        n = _new_loop_id()
        start_lbl = f"while{n}"
        end_lbl   = f"endwhile{n}"
        # início do loop
        code.append(f"{start_lbl}:")
        # avalia condição
        code.extend(generate_code(node.condition, symbol_table))
        # se condição for falsa, salta para fim
        code.append(f"JZ {end_lbl}")
        # bloco do loop
        code.extend(generate_code(node.body, symbol_table))
        # volta ao início
        code.append(f"JUMP {start_lbl}")
        # rótulo de saída
        code.append(f"{end_lbl}:")
    # ────────────────────────────────────────────────────────────────────────────────

    # ─── ForStmtNode ─────────────────────────────────────────────────────────────
    if isinstance(node, ForStmtNode):
        # inicialização
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

        # bloco
        code.extend(generate_code(node.body, symbol_table))

        # incremento/decremento
        code.append(f"PUSHG {offset}")
        code.append("PUSHI 1")
        code.append("ADD" if node.direction == 'to' else "SUB")
        code.append(f"STOREG {offset}")

        code.append(f"JUMP {start_lbl}")
        code.append(f"{end_lbl}:")
    # ────────────────────────────────────────────────────────────────────────────────
    
    elif node is None:
        pass
    
    return code



def generate_program_code(ast):
    # Construir a tabela de símbolos a partir da AST
    symbol_table = build_symbol_table(ast)
    code = []
    #1º Declaraqção das vars
    # Código para as declarações globais (variáveis) é gerado a partir de opt_variable
    var_code = generate_code(ast.opt_variable, symbol_table)
    code.extend(var_code)

    #2º BLOCO
    # Por o  START para iniciar a execução do bloco 
    code.append("START")
    block_code = generate_code(ast.block, symbol_table)
    code.extend(block_code)


    # Por o STOP para terminar o programa
    code.append("STOP")
    return code

# Função só para debug para ajudar a ver melhor
def pretty_symbol_table(table):
    print("Tabela de Símbolos:")
    # imprime em JSON, com indentação e caracteres UTF‑8
    print(json.dumps(table, indent=4, ensure_ascii=False))