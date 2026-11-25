import turtle
import math
import time

s = turtle.Screen()
s.setup(800, 800)
s.bgcolor("#151515")
s.title("Triangle Spiral Illusion")
s.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(1)

colors = ["#e65345", "#ff7655", "#a34bcb", "#6245e8", "#3939a8"]

def triangle(cx, cy, size, angle, color):
    points = []

    for i in range(3):
        a = math.radians(angle + i * 120)
        points.append((
            cx + size * math.cos(a),
            cy + size * math.sin(a)
        ))
    t.penup()
    t.goto(points[0])
    t.pencolor(color)
    t.pendown()

    for p in points[1:] + points[1:]:
        x0, y0 = t.position()
        for k in range(1, 7):
            t.goto(
                x0 + (p[0] - x0) * k / 6,
                y0 + (p[1] - y0) * k / 6
            )
            s.update()
            time.sleep(0.003)

def spiral(x, y, size, rotation):
    for j in range(9):
        triangle(
            x, y, size * (0.88 ** j),
            rotation + j * 9,
            colors[j % 5]
        )

for i in range(14):
    a = math.radians(i * 360 / 14)
    x = 260 * math.cos(a)
    y = 260 * math.sin(a)

    spiral(x, y, 78, i * 25)
spiral(0, 0, 175, 90)

turtle.done()