from exceptions import RuleNotDefined, ShapeNotDefined
from ply import yacc as yacc
from utils import *
import os
import errno

try:
    os.mkdir('parser')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

shape_scope:list[Shape] = []
locals_rules:list[Rule] = []
draws:list[Draw] = []

def p_scene(p):

	'''scene : draws_instruction'''
	p[0] = Scene(draws)
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
	else: # Si es una lista
		if p.slice[2].type == 'shape':
			shape_scope.append(p[2])
		else:
			draws.append(p[2])

def p_draw(p):
	'''draw : DRAW ID number COMMA number
	        | DRAW ID
			| DRAW NILL'''
	if p[2] == 'nill':
		p[0] = Draw(Nill(), Value(0), Value(0))
	else:
		id = p[2]
		for shape in shape_scope:
			if shape and shape.name == id: 
				try:
					x = p[3]
					y = p[5]
				except:
					x = Value(0)
					y = Value(0)
				p[0] = Draw(shape,x,y)
				break
		else:
			token = p.slice[2]
			p[0] = Draw(token,Value(0),Value(0))
			print(ShapeNotDefined(token).warning_message)
			# print(f'Warning: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no es una figura definida')


def p_shape(p):
	'''shape : SHAPE ID O_KEY pencil rules_locals axiom C_KEY'''
	if len(shape_scope) > 0:
		for shape in shape_scope:
			if shape.name == p[2]:
				token = p.slice[2]
				print(ShapeNotDefined(token).warning_message)
				# print(f'Warning: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} ya es una figura')
				p[0] = Shape(None,p[4],p[5],p[6])
				return
	global locals_rules
	locals_rules = []
	p[0] = Shape(p[2],p[4],p[5],p[6])

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
		p[0] = p[1]

