from grammar import *

# input = open(f"tester/test0.txt").read() # DONE
# input = open(f"tester/test1.txt").read() # NO
# input = open(f"tester/test2.txt").read() # NO
# input = open(f"tester/test3.txt").read() # NO
# input = open(f"tester/test4.txt").read() # NO
# input = open(f"tester/test5.txt").read() # NO
# input = open(f"tester/test6.txt").read() # NO


# input = open(f"tester/test15.txt").read() # DONE
# input = open(f"tester/test16.txt").read() # DONE
# input = open(f"tester/test17.txt").read() # NO
# input = open(f"tester/test18.txt").read() # DONE

ast = parser.parse(input,lexer=lexer)
if ast:
	print(ast) 
else:
	raise RuntimeError("AST Incomplete")
ast.evaluate()