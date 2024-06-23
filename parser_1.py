import ply.yacc as yacc
from lexer import tokens

# Grammar rules for parsing
def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = ('var', p[1])

def p_expression_lambda(p):
    'expression : HASH VARIABLE DOT expression'
    p[0] = ('lambda', p[2], p[4])

def p_expression_application(p):
    'expression : LPAREN expression expression RPAREN'
    p[0] = ('apply', p[2], p[3])

def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Build the parser
parser = yacc.yacc()
