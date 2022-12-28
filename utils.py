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
    def __init__(self,parent=None,depth=None,value=None):
        self.locals={}
        self.locals[depth]=value
        self.parent=parent
        
    def create_children(self):
        return Context(self)
    
    def search(self,token):
        for vname , value in self.locals.items():
            if vname == token.value:
                return value 
        if self.parent is None:
            print(f'SemanticError: "{token.value}" en la línea {token.lineno}, columna {find_column(token)} no esta definido')
        return self.parent.search(token)
    
    def set_value(self,name,value):
        if name in self.locals.keys():
            self.locals[name]=value
        else: self.parent.set_value(name,value)
        
class Node:
    def evaluate(self):
        raise NotImplementedError()
   
class NodeInstruction(Node):
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope=None):
        raise NotImplementedError()    

class ConditionNode(NodeInstruction):
    def evaluate(self, ttle:turtle.Turtle, depth: int):
        raise NotImplementedError()

class ExpressionNode(NodeInstruction):
    def evaluate(self, ttle:turtle.Turtle, depth: int):
        raise NotImplementedError()

class Scene(Node):
    def __init__(self, draws, error_list):
        self.draws:list[Draw] = draws
        self.error_list:list = error_list

    def evaluate(self):
        try:
            for draw in self.draws:
                draw.evaluate()
            turtle.done()
        except turtle.Terminator: pass
        except _tkinter.TclError: pass

class Axiom(NodeInstruction):
    def __init__(self, instructions:list[NodeInstruction]):
        self.instructions = instructions

    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope=None):
        for elem in self.instructions:
            elem.evaluate(ttle,context=Context(),scope=scope)

class Rule(NodeInstruction):
    def __init__(self, name:str, param:str, instructions:list[NodeInstruction]):
        self.name = name
        self.instructions = instructions
        self.param=param
    def evaluate(self, ttle:turtle.Turtle, context:Context,scope):
        depth=context.locals[self.param]
        for elem in self.instructions:
            elem.evaluate(ttle, context,scope)

class Shape(NodeInstruction):
    def __init__(self, name:str, pencil:str, rules:list[Rule], axiom:Axiom):
        self.stack = []
        self.name = name
        self.pencil = pencil
        self.axiom = axiom
        self.scope={}
        self.rules=rules
    def evaluate(self, ttle:turtle.Turtle, context:Context=None, scope=None):
        if self.rules:
            for rule in self.rules:
                self.scope[rule.name]=rule
        ttle.pencolor(self.pencil)
        self.axiom.evaluate(ttle,scope=self.scope)

class Draw(Node):
    def __init__(self, shape:Shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y

    def evaluate(self):
        ttle = turtle.Turtle()
        ttle.left(90)
        ttle.up()
        ttle.goto(self.x.evaluate(ttle), self.y.evaluate(ttle))
        ttle.down()
        ttle.speed(3)
        ttle.pensize(2)
        self.shape.evaluate(ttle)
        ttle.hideturtle()

class LeftInstruction(NodeInstruction):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, ttle, context,scope):
        angle=self.expression.evaluate(ttle,context,scope)
        ttle.left(angle)

class RightInstruction(NodeInstruction):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, ttle, context,scope):
        angle=self.expression.evaluate(ttle,context,scope)
        ttle.right(angle)

class LineInstruction(NodeInstruction):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, ttle, context,scope):
        distance=self.expression.evaluate(ttle,context,scope)
        ttle.forward(distance)

class PushInstruction(NodeInstruction):
    def __init__(self):
        pass

    def evaluate(self, ttle, context,scope):
        stack.append((ttle.xcor(), ttle.ycor(), ttle.heading()))

class PopInstruction(NodeInstruction):
    def __init__(self):
        pass

    def evaluate(self, ttle, context,scope):
        pos_x,pos_y,angle = stack.pop()
        ttle.up()
        ttle.goto(pos_x, pos_y)
        ttle.setheading(angle)
        ttle.down()

class JumpInstruction(NodeInstruction):
    def __init__(self, exp1, exp2):
        self.x = exp1
        self.y = exp2

    def evaluate(self, ttle, context,scope):
        ttle.up()
        x=self.x.evaluate(ttle,context,scope)
        y=self.y.evaluate(ttle,context,scope)
        ttle.goto(x,y)
        ttle.down()

class Nill(NodeInstruction):
    def __init__(self):
        pass

    def evaluate(self, ttle, context,scope):
        pass

class Assign(NodeInstruction):
    def __init__(self,ID,expression):
        self.ID=ID
        self.expression=expression
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        context.set_value(self.ID,self.expression.evaluate(ttle,context,scope))

class Set_X(NodeInstruction):
    def __init__(self,expression):
        self.expression = expression
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        ttle.setx(self.expression.evaluate(ttle,context,scope))

class Set_Y(NodeInstruction):
    def __init__(self,expression):
        self.expression = expression
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        ttle.sety(self.expression.evaluate(ttle,context,scope))

class Get_X(NodeInstruction):
    def __init__(self,ID):
        self.ID = ID
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        context.set_value(self.ID,ttle.xcor())
    
class Get_Y(NodeInstruction):
    def __init__(self,ID):
        self.ID = ID
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        context.set_value(self.ID,ttle.ycor())    

class SetPencil(NodeInstruction):
    def __init__(self,ID):
        self.ID = ID
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        ttle.pencolor(self.ID) 

