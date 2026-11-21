import turtle
import colorsys
import math
import random

SPANS = [(0, 78), (78, 204), (204, 498), (498, 618)]
GROUND, TOP = -175, 150
FLASHES = [(100, 0.5), (150, 0.4), (260, 0.6), (330, 0.5), (390, 0.7), (450, 0.5), (540, 0.3)]

screen = turtle.Screen()
screen.setup(780, 480)
screen.bgcolor("#03030a")
screen.colormode(1.0)
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.penup()

def clamp(x):
    return max(0.0, min(1.0, x))

def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)

def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))

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

def flash_at(i):
    fl = 0.0
    for f0, amp in FLASHES:
        age = (i - f0) / 30
        if age >= 0:
            fl = max(fl, amp * math.exp(-age * 8))
    return fl

def sky(fl):
    lit = (0.5, 0.55, 0.9)
    top = mix((0.02, 0.02, 0.07), lit, fl * 0.5)
    low = mix((0.3, 0.1, 0.24), (0.9, 0.8, 1), fl * 0.6)
    for i in range(60):
        y = 236 - i * 8
        col = mix(top, low, (i / 59) ** 1.6)
        stroke([(-390, y), (390, y)], col, 10)

def ground(fl):
    for i in range(9):
        y = -168 - i * 8
        col = mix((0.2, 0.7, 0.14), (0, 0, 0.3), i / 8)
        col = mix(col, (0.4, 0.4, 0.6), fl * 0.3)
        stroke([(-390, y), (390, y)], col, 10)

def clouds(tm, cx, fl, power):
    rng = random.Random(3)
    for i in range(260):
        a = rng.uniform(0, 6.283)
        a += tm * (0.25 + 0.35 * power)
        rr = rng.uniform(0, 520)
        x = cx * 0.6 + rr * 0.13 * math.cos(a)
        y = 190 + rr * 0.13 * math.sin(a) - rr * 0.04
        v = rng.uniform(0.03, 0.12)
        v += 0.1 * (1 - rr / 520)
        dark = (v * 0.9, v * 0.7, v * 1.5)
        t.goto(x, y)
        lit = mix(dark, (0.6, 0.6, 0.95), fl * 0.6)
        t.dot(rng.uniform(50, 105), lit)

def center(u, tm, cx):
    sway = 38 * math.sin(tm * 1.4 + u * 5)
    return cx + sway * u ** 1.2

def ring_pt(x0, y, r, ang):
    c, s = math.cos(ang), math.sin(ang)
    return x0 + r * c, y + r * 0.2 * s

def tunnel(tm, extent, power, cx):
    wd = 0.35 + 0.65 * power
    for k in range(46):
        u = k / 45
        if u < 1 - extent:
            continue
        y = GROUND + u * (TOP - GROUND)
        r = (6 + 80 * u ** 1.9) * wd
        x0 = center(u, tm, cx)
        hue = 0.07 + 0.62 * u
        shift = int(tm * 9 + k)
        for j in range(30):
            if (j + shift) % 3 == 0:
                continue
            ang = 6.283 * (j + 0.5) / 30
            dim = 1.0 if math.sin(ang) < 0 else 0.35
            p = ring_pt(x0, y, r, ang)
            q = ring_pt(x0, y, r, ang + 0.17)
            stroke([p, q], neon(hue, 0.8, dim), 3)

def debris(tm, extent, power, cx):
    rng = random.Random(4)
    for i in range(int(170 * power)):
        a0 = rng.uniform(0, 6.283)
        u0, kf = rng.random(), rng.uniform(1.0, 1.8)
        spd = rng.uniform(0.12, 0.3)
        size = rng.radint(2, 5)
        hue = rng.choice([0.08, 0.55, 0.9, 0.12])
        u = 1 - extent + (u0 + tm * spd) % 1 * extent
        r = (6 + 80 * u ** 1.9) * kf
        r *= 0.35 + 0.65 * power
        ang = a0 + tm * (5 + 4 * (1 - u))
        x = center(u, tm, cx) + r * math.cos(ang)
        y = GROUND + u * (TOP - GROUND)
        y += r * 0.2 * math.sin(ang)
        t.goto(x, y)
        t.dot(size, neon(hue, 0.5))

def dust(tm, cx, power):
    rng = random.Random(6)
    for i in range(int(60 * power)):
        a = rng.uniform(0, 6.283) + tm * 5
        rad = 30 + 110 * rng.random()
        t.goto(cx + rad * math.cos(a), GROUND + 6 + rad * 0.18 * math.sin(a))
        glow = neon(0.04, 0.7, 0.45 * power)
        t.dot(rng.uniform(8, 16), glow)