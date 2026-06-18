from lexica.lexer import nome_id
from parse.LangParserVisitor import LangParserVisitor

INT = "INTEGER"
BOOL = "BOOLEAN"


class AnalisadorSemantico(LangParserVisitor):
    def __init__(self):
        self.tabela = {}
        self.erros = []

    def _erro(self, linha, msg):
        self.erros.append(f"Linha {linha}: {msg}")

    def _linha(self, no):
        return no.symbol.line

    def visitDeclTip(self, ctx):
        tipo = ctx.tip().getText().upper()
        for id_token in ctx.listId().ID():
            nome = nome_id(id_token.getText())
            if nome in self.tabela:
                self._erro(id_token.symbol.line, f"variavel '{nome}' ja declarada")
            else:
                self.tabela[nome] = tipo

    def visitCmdAtribuicao(self, ctx):
        nome = nome_id(ctx.ID().getText())
        linha = self._linha(ctx.ID())
        if nome not in self.tabela:
            self._erro(linha, f"variavel '{nome}' nao declarada")
            return
        tipo_expr = self.visit(ctx.expr())
        if tipo_expr and self.tabela[nome] != tipo_expr:
            self._erro(linha, f"tipo incompativel na atribuicao de '{nome}'")

    def visitCmdLeitura(self, ctx):
        for id_token in ctx.listId().ID():
            nome = nome_id(id_token.getText())
            if nome not in self.tabela:
                self._erro(id_token.symbol.line, f"variavel '{nome}' nao declarada")

    def visitCmdEnquanto(self, ctx):
        linha = ctx.WHILE().symbol.line
        tipo = self.visit(ctx.expr())
        if tipo and tipo != BOOL:
            self._erro(linha, "condicao do WHILE deve ser booleana")
        self.visit(ctx.cmd())

    def visitCmdEscrita(self, ctx):
        for elem in ctx.listW().elemW():
            if elem.expr():
                self.visit(elem.expr())

    def visitExprLog(self, ctx):
        linha = ctx.OPLOG().symbol.line
        t1 = self.visit(ctx.expr())
        t2 = self.visit(ctx.exprRel())
        if t1 != BOOL or t2 != BOOL:
            self._erro(linha, "operador logico exige operandos booleanos")
        return BOOL

    def visitExprPass(self, ctx):
        return self.visit(ctx.exprRel())

    def visitExprRelOp(self, ctx):
        linha = ctx.OPREL().symbol.line
        t1 = self.visit(ctx.exprRel())
        t2 = self.visit(ctx.exprAd())
        if t1 != INT or t2 != INT:
            self._erro(linha, "operador relacional exige inteiros")
        return BOOL

    def visitExprRelPass(self, ctx):
        return self.visit(ctx.exprAd())

    def visitExprAdOp(self, ctx):
        linha = ctx.OPAD().symbol.line
        t1 = self.visit(ctx.exprAd())
        t2 = self.visit(ctx.term())
        if t1 != INT or t2 != INT:
            self._erro(linha, "operador aritmetico exige inteiros")
        return INT

    def visitExprAdPass(self, ctx):
        return self.visit(ctx.term())

    def visitTermMul(self, ctx):
        linha = ctx.OPMULT().symbol.line
        t1 = self.visit(ctx.term())
        t2 = self.visit(ctx.factor())
        if t1 != INT or t2 != INT:
            self._erro(linha, "operador aritmetico exige inteiros")
        return INT

    def visitTermPass(self, ctx):
        return self.visit(ctx.factor())

    def visitFatorNeg(self, ctx):
        linha = ctx.OPNEG().symbol.line
        t = self.visit(ctx.factor())
        if t != BOOL:
            self._erro(linha, "operador ~ exige operando booleano")
        return BOOL

    def visitFatorPar(self, ctx):
        return self.visit(ctx.expr())

    def visitFatorId(self, ctx):
        nome = nome_id(ctx.ID().getText())
        linha = self._linha(ctx.ID())
        if nome not in self.tabela:
            self._erro(linha, f"variavel '{nome}' nao declarada")
            return None
        return self.tabela[nome]

    def visitFatorCte(self, ctx):
        return INT

    def visitFatorTrue(self, ctx):
        return BOOL

    def visitFatorFalse(self, ctx):
        return BOOL


def analisar_semantica(arvore):
    analisador = AnalisadorSemantico()
    analisador.visit(arvore)
    return analisador
