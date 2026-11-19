import tkinter as tk

root = tk.Tk()
root.title("Moonrise")
root.geometry("800x600")

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

moon_y = 520

def animate():
    global moon_y
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 800, 600, fill="#101b3d", outline="")

    for x, y in [(100, 80), (180, 130), (300, 70), (520, 100), (680, 60), (740, 180)]:
        canvas.create_oval(x, y, x + 4, y + 4, fill="white", outline="")

    canvas.create_oval(340, moon_y - 60, 460, moon_y + 60, fill="#fff1a8", outline="")
    canvas.create_rectangle(0, 500, 800, 600, fill="#14291d", outline="")

    moon_y -= 0.7
    if moon_y < 250:
        moon_y = 520
    root.after(40, animate)

animate()
root.mainloop()