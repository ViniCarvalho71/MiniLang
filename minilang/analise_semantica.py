class Simbolo:
    def __init__(self, nome, tipo, origem):
        self.nome = nome
        self.tipo = tipo
        self.origem = origem

class Escopo:
    def __init__(self, nome, escopo_pai=None):
        self.nome = nome
        self.escopo_pai = escopo_pai
        self.simbolos = {}

    def adicionar_simbolo(self, simbolo):
        if simbolo.nome in self.simbolos:
            raise Exception(f"Símbolo '{simbolo.nome}' já declarado neste escopo.")
        self.simbolos[simbolo.nome] = simbolo

    def buscar_simbolo(self, nome):
        if nome in self.simbolos:
            return [self.nome, self.simbolos[nome].nome]
        elif self.escopo_pai is not None:
            return self.escopo_pai.buscar_simbolo(nome)
        else:
            return None

escopo_global = Escopo("global")
escopo_global.adicionar_simbolo(Simbolo("x", "int", "1:5"))

escopo_local1 = Escopo("local1", escopo_global)
escopo_local1.adicionar_simbolo(Simbolo("x", "int", "2:5"))

escopo_local2 = Escopo("local2", escopo_global)
escopo_local2.adicionar_simbolo(Simbolo("y", "int", "3:5"))

escopo_local3 = Escopo("local3", escopo_local1)
escopo_local3.adicionar_simbolo(Simbolo("z", "int", "4:5"))

print(escopo_local3.buscar_simbolo("x"))
print(escopo_local3.buscar_simbolo("y"))
print(escopo_local3.buscar_simbolo("z"))
