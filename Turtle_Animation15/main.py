import turtle, colorsys

t = turtle.Turtle();
t.hideturtle();
t.penup()

turtle.bgcolor("black");
turtle.colormode(1.0)

s, r, b, dt, N = 10, 28, 8 / 3, 0.008, 7000
x, y, z = 0.1, 0.0, 0.0
for i in range(N):
    dx, dy, dz = s * (y - x), x * (r - z) - y, x * y - b * z
    x, y, z = x + dx * dt, y + dy * dt, z + dz * dt
    t.color(colorsys.hsv_to_rgb(i / N, 1, 1))
    t.goto(x * 14, (z - 26) * 14);
    t.pendown()

turtle.done()