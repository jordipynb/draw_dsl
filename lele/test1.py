 #Importamos la librería turtle
import math
import turtle

# Todo lo que queremos lograr

#Cuadrados simples
# cuadrado = turtle.Turtle()
# for x in range(0, 4):
#     cuadrado.forward(50)
#     cuadrado.left(90)

#Más cuadrados
# loop = turtle.Turtle()
# loop.color('red', 'blue')
# loop.begin_fill()
# grados = 0
# loop.speed(15)
# for x in range(1, 40):
#     for x in range(0, 4):
#         loop.forward(100)
#         loop.left(90)
#     loop.left(grados + 10)
# loop.end_fill()

# def koch(size, n):
#     if n == 0:
#         turtle.fd(size)
#     else:
#         for angle in [0, 60, -120, 60]:
#            turtle.left(angle)
#            koch(size/3, n-1)

# turtle.setup(800,400)
# turtle.speed (50) # Controla la velocidad de dibujo
# turtle.penup()
# turtle.goto(-300, -50)
# turtle.pendown()
# turtle.pensize(2)
# koch(600,4) # 0 orden Longitud de curva de Koch, grado
# turtle.hideturtle()

# turtle.setup(600,600)
# turtle.speed(0)
# turtle.penup()
# turtle.goto(-200, 100)
# turtle.pendown()
# turtle.pensize(2)
# level = 4
# koch(400,level) 
# turtle.right(120)
# koch(400,level)
# turtle.right(120)
# koch(400,level)
# turtle.hideturtle()

# def hilbert(level, angle, step):   
#     if level == 0: return
#     turtle.right(angle) 
#     hilbert(level-1, -angle, step) 
#     turtle.forward(step) 
#     turtle.left(angle) 
#     hilbert(level-1, angle, step) 
#     turtle.forward(step) 
#     hilbert(level-1, angle, step) 
#     turtle.left(angle) 
#     turtle.forward(step) 
#     hilbert(level-1, -angle, step) 
#     turtle.right(angle) 
  
# level = 3
# size = 200
# turtle.penup() 
# turtle.goto(-size / 2.0, size / 2.0) 
# turtle.pendown() 
# hilbert(level, 90, size/(2**level-1)) 

turtle.done()
