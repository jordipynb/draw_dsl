import turtle
import _tkinter
from ply.lex import LexToken
from lexer import *

stack:list = []
lexer = lex.lex()

def find_column(t):
	last_cr = t.lexer.lexdata.rfind('\n' , 0, t.lexpos)
	if last_cr < 0:
		last_cr = 0
	column = (t.lexpos - last_cr)
	return column 
    
class Context:
    def __init__(self, parent=None):
        self.locals = {}
        self.parent = parent
        
    def create_children(self):
        return Context(self)
    
    def search(self, token:LexToken):
        for vname , value in self.locals.items():
            if vname == token.value:
                return value 
        if self.parent is None:
            print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no esta definido')
        return self.parent.search(token)
    
    def set_value(self, name, value):
        if name in self.locals.keys():
            self.locals[name]=value
            return True
        if self.parent: return self.parent.set_value(name,value)
        return False
        
class Node:
    def evaluate(self):
        raise NotImplementedError()
   
class ContextNode(Node):
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        raise NotImplementedError()    

class Rule(ContextNode):
    def __init__(self, name:str, param:str, instructions:list[ContextNode]):
        self.name = name
        self.instructions = instructions
        self.param=param

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        for elem in self.instructions:
            elem.evaluate(ttle, context, scope)

class Axiom(ContextNode):
    def __init__(self, instructions:list[ContextNode]):
        self.instructions = instructions

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        context = Context()
        for elem in self.instructions:
            elem.evaluate(ttle, context, scope)

class Shape(ContextNode):
    def __init__(self, name:str, pencil:str, rules:list[Rule], axiom:Axiom):
        self.stack = []
        self.name = name
        self.pencil = pencil
        self.axiom = axiom
        self.scope={}
        self.rules=rules

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        if self.rules:
            for rule in self.rules:
                self.scope[rule.name]=rule
        ttle.pencolor(self.pencil)
        self.axiom.evaluate(ttle, scope=self.scope)

class Nill(ContextNode):
    def __init__(self):
        pass

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        pass

class Break(ContextNode):
    def __init__(self):
        pass
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self

class Value(ContextNode):
    def __init__(self, value):
        self.value=value

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.value

class TrueCondition(ContextNode):
    def __init__(self):
       pass
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return True 

class FalseCondition(ContextNode):
    def __init__(self):
       pass
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return False  

class Draw(Node):
    def __init__(self, shape:Shape, x:Value, y:Value):
        self.shape = shape
        self.x = x
        self.y = y

    def evaluate(self):
        ttle = turtle.Turtle()
        ttle.left(90)
        ttle.up()
        ttle.goto(self.x.evaluate(ttle), self.y.evaluate(ttle))
        ttle.down()
        ttle.speed(0)
        ttle.pensize(2)
        self.shape.evaluate(ttle)
        ttle.hideturtle()

class Scene(Node):
    def __init__(self, draws:list[Draw], error_list:list[str]):
        self.draws = draws
        self.error_list = error_list

    def evaluate(self):
        try:
            for draw in self.draws:
                draw.evaluate()
            turtle.done()
        except turtle.Terminator: pass
        except _tkinter.TclError: pass

class LeftInstruction(ContextNode):
    def __init__(self, expression:ContextNode):
        self.expression = expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        angle=self.expression.evaluate(ttle, context, scope)
        ttle.left(angle)

class RightInstruction(ContextNode):
    def __init__(self, expression:ContextNode):
        self.expression = expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        angle=self.expression.evaluate(ttle, context, scope)
        ttle.right(angle)

class LineInstruction(ContextNode):
    def __init__(self, expression:ContextNode):
        self.expression = expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        distance=self.expression.evaluate(ttle, context, scope)
        ttle.forward(distance)

class PushInstruction(ContextNode):
    def __init__(self):
        pass

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        stack.append((ttle.xcor(), ttle.ycor(), ttle.heading()))

class PopInstruction(ContextNode):
    def __init__(self):
        pass

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict=None):
        pos_x, pos_y, angle = stack.pop()
        ttle.up()
        ttle.goto(pos_x, pos_y)
        ttle.setheading(angle)
        ttle.down()

