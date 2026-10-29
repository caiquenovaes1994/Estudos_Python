import colorsys
import turtle
from math import *

t = turtle.Turtle();
t.hideturtle();
t.penup();

turtle.bgcolor("black");
turtle.colormode(1.0)

N, S = 1400, 140
for i in range(N):
    a = i / N * 12 * pi
    r = exp(cos(a)) - 2 * cos(4 * a) - sin(a / 12) ** 5
    x, y = S * r * sin(a), S * r * cos(a)
    t.color(colorsys.hsv_to_rgb(i / N, 1, 1))
    t.goto(x, y)
    t.pendown();

    if i % 7 == 0:
        t.goto(0, 0);
        t.goto(x, y)

turtle.done()