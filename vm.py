import argparse
import sys

def main():
    pilha = []
    instructions = read_bytecode()

    for instruction in instructions:
        op = instruction["op"]
        arg = instruction["arg"]

        if op == "PUSH_INT":
            pilha.append(int(arg))
        elif op == "ADD":
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(a + b)
        elif op == "SUB":
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(a - b)
        elif op == "MUL":
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(a * b)
        elif op == "DIV":
            b = pilha.pop()
            a = pilha.pop()
            if b != 0:
                pilha.append(a // b)
            else:
                print("Erro: Divisão por zero")
                return 1
        elif op == "PRINT":
            if pilha:
                print(pilha[-1])
            else:
                print("Erro: Pilha vazia")
                return 1
        else:
            print(f"Erro: Instrução desconhecida '{op}'")
            return 1


def read_bytecode():
    argumentos = argparse.ArgumentParser(description="VM do MiniLang")
    argumentos.add_argument("ByteCode", help="Caminho do arquivo .bc")
    args = argumentos.parse_args()
    instructions = []

    try:
        with open(args.ByteCode, "r", encoding="utf-8") as bytecode_file:
            bytecode = bytecode_file.read()
            bytecode = bytecode.strip().split("\n")

            for instruction in bytecode:
                instruction = instruction.strip().split(" ")
                instructions.append({"op": instruction[0], "arg": instruction[1] if len(instruction) > 1 else None})

            return instructions
    except (OSError, UnicodeError) as erro:
        print(f"Erro ao ler arquivo: {erro.strerror}")
        return None

if __name__ == "__main__":
    sys.exit(main())