import pygame

pygame.init()

W, H = 980, 620
tela = pygame.display.set_mode((W, H))

pygame.display.set_caption("Urna Eletrônica em Python")

clock = pygame.time.Clock()

BG = (8, 11, 16)
PAINEL = (243, 245, 248)
TECLA = (31, 36, 44)
BRANCO = (248, 250, 252)
TEXTO = (20, 24, 30)
CINZA = (125, 135, 150)
VERDE = (48, 190, 110)
LARANJA = (247, 145, 55)
VERMELHO = (225, 70, 70)
AZUL = (40, 100, 220)
PRETO = (0, 0, 0)

f1 = pygame.font.SysFont("segoeui", 24, bold=True)
f2 = pygame.font.SysFont("segoeui", 18, bold=True)
f3 = pygame.font.SysFont("segoeui", 38, bold=True)
f4 = pygame.font.SysFont("segoeui", 30, bold=True)

candidatos = {
    "13": (
        "LUIS INACIO LULA\nDA SILVA",
        "PT",
        VERMELHO,
        BRANCO
    ),
    "14": (
        "RENAN SANTOS",
        "MISSAO",
        (255, 255, 0),
        PRETO
    ),
    "22": (
        "FLAVIO BOLSONARO",
        "PL",
        AZUL,
        BRANCO
    )
}

digitado = ""
mensagem = ""
fim = False
fim_ate = 0


def escrever(
    txt,
    fonte,
    cor,
    x,
    y,
    centro=False
):
    linhas = str(txt).split("\n")
    altura_linha = fonte.get_linesize()
    offset_y = ((len(linhas) - 1) * altura_linha) / 2 if centro else 0

    for i, linha in enumerate(linhas):
        img = fonte.render(
            linha,
            True,
            cor
        )

        pos_y = y - offset_y + i * altura_linha

        if centro:
            rect = img.get_rect(
                center=(x, int(pos_y))
            )
        else:
            rect = img.get_rect(
                topleft=(x, int(pos_y))
            )

        tela.blit(
            img,
            rect
        )


def botao(
    rect,
    label,
    cor
):
    pygame.draw.rect(
        tela,
        cor,
        rect,
        border_radius=12
    )

    cor_texto = (
        TEXTO
        if cor == BRANCO
        else BRANCO
    )

    escrever(
        label,
        f2,
        cor_texto,
        rect.centerx,
        rect.centery,
        True
    )


teclas = []

for i, numero in enumerate(
    "123456789"
):
    x = 690 + (i % 3) * 82
    y = 150 + (i // 3) * 72

    teclas.append(
        (
            pygame.Rect(
                x, y, 66, 56
            ),
            numero
        )
    )

teclas.append(
    (
        pygame.Rect(
            772, 366, 66, 56
        ),
        "0"
    )
)

b_branco = pygame.Rect(
    650, 455, 92, 58
)

b_corrige = pygame.Rect(
    750, 455, 92, 58
)

b_confirma = pygame.Rect(
    850, 455, 108, 68
)

rodando = True

while rodando:
    agora = pygame.time.get_ticks()

    if fim and agora >= fim_ate:
        fim = False
        digitado = ""
        mensagem = ""

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if (
            evento.type == pygame.KEYDOWN
            and not fim
        ):
            if (
                evento.unicode.isdigit()
                and len(digitado) < 2
                and not mensagem
            ):
                digitado += evento.unicode

            elif evento.key == pygame.K_ESCAPE:
                digitado = ""
                mensagem = ""

            elif evento.key == pygame.K_b:
                digitado = ""
                mensagem = "VOTO EM BRANCO"

            elif evento.key == pygame.K_RETURN:
                fim = True
                fim_ate = agora + 1500

        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and not fim
        ):
            for rect, numero in teclas:
                if (
                    rect.collidepoint(
                        evento.pos
                    )
                    and len(digitado) < 2
                    and not mensagem
                ):
                    digitado += numero

            if b_branco.collidepoint(
                evento.pos
            ):
                digitado = ""
                mensagem = "VOTO EM BRANCO"

            if b_corrige.collidepoint(
                evento.pos
            ):
                digitado = ""
                mensagem = ""

            if b_confirma.collidepoint(
                evento.pos
            ):
                fim = True
                fim_ate = agora + 1500

    tela.fill(BG)

    escrever(
        "URNA ELETRONICA EM PYTHON",
        f1,
        BRANCO,
        38,
        24
    )

    escrever(
        "TREINO EM PYTHON",
        f2,
        CINZA,
        40,
        58
    )

    pygame.draw.rect(
        tela,
        PAINEL,
        (40, 100, 560, 470),
        border_radius=18
    )

    pygame.draw.rect(
        tela,
        (20, 24, 31),
        (630, 100, 310, 470),
        border_radius=18
    )

    if fim:
        fonte_fim = pygame.font.SysFont(
            "segoeui",
            86,
            bold=True
        )

        escrever(
            "FIM",
            fonte_fim,
            TEXTO,
            320,
            310,
            True
        )

    else:
        escrever(
            "SEU VOTO PARA",
            f2,
            CINZA,
            75,
            135
        )

        escrever(
            "PRESIDENTE // SIMULACAO",
            f1,
            TEXTO,
            75,
            170
        )

        escrever(
            "NUMERO",
            f2,
            CINZA,
            75,
            225
        )

        for i in range(2):
            caixa = pygame.Rect(
                75 + i * 70,
                255,
                58,
                66
            )

            pygame.draw.rect(
                tela,
                CINZA,
                caixa,
                2,
                border_radius=8
            )

            if i < len(digitado):
                escrever(
                    digitado[i],
                    f3,
                    TEXTO,
                    caixa.centerx,
                    caixa.centery,
                    True
                )

        if mensagem:
            escrever(
                mensagem,
                f4,
                TEXTO,
                75,
                360
            )

        elif (
            len(digitado) == 2
            and digitado in candidatos
        ):
            dados = candidatos[digitado]
            nome, sigla, cor = dados[0], dados[1], dados[2]
            cor_sigla = dados[3] if len(dados) > 3 else BRANCO

            pygame.draw.circle(
                tela,
                cor,
                (465, 315),
                62
            )

            escrever(
                sigla,
                f1,
                cor_sigla,
                465,
                315,
                True
            )

            escrever(
                nome,
                f4,
                TEXTO,
                75,
                360
            )

        elif len(digitado) == 2:
            escrever(
                "VOTO NULO",
                f4,
                LARANJA,
                75,
                360
            )

        else:
            escrever(
                "Digite 13, 14 ou 22 para testar",
                f2,
                CINZA,
                75,
                360
            )

    for rect, numero in teclas:
        botao(
            rect,
            numero,
            TECLA
        )

    botao(
        b_branco,
        "BRANCO",
        BRANCO
    )

    botao(
        b_corrige,
        "CORRIGE",
        LARANJA
    )

    botao(
        b_confirma,
        "CONFIRMA",
        VERDE
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()