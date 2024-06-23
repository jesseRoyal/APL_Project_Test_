import ply.lex as lex

# Token definitions
tokens = (
    'HASH',
    'DOT',
    'LPAREN',
    'RPAREN',
    'VARIABLE',
)

# Token regular expressions
t_HASH = r'\#'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Variable token
def t_VARIABLE(t):
    r'[a-z]'
    return t

# Ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
