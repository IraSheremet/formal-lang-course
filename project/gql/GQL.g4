grammar GQL;

prog:	(stmt NEWLINE?)* EOF ;

stmt:   var '=' expr LINE_END
    |   'print' expr LINE_END
    ;

var:    initial_letter string ;
initial_letter: IDENTIFIER_CHAR ;
string: (initial_letter | '/' | '.' | INT)* ;


expr:	LEFT_PARENTHESIS expr RIGHT_PARENTHESIS
    |   var
    |   val
    |   map
    |   filter
    |   intersect
    |   concat
    |   union
    |   star
    ;

val:    LEFT_PARENTHESIS val RIGHT_PARENTHESIS
    |   QUOTE string QUOTE
    |   INT
    |   BOOL
    |   graph
    |   vertices
    |   labels
    |   edges
    ;

graph:  'set_start' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'set_final' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'add_start' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'add_final' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'load_graph' LEFT_PARENTHESIS path RIGHT_PARENTHESIS
    |   var
    ;

path:   QUOTE string QUOTE
    |   var
    ;

vertices:   'get_start' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   'get_final' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   'get_reachable' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   'get_vertices' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   LEFT_CURLY_BRACE INT (COMMA INT)* RIGHT_CURLY_BRACE
        |   var
        |   EMPTY_SET
        ;

labels: 'get_labels' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
    |   LEFT_CURLY_BRACE (QUOTE string QUOTE | INT | var) (COMMA (QUOTE string QUOTE | INT | var))* RIGHT_CURLY_BRACE
    |   EMPTY_SET
    ;

edges:  'get_edges' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
    |   LEFT_CURLY_BRACE LEFT_PARENTHESIS INT COMMA (val | var) COMMA INT RIGHT_PARENTHESIS ( COMMA LEFT_PARENTHESIS INT COMMA (val | var) COMMA INT RIGHT_PARENTHESIS )* RIGHT_CURLY_BRACE
    |   EMPTY_SET
    ;


lambda: 'fun' LEFT_PARENTHESIS var RIGHT_PARENTHESIS LEFT_CURLY_BRACE expr RIGHT_CURLY_BRACE ;
map:    'map' LEFT_PARENTHESIS lambda COMMA expr RIGHT_PARENTHESIS ;
filter: 'filter' LEFT_PARENTHESIS lambda COMMA expr RIGHT_PARENTHESIS ;

intersect   :  'intersect' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS ;
concat      :   'concat' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS ;
union       :   'union' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS ;
star        :   LEFT_PARENTHESIS expr RIGHT_PARENTHESIS '*' ;

COMMA: ',' ;
QUOTE: '"' ;
LEFT_CURLY_BRACE: '{';
RIGHT_CURLY_BRACE: '}';
LEFT_PARENTHESIS: '(' ;
RIGHT_PARENTHESIS: ')' ;
LINE_END: ';' ;
EMPTY_SET: 'set()';
WS: ([ \t\n\r\f] | ('/*' ~[\r\n]* '*/')) -> skip;
NEWLINE : [\r\n]+ -> skip ;
IDENTIFIER_CHAR : '_' | [a-z] | [A-Z] ;
INT     : '-'? [1-9][0-9]* | '0' ;
BOOL    : 'true' | 'false'  ;
