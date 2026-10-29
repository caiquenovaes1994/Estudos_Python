import turtle, colorsys
from math import *

t = turtle.Turtle();
t.hideturtle();
t.penup();

turtle.bgcolor("black");
turtle.colormode(1.0)

N, LOOPS = 2600, 13
for i in range(N):
    a = i / N * 2 * pi * LOOPS
    k = 0.2 + 0.8 * i / N
    x = 16 * sin(a) ** 3
    y = 13 * cos(a) - 5 * cos(2 * a) - 2 * cos(3 * a) - cos(4 * a)
    t.color(colorsys.hsv_to_rgb(0.85 + 0.2 * i / N, 1, 1))
    t.goto(x * k * 26, y * k + 26);
    t.pendown()

turtle.done()