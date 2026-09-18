import sys

from minilang.lexer import Lexer


if len(sys.argv) != 2:
    print("Uso: python main.py <arquivo.min>")
    sys.exit(1)

caminho_arquivo = sys.argv[1]

with open(caminho_arquivo, "r", encoding="utf-8") as codigo_fonte:
    source = codigo_fonte.read()

lexer = Lexer(source, 0, 0, 1, 1, 1, 1, [])

tokens, diagnostics = lexer.scan_tokens()

print("Tokens:")
for token in tokens:
    print(token)

print("\nDiagnósticos:")
for diagnostic in diagnostics:
    print(diagnostic)