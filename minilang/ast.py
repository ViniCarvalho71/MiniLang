class AST:

    def __init__(self, tokens, start, current):
        self.tokens = tokens
        self.start = start
        self.current = current

    # Expr → Termo PLUS Expr
    # | Termo MINUS Expr
    # | Termo

    # Termo → IDENT | INT_LITERAL
    def expressao(self):
        def expressao(self):
        aux = self.current
        if aux < len(self.tokens) and self.tokens[aux] in ("INT_LITERAL", "IDENT"):
            aux += 1
            if aux < len(self.tokens) and self.tokens[aux] in ("PLUS", "MINUS"):
                aux += 1
                old = self.current
                self.current = aux
                res = self.expressao()
                self.current = old  
                
                if res == 0:
                    return 0
                return (aux - self.current) + res
            return aux - self.current
        return 0

    def atribuicao(self) -> int:
        aux = self.current

        if self.token[aux] == 'IDENT':
            aux += 1
            if self.token[aux] == 'ASSIGN':
                aux += 1
                return aux
        return 0

    def declaracao(self) -> int:
        aux = self.current

        if self.token[aux] == 'KW_INT':
            aux += 1
            if self.token[aux] == 'IDENT':
                aux += 1
                if self.token[aux] == 'SEMICOLON':
                    aux += 1
                    return aux
        return 0