import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 40)
T = 40
casas = [(x, y) for x in range(15) for y in range (10)]
minas = set(random.sample(casas, 22))
abertas = set()
bandeiras = set()
perdeu = False
cores = [None, "blue", "green4", "red", "navy", "maroon", "teal", "black", "gray"]

def vizinhas(c):
    lista = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            v = (c[0] + dx, c[1] + dy)
            if v in casas:
                lista.append(v)
    return lista

def numero(c):
    return len(minas.intersection(vizinhas(c)))

def abrir(c):
    fila = [c]
    while fila:
        c = fila.pop()
        if c in abertas or c in bandeiras:
            continue
        abertas.add(c)
        if numero(c) == 0 and c not in minas:
            fila += vizinhas(c)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        clicou = evento.type == pygame.MOUSEBUTTONDOWN
        if clicou and not perdeu:
            x, y = evento.pos
            c = (x // T, y // T)
            if evento.button == 3 and c not in abertas:
                bandeiras ^= {c}
            if evento.button == 1:
                abrir(c)
                perdeu = c in minas and c in abertas

    tela.fill("gray20")
    mouse = pygame.mouse.get_pos()
    for c in casas:
        r = pygame.Rect(c[0] * T, c[1] * T, T, T)
        r = r.inflate(-2, -2)
        if c in minas and perdeu:
            pygame.draw.rect(tela, "orange", r)
            pygame.draw.circle(tela, "black", r.center, 9)
        elif c in abertas:
            pygame.draw.rect(tela, "gainsboro", r)
            n = numero(c)
            if n:
                img = fonte.render(str(n), True, cores[n])
                pos = img.get_rect(center=r.center)
                tela.blit(img, pos)
        else:
            azul = "steelblue"
            if r.collidepoint(mouse):
                azul = "lightskyblue"
            pygame.draw.rect(tela, azul, r, 0 , 5)
            if c in bandeiras:
                x, y = r.center
                cabo = (x - 8, y - 13, 3, 26)
                pygame.draw.rect(tela, "black", cabo)
                p = [(x - 5, y - 13), (x + 11, y -6), (x - 5, y + 1)]
                pygame.draw.polygon(tela, "red", p)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()