import turtle, math, random

random.seed(11)
sc = turtle.Screen()
sc.setup(1080, 890)
sc.bgcolor("#050816")
sc.tracer(8, 0)

WHITE = (232, 228, 220)
RED = (192, 57, 43)
INK = (20, 24, 44)
GLOW = ((1, (40, 36, 16)), (0.45, (70, 62, 30)))

def pen(w=1):
    t = turtle.Turtle()
    t.hideturtle()
    t.pensize(w)
    return t

def mix(a, b, k):
    return tuple(a[j] + (b[j] - a[j]) * k for j in range(3))

def hx(c):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)

def poly(t, pts, c):
    t.penup()
    t.goto(pts[0])
    t.pendown()
    t.color(hx(c))
    t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.end_fill()
    t.penup()

def disc(t, x, y, d, c):
    t.penup()
    t.goto(x, y)
    t.dot(d, hx(c))

art = pen(2)
fx = pen()
wave = pen(3)
cx = 0.80

def band(y, c):
    r = [(-540, y), (540, y), (540, y - 13), (-540, y - 13)]
    poly(art, r, c)

def trap(xa, xb, y0, y1, ha, hb, c):
    pts = [(xa - ha, y0), (xa + ha, y0), (xb + hb, y1), (xb - hb, y1)]
    poly(art, pts, c)

# night sky

for i in range(40):
    c = mix((8, 10, 34), (44, 50, 104), i / 40)
    band(445 - i * 12, c)

# sea
for i in range(36):
    c = mix((16, 34, 70), (4, 12, 30), i / 36)
    band(-35 - i * 12, c)

# stars
for _ in range(80):
    x = random.randint(-530, 530)
    y = random.randint(30, 440)
    s = random.choice([2, 3, 4])
    disc(art, x, y, s, (201, 212, 255))

# moon
rings = [(190, (16, 24, 63)), (150, (26, 38, 86)), (112, (243, 237, 210))]
for d, c in rings:
    disc(art, 290, 350, d, c)

# rock
poly(art, [(-340, -185), (-290, -130), (-215, -105), (-150, -70), (-10, -70), (50, -110), (120, -135), (150, -185)], (11, 15, 30))

# tower
for i in range(6):
    y0 = -70 + i * 42
    y1 = y0 + 43
    w0 = 48 - 18 * (y0 + 70) / 252
    w1 = 48 - 18 * (y1 + 70) / 252
    c = WHITE if i % 2 == 0 else RED
    trap(cx, cx, y0, y1, w0, w1, c)
    d = mix(c, (10, 12, 30), 0.5)
    trap(cx + w0 * 0.67, cx + w1 * 0.67, y0, y1, w0 * 0.33, w1 * 0.33, d)

# lamp room
trap(cx, cx, 183, 196, 34, 34, INK)
trap(cx, cx, 196, 236, 22, 22, (255, 210, 110))
poly(art, [(cx - 30, 236), (cx + 30, 236), (cx, 272)], RED)
disc(art, cx, 277, 8, WHITE)
for y in (10, 90):
    trap(cx, cx, y, y + 22, 6, 6, INK)

def sweep(a):
    fx.clear()
    dx = 900 * math.cos(a)
    w = 25 + 70 * abs(math.sin(a))
    for s in (1, -1):
        for k, c in GLOW:
            tip = cx + s * dx
            poly(fx, [(cx, 216), (tip, 216 + w * k), (tip, 216 - w * k)], c)

def ripple(n):
    wave.clear()
    for r in range(9):
        y = -195 - r * 28
        wave.penup()
        wave.goto(-540, y)
        wave.pendown()
        c = mix((70, 105, 170), (22, 40, 90), r / 9)
        wave.color(hx(c))
        for x in range(-540, 541, 20):
            dy = 5 * math.sin(x / 45 + n / 7 + r)
            wave.goto(x, y + dy)

# animate
try:
    sc.update()
    for n in range(220):
        sweep(n * 0.05)
        ripple(n)
        sc.update()
    turtle.done()
except (turtle.Terminator, turtle.TK.TclError):
    pass