def p_rules(p):
	'''rules  : rules rule
	          | rule'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [*p[1],p[2]]

def p_rule(p):
	'''rule  : RULE ID O_PAR ID C_PAR O_KEY instructions C_KEY'''
	for rule in locals_rules:
		if rule.name == p[2]:
			token = p.slice[2]
			print(RuleNotDefined(token))
			# print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} ya es una regla')
			# return
	p[0] = Rule(p[2], p[4], p[7], p.slice[2])
	locals_rules.append(p[0])

def p_instructions(p):
	'''instructions : instructions instruction
				    | instruction '''
	if len(p)==2:
		p[0] = [p[1]]
	else:
		p[0] = [*p[1],p[2]]

def p_instruction(p):
	'''instruction	:	instruction_base
					|	IF conditions O_KEY instructions C_KEY			
					|	IF conditions O_KEY instructions C_KEY ELSE O_KEY instructions C_KEY
					|	WHILE conditions O_KEY loop_instructions C_KEY'''
	if p[1] == 'if':
		if len(p) > 6: p[0] = If(p[2],p[4],p[8])
		else:  p[0] = If(p[2],p[4])
	elif p[1] == 'while': p[0] = While(p[2],p[4])
	else: p[0] = p[1]

def p_instruction_base(p):
	'''instruction_base	: LEFT  expression   
						| RIGHT expression     
						| LINE  expression   
						| JUMP  expression COMMA expression      
						| NILL  
						| PUSH		
						| POP 
						| CALL_SHAPE ID
						| CALL_RULE ID O_PAR expression C_PAR
						| ID EQUAL expression
						| ID EQUAL condition
						| ID EQUAL GET_X
						| ID EQUAL GET_Y
						| SET_X expression 
						| SET_Y expression 
						| SET_PENCIL ID '''
	if p[1] == 'left':
		p[0] = LeftInstruction(p[2])
	elif p[1] == 'right':
		p[0] = RightInstruction(p[2])
	elif p[1] == 'line':
		p[0] = LineInstruction(p[2])
	elif p[1] == 'jump': p[0] = JumpInstruction(p[2], p[4])
	elif p[1] == 'nill': p[0] = Nill()
	elif p[1] == 'push': p[0] = PushInstruction()
	elif p[1] == 'pop':  p[0] = PopInstruction()
	elif p[1] == 'call_shape': 
		for shape in shape_scope:
			if shape and shape.name == p[2]: 
				p[0] = CallShapeInstruction(shape)
				break
		else:
			token = p.slice[2]
			print(ShapeNotDefined(token))
			# print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no es una figura definida')
	elif p[1] == 'set_x': p[0] = SetX(p[2])
	elif p[1] == 'set_y': p[0] = SetY(p[2])
	elif p[1] == 'set_pencil': p[0] = SetPencil(p[2])
	elif p[3] == 'get_x': p[0] = GetX(p[1])
	elif p[3] == 'get_y': p[0] = GetY(p[1])
	elif p[1] == 'call_rule': p[0] = CallRuleInstruction(p.slice[2],p[4])
	else: p[0] = Assign(p[1],p[3])

def p_loop_instruction(p):
	'''loop_instruction		: instruction_base
							| BREAK
							| IF conditions O_KEY loop_instructions  C_KEY
							| IF conditions O_KEY loop_instructions C_KEY ELSE O_KEY loop_instructions C_KEY
							| WHILE conditions O_KEY loop_instructions C_KEY'''
    
	if p[1] == 'if':
		if len(p) > 6: p[0] = If(p[2],p[4],p[8])
		else:  p[0] = If(p[2],p[4])
	elif p[1] == 'break': p[0] = Break(p.slice[1])
	elif p[1] == 'while': p[0] = While(p[2],p[4])
	else: p[0] = p[1]

def p_loop_instructions(p):
	'''loop_instructions 	: loop_instructions loop_instruction
				    		| loop_instruction '''
	if len(p)==2:
		p[0] = [p[1]]
	else:
		p[0] = [*p[1],p[2]]	

def p_condition(p):
	'''condition    : expression GREATER expression
					| expression MENOR expression
					| expression EQUAL_EQUAL expression
					| FALSE
					| TRUE
					| NOT condition'''
	if p[1] == 'true': p[0] = TrueCondition()
	elif p[1] == 'false': p[0] = FalseCondition()
	elif p[2] == '>' : p[0] = GreaterCondition(p[1],p[3])
	elif p[2] == '<' : p[0] = MenorCondition(p[1],p[3])
	elif p[2] == '==': p[0] = EqualCondition(p[1],p[3])
	else: p[0] = NotCondition(p[2])

def p_conditions(p):
	'''conditions	: conditions AND condition
					| conditions OR condition
					| condition
					| O_PAR conditions C_PAR
					| NOT O_PAR conditions C_PAR ''' 
	if len(p)>2:
		if p[2] == 'and': p[0]=AndCondition(p[1],p[3])
		elif p[2] == 'or': p[0]=OrCondition(p[1],p[3])
		elif p[1] == 'not': p[0]=NotCondition(p[3])
		elif p[1] == '(' : p[0]=p[2]
	else: p[0]=p[1]

def p_expression(p):
	'''expression   : expression SUM term
					| expression SUB term
					| term	'''
    
	if len(p) > 2:
		if p[2] == '+': p[0] = SumExpr(p[1],p[3])
		elif p[2] == '-': p[0] = SubExpr(p[1],p[3])
	else : p[0] = p[1]

def p_term(p):
	'''term	:	term MUL pow
			|	term DIV pow
			|	pow'''
	if len(p) > 2:
		if p[2] == '*': p[0] = MultExpr(p[1],p[3])
		elif p[2] == '/': p[0] = DivExpr(p[1],p[3])
	else : p[0] = p[1]

def p_pow(p):
	'''pow	: pow POW factor
			| factor'''
	if len(p) > 2:
		p[0] = PowExpr(p[1],p[3])
	else : p[0] = p[1]

def p_factor(p):
	'''factor	: number
				| ID
				| O_PAR expression C_PAR
				| FUNC O_PAR expression C_PAR'''
	if p.slice[1].type == 'ID': p[0] = Factor(p.slice[1])
	elif p[1] == '(': p[0] = p[2]
	elif len(p) > 4 : p[0] = Function(functions[p[1]],p[3],p.slice[1])
	else : p[0] = p[1]

def p_number(p):
	'''number 	: FLOAT
				| SUB FLOAT'''
	if len(p) == 2: 
		if isinstance(p[1],float): p[0] = Value(p[1])
		else: p[0] = Value(constants[p[1]])
	else:
		if isinstance(p[2],float): p[0] = Value(-1*p[2])
		else: p[0] = Value(-1*constants[p[2]])

def p_axiom(p):
	'''axiom  : AXIOM O_KEY instructions C_KEY'''
	p[0] = Axiom(p[3])

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



# SE REPORTA LOS ERRORES EN COMPILACION YA EN RUNTIME SE DA EXCEPCIONES
# COMPROBAR Q LOS ID DE FILL Y PENCIL SON COLORES, TAMBIEN ACEPTAR HEXADECIMALES CON EXPRESIONES REGULARES
# CHEKEAR LA GRAMATICA EN GRAN MEDIDA HASTA PARTIRLA O ENCONTRAR UNA SECUENCIA Q LA GENERA Y NO DEBA
# HACER EL FLUJO DEL CODIGO --
#                            |
#   INPUT -> COMANDO DE PARADA DE ESCRITURA -> MOSTRAR SECUENCImmmmnmnA DE ERRORES ORDENADAS Y PREGUNTAR SI ESTA SEGURO DE RUNEAR EL CODE
#   YES -> EVALUAR EL AST A PESAR DE LOS ERRORES (SI DEJA, CUANDO ENCONTRAMOS NONE LANZAR ERRORES SEMANTICOS POR ORDEN), SINO DEJA 
#          ES XQ HUBO ERRORES DE SYNTAXIS Y EL LOS LANZA SOLO
#   NO  -> CONTINUAR CON EL INPUT HASTA Q VUELVA A PONER COMANDO DE PARADA
#   SI HAY ERRORES RUNTIME NO ES NUESTRO PROBLEMA PERO PODRIAMOS PONERLOS NOSOTROS POR SI JODE LA PINTURA                          
parser = yacc.yacc(outputdir='./parser/')