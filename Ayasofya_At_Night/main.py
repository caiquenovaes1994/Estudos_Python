import turtle, math, random, colorsys

random.seed(34)
sc = turtle.Screen()
sc.setup(1080, 880)
sc.colormode(255)
sc.bgcolor(10, 10, 24)
sc.tracer(0, 0)

HZ = -120
GOLD = (255, 200, 110)
WARM = (255, 226, 150)
CREAM = (255, 238, 205)
SEA = (34, 30, 84)

def pen():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.speed(0)
    return t

def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

def warm(c, k):
    return mix(c, GOLD, k)

def poly(t, pts, c, base=HZ):
    t.color(c)
    t.goto(pts[0])
    t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.end_fill()
    if base is not None and min(y for x, y in pts) >= base - 3:
        m = [(x, 2 * base - y) for x, y in pts]
        poly(t, m, mix(c, SEA, 0.66), None)

def box(t, x, y, w, h, c, base=HZ):
    poly(t, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], c, base)

def wall(t, x, y, w, h, c, k=0.45, base=HZ):
    for j in range(4):
        f = warm(c, k * (1 - j / 3) ** 1.5)
        box(t, x, y + h * j / 4, w, h / 4 + 1, f, base)

def disc(t, x, y, d, c):
    t.goto(x, y)
    t.dot(d, c)

def line(t, pts, c, w=2):
    t.pensize(w)
    t.color(c)
    t.goto(pts[0])
    t.pendown()
    for p in pts[1:]:
        t.goto(p)
    t.penup()

def glow(t, x, y, r, c, bg, n=8):
    for i in range(n):
        disc(t, x, y, r * (n - i) / 2, mix(bg, c, i / (n - 1)))

def sky(y):
    k = min(max((440 - y) / 560, 0), 1)
    c = mix((5, 7, 24), (44, 32, 92), min(k * 1.6, 1))
    c = mix(c, (255, 164, 106), max(0, k - 0.8) / 0.2)
    return c

def dome(t, cx, base, r, c, mb=HZ, ry=0.95, k=0.45):
    hh = r * ry
    for j in range(6):
        h0, h1 = hh * j / 6, hh * (j + 1) / 6 + 0.6
        hs = [h0 + (h1 - h0) * q / 4 for q in range(5)]
        xs = [r * math.sqrt(max(0, 1 - (h / hh) ** 2)) for h in hs]
        pts = [(cx - xs[q], base + hs[q]) for q in range(5)]
        pts += [(cx + xs[q], base + hs[q]) for q in (4, 3, 2, 1, 0)]
        poly(t, pts, warm(c, k * (1 - j / 5) ** 1.5), mb)

def minaret(t, x, h, c, n=2, u=1):
    for j in range(3):
        f = warm(c, 0.38 - j * 0.13)
        box(t, x - 6 * u, HZ + h * j / 3, 12 * u, h / 3 + 1, f)
    for q in range(n):
        y = HZ + h * (0.6 + q * 0.14)
        box(t, x - 10 * u, y, 20 * u, 5 * u, warm(c, 0.2))
        disc(t, x, y + 9 * u, 4 * u, WARM)
    top = HZ + h
    poly(t, [(x - 7 * u, top), (x, top + 52 * u), (x + 7 * u, top)], c)
    line(t, [(x, top + 52 * u), (x, top + 66 * u)], CREAM, 2)

def star(t, x, y, r, c):
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        q = r if i % 2 == 0 else r * 0.4
        pts.append((x - q * math.cos(a), y + q * math.sin(a)))
    poly(t, pts, c, None)

def crescent(t, x, y, r, c):
    d, ri = r * 0.34, r * 0.8
    px = (d * d + r * r - ri * ri) / (2 * d)
    py = math.sqrt(r * r - px * px)
    a = math.atan2(py, px)
    b = math.atan2(py, px - d)
    pts = []
    for i in range(25):
        u = a + (2 * math.pi - 2 * a) * i / 24
        pts.append((x + r * math.cos(u), y + r * math.sin(u)))
    for i in range(25):
        u = 2 * math.pi - b - (2 * math.pi - 2 * b) * i / 24
        pts.append((x + d + ri * math.cos(u), y + ri * math.sin(u)))
    poly(t, pts, c, None)

