import turtle, colorsys

screen = turtle.Screen()
screen.bgcolor("black")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

for i in range(150):
    t.pencolor(colorsys.hsv_to_rgb(0.12 - i / 150 * 0.12, 1, 1))
    t.forward(i * 2.8)
    t.right(165)

turtle.done()