class Inteiro:
    def __init__(self, value):
        self.value = value

class Variavel:
    def __init__(self, value):
        self.value = value

class Binaria:
    def __init__(self, operator, right, left):
        self.operator = operator
        self.right = right
        self.left = left

class Atribuicao:
    def __init__(self, variable : Variavel, expr):
        self.variable = variable
        self.expr = expr

class Declaracao:
    def __init__(self, type, ident):
        self.type = type
        self.ident = ident

class Print:
    def __init__(self, command, expr):
        self.command = command
        self.expr = expr




class Parser:

    def __init__(self, tokens, start, current):
        self.tokens = tokens #cada token é (nome, valor, linha, coluna)
        self.start = start
        self.current = current

    # Expr → Termo PLUS Expr
    # | Termo MINUS Expr
    # | Termo
    # Termo → IDENT | INT_LITERAL
    def Expressao(self):
        esquerda = self.termo()  
        if esquerda is None:
            return None
            
        while self.current < len(self.tokens) and self.tokens[self.current][0] in ("PLUS", "MINUS"):
            op_token = self.tokens[self.current]
            operador = op_token[1]
            self.current += 1 
            
            direita = self.termo()  
            if direita is None:
                return None  
                
            esquerda = Binaria(operador, esquerda, direita)
            
        return esquerda

    def Termo(self):
        esquerda = self.Fator()
        if esquerda is None:
            return None
            
        while self.current < len(self.tokens) and self.tokens[self.current][0] in ("STAR", "SLASH"):
            op_token = self.tokens[self.current]
            operador = op_token[1] # ou o tipo do operador
            self.current += 1 # consome o STAR ou SLASH
            
            direita = self.Fator()
            if direita is None:         
                return None
   
            esquerda = Binaria(operador, esquerda, direita)
            
        return esquerda
    
    def Fator(self):
        if(self.current < len(self.tokens) and self.tokens[self.current][0] == "IDENT"):
            var_name = self.tokens[self.current][1]
            self.current += 1
            return Variavel(var_name)
        elif(self.current < len(self.tokens) and self.tokens[self.current][0] == "INT_LITERAL"):
            int_name = self.tokens[self.current][1]
            self.current += 1
            return Inteiro(int_name)

        if self.current < len(self.tokens) and self.tokens[self.current][0] == "LPAREN":
            self.current += 1 
            expr = self.Expressao()  
            
      
            if self.current < len(self.tokens) and self.tokens[self.current][0] == "RPAREN":
                self.current += 1  
                return expr  
            
            return None
        return None
    

    def Atribuicao(self) -> Atribuicao | None:
        if self.tokens[self.current][0] == 'IDENT':
            variavel = Variavel(self.tokens[self.current][1])
            self.current += 1
            if self.tokens[self.current][0] == 'ASSIGN':
                self.current += 1
                expresao = self.Expressao()
                if self.tokens[self.current][0] == 'SEMICOLON':
                    self.current += 1
                    return Atribuicao(variavel, expresao)
        return None

    def Declaracao(self) -> Declaracao | None:
        if self.tokens[self.current][0] == 'KW_INT':
            tipo = self.tokens[self.current][1]
            self.current += 1 
            if self.tokens[self.current][0] == 'IDENT':
                ident = self.tokens[self.current][1]
                self.current += 1 
                if self.tokens[self.current][0] == 'SEMICOLON':
                    self.current += 1 
                    return Declaracao(tipo, ident)
        return None