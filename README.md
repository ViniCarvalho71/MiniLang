# MiniLang — Analisadores Léxico e Sintático

Projeto desenvolvido para implementação de um analisador léxico manual e de um parser descendente recursivo para a linguagem **MiniLang**, com visualização textual da Árvore Sintática Abstrata (AST).

O analisador recebe o conteúdo completo de um arquivo-fonte, percorre a entrada da esquerda para a direita e produz os tokens reconhecidos e os diagnósticos encontrados durante a análise.

No modo completo, os tokens alimentam o parser, que reconhece os comandos e constrói a AST. A árvore representa a estrutura do programa; as expressões não são executadas e não há análise semântica.

```text
Código-fonte → Lexer → Tokens → Parser → AST → Visualização textual
```

## Requisitos e preparação

* Python 3.9 ou superior, disponível no terminal.
* Nenhuma biblioteca externa: o projeto e os testes utilizam a biblioteca padrão do Python.
* Arquivos-fonte salvos em UTF-8, preferencialmente com extensão `.min`.

Abra o terminal na pasta raiz `MiniLang`, onde estão `main.py` e `README.md`, e confira o interpretador:

```bash
python --version
```

No Windows, se o comando disponível for `py`, substitua `python` por `py -3` nos comandos abaixo. Se houver erro de codificação ao imprimir a árvore, use `python -X utf8 main.py examples/ast.min`.

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
│   ├── test_parser.py
│   ├── test_main.py
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

Contém testes automatizados do lexer, do parser e da integração pelo `main.py`. Os testes do parser verificam os nós da AST, precedência, associatividade, parênteses, sequência de comandos, entrada vazia, consumo de EOF e diagnósticos com posição. Os testes de integração executam os exemplos de entrega e verificam os códigos de saída.

### `examples/programa.min`

Arquivo-fonte de exemplo escrito em MiniLang.

O programa contém exemplos das principais construções léxicas da linguagem e pode ser utilizado para testar manualmente o analisador.

## Execução

Para consultar os argumentos disponíveis:

```bash
python main.py --help
```

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

O arquivo inválido contém um comentário na primeira linha e `print(2 + );` na segunda; falta o operando direito da soma.

### Saída e códigos de retorno

* `Tokens:` lista tuplas no formato `(tipo, lexema, linha, coluna)`, incluindo `EOF`.
* `Diagnósticos:` lista os erros léxicos; sem erros, a seção fica vazia.
* `AST:` aparece após uma análise sintática bem-sucedida, exceto no modo `--somente-lexer`.
* Erros de leitura e erros sintáticos são exibidos na saída de erro do terminal.
* Código `0`: análise concluída com sucesso; código `1`: erro de leitura, léxico ou sintático; código `2`: argumentos de linha de comando inválidos.

Use aspas quando o caminho do arquivo contiver espaços, por exemplo: `python main.py "examples/meu programa.min"`.

## Testes

Os testes automatizados podem ser executados com:

```bash
python -m unittest discover -s tests -v
```

Para executar apenas os testes do parser:

```bash
python -m unittest discover -s tests -p "test_parser.py" -v
```

Para executar apenas os testes de integração:

```bash
python -m unittest discover -s tests -p "test_main.py" -v
```

### Cobertura e resultado verificado

| Arquivo | Verificações |
| --- | --- |
| `test_processamento_simbolo_a_simbolo.py` | Tokens, posições, palavras reservadas, operadores, comentários, entrada vazia e caracteres inválidos |
| `test_parser.py` | Declarações, atribuições, `print`, ordem dos comandos, entrada vazia e comentários, estrutura da AST, precedência, associatividade à esquerda, parênteses e consumo de EOF |
| `test_parser.py` | Erros com token, linha e coluna; interrupção no primeiro erro; rejeição de construções fora do escopo; visualização completa da AST |
| `test_main.py` | Execução do exemplo válido com AST, exemplo inválido com diagnóstico e exemplo original no modo léxico, incluindo códigos de saída |

`test_lexer.py` configura a apresentação dos grupos de testes; os testes léxicos estão em `test_processamento_simbolo_a_simbolo.py`.

Na verificação de 2 de novembro de 2026, a suíte completa passou com **25 testes**, incluindo casos adicionais executados com `subTest`:

```text
Ran 25 tests
OK
```

Os testes inspecionam a estrutura das expressões sem executá-las. Por exemplo, `print(1 / 0);` é sintaticamente válido e gera uma AST, sem realizar a divisão.

## Gramática reconhecida pelo parser

```text
programa   → item* EOF
item       → declaracao | atribuicao | saida
declaracao → "int" IDENT ";"
atribuicao → IDENT "=" expressao ";"
saida      → "print" "(" expressao ")" ";"
expressao  → termo (("+" | "-") termo)*
termo      → fator (("*" | "/") fator)*
fator      → IDENT | INT_LITERAL | "(" expressao ")"
```

`*` na notação da gramática indica zero ou mais repetições. Multiplicação e divisão têm precedência sobre soma e subtração. Operadores de mesma precedência associam à esquerda: `10 - 3 - 2` gera `(10 - 3) - 2`. Parênteses alteram o agrupamento.

O parser aceita entrada vazia, produzindo `Programa` com uma lista de itens vazia, e exige o consumo completo da entrada até `EOF`. `print(y);` é válido mesmo sem declaração de `y`, pois a verificação de variáveis não faz parte da análise sintática.

## Organização do parser e da AST

O parser está em `minilang/ast.py`. `Esperado()` consome um token do tipo exigido ou lança `SyntaxError`. `Programa()` reúne os comandos de `ListaItens()`; `Item()` seleciona declaração, atribuição ou saída. `Expressao()`, `Termo()` e `Fator()` constroem as expressões respeitando precedência e associatividade.

Os nós produzidos são `Programa`, `Declaracao`, `Atribuicao`, `Print`, `Binaria`, `Inteiro` e `Variavel`. Na visualização, o nó `Print` aparece com o rótulo `Saida`. Os filhos de uma operação binária são exibidos na ordem esquerda, direita.

## Conteúdo para a entrega do Trabalho 02

* Parser e classes da AST: `minilang/ast.py`.
* Visualização textual: `minilang/visualizador.py`.
* Integração e execução: `main.py`.
* Testes automatizados: pasta `tests/`, com resultado verificado acima.
* Programa válido e AST correspondente: `examples/ast.min` e a seção de exemplo deste README.
* Programa inválido e diagnóstico correspondente: `examples/erro_sintatico.min` e as instruções deste README.
* Requisitos, comandos de execução, gramática e limitações: este README.

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
