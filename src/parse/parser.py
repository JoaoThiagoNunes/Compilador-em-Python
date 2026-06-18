from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees

from lexica.LangLexer import LangLexer
from parse.LangParser import LangParser


class ErroSintatico(ErrorListener):
    def __init__(self):
        self.mensagem = None

    def syntaxError(self, recognizer, symbol, line, column, msg, e):
        if self.mensagem:
            return

        if symbol is None:
            encontrado = "EOF"
        else:
            encontrado = symbol.text

        esperado = self._tokens_esperados(recognizer, e)
        self.mensagem = (
            f"Linha {line}: encontrado '{encontrado}' vs esperado {esperado}"
        )

    def _tokens_esperados(self, recognizer, e):
        if e is None or not hasattr(e, "getExpectedTokens"):
            return "?"

        nomes = recognizer.symbolicNames
        lista = []
        for t in e.getExpectedTokens():
            if 0 <= t < len(nomes) and nomes[t]:
                lista.append(nomes[t])

        if not lista:
            return "?"
        if len(lista) > 6:
            resto = len(lista) - 6
            return ", ".join(lista[:6]) + f", ... (+{resto})"
        return ", ".join(lista)


def analisar(arquivo):
    from antlr4 import CommonTokenStream, FileStream

    entrada = FileStream(arquivo, encoding="utf-8")
    lexer = LangLexer(entrada)
    tokens = CommonTokenStream(lexer)

    parser = LangParser(tokens)
    parser.removeErrorListeners()

    erros = ErroSintatico()
    parser.addErrorListener(erros)

    arvore = parser.prog()
    return arvore, parser, erros


def mostrar_arvore(arvore, parser):
    return Trees.toStringTree(arvore, None, parser)
