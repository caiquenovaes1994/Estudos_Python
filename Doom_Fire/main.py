import random, time

W, H = 70, 24
fire = [[0] * W for _ in range(H)]
fire[-1] = [36] * W

# Limpa a tela e esconde o cursor
print("\033[2J\033[?25l", end="")

try:
    while True:
        for y in range(1, H):
            for x in range(W):
                k = random.randint(0, 3)
                fire[y - 1][(x - k + 1) % W] = max(0, fire[y][x] - k)

        out = []
        for row in fire:
            for v in row:
                r = min(255, v * 14)
                g = max(0, min(255, (v - 12) * 14))
                b = max(0, (v - 30) * 40)
                out.append(f"\033[48;2;{r};{g};{b}m ")
            out.append("\033[0m\n")

        print("\033[H" + "".join(out), end="", flush=True)
        time.sleep(0.04)
except KeyboardInterrupt:
    print("\033[0m\033[?25h\033[2J\033[H", end="")