def cloud(t, x, y, w, c):
    pts = [(x, y), (x + w * 0.3, y + 7), (x + w * 0.8, y + 5)]
    pts += [(x + w, y), (x + w * 0.7, y - 4), (x + w * 0.25, y - 5)]
    poly(t, pts, c, None)

art = pen()
rp = pen()
lit = pen()
fy = pen()
gl = pen()
fw = pen()

# dusk sky
for i in range(70):
    y = 440 - (i + 1) * 8
    box(art, -540, y, 1080, 9, sky(y + 4), None)

# afterglow clouds
for i in range(7):
    x = random.randint(-520, 300)
    y = random.randint(-10, 190)
    c = mix(sky(y), (255, 150, 140), 0.5)
    cloud(art, x, y, random.randint(140, 280), c)

# bosphorus water
for i in range(40):
    y = HZ - (i + 1) * 8
    c = mix(SEA, (8, 8, 28), i / 39)
    box(art, -540, y, 1080, 9, c, None)

# stars

STARS = []
while len(STARS) < 80:
    x = random.randint(-530, 530)
    y = random.randint(120, 430)
    if abs(x + 440) > 110 or y < 270:
        STARS.append((x, y))
        c = mix(sky(y), CREAM, 0.8)
        disc(art, x, y, random.choice([2, 2, 3]), c)

#crescent moon
MX, MY = -430, 330
glow(art, MX, MY, 44, (96,86, 160), sky(MY), 6)
crescent(art, MX, MY, 38, CREAM)
star(art, MX + 54, MY + 4, 12, CREAM)

# far hills
def hill(x):
    return 56 + 24 * math.sin(x / 85) + 12 * math.sin(x / 23)

FAR2 = (92, 58, 112)
x = -540
while x < 540:
    w = random.randint(30, 60)
    h = 50 + 18 * math.sin(x / 130) + random.randint(0, 14)
    box(art, x, HZ, w, h, FAR2)
    x += w - 3

#old city
FAR = (34, 28, 72)
WINDOWS = []
x = -540
while x < 540:
    w = random.randint(22, 44)
    box(art, x, HZ, w, hill(x + w / 2) * 0.7, FAR)
    x += w - 2
for i in range(110):
    wx = random.randint(-530, 530)
    wy = random.randint(HZ + 6, HZ + int(hill(wx) * 0.7) - 6)
    WINDOWS.append((wx, wy))
    disc(art, wx, wy, 3, mix(GOLD, FAR, random.random() * 0.5))

# ayasofy (santa sofia)
HX, U = 0, 1.75
HAG = (122, 84, 108)
wall(art, HX - 128 * U, HZ, 256 * U, 54 * U, HAG)
wall(art, HX - 108 * U, HZ + 54 * U, 216 * U, 22 * U, HAG)
for sx in (-1, 1):
    wall(art, HX + sx * 136 * U - 13 * U, HZ, 26 * U, 104 * U, HAG)
    wall(art, HX + sx * 160 * U - 10 * U, HZ, 20 * U, 70 * U, HAG)
    dome(art, HX + sx * 74 * U, HZ + 76 * U, 48 * U, HAG)
    dome(art, HX + sx * 118 * U, HZ + 76 * U, 26 * U, HAG)
dome(art, HX, HZ + 76 * U, 70 * U, HAG, ry=0.76)
for k in range(16):
    box(art, HX - 64 * U + k * 8.6 * U, HZ + 80 * U, 4 * U, 11 * U, WARM, None)
for k in range(9):
    x = HX - 100 * U + k * 25 * U
    box(art, x, HZ + 14 * U, 9 * U, 24 * U, GOLD, None)
    disc(art, x + 4.5 * U, HZ + 38 * U, 9 * U, GOLD)
