
from grammar import *
from semantics.core import check_semantics


class System:
    def run_tester(self, tester_name):
        input = open(f"tester/{tester_name}.txt").read()
        
        ast:Scene = parser.parse(input,lexer=lexer)
        if not ast:
            raise RuntimeError("AST Incomplete")
        if check_semantics(ast):
            ast.evaluate()