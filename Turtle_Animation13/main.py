from math import *
import turtle, colorsys

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.penup()

turtle.bgcolor("black")
turtle.colormode(1.0)

R, r, d, N = 100, 37, 80, 3700
for i in range(N):
    a = i / N * 2 * pi * r
    x = (R - r) * cos(a) + d * cos((R - r) / r * a)
    y = (R - r) * sin(a) - d * sin((R - r) / r * a)
    t.color(colorsys.hsv_to_rgb(i / N, 1, 1))
    t.goto(x * 2.7, y * 2.7)
    t.pendown()

turtle.done()
