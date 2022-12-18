from grammar import *

input = '''shape triangles {
	pencil red
	fill yellow
	axiom { 
		right 90 
		line 400 
		left 90
		line 300 
		left 126
		line 500 
	}
	rule first {
		base : nill 
		line 300
	}
	rule fitness {
		base : nill
		line 300
		call_rule fitness
	}
}
shape triangle {
	axiom { 
		right 90
		line 400
		left 90
		line 300
		left 126
		line 500
		call_shape triangles
		call_rule follow
	}
	rule follow {
		base { 
			line 400
			left 90
			line 300
		}
		line 300
	}
	depth 6
}
draw triangles 1 , 1
draw nill
draw triangle 40 , 40'''

# Give the lexer some input
# Build the lexer
# lexer = lex.lex(optimize=1)
#lexer.input(input)
 
# Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)

# # parser = yacc.yacc(optimize=1)
ast = parser.parse(input,lexer=lexer)
if ast:
	print(ast) 
else:
	raise RuntimeError("AST Incomplete")
ast.evaluate()