
class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]