import sys
import math
import random
import pygame
import numpy as np

# -------------------------------------------------------------
# Configuration & Pygame Initialization
# -------------------------------------------------------------
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Life Cycle Simulation")
clock = pygame.time.Clock()

CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Colors
GOLD = (255, 210, 65)
RED = (255, 60, 45)
WHITE = (255, 255, 255)
CYAN = (90, 200, 255)
DEEP_SPACE = (5, 6, 18)

# Fonts
font_title = pygame.font.SysFont("arial", 22, bold=True)
font_sub = pygame.font.SysFont("arial", 14)

# Global Animation State
life = 0.0
t = 0.0
flare_rays = []

# Background starfield
bg_stars = [
    (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(1.0, 2.5), random.uniform(0.4, 1.0))
    for _ in range(180)
]


# -------------------------------------------------------------
# Math & Easing Helpers
# -------------------------------------------------------------
def ease(x):
    """Smooth cubic ease-in-out curve clamped to [0, 1]."""
    x = max(0.0, min(1.0, float(x)))
    return x * x * (3.0 - 2.0 * x)


def smooth(val, edge, width=0.18):
    """Smoothstep threshold activation curve."""
    if val <= edge:
        return 0.0
    progress = (val - edge) / width
    progress = max(0.0, min(1.0, progress))
    return progress * progress * (3.0 - 2.0 * progress)


def mix(color_a, color_b, factor):
    """Interpolate smoothly between two RGB colors."""
    factor = max(0.0, min(1.0, factor))
    return tuple(int(a + (b - a) * factor) for a, b in zip(color_a, color_b))


# -------------------------------------------------------------
# Supernova Remnant / Particle Shell System
# -------------------------------------------------------------
class SupernovaShell:
    def __init__(self):
        self.particles = []
        self.blasted = False

    def blast(self, speed):
        """Discharge explosive matter once supernova threshold is triggered."""
        if speed > 0.05 and not self.blasted:
            self.blasted = True
            for _ in range(500):
                angle = random.uniform(0, 2 * math.pi)
                spd = random.uniform(speed * 25, speed * 65)
                self.particles.append({
                    "x": CENTER_X,
                    "y": CENTER_Y,
                    "vx": math.cos(angle) * spd,
                    "vy": math.sin(angle) * spd,
                    "life": 1.0,
                    "decay": random.uniform(0.15, 0.35),
                    "size": random.uniform(2.0, 4.5),
                    "color": random.choice([GOLD, RED, (255, 160, 50), (255, 240, 210), (180, 220, 255)])
                })

    def update(self, dt_seconds):
        for p in self.particles:
            p["x"] += p["vx"] * dt_seconds
            p["y"] += p["vy"] * dt_seconds
            p["life"] = max(0.0, p["life"] - p["decay"] * dt_seconds)

    def draw(self, surface):
        for p in self.particles:
            if p["life"] > 0:
                alpha_color = tuple(int(c * p["life"]) for c in p["color"])
                radius = max(1, int(p["size"] * p["life"]))
                pygame.draw.circle(surface, alpha_color, (int(p["x"]), int(p["y"])), radius)

    def reset(self):
        self.particles.clear()
        self.blasted = False


shell = SupernovaShell()


def rays(count, flare):
    """Generate dynamic solar corona rays radiating from the star."""
    if flare <= 0.001:
        return
    for i in range(count):
        angle = (i / count) * 2 * math.pi + t * 0.4 + (count * 0.12)
        pulsing_length = (70 + 40 * math.sin(t * 3.5 + i * 1.7)) * flare
        flare_rays.append((angle, pulsing_length, flare))


# -------------------------------------------------------------
# Star Life Stages
# -------------------------------------------------------------
def core(life):
    r = ease(life / 0.4) * 190
    a = np.linspace(0, 6.28, 900)
    return r * np.cos(a + t), r * np.sin(a)


def burn(life):
    flare_rays.clear()
    for ring in range(4):
        flare = smooth(life, 0.42 + ring * 0.04)
        rays(ring * 6 + 5, flare * 1.3)
    return flare_rays


def nova(life):
    swell = smooth(life, 0.75)
    colour = mix(GOLD, RED, swell)
    shell.blast(speed=9.8 * swell)
    return colour, swell


