import ply.lex as lex

reserved = {
    'for': 'FOR',
    'do': 'DO',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE'
}

tokens = [
    'LPAREN', 'RPAREN', 'Identificador'
] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'Identificador')
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()