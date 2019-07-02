import ply.lex as lex

reserved = {
        'c' : 'CFUNK',
        'floor' : 'FLOOR',
        'size' : 'SIZE',
        'length' : 'LENGTH',
        'print' : 'PRINT'
}

# List of token names (always required)
tokens = ['EXPONENT',
          'PLUS',
          'MINUS',
          'TIMES',
          'DIVIDE',
          'EQUAL',
          'LPAREN',
          'RPAREN',
          'MODULO',
          'SEMICOLON',
          'COLON',
          'LBRACKET',
          'RBRACKET',
          'LCURLBRACE',
          'RCURLBRACE',
          'PIPE',
          'AMPER',
          'COMMA',
          'CARAT',
          'BANG',
          'DOT',
          'QUESTION',
          'NOTEQUAL',
          'ISEQUAL',
          'GREATEQUAL',
          'LESSEQUAL',
          'GREATERTHAN',
          'LESSTHAN',
          'IF',
          'ELSE',
          'FOR',
          'WHILE',
          'IN',
          'DO',
          'NEXT',
          'BREAK',
          'RETURN',
          'FUNCTION',
          'NUMBER_LITERAL',
          'STRING_LITERAL',
          'IDENTIFIER',
          'VOID',
          'NULL',
          'LOGICAL',
          'INTEGER',
          'FLOAT',
          'STRING',
          'OBJECT',
          'NUMERIC',
          'DOLLASIGN',
          'OBJECT_CLASS_SPEC',
          'BOOL_LITERAL',
] + list(reserved.values())

# THESE (short, regex-only token rules) HAPPEN SECOND
#t_STRING_LITERAL = r'"[a-zA-Z_][a-zA-Z0-9_]*"' stripped quotes below
#t_ELSE = r'else'
t_QUESTION = r'\?'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_MODULO = r'%'
t_SEMICOLON = r';'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLBRACE = r'\{'
t_RCURLBRACE = r'\}'
t_PIPE = r'\|'
t_AMPER = r'&'
t_COMMA = r','
t_CARAT = r'\^'
t_BANG = r'!'
t_DOT = r'\.'
t_NOTEQUAL = r'!\='
t_GREATEQUAL = r'\>\='
t_LESSEQUAL = r'\<\='
t_GREATERTHAN = r'\>'
t_LESSTHAN = r'\<'
t_DOLLASIGN = r'\$' #ty_dollasign
t_ignore = ' \t'

# THESE (function defs) HAPPEN FIRST (are applied first)
# a regex rule with some action code

def t_BOOL_LITERAL(t):
    r'[TF]'
    return t

def t_IF(t):
    r'if'
    return t

def t_FOR(t):
   r'for'
   return t

def t_WHILE(t):
    r'while'
    return t

def t_INTEGER(t):
    r'integer\$?'
    return t

def t_IN(t):
    r'in'
    return t

def t_DO(t):
    r'do'
    return t

def t_NEXT(t):
    r'next'
    return t

def t_BREAK(t):
    r'break'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_ISEQUAL(t):
    r'\=\='
    return t

def t_EQUAL(t):
    r'\='
    return t

def t_ELSE(t):
    r'else'
    return t

def t_EXPONENT(t):
    r'[eE][+\-]?\d+'
    return t

def t_VOID(t):
    r'void\$?'
    return t

def t_NULL(t):
    r'null\$?'
    return t

def t_LOGICAL(t):
    r'logical\$?'
    return t

def t_FLOAT(t):
    r'float\$?'
    return t

def t_STRING(t):
    r'string\$?'
    return t

def t_OBJECT(t):
    r'object\$?'
    return t

def t_NUMERIC(t):
    r'numeric\$?'
    return t

def t_NUMBER_LITERAL(t):
    r'[0-9]*\.[0-9]+|[0-9]+'
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"[a-zA-Z_][a-zA-Z0-9_]*"'
    t.value = t.value.strip('\"')
    return t

def t_OBJECT_CLASS_SPEC(t):
    r'<[a-zA-Z_]+[a-zA-Z0-9_]*>'
    t.value = t.value.strip('\<')
    t.value = t.value.strip('\>')
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_]+[a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# test it out
data = ''
#data = '3 + 4 e-44 "hello" hi,^!? = == != <> <= ]){} if do while. <Object> object float$ c(5,6) carrot ace'

# give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break # done
    print(tok)
