import turtle as t
import math
import random
import time

SCALE = 10
WIDTH, HEIGHT = 900, 900
BACKGROUND = "#000000"
CENTER_X, CENTER_Y = 0, -8
SEED = 27
DRAW_DELAY = 0.008
FPS_DELAY = 0.025
FLAP_SPEED = 0.055
MIN_WING_WIDTH = 0.34

random.seed(SEED)
screen = t.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Silver Butterfly")
screen.bgcolor(BACKGROUND)
screen.tracer(0)
canvas = screen.getcanvas()

pen = t.Turtle(visible=False)
pen.speed(0)
pen.penup()

wing_items = {}

def gray(value):
    value = max(0, min(255, int(value)))
    return f"#{value:02x}{value:02x}{value:02x}"

def cubic_point(p0, p1, p2, p3, u):
    v = 1.0 - u
    x = v ** 3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * p3[0]
    y = v ** 3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * p3[1]
    return x, y

def transform_segments(local_segments, side):
    return [[(CENTER_X + side * x, CENTER_Y + y) for x, y in segment]
            for segment in local_segments]

UPPER_WING = [
    ((0, 0), (5.8, 15.5), (21.5, 38), (37.5, 40)),
    ((37.5, 40), (38.5, 28.5), (31, 3.5), (23, 0)),
    ((23, 0), (15, 0.7), (5.5, -0.1), (0, 0))
]

LOWER_WING = [
    ((0, 0), (6.5, -0.1), (17, 0.8), (23.5, -1.4)),
    ((23.5, -1.4), (25, -10.5), (17, -30), (10.5, -30)),
    ((10.5, -30), (4.5, -29), (0.8, -9), (0, 0))
]

def make_boundary(segments, samples_per_curve=100):
    boundary = []
    for index, (p0, p1, p2, p3) in enumerate(segments):
        for i in range(0 if index == 0 else 1, samples_per_curve + 1):
            boundary.append(cubic_point(p0, p1, p2, p3, i / samples_per_curve))
    return boundary

def fill_wing(boundary):
    pen.penup()
    pen.goto(boundary[0][0] * SCALE, boundary[0][1] * SCALE)
    pen.pencolor("#151515")
    pen.fillcolor("#101010")
    pen.pensize(1)
    pen.begin_fill()
    pen.pendown()
    for x, y in boundary[1:]:
        pen.goto(x * SCALE, y * SCALE)
    pen.goto(boundary[0][0] * SCALE, boundary[0][1] * SCALE)
    pen.end_fill()
    pen.penup()

def draw_strand(start, end, side, steps=19):
    sx = start[0] + random.uniform(-0.045, 0.045)
    sy = start[1] + random.uniform(-0.045, 0.045)
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    bend = (abs(dy) * random.uniform(0.015, 0.065) + abs(dx) * random.uniform(0.008, 0.030)) * side
    c1 = (sx + dx * 0.24 + bend * 0.20, sy + dy * 0.34)
    c2 = (sx + dx * 0.72 + bend, sy + dy * 0.82)

    shade = random.randint(38, 100)
    chance = random.random()
    if chance < 0.055:
        shade = random.randint(112, 158)
    elif chance < 0.13:
        shade = random.randint(82, 125)

    pen.pencolor(gray(shade))
    pen.pensize(random.choice((0.45, 0.55, 0.65, 0.75, 0.85)))
    pen.penup()
    pen.goto(sx * SCALE, sy * SCALE)
    pen.pendown()
    for step in range(1, steps + 1):
        x, y = cubic_point((sx, sy), c1, c2, (ex, ey), step / steps)
        pen.goto(x * SCALE, y * SCALE)
    pen.penup()

def draw_wing(side, is_upper):
    side_mult = 1 if side in ("right", 1) else -1
    local = UPPER_WING if is_upper else LOWER_WING
    segments = transform_segments(local, side_mult)
    before = set(canvas.find_all())
    boundary = make_boundary(segments)
    fill_wing(boundary)

    counts = (190, 220, 130) if is_upper else (155, 170, 110)
    start = (CENTER_X, CENTER_Y)
    strands_done = 0

    for segment, count in zip(segments, counts):
        p0, p1, p2, p3 = segment
        for i in range(1, count + 1):
            endpoint = cubic_point(p0, p1, p2, p3, i / count)
            draw_strand(start, endpoint, side_mult)
            strands_done += 1
            if strands_done % 5 == 0:
                screen.update()
            time.sleep(DRAW_DELAY)
    
    edge_shades = (139, 94, 72) if is_upper else (122, 94, 81)
    edge_widths = (1.25, 1.05, 0.90)
    for segment, shade, width in zip(segments, edge_shades, edge_widths):
        p0, p1, p2, p3 = segment
        pen.pencolor(gray(shade))
        pen.pensize(width)
        pen.goto(p0[0] * SCALE, p0[1] * SCALE)
        pen.pendown()
        for i in range(1, 111):
            x, y = cubic_point(p0, p1, p2, p3, i / 110)
            pen.goto(x * SCALE, y * SCALE)
        pen.penup()

    screen.update()
    after = set(canvas.find_all())
    wing_items[(side, is_upper)] = sorted(after - before)

def draw_center_glow():
    before = set(canvas.find_all())
    pen.penup()
    pen.goto(CENTER_X * SCALE, CENTER_Y * SCALE)
    for size, colour in [(21, "#181818"), (16, "#2c2c2c"), (11, "#515151"), (7, "#858585"), (4, "#c5c5c5"), (2, "#ffffff")]:
        pen.dot(size, colour)

    for i in range(24):
        angle = 2 * math.pi * i / 24
        length = random.uniform(0.35, 0.9)
        x2 = CENTER_X + math.cos(angle) * length
        y2 = CENTER_Y + math.sin(angle) * length
        pen.pencolor(gray(random.randint(95, 175)))
        pen.pensize(random.choice((0.5, 0.7, 0.9)))
        pen.goto(CENTER_X * SCALE, CENTER_Y * SCALE)
        pen.pendown()
        pen.goto(x2 * SCALE, y2 * SCALE)
        pen.penup()
    after = set(canvas.find_all())
    wing_items[("center", None)] = sorted(after - before)

def animate_flap():
    center_canvas_x = WIDTH / 2 + CENTER_X * SCALE
    center_canvas_y = HEIGHT / 2 - CENTER_Y * SCALE
    current_factor = 1.0
    phase = 0.0

    while True:
        phase += FLAP_SPEED
        factor = MIN_WING_WIDTH + (1 - MIN_WING_WIDTH) * (0.5 + 0.5 * math.cos(phase))
        ratio = factor / current_factor

        for (side, is_upper), items in wing_items.items():
            anchor_x = center_canvas_x
            for item_id in items:
                try:
                    canvas.scale(item_id, anchor_x, center_canvas_y, ratio, 1.0)
                except Exception:
                    pass

        current_factor = factor
        screen.update()
        time.sleep(FPS_DELAY)

if __name__ == "__main__":
    draw_center_glow()
    draw_wing("right", True)
    draw_wing("right", False)
    draw_wing("left", True)
    draw_wing("left", False)

    screen.tracer(True)
    try:
        animate_flap()
    except t.Terminator:
        pass
    screen.mainloop()