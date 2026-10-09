import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont('Arial', 26, bold=True)
PECAS = [
    ([(0, 1), (1, 1), (2,1), (3,1)], "cyan"),
    ([(1, 0), (2, 0), (1, 1), (2, 1)], "yellow"),
    ([(1, 0), (0, 1), (1, 1), (2, 1)], "magenta"),
    ([(0, 0), (0, 1), (1, 1), (2, 1)], "royalblue"),
    ([(2, 0), (0, 1), (1, 1), (2, 1)], "orange"),
    ([(1, 0), (2, 0), (0, 1), (1, 1)], "limegreen"),
    ([(0, 0), (1, 0), (1, 1), (2, 1)], "red"),
]
grade = [[None] * 10 for _ in range(20)]

def nova_peca():
    blocos, cor = random.choice(PECAS)
    return blocos, cor, 3, 0

def livre(blocos, px, py):
    for x, y in blocos:
        gx, gy = px + x, py + y
        if not (0 <= gx < 10 and gy <20):
            return False
        if grade[gy][gx]:
            return False
    return True

def bloco(x, y, cor):
    r = (200 + x * 20, y * 20, 19, 19)
    pygame.draw.rect(tela, cor, r, 0, 3)

blocos, cor, px, py = nova_peca()
lados = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
queda = 0
pontos = 0
rodando = True
while rodando:
    agora = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            k = evento.key
            dx = lados.get(k, 0)
            if dx and livre(blocos, px + dx, py):
                px += dx
            if k == pygame.K_UP and cor != "yellow":
                girada = [(2 - y, x) for x, y in blocos]
                if livre(girada, px, py):
                    blocos = girada
            if k == pygame.K_SPACE:
                while livre(blocos, px, py + 1):
                    py += 1
                queda = 0

    if agora - queda > 500:
        queda = agora
        if livre(blocos, px, py + 1):
            py += 1
        else:
            for x, y in blocos:
                grade[py + y][px + x] = cor
            grade = [l for l in grade if None in l]
            cheias = 20 - len(grade)
            pontos += cheias * 100
            vazias = [[None] * 10 for _ in range(cheias)]
            grade = vazias + grade
            blocos, cor, px, py = nova_peca()
            if not livre(blocos, px, py):
                grade = [[None] * 10 for _ in range(20)]
                pontos = 0

    tela.fill((20, 20, 35))
    for y in range(20):
        for x in range(10):
            bloco(x, y, grade[y][x] or (40, 40, 60))
    for x, y in blocos:
        bloco(px + x, py + y, cor)
    placar = f"PONTOS {pontos}"
    texto = fonte.render(placar, True, "white")
    tela.blit(texto, (425, 30))
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()