# -------------------------------------------------------------
# Renderer & HUD
# -------------------------------------------------------------
def get_stage_info(life_val):
    if life_val < 0.40:
        return "STAGE 1: PROTOSTAR ACCRETION", "Gravitational collapse forming the hot stellar core."
    elif life_val < 0.75:
        return "STAGE 2: MAIN SEQUENCE", "Stable hydrogen nuclear fusion & active corona flares."
    elif life_val < 0.95:
        return "STAGE 3: RED GIANT", "Hydrogen exhaustion; thermal expansion of outer layers."
    else:
        return "STAGE 4: SUPERNOVA EXPLOSION", "Cataclysmic core collapse & expanding nebula shell."


def draw(core_data, burn_data, nova_data):
    # 1. Background Stars
    for sx, sy, size, brightness in bg_stars:
        twinkle = 0.7 + 0.3 * math.sin(t * 2.0 + sx)
        col = int(255 * brightness * twinkle)
        pygame.draw.circle(screen, (col, col, col), (sx, sy), int(size))

    colour, swell = nova_data
    xs, ys = core_data

    # 2. Supernova Shell Shockwave Particles
    shell.draw(screen)

    # 3. Outer Glow / Red Giant Swell Aura
    base_radius = int(ease(life / 0.4) * (65 + 75 * swell))
    if base_radius > 2:
        glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Multi-layer glow
        glow_layers = 5
        for i in range(glow_layers, 0, -1):
            layer_r = int(base_radius * (1.0 + i * 0.35))
            alpha = int(35 / i)
            glow_color = (*colour, alpha)
            pygame.draw.circle(glow_surf, glow_color, (CENTER_X, CENTER_Y), layer_r)
        screen.blit(glow_surf, (0, 0))

    # 4. Solar Flares / Burn Rays
    if burn_data and base_radius > 5:
        for angle, length, flare_intensity in burn_data:
            start_x = CENTER_X + math.cos(angle) * (base_radius * 0.9)
            start_y = CENTER_Y + math.sin(angle) * (base_radius * 0.9)
            end_x = CENTER_X + math.cos(angle) * (base_radius + length)
            end_y = CENTER_Y + math.sin(angle) * (base_radius + length)
            ray_col = mix(colour, (255, 255, 200), 0.5)
            pygame.draw.line(screen, ray_col, (start_x, start_y), (end_x, end_y), max(1, int(2 * flare_intensity)))

    # 5. Dynamic Core Plasma Surface
    if len(xs) > 0 and base_radius > 1:
        # Scale and center points
        scale = (base_radius / 190.0) if base_radius > 0 else 0.0
        pts = [(int(CENTER_X + x * scale), int(CENTER_Y + y * scale)) for x, y in zip(xs, ys)]
        if len(pts) > 2:
            pygame.draw.polygon(screen, colour, pts)

        # Hot white center
        inner_r = max(1, int(base_radius * 0.35 * (1.0 - swell * 0.5)))
        pygame.draw.circle(screen, WHITE, (CENTER_X, CENTER_Y), inner_r)

    # 6. HUD / Status Display
    stage_title, stage_desc = get_stage_info(life)
    title_surf = font_title.render(stage_title, True, colour)
    desc_surf = font_sub.render(stage_desc, True, (200, 205, 220))
    time_surf = font_sub.render(f"Life Progress: {min(100.0, life * 100):.1f}%  |  Press SPACE to Reset", True, (160, 170, 190))

    screen.blit(title_surf, (30, 30))
    screen.blit(desc_surf, (30, 62))
    screen.blit(time_surf, (30, HEIGHT - 45))

    # Progress bar
    bar_w, bar_h = 320, 8
    pygame.draw.rect(screen, (40, 45, 60), (30, HEIGHT - 22, bar_w, bar_h), border_radius=4)
    filled_w = int(bar_w * min(1.0, life / 1.0))
    if filled_w > 0:
        pygame.draw.rect(screen, colour, (30, HEIGHT - 22, filled_w, bar_h), border_radius=4)


# -------------------------------------------------------------
# Main Simulation Loop
# -------------------------------------------------------------
def main():
    global life, t
    dt = 0.0

    while True:
        dt = clock.tick(60) / 1000.0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_r):
                    life = 0.0
                    shell.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        t += dt * 1.4
        life += dt / 29.0

        # Loop lifecycle after supernova remnant expands
        if life > 1.25:
            life = 0.0
            shell.reset()

        shell.update(dt)

        screen.fill(DEEP_SPACE)
        draw(core(life), burn(life), nova(life))
        pygame.display.flip()


if __name__ == "__main__":
    main()