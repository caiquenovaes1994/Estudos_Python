import math
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

N = 800
golden = math.pi * (3 - math.sqrt(5))
points = [(1.3 * math.sqrt(n) * math.cos(n * golden),
1.3 * math.sqrt(n) * math.sin(n * golden)) for n in range (N)]

plt.figure(figsize=(6, 6), facecolor="black")
ax = plt.gca()
ax.axis("off")
ax.set_aspect("equal")
ax.set_xlim(-78, 78)
ax.set_ylim(-78, 78)

for i in range(36):
    a = i * 2 * math.pi / 36
    ax.add_patch(Ellipse((55 * math.cos(a), 55 * math.sin(a)), 38, 13, angle=math.degrees(a), fc="gold", ec="orange", zorder=0))

    plt.pause(0.03)

dots = ax.scatter([], [], s=20, c=[], cmap="copper", vmin=0, vmax= 1.6 * N)
for n in range(10, N + 1, 10):
    dots.set_offsets(points[:n])
    dots.set_array(list(range(n)))
    plt.pause(0.01)

plt.show()