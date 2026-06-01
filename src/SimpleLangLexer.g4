lexer grammar SimpleLangLexer;

// Palavras reservadas 
PROGRAM : 'PROGRAM';
VAR     : 'VAR';
INTEGER : 'INTEGER';
BOOLEAN : 'BOOLEAN';
STRING  : 'STRING';
BEGIN   : 'BEGIN';
END     : 'END';
WHILE   : 'WHILE';
DO      : 'DO';
READ    : 'READ';
WRITE   : 'WRITE';
TRUE    : 'TRUE';
FALSE   : 'FALSE';
IF      : 'IF';
THEN    : 'THEN';
ELSE    : 'ELSE';

// Operadores relacionais 
EQ  : '=';
NEQ : '<>';
LT  : '<';
GT  : '>';
LE  : '<=';
GE  : '>=';

//  Operadores aritméticos          
PLUS  : '+';
MINUS : '-';
TIMES : '*';
DIV   : '/';

// Operadores lógicos
AND : 'AND';
OR  : 'OR';
NOT : 'NOT';

// Atribuição e pontuação 
ASSIGN    : ':=';
COLON     : ':';
SEMICOLON : ';';
COMMA     : ',';
DOT       : '.';
LPAREN    : '(';
RPAREN    : ')';

// truncados para 16 chars no listener
IDENTIFIER
    : [a-zA-Z][a-zA-Z0-9]*
    ;

// Inteiros com sinal opcional (validados -32768..32767 no listener) 
CTE
    : [+-]? [0-9]+
    ;

// Literais string
CADEIA
    : '"' .*? '"'
    ;

// Comentários  (sintaxe / comentário /)
COMMENT
    : '/' .*? '/' -> skip
    ;

// Espaços em branco
WS
    : [ \t\r\n]+ -> skip
    ;
