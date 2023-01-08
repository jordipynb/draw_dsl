from ply.lex import LexToken
from utils import token_info
    
class SemanticException(Exception):
    def __init__(self, msg:str = "Unknow exception") -> None:
        self.msg = msg
        
    def __str__(self) -> str:
        return f"Semantic Error: {self.msg}"

class IdentifierNotDefined(SemanticException):
    def __init__(self, token: LexToken) -> None:
        value, line, column = token_info(token)
        msg = f"Identifier '{value}' in line '{line}' and column '{column}' isn't defined"
        super().__init__(msg)
        
class ShapeNotDefined(SemanticException):
    def __init__(self, token: LexToken) -> None:
        value, line, column = token_info(token)
        msg = f"Shape '{value}' in line '{line}' and column '{column}' isn't defined"
        super().__init__(msg)

class RuleNotDefined(SemanticException):
    def __init__(self, token: LexToken) -> None:
        value, line, column = token_info(token)
        msg = f"Rule '{value}' in line '{line}' and column '{column}' isn't defined"
        super().__init__(msg)
        
class BreakException(SemanticException):
    def __init__(self) -> None:
        msg = "'break' instruction must be defined inside a loop"
        super().__init__(msg)