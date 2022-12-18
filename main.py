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

ast = parser.parse(input,lexer=lexer)
if ast:
	print(ast) 
else:
	raise RuntimeError("AST Incomplete")
ast.evaluate()