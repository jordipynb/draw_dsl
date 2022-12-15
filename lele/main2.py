
from textx import metamodel_from_file, TextXSemanticError

turtleMeta = metamodel_from_file('turtle.tx')

scene = turtleMeta.model_from_file('codeExamples/triangle_and_square.turtle')

import turtle

def draw_shape(shape):
    turtle.pencolor(shape.pencil.color if shape.pencil is not None else 'black')
    turtle.fillcolor(shape.fill.color if shape.fill is not None else 'white')
    turtle.down()
    turtle.begin_fill()
    #for l in shape.lines:
    #    draw_line(l)
    turtle.end_fill()
    
def draw_line(l):
    turtle.left(l.direction.angle.degrees)
    turtle.forward(l.length)

for d in scene.draw_instructions:
    turtle.up()
    turtle.goto(d.position.x if d.position is not None else 0,
                d.position.y if d.position is not None else 0)
    draw_shape(d.shape)

turtle.hideturtle()
turtle.done()