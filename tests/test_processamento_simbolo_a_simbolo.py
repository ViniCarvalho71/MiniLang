"""Testes do processamento da entrada símbolo a símbolo."""

import sys
import unittest

from minilang.lexer import Lexer


NOME_DA_LEVA = "Processamento símbolo a símbolo" # Só para ser reconhecido no teste que roda todos os testes


class TesteProcessamentoSimboloASimbolo(unittest.TestCase):
    def analisar(self, source):
        lexer = Lexer(source, 0, 0, 1, 1, 1, 1, [])
        tokens, diagnostics = lexer.scan_tokens()

        # Exibe o resultado para facilitar a conferência manual dos testes.
        print(f"\n  Entrada: {source!r}", file=sys.stderr)
        print("  Tokens:", file=sys.stderr)
        for tipo, lexema, linha, coluna in tokens:
            print(
                f"    - {tipo:<15} lexema={lexema!r:<10} posição={linha}:{coluna}",
                file=sys.stderr,
            )

        if diagnostics:
            print("  Diagnósticos:", file=sys.stderr)
            for simbolo, linha, coluna, mensagem in diagnostics:
                print(
                    f"    - símbolo={simbolo!r} posição={linha}:{coluna} "
                    f"mensagem={mensagem}",
                    file=sys.stderr,
                )
        else:
            print("  Diagnósticos: nenhum", file=sys.stderr)

        return tokens, diagnostics

    def test_fonte_vazia_produz_apenas_eof(self):
        tokens, diagnostics = self.analisar("")

        self.assertEqual(tokens, [("EOF", "", 1, 1)])
        self.assertEqual(diagnostics, [])

    def test_palavras_reservadas_e_identificadores_completos(self):
        tokens, diagnostics = self.analisar("int intx ifx while1 while")

        self.assertEqual(
            tokens,
            [
                ("KW_INT", "int", 1, 1),
                ("IDENT", "intx", 1, 5),
                ("IDENT", "ifx", 1, 10),
                ("IDENT", "while1", 1, 14),
                ("KW_WHILE", "while", 1, 21),
                ("EOF", "", 1, 26),
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_literais_inteiros_e_sinais_separados(self):
        tokens, diagnostics = self.analisar("007 -10 +7")

        self.assertEqual(
            tokens,
            [
                ("INT_LITERAL", "007", 1, 1),
                ("MINUS", "-", 1, 5),
                ("INT_LITERAL", "10", 1, 6),
                ("PLUS", "+", 1, 9),
                ("INT_LITERAL", "7", 1, 10),
                ("EOF", "", 1, 11),
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_maior_casamento_dos_operadores(self):
        tokens, diagnostics = self.analisar("= == === != < <= > >=")

        self.assertEqual(
            [token[0] for token in tokens],
            [
                "ASSIGN",
                "EQUAL_EQUAL",
                "EQUAL_EQUAL",
                "ASSIGN",
                "BANG_EQUAL",
                "LESS",
                "LESS_EQUAL",
                "GREATER",
                "GREATER_EQUAL",
                "EOF",
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_operadores_aritmeticos_e_delimitadores(self):
        tokens, diagnostics = self.analisar("a/b+-*(){ };")

        self.assertEqual(
            [token[0] for token in tokens],
            [
                "IDENT",
                "SLASH",
                "IDENT",
                "PLUS",
                "MINUS",
                "STAR",
                "LPAREN",
                "RPAREN",
                "LBRACE",
                "RBRACE",
                "SEMICOLON",
                "EOF",
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_comentarios_de_linha_sao_descartados(self):
        tokens, diagnostics = self.analisar("a// comment\n while")

        self.assertEqual(
            tokens,
            [
                ("IDENT", "a", 1, 1),
                ("KW_WHILE", "while", 2, 2),
                ("EOF", "", 2, 7),
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_comentario_no_final_da_fonte(self):
        tokens, diagnostics = self.analisar("///x")

        self.assertEqual(tokens, [("EOF", "", 1, 5)])
        self.assertEqual(diagnostics, [])

    def test_caracteres_invalidos_geram_diagnosticos_e_analise_continua(self):
        tokens, diagnostics = self.analisar("! @ !=")

        self.assertEqual(
            tokens,
            [
                ("BANG_EQUAL", "!=", 1, 5),
                ("EOF", "", 1, 7),
            ],
        )
        self.assertEqual(
            [diagnostic[:3] for diagnostic in diagnostics],
            [("!", 1, 1), ("@", 1, 3)],
        )
        self.assertTrue(all(diagnostic[3] for diagnostic in diagnostics))

    def test_alfabeto_dos_identificadores_aceita_apenas_ascii(self):
        tokens, diagnostics = self.analisar("vãlor")

        self.assertEqual(
            tokens,
            [
                ("IDENT", "v", 1, 1),
                ("IDENT", "lor", 1, 3),
                ("EOF", "", 1, 6),
            ],
        )
        self.assertEqual(diagnostics[0][:3], ("ã", 1, 2))

    def test_posicoes_dos_tokens_e_largura_do_tab(self):
        tokens, diagnostics = self.analisar("\tprint\n  x")

        self.assertEqual(
            tokens,
            [
                ("KW_PRINT", "print", 1, 2),
                ("IDENT", "x", 2, 3),
                ("EOF", "", 2, 4),
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_crlf_conta_como_uma_quebra_de_linha(self):
        tokens, diagnostics = self.analisar("int\r\n  print")

        self.assertEqual(
            tokens,
            [
                ("KW_INT", "int", 1, 1),
                ("KW_PRINT", "print", 2, 3),
                ("EOF", "", 2, 8),
            ],
        )
        self.assertEqual(diagnostics, [])

    def test_exemplo_completo_do_enunciado(self):
        tokens, diagnostics = self.analisar("if(total2>=10){print(total2);}")

        self.assertEqual(
            [token[0] for token in tokens],
            [
                "KW_IF",
                "LPAREN",
                "IDENT",
                "GREATER_EQUAL",
                "INT_LITERAL",
                "RPAREN",
                "LBRACE",
                "KW_PRINT",
                "LPAREN",
                "IDENT",
                "RPAREN",
                "SEMICOLON",
                "RBRACE",
                "EOF",
            ],
        )
        self.assertEqual(diagnostics, [])


if __name__ == "__main__":
    unittest.main()
