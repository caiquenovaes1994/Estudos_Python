import turtle
import math
import random
import time

# --- Screen Setup ---
screen = turtle.Screen()
screen.setup(width=1000, height=850)
screen.bgcolor("#04010a")
screen.title("Blooming Heart")
screen.tracer(0)

# --- Dedicated Turtle Pens ---
bg_pen = turtle.Turtle()
lattice_pen = turtle.Turtle()
bloom_pen = turtle.Turtle()
halo_pen = turtle.Turtle()
text_pen = turtle.Turtle()

all_pens = [bg_pen, lattice_pen, bloom_pen, halo_pen, text_pen]
for pen in all_pens:
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

# --- Palette & Sacred Geometry Constants ---
SACRED_PALETTE = [
    "#ffe066", "#ffaa00", "#ff5500", "#ff0066", "#d400ff", "#8800ff", "#00e5ff", "#ffffff"
]

GOLDEN_ANGLE = math.radians(137.50776)
CENTER_Y = 35
BASE_SCALE = 16.0
TOTAL_SEEDS = 650

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        int(max(0, min(1, rgb[0])) * 255),
        int(max(0, min(1, rgb[1])) * 255),
        int(max(0, min(1, rgb[2])) * 255)
    )

def interpolate_palette(palette, t):
    t = max(0.0, min(1.0, t))
    pos = t * (len(palette) - 1)
    i0 = int(pos)
    i1 = min(i0 + 1, len(palette) - 1)
    frac = pos - i0
    c0 = hex_to_rgb(palette[i0])
    c1 = hex_to_rgb(palette[i1])
    r = c0[0] + (c1[0] - c0[0]) * frac
    g = c0[1] + (c1[1] - c0[1]) * frac
    b = c0[2] + (c1[2] - c0[2]) * frac
    return rgb_to_hex((r, g, b))

def parametric_heart(t):
    x = 16 * (math.sin(t) ** 3)
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, y

# --- Background Cosmic Dust ---
def draw_background():
    random.seed(137)
    star_colors = ["#1a0933", "#2c1050", "#481b7a", "#6b26ab", "#ffffff", "#ffe066"]
    for _ in range(160):
        x = random.randint(-490, 490)
        y = random.randint(-410, 410)
        dist = math.hypot(x, y - CENTER_Y)
        # Avoid cluttering the core of the heart
        if dist < 120 and random.random() < 0.65:
            continue
        c = random.choice(star_colors)
        sz = random.uniform(1.0, 2.6)
        bg_pen.goto(x, y)
        bg_pen.dot(sz, c)
        
        # Subtle cross flare on a few bright stars
        if random.random() < 0.08:
            bg_pen.pensize(1)
            bg_pen.pencolor(c)
            bg_pen.pendown()
            bg_pen.forward(sz * 1.8)
            bg_pen.backward(sz * 3.6)
            bg_pen.forward(sz * 1.8)
            bg_pen.left(90)
            bg_pen.forward(sz * 1.8)
            bg_pen.backward(sz * 3.6)
            bg_pen.forward(sz * 1.8)
            bg_pen.right(90)
            bg_pen.penup()

# --- Sacred Geometry Lattice (Cardioid Chords) ---
def draw_sacred_lattice():
    num_pts = 72
    pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i) / num_pts
        hx, hy = parametric_heart(angle)
        px = hx * BASE_SCALE
        py = hy * BASE_SCALE + CENTER_Y
        pts.append((px, py))

    lattice_pen.pensize(1)
    for i in range(num_pts):
        j = (i * 2) % num_pts
        p1 = pts[i]
        p2 = pts[j]
        ratio = (i / num_pts)
        c = interpolate_palette(["#2b0744", "#4f0f70", "#8800ff", "#2b0744"], ratio)
        lattice_pen.pencolor(c)
        lattice_pen.goto(p1)
        lattice_pen.pendown()
        lattice_pen.goto(p2)
        lattice_pen.penup()