for k in range(7):
    box(art, HX - 78 * U + k * 26 * U, HZ + 58 * U, 7 * U, 14 * U, WARM, None)
top = HZ + 76 * U + 70 * U * 0.76
line(art, [(HX, top), (HX, top + 26)], CREAM, 3)
crescent(art, HX, top + 38, 13, CREAM)
for sx, h in ((-180, 216), (-164, 176), (164, 176), (188,216)):
    minaret(art, HX + sx * U, h * U, HAG, 3, 1.5)

# karakoy enbankment
box(art, -540, HZ - 6, 1080, 8, (74, 70, 130), None)
for x in range(-520, 540, 40):
    line(art, [(x, HZ), (x, HZ + 22)], (86, 82, 150), 2)
    disc(art, x, HZ + 26, 8, GOLD)

def lights(n):
    lit.clear()
    for i, (sx, sy) in enumerate(STARS):
        if (n // 9 + i) % 6 == 0:
            disc(lit, sx, sy, 5, CREAM)
    for wx, wy in WINDOWS:
        if (n // 15 + wx) % 6 == 0:
            disc(lit, wx, wy, 5, WARM)

def ferry(n):
    fy.clear()
    x = (n * 3.1) % 1500 - 700
    y = HZ - 78
    hull = [(x - 74, y + 8), (x + 78, y + 8)]
    hull += [(x + 60, y - 10), (x - 54, y -10)]
    poly(fy, hull, (70, 50, 80), None)
    box(fy, x - 56, y + 8, 112, 16, CREAM, None)
    box(fy, x - 38, y + 24, 76, 14, CREAM, None)
    box(fy, x + 8, y + 38, 14, 18, (200, 70, 80), None)
    for k in range(9):
        disc(fy, x - 48 + k * 12, y + 16, 6, GOLD)
    for k in range(6):
        disc(fy, x - 30 + k * 12, y + 31, 5, GOLD)
    c1, c2 = mix(GOLD, SEA, 0.4), mix(GOLD, SEA, 0.65)
    line(fy, [(x - 70, y - 16), (x + 70, y -16)], c1, 4)
    line(fy, [(x - 40, y - 28), (x + 40, y - 28)], c2, 3)
    
FLOCK = []
for i in range(6):
    FLOCK.append((random.randint(0, 1300), random.randint(120, 300), random.uniform(1.2, 2.2)))

def gulls(n):
    gl.clear()
    for i, (gx, gy, s) in enumerate(FLOCK):
        x = (gx + n * s) % 1300 - 650
        y = gy + 10 * math.sin(n / 14 + i)
        w = 14 + 5 * math.sin(n / 3 + i)
        v = [(x - 18, y + w), (x, y), (x + 18, y + w)]
        line(gl, v, CREAM, 3)

def ripple(n):
    rp.clear()
    for j, x in enumerate(range(-520, 540, 40)):
        for i in range(6):
            y = HZ - 16 - i * 14
            w = 14 - i * 1.5 + 4 * math.sin(n / 8 + j + i)
            c = mix(GOLD, SEA, 0.55 + i * 0.07)
            line(rp, [(x - w, y), (x + w, y)], c, 2)

SHOWS = [(-380, 340, 40), (380, 330, 110), (-150, 400, 180), (170, 390, 250), (-420, 300, 320), (430, 360, 370)]
BURST = [(255, 120, 130), (255, 214, 120), (140, 200, 255)]

def fireworks(n):
    fw.clear()
    for cx, cy, t0 in SHOWS:
        k = n - t0
        if 0 <= k < 70:
            r = 14 + k * 2.4
            for j in range(24):
                a = j * math.pi / 12
                x = cx + r * math.cos(a)
                y = cy + r * math.sin(a) - k * k / 90
                c = mix(sky(y), BURST[j % 3], (1 - k / 70) ** 0.5)
                disc(fw, x, y, 6, c)

# animate
for n in range(420):
    ripple(n)
    lights(n)
    ferry(n)
    gulls(n)
    fireworks(n)
    sc.update()

turtle.done()