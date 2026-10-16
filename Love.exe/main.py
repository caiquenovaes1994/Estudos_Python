import pygame
import math
import random
import sys

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
WIDTH, HEIGHT = 680, 950
FPS = 60

# Color Palettes (User can cycle with SPACE)
COLOR_PALETTES = [
    {
        "name": "Neon Violet (Original)",
        "glow": (180, 50, 255, 60),
        "outer": (185, 30, 255),
        "mid": (240, 130, 255),
        "core": (255, 235, 255),
        "title": (195, 150, 255),
        "title_glow": (140, 30, 235),
        "particles": [(210, 120, 255), (170, 70, 255), (255, 220, 255)],
    },
    {
        "name": "Romantic Pink",
        "glow": (255, 60, 150, 60),
        "outer": (255, 40, 120),
        "mid": (255, 140, 190),
        "core": (255, 240, 248),
        "title": (255, 160, 200),
        "title_glow": (220, 30, 100),
        "particles": [(255, 130, 180), (255, 70, 140), (255, 220, 240)],
    },
    {
        "name": "Cyber Cyan",
        "glow": (0, 200, 255, 60),
        "outer": (0, 150, 255),
        "mid": (100, 225, 255),
        "core": (230, 250, 255),
        "title": (140, 230, 255),
        "title_glow": (0, 130, 230),
        "particles": [(100, 220, 255), (0, 180, 240), (220, 250, 255)],
    },
    {
        "name": "Golden Glow",
        "glow": (255, 180, 40, 60),
        "outer": (255, 140, 20),
        "mid": (255, 215, 100),
        "core": (255, 250, 230),
        "title": (255, 220, 130),
        "title_glow": (220, 120, 20),
        "particles": [(255, 210, 110), (255, 160, 40), (255, 250, 220)],
    },
]

# Butterfly wing polygon coordinates (normalized)
UPPER_WING_PTS = [
    (0.05, -0.05), (0.25, -0.45), (0.55, -0.85), (0.85, -0.90),
    (1.00, -0.65), (0.95, -0.30), (0.70, -0.05), (0.40, 0.05), (0.10, 0.02)
]
LOWER_WING_PTS = [
    (0.08, 0.05), (0.35, 0.08), (0.65, 0.20), (0.75, 0.45),
    (0.60, 0.75), (0.35, 0.85), (0.15, 0.60), (0.05, 0.20)
]

CACHED_SIZES = [8, 11, 14, 18, 22, 26, 32, 40, 50, 65, 80]
FLAP_STEPS = 16


