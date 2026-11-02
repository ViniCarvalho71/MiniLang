# MiniLang — Analisadores Léxico e Sintático

Projeto desenvolvido para implementação de um analisador léxico manual e de um parser descendente recursivo para a linguagem **MiniLang**, com visualização textual da Árvore Sintática Abstrata (AST).

O analisador recebe o conteúdo completo de um arquivo-fonte, percorre a entrada da esquerda para a direita e produz os tokens reconhecidos e os diagnósticos encontrados durante a análise.

## Integrantes

* Nome: Mauricio Shiguemitsu Kamado Ikeda / RA: 199029
* Nome: Paulo Henrique Almeida Veloso Leite / RA: 2008124
* Nome: Vinícius de Andrade Costa / RA: 2002512
* Nome: Vinícius Estevão Consolino Brandi / RA: 2002558
* Nome: Vinícius Carvalho da Silva / RA: 2002503

## Estrutura do projeto

```text
MiniLang/
├── README.md
├── main.py
├── minilang/
│   ├── __init__.py
│   ├── lexer.py
│   ├── ast.py
│   └── visualizador.py
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   └── test_processamento_simbolo_a_simbolo.py
└── examples/
    ├── programa.min
    ├── ast.min
    └── erro_sintatico.min
```

### `main.py`

Ponto de entrada do programa.

É responsável por ler o arquivo-fonte, executar o lexer e o parser e exibir a AST. A opção `--somente-lexer` permite executar apenas a análise léxica.

### `minilang/ast.py` e `minilang/visualizador.py`

`ast.py` contém as classes dos nós e o parser. `visualizador.py` percorre os nós e formata a árvore com os operandos esquerdo e direito nessa ordem, sem executar as expressões.

### `minilang/lexer.py`

Contém a implementação do analisador léxico.

O lexer percorre o código-fonte símbolo por símbolo, reconhecendo tokens, ignorando comentários e espaços em branco e registrando diagnósticos para símbolos inválidos.

### `tests/`

Contém os testes automatizados utilizados para verificar o comportamento do lexer, incluindo reconhecimento de tokens, posições, comentários, casos-limite e tratamento de caracteres inválidos.

### `examples/programa.min`

Arquivo-fonte de exemplo escrito em MiniLang.

O programa contém exemplos das principais construções léxicas da linguagem e pode ser utilizado para testar manualmente o analisador.

## Execução

A partir da pasta raiz do projeto, execute:

```bash
python main.py examples/ast.min
```

O programa exibe os tokens, os diagnósticos e a AST. Requer Python 3.9 ou superior, sem dependências externas.

Para executar somente o lexer com o exemplo original:

```bash
python main.py examples/programa.min --somente-lexer
```

Esse exemplo original inclui construções reconhecidas pelo lexer que estão fora do escopo do parser.

## Exemplo de AST

O arquivo `examples/ast.min` contém:

```text
int x;
x = 2 + 3 * 4;
print(x);
```

A árvore exibida é:

```text
Programa
├── Declaracao(x)
├── Atribuicao(x)
│   └── Binaria(+)
│       ├── Inteiro(2)
│       └── Binaria(*)
│           ├── Inteiro(3)
│           └── Inteiro(4)
└── Saida
    └── Variavel(x)
```

A multiplicação fica no ramo direito da soma, preservando a precedência. Parênteses alteram o agrupamento; operações de mesma precedência associam à esquerda.

Para demonstrar um erro sintático:

```bash
python main.py examples/erro_sintatico.min
```

O resultado inclui `Esperada uma expressão, encontrado RPAREN na linha 2, coluna 11`. O programa para no primeiro erro sintático e retorna código de saída 1. Erros léxicos também impedem a geração da AST.

## Testes

Os testes automatizados podem ser executados com:

```bash
python -m unittest discover -s tests -v
```

## Organização do lexer

O lexer mantém um cursor sobre o código-fonte e processa a entrada da esquerda para a direita.

Durante a análise, são mantidas informações como:

* posição inicial do lexema atual;
* posição atual na entrada;
* linha e coluna atuais;
* linha e coluna de início do lexema;
* tokens produzidos;
* diagnósticos encontrados.

A implementação utiliza operações específicas para avançar e consultar símbolos da entrada, reconhecer identificadores e números, tratar comentários e adicionar tokens ou diagnósticos ao resultado.

Entre as operações utilizadas pelo lexer estão:

* `scan_tokens()`
* `scan_token()`
* `at_end()`
* `advance()`
* `peek()`
* `peek_next()`
* `match()`
* `add_token()`
* `identifier()`
* `number()`
* `line_comment()`
* `report_invalid_character()`

O reconhecimento é realizado manualmente, sem divisão prévia da entrada em palavras ou tokens.

## Escopo léxico

O lexer da MiniLang reconhece:

* palavras reservadas: `int`, `print`, `if`, `else` e `while`;
* identificadores;
* literais inteiros;
* operador de atribuição `=`;
* operadores aritméticos `+`, `-`, `*` e `/`;
* operadores relacionais `==`, `!=`, `<`, `<=`, `>` e `>=`;
* delimitadores `(`, `)`, `{`, `}` e `;`;
* comentários de linha iniciados por `//`;
* espaços em branco, tabulações e quebras de linha.

Comentários e espaços em branco são consumidos pelo lexer, mas não são incluídos na lista de tokens.

Ao final da entrada, o lexer produz um token `EOF`.

## Limitações conhecidas

O parser reconhece declarações `int x;`, atribuições, `print`, identificadores, inteiros e expressões com `+`, `-`, `*`, `/` e parênteses. Declarações com inicialização (`int x = 1;`), `if`, `else`, `while`, blocos, operadores relacionais e unários estão fora do escopo. O parser não verifica declarações de variáveis nem executa o programa.
