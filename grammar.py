from ply import yacc as yacc
from lexer import *
from utils import *

lexer = lex.lex()
input = ""
errors_list = []
# Definición de la gramática
def p_scene(p):
	'''scene  : draws_instruction'''

def p_draws_instruction(p):
	'''draws_instruction : shape draws_instruction
	                     | draw draws_instruction
						 | shape
						 | draw'''

def p_draw(p):
	'''draw : DRAW ID INT COMMA INT
	        | DRAW ID
			| DRAW NILL'''

def p_shape(p):
	'''shape : SHAPE ID O_KEY pencil'''

	
def p_pencil(p):
	'''pencil : PENCIL ID fill
			  | fill'''

def p_fill(p):
	'''fill   : FILL ID axiom
			  | axiom'''

def p_axiom(p):
	'''axiom  : AXIOM O_KEY instructions C_KEY rules'''

def p_rules(p):
	'''rules  : rule rules
			  | depth'''

def p_rule(p):
	'''rule  : RULE ID O_KEY base instructions loops'''

def p_base(p):
	'''base : BASE TWO_POINT instruction_base 
			| BASE O_KEY instructions_base C_KEY'''

def p_instructions(p):
	'''instructions : instruction instructions
				    | instruction '''

def p_instruction(p):
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

def p_instruction_base(p):
	'''instruction_base  : LEFT  INT 
						 | LEFT FLOAT    
						 | RIGHT INT 
						 | RIGHT FLOAT     
						 | LINE  INT   
						 | JUMP  INT COMMA INT      
						 | NILL  
						 | PUSH  INT COMMA INT 		
						 | POP '''

def p_instructions_base(p):
	'''instructions_base : instruction_base instructions_base
				    	 | instruction_base '''

def p_loops(p):
	'''loops  : ITER INT C_KEY
			  | C_KEY'''
	if len(p)==2:
		p[0] = 0
	else:
		if p[2] < 0:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe ser mayor o igual que cero!')
			return
		p[0] = p[2]

def p_depth(p):
	'''depth  : DEPTH INT C_KEY
	          | C_KEY'''
	if len(p)==2:
		p[0] = 0
	else:
		if p[2] < 0:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe ser mayor o igual que cero!')
			return
		p[0] = p[2]


def p_error(p):
	if p:
        #errors_list.append("Erreur de syntaxe à la ligne %s"%(p.lineno))
		if p.value in reserved:
			token = f"keyword '{p.value}' en la línea {p.lineno}, columna {find_column(p)}"
		else:
			token = f"'{p.value}' en la línea {p.lineno}, columna {find_column(p)}"
		print(f"SyntaxError: Unexpected {token}")
		parser.errok()
	else:
		print("Unexpected end of input")

def find_column(t):
	last_cr = t.lexer.lexdata.rfind('\n' , 0, t.lexpos)
	if last_cr < 0:
		last_cr = 0
	column = (t.lexpos - last_cr)
	return column 

# SE REPORTA LOS ERRORES EN COMPILACION YA EN RUNTIME SE DA EXCEPCIONES
# SE DEBE PONER TAMBIEN LAS COLUMNAS
parser = yacc.yacc()