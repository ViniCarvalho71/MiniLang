class AnaliseSemantica:

    def __init__(self):
        self.tabela = []
        self.escopo = 0
        self.erros = []

    def InsereTabela(self, simbolo, nome, tipo, origem):
        dic = {
            "simbolo": simbolo,
            "nome": nome,
            "tipo": tipo,
            "origem": origem
        }
        
        if(len(self.tabela) < self.escopo):
            lista = [dic]
            self.tabela.append(lista)
        elif self.VerificaDeclaracao(self, nome):
            self.tabela[self.escopo].append(dic)
        else:
            self.erros.append("ER_REDECLARACAO")


    def VerificaDeclaracao(self, nome):
        for l in self.tabela[self.escopo]:
            if(l.nome == nome):
                return False
        return True

    def VerificaAtribuicao(self, nome):
        for x in range()
        



        