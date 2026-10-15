import turtle
import math
import random
import colorsys

screen = turtle.Screen()
screen.setup(width=1000, height=850)
screen.bgcolor("#03020c")
screen.title("Cosmic Tree")
screen.colormode(1.0)
screen.tracer(5)
t = turtle.Turtle()
t.hideturtle()
t.speed(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

def refresh(step, interval=4):
    if step % interval == 0:
        screen.update()

def get_hsv(h, s=0.85, v=1.0):
    return colorsys.hsv_to_rgb(h % 1.0, s, v)

random.seed(42)
num_stars = 200
star_hues = (0.55, 0.75, 0.90, 0.12, 0.30)

pen.penup()
for i in range(num_stars):
    x = random.randint(-490, 490)
    y = random.randint(-410, 410)
    pen.goto(x, y)
    
    hue = random.choice(star_hues)
    sat = random.uniform(0.15, 0.6)
    val = random.uniform(0.6, 1.0)
    pen.color(get_hsv(hue, sat, val))
    
    star_size = random.uniform(1.0, 2.8)
    pen.dot(star_size)

    if random.random() < 0.12:
        pen.pensize(1)
        pen.pendown()
        pen.forward(star_size * 2)
        pen.backward(star_size * 4)
        pen.forward(star_size * 2)
        pen.left(90)
        pen.forward(star_size * 2)
        pen.backward(star_size * 4)
        pen.forward(star_size * 2)
        pen.right(90)
        pen.penup()
        
    refresh(i, interval=6)

screen.update()

t.penup()
t.goto(0, -320)
for r_angle in [210, 235, 270, 305, 330]:
    t.goto(0, -320)
    t.setheading(r_angle)
    t.pendown()
    t.pensize(4)
    t.pencolor(get_hsv(0.65, 0.7, 0.6))
    for step in range(5):
        t.forward(random.randint(10, 18))
        t.right(random.randint(-15, 15))
        t.pensize(max(1, 4 - step * 0.7))
    t.penup()

screen.update()

step_count = 0

def draw_cosmic_tree(branch_len, angle, pensize_val, hue, depth):
    global step_count
    
    if branch_len < 13 or depth <= 0:
        t.color(get_hsv(hue, s=0.9, v=1.0))
        leaf_size = random.uniform(4.5, 9.0)
        t.dot(leaf_size)
        
        t.color(get_hsv(hue + 0.05, s=0.25, v=1.0))
        t.dot(leaf_size * 0.45)
        
        step_count += 1
        refresh(step_count, interval=3)
        return

    t.pensize(max(1.0, pensize_val))
    val = min(1.0, 0.5 + (9 - depth) * 0.06)
    t.pencolor(get_hsv(hue, s=0.8, v=val))
    
    t.pendown()
    t.forward(branch_len)
    
    step_count += 1
    refresh(step_count, interval=3)

    sub_len_left = branch_len * random.uniform(0.72, 0.81)
    sub_len_right = branch_len * random.uniform(0.72, 0.81)
    next_pensize = pensize_val * 0.72
    left_angle = angle + random.uniform(-4, 5)
    right_angle = angle + random.uniform(-4, 5)
    
    t.left(left_angle)
    draw_cosmic_tree(sub_len_left, angle * 0.94, next_pensize, hue + 0.035, depth - 1)
    
    if depth in (5, 6) and random.random() < 0.4:
        t.right(left_angle)
        draw_cosmic_tree(branch_len * 0.5, angle, next_pensize * 0.8, hue + 0.05, depth - 2)
        t.left(left_angle)
    
    t.right(left_angle + right_angle)
    draw_cosmic_tree(sub_len_right, angle * 0.94, next_pensize, hue + 0.07, depth - 1)
    
    t.left(right_angle)
    t.penup()
    t.backward(branch_len)

t.penup()
t.goto(0, -320)
t.setheading(90)
t.pendown()

draw_cosmic_tree(
    branch_len=115,
    angle=23,
    pensize_val=11,
    hue=0.55,
    depth=8
)

screen.update()
turtle.done()