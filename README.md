# Projeto Compilador - Analisador Léxico e Sintático

Este repositório contém o desenvolvimento de um compilador para uma linguagem de programação acadêmica, desenvolvido para a disciplina de **Linguagens Formais e Compiladores**.

## 📌 Informações do Projeto
* **Curso:** Ciência da Computação
* **Disciplina:** Linguagens Formais e Compiladores
* **Docente:** Profa. Ma. Layse Souza
* **Aluno:** João Thiago Nunes

---

## 📑 1. Descrição Léxica

A análise léxica é responsável por identificar e agrupar os caracteres do código-fonte em unidades significativas chamadas **Tokens**. Nesta etapa, o foco está na estrutura individual dos termos e não na organização hierárquica deles.

### ⚙️ Regras Gerais e Restrições
* **Case Insensitivity:** A linguagem não diferencia letras maiúsculas de minúsculas.
* **Espaços em Branco:** Todos os espaços em branco entre os tokens são ignorados e descartados.
* **Comentários:** Comentários de linha são delimitados por `// .. //` (ex: `// isto é um comentário //`). O conteúdo interno é totalmente descartado.
* **Identificadores (`ID`):** * Sequência de letras e números que começa obrigatoriamente por uma letra.
  * Comprimento máximo de **16 caracteres**. Caracteres adicionais além deste limite são truncados/descartados.
* **Constantes Inteiras (`CTE`):**
  * Números inteiros, podendo ser com sinal (`+`, `-`) ou sem sinal.
  * O valor armazenado não pode ultrapassar o limite de **2 bytes** (valores entre -32768 e 32767).
* **Cadeias de Caracteres (`CADEIA` / `STRING`):**
  * Delimitadas obrigatoriamente por aspas duplas no início e fim (ex: `"exemplo"`).

### 🪙 Palavras Reservadas
Se o token for uma palavra reservada, o seu tipo é a própria palavra.
> `PROGRAM`, `INTEGER`, `BOOLEAN`, `BEGIN`, `END`, `WHILE`, `DO`, `READ`, `VAR`, `FALSE`, `TRUE`, `WRITE`

### 📊 Tabelas de Tokens, Tipos e Atributos

#### Operadores Aritméticos, Lógicos e de Negação
| Símbolo | Token | Tipo | Atributo |
| :---: | :---: | :---: | :---: |
| `+` | `OPAD` | `MAIS` | - |
| `-` | `OPAD` | `MENOS` | - |
| `*` | `OPMULT` | `VEZES` | - |
| `/` | `OPMULT` | `DIV` | - |
| `OR` | `OPLOG` | `OR` | - |
| `AND` | `OPLOG` | `AND` | - |
| `~` | `OPNEG` | `NEG` | - |

#### Operadores Relacionais
| Símbolo | Token | Tipo | Atributo |
| :---: | :---: | :---: | :---: |
| `<` | `OPREL` | `MENOR` | - |
| `<=` | `OPREL` | `MENIG` | - |
| `>` | `OPREL` | `MAIOR` | - |
| `>=` | `OPREL` | `MAIG` | - |
| `==` | `OPREL` | `IGUAL` | - |
| `<>` | `OPREL` | `DIFER` | - |

#### Símbolos Especiais e Pontuação
| Símbolo | Token | Tipo | Atributo |
| :---: | :---: | :---: | :---: |
| `;` | `PVIG` | Ponto e Vírgula | - |
| `.` | `PONTO` | Ponto Final | - |
| `:` | `DPONTOS` | Dois Pontos | - |
| `,` | `VIG` | Vírgula | - |
| `(` | `ABPAR` | Abre Parênteses | - |
| `)` | `FPAR` | Fecha Parênteses | - |
| `:=` | `ATRIB` | Atribuição | - |

### 🚨 Tratamento de Erros e Sucesso Léxico
* **Em caso de Erro:** O compilador interrompe a execução imediatamente e exibe na tela a localização exata (`Linha` e `Coluna`) do caractere inválido.
* **Em caso de Sucesso:** O analisador gera e imprime a lista de tokens identificados no formato: `[Token, Tipo, Valor do Atributo]`.

---

## 📐 2. Descrição Sintática

A análise sintática determina se a estrutura dos tokens obedece às regras gramaticais da linguagem. Os termos em **letras maiúsculas** correspondem aos terminais (tokens vindos do léxico), enquanto os em minúsculas representam os não-terminais.

### 📑 Gramática Original (Com Conflitos)

```bnf
Prog       --> PROGRAM IDENTIFIER PVIG Decls CmdComp PONTO
Decls      --> ε | VAR ListDecl
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
