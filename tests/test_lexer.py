"""Configuração geral para descobrir e exibir todos os grupos de testes."""

import sys
import unittest


class ResultadoOrganizadoPorLevas(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modulo_atual = None

    def startTest(self, test):
        modulo_do_teste = test.__class__.__module__

        if modulo_do_teste != self.modulo_atual:
            modulo = sys.modules.get(modulo_do_teste)
            nome_da_leva = getattr(modulo, "NOME_DA_LEVA", modulo_do_teste)

            self.stream.writeln("=" * 70)
            self.stream.writeln(f"INÍCIO DA LEVA: {nome_da_leva}")
            self.stream.writeln("=" * 70)
            self.modulo_atual = modulo_do_teste

        super().startTest(test)

    def stopTest(self, test):
        super().stopTest(test)
        self.stream.writeln()


# O comando de descoberta usa este resultado para organizar todos os arquivos.
unittest.TextTestRunner.resultclass = ResultadoOrganizadoPorLevas
