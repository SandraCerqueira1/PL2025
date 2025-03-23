# calc_yacc.py
from calc_lex import lexer  

class ParserLL1:
    def __init__(self, expression):
        self.tokens = []
        lexer.input(expression)  # Passa a expressão para o lexer
        self.current_token = lexer.token()  # Obtém o primeiro token

    def advance(self):
        # Avança para o próximo token
        self.current_token = lexer.token()

    def eat(self, expected):
        if self.current_token and self.current_token.type == expected:
            self.advance()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}, expected: {expected}")

    def factor(self):
        token = self.current_token
        if token is None:
            raise SyntaxError("Unexpected end of expression")
        
        if token.type == 'NUMBER':  
            value = token.value
            self.eat('NUMBER')
            return value
        elif token.type == 'AP':
            self.eat('AP')
            result = self.expr()
            self.eat('FP')
            return result
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token.type in ('MULT', 'DIV'):
            token = self.current_token
            if token.type == 'MULT':
                self.eat('MULT')
                result *= self.factor()
            elif token.type == 'DIV':
                self.eat('DIV')
                denominator = self.factor()
                if denominator == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= denominator
        return result

    def expr(self):
        result = self.term()
        while self.current_token and self.current_token.type in ('ADD', 'MINUS'):
            token = self.current_token
            if token.type == 'ADD':
                self.eat('ADD')
                result += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                result -= self.term()
        return result

    def parse(self):
        return self.expr()


if __name__ == '__main__':
    
    expressions = [
        "2+3",
        "67-(2+3*4)",
        "(9-2)*(13-4)"
    ]
    
    
    for data in expressions:
        parser = ParserLL1(data)
        try:
            result = parser.parse()
            print(f"Resultado de '{data}': {result}")
        except SyntaxError as e:
            print(f"Erro sintático em '{data}': {e}")
        except ZeroDivisionError as e:
            print(f"Erro de divisão por zero em '{data}': {e}")
