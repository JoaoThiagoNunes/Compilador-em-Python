from LangParserVisitor import LangParserVisitor


class GeradorCodigo(LangParserVisitor):
    def __init__(self):
        self.instrucoes = []
        self.temp = 0
        self.rot = 0
        self.tabela = {}

    def _temp(self):
        self.temp += 1
        return f"t{self.temp}"

    def _rot(self):
        self.rot += 1
        return f"L{self.rot}"

    def _valor_inicial(self, tipo):
        if tipo == "INTEGER":
            return "0"
        if tipo == "BOOLEAN":
            return "false"
        return '""'

    def visitProg(self, ctx):
        self.instrucoes.append("PARA")
        self.visit(ctx.decls())
        self.visit(ctx.cmdComp())

    def visitDeclTip(self, ctx):
        tipo = ctx.tip().getText().upper()
        for id_token in ctx.listId().ID():
            nome = id_token.getText()
            self.tabela[nome] = tipo
            self.instrucoes.append(f"ALME {self._valor_inicial(tipo)} {nome}")

    def visitCmdLeitura(self, ctx):
        for id_token in ctx.listId().ID():
            self.instrucoes.append(f"LEIT {id_token.getText()}")

    def visitCmdEscrita(self, ctx):
        for elem in ctx.listW().elemW():
            if elem.CADEIA():
                texto = elem.CADEIA().getText()
                self.instrucoes.append(f"IMPR {texto}")
            else:
                alvo = self.visit(elem.expr())
                self.instrucoes.append(f"IMPR {alvo}")

    def visitCmdAtribuicao(self, ctx):
        dest = ctx.ID().getText()
        orig = self.visit(ctx.expr())
        self.instrucoes.append(f"ATRI {orig} {dest}")

    def visitCmdSe(self, ctx):
        cond = self.visit(ctx.expr())
        rot_senao = self._rot()
        rot_fim = self._rot()

        if ctx.ELSE():
            self.instrucoes.append(f"DSVF {cond} {rot_senao}")
            self.visit(ctx.cmd(0))
            self.instrucoes.append(f"DSVI {rot_fim}")
            self.instrucoes.append(f"ROT {rot_senao}")
            self.visit(ctx.cmd(1))
            self.instrucoes.append(f"ROT {rot_fim}")
        else:
            self.instrucoes.append(f"DSVF {cond} {rot_fim}")
            self.visit(ctx.cmd(0))
            self.instrucoes.append(f"ROT {rot_fim}")

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

    def visitExprRel(self, ctx):
        esq = self.visit(ctx.expr())
        dir = self.visit(ctx.expr2())
        op = ctx.OPREL().getText()
        mapa = {
            "==": "IGUAL",
            "<>": "DIF",
            "<": "MENOR",
            "<=": "MENIG",
            ">": "MAIOR",
            ">=": "MAIG",
        }
        nome = mapa.get(op, "IGUAL")
        t = self._temp()
        self.instrucoes.append(f"{nome} {esq} {dir} {t}")
        return t

    def visitExprPass(self, ctx):
        return self.visit(ctx.expr2())

    def visitExprAd(self, ctx):
        esq = self.visit(ctx.expr2())
        dir = self.visit(ctx.term())
        op = "SOMA" if ctx.OPAD().getText() == "+" else "SUBT"
        t = self._temp()
        self.instrucoes.append(f"{op} {esq} {dir} {t}")
        return t

    def visitExpr2Pass(self, ctx):
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
        return ctx.ID().getText()

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
