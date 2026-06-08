"""Ponto de entrada do compilador — analise lexica."""

from __future__ import annotations

import sys

from antlr4 import CommonTokenStream, FileStream, Token
from antlr4.error.ErrorListener import ErrorListener

from LangLexer import LangLexer
from token_output import format_token_line


class LexerErrorListener(ErrorListener):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        char = offendingSymbol.text if offendingSymbol else "?"
        self.errors.append(
            f"Linha {line}:{column} - erro lexico: caractere/token invalido '{char}'"
        )


def run_lexical(source_file: str) -> int:
    try:
        input_stream = FileStream(source_file, encoding="utf-8")
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {source_file}")
        return 1

    lexer = LangLexer(input_stream)
    error_listener = LexerErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    stream = CommonTokenStream(lexer)
    stream.fill()

    token_names = lexer.symbolicNames

    sep = "-" * 60
    print(f"\n{sep}")
    print(f"  TOKENS - {source_file}")
    print(sep)
    print(f"{'Linha':<7} {'Tipo':<12} {'Atributo'}")
    print(sep)

    for tok in stream.tokens:
        if tok.type == Token.EOF:
            continue

        type_name = (
            token_names[tok.type]
            if tok.type < len(token_names)
            else str(tok.type)
        )
        print(format_token_line(tok, type_name))

    print(f"{sep}\n")

    if error_listener.errors:
        print("ERROS LEXICOS:")
        for e in error_listener.errors:
            print(f"  {e}")
        return 1

    print("Analise lexica concluida sem problemas.")
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.sl>")
        sys.exit(1)

    sys.exit(run_lexical(sys.argv[1]))


if __name__ == "__main__":
    main()
