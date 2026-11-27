from minilang import ast


class GeradorBytecode:
    def __init__(self):
        self.bytecode = []
        self.mapa_origem = {}
        self.pc = 0
        self.enderecos = {}
        self.tipos_memoria = []
        self.rotulos = {}
        self.saltos = {}
        self.rotulo_duplicado = False

    # Usar essa função aqui -> Vinícius Andrade
    # Ela deve ser chamada a cada instrução que vc montar no RI, ou seja
    # Fez o s1, chama ela
    # Fez o s2, chama ela
    # Fez o s0, chama ela
    # Até terminar
    def processa_ri(self, op, destino=None, condicao=None, linha=None, coluna=None):
        if op == "ROTULO":
            if not isinstance(destino, str) or not destino.strip():
                return
            if destino in self.rotulos:
                self.rotulo_duplicado = True
            else:
                self.rotulos[destino] = self.pc
            return
        elif op == "GOTO" or op == "IF_FALSE":
            if not isinstance(destino, str) or not destino.strip():
                return
            opcode = "JMP"
            instrucoes = []
            if op == "IF_FALSE":
                instrucao = self.carrega_operando(condicao)
                if instrucao is None:
                    return
                instrucoes.append(instrucao)
                opcode = "JMP_FALSE"
            self.saltos[self.pc + len(instrucoes)] = (opcode, destino)
            instrucoes.append(f"{opcode} {destino}")
            self.emite_bytecode(instrucoes, linha, coluna)
            return
        elif op == "HALT":
            if not self.verifica_saltos():
                return
            for indice, (salto, rotulo) in self.saltos.items():
                self.bytecode[indice] = f"{salto} {self.rotulos[rotulo]}"
            self.emite_bytecode(["HALT"], linha, coluna)
            return

        if isinstance(op, ast.Binaria): #Verifica operaçoes
            if destino is None:
                return
            match op.operator:
                case "PLUS":
                    opcode = "ADD"
                case "MINUS":
                    opcode = "SUB"
                case "STAR":
                    opcode = "MUL"
                case "SLASH":
                    opcode = "DIV"
                case "LESS":
                    opcode = "LT"
                case "LESS_EQUAL":
                    opcode = "LE"
                case "GREATER":
                    opcode = "GT"
                case "GREATER_EQUAL":
                    opcode = "GE"
                case "EQUAL_EQUAL":
                    opcode = "EQ"
                case "BANG_EQUAL":
                    opcode = "NE"
                case "AND":
                    opcode = "AND"
                case "OR":
                    opcode = "OR"
                case _:
                    return
            instrucoes = [
                self.carrega_operando(op.left),
                self.carrega_operando(op.right),
                opcode,
            ]
        elif isinstance(op, ast.Declaracao): #Verifica declaração
            destino = op.ident
            valor = {"int": 0, "bool": False}.get(op.type)
            instrucoes = [self.carrega_operando(valor)]
        elif isinstance(op, ast.Atribuicao): #Verifica atribuição
            destino = op.variable
            instrucoes = [self.carrega_operando(op.expr)]
        elif isinstance(op, ast.Print): #print
            temp = self.carrega_operando(op.expr)
            if temp is None:
                return
            self.emite_bytecode([temp, "PRINT"], linha, coluna)
            return
        else:
            return

        nome = self.nome_referencia(destino)
        if nome is None or None in instrucoes:
            return
        if nome not in self.enderecos:
            if isinstance(op, ast.Binaria):
                tipo = "int" if opcode in ("ADD", "SUB", "MUL", "DIV") else "bool"
            else:
                carga, argumento = instrucoes[0].split()
                if carga == "LOAD":
                    tipo = self.tipos_memoria[int(argumento)]
                else:
                    tipo = "bool" if carga == "PUSH_BOOL" else "int"
            self.enderecos[nome] = len(self.tipos_memoria)
            self.tipos_memoria.append(tipo)
        endereco = self.enderecos[nome]
        instrucoes.append(f"STORE {endereco}")
        self.emite_bytecode(instrucoes, linha, coluna)

    def emite_bytecode(self, instrucoes, linha, coluna):
        for instrucao in instrucoes:
            if linha is not None and coluna is not None:
                self.mapa_origem[str(self.pc)] = {"linha": linha, "coluna": coluna}
            self.bytecode.append(instrucao)
            self.pc += 1

    def carrega_operando(self, operando):
        if isinstance(operando, (ast.Inteiro, ast.Booleano)):
            operando = operando.value
        if isinstance(operando, bool):
            return f"PUSH_BOOL {str(operando).lower()}"
        if isinstance(operando, int):
            return f"PUSH_INT {operando}"

        nome = self.nome_referencia(operando)
        if nome in self.enderecos:
            return f"LOAD {self.enderecos[nome]}"

    def nome_referencia(self, referencia):
        if isinstance(referencia, ast.Variavel):
            referencia = referencia.value
        if isinstance(referencia, str):
            return referencia

    # Usar essa função aqui -> Maurício
    def monta_artefato(self, mapa_origem=None): # Essa função vai ser chamada pela VM para pegar o artefado no padrão do slide
        if not self.verifica_saltos():
            return None
        bytecode = self.bytecode.copy()
        if not bytecode or bytecode[-1] != "HALT":
            bytecode.append("HALT")

        for indice, (salto, rotulo) in self.saltos.items():
            bytecode[indice] = f"{salto} {self.rotulos[rotulo]}"

        instrucoes = []
        for instrucao in bytecode:
            opcode, _, argumento = instrucao.partition(" ")
            arg = None
            if opcode == "PUSH_BOOL":
                arg = argumento == "true"
            elif argumento:
                arg = int(argumento)
            instrucoes.append({"op": opcode, "arg": arg})

        mapa_final = self.mapa_origem.copy()
        if mapa_origem is not None:
            for indice, posicao in mapa_origem.items():
                mapa_final[str(indice)] = posicao

        return {
            "versao": 1,
            "instrucoes": instrucoes,
            "tipos_memoria": self.tipos_memoria.copy(),
            "mapa_origem": mapa_final,
        }

    def verifica_saltos(self): 
        if self.rotulo_duplicado:
            return False
        for _, rotulo in self.saltos.values():
            if rotulo not in self.rotulos:
                return False
        return True
