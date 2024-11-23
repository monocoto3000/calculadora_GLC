import ply.lex as lex
from collections import defaultdict

tokens = (
    'DECIMAL',
    'ENTERO',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'LPAREN',
    'RPAREN',
)

t_SUMA    = r'\+'
t_RESTA   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

token_frequencies = defaultdict(int)
token_values = []

def t_DECIMAL(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    token_frequencies['DECIMAL'] += 1
    token_values.append(('DECIMAL', t.value))
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    token_frequencies['ENTERO'] += 1
    token_values.append(('ENTERO', t.value))
    return t

def t_error(t):
    print(f"Caracter invalido '{t.value[0]}'")
    t.lexer.skip(1)

t_ignore = ' \t'

lexer = lex.lex()

def analyze_expression(expression):
    token_frequencies.clear()
    token_values.clear()
    
    lexer.input(expression)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type in ['SUMA', 'RESTA', 'MULT', 'DIV', 'LPAREN', 'RPAREN']:
            token_frequencies[tok.type] += 1
            token_values.append((tok.type, tok.value))
    
    return token_values, dict(token_frequencies)