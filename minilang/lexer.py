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
        pass

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
        pass

    def line_comment(self):
        pass

    def report_invalid_character(self, c):
        pass