# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('AXIOM', 'BASE', 'CALL_RULE', 'CALL_SHAPE', 'COMMA', 'C_KEY', 'DEPTH', 'DRAW', 'FILL', 'FLOAT', 'ID', 'INT', 'ITER', 'LEFT', 'LINE', 'NILL', 'O_KEY', 'PENCIL', 'RIGHT', 'RULE', 'SHAPE', 'TWO_POINT'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_FLOAT>\\d+\\.\\d+)|(?P<t_INT>-\\d+ | \\d+)|(?P<t_ID>[a-zA-Z][a-zA-Z_0-9]*)|(?P<t_newline>\\n+)|(?P<t_ignore_COMMENT>\\#.*)|(?P<t_O_KEY>\\{)|(?P<t_C_KEY>\\})|(?P<t_TWO_POINT>:)|(?P<t_COMMA>,)', [None, ('t_FLOAT', 'FLOAT'), ('t_INT', 'INT'), ('t_ID', 'ID'), ('t_newline', 'newline'), (None, None), (None, 'O_KEY'), (None, 'C_KEY'), (None, 'TWO_POINT'), (None, 'COMMA')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
