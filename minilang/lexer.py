class Lexer:
    
    def __init__(self, source, start, current, line, column, start_line, start_column, diagnostics):
        self.source = source
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
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column

            self.scan_token()

        self.tokens.append(("EOF", "", self.line, self.column))
        return self.tokens, self.diagnostics

    def scan_token(self):
        c = self.advance()

        if self.is_digit(c):
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

    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        if self.at_end():
            return '\0'
        
        c = self.source[self.current]
        self.current += 1
        
        if c == '\n' or c == '\r':
            self.line += 1
            self.column = 1
        else:
            self.column += 1  

        return c


    def peek(self):
        if self.at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.at_end():
            return '\0'
        
        return self.source[self.current + 1]

    def match(self, expected):
        if self.peek() == expected:
            self.advance()
            return True
        return False
        
    def add_token(self, type_):
        lexeme = self.source[self.start:self.current]
        self.tokens.append((type_, lexeme, self.start_line, self.start_column))

    def identifier(self):
        pass

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        self.add_token("INT_LITERAL")

    def is_digit(self, c):
        return '0' <= c <= '9'

    def line_comment(self):
        pass

    def report_invalid_character(self, c):
        pass