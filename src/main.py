import sys
from antlr4 import CommonTokenStream, FileStream, Token
from antlr4.error.ErrorListener import ErrorListener
from LangLexer import LangLexer
from lexer import LexerValidator
from parser import analisar, mostrar_arvore
from token_output import format_token_line

class LexicalError(Exception):
    def __init__(self, message):
        self.message = message


class LexerErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        char = offendingSymbol.text if offendingSymbol else "?"
        error = f"Linha {line}:{column} - erro lexico: caractere/token invalido '{char}'"
        self.errors.append(error)
        raise LexicalError(error)


def run_lexical(source_file):
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
    try:
        stream.fill()
    except LexicalError as err:
        print(f"\nERRO LEXICO:\n  {err.message}")
        return 1

    validator = LexerValidator()
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

        type_name = token_names[tok.type] if tok.type < len(token_names) else str(tok.type)
        display_value = None

        if type_name == "ID":
            display_value = validator.validate_identifier(tok.text, tok.line, tok.column)
        elif type_name == "CTE":
            if not validator.validate_integer(tok.text, tok.line, tok.column):
                print(format_token_line(tok, type_name, tok.text))
                print(f"\n{validator.report()}")
                return 1
            display_value = tok.text

        print(format_token_line(tok, type_name, display_value))

    print(f"{sep}\n")

    if error_listener.errors:
        print("ERROS LEXICOS:")
        for e in error_listener.errors:
            print(f"  {e}")
        return 1

    print(validator.report())
    if validator.has_errors():
        return 1
    return 0


def run_parse(source_file):
    try:
        arvore, parser, erros = analisar(source_file)
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {source_file}")
        return 1

    sep = "-" * 60
    print(f"\n{sep}")
    print(f"  ANALISE SINTATICA - {source_file}")
    print(sep)

    if erros.mensagem:
        print(f"ERRO SINTATICO: {erros.mensagem}")
        return 1

    print("Programa sintaticamente valido.\n")
    print("Arvore sintatica:")
    print(mostrar_arvore(arvore, parser))
    print()
    return 0


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.sl> [--parse]")
        sys.exit(1)

    arquivo = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--parse":
        sys.exit(run_parse(arquivo))

    sys.exit(run_lexical(arquivo))


if __name__ == "__main__":
    main()
