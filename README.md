# Compilador — Projeto I (Linguagens Formais e Compiladores)

Compilador para linguagem imperativa simples, desenvolvido com **ANTLR 4** e **Python 3**.

## Informacoes do Projeto

* **Curso:** Ciencia da Computacao
* **Disciplina:** Linguagens Formais e Compiladores
* **Docente:** Profa. Ma. Layse Souza
* **Aluno:** Joao Thiago Nunes

---

## Requisitos

- Python 3.10+
- Java JRE 11+ (para gerar o lexer com ANTLR)

## Instalacao

```powershell
pip install -r requirements.txt
.\build.ps1
```

## Uso

```powershell
cd src
python main.py ..\examples\ok_lexico.sl
```

## Estrutura

```
src/
  LangLexer.g4      # Especificacao lexica
  token_output.py   # Formatacao tipo + atributo
  lexer.py          # Validacoes pos-lexicas
  main.py           # CLI
examples/           # Programas de teste
```

## Fases implementadas

| Commit | Conteudo |
|--------|----------|
| 1 | Estrutura base, build, dependencias |
| 2 | Lexer conforme especificacao (tokens, atributos, case-insensitive) |
| 3 | Validacoes (ID 16 chars, CTE 16 bits) e erros lexicos |

## Gerar codigo ANTLR

Apos alterar `LangLexer.g4`, execute na raiz do projeto:

```powershell
.\build.ps1
```

O arquivo `LangLexer.py` e gerado em `src/` e ignorado pelo git.

---

## Descricao Lexica

A analise lexica identifica e agrupa caracteres do codigo-fonte em **tokens**.

### Regras gerais

* **Case insensitivity:** a linguagem nao diferencia maiusculas de minusculas.
* **Espacos em branco:** descartados entre tokens.
* **Comentarios:** delimitados por `/ ... /` (ex.: `/ isto e um comentario /`).
* **Identificadores (`ID`):** comecam por letra; maximo **16 caracteres** (extras truncados).
* **Constantes inteiras (`CTE`):** sinal opcional; intervalo **-32768 a 32767** (2 bytes).
* **Cadeias (`CADEIA`):** delimitadas por aspas duplas (ex.: `"texto"`).

### Palavras reservadas

`PROGRAM`, `INTEGER`, `BOOLEAN`, `BEGIN`, `END`, `WHILE`, `DO`, `READ`, `VAR`, `FALSE`, `TRUE`, `WRITE`

### Tabelas de tokens

#### Operadores aritmeticos, logicos e negacao

| Simbolo | Token | Atributo |
| :---: | :---: | :---: |
| `+` | `OPAD` | `MAIS` |
| `-` | `OPAD` | `MENOS` |
| `*` | `OPMULT` | `VEZES` |
| `/` | `OPMULT` | `DIV` |
| `OR` | `OPLOG` | `OR` |
| `AND` | `OPLOG` | `AND` |
| `~` | `OPNEG` | `NEG` |

#### Operadores relacionais

| Simbolo | Token | Atributo |
| :---: | :---: | :---: |
| `<` | `OPREL` | `MENOR` |
| `<=` | `OPREL` | `MENIG` |
| `>` | `OPREL` | `MAIOR` |
| `>=` | `OPREL` | `MAIG` |
| `==` | `OPREL` | `IGUAL` |
| `<>` | `OPREL` | `DIFER` |

#### Pontuacao

| Simbolo | Token |
| :---: | :---: |
| `;` | `PVIG` |
| `.` | `PONTO` |
| `:` | `DPONTOS` |
| `,` | `VIG` |
| `(` | `ABPAR` |
| `)` | `FPAR` |
| `:=` | `ATRIB` |

### Tratamento de erros lexicos

* **Erro:** interrompe a execucao e exibe linha/coluna do caractere invalido.
* **Sucesso:** imprime tokens no formato `Linha | Tipo | Atributo`.

---

## Descricao Sintatica (referencia)

Gramatica original com conflitos (a ser corrigida nas proximas fases):

```bnf
Prog       --> PROGRAM IDENTIFIER PVIG Decls CmdComp PONTO
Decls      --> e | VAR ListDecl
ListDecl   --> DeclTip | DeclTip ListDecl
DeclTip    --> ListId DPONTOS Tip PVIG
ListId     --> IDENTIFIER | IDENTIFIER VIG ListId
Tip        --> INTEGER | BOOLEAN | STRING

CmdComp    --> BEGIN ListCmd END
ListCmd    --> Cmd | Cmd PVIG ListCmd
Cmd        --> CmdIf | CmdWhile | CmdRead | CmdWrite | CmdAtrib | CmdComp

CmdIf      --> IF Expr THEN Cmd
             | IF Expr THEN Cmd ELSE Cmd

CmdWhile   --> WHILE Expr DO Cmd

CmdRead    --> READ ( ListId )
CmdWrite   --> WRITE ( ListW )
ListW      --> ElemW | ElemW VIG ListW
ElemW      --> Expr | CADEIA

CmdAtrib   --> IDENTIFIER := Expr

Expr       --> Expr OPREL Expr | Expr OPAD Expr | Expr OPMULT Expr
Expr       --> IDENTIFIER | CTE | ABPAR EXPR FPAR | TRUE | FALSE | OPNEG Expr
```
