import turtle as tu

roo = tu.Turtle()
wn = tu.Screen()
wn.bgcolor("black")
wn.title("Fractal Tree Pattern")

roo.left(90)
roo.speed(2000)

# --- First Fractal Branch (Yellow) ---
def draw(l):
    if l < 10:
        return
    else:
        roo.pensize(2)
        roo.pencolor("yellow")
        roo.forward(l)
        roo.left(30)
        draw(3 * l / 4)
        roo.right(60)
        draw(3 * l / 4)
        roo.left(30)
        roo.pensize(2)
        roo.backward(l)

draw(20)

# --- Second Fractal Branch (Magenta) ---
roo.right(90)
roo.speed(2000)

def draw(l):
    if l < 10:
        return
    else:
        roo.pensize(2)
        roo.pencolor("magenta")
        roo.forward(l)
        roo.left(30)
        draw(3 * l / 4)
        roo.right(60)
        draw(3 * l / 4)
        roo.left(30)
        roo.pensize(2)
        roo.backward(l)

draw(20)

# --- Third Fractal Branch (Red) ---
roo.left(270)
roo.speed(2000)

def draw(l):
    if l < 10:
        return
    else:
        roo.pensize(2)
        roo.pencolor("red")
        roo.forward(l)
        roo.left(45)
        draw(l / 2)
        roo.right(90)
        draw(l / 2)
        roo.left(45)
        roo.pensize(2)
        roo.backward(l)

draw(20)

# --- Fourth Fractal Branch (Cyan) ---
roo.right(90)
roo.speed(2000)

def draw(l):
    if l < 10:
        return
    else:
        roo.pensize(2)
        roo.pencolor("cyan")
        roo.forward(l)
        roo.left(45)
        draw(l / 2)
        roo.right(90)
        draw(l / 2)
        roo.left(45)
        roo.pensize(2)
        roo.backward(l)

draw(20)

roo.hideturtle()
wn.exitonclick()