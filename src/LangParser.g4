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
    | STRING
    ;

cmdComp
    : BEGIN listCmd END
    ;

listCmd
    : cmd (PVIG cmd)*
    ;

cmd
    : cmdIf
    | cmdWhile
    | cmdRead
    | cmdWrite
    | cmdAtrib
    | cmdComp
    ;

cmdIf
    : IF expr THEN cmd (ELSE cmd)?          # cmdSe
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
    : expr OPREL expr2                      # exprRel
    | expr2                                 # exprPass
    ;

expr2
    : expr2 OPAD term                       # exprAd
    | term                                  # expr2Pass
    ;

term
    : term OPMULT factor                    # termMul
    | factor                                # termPass
    ;

factor
    : OPNEG factor                          # fatorNeg
    | ABPAR expr FPAR                       # fatorPar
    | ID                                    # fatorId
    | CTE                                     # fatorCte
    | TRUE                                    # fatorTrue
    | FALSE                                   # fatorFalse
    ;
