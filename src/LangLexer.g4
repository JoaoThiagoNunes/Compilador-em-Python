lexer grammar LangLexer;

options { caseInsensitive = true; }

// Palavras reservadas
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

// Operadores aritmeticos (tipo OPAD / OPMULT definidos abaixo)
fragment MAIS_CHAR  : '+';
fragment MENOS_CHAR : '-';

// Operadores relacionais (tipo OPREL)
fragment MENOR_CHAR  : '<';
fragment MAIOR_CHAR  : '>';

// Operadores logicos (tipo OPLOG)
// AND e OR ja definidos como palavras reservadas acima

// Negacao logica
OPNEG : '~';

// Pontuacao
PVIG   : ';';
PONTO  : '.';
DPONTOS: ':';
VIG    : ',';
ABPAR  : '(';
FPAR   : ')';
ATRIB  : ':=';

// Operadores compostos — devem vir antes dos simples
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

// Identificador (max 16 chars validado pos-lex)
fragment LETTER     : [a-z];
fragment ALNUM      : [a-z0-9];

ID
    : LETTER ALNUM*
    ;

// Constante inteira (intervalo validado pos-lex)
CTE
    : [+-]? [0-9]+
    ;

// Literal string
CADEIA
    : '"' ~["\r\n]* '"'
    ;

// Comentarios: / texto /
COMMENT
    : '/' ~[\r\n]* '/' -> skip
    ;

// Espacos em branco
WS
    : [ \t\r\n]+ -> skip
    ;
