from semantics.visitors.validate_visitor import ContextValidatorVisitor
import exceptions
def check_semantics(ast):
    visitor = ContextValidatorVisitor()
    visitor.visit(ast)
    if visitor.has_errors:
        visitor.show_errors
        return False
    return True