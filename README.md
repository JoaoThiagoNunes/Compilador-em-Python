# Compilador — Projeto I (Linguagens Formais e Compiladores)

Compilador para linguagem imperativa simples, desenvolvido com **ANTLR 4** e **Python 3**.

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
