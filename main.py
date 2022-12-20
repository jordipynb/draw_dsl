from grammar import *

input1 = open(f"tester/test0.txt").read() # DONE
input2 = open(f"tester/test1.txt").read() # DONE
input3 = open(f"tester/test2.txt").read() # DONE

input = input1 + '\n' + input2 + '\n' + input3

ast = parser.parse(input,lexer=lexer)
if ast:
	print(ast) 
else:
	raise RuntimeError("AST Incomplete")
ast.evaluate()