# ==========================================
# BUTTERFLY RENDERER & CACHE
# ==========================================
def render_butterfly_surface(size, flap, palette):
    """Renders a single butterfly with glowing wings and body."""
    pad = max(16, int(size * 1.6))
    surf = pygame.Surface((pad, pad), pygame.SRCALPHA)
    bcx, bcy = pad / 2.0, pad / 2.0
    s = size * 0.44

    def transform_pt(x, y, is_right):
        sx = x * flap
        return (bcx + sx if is_right else bcx - sx, bcy + y)

    # 1. Glow Layer (Additive)
    glow_col = palette["glow"]
    for is_right in (False, True):
        u_pts = [transform_pt(px * s, py * s, is_right) for px, py in UPPER_WING_PTS]
        l_pts = [transform_pt(px * s, py * s, is_right) for px, py in LOWER_WING_PTS]
        pygame.draw.polygon(surf, glow_col, u_pts)
        pygame.draw.polygon(surf, glow_col, l_pts)

    # 2. Outer Wings
    for is_right in (False, True):
        u_pts = [transform_pt(px * s, py * s, is_right) for px, py in UPPER_WING_PTS]
        l_pts = [transform_pt(px * s, py * s, is_right) for px, py in LOWER_WING_PTS]
        pygame.draw.polygon(surf, palette["outer"], u_pts)
        pygame.draw.polygon(surf, palette["outer"], l_pts)

        # 3. Mid Wings (Inner highlight)
        u_in = [transform_pt(px * s * 0.70 + 0.04 * s, py * s * 0.70 - 0.02 * s, is_right) for px, py in UPPER_WING_PTS]
        l_in = [transform_pt(px * s * 0.70 + 0.03 * s, py * s * 0.70 + 0.03 * s, is_right) for px, py in LOWER_WING_PTS]
        pygame.draw.polygon(surf, palette["mid"], u_in)
        pygame.draw.polygon(surf, palette["mid"], l_in)

        # 4. Core Brightness
        u_c = [transform_pt(px * s * 0.40 + 0.07 * s, py * s * 0.40 - 0.03 * s, is_right) for px, py in UPPER_WING_PTS]
        l_c = [transform_pt(px * s * 0.40 + 0.05 * s, py * s * 0.40 + 0.05 * s, is_right) for px, py in LOWER_WING_PTS]
        pygame.draw.polygon(surf, palette["core"], u_c)
        pygame.draw.polygon(surf, palette["core"], l_c)

    # 5. Body & Antennae
    bw = max(2, int(size * 0.045))
    bh = max(4, int(size * 0.38))
    pygame.draw.ellipse(surf, palette["core"], (int(bcx - bw / 2), int(bcy - bh * 0.4), bw, bh))

    ant_len = size * 0.22
    tip_l = (bcx - ant_len * 0.4 * flap, bcy - bh * 0.45 - ant_len * 0.6)
    tip_r = (bcx + ant_len * 0.4 * flap, bcy - bh * 0.45 - ant_len * 0.6)
    pygame.draw.line(surf, palette["mid"], (bcx, bcy - bh * 0.35), tip_l, max(1, int(size * 0.02)))
    pygame.draw.line(surf, palette["mid"], (bcx, bcy - bh * 0.35), tip_r, max(1, int(size * 0.02)))

    return surf


class ButterflyCache:
    """Caches pre-rendered butterflies for optimal 60+ FPS performance."""
    def __init__(self):
        self.caches = {}

    def build_for_palette(self, palette_idx):
        if palette_idx in self.caches:
            return
        palette = COLOR_PALETTES[palette_idx]
        cache = {}
        for sz in CACHED_SIZES:
            for f_idx in range(FLAP_STEPS):
                # Wing flap oscillates between 0.25 (closed) and 1.0 (open)
                flap = 0.22 + 0.78 * abs(math.cos(f_idx * math.pi / FLAP_STEPS))
                cache[(sz, f_idx)] = render_butterfly_surface(sz, flap, palette)
        self.caches[palette_idx] = cache

    def get(self, palette_idx, size, flap_phase, alpha=255):
        self.build_for_palette(palette_idx)
        cache = self.caches[palette_idx]

        # Closest size in cache
        best_sz = min(CACHED_SIZES, key=lambda s: abs(s - size))
        norm_phase = (flap_phase % (2 * math.pi)) / (2 * math.pi)
        f_idx = int(norm_phase * FLAP_STEPS) % FLAP_STEPS

        surf = cache[(best_sz, f_idx)]
        if alpha < 250:
            surf = surf.copy()
            surf.set_alpha(max(0, min(255, int(alpha))))
        return surf


# ==========================================
# MATHEMATICAL HEART CURVE
# ==========================================
def heart_coords(t, scale, cx, cy):
    """
    Standard parametric heart curve:
    x = 16 * sin^3(t)
    y = -(13*cos(t) - 5*cos(2t) - 2*cos(3t) - cos(4t))
    """
    x = 16.0 * (math.sin(t) ** 3)
    y = -(13.0 * math.cos(t) - 5.0 * math.cos(2.0 * t) - 2.0 * math.cos(3.0 * t) - math.cos(4.0 * t))
    return cx + x * scale, cy + (y - 1.0) * scale


