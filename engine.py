import snake
import numpy as np

g = snake.occupied_corners()
print(g)
print(g.cor)
print(g.cor_map)
print(g.cor[g.cor_map])
print(g.cor[g.cor_map[0, 1]])