class If(NodeInstruction):
    def __init__(self,condition:ConditionNode,if_body:list[NodeInstruction],else_body:list[NodeInstruction]=None):
       self.condition=condition
       self.if_body=if_body
       self.else_body=else_body
    def evaluate(self, ttle: turtle.Turtle,context:Context,scope):
        context=context.create_children()
        if self.condition.evaluate(ttle,context,scope):
            for instruction in self.if_body:
                result = instruction.evaluate(ttle, context,scope)
                if isinstance(result,Break): return result
        elif self.else_body:
            for instruction in self.else_body:
                result = instruction.evaluate(ttle, context,scope)
                if isinstance(result,Break): return result

class While(NodeInstruction):
    def __init__(self,condition:ConditionNode,body:list[NodeInstruction]):
        self.condition = condition
        self.body=body
    def evaluate(self, ttle: turtle.Turtle,context,scope):
        while self.condition.evaluate(ttle, context,scope):
            context=context.create_children()
            for instruction in self.body:
                if isinstance(instruction,Break) or isinstance(instruction.evaluate(ttle, context,scope),Break): break
                

class Break(NodeInstruction):
    def __init__(self):
        pass
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return self

class AndOperator(ConditionNode):
    def __init__(self,prop1:ConditionNode,prop2:ConditionNode):
       self.prop1=prop1
       self.prop2=prop2
    def evaluate(self, ttle: turtle.Turtle,context,scope):
        return self.prop1.evaluate(ttle,context,scope) and self.prop2.evaluate(ttle,context,scope)

class OrOperator(ConditionNode):
    def __init__(self,prop1:ConditionNode,prop2:ConditionNode):
       self.prop1=prop1
       self.prop2=prop2
    def evaluate(self,ttle: turtle.Turtle,context,scope):
        return self.prop1.evaluate(ttle,context,scope) or self.prop2.evaluate(ttle,context,scope)

class NotOperator(ConditionNode):
    def __init__(self,condiction:ConditionNode):
        self.condition=condiction
    def evaluate(self, ttle: turtle.Turtle,context,scope):
        return not self.condition.evaluate(ttle,context,scope)

class GreaterCondition(ConditionNode):
    def __init__(self,exp1:ExpressionNode,exp2:ExpressionNode):
       self.exp1=exp1
       self.exp2=exp2
    def evaluate(self,ttle: turtle.Turtle,context,scope):
        return self.exp1.evaluate(ttle,context,scope) > self.exp2.evaluate(ttle,context,scope)

class MenorCondition(ConditionNode):
    def __init__(self,exp1:ExpressionNode,exp2:ExpressionNode):
       self.exp1=exp1
       self.exp2=exp2
    def evaluate(self,ttle: turtle.Turtle,context,scope):
        return self.exp1.evaluate(ttle,context,scope) < self.exp2.evaluate(ttle,context,scope)

class EqualCondition(ConditionNode):
    def __init__(self,exp1:ExpressionNode,exp2:ExpressionNode):
       self.exp1=exp1
       self.exp2=exp2
    def evaluate(self,ttle: turtle.Turtle,context,scope):
        return self.exp1.evaluate(ttle,context,scope) == self.exp2.evaluate(ttle,context,scope)

class TrueCondition(ConditionNode):
    def __init__(self):
       pass
    def evaluate(self,ttle: turtle.Turtle,context,scope):
        return True 

class FalseCondition(ConditionNode):
    def __init__(self):
       pass
    def evaluate(self,ttle: turtle.Turtle,context,scope):
        return False               

class Expression(Node):
    def __init__(self,exp1,exp2):
        pass
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        pass

class SumExpression(Expression):
    def __init__(self,exp1,exp2):
        self.exp1=exp1
        self.exp2=exp2
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return   self.exp1.evaluate(ttle,context,scope) + self.exp2.evaluate(ttle,context,scope)
    
class SubExpression(Expression):
    def __init__(self,exp1,exp2):
        self.exp1=exp1
        self.exp2=exp2
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return   self.exp1.evaluate(ttle,context,scope) - self.exp2.evaluate(ttle,context,scope)

class MulTerm(Expression):
    def __init__(self,exp1,exp2):
        self.exp1=exp1
        self.exp2=exp2
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return   self.exp1.evaluate(ttle,context,scope) * self.exp2.evaluate(ttle,context,scope)

class DivTerm(Expression):
    def __init__(self,exp1,exp2):
        self.exp1=exp1
        self.exp2=exp2
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return   self.exp1.evaluate(ttle,context,scope) / self.exp2.evaluate(ttle,context,scope)

class Pow(Expression):
    def __init__(self,exp1,exp2):
        self.exp1=exp1
        self.exp2=exp2
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return   math.pow(self.exp1.evaluate(ttle,context,scope),self.exp2.evaluate(ttle,context,scope))

class Factor(Expression):
    def __init__(self,ID):
        self.ID=ID
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return  context.search(self.ID)

class Value(Expression):
    def __init__(self,value):
        self.value=value
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return  self.value

class Function(Expression):
    def __init__(self,func,expression : Expression):
        self.expression=expression
        self.func=func
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope=None):
        return self.func(self.expression.evaluate(ttle,context,scope))

class CallShapeInstruction(NodeInstruction):
    def __init__(self, shape:Shape):
        self.shape = shape

    def evaluate(self, ttle, depth):
        self.shape.evaluate(ttle)

class CallRuleInstruction(NodeInstruction):
    def __init__(self, token:LexToken, expression: Expression ):
        self.id =  token.value
        self.expression = expression

    def evaluate(self, ttle, context,scope:dict[str,Rule]):
        depth=self.expression.evaluate(ttle,context)
        rule=scope[self.id]
        new_context=Context(parent=None,depth=rule.param,value=depth)
        rule.evaluate(ttle, new_context,scope)

class CallableRule(Node):
    def __init__(self, token:LexToken):
        self.token = token

    def search_rule(self, locals_rule:list[Rule]):
        for rule in locals_rule:
            if self.token.value == rule.name:
                return rule
        return self.token