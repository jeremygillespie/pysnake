import snake
import numpy as np

walls = np.full((10, 10), False, dtype=bool)
walls[0:5, 3] = True
walls[3:8, 6] = True
g = snake.printable(width=10, height=10, walls=walls)
g.cor[g.cor_map[0, 0, 0]] = snake.cor_pos
g.cor[g.cor_map[3, 6, 0]] = snake.cor_neg
g.occ[3:8, 1] = np.arange(5) + 1
print(g)
