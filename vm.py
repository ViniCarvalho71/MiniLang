import argparse
import sys
import json

def main():
    pilha = []
    bytecode = read_bytecode()

    memoria = [None] * len(bytecode["tipos_memoria"])

    for instruction in bytecode["instrucoes"]:
        op = instruction["op"]
        arg = instruction["arg"]
        if op == "PUSH_INT":
            if type(arg) is not int:
                print(f"Erro: Valor inteiro inválido '{arg}'")
                return 1
            pilha.append(arg)
        elif op == "PUSH_BOOL":
            if type(arg) is not bool:
                print(f"Erro: Valor booleano inválido '{arg}'")
                return 1
            pilha.append(arg)
        elif op == "ADD":
            if not validate_pilha(pilha, 2, "ADD"):
                return 1
            b = pilha.pop()
            a = pilha.pop()
            if not validate_int(a, b, "ADD"):
                return 1
            pilha.append(a + b)
        elif op == "SUB":
            if not validate_pilha(pilha, 2, "SUB"):
                return 1
            b = pilha.pop()
            a = pilha.pop()
            if not validate_int(a, b, "SUB"):
                return 1
            pilha.append(a - b)
        elif op == "MUL":
            if not validate_pilha(pilha, 2, "MUL"):
                return 1
            b = pilha.pop()
            a = pilha.pop()
            if not validate_int(a, b, "MUL"):
                return 1
            pilha.append(a * b)
        elif op == "DIV":
            if not validate_pilha(pilha, 2, "DIV"):
                return 1
            b = pilha.pop()
            a = pilha.pop()
            if not validate_int(a, b, "DIV"):
                return 1
            if b != 0:
                resultado = a // b
                if resultado < 0 and a % b != 0:
                    resultado += 1
                pilha.append(resultado)
            else:
                print("Erro: Divisão por zero")
                return 1
        elif op == "STORE":
            address = arg
            if type(address) is not int or address < 0 or address >= len(memoria):
                print("Erro: Endereço de memória inválido")
                return 1
            if not validate_pilha(pilha, 1, "STORE"):
                return 1
            value = pilha.pop()
            type_value = type(value).__name__
            expected_type = bytecode["tipos_memoria"][address]
            if type_value != expected_type:
                print(f"Erro: Esperado '{expected_type}', mas recebeu '{type_value}'")
                return 1
            memoria[address] = value
        elif op == "LOAD":
            address = arg
            if type(address) is not int or address < 0 or address >= len(memoria):
                print("Erro: Endereço de memória inválido")
                return 1
            value = memoria[address]
            if value is None:
                print(f"Erro: Tentativa de carregar valor de endereço não inicializado {address}")
                return 1
            if not validate_pilha(pilha, 1, "LOAD"):
                return 1
            pilha.append(value)
        elif op == "PRINT":
            if not validate_pilha(pilha, 1, "PRINT"):
                return 1
            print(pilha.pop())
        else:
            print(f"Erro: Instrução desconhecida '{op}'")
            return 1

        print(f"Pilha atual: {pilha}")
        print(f"Memória atual: {memoria}")


def read_bytecode():
    argumentos = argparse.ArgumentParser(description="VM do MiniLang")
    argumentos.add_argument("ByteCode", help="Caminho do arquivo .bc")
    args = argumentos.parse_args()

    try:
        with open(args.ByteCode, "r", encoding="utf-8") as bytecode_file:
            bytecode = json.load(bytecode_file)

            return bytecode
    except (OSError, UnicodeError) as erro:
        print(f"Erro ao ler arquivo: {erro.strerror}")
        return None

def validate_pilha(pilha, quantity, op):
    if len(pilha) < quantity:
        print(f"Erro: Pilha não possui elementos suficientes para a operação {op}")
        return False
    return True

def validate_int(a, b, op):
    if type(a) is not int or type(b) is not int:
        print(f"Erro: Operação {op} requer operandos inteiros, mas recebeu '{type(a).__name__}' e '{type(b).__name__}'")
        return False
    return True

if __name__ == "__main__":
    sys.exit(main())