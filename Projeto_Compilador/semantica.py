from ast_nodes import *

def check_semantics(ast, symbol_table):
    errors = []

    def visit(node):
        if node is None:
            return

        elif isinstance(node, ProgramaNode):
            visit(node.opt_variable)
            visit(node.block)

        elif isinstance(node, Opt_variableNode):
            visit(node.child)

        elif isinstance(node, VariablesNode):
            for decl in node.vars_node:
                visit(decl)

        elif isinstance(node, BlockNode):
            visit(node.stmt_list)

        elif isinstance(node, StmtListNode):
            for stmt in node.statements:
                visit(stmt)

        elif isinstance(node, AssignNode):
            check_variable(node.variable)
            visit(node.expression)

            # Verificação de tipos
            var_type = infer_type(node.variable)
            expr_type = infer_type(node.expression)

            if var_type == "unknown" or expr_type == "unknown":
                var_name = node.variable.id
                errors.append(f"Erro: Tipo desconhecido na atribuição para variável '{var_name}'.")
            elif var_type != expr_type:
                if not (var_type == "real" and expr_type == "integer"):
                    var_name = node.variable.id
                    errors.append(f"Erro: Atribuição incompatível. Variável '{var_name}' é do tipo '{var_type}' mas expressão é do tipo '{expr_type}'.")


        elif isinstance(node, VariableNode):
            check_variable(node)

        elif isinstance(node, IfStmtNode):
            visit(node.condition)
            visit(node.then_stmt)
            if node.else_stmt:
                visit(node.else_stmt)

        elif isinstance(node, WhileStmtNode):
            visit(node.condition)
            visit(node.body)

        elif isinstance(node, ForStmtNode):
            check_variable(node.init_assign.variable)
            visit(node.init_assign.expression)
            visit(node.bound_expr)
            visit(node.body)

        elif isinstance(node, ReadLnStmtNode):
            check_variable(node.var_node)

        elif isinstance(node, WriteStmtNode) or isinstance(node, WriteLnStmtNode):
            if node.output_args:
                for item in node.output_args.items:
                    if isinstance(item.value, VariableNode):
                        check_variable(item.value)
        
        elif isinstance(node, RelOpNode):
            visit(node.left)
            visit(node.right)

            left_type = infer_type(node.left)
            right_type = infer_type(node.right)

            # Só permite comparação entre tipos iguais
            if left_type != right_type:
                errors.append(f"Erro: Comparação entre tipos incompatíveis: '{left_type}' e '{right_type}'.")

        elif isinstance(node, BinOpNode):
            visit(node.left)
            visit(node.right)

        elif isinstance(node, NotNode):
            visit(node.expr)

        elif isinstance(node, LengthNode):
            visit(node.expr)

        # Literais
        elif isinstance(node, (NumberNode, RealNode, StringNode, BoolNode)):
            pass  # sempre válidos

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
                # Se for acesso a array (ou string), retorna o tipo dos elementos
                if node.index is not None:
                    if var_info["type"] == "structured":
                        return var_info["elem_type"]
                    elif var_info["type"] == "string":
                        return "string"  # Strings indexadas retornam caracteres
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

    visit(ast)
    return errors
