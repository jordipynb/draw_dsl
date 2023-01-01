from grammar import *
from semantics.visitors import FormatVisitor, SemanticCheckerVisitor

# input = open(f"tester/test0.txt").read() # DONE
# input = open(f"tester/test1.txt").read() # DONE
# input = open(f"tester/test2.txt").read() # DONE
# input = open(f"tester/test3.txt").read() # DONE
# input = open(f"tester/test4.txt").read() # DONE
# input = open(f"tester/test5.txt").read() # DONE
# input = open(f"tester/test6.txt").read() # DONE


# input = open(f"tester/test15.txt").read() # DONE
# input = open(f"tester/test16.txt").read() # DONE
# input = open(f"tester/test17.txt").read() # DONE
# input = open(f"tester/test18.txt").read() # DONE


# Lele testers
input = open(f"tester/test19sem.txt").read()
# input = open(f"tester/test20sem_check_PencilColor.txt").read() # DONE
# input = open(f"tester/test20sem_check_CallRuleInstruction.txt").read() # DONE


ast:Scene = parser.parse(input,lexer=lexer)
if ast:
	print(ast) 
else:
	raise RuntimeError("AST Incomplete")
# ast.evaluate()
# print(f"{ast=}, {type(ast)=}")

semantic = SemanticCheckerVisitor()
asn = "Errors:"
errors = semantic.visit(ast)
errors = "\n".join(errors) if len(errors) > 0 else "No existen errores"
print(f"{asn}\n{errors}")
print(FormatVisitor().visit(ast))
