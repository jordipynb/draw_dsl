from ply.lex import LexToken
from utils import token_info

class EmptyError(Exception):
    pass
class SemanticException(Exception):
    def __init__(self, msg: str = "Unknow exception") -> None:
        self.msg = msg

    @property
    def warning_message(self):
        return f"Warning: {self.msg}"
    
    @property
    def runtime_error(self):
        return f"Runtime Error: {self.msg}"

    def __str__(self) -> str:
        return f"Semantic Error: {self.msg}"

class ColorNotDefined(SemanticException):
    def __init__(self, value) -> None:
        msg = f"Color '{value}' isn't a valid color"
        super().__init__(msg)

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
    def __init__(self, token: LexToken) -> None:
        value, line, column = token_info(token)
        msg = f"'break' instruction in line {line} and column {column} must be defined inside a loop"
        super().__init__(msg)
        
class CommandNotDefined(Exception):
    def __init__(self, command:str) -> None:
        self.command = command
    
    def __str__(self) -> str:
        return f"Command '{self.command}' is not defined"
