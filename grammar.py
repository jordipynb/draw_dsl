from lexer import *
from ply import yacc as yacc

# Definición de la gramática
def p_scene(t):
	'''scene    : draws_instruction scene
	            | draws_instruction
				| shapes'''
	if len(t) == 3:
		shapes = t[2][0] 
		for shape in shapes:
			if shape.name in t[1][0]:
				raise SyntaxError(f"{shape.name} no es figura unica")
		t[2][0].union(t[1][0])
		t[0] = t[2].insert(0, t[1])
	else:
		t[0] = [t[1]]


def p_draws_instruction(t):
	'''draws_instruction : shapes draws'''

def p_shapes(t):
	'''shapes : shape shapes 
	          | shape'''

def p_draws(t):
	'''draws  : draw draws
			  | draw'''

def p_draw(t):
	'''draw : DRAW ID INT COMMA INT'''

def p_shape(t):
	'''shape : SHAPE ID pencil'''

	
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

def p_depth(t):
	'''depth  : DEPTH INT'''

def p_loops(t):
	'''loops  : ITER INT C_KEY
			  | C_KEY'''

def p_error(t):
    raise SyntaxError(f'WARNING!!! Syntax Error "{t.value}" en la línea {t.lineno}')