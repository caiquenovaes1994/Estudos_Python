import turtle, math, random, colorsys

# São Paulo à noite: Ponte Estaiada sobre o Rio Pinheiros, Copan, Banespa,
# Edifício Itália, MASP e as torres da Paulista, com garoa, trânsito na
# Marginal, trem da CPTM, helicópteros e réveillon na Paulista.

random.seed(55)
sc = turtle.Screen()
sc.setup(1080, 880)
sc.title("São Paulo at Night")
sc.colormode(255)
sc.bgcolor(8, 6, 22)
sc.tracer(0, 0)

RB = -130            # margem do rio (linha do reflexo)
HZ = -100            # base dos prédios / Marginal Pinheiros
NB = -380            # margem de cá (trilhos da CPTM)
GOLD = (255, 196, 108)
WARM = (255, 224, 150)
CREAM = (255, 240, 212)
SODIUM = (255, 158, 72)
RIVER = (32, 22, 58)
RED = (236, 44, 52)
EX = 60              # mastro da Ponte Estaiada
CROSS, TOP = 100, 310
LEGK = 50 / (CROSS - RB)
MX, MY = 250, 352    # lua


def pen():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.speed(0)
    t.setundobuffer(None)
    return t

def mix(a, b, k):
    k = min(max(k, 0), 1)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

def neon(h, s=0.6, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h % 1, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def poly(t, pts, c, refl=True):
    t.color(c)
    t.goto(pts[0])
    t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.end_fill()
    if refl and min(y for x, y in pts) >= RB - 3:
        poly(t, [(x, 2 * RB - y) for x, y in pts], mix(c, RIVER, 0.62), False)

def box(t, x, y, w, h, c, refl=True):
    poly(t, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], c, refl)

def wall(t, x, y, w, h, c, k=0.5):
    for j in range(4):
        box(t, x, y + h * j / 4, w, h / 4 + 1, mix(c, GOLD, k * (1 - j / 3) ** 1.5))

def disc(t, x, y, d, c):
    t.goto(x, y)
    t.dot(d, c)

def line(t, pts, c, w=2, refl=False):
    t.pensize(w)
    t.color(c)
    t.goto(pts[0])
    t.pendown()
    for p in pts[1:]:
        t.goto(p)
    t.penup()
    if refl:
        line(t, [(x, 2 * RB - y) for x, y in pts], mix(c, RIVER, 0.62), w)

def glow(t, x, y, r, c, bg, n=8):
    for i in range(n):
        disc(t, x, y, r * (n - i) / 2, mix(bg, c, i / (n - 1)))

def sky(y):
    k = min(max((440 - y) / (440 - RB), 0), 1)
    c = mix((6, 5, 22), (54, 32, 92), k * 1.35)
    return mix(c, (226, 118, 84), (k - 0.7) / 0.3)   # brilho alaranjado da cidade

def cloud(t, x, y, w, c):
    pts = [(x, y), (x + w * 0.2, y + 9), (x + w * 0.5, y + 13), (x + w * 0.8, y + 8),
           (x + w, y), (x + w * 0.75, y - 5), (x + w * 0.3, y - 6)]
    poly(t, pts, c, False)

def deck_y(x):
    return -40 - 60 * ((x - EX) / 280) ** 2

DECK = [(x, deck_y(x)) for x in range(EX - 280, EX + 281, 20)]

art = pen()

# céu poluído de luz
for i in range(72):
    y = 440 - (i + 1) * 8
    box(art, -540, y, 1080, 9, sky(y + 4), False)

# rio pinheiros
for i in range(32):
    y = RB - (i + 1) * 8
    box(art, -540, y, 1080, 9, mix((70, 40, 92), (8, 6, 22), i / 31), False)

# nuvens baixas iluminadas pela cidade
for i in range(9):
    x = random.randint(-560, 420)
    y = random.randint(60, 300)
    cloud(art, x, y, random.randint(160, 320), mix(sky(y), (210, 120, 130), 0.28))

