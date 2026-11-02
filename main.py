import argparse
import sys

from minilang.ast import Parser
from minilang.lexer import Lexer
from minilang.visualizador import formatar_ast


def main():
    argumentos = argparse.ArgumentParser(description="Analisador da MiniLang")
    argumentos.add_argument("arquivo", help="Caminho do arquivo .min")
    argumentos.add_argument(
        "--somente-lexer", action="store_true", help="Executa apenas a análise léxica"
    )
    args = argumentos.parse_args()

    try:
        with open(args.arquivo, "r", encoding="utf-8") as codigo_fonte:
            source = codigo_fonte.read()
    except (OSError, UnicodeError) as erro:
        print(f"Erro ao ler arquivo: {erro}", file=sys.stderr)
        return 1

    tokens, diagnostics = Lexer(source, 0, 0, 1, 1, 1, 1, []).scan_tokens()

    print("Tokens:")
    for token in tokens:
        print(token)

    print("\nDiagnósticos:")
    for diagnostic in diagnostics:
        print(diagnostic)

    if diagnostics:
        return 1
    if args.somente_lexer:
        return 0

    try:
        arvore = Parser(tokens, 0, 0).Programa()
    except SyntaxError as erro:
        print(f"Erro sintático: {erro}", file=sys.stderr)
        return 1

    print("\nAST:")
    print(formatar_ast(arvore))
    return 0


if __name__ == "__main__":
    sys.exit(main())
