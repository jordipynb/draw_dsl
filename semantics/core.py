from semantics.visitors.validate_visitor import ContextValidatorVisitor

def check_semantics(ast):
    visitor = ContextValidatorVisitor()
    if not visitor.visit(ast):
        raise Exception(visitor.error)