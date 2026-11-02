"""Verifica os exemplos de entrega pelo ponto de entrada real."""

from pathlib import Path
import subprocess
import sys
import unittest


NOME_DA_LEVA = "Integracao do programa"
RAIZ = Path(__file__).resolve().parents[1]


class TesteMain(unittest.TestCase):
    def executar(self, *argumentos):
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", "main.py", *argumentos],
            cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", timeout=10,
        )

    def test_exemplo_valido_mostra_ast(self):
        resultado = self.executar("examples/ast.min")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stderr, "")
        self.assertIn("AST:\nPrograma\n", resultado.stdout)
        self.assertIn("Declaracao(x)", resultado.stdout)
        self.assertIn("Binaria(*)", resultado.stdout)

    def test_exemplo_invalido_mostra_diagnostico(self):
        resultado = self.executar("examples/erro_sintatico.min")
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("Erro sintático:", resultado.stderr)
        self.assertIn("RPAREN na linha 2, coluna 11", resultado.stderr)
        self.assertNotIn("AST:", resultado.stdout)

    def test_exemplo_original_no_modo_lexer(self):
        resultado = self.executar("examples/programa.min", "--somente-lexer")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Tokens:", resultado.stdout)
        self.assertNotIn("AST:", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
