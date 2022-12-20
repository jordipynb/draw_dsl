from ply import yacc as yacc
from lexer import *
from utils import *

lexer = lex.lex()
errors_list = []
shape_scope:list[Shape] = []
locals_rules:list[Rule] = []
draws:list[Draw] = []

# Definición de la gramática
def p_scene(p):
	'''scene : draws_instruction'''
	p[0] = Scene(draws, errors_list)
	global shape_scope, locals_rules
	del shape_scope, locals_rules

def p_draws_instruction(p):
	'''draws_instruction : draws_instruction shape
	                     | draws_instruction draw
						 | shape
						 | draw'''
	if len(p) == 2:
		if p.slice[1].type == 'shape':
			shape_scope.append(p[1])
		else:
			draws.append(p[1])
	else:
		if p.slice[2].type == 'shape':
			shape_scope.append(p[2])
		else:
			draws.append(p[2])

def p_draw(p):
	'''draw : DRAW ID INT COMMA INT
	        | DRAW ID
			| DRAW NILL'''
	if p[2] == 'nill':
		p[0] = Draw(Nill())
		return
	for shape in shape_scope:
		if shape and shape.name == p[2]: 
			p[0] = Draw(shape,p[3],p[5]) if len(p) == 6 else Draw(shape)
			return
	token = p.slice[2]
	print(f'Warning: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no es una figura definida')

def p_shape(p):
	'''shape : SHAPE ID O_KEY pencil rules_locals axiom C_KEY'''
	if len(shape_scope) > 0:
		for shape in shape_scope:
			if shape.name == p[2]:
				token = p.slice[2]
				print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} ya es una figura')
				return
	global locals_rules
	locals_rules = []
	p[0] = Shape(p[2],p[4],p[6])

colors = ['red','blue','yellow','green','magenta'] 
r'\#[0-9a-f]{6}'
# Comprobar q el ID es un color
def p_pencil(p):
	'''pencil : PENCIL ID
			  | '''
	if len(p) > 2:
		p[0] = p[2]
	else:
		p[0] = 'black'

def p_rules_locals(p):
	'''rules_locals : rules
	                | '''
	if len(p) == 2:
		for i,rule in enumerate(locals_rules):
			for j, instuction in enumerate(rule.instructions):
				if isinstance(instuction, CallableRule):
					value = instuction.search_rule(locals_rules)
					if isinstance(value, LexToken):
						print(f'SemanticError: "{value.value}" en la línea {value.lineno}, columna {find_column(value)} no es una regla definida!')
					else:
						locals_rules[i].instructions[j] = value

