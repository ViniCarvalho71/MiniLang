"""Testes do parser: AST, consumo da entrada e diagnosticos sintaticos."""

import unittest

from minilang.ast import (
    Atribuicao, Binaria, Declaracao, Inteiro, Parser, Print, Programa, Variavel,
)
from minilang.lexer import Lexer
from minilang.visualizador import formatar_ast


NOME_DA_LEVA = "Analisador sintatico"


class TesteParser(unittest.TestCase):
    def criar_parser(self, fonte):
        tokens, diagnosticos = Lexer(fonte, 0, 0, 1, 1, 1, 1, []).scan_tokens()
        self.assertEqual(diagnosticos, [])
        return Parser(tokens, 0, 0)

    def analisar(self, fonte):
        parser = self.criar_parser(fonte)
        arvore = parser.Programa()
        self.assertIsInstance(arvore, Programa)
        self.assertEqual(parser.current, len(parser.tokens), "Deve consumir inclusive EOF")
        return arvore

    def estrutura(self, no):
        """Compara a AST inteira, sem calcular o resultado das expressoes."""
        if isinstance(no, Binaria):
            return (no.operator, self.estrutura(no.left), self.estrutura(no.right))
        if isinstance(no, Inteiro):
            return ("inteiro", str(no.value))
        if isinstance(no, Variavel):
            return ("variavel", no.value)
        self.fail(f"No inesperado: {type(no).__name__}")

    def test_declaracao(self):
        no = self.analisar("int total;").itens[0]
        self.assertIsInstance(no, Declaracao)
        self.assertEqual((no.type, no.ident), ("int", "total"))

    def test_atribuicao(self):
        no = self.analisar("total = 42;").itens[0]
        self.assertIsInstance(no, Atribuicao)
        self.assertIsInstance(no.variable, Variavel)
        self.assertEqual(no.variable.value, "total")
        self.assertEqual(self.estrutura(no.expr), ("inteiro", "42"))

    def test_print_sem_exigir_declaracao(self):
        no = self.analisar("print(y);").itens[0]
        self.assertIsInstance(no, Print)
        self.assertEqual(no.command, "print")
        self.assertEqual(self.estrutura(no.expr), ("variavel", "y"))

    def test_sequencia_preserva_ordem(self):
        itens = self.analisar("int x; x = 2; print(x); int y;").itens
        self.assertEqual([type(no) for no in itens], [Declaracao, Atribuicao, Print, Declaracao])
        self.assertEqual(itens[0].ident, "x")
        self.assertEqual(itens[3].ident, "y")

    def test_entrada_vazia_e_comentarios(self):
        for fonte in ("", " \t\n", "// somente comentario\n"):
            with self.subTest(fonte=fonte):
                self.assertEqual(self.analisar(fonte).itens, [])

    def test_precedencia_associatividade_e_parenteses(self):
        i = lambda valor: ("inteiro", str(valor))
        casos = [
            ("2 + 3 * 4", ("+", i(2), ("*", i(3), i(4)))),
            ("2 * 3 + 4", ("+", ("*", i(2), i(3)), i(4))),
            ("8 - 6 / 2", ("-", i(8), ("/", i(6), i(2)))),
            ("(2 + 3) * 4", ("*", ("+", i(2), i(3)), i(4))),
            ("10 - 3 - 2", ("-", ("-", i(10), i(3)), i(2))),
            ("8 / 2 / 2", ("/", ("/", i(8), i(2)), i(2))),
            ("10 - 3 + 2", ("+", ("-", i(10), i(3)), i(2))),
            ("8 / 2 * 3", ("*", ("/", i(8), i(2)), i(3))),
            ("10 - (3 - 2)", ("-", i(10), ("-", i(3), i(2)))),
            ("((2))", i(2)),
            ("1 / 0", ("/", i(1), i(0))),
        ]
        for expressao, esperado in casos:
            with self.subTest(expressao=expressao):
                no = self.analisar(f"print({expressao});").itens[0]
                self.assertEqual(self.estrutura(no.expr), esperado)

    def test_erros_informam_token_e_posicao(self):
        casos = [
            ("print(2 + );", "RPAREN", 1, 11),
            ("x = ;", "SEMICOLON", 1, 5),
            ("int ;", "SEMICOLON", 1, 5),
            ("int x", "EOF", 1, 6),
            ("x 2;", "INT_LITERAL", 1, 3),
            ("print 2;", "INT_LITERAL", 1, 7),
            ("print(2;", "SEMICOLON", 1, 8),
            ("print((2 + 3);", "SEMICOLON", 1, 14),
            ("print();", "RPAREN", 1, 7),
            ("print(2 * );", "RPAREN", 1, 11),
            ("print(2", "EOF", 1, 8),
            ("print(1); 2", "INT_LITERAL", 1, 11),
            ("int x;\nprint(2 + );", "RPAREN", 2, 11),
        ]
        for fonte, token, linha, coluna in casos:
            with self.subTest(fonte=fonte):
                with self.assertRaises(SyntaxError) as erro:
                    self.criar_parser(fonte).Programa()
                self.assertIn(token, str(erro.exception))
                self.assertIn(f"linha {linha}, coluna {coluna}", str(erro.exception))

    def test_para_no_primeiro_erro(self):
        parser = self.criar_parser("int ; print(2 + );")
        with self.assertRaisesRegex(SyntaxError, "Esperado IDENT, encontrado SEMICOLON"):
            parser.Programa()
        self.assertEqual(parser.current, 1)

    def test_rejeita_construcoes_fora_do_escopo(self):
        for fonte in ("if(x) print(x);", "while(x) print(x);", "else", "{int x;}",
                      "print(1 < 2);", "print(-1);", "print(+1);", "int x = 1;"):
            with self.subTest(fonte=fonte):
                with self.assertRaises(SyntaxError):
                    self.criar_parser(fonte).Programa()

    def test_visualizacao_da_ast_completa(self):
        arvore = self.analisar("int x; x = 2 + 3 * 4; print(x);")
        self.assertEqual(formatar_ast(arvore), "\n".join([
            "Programa", "├── Declaracao(x)", "├── Atribuicao(x)",
            "│   └── Binaria(+)", "│       ├── Inteiro(2)",
            "│       └── Binaria(*)", "│           ├── Inteiro(3)",
            "│           └── Inteiro(4)", "└── Saida", "    └── Variavel(x)",
        ]))


if __name__ == "__main__":
    unittest.main()
