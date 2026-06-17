# Correcoes da gramatica — Especificacao Projeto I

Documento de referencia: `Especificacao - Projeto I (1).pdf` (Prof. Layse Souza).

## Problemas da gramatica original (enunciado)

### 1. Expressoes ambiguas

Todas as producoes de `Expr` no mesmo nivel geravam ambiguidade
(ex.: `1 + 2 * 3`).

**Corrigido** com niveis de precedencia:

```
expr    -> expr OPLOG exprRel | exprRel
exprRel -> exprRel OPREL exprAd | exprAd
exprAd  -> exprAd OPAD term    | term
term    -> term OPMULT factor   | factor
factor  -> OPNEG factor | ( expr ) | ID | CTE | TRUE | FALSE
```

Ordem (menor para maior): `OPLOG` < `OPREL` < `OPAD` < `OPMULT` < `OPNEG`.

### 2. OPENG aplicado a Expr

O enunciado indica que operandos primarios (`ID`, `CTE`, `( expr )`,
`TRUE`, `FALSE`, `OPNEG`) estavam no nivel errado.

**Corrigido:** primarios ficam apenas em `factor`.

### 3. Declaracao de variaveis

Formato exigido: `id1 , id2 : INTEGER ;`

Tipos permitidos: apenas `INTEGER` e `BOOLEAN` (conforme palavras reservadas do PDF).

### 4. O que NAO faz parte desta especificacao

- Comandos `IF`, `THEN`, `ELSE` (nao estao nas palavras reservadas do PDF)
- Tipo `STRING` como palavra reservada (literais usam token `CADEIA`)
