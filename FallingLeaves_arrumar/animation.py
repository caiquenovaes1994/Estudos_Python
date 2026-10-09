import tkinter as tk
import random
import math

root = tk.Tk()
root.title("Falling Autumn Leaves")
root.geometry("800x600")
root.resizable(False, False)

canvas = tk.Canvas(root, width=800, height=600, bg="#183047")
canvas.pack()

leaves = []

colors = [
    "#ff7043",
    "#ff9800",
    "#fdd835",
    "#e53935",
    "#8d6e63"
]

for _ in range(90):
    leaves.append([
        random.randint(0, 800),
        random.randint(-600, 600),
        random.randint(5, 11),
        random.uniform(1.5, 4),
        random.uniform(0, 6.28),
        random.uniform(0.02, 0.06),
        random.choice(colors),
    ])

    def animate():
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 800, 600, fill="#182047", outline="")
        canvas.create_rectangle(0, 520, 80, 600,fill="#4e342e", outline="")

        for x in [80, 700]:
            canvas.create_rectangle(
                x - 12, 250,
                x + 90, 330,
                fill="#9e3d20",
                outline=""
            )
            canvas.create_oval(
            x - 90, 150,
            x + 90, 330,
            fill="#9e3d20",
            outline=""
            )
            canvas.create_oval(
                x - 120, 190,
                x + 40, 350,
                fill="#c75b25",
                outline=""
            )
        for leaf in leaves:
            x, y, size, speed, phase, wave, color = leaf
            leaf[1] += speed
            leaf[4] += wave
            leaf[0] += math.sin(leaf[4]) * 2.5

            if leaf[1] > 610:
                leaf[0] = random.randint(0, 800)
                leaf[1] = random.randint(-100, 20)
                leaf[2] = random.randint(5, 11)

            canvas.create_oval(
                x - size,
                y - size * 0.55,
                x + size,
                y + size * 0.55,
                fill=color,
                outline=""
            )

            canvas.create_line(
                x - size,
                y,
                x + size,
                y,
                fill="#6d2c1b",
                width=1
            )
    root.after(30, animate)
    animate()
    root.mainloop()