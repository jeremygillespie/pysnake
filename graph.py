import numpy as np

north = (0, 1)
south = (0, -1)
east = (1, 0)
west = (-1, 0)


def offset(a, b):
    return tuple(np.array(a) + np.array(b))


class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.occupied = np.zeros((width, height))
        self.head = (0, 0)
