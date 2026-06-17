# Compilador — Projeto I (Linguagens Formais e Compiladores)

Compilador para a linguagem definida em **Especificacao - Projeto I** (Prof. Layse Souza), usando **ANTLR 4** e **Python 3**.

## Informacoes

* **Disciplina:** Linguagens Formais e Compiladores
* **Docente:** Profa. Ma. Layse Souza
* **Aluno:** Joao Thiago Nunes

## Instalacao

```powershell
pip install -r requirements.txt
.\build.ps1
```

## Uso

```powershell
cd src

python main.py ..\examples\ok_lexico.sl
python main.py ..\examples\ok_programa.sl --parse
python main.py ..\examples\ok_programa.sl --semantic
python main.py ..\examples\ok_programa.sl --code
```

## Estrutura

```
src/
  LangLexer.g4      # Tokens conforme PDF
  LangParser.g4     # Gramatica corrigida
  token_output.py   # Saida tipo + atributo
  lexer.py          # Validacao ID (16) e CTE (16 bits)
  parser.py         # Analise sintatica
  semantic.py       # Analise semantica
  codegen.py        # Geracao de codigo
  main.py
examples/
docs/conflitos.md
```

---

## Descricao lexica (conforme PDF)

### Palavras reservadas

`PROGRAM`, `INTEGER`, `BOOLEAN`, `BEGIN`, `END`, `WHILE`, `DO`, `READ`, `VAR`, `FALSE`, `TRUE`, `WRITE`

### Regras

* Case insensitive
* Comentarios: `/ texto /`
* ID: letra + letras/numeros, max 16 caracteres (extras truncados)
* CTE: inteiro com sinal opcional, intervalo -32768..32767
* CADEIA: `"texto"` (tipo lexico para strings)

### Tokens com atributo

| Simbolo | Tipo | Atributo |
|---------|------|----------|
| `+` `-` | OPAD | MAIS MENOS |
| `*` `/` | OPMULT | VEZES DIV |
| `OR` `AND` | OPLOG | OR AND |
| `~` | OPNEG | NEG |
| `<` `<=` `>` `>=` `==` `<>` | OPREL | MENOR MENIG MAIOR MAIG IGUAL DIFER |
| identificador | ID | cadeia |
| inteiro | CTE | valor |
| `"..."` | CADEIA | texto |

### Pontuacao

`;` PVIG · `.` PONTO · `:` DPONTOS · `,` VIG · `(` ABPAR · `)` FPAR · `:=` ATRIB

### Erro lexico

Para execucao e informa linha/coluna. Sucesso imprime tokens com tipo e atributo.

---

## Descricao sintatica

Gramatica corrigida (detalhes em `docs/conflitos.md`):

```bnf
Prog     -> PROGRAM ID ; Decls CmdComp .
Decls    -> | VAR ListDecl
DeclTip  -> ListId : Tip ;
Tip      -> INTEGER | BOOLEAN
CmdComp  -> BEGIN ListCmd END
Cmd      -> While | Read | Write | Atrib | CmdComp
While    -> WHILE Expr DO Cmd
Read     -> READ ( ListId )
Write    -> WRITE ( ListW )
Atrib    -> ID := Expr
Expr     -> niveis OPLOG, OPREL, OPAD, OPMULT, factor (OPENG)
```

---

## Gerar codigo ANTLR

```powershell
.\build.ps1
```
