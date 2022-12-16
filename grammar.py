from ast import keyword
from lexer import *
from ply import yacc as yacc
from utils import *

# Definición de la gramática
def p_scene(t):
	'''scene    : draws_instruction scene
	            | draws_instruction
				| shapes'''

def p_draws_instruction(t):
	'''draws_instruction : shapes draws'''

def p_shapes(t):
	'''shapes : shape shapes 
	          | shape'''

def p_draws(t):
	'''draws  : draw draws
			  | draw'''

def p_draw(t):
	'''draw : DRAW ID INT COMMA INT
	        | DRAW ID
	        | DRAW NILL'''

def p_shape(t):
	'''shape : SHAPE ID O_KEY pencil'''

	
def p_pencil(t):
	'''pencil : PENCIL ID fill
			  | fill'''

def p_fill(t):
	'''fill   : FILL ID axiom
			  | axiom'''

def p_axiom(t):
	'''axiom  : AXIOM O_KEY instructions C_KEY rules'''

def p_rules(t):
	'''rules  : rule rules
			  | depth'''

def p_rule(t):
	'''rule  : RULE ID O_KEY base instructions loops'''

def p_base(t):
	'''base : BASE TWO_POINT instruction_base 
			| BASE O_KEY instructions_base C_KEY'''

def p_instructions(t):
	'''instructions : instruction instructions
				    | instruction '''

def p_instruction(t):
	'''instruction  : LEFT  INT 
				    | LEFT FLOAT    
					| RIGHT INT 
					| RIGHT FLOAT     
					| LINE  INT   
					| JUMP  INT COMMA INT      
					| NILL  
					| PUSH  INT COMMA INT 		
					| POP 
					| CALL_RULE ID
					| CALL_SHAPE ID'''

def p_instruction_base(t):
	'''instruction_base  : LEFT  INT 
						 | LEFT FLOAT    
						 | RIGHT INT 
						 | RIGHT FLOAT     
						 | LINE  INT   
						 | JUMP  INT COMMA INT      
						 | NILL  
						 | PUSH  INT COMMA INT 		
						 | POP '''

def p_instructions_base(t):
	'''instructions_base : instruction_base instructions_base
				    	 | instruction_base '''

def p_loops(t):
	'''loops  : ITER INT C_KEY
			  | C_KEY'''
	if len(t)==2:
		t[0] = 0
	else:
		if t[2] < 0:
			print(f'Semantic error: "{t.slice[2].value}" en la línea {t.slice[2].lineno} debe ser mayor o igual que cero!')
		t[0] = t[2]

def p_depth(t):
	'''depth  : DEPTH INT C_KEY
	          | C_KEY'''
	if len(t)==2:
		t[0] = 0
	else:
		if t[2] < 0:
			print(f'Semantic error: "{t.slice[2].value}" en la línea {t.slice[2].lineno} debe ser mayor o igual que cero!')
			return
		t[0] = t[2]


def p_error(p):
	if p == None:
		token = "EOF"
	else:
		if p.value in reserved:
			token = f"keyword '{p.value}' en la línea {p.lineno}"
		else:
			token = f"'{p.value}' en la línea {p.lineno}"
	print(f"Syntax error: No se esperaba {token}")