from LangParserVisitor import LangParserVisitor
from lexer import nome_id


class GeradorCodigo(LangParserVisitor):
    def __init__(self):
        self.instrucoes = []
        self.temp = 0
        self.rot = 0

    def _temp(self):
        self.temp += 1
        return f"t{self.temp}"

    def _rot(self):
        self.rot += 1
        return f"L{self.rot}"

    def visitProg(self, ctx):
        self.instrucoes.append("PARA")
        self.visit(ctx.decls())
        self.visit(ctx.cmdComp())

    def visitDeclTip(self, ctx):
        tipo = ctx.tip().getText().upper()
        valor = "0" if tipo == "INTEGER" else "false"
        for id_token in ctx.listId().ID():
            self.instrucoes.append(f"ALME {valor} {nome_id(id_token.getText())}")

    def visitCmdLeitura(self, ctx):
        for id_token in ctx.listId().ID():
            self.instrucoes.append(f"LEIT {nome_id(id_token.getText())}")

    def visitCmdEscrita(self, ctx):
        for elem in ctx.listW().elemW():
            if elem.CADEIA():
                self.instrucoes.append(f"IMPR {elem.CADEIA().getText()}")
            else:
                self.instrucoes.append(f"IMPR {self.visit(elem.expr())}")

    def visitCmdAtribuicao(self, ctx):
        dest = nome_id(ctx.ID().getText())
        orig = self.visit(ctx.expr())
        self.instrucoes.append(f"ATRI {orig} {dest}")

    def visitCmdEnquanto(self, ctx):
        rot_ini = self._rot()
        rot_fim = self._rot()
        self.instrucoes.append(f"ROT {rot_ini}")
        cond = self.visit(ctx.expr())
        self.instrucoes.append(f"DSVF {cond} {rot_fim}")
        self.visit(ctx.cmd())
        self.instrucoes.append(f"DSVI {rot_ini}")
        self.instrucoes.append(f"ROT {rot_fim}")

    def visitCmdComp(self, ctx):
        self.visit(ctx.listCmd())

    def visitListCmd(self, ctx):
        for cmd in ctx.cmd():
            self.visit(cmd)

    def visitExprLog(self, ctx):
        esq = self.visit(ctx.expr())
        dir = self.visit(ctx.exprRel())
        op = "OU" if ctx.OPLOG().getText().upper() == "OR" else "E"
        t = self._temp()
        self.instrucoes.append(f"{op} {esq} {dir} {t}")
        return t

    def visitExprPass(self, ctx):
        return self.visit(ctx.exprRel())

    def visitExprRelOp(self, ctx):
        esq = self.visit(ctx.exprRel())
        dir = self.visit(ctx.exprAd())
        op = ctx.OPREL().getText()
        mapa = {
            "==": "IGUAL",
            "<>": "DIF",
            "<": "MENOR",
            "<=": "MENIG",
            ">": "MAIOR",
            ">=": "MAIG",
        }
        t = self._temp()
        self.instrucoes.append(f"{mapa[op]} {esq} {dir} {t}")
        return t

    def visitExprRelPass(self, ctx):
        return self.visit(ctx.exprAd())

    def visitExprAdOp(self, ctx):
        esq = self.visit(ctx.exprAd())
        dir = self.visit(ctx.term())
        op = "SOMA" if ctx.OPAD().getText() == "+" else "SUBT"
        t = self._temp()
        self.instrucoes.append(f"{op} {esq} {dir} {t}")
        return t

    def visitExprAdPass(self, ctx):
        return self.visit(ctx.term())

    def visitTermMul(self, ctx):
        esq = self.visit(ctx.term())
        dir = self.visit(ctx.factor())
        op = "MULT" if ctx.OPMULT().getText() == "*" else "DIVI"
        t = self._temp()
        self.instrucoes.append(f"{op} {esq} {dir} {t}")
        return t

    def visitTermPass(self, ctx):
        return self.visit(ctx.factor())

    def visitFatorNeg(self, ctx):
        op = self.visit(ctx.factor())
        t = self._temp()
        self.instrucoes.append(f"NAO {op} {t}")
        return t

    def visitFatorPar(self, ctx):
        return self.visit(ctx.expr())

    def visitFatorId(self, ctx):
        return nome_id(ctx.ID().getText())

    def visitFatorCte(self, ctx):
        valor = ctx.CTE().getText()
        t = self._temp()
        self.instrucoes.append(f"CMET {valor} {t}")
        return t

    def visitFatorTrue(self, ctx):
        t = self._temp()
        self.instrucoes.append(f"CMET true {t}")
        return t

    def visitFatorFalse(self, ctx):
        t = self._temp()
        self.instrucoes.append(f"CMET false {t}")
        return t


def gerar_codigo(arvore):
    gerador = GeradorCodigo()
    gerador.visit(arvore)
    return gerador
