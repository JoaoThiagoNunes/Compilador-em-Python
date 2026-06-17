lexer grammar LangLexer;

options { caseInsensitive = true; }

// Palavras reservadas (conforme Especificacao Projeto I)
PROGRAM : 'PROGRAM';
VAR     : 'VAR';
INTEGER : 'INTEGER';
BOOLEAN : 'BOOLEAN';
BEGIN   : 'BEGIN';
END     : 'END';
WHILE   : 'WHILE';
DO      : 'DO';
READ    : 'READ';
WRITE   : 'WRITE';
TRUE    : 'TRUE';
FALSE   : 'FALSE';

fragment MAIS_CHAR  : '+';
fragment MENOS_CHAR : '-';
fragment MENOR_CHAR : '<';
fragment MAIOR_CHAR : '>';

OPNEG : '~';

PVIG   : ';';
PONTO  : '.';
DPONTOS: ':';
VIG    : ',';
ABPAR  : '(';
FPAR   : ')';
ATRIB  : ':=';

OPREL
    : '=='
    | '<='
    | '>='
    | '<>'
    | MENOR_CHAR
    | MAIOR_CHAR
    ;

OPAD
    : MAIS_CHAR
    | MENOS_CHAR
    ;

OPMULT
    : '*'
    | '/'
    ;

OPLOG
    : 'OR'
    | 'AND'
    ;

fragment LETTER : [a-z];
fragment ALNUM  : [a-z0-9];

ID
    : LETTER ALNUM*
    ;

CTE
    : [+-]? [0-9]+
    ;

CADEIA
    : '"' ~["\r\n]* '"'
    ;

COMMENT
    : '/' ~[\r\n]* '/' -> skip
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
