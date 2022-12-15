from grammar import*

input = '''shape triangle
	pencil red
	fill yellow
	axiom { 
		right 90 
		line 400 
		left 90
		line 300 
		left 126.9
		line 500
		call_shape triangle 
		call_rule follow
	}
	rule first {
		base: nill
		line 300
		iter 0
	}
	depth 5 
shape triangle
	pencil red
	fill yellow
	axiom { 
		right 90
		line 400
		left 90
		line 300
		left 126.9
		line 500
		call_shape triangle
		call_rule follow
	}
	rule follow {
		base: nill
		line 300
	}
	depth 5

draw triangle 1 , 1'''

# Give the lexer some input
# Build the lexer
# lexer = lex.lex(optimize=1)
lexer = lex.lex()
lexer.input(input)
 
# Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)

# # parser = yacc.yacc(optimize=1)
parser = yacc.yacc()
parser.parse(input,lexer=lexer)