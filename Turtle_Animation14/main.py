from math import *
import turtle, colorsys

t = turtle.Turtle();
t.hideturtle();
t.penup();

turtle.bgcolor("black");
turtle.colormode("1.0")

GOLD = pi * (3 - sqrt(5))
N = 2400
for i in range(N):
    r = 9 * sqrt(i)
    a = i * GOLD
    t.goto(r * cos(a), r * sin(a))
    t.dot(3 + 1 / 500, colorsys.hsv_to_rgb(i / N, 0.8, 1))

turtle.done()