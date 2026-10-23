import turtle
import time

s = turtle.Screen()

s.bgcolor("#080614")
s.setup(700, 700)
s.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)

color = ["#ffd166", "#ff5da2", "#55f7e8", "#8388ff"]

for i in range(36):
    t.pencolor(color[i % 4])
    t.circle(100, 60)
    t.left(120)
    t.circle(100, 60)
    t.left(120)
    t.right(10)
    s.update()
    time.sleep(0.08)

for i, r in enumerate([130, 160, 190, 220]):
    t.penup()
    t.goto(0, -r)
    t.setheading(0)
    t.pendown()
    t.pencolor(color[i % len(color)])
    t.circle(r)
    s.update()
    time.sleep(0.3)

turtle.done()