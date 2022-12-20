from ply import lex as lex

# List of token names.   This is always required
reserved = {
    'shape'      : 'SHAPE',
    'draw'       : 'DRAW',
    'pencil'     : 'PENCIL',
    'left'       : 'LEFT',
    'right'      : 'RIGHT',
    'line'       : 'LINE',
    'call_shape' : 'CALL_SHAPE',
    'call_rule'  : 'CALL_RULE',
    'base'       : 'BASE',
    'nill'       : 'NILL',
    'iter'       : 'ITER',
    'axiom'      : 'AXIOM',
    'rule'       : 'RULE',
    'jump'       : 'JUMP',
    'push'       : 'PUSH',
    'pop'        : 'POP',
 }

tokens  = ['O_KEY', 'C_KEY', 'O_PAR', 'C_PAR','INT', 'TWO_POINT', 'COMMA', 'ID'] + list(reserved.values())

# Regular expression rules for simple tokens
t_O_KEY       = r'\{'
t_C_KEY       = r'\}'
t_O_PAR       = r'\('
t_C_PAR       = r'\)'
t_TWO_POINT   = r':'
t_COMMA       = r','

# A regular expression rule with some action code
def t_INT(t):
    r'-\d+ | \d+'
    try:
        t.value = int(t.value)
    except:
        print(f'Error en línea {t.lineno}!! Token: {t.value} debe ser un entero') 
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')# Check for reserved words
    return t

# A string containing ignored characters (spaces, tabs and comment)
t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
# Error handling rule
def t_error(t):
    print(f'Token Inválido "{t.value[0]}" en la línea {t.lineno}')
    t.lexer.skip(1)