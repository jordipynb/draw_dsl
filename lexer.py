from ply import lex as lex
import math

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
    'nill'       : 'NILL',
    'axiom'      : 'AXIOM',
    'rule'       : 'RULE',
    'jump'       : 'JUMP',
    'push'       : 'PUSH',
    'pop'        : 'POP',
    'while'      : 'WHILE',
    'if'         : 'IF',
    'not'        : 'NOT',
    'else'       : 'ELSE',
    'and'        : 'AND',
    'or'         : 'OR',
    'true'       :'TRUE',
    'false'      :'FALSE',
    'get_x'      :'GET_X',
    'set_x'      :'SET_X',
    'get_y'      :'GET_Y',
    'set_y'      :'SET_Y',
    'set_pencil' :'SET_PENCIL',
    'break'      :'BREAK'
 }
functions={'sin':lambda x: math.sin(x),'cos': lambda x : math.cos(x)}

constants={'pi':math.pi,'e':math.e}

tokens  = ['O_KEY', 'C_KEY', 'O_PAR', 'FUNC', 'C_PAR','FLOAT', 'COMMA', 'ID','SUM','SUB','DIV','MUL','GREATER','MENOR','EQUAL','EQUAL_EQUAL','POW'] + list(reserved.values())

# Regular expression rules for simple tokens
t_O_KEY       = r'\{'
t_C_KEY       = r'\}'
t_O_PAR       = r'\('
t_C_PAR       = r'\)'
t_COMMA       = r','
t_SUM         = r'\+'
t_SUB         = r'-'
t_DIV         = r'/'
t_MUL         = r'\*'
t_GREATER     = r'>'
t_MENOR       = r'<'
t_EQUAL       = r'='
t_EQUAL_EQUAL = r'=='
t_POW         = r'\^'

# A regular expression rule with some action code
def t_FLOAT(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except:
        print(f'Error en línea {t.lineno}!! Token: {t.value} debe ser un entero') 
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')# Check for reserved words
    if t.type== 'ID' and (t.value == 'sin' or t.value == 'cos'):
        t.type = 'FUNC'
    if t.type== 'ID' and (t.value == 'e' or t.value == 'pi'):
        t.type = 'FLOAT'
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