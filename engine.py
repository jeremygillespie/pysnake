import snake
import numpy as np

occupied = np.full((10, 10), 0, dtype=int)

print(snake.output(occupied))
