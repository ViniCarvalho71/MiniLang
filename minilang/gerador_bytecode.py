from minilang import ast

class GeradorBytecode:
    def __init__(self, t1 : list, t2:list, so:list):
        self.bytecode : list = []
        self.pcs = []
        self.stack : list = []
        self.pc = 0
        self.t1 : list = t1
        self.t2 : list = t2
        self.so : list = so

    
    def processa_ri(self, op):
        for x in op:
            
            if(isinstance(x, ast.Binaria)):
                if(x.left == "t1" or x.left == "t2"):
                    self.bytecode.append("LOAD " + self.stack[-1])
                else:
                    self.bytecode.append("PUSH " + x.left)

                self.pcs.append(self.pc)
                self.pc += 1
                

                if(x.right == "t2" or x.right == "t2"):
                    self.bytecode.append("LOAD " + self.stack[-1])
                else:
                    self.bytecode.append("PUSH " + x.right)

                self.pcs.append(self.pc)
                self.pc += 1

                match x.operador:
                    case "PLUS":
                        self.bytecode.append("ADD")
                    case "MINUS":
                        self.bytecode.append("SUB")
                    case "STAR":
                        self.bytecode.append("MUL")
                    case "SLASH":
                        self.bytecode.append("DIV")
                    case _:
                        self.pcs.append(self.pc)
                        self.pc += 1

                self.bytecode.append("STORE " + self.stack[-1])

                self.pcs.append(self.pc)
                self.pc += 1
                if(self.stack[-1] == 2):
                    self.stack = []
                self.stack(self.stack[-1] + 1)
                
            if(isinstance(x, ast.Declaracao)):
                self.bytecode.append("PUSH_INT " + x.value)
                self.pcs.append(self.pc)
                self.pc += 1
                if(self.stack[-1] == 2):
                    self.stack = []
                self.bytecode.append("STORE " + self.stack[-1])
                self.pcs.append(self.pc)
                self.pc += 1
            if(isinstance(x, ast.Atribuicao)):
                self.bytecode.append("LOAD " + self.stack[-1])
                if(self.stack[-1] == 2):
                    self.stack = []
                self.bytecode.append("STORE " + self.stack[-1])
            

        

    
    