def p_rules(p):
	'''rules  : rule rules
	          | rule'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1],*p[2]]

def p_rule(p):
	'''rule  : RULE ID O_KEY base instructions loop C_KEY'''
	for rule in locals_rules:
		if rule.name == p[2]:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} ya es una regla')
			return
	p[0] = Rule(p[2], p[4], p[5], p[6])
	locals_rules.append(p[0])

def p_base(p):	
	'''base : BASE TWO_POINT instruction_base
	        | BASE O_KEY instructions_base C_KEY'''
	if p[2] == ':': p[0] = [p[3]]
	else : p[0] = p[3]

def p_instructions_base(p):
	'''instructions_base : instruction_base instructions_base
				    	 | instruction_base '''
	if len(p)==2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1],*p[2]]

def p_instruction_base(p):
	'''instruction_base  : LEFT  INT   
						 | RIGHT INT     
						 | LINE  INT   
						 | JUMP  INT COMMA INT      
						 | NILL  
						 | PUSH  INT COMMA INT 		
						 | POP 
						 | CALL_SHAPE ID'''
	if p[1] == 'left':
		if 0 <= p[2] and p[2] <= 180: p[0] = LeftInstruction(p[2])
		else:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe estar en rango [0, 180]')
	elif p[1] == 'right':
		if 0 <= p[2] and p[2] <= 180: p[0] = RightInstruction(p[2])
		else:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe estar en rango [0, 180]')
	elif p[1] == 'line':
		if p[2] > 0: p[0] = LineInstruction(p[2])
		else:	
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe ser positivo!')
	elif p[1] == 'jump': p[0] = JumpInstruction(p[2], p[4])
	elif p[1] == 'nill': p[0] = Nill()
	elif p[1] == 'push': p[0] = PushInstruction(p[2], p[4])
	elif p[1] == 'pop':  p[0] = PopInstruction()
	else: # es un call_shape
		for shape in shape_scope:
			if shape and shape.name == p[2]: 
				p[0] = CallShapeInstruction(shape)
				break
		else:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no es una figura definida')

def p_instructions(p):
	'''instructions : instruction instructions
				    | instruction '''
	if len(p)==2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1],*p[2]]

def p_instruction(p):
	'''instruction  : instruction_base
	                | CALL_RULE ID'''
	if p[1] == 'call_rule':
		for rule in locals_rules:
			if rule and rule.name == p[2]: 
				p[0] = CallRuleInstruction(rule)
				break
		else: p[0] = CallableRule(p.slice[2])
	else: # es un instruction_base
		p[0] = p[1]

def p_loop(p):
	'''loop : ITER INT
			| '''
	if len(p)==3:
		if p[2] < 0:
			token = p.slice[2]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe ser no negativo!')
		else: p[0] = p[2]
	else: p[0] = 0

def p_axiom(p):
	'''axiom  : AXIOM O_KEY instructions_axiom C_KEY'''
	p[0] = Axiom(p[3])

def p_instructions_axiom(p):
	'''instructions_axiom : instruction_axiom instructions_axiom
	                      | instruction_axiom'''
	if len(p)==2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1],*p[2]]

def p_instruction_axiom(p):
	'''instruction_axiom  : instruction_base
	                      | CALL_RULE ID O_PAR INT C_PAR'''
	if p[1] == 'call_rule':
		if p[4] < 0:
			token = p.slice[4]
			print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} debe ser no negativo!')
		else:
			for rule in locals_rules:
				if rule and rule.name == p[2]: 
					p[0] = CallRuleInstruction(rule, depth=p[4])
					break
			else:
				token = p.slice[2]
				print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no es una regla definida!')
	else: # es un instruction_base
		p[0] = p[1]

def p_error(p):
	if p:
		if p.value in reserved:
			token = f"keyword '{p.value}' at line {p.lineno}, column {find_column(p)}"
		else:
			token = f"'{p.value}' at line {p.lineno}, column {find_column(p)}"
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
# COMPROBAR Q LOS ID DE FILL Y PENCIL SON COLORES, TAMBIEN ACEPTAR HEXADECIMALES CON EXPRESIONES REGULARES
# CHEKEAR LA GRAMATICA EN GRAN MEDIDA HASTA PARTIRLA O ENCONTRAR UNA SECUENCIA Q LA GENERA Y NO DEBA
# HACER EL FLUJO DEL CODIGO --
#                            |
#   INPUT -> COMANDO DE PARADA DE ESCRITURA -> MOSTRAR SECUENCIA DE ERRORES ORDENADAS Y PREGUNTAR SI ESTA SEGURO DE RUNEAR EL CODE
#   YES -> EVALUAR EL AST A PESAR DE LOS ERRORES (SI DEJA, CUANDO ENCONTRAMOS NONE LANZAR ERRORES SEMANTICOS POR ORDEN), SINO DEJA 
#          ES XQ HUBO ERRORES DE SYNTAXIS Y EL LOS LANZA SOLO
#   NO  -> CONTINUAR CON EL INPUT HASTA Q VUELVA A PONER COMANDO DE PARADA
#   SI HAY ERRORES RUNTIME NO ES NUESTRO PROBLEMA PERO PODRIAMOS PONERLOS NOSOTROS POR SI JODE LA PINTURA                          
parser = yacc.yacc()