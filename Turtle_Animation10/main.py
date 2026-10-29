from turtle import backward
from turtle import forward
from turtle import *

tracer(15)
bgcolor("black")
c = ("#ff66cc", "white")
pensize(3)
for i in range(520):
    forward(i)
    right(90)
    color(c[i % 2])
    for j in range(6):
        forward(i)
        right(145)
        backward(j / 2)
        left(180)

done()