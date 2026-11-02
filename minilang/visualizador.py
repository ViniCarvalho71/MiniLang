from minilang.ast import (
    Programa, Declaracao, Atribuicao, Print, Binaria, Inteiro, Variavel,
)


def descrever(no):
    """Retorna o rotulo e os filhos de um no da AST, sem executa-lo."""
    if isinstance(no, Programa):
        return "Programa", no.itens
    if isinstance(no, Declaracao):
        return f"Declaracao({no.ident})", []
    if isinstance(no, Atribuicao):
        return f"Atribuicao({no.variable.value})", [no.expr]
    if isinstance(no, Print):
        return "Saida", [no.expr]
    if isinstance(no, Binaria):
        return f"Binaria({no.operator})", [no.left, no.right]
    if isinstance(no, Inteiro):
        return f"Inteiro({no.value})", []
    if isinstance(no, Variavel):
        return f"Variavel({no.value})", []
    raise TypeError(f"No de AST desconhecido: {type(no).__name__}")


def formatar_ast(raiz):
    """Formata a arvore com os operandos esquerdo e direito nessa ordem."""
    linhas = []

    def visitar(no, prefixo="", ultimo=True, raiz=False):
        rotulo, filhos = descrever(no)
        conector = "" if raiz else ("└── " if ultimo else "├── ")
        linhas.append(prefixo + conector + rotulo)
        proximo = prefixo + ("" if raiz else ("    " if ultimo else "│   "))
        for indice, filho in enumerate(filhos):
            visitar(filho, proximo, indice == len(filhos) - 1)

    visitar(raiz, raiz=True)
    return "\n".join(linhas)
