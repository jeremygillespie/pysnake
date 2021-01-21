import snake
from snake import point
import numpy as np

walls = np.full((10, 10), False, dtype=bool)
walls[0:5, 3] = True
walls[3:8, 6] = True
g = snake.printable(width=10, height=10, walls=walls)
g.occ[5:8, 1] = np.arange(3) + 1
print(g)
g.step(point(7, 2), point(7, 1), 3)
print(g)
g.step(point(8, 2), point(7, 2), 3)
print(g)
g.step(point(9, 2), point(8, 2), 3)
print(g)
g.step(point(9, 3), point(9, 2), 3)
print(g)
