# MiniLang — Analisador Léxico

Projeto desenvolvido para implementação de um analisador léxico manual para a linguagem **MiniLang**.

O analisador recebe o conteúdo completo de um arquivo-fonte, percorre a entrada da esquerda para a direita e produz os tokens reconhecidos e os diagnósticos encontrados durante a análise.

## Integrantes

* Nome: Mauricio Shiguemitsu Kamado Ikeda / RA: 199029
* Nome: Paulo Henrique Almeida Veloso Leite / RA: 2008124
* Nome: Vinícius de Andrade Costa / RA: 2002512
* Nome: Vinícius Estevão Consolino Brandi / RA: 
* Nome: Vinícius Carvalho da Silva / RA: 2002503

## Estrutura do projeto

```text
MiniLang/
├── README.md
├── main.py
├── minilang/
│   ├── __init__.py
│   └── lexer.py
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   └── test_processamento_simbolo_a_simbolo.py
└── examples/
    └── programa.min
```

### `main.py`

Ponto de entrada do programa.

É responsável por receber o caminho de um arquivo-fonte MiniLang, ler seu conteúdo e encaminhá-lo ao analisador léxico.

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
python main.py examples/programa.min
```

O `main.py` irá ler o conteúdo do arquivo informado e executar a análise léxica.

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

Nenhuma limitação conhecida no momento.
