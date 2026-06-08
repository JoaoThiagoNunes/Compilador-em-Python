# Correcoes da gramatica original

## 1. Expressoes ambiguas

**Original:** todos os operadores no mesmo nivel de `Expr`.

**Corrigido:** `expr -> expr OPREL expr2 | expr2`, depois `expr2 -> expr2 OPAD term | term`, etc.

## 2. Operandos primarios

**Original:** segunda producao de `Expr` competia com expressoes completas.

**Corrigido:** primarios ficam em `factor` (`ID`, `CTE`, `TRUE`, `FALSE`, parenteses, `OPNEG`).

## 3. Declaracao de variaveis

Formato: `a , b : INTEGER ;`

## 4. Lexer

Incluidos `IF`, `THEN`, `ELSE` e tipo `STRING`.
