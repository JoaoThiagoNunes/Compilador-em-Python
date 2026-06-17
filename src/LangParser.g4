// Gramatica corrigida conforme Especificacao Projeto I (Prof. Layse Souza).
// Terminais = tokens do LangLexer.g4
//
// Correcoes em relacao a gramatica original do enunciado:
// - Precedencia: OPLOG < OPREL < OPAD < OPMULT < OPNEG
// - OPENG (operandos primarios) restrito a factor, nao a expr inteira

parser grammar LangParser;

options { tokenVocab = LangLexer; }

prog
    : PROGRAM ID PVIG decls cmdComp PONTO
    ;

decls
    :
    | VAR listDecl
    ;

listDecl
    : declTip+
    ;

declTip
    : listId DPONTOS tip PVIG
    ;

listId
    : ID (VIG ID)*
    ;

tip
    : INTEGER
    | BOOLEAN
    ;

cmdComp
    : BEGIN listCmd END
    ;

listCmd
    : cmd (PVIG cmd)*
    ;

cmd
    : cmdWhile
    | cmdRead
    | cmdWrite
    | cmdAtrib
    | cmdComp
    ;

cmdWhile
    : WHILE expr DO cmd                     # cmdEnquanto
    ;

cmdRead
    : READ ABPAR listId FPAR                # cmdLeitura
    ;

cmdWrite
    : WRITE ABPAR listW FPAR                # cmdEscrita
    ;

listW
    : elemW (VIG elemW)*
    ;

elemW
    : expr
    | CADEIA
    ;

cmdAtrib
    : ID ATRIB expr                         # cmdAtribuicao
    ;

expr
    : expr OPLOG exprRel                    # exprLog
    | exprRel                               # exprPass
    ;

exprRel
    : exprRel OPREL exprAd                  # exprRelOp
    | exprAd                                # exprRelPass
    ;

exprAd
    : exprAd OPAD term                      # exprAdOp
    | term                                  # exprAdPass
    ;

term
    : term OPMULT factor                    # termMul
    | factor                                # termPass
    ;

factor
    : OPNEG factor                          # fatorNeg
    | ABPAR expr FPAR                       # fatorPar
    | ID                                    # fatorId
    | CTE                                   # fatorCte
    | TRUE                                  # fatorTrue
    | FALSE                                 # fatorFalse
    ;
