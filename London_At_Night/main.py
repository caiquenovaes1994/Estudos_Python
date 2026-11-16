import turtle, math, random, time

random.seed(21)
sc = turtle.Screen()
sc.setup(1080, 890)
sc.colormode(255)
sc.bgcolor((4, 6, 20))
sc.tracer(0, 0)

GOLD = (255, 200, 110)
WARM = (255, 226, 150)
CREAM = (255, 238, 200)
INK = (12, 15, 36)
FAR = (22, 26, 58)
RED = (196, 30, 42)
HORIZON = -130
TX, EX, EY, ER, SX = -210, 190, 70, 200, 440


def pen(w=1):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.pensize(w)
    return t

def mix(a, b, k):
    return tuple(int(a[j] + (b[j] - a[j]) * k) for j in range(len(a)))

def poly(t, pts, c):
    t.goto(pts[0])
    t.color(c)
    t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.end_fill()

def box(t, x, y, w, h, c):
    poly(t, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], c)

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

def skyc(y):
    k = min(max((445 - y) / 575, 0), 1)
    c = mix((4, 6, 20), (30, 28, 78), min(k * 1.6, 1))
    return mix(c, (150, 74, 112), max(0, (k - 0.45) / 0.55))

def blocked(x, y):
    if abs(x - TX) < 80 and y < 440:
        return True
    if abs(x - SX) < 70 and y < 400:
        return True
    return math.hypot(x - EX, y - EY) < ER + 20

art = pen()
hd = pen()
eye = pen()
lit = pen()
bus = pen()
fw = pen()
tw = pen()

# dusk sky
for i in range(48):
    y = 445 - (i + 1) * 12
    box(art, -540, y, 1080, 13, skyc(y + 6))

# stars
STARS = []
while len(STARS) < 70:
    x = random.randint(-530, 530)
    y = random.randint(40, 440)
    if blocked(x, y):
        continue
    s = random.choice([2, 2, 3, 4])
    STARS.append((x, y, s))
    disc(art, x, y, s, mix(skyc(y), CREAM, random.random() * 0.7 + 0.3))

# moon
MX, MY = -420, 345
disc(art, MX, MY, 150, mix(skyc(MY), CREAM, 0.06))
disc(art, MX, MY, 112, mix(skyc(MY), CREAM, 0.14))
disc(art, MX, MY, 74, (250, 242, 222))
disc(art, MX + 20, MY + 12, 66, mix(skyc(MY), CREAM, 0.14))

# river
for i in range(26):
    c = mix((54, 36, 96), (4, 6, 20), i / 25)
    box(art, -540, HORIZON - 30 - (i + 1) * 12, 1080, 13, c)

wave = pen(2)

