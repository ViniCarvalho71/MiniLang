class Lexer:

    # Palavras que começam como identificadores, mas possuem um token próprio.
    KEYWORDS = {
        "int": "KW_INT",
        "print": "KW_PRINT",
        "if": "KW_IF",
        "else": "KW_ELSE",
        "while": "KW_WHILE",
    }

    def __init__(self, source, start, current, line, column, start_line, start_column, diagnostics):
        # No Windows, CRLF deve contar como uma única quebra de linha.
        self.source = source.replace("\r\n", "\n")
        self.start = start
        self.current = current
        self.line = line
        self.column = column
        self.start_line = start_line
        self.start_column = start_column
        self.diagnostics = diagnostics
        self.tokens = []

    def scan_tokens(self):
        while not self.at_end():
            # Guarda a posição em que o próximo lexema começa.
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column

            self.scan_token()

        self.tokens.append(("EOF", "", self.line, self.column))
        return self.tokens, self.diagnostics

    def scan_token(self):
        # O comentário precisa ser verificado antes da barra de divisão.
        if self.peek() == "/" and self.peek_next() == "/":
            self.advance()
            self.advance()
            self.line_comment()
            return

        # Consome o primeiro caractere do próximo token.
        c = self.advance()

        if self.is_letter(c) or c == "_":
            self.identifier()

        elif self.is_digit(c):
            self.number()

        elif c == "=":
            if self.match("="):
                self.add_token("EQUAL_EQUAL")
            else:
                self.add_token("ASSIGN")

        elif c == "!":
            if self.match("="):
                self.add_token("BANG_EQUAL")
            else:
                self.report_invalid_character(c)

        elif c == "<":
            if self.match("="):
                self.add_token("LESS_EQUAL")
            else:
                self.add_token("LESS")

        elif c == ">":
            if self.match("="):
                self.add_token("GREATER_EQUAL")
            else:
                self.add_token("GREATER")

        elif c == "+":
            self.add_token("PLUS")

        elif c == "-":
            self.add_token("MINUS")

        elif c == "*":
            self.add_token("STAR")

        elif c == "/":
            self.add_token("SLASH")

        elif c == "(":
            self.add_token("LPAREN")

        elif c == ")":
            self.add_token("RPAREN")

        elif c == "{":
            self.add_token("LBRACE")

        elif c == "}":
            self.add_token("RBRACE")

        elif c == ";":
            self.add_token("SEMICOLON")

        elif self.is_whitespace(c):
            # Espaços são consumidos, mas não produzem tokens.
            while self.is_whitespace(self.peek()):
                self.advance()

        else:
            self.report_invalid_character(c)

    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        if self.at_end():
            return "\0"

        # Toda atualização de linha e coluna fica centralizada neste método.
        c = self.source[self.current]
        self.current += 1

        if c == "\n" or c == "\r":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return c

    def peek(self):
        if self.at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected):
        if self.peek() == expected:
            self.advance()
            return True
        return False

    def add_token(self, type_):
        # O lexema contém tudo que foi consumido desde start.
        lexeme = self.source[self.start:self.current]
        self.tokens.append((type_, lexeme, self.start_line, self.start_column))

    def identifier(self):
        # Consome o identificador inteiro antes de consultar as palavras reservadas.
        while (
            self.is_letter(self.peek())
            or self.is_digit(self.peek())
            or self.peek() == "_"
        ):
            self.advance()

        lexeme = self.source[self.start:self.current]
        token_type = self.KEYWORDS.get(lexeme, "IDENT")
        self.add_token(token_type)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        self.add_token("INT_LITERAL")

    def is_digit(self, c):
        return "0" <= c <= "9"

    def is_letter(self, c):
        return ("a" <= c <= "z") or ("A" <= c <= "Z")

    def is_whitespace(self, c):
        return c == " " or c == "\t" or c == "\r" or c == "\n"

    def line_comment(self):
        # A quebra de linha será consumida como espaço na próxima iteração.
        while not self.at_end() and self.peek() != "\r" and self.peek() != "\n":
            self.advance()

    def report_invalid_character(self, c):
        # O caractere inválido já foi consumido, então a análise pode continuar.
        message = f"Caractere inválido: {c!r}."
        self.diagnostics.append(
            (c, self.start_line, self.start_column, message)
        )
