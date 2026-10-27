import turtle
import math
import random

random.seed(13)

screen = turtle.Screen()
screen.setup(800, 400)
screen.bgcolor("#0b0618")

t = turtle.Turtle()
t.speed(0)

def stars():
    t.penup()
    for _ in range(70):
        x = random.randint(-390, 390)
        y = random.randint(-230, 230)
        t.goto(x, y)
        t.dot(random.randint(2, 4), "white")

def poly(points, edge, fill, width=3):
    t.color(edge, fill)
    t.pensize(width)
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
    t.end_fill()
    t.penup()

def moon():
    t.penup()
    glow = [(300, "#1b0d38"), (262, "#2a1650"), (230, "#3c2169")]
    for size, col in glow:
        t.goto(215, 105)
        t.dot(size, col)
    t.goto(215, 105)
    t.dot(200, "#fff1b8")
    craters = [(180, 130, 40), (250, 80, 28), (205, 60, 18)]
    for x, y, s in craters:
        t.goto(x, y)
        t.dot(s, "#f1dc98")

def bat(x, y, s):
    shape = [(0, 6), (-14, 16), (-30, 14), (-24, 4), (-34, -6), (-16, -2), (-6, -10), (0, -4), (6, -10), (16, -2), (34, -6), (24, 4), (30, 14), (14, 16)]
    pts = [(x + px * s, y + py * s)
    for px, py in shape]
    poly(pts, "#b58cf0", "#2b1650", 2)
    for dx in (-4, 4):
        t.goto(x + dx * s, y + 5 * s)
        t.dot(4 * s, "#ff5e7e")

def body():
    t.penup()
    glow = [(330, "#150a2e"), (290, "#1e0f40")]
    for size, col in glow:
        t.goto(0, 0)
        t.dot(size, col)
    
    t.goto(-105, 10)
    t.setheading(90)
    t.color("#b9a7ff", "#f6f2ff")
    t.pensize(5)
    t.pendown()
    t.begin_fill()
    t.circle(-105, 180)
    t.forward(125)
    for i in range(4):
        t.circle(-26.25, 180)
        t.right(180)
    t.setheading(90)
    t.forward(125)
    t.end_fill()
    t.penup()

def arms():
    for x, y in [(-122, -10), (122, -501)]:
        t.goto(x, y)
        t.dot(44, "#b9a7ff")
        t.dot(36, "#f6f2ff")

def face():
    for x in (-40, 40):
        t.goto(x, 28)
        t.dot(50, "#1b1033")
        t.goto(x + 9, 40)
        t.dot(16, "#ffffff")
        t.goto(x - 8, 20)
        t.dot(8, "#ffffff")
    for x in (-68, 68):
        t.goto(x, -4)
        t.dot(30, "#ffb3d9")
    t.goto(-14, -6)
    t.setheading(-60)
    t.color("#1b1033")
    t.pensize(5)
    t.pendown()
    t.circle(16, 120)
    t.penup()

def hat():
    cone = [(-50, 106), (-36, 152), (-8, 182), (34, 206), (28, 168), (16, 142), (52, 112)]
    poly(cone, "#c9a8ff", "#5b25c9", 3)
    brim = [(-90, 80), (-40, 84), (40, 90), (92, 102), (40, 112), (-40, 106)]
    poly(brim, "#c9a8ff", "#7a3df0", 3)
    band = [(-46, 112), (-42, 128), (48, 130), (50, 116)]
    poly(band, "#ffe08a", "#ffb347", 2)
    t.goto(2, 122)
    t.dot(14, "#ffe08a")

def pumpkin(x, y):
    t.goto(x, y)
    t.dot(88, "#b24f00")
    for dx in (-22, 22):
        t.goto(x + dx, y)
        t.dot(60, "#ff8a1f")
    t.goto(x, y)
    t.dot(54, "#ff9d3a")
    stem = [(x - 4, y + 40), (x + 4, y + 40), (x + 9, y + 56), (x, y + 52)]
    poly(stem, "#4fae3a", "#2f7a22")
    for dx in (-18, 18):
        ex = x + dx
        eye = [(ex - 9, y + 4), (ex + 9, y + 4), (ex, y + 20)]
        poly(eye, "#ffe45c", "#ffd21f", 2)
        grin = [(x - 20, y - 10), (x - 10, y - 20), (x, y - 10), (x + 20, y - 10)]
        poly(grin, "#ffe45c", "#ffd21f", 2)

stars()
moon()
bat(205, 125, 1.3)
bat(-250, 150, 1.0)
bat(300, -20, 0.9)
body()
arms()
face()
hat()
pumpkin(-225, -150)
t.hideturtle()
turtle.done()