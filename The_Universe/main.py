import pygame
import math
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorlar System | Created with Python")

clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("arial", 32, bold=True)
planet_font = pygame.font.SysFont("arial", 15, bold=True)
credit_font = pygame.font.SysFont("arial", 22, bold=True)

# Color
BLACK = (4, 5, 20)
WHITE = (255, 255, 255)
CYAN = (0, 230, 255)
GOLD = (255, 200, 50)

# Solar System Center
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Background stars
stars = []

for _ in range(220):
    stars.append((
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ))

# Plante Information
planets = [
    {"name": "Mercury", "orbit": 65, "size": 5, "color": (180, 180, 180), "speed": 0.045},

    {"name": "Venus", "orbit": 100, "size": 8, "color": (255, 180, 80), "speed": 0.032},

    {"name": "Earth", "orbit": 140, "size": 9, "color": (50, 140, 255), "speed": 0.024},

    {"name": "Mars", "orbit": 180, "size": 7, "color": (255, 80, 60), "speed": 0.019},

    {"name": "Jupiter", "orbit": 225, "size": 15, "color": (230, 180, 130), "speed": 0.012},

    {"name": "Saturn", "orbit": 275, "size":13, "color": (240, 210, 130), "speed": 0.009},

    {"name": "Uranus", "orbit": 320, "size": 10, "color": (100, 230, 230), "speed": 0.006},

    {"name": "Neptune", "orbit": 355, "size": 10, "color": (70, 100, 255), "speed": 0.004},
]

angles = [random.uniform(0, math.tau) for _ in planets]

def draw_glow(surface, x, y, radius, color):
    """Draw a soft glowing circle."""
    for i in range(5, 0, -1):
        glow_radius = radius + i * 7
        alpha_surface = pygame.Surface(
            (glow_radius * 2, glow_radius * 2),
            pygame.SRCALPHA
        )

        alpha = max(8, 35 - i * 5)

        pygame.draw.circle(
            alpha_surface,
            (*color, alpha),
            (glow_radius, glow_radius),
            glow_radius
        )

        surface.blit(
            alpha_surface,
            (int(x - glow_radius), int(y - glow_radius))
        )

    pygame.draw.circle(
        surface,
        color,
        (int(x), int(y)),
        radius
    )
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(BLACK)

    # Draw Stars
    for x, y, size in stars:
        pygame.draw.circle(screen, WHITE, (x, y), size)

    # Title
    title = title_font.render(
        "SOLAR SYSTEM",
        True,
        CYAN
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 20)
    )

    # Draw orbit paths
    for planet in planets:
        pygame.draw.circle(
            screen,
            (35, 45, 75),
            (CENTER_X, CENTER_Y),
            planet["orbit"],
            1
        )
    
    # Draw glowing Sun
    draw_glow(
        screen,
        CENTER_X,
        CENTER_Y,
        25,
        GOLD
    )

    sun_label = planet_font.render(
        "SUN",
        True,
        GOLD
    )

    screen.blit(
        sun_label,
        (CENTER_X - sun_label.get_width() // 2, CENTER_Y + 34)
    )

    # Animate planets
    for i, planet in enumerate(planets):
        angles[i] += planet["speed"]

        x = CENTER_X + math.cos(angles[i]) * planet["orbit"]
        y = CENTER_Y + math.sin(angles[i]) * planet["orbit"]

        # Saturn rings
        if planet["name"] == "Saturn":
            pygame.draw.ellipse(
                screen,
                (210, 190, 130),
                (
                    int(x - planet["size"] * 1.8),
                    int(y - planet["size"] * 0.6),
                    planet["size"] * 3.6,
                    planet["size"] * 1.2
                ),
                2
            )
        
        # Planet glow and body
        draw_glow(
            screen,
            x,
            y,
            planet["size"],
            planet["color"]
        )

        # Planet name
        label = planet_font.render(
            planet["name"],
            True,
            WHITE
        )

        screen.blit(
            label,
            (
                int(x - label.get_width() // 2),
                int(y + planet["size"] + 8)
            )
        )
    
    # Creator credit
    credit = credit_font.render(
        "CREATED BY CAIQUE NOVAES",
        True,
        (0, 255, 170)
    )

    screen.blit(
        credit,
        (
            WIDTH // 2 - credit.get_width() // 2,
            HEIGHT - 42
        )
    )

    pygame.display.flip()
pygame.quit()