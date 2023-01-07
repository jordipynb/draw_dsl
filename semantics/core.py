from semantics.visitors.validate_visitor import ContextValidatorVisitor

def check_semantics(ast):
    visitor = ContextValidatorVisitor()
    visitor.visit(ast)
    visitor.show_errors