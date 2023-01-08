from grammar import *
from semantics.core import check_semantics

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
# input = open(f"tester/test19sem.txt").read()
# input = open(f"tester/test20sem_check_PencilColor.txt").read() # DONE
input = open(f"tester/test21_check_CallRuleInstruction.txt").read() # DONE


ast:Scene = parser.parse(input,lexer=lexer)
if not ast:
	raise RuntimeError("AST Incomplete")
check_semantics(ast)
ast.evaluate()