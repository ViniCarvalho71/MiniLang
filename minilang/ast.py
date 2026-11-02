from __future__ import annotations


class Inteiro:
    def __init__(self, value):
        self.value = value

class Variavel:
    def __init__(self, value):
        self.value = value

class Binaria:
    def __init__(self, operator, left, right):
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

class Programa:
    def __init__(self, itens):
        self.itens = itens



class Parser:

    def __init__(self, tokens, start, current):
        self.tokens = tokens #cada token é (nome, valor, linha, coluna)
        # self.tokens = ["KW_PRINT", "LPAREN", "IDENT", "RPAREN", "SEMICOLON", ""]
        self.start = start
        self.current = current


    def Esperado(self, esperado):
        token = self.tokens[self.current]

        if token[0] == esperado:
            self.current += 1
            return token
        raise SyntaxError(
            f"Esperado {esperado}, encontrado {token[0]} "
            f"na linha {token[2]}, coluna {token[3]}"
        
        )
    # Expr → Termo PLUS Expr
    # | Termo MINUS Expr
    # | Termo
    # Termo → IDENT | INT_LITERAL
    def Expressao(self):
        esquerda = self.Termo()  
        if esquerda is None:
            return None
            
        while self.current < len(self.tokens) and self.tokens[self.current][0] in ("PLUS", "MINUS"):
            op_token = self.tokens[self.current]
            operador = op_token[1]
            self.current += 1 
            
            direita = self.Termo()  
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


    def Atribuicao(self) -> Atribuicao:
        ident = self.Esperado("IDENT")
        variavel = Variavel(ident[1])

        self.Esperado("ASSIGN")

        expressao = self.Expressao()
        if expressao is None:
            token = self.tokens[self.current]
            raise SyntaxError(
                f"Esperada uma expressão, encontrado {token[0]} "
                f"na linha {token[2]}, coluna {token[3]}"
            )

        self.Esperado("SEMICOLON")

        return Atribuicao(variavel, expressao)

    def Declaracao(self) -> Declaracao:
        tipo = self.Esperado("KW_INT")
        ident = self.Esperado("IDENT")
        self.Esperado("SEMICOLON")
        return Declaracao(tipo[1], ident[1])

    def Saida(self) -> Print:
        token = self.Esperado("KW_PRINT")
        self.Esperado("LPAREN")
        expr = self.Expressao()
        if expr is None:
            atual = self.tokens[self.current]
            raise SyntaxError(
                f"Esperada uma expressão, encontrado {atual[0]} "
                f"na linha {atual[2]}, coluna {atual[3]}"
            )

        self.Esperado("RPAREN")
        self.Esperado("SEMICOLON")
        return Print(token[1], expr)



    def Item(self) -> Declaracao | Atribuicao | Print:
        token = self.tokens[self.current]
        tipo = token[0]
        if tipo == "KW_INT":
            return self.Declaracao()
        elif tipo == "IDENT":
            return self.Atribuicao()
        elif tipo == "KW_PRINT":
            return self.Saida()
        raise SyntaxError(
            f"Comando inesperado: {token[0]} "
            f"na linha {token[2]}, coluna {token[3]}"
        )

    def ListaItens(self) -> list[Declaracao | Atribuicao | Print]:
        itens = []
        while self.tokens[self.current][0] != "EOF":
            itens.append(self.Item())

        return itens
    
    def Programa(self) -> Programa:
        itens = self.ListaItens()
        self.Esperado("EOF")

        return Programa(itens)