# estrelas (poucas: é São Paulo)
TALL = [(-372, -308, 352), (-235, -165, 285), (380, 500, 362), (MX - 125, MX + 125, 480)]

def blocked(x, y):
    return any(a - 8 < x < b + 8 and y < top + 8 for a, b, top in TALL)

STARS = []
while len(STARS) < 46:
    x = random.randint(-530, 530)
    y = random.randint(190, 432)
    if not blocked(x, y):
        s = random.choice([2, 2, 3])
        STARS.append((x, y, s))
        disc(art, x, y, s, mix(sky(y), CREAM, 0.55))

# lua cheia atrás da névoa
glow(art, MX, MY, 70, (120, 100, 150), sky(MY), 7)
disc(art, MX, MY, 58, (250, 238, 214))
disc(art, MX - 10, MY + 8, 13, (232, 220, 198))
disc(art, MX + 12, MY - 7, 10, (236, 224, 202))
disc(art, MX + 4, MY + 15, 6, (236, 224, 202))
cloud(art, MX - 100, MY - 16, 210, mix(sky(MY), (200, 150, 170), 0.35))

# selva de pedra ao fundo
FAR = (52, 36, 84)
x = -560
while x < 560:
    w = random.randint(26, 56)
    h = random.randint(70, 175) + int(30 * math.sin(x / 140))
    box(art, x, RB, w, h + 30, FAR)
    for _ in range(w * h // 1300):
        wx = random.uniform(x + 3, x + w - 3)
        wy = random.uniform(HZ + 10, RB + h + 24)
        disc(art, wx, wy, 2, mix(FAR, GOLD, random.uniform(0.25, 0.6)))
    x += w - 3

# torres de TV da Paulista
AVI = []

def tvtower(cx, top, wb):
    st = (128, 104, 148)
    line(art, [(cx - wb, HZ), (cx - 4, top)], st, 2, True)
    line(art, [(cx + wb, HZ), (cx + 4, top)], st, 2, True)
    n = 12
    for i in range(n):
        y0 = HZ + (top - HZ) * i / n
        y1 = HZ + (top - HZ) * (i + 1) / n
        h0 = wb + (4 - wb) * i / n
        h1 = wb + (4 - wb) * (i + 1) / n
        line(art, [(cx - h0, y0), (cx + h1, y1)], st, 1)
        line(art, [(cx + h0, y0), (cx - h1, y1)], st, 1)
        line(art, [(cx - h1, y1), (cx + h1, y1)], st, 1)
    pf = HZ + (top - HZ) * 0.72
    box(art, cx - 14, pf, 28, 10, (70, 58, 96), False)
    line(art, [(cx, top), (cx, top + 30)], st, 2, True)
    AVI.append((cx, top + 30))
    AVI.append((cx - 14, pf + 12))
    AVI.append((cx + 14, pf + 12))

tvtower(412, 330, 26)
tvtower(478, 288, 20)

# prédios do meio com janelas que acendem
MID = (26, 20, 50)
LIGHTS = []
ROOF = []
x = -560
while x < 560:
    w = random.randint(38, 74)
    h = random.randint(110, 250)
    top = HZ + h
    c = mix(MID, (42, 32, 72), random.random())
    box(art, x, RB, w, top - RB, c)
    box(art, x + w - 6, RB, 6, top - RB, mix(c, (8, 6, 20), 0.5))
    if random.random() < 0.5:
        box(art, x + w * 0.3, top, w * 0.35, 9, c)
    for r in range((h - 40) // 16):
        for col in range((w - 8) // 12):
            wx, wy = x + 6 + col * 12, HZ + 34 + r * 16
            if random.random() < 0.55:
                box(art, wx, wy, 5, 7, mix(c, (70, 60, 110), 0.5), False)
                if random.random() < 0.5:
                    tone = random.choice([WARM, WARM, CREAM, (190, 220, 255)])
                    LIGHTS.append((wx, wy, random.randint(0, 150), tone))
    if random.random() < 0.6:
        line(art, [(x + w / 2, top), (x + w / 2, top + 12)], (80, 66, 110), 1)
        ROOF.append((x + w / 2, top + 12))
    x += w + random.randint(-3, 8)

# copan
def copan():
    x0, x1, top = -548, -398, 64
    box(art, x0, RB, x1 - x0, top - RB, (34, 28, 60))
    for i in range(15):
        k = 0.5 + 0.5 * math.sin((i - 3) / 2.2)
        box(art, x0 + i * 10, HZ, 10.5, top - HZ, mix((30, 26, 56), (124, 98, 122), k * 0.6))
    for y in range(HZ + 6, top, 7):
        line(art, [(x0, y), (x1, y)], (18, 14, 34), 2)
    for y in range(HZ + 9, top - 2, 7):
        for wx in range(x0 + 4, x1 - 3, 6):
            if random.random() < 0.2:
                disc(art, wx, y, 2, mix((60, 50, 80), WARM, random.uniform(0.5, 1)))
    box(art, x0 + 24, top, 46, 8, (40, 32, 66))
    AVI.append((x0 + 47, top + 12))

# banespa (edifício altino arantes)
def banespa(cx):
    ban = (58, 44, 84)
    tiers = [(110, HZ, 170), (80, 70, 80), (56, 150, 60), (36, 210, 40), (20, 250, 25)]
    for w, y, h in tiers:
        y0 = RB if y == HZ else y
        wall(art, cx - w / 2, y0, w, y + h - y0, ban, 0.55)
        for k in range(int(w // 10) - 1):
            xx = cx - w / 2 + 8 + k * 10
            line(art, [(xx, y + 6), (xx, y + h - 6)], mix(ban, WARM, 0.5), 2)
    poly(art, [(cx - 10, 275), (cx + 10, 275), (cx, 330)], mix(ban, GOLD, 0.3))
    line(art, [(cx, 330), (cx, 346)], CREAM, 2)
    AVI.append((cx, 348))

# edifício itália com o terraço no topo
def italia(cx):
    w, top = 64, 252
    ita = (30, 28, 58)
    box(art, cx - w / 2, RB, w, top - RB, ita)
    box(art, cx + w / 2 - 14, RB, 14, top - RB, (20, 18, 42))
    for r in range(HZ + 14, top - 22, 9):
        for col in range(6):
            if random.random() < 0.45:
                box(art, cx - w / 2 + 5 + col * 9, r, 5, 4, mix(ita, WARM, random.uniform(0.4, 0.9)), False)
    box(art, cx - w / 2 - 3, top - 16, w + 6, 16, (44, 40, 80))
    for col in range(8):
        box(art, cx - w / 2 + 1 + col * 8, top - 12, 5, 8, GOLD, False)
    box(art, cx - 12, top, 24, 10, (40, 36, 72))
    line(art, [(cx, top + 10), (cx, top + 30)], (120, 110, 150), 2)
    AVI.append((cx, top + 31))

# masp, suspenso nos pilares vermelhos
def masp():
    x0, x1 = 352, 500
    mred = (206, 34, 40)
    box(art, x0 + 10, HZ + 30, x1 - x0 - 20, 40, (24, 26, 44))
    for k in range(10):
        box(art, x0 + 16 + k * 13, HZ + 40, 9, 20, mix((24, 26, 44), (170, 210, 255), 0.55), False)
    box(art, x0, HZ + 70, x1 - x0, 12, mred)
    box(art, x0, RB, 12, HZ + 82 - RB, mred)
    box(art, x1 - 12, RB, 12, HZ + 82 - RB, mred)
    line(art, [(x0, HZ + 82), (x1, HZ + 82)], (255, 110, 100), 2)

copan()
banespa(-340)
italia(-200)
masp()

RECTS = [(-548, -398, 76), (-395, -285, 70), (-380, -300, 150), (-368, -312, 210),
         (-358, -322, 250), (-235, -165, 290), (352, 500, HZ + 84)]

def hidden(x, y):
    return any(a - 8 < x < b + 2 and y < top for a, b, top in RECTS)

LIGHTS = [L for L in LIGHTS if not hidden(L[0], L[1])]
AVI += [p for p in ROOF if not hidden(*p)]
AVI = [(x, y, random.randint(0, 47)) for x, y in AVI]
for ax, ay, _ in AVI:
    disc(art, ax, ay, 4, (110, 30, 46))

# marginal pinheiros
box(art, -540, RB, 1080, HZ - RB, (22, 18, 36), False)
for x in range(-540, 540, 30):
    line(art, [(x, (RB + HZ) / 2), (x + 14, (RB + HZ) / 2)], (110, 100, 124), 1)
line(art, [(-540, HZ), (540, HZ)], (64, 54, 86), 2)
line(art, [(-540, RB), (540, RB)], (80, 66, 110), 2)
for x in range(-520, 541, 60):
    line(art, [(x, HZ), (x, HZ + 24), (x + 8, HZ + 26)], (70, 60, 90), 2)
    glow(art, x + 8, HZ + 25, 10, SODIUM, (40, 30, 60), 4)

# margem de cá, trilhos da cptm
box(art, -540, -440, 1080, NB + 440, (14, 12, 26), False)
box(art, -540, NB - 4, 1080, 4, (60, 52, 90), False)
for x in range(-540, 541, 24):
    box(art, x, NB - 32, 14, 4, (40, 34, 56), False)
line(art, [(-540, NB - 26), (540, NB - 26)], (110, 104, 140), 2)
for x in range(-500, 541, 160):
    line(art, [(x, NB - 28), (x, NB + 42)], (60, 52, 84), 3)
    line(art, [(x, NB + 38), (x + 18, NB + 38)], (60, 52, 84), 2)
line(art, [(-540, NB + 34), (540, NB + 34)], (76, 66, 104), 1)

lit = pen()
bk = pen()
tw = pen()
av = pen()
rp = pen()
tr = pen()
br = pen()
tn = pen()
hp = pen()
fw = pen()
rn = pen()


def lights(n):
    # cada janela acende uma vez (desenho incremental, sem redesenhar tudo)
    for x, y, on, c in LIGHTS:
        if on == n:
            box(lit, x, y, 5, 7, c, False)

def blink(n):
    # alguns apartamentos apagam e acendem
    if n % 40 == 0:
        bk.clear()
        for i in range(10):
            x, y, on, c = LIGHTS[(n * 7 + i * 37) % len(LIGHTS)]
            if on < n:
                box(bk, x, y, 5, 7, (44, 36, 74), False)

def twinkle(n):
    tw.clear()
    for k, (x, y, s) in enumerate(STARS[::2]):
        a = (math.sin(n / 8 + k * 1.9) + 1) / 2
        disc(tw, x, y, s + 1, mix(sky(y), CREAM, a))

def aviation(n):
    av.clear()
    for x, y, ph in AVI:
        if (n + ph) % 48 < 16:
            disc(av, x, y, 12, mix(RED, (40, 20, 50), 0.55))
            disc(av, x, y, 6, (255, 80, 80))

def arm(y, s):
    return EX + s * LEGK * (y - CROSS)

def clip(p, q):
    # corta o reflexo na margem de cá (y = NB)
    if p[1] >= NB:
        return p
    k = (NB - q[1]) / (p[1] - q[1])
    return (q[0] + (p[0] - q[0]) * k, NB)

def bridge(n):
    br.clear()
    h0 = n / 260
    tint = neon(h0, 0.35)
    ym = 2 * RB - NB
    for s in (-1, 1):
        bx, tx = EX - s * 50, arm(TOP, s)
        mx = bx + (tx - bx) * (ym - RB) / (TOP - RB)
        c = mix((150, 146, 184), tint, 0.25) if s < 0 else mix((228, 224, 242), tint, 0.3)
        poly(br, [(bx - 7, RB), (bx + 7, RB), (tx + 4, TOP), (tx - 4, TOP)], c, False)
        poly(br, [(bx - 7, RB), (bx + 7, RB), (mx + 5, NB), (mx - 5, NB)], mix(c, RIVER, 0.62), False)
    for s in (-1, 1):
        for j in range(12):
            ay = 150 + j * 13
            ax = arm(ay, s)
            dx = EX + s * (40 + j * 21)
            dy = deck_y(dx)
            c = neon(h0 + j * 0.03)
            line(br, [(ax, ay), (dx, dy)], c, 2)
            sh = 3 * math.sin(n / 6 + j)
            a, b = (ax + sh, 2 * RB - ay), (dx, 2 * RB - dy)
            if b[1] > NB:
                line(br, [clip(a, b), b], mix(c, RIVER, 0.6), 2)
    poly(br, DECK + [(x, y - 9) for x, y in reversed(DECK)], (44, 38, 70))
    line(br, DECK, mix(WARM, tint, 0.3), 2)
    for x, y in DECK[1::2]:
        disc(br, x, y + 4, 5, WARM)
    for k in range(8):
        u = (n * 1.7 + k * 71) % 560
        x = EX - 280 + u if k % 2 else EX + 280 - u
        disc(br, x, deck_y(x) - 4, 4, CREAM if k % 2 else RED)
    on = n % 40 < 14
    for s in (-1, 1):
        disc(br, arm(TOP, s), TOP + 6, 7, (255, 70, 70) if on else (100, 30, 44))

CARS = [(random.uniform(0, 1240), random.uniform(2.4, 4.6), k % 2) for k in range(26)]

def traffic(n):
    tr.clear()
    for x0, v, lane in CARS:
        if lane == 0:
            x, y, d = (x0 + n * v) % 1240 - 620, HZ - 9, 1
        else:
            x, y, d = 620 - (x0 + n * v) % 1240, RB + 9, -1
        line(tr, [(x - d * 8, y), (x - d * 40, y)], (110, 40, 56), 3)
        disc(tr, x - d * 8, y, 5, RED)
        disc(tr, x, y, 7, CREAM)
        ry = 2 * RB - y
        line(tr, [(x, ry), (x, ry - 22)], mix(CREAM, RIVER, 0.6), 2)

def ripple(n):
    rp.clear()
    for j, x in enumerate(range(-520, 541, 40)):
        for i in range(6):
            y = RB - 44 - i * 28 - (j % 2) * 10
            w = 12 - i * 1.2 + 4 * math.sin(n / 7 + j * 1.3 + i)
            if abs(x - EX) < 170:
                c = mix(neon(n / 260 + j * 0.05), RIVER, 0.35 + i * 0.08)
            elif abs(x - MX) < 30:
                c = mix(CREAM, RIVER, 0.3 + i * 0.09)
            else:
                c = mix(SODIUM, RIVER, 0.5 + i * 0.07)
            line(rp, [(x - w, y), (x + w, y)], c, 2)

def train(n):
    tn.clear()
    x0 = (n * 7) % 2400 - 1400
    y = NB - 26
    for k in range(4):
        x = x0 + k * 168
        if x > 560 or x + 160 < -560:
            continue
        box(tn, x, y, 160, 40, (176, 182, 200), False)
        box(tn, x, y + 6, 160, 5, (214, 30, 46), False)
        box(tn, x, y + 36, 160, 4, (120, 124, 150), False)
        for q in range(6):
            box(tn, x + 10 + q * 25, y + 16, 16, 14, (220, 236, 255), False)
        line(tn, [(x + 60, y + 40), (x + 74, NB + 34), (x + 88, y + 40)], (90, 90, 120), 1)
    xf = x0 + 3 * 168 + 160
    if -560 < xf < 580:
        poly(tn, [(xf, y), (xf + 14, y + 4), (xf + 16, y + 24), (xf + 6, y + 40), (xf, y + 40)], (176, 182, 200), False)
        disc(tn, xf + 12, y + 10, 8, CREAM)
    if -560 < x0 < 560:
        disc(tn, x0 + 3, y + 10, 6, RED)

def helicopter(x, y, d, n):
    body = [(-22, 0), (-14, -8), (14, -7), (20, 0), (16, 8), (-10, 9)]
    poly(hp, [(x + d * bx, y + by) for bx, by in body], (26, 24, 42), False)
    box(hp, x - 16 if d < 0 else x + 8, y - 1, 8, 6, (150, 190, 230), False)
    line(hp, [(x - d * 16, y + 2), (x - d * 52, y + 6), (x - d * 56, y + 14)], (26, 24, 42), 3)
    line(hp, [(x - 14, y - 13), (x + 14, y - 13)], (70, 66, 96), 2)
    line(hp, [(x, y + 9), (x, y + 14)], (70, 66, 96), 2)
    r = 36 * abs(math.cos(n * 0.9))
    line(hp, [(x - r, y + 14), (x + r, y + 14)], (110, 106, 140), 2)
    if n % 20 < 6:
        disc(hp, x, y + 10, 7, (255, 70, 70))
    if n % 30 < 3:
        disc(hp, x - d * 54, y + 14, 6, (255, 255, 255))

def helis(n):
    hp.clear()
    x = 640 - n * 2.3
    if -640 < x < 640:
        helicopter(x, 236 + 8 * math.sin(n / 20), -1, n)
    x = -640 + (n - 150) * 2.8
    if -640 < x < 640:
        helicopter(x, 168 + 6 * math.sin(n / 17), 1, n)

DROPS = [(random.uniform(-560, 560), random.uniform(-450, 450), random.uniform(7, 11)) for _ in range(60)]

def garoa(n):
    rn.clear()
    count = int(len(DROPS) * max(0, 1 - n / 260))
    for x0, y0, v in DROPS[:count]:
        y = (y0 - n * v + 450) % 900 - 450
        x = (x0 - n * v * 0.25 + 560) % 1120 - 560
        line(rn, [(x, y), (x - 3, y - 12)], (120, 116, 160), 1)

SHOWS = [
    (290, 420, 300, GOLD),
    (306, -120, 340, (120, 220, 255)),
    (322, 260, 250, (255, 120, 190)),
    (338, -440, 300, CREAM),
    (354, 120, 380, (170, 255, 150)),
    (372, -280, 290, GOLD),
    (390, 460, 380, (255, 120, 120)),
    (404, -20, 260, (200, 160, 255)),
]

def fireworks(n):
    fw.clear()
    for n0, x, y, c in SHOWS:
        t = n - n0
        if -20 < t <= 0:
            ry = HZ + (y - HZ) * (t + 20) / 20
            disc(fw, x, ry, 6, CREAM)
        if t < 0 or t > 80:
            continue
        fade = 1 - t / 80
        for k in range(24):
            a = math.tau * k / 24 + (k % 2) * 0.1
            v = 3.4 + (k % 3) * 1.1
            for lag in (0, 6):
                u = max(t - lag, 0)
                px = x + math.cos(a) * v * u
                py = y + math.sin(a) * v * u - 0.035 * u * u
                f = fade * (1 - lag / 12)
                disc(fw, px, py, 5 * f + 2, mix((60, 40, 90), c, f))


# animação
sc.update()
for n in range(500):
    twinkle(n)
    lights(n)
    blink(n)
    aviation(n)
    if n % 2 == 0:
        ripple(n)
    traffic(n)
    bridge(n)
    train(n)
    helis(n)
    fireworks(n)
    garoa(n)
    sc.update()

turtle.done()
