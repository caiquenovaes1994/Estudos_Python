import turtle
import colorsys
import math
import random
import time

random.seed(4)
GRAV, STEPS = 12, 18

screen = turtle.Screen()
screen.setup(780, 480)
screen.bgcolor("#02020a")
screen.colormode(1.0)
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.penup()

def neon(h, s=0.85, v=1.0):
    return colorsys.hsv_to_rgb(h % 1, s, v)

def stroke(pts, color, width):
    t.pencolor(color)
    t.pensize(width)
    t.goto(*pts[0])
    t.pendown()
    for p in pts[1:]:
        t.goto(*p)
    t.penup()

def building(x, w, h):
    color = neon(0.7, 0.5, 0.07)
    for dx in range(0, w, 3):
        top = -240 + h
        stroke([(x + dx, -240), (x + dx, top)], color, 4)
    for _ in range(w // 8):
        wx = x + random.randint(2, w - 2)
        t.goto(wx, -240 + random.randint(5, h - 5))
        t.dot(3, "#ffd27a")

def sky():
    for _ in range(90):
        x = random.randint(-385, 385)
        t.goto(x, random.randint(-100, 235))
        t.dot(random.randint(1, 3), "white")
    x = -390
    while x < 390:
        w = random.randint(24, 46)
        building(x, w, random.randint(25, 80))
        x += w
    screen.update()

def rise(cx, cy):
    pts = []
    for i in range(221):
        u = i / 220
        wob = 2 * math.sin(u * 30) * (1 - u)
        pts.append((cx + wob, -200 + (cy + 200) * u))
    for k in range(0, 220, 20):
        v = 0.4 + 0.6 * k / 220
        stroke(pts[k:k + 21], neon(0.12, 0.4, v), 2)
        screen.update()
        time.sleep(0.015)
    t.goto(cx, cy)
    t.dot(22, "white")
    screen.update()

def pos(cx, cy, a, v, tm):
    x = cx + v * math.cos(a) * tm
    y = cy + v * math.sin(a) * tm - GRAV * tm * tm
    return x, y

def shell(cx, cy, hue, size, n):
    rays = []
    for i in range(n):
        a = 6.283 * i / n + random.gauss(0, 0.03)
        v = size * random.uniform(0.6, 1)
        h = hue + random.gauss(0, 0.04)
        rays.append((a, v, h))
    for j in range(STEPS):
        fade = 1 - j / STEPS
        for a, v, h in rays:
            p = pos(cx, cy, a, v, j * 0.11)
            q = pos(cx, cy, a, v, (j + 1) * 0.11)
            sat = 0.4 + 0.5 * j / STEPS
            color = neon(h, sat, 0.35 + 0.65 * fade)
            stroke([p, q], color, 2)
        screen.update()
        time.sleep(0.02)

def glitter(cx, cy, hue, size):
    for _ in range(45):
        a = random.uniform(0, 6.283)
        r = size * random.uniform(1.3, 2.0)
        x, y = r * math.cos(a), r * math.sin(a)
        t.goto(cx + x, cy + y - 50)
        t.dot(random.randint(2, 4), neon(hue, 0.4))
    screen.update()

def boom(cx, cy, hue):
    rise(cx, cy)
    shell(cx, cy, hue, 62, 64)
    glitter(cx, cy, hue, 62)

def finale():
    rise(0, 30)
    shell(0, 30, 0.1, 105, 110)
    shell(0, 30, 0.75, 55, 60)
    glitter(0, 30, 0.9, 105)

sky()
boom(-250, 60, 0.55)
boom(250, 80, 0.92)
boom(-60, 110, 0.12)
boom(130, -10, 0.35)
finale()
turtle.done()