class JumpInstruction(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
        self.x = exp1
        self.y = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        ttle.up()
        x=self.x.evaluate(ttle, context, scope)
        y=self.y.evaluate(ttle, context, scope)
        ttle.goto(x, y)
        ttle.down()

class Assign(ContextNode):
    def __init__(self, ID, expression:ContextNode):
        self.ID=ID
        self.expression=expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        name = self.ID
        value = self.expression.evaluate(ttle, context, scope)
        if not context.set_value(name, value):
            context.locals[name] = value

class SetX(ContextNode):
    def __init__(self, expression:ContextNode):
        self.expression = expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        ttle.setx(self.expression.evaluate(ttle, context, scope))

class SetY(ContextNode):
    def __init__(self, expression:ContextNode):
        self.expression = expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        ttle.sety(self.expression.evaluate(ttle,context,scope))

class GetX(ContextNode):
    def __init__(self, ID):
        self.ID = ID

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        name = self.ID
        value = ttle.xcor()
        if not context.set_value(name, value):
            context.locals[name] = value
    
class GetY(ContextNode):
    def __init__(self, ID):
        self.ID = ID

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        name = self.ID
        value = ttle.ycor()
        if not context.set_value(name, value):
            context.locals[name] = value  

class SetPencil(ContextNode):
    def __init__(self, ID):
        self.ID = ID
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        ttle.pencolor(self.ID) 

class If(ContextNode):
    def __init__(self, condition:ContextNode, if_body:list[ContextNode], else_body:list[ContextNode]=None):
       self.condition = condition
       self.if_body = if_body
       self.else_body = else_body

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        context = context.create_children()
        if self.condition.evaluate(ttle, context, scope):
            for instruction in self.if_body:
                result = instruction.evaluate(ttle, context, scope)
                if isinstance(result,Break): return result
        elif self.else_body:
            for instruction in self.else_body:
                result = instruction.evaluate(ttle, context, scope)
                if isinstance(result,Break): return result

class While(ContextNode):
    def __init__(self, condition:ContextNode, body:list[ContextNode]):
        self.condition = condition
        self.body = body

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        context=context.create_children()
        while self.condition.evaluate(ttle, context, scope):
            for instruction in self.body:
                if isinstance(instruction,Break) or isinstance(instruction.evaluate(ttle, context, scope),Break): return
                
class AndOperator(ContextNode):
    def __init__(self, prop1:ContextNode, prop2:ContextNode):
       self.prop1 = prop1
       self.prop2 = prop2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.prop1.evaluate(ttle, context, scope) and self.prop2.evaluate(ttle, context, scope)

class OrOperator(ContextNode):
    def __init__(self, prop1:ContextNode, prop2:ContextNode):
       self.prop1 = prop1
       self.prop2 = prop2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.prop1.evaluate(ttle, context, scope) or self.prop2.evaluate(ttle, context, scope)

class NotOperator(ContextNode):
    def __init__(self, condiction:ContextNode):
        self.condition = condiction

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return not self.condition.evaluate(ttle, context, scope)

class GreaterCondition(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
       self.exp1 = exp1
       self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) > self.exp2.evaluate(ttle, context, scope)

class MenorCondition(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
       self.exp1 = exp1
       self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) < self.exp2.evaluate(ttle, context, scope)

class EqualCondition(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
       self.exp1 = exp1
       self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) == self.exp2.evaluate(ttle, context, scope)             

class SumExpression(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) + self.exp2.evaluate(ttle, context, scope)
    
class SubExpression(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) - self.exp2.evaluate(ttle, context, scope)

class MulTerm(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) * self.exp2.evaluate(ttle, context, scope)

class DivTerm(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.exp1.evaluate(ttle, context, scope) / self.exp2.evaluate(ttle, context, scope)

class Pow(ContextNode):
    def __init__(self, exp1:ContextNode, exp2:ContextNode):
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return math.pow(self.exp1.evaluate(ttle, context, scope), self.exp2.evaluate(ttle, context, scope))

class Factor(ContextNode):
    def __init__(self, ID):
        self.ID = ID

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return context.search(self.ID)

class Function(ContextNode):
    def __init__(self, func, expression:ContextNode):
        self.expression = expression
        self.func = func

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        return self.func(self.expression.evaluate(ttle,context,scope))

class CallShapeInstruction(ContextNode):
    def __init__(self, shape:Shape):
        self.shape = shape

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        self.shape.evaluate(ttle)

class CallRuleInstruction(ContextNode):
    def __init__(self, token:LexToken, expression:ContextNode):
        self.id = token.value
        self.expression = expression

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope:dict[str,Rule]=None):
        depth = self.expression.evaluate(ttle, context)
        rule = scope[self.id]
        new_context = Context()
        new_context.locals[rule.param] = depth
        rule.evaluate(ttle, new_context, scope)