# --- Generate Phyllotaxis Heart Particles ---
heart_particles = []
for i in range(TOTAL_SEEDS):
    r_ratio = math.sqrt(i / TOTAL_SEEDS)
    theta = i * GOLDEN_ANGLE
    t_angle = theta % (2 * math.pi)
    hx, hy = parametric_heart(t_angle)
    
    tx = hx * BASE_SCALE * r_ratio
    ty = hy * BASE_SCALE * r_ratio + CENTER_Y
    
    color = interpolate_palette(SACRED_PALETTE, r_ratio)
    glow_color = interpolate_palette(["#330066", "#8800ff", "#00e5ff"], r_ratio)
    
    # Seeds are larger towards the perimeter and varied
    dot_size = 2.4 + 2.8 * (r_ratio ** 1.3) + (1.2 if i % 9 == 0 else 0)
    
    heart_particles.append({
        "x": tx,
        "y": ty,
        "color": color,
        "glow": glow_color,
        "size": dot_size,
        "ratio": r_ratio
    })

# --- Draw Outer Glowing Aura Contour ---
def draw_outer_aura(scale_multiplier=1.0, alpha_color="#ff0066"):
    halo_pen.clear()
    halo_pen.pensize(1.5)
    
    for layer, (s_mult, color) in enumerate([
        (1.04 * scale_multiplier, "#440055"),
        (1.08 * scale_multiplier, "#770099"),
        (1.13 * scale_multiplier, "#aa00bb"),
        (1.19 * scale_multiplier, alpha_color)
    ]):
        halo_pen.pencolor(color)
        halo_pen.penup()
        for step in range(120):
            t = (2 * math.pi * step) / 120
            hx, hy = parametric_heart(t)
            x = hx * BASE_SCALE * s_mult
            y = hy * BASE_SCALE * s_mult + CENTER_Y
            if step == 0:
                halo_pen.goto(x, y)
                halo_pen.pendown()
            else:
                halo_pen.goto(x, y)
        halo_pen.penup()

# --- Elegant Title & Typography ---
def render_text():
    text_pen.penup()
    text_pen.goto(0, -350)
    text_pen.color("#ffe066")
    text_pen.write("✦ BLOOMING HEART ✦", align="center", font=("Courier", 16, "bold"))
    
    text_pen.goto(0, -378)
    text_pen.color("#b377ff")
    text_pen.write("Golden Ratio Phyllotaxis • Sacred Geometry", align="center", font=("Helvetica", 11, "italic"))

# --- Blooming Animation Sequence ---
def bloom_heart():
    draw_background()
    screen.update()
    
    draw_sacred_lattice()
    screen.update()
    
    draw_outer_aura(1.0, "#ff0066")
    render_text()
    screen.update()
    
    # Progressively bloom seeds from center outward in a golden spiral
    batch_size = 7
    for i, p in enumerate(heart_particles):
        bloom_pen.goto(p["x"], p["y"])
        # Outer glow
        bloom_pen.dot(p["size"] + 3.0, p["glow"])
        # Inner radiant seed
        bloom_pen.dot(p["size"], p["color"])
        
        # Highlight on edge seeds
        if p["ratio"] > 0.88 and i % 5 == 0:
            bloom_pen.dot(p["size"] * 0.45, "#ffffff")
            
        if (i + 1) % batch_size == 0 or i == TOTAL_SEEDS - 1:
            screen.update()
            time.sleep(0.008)

# --- Pulsating Heartbeat / Breathing Aura Loop ---
pulse_step = 0
def heartbeat_pulse():
    global pulse_step
    pulse_step += 1
    
    # Double-thump cardiac wave
    scale_wave = 1.0 + 0.04 * math.sin(pulse_step * 0.12) + 0.02 * math.sin(pulse_step * 0.24)
    aura_colors = ["#ff0066", "#d400ff", "#8800ff", "#00e5ff", "#ff5500"]
    c = aura_colors[(pulse_step // 8) % len(aura_colors)]
    
    draw_outer_aura(scale_wave, c)
    screen.update()
    
    screen.ontimer(heartbeat_pulse, 45)

# --- Run Application ---
bloom_heart()
heartbeat_pulse()
turtle.done()