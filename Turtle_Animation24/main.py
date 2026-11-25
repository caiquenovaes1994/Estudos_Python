from turtle import *
import math

bgcolor('black')
tracer(100)
hideturtle()
a = 0

for _ in range(70):
    for i in range(12):
        color(['hotpink', 'white', 'violet'][i % 3])
        penup()
        home()
        setheading(i * 30 + a)
        pendown()
        r = 80 + 40 * math.sin(a / 15)
        circle(r, 120)
        lt(120)
        circle(r, 120)
    a += 1
    update()
done()