# ==========================================
# PARTICLE & BURST SYSTEM
# ==========================================
class Particle:
    """Twinkling stardust drifting in the background."""
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.reset()
        self.y = random.uniform(0, h)

    def reset(self):
        self.x = random.uniform(0, self.w)
        self.y = self.h + random.uniform(5, 50)
        self.vy = random.uniform(-0.8, -0.3)
        self.vx = random.uniform(-0.3, 0.3)
        self.size = random.choice([1, 1, 2, 2, 3])
        self.phase = random.uniform(0, math.pi * 2)
        self.phase_speed = random.uniform(0.04, 0.08)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.phase += self.phase_speed
        if self.y < -10 or self.x < -10 or self.x > self.w + 10:
            self.reset()

    def draw(self, surf, palette):
        alpha = int(140 + 115 * math.sin(self.phase))
        if alpha <= 5:
            return
        col = random.choice(palette["particles"])
        p_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*col, alpha), (self.size, self.size), self.size)
        surf.blit(p_surf, (int(self.x) - self.size, int(self.y) - self.size), special_flags=pygame.BLEND_ADD)


class BurstButterfly:
    """Spawns upon user click and flutters outward gracefully."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(2.0, 5.5)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd - 1.2
        self.size = random.uniform(16, 28)
        self.flap_phase = random.uniform(0, 10)
        self.flap_speed = random.uniform(9.0, 15.0)
        self.life = 1.0
        self.decay = random.uniform(0.012, 0.022)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.97
        self.vy *= 0.97
        self.flap_phase += self.flap_speed * dt
        self.life -= self.decay

    def draw(self, surf, bfly_cache, palette_idx):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life ** 1.5))
        img = bfly_cache.get(palette_idx, int(self.size), self.flap_phase, alpha=alpha)
        surf.blit(img, (int(self.x - img.get_width() / 2), int(self.y - img.get_height() / 2)), special_flags=pygame.BLEND_ADD)


# ==========================================
# MAIN APPLICATION
# ==========================================
def main():
    pygame.init()
    pygame.font.init()

    # Setup display
    current_w, current_h = WIDTH, HEIGHT
    screen = pygame.display.set_mode((current_w, current_h), pygame.RESIZABLE)
    pygame.display.set_caption("Love.exe 🦋")
    clock = pygame.time.Clock()

    # Fonts
    title_font = pygame.font.SysFont(['segoeuiblack', 'arialblack', 'impact', 'trebuchetms', 'arial'], 54, bold=True)
    ui_font = pygame.font.SysFont(['segoeui', 'arial', 'tahoma'], 14)

    bfly_cache = ButterflyCache()
    palette_idx = 0
    bfly_cache.build_for_palette(palette_idx)

    # Ambient particles
    particles = [Particle(current_w, current_h) for _ in range(80)]
    bursts = []

    # Tunnel State
    NUM_HEART_RINGS = 6
    tunnel_progress = [i / NUM_HEART_RINGS for i in range(NUM_HEART_RINGS)]
    tunnel_speed = 0.22  # Cycles per second
    is_paused = False
    fullscreen = False

    time_elapsed = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if not is_paused:
            time_elapsed += dt

        cur_palette = COLOR_PALETTES[palette_idx]

        # --------------------------------------
        # EVENT HANDLING
        # --------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                current_w, current_h = event.w, event.h
                screen = pygame.display.set_mode((current_w, current_h), pygame.RESIZABLE)
                particles = [Particle(current_w, current_h) for _ in range(80)]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click burst
                    mx, my = event.pos
                    for _ in range(12):
                        bursts.append(BurstButterfly(mx, my))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    palette_idx = (palette_idx + 1) % len(COLOR_PALETTES)
                    bfly_cache.build_for_palette(palette_idx)
                elif event.key == pygame.K_UP:
                    tunnel_speed = min(1.2, tunnel_speed + 0.05)
                elif event.key == pygame.K_DOWN:
                    tunnel_speed = max(0.05, tunnel_speed - 0.05)
                elif event.key == pygame.K_p:
                    is_paused = not is_paused
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    current_w, current_h = screen.get_size()
                    particles = [Particle(current_w, current_h) for _ in range(80)]

        # --------------------------------------
        # UPDATE ANIMATIONS
        # --------------------------------------
        if not is_paused:
            for i in range(NUM_HEART_RINGS):
                tunnel_progress[i] = (tunnel_progress[i] + tunnel_speed * dt) % 1.0

        for p in particles:
            p.update()

        for b in bursts[:]:
            b.update(dt)
            if b.life <= 0:
                bursts.remove(b)

        # Dynamic Heart Center and Parallax tilt
        mx, my = pygame.mouse.get_pos()
        tilt_x = (mx - current_w / 2) * 0.04
        tilt_y = (my - current_h / 2) * 0.03

        # Base centers
        cx = current_w / 2 + tilt_x
        cy = current_h * 0.54 + tilt_y

        # Heartbeat pulse oscillation
        heartbeat = 1.0 + 0.04 * (math.sin(time_elapsed * 3.8) ** 4)

        # --------------------------------------
        # RENDERING
        # --------------------------------------
        # Deep dark background with subtle vignette tint
        screen.fill((3, 1, 8))

        # Ambient floating sparkles
        for p in particles:
            p.draw(screen, cur_palette)

        # --------------------------------------
        # 1. EXPANDING HEART TUNNEL
        # --------------------------------------
        # Sort rings so smaller ones are drawn inside / behind larger ones
        sorted_rings = sorted(enumerate(tunnel_progress), key=lambda x: x[1])

        for ring_idx, prog in sorted_rings:
            # Perspective zoom: progress^2 gives 3D depth acceleration
            scale = (0.5 + (prog ** 2.1) * 12.8) * heartbeat

            # Smooth alpha fade in near center and fade out near outer perimeter
            if prog < 0.15:
                ring_alpha = int(255 * (prog / 0.15))
            elif prog > 0.82:
                ring_alpha = int(255 * ((1.0 - prog) / 0.18))
            else:
                ring_alpha = 255

            if ring_alpha <= 5:
                continue

            # Number of butterflies on this heart ring
            count = max(8, int(scale * 2.9))
            bfly_size = max(8, int(scale * 2.6))

            for i in range(count):
                t = (2.0 * math.pi * i) / count
                hx, hy = heart_coords(t, scale, cx, cy)

                # Individual wing flapping offset
                flap_phase = time_elapsed * 8.0 + (i * 0.8) + (ring_idx * 1.5)
                bfly_img = bfly_cache.get(palette_idx, bfly_size, flap_phase, alpha=ring_alpha)

                bx = int(hx - bfly_img.get_width() / 2)
                by = int(hy - bfly_img.get_height() / 2)
                screen.blit(bfly_img, (bx, by), special_flags=pygame.BLEND_ADD)

        # --------------------------------------
        # 2. DISTINCTIVE SPINE & WING EXTENSIONS
        # (Faithfully reproducing the inspiration image layout)
        # --------------------------------------
        top_y_base = cy - 430 * (heartbeat * 0.9)
        spine_sway = math.sin(time_elapsed * 2.5) * 4.0

        # A. Top Column Butterflies (reaching towards Love.exe)
        top_spine = [
            (cx - 24 + spine_sway * 0.3, cy - 350, 30),  # Upper pair "X X"
            (cx + 24 + spine_sway * 0.3, cy - 350, 30),
            (cx + spine_sway * 0.5, cy - 290, 36),       # Center large butterfly
            (cx - 16, cy - 210, 26),
            (cx + 16, cy - 210, 26),
            (cx - 12, cy - 130, 24),
            (cx + 12, cy - 130, 24),
            (cx, cy - 40, 20),                           # Cleft center
        ]

        # B. Bottom Column Butterflies (descending from heart tip)
        bot_spine = [
            (cx, cy + 160, 26),
            (cx, cy + 235, 23),
            (cx, cy + 320, 21),
            (cx, cy + 380, 28),
        ]

        # C. Side Wing Flares (Horizontal arcs)
        wing_flares = [
            # Top-left wing arc
            (cx - 150, cy - 250, 28), (cx - 205, cy - 245, 26), (cx - 255, cy - 235, 24),
            # Top-right wing arc
            (cx + 150, cy - 250, 28), (cx + 205, cy - 245, 26), (cx + 255, cy - 235, 24),
            # Mid-side butterflies
            (cx - 95, cy - 215, 24), (cx + 95, cy - 215, 24),
            # Lower diagonal flares
            (cx - 230, cy + 170, 26), (cx + 230, cy + 170, 26),
            (cx - 135, cy + 280, 24), (cx + 135, cy + 280, 24),
        ]

        all_fixed_decorations = top_spine + bot_spine + wing_flares
        for idx, (fx, fy, fsz) in enumerate(all_fixed_decorations):
            # Scale with heartbeat
            dx = fx - cx
            dy = fy - cy
            cur_x = cx + dx * heartbeat
            cur_y = cy + dy * heartbeat

            # Floating micro-oscillation
            cur_y += math.sin(time_elapsed * 3.0 + idx * 0.5) * 3.0

            flap_phase = time_elapsed * 7.5 + idx * 0.9
            b_surf = bfly_cache.get(palette_idx, fsz, flap_phase, alpha=240)
            screen.blit(b_surf, (int(cur_x - b_surf.get_width() / 2), int(cur_y - b_surf.get_height() / 2)), special_flags=pygame.BLEND_ADD)

        # --------------------------------------
        # 3. INTERACTIVE BURSTS
        # --------------------------------------
        for b in bursts:
            b.draw(screen, bfly_cache, palette_idx)

        # --------------------------------------
        # 4. TITLE: "Love.exe 🦋"
        # --------------------------------------
        title_text = "Love.exe"
        title_x = int(current_w / 2 - 45)
        title_y = int(max(40, current_h * 0.08))

        # Neon Glow Effect for Title
        glow_offsets = [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]
        for ox, oy in glow_offsets:
            glow_surf = title_font.render(title_text, True, cur_palette["title_glow"])
            glow_rect = glow_surf.get_rect(center=(title_x + ox, title_y + oy))
            screen.blit(glow_surf, glow_rect)

        # Main Title Text
        main_title = title_font.render(title_text, True, cur_palette["title"])
        main_rect = main_title.get_rect(center=(title_x, title_y))
        screen.blit(main_title, main_rect)

        # Large Header Butterfly next to title (Tilted ~20 degrees, fluttering wings)
        header_flap = time_elapsed * 8.0
        large_bfly = bfly_cache.get(palette_idx, 75, header_flap, alpha=255)
        # Rotate butterfly ~22 degrees
        rot_bfly = pygame.transform.rotate(large_bfly, 22 + math.sin(time_elapsed * 2.0) * 4.0)
        bfly_x = main_rect.right + 25 - rot_bfly.get_width() // 2
        bfly_y = main_rect.centery - 10 - rot_bfly.get_height() // 2
        screen.blit(rot_bfly, (bfly_x, bfly_y), special_flags=pygame.BLEND_ADD)

        # --------------------------------------
        # 5. SUBTLE FOOTER HINT
        # --------------------------------------
        info_str = f"Theme: {cur_palette['name']} [SPACE] | Speed: {tunnel_speed:.2f}x [↑/↓] | Click to burst"
        info_surf = ui_font.render(info_str, True, (120, 80, 160))
        screen.blit(info_surf, (current_w // 2 - info_surf.get_width() // 2, current_h - 28))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()