# old city
LIGHTS = []
x = -560
while x < 560:
    w = random.randint(34, 70)
    h = random.randint(60, 190)
    box(art, x, HORIZON, w, h, FAR)
    for r in range(h // 24):
        for col in range(w // 16):
            wx = x + 6 + col * 16
            wy = HORIZON + 10 + r * 24
            box(art, wx, wy, 5, 7, (38, 44, 90))
            LIGHTS.append((wx, wy, 5, 7, random.randint(10, 130), random.random() > 0.5))
    x += w - 4

# parliament
P0, P1 = -540, TX - 62
box(art, P0, HORIZON, P1 - P0, 96, (16, 20, 46))
box(art, P0, HORIZON + 96, P1 - P0, 8, (26, 32, 66))
for x in range(P0 + 14, P1 - 24, 34):
    poly(art, [(x, HORIZON + 104), (x + 22, HORIZON + 104), (x + 6, HORIZON + 152)], (16, 20, 46))
    box(art, x + 6, HORIZON + 24, 9, 34, (40, 46, 96))
    on = random.randint(4, 40)
    LIGHTS.append((x + 6, HORIZON + 24, 9, 34, on, True))

# big ben
def clock(t, n):
    cx, cy = TX, 173
    disc(t, cx, cy, 120, GOLD)
    disc(t, cx, cy, 110, (20, 24, 50))
    disc(t, cx, cy, 102, CREAM)
    for k in range(12):
        a = math.tau * k / 12
        mx, my = cx + 41 * math.sin(a), cy + 41 * math.cos(a)
        disc(t, mx, my, 6, (40, 36, 60))
    m = 50 + 10 * min(n / 240, 1)
    am = math.tau * m / 60
    ah = math.tau * (11 + m / 60) / 12
    hx, hy = cx + 28 * math.sin(ah), cy + 28 * math.cos(ah)
    line(t, [(cx, cy), (hx, hy)], (20, 20, 40), 7)
    mx, my = cx + 44 * math.sin(am), cy + 44 * math.cos(am)
    line(t, [(cx, cy), (mx, my)], (20, 20, 40), 4)
    disc(t, cx, cy, 10, (20, 20, 40))

def tower(cx):
    box(art, cx - 62, HORIZON, 124, 22, (20, 25, 54))
    box(art, cx - 52, HORIZON + 22, 104, 190, INK)
    box(art, cx + 40, HORIZON + 22, 12, 190, (24, 30, 64))
    for r in range(3):
        for col in (-30, 16):
            wy = HORIZON + 42 + r * 62
            box(art, cx + col, wy, 14, 38, (40, 46, 96))
            on = random.randint(4, 40)
            LIGHTS.append((cx + col, wy, 14, 38, on, True))
    box(art, cx - 62, 82, 124, 14, (24, 30, 64))
    box(art, cx - 70, 96, 140, 154, INK)
    box(art, cx + 58, 96, 12, 154, (24, 30, 64))
    clock(hd, 0)
    box(art, cx - 54, 262, 108, 56, INK)
    for i in range(3):
        box(art, cx - 40 + i * 30, 270, 20, 40, (40, 46, 96))
        LIGHTS.append((cx - 40 + i * 30, 270, 20, 40, 30 + i * 6, True))
    for s in (-1, 1):
        poly(art, [(cx + s * 70, 250), (cx + s * 56, 250), (cx + s * 63, 290)], INK)
    poly(art, [(cx - 62, 318), (cx + 62, 318), (cx + 16, 404), (cx - 16, 404)], (16, 20, 44))
    poly(art, [(cx - 16, 404), (cx + 16, 404), (cx, 432)], INK)
    line(art, [(cx - 62, 318), (cx - 16, 404)], (150, 100, 120), 2)
    line(art, [(cx, 432), (cx, 442)], GOLD, 3)

tower(TX)

# the shard
poly(art, [(SX - 58, HORIZON), (SX + 58, HORIZON), (SX, 390)], (28, 38, 82))
poly(art, [(SX, HORIZON), (SX + 58, HORIZON), (SX, 390)], (16, 22, 52))
for r in range(1, 14):
    y = HORIZON + r * 36
    half = 58 * (1 - (y - HORIZON) / (390 - HORIZON))
    line(art, [(SX - half, y), (SX + half, y)], (60, 80, 140), 2)
box(art, SX - 2, 390, 4, 48, (90, 110, 170))

# london eye
PODS = [CREAM, (120, 230, 255), GOLD, (255, 150, 210), (170, 150, 255)]

def wheel(t, n, on):
    a0 = math.radians(n * 0.22)
    steel = mix((70, 82, 130), (210, 222, 255), on)
    for s in (-1, 1):
        poly(t, [(EX - 5, EY), (EX + 5, EY), (EX + s * 78, HORIZON), (EX + s * 52, HORIZON)], (96, 108, 160))
    rim = [(EX + ER * math.cos(k * math.tau / 60), EY + ER * math.sin(k * math.tau / 60)) for k in range(61)]
    line(t, rim, steel, 5)
    inner = [(EX + (ER - 16) * math.cos(k * math.tau / 60), EY + (ER - 16) * math.sin(k * math.tau / 60)) for k in range(61)]
    line(t, inner, steel, 2)
    for j in range(32):
        a = a0 + math.tau * j / 32
        end = (EX + ER * math.cos(a), EY + ER * math.sin(a))
        c = mix((60, 70, 120), (150, 170, 220), on)
        line(t, [(EX, EY), end], c, 1)
    for j in range(32):
        a = a0 + math.tau * j / 32
        c = mix((60, 70, 120), PODS[(j + n // 18) % 5], on)
        disc(t, EX + ER * math.cos(a), EY + ER * math.sin(a), 15, c)
    disc(t, EX, EY, 24, steel)

wheel(eye, 0, 0)

# embankment
box(art, -540, HORIZON - 30, 1080, 30, (10, 13, 32))
box(art, -540, HORIZON - 4, 1080, 4, (70, 76, 130))
LAMPS = [-520 + k * 40 for k in range(27)]
for x in LAMPS:
    line(art, [(x, HORIZON - 4), (x, HORIZON + 24)], (40, 46, 90), 2)
    disc(art, x, HORIZON + 28, 9, (60, 66, 110))

# animate
def lights(n):
    lit.clear()
    for x, y, w, h, on, live in LIGHTS:
        if live and n > on and (n + x + y) % 97 > 1:
            box(lit, x, y, w, h, WARM)
    if n > 12:
        for lx in LAMPS:
            disc(lit, lx, HORIZON + 28, 11, WARM)
    for r in range(1, 14):
        sy = HORIZON + r * 36 + 14
        half = 58 * (1 - (sy - HORIZON) / (390 - HORIZON))
        if n > 20 + r * 5:
            ends = [(SX - half + 8, sy), (SX + half - 8, sy)]
            line(lit, ends, (170, 200, 255), 3)
    if n % 50 < 25:
        disc(lit, SX, 440, 9, (255, 120, 110))

def double_decker(n):
    bus.clear()
    x = -760 + n * 3.8
    y = HORIZON - 18
    box(bus, x, y + 12, 190, 44, RED)
    box(bus, x + 8, y + 56, 174, 38, RED)
    box(bus, x + 4, y + 94, 182, 6, (130, 18, 28))
    for i in range(7):
        box(bus, x + 14 + i * 24, y + 62, 18, 22, WARM)
    for i in range(6):
        box(bus, x + 12 + i * 24, y + 22, 18, 20, WARM)
    box(bus, x + 150, y + 22, 30, 28, (255, 238, 200))
    for wx in (x + 40, x + 150):
        disc(bus, wx, y + 10, 28, (14, 14, 22))
        disc(bus, wx, y + 10, 12, (120, 120, 140))
    disc(bus, x + 190, y + 28, 10, CREAM)

SHOWS = [
    (240, 40, 250, GOLD),
    (256, -90, 330, (120, 230, 255)),
    (272, 330, 290, (255, 140, 210)),
    (288, -300, 250, GOLD),
    (304, 120, 340, CREAM),
]

def fireworks(n):
    fw.clear()
    for n0, x, y, c in SHOWS:
        t = n - n0
        if -18 < t <= 0:
            ry = HORIZON + (y - HORIZON) * (t + 18) / 18
            disc(fw, x, ry, 7, CREAM)
        if t < 0 or t > 80:
            continue
        fade = 1 - t / 80
        for k in range(40):
            a = math.tau * k / 40 + (k % 2) * 0.08
            v = (3.6 + (k % 3)) * 1.15
            for lag in (0, 4, 8):
                u = max(t - lag, 0)
                px = x + math.cos(a) * v * u
                py = y + math.sin(a) * v * u - 0.035 * u * u
                f = fade * (1 - lag / 14)
                disc(fw, px, py, 5 * f + 2, mix((60, 40, 90), c, f))

def twinkle(n):
    tw.clear()
    for k, (x, y, s) in enumerate(STARS[:34]):
        a = (math.sin(n / 7 + k * 1.7) + 1) / 2
        disc(tw, x, y, s + 1, mix(skyc(y), CREAM, a))

def ripple(n):
    wave.clear()
    for r in range(8):
        y = HORIZON - 50 - r * 34
        wave.goto(-540, y)
        wave.color(mix((120, 90, 160), (30, 34, 80), r / 8))
        wave.pendown()
        for x in range(-540, 541, 20):
            wave.goto(x, y + 5 * math.sin(x / 50 + n / 7 + r))
        wave.penup()

sc.update()
for n in range(390):
    twinkle(n)
    lights(n)
    hd.clear()
    clock(hd, n)
    eye.clear()
    wheel(eye, n, min(1, n / 40))
    double_decker(n)
    fireworks(n)
    ripple(n)
    sc.update()
    time.sleep(0.02)

turtle.done()