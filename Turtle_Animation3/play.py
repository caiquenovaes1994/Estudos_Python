import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Python Drawing")

pen = turtle.Turtle()
pen.speed(3)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

for i in range(360):
    pen.pencolor(colors[i % len(colors)])
    pen.forward(200)
    pen.left(170